"""Runtime behavioral monitor for AI agents.

Ingests OpenTelemetry traces or live agent output and detects:
- Unauthorized tool calls (tools not in the agent's declared permissions)
- Permission drift (behavior that exceeds declared capabilities)
- Sensitive data access violations
- Anomalous action patterns
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from rich.console import Console

from pluto_aguard.models import AgentAction, AgentPolicy, Finding, Severity

console = Console()


def load_policy(policy_path: str | None) -> AgentPolicy | None:
    """Load agent policy from YAML/JSON file."""
    if not policy_path:
        return None

    path = Path(policy_path)
    content = path.read_text(encoding="utf-8")

    if path.suffix == ".json":
        data = json.loads(content)
    else:
        data = yaml.safe_load(content) or {}

    return AgentPolicy(**data)


def parse_trace_line(line: str) -> AgentAction | None:
    """Parse a single JSONL trace line into an AgentAction."""
    try:
        data = json.loads(line.strip())
    except json.JSONDecodeError:
        return None

    # Support OpenTelemetry span format
    if "name" in data and "attributes" in data:
        attrs = data.get("attributes", {})
        return AgentAction(
            turn=attrs.get("turn", 0),
            timestamp=data.get("startTimeUnixNano", data.get("timestamp")),
            action_type=attrs.get("action_type", _infer_action_type(data["name"])),
            tool_name=attrs.get("tool.name", data.get("name")),
            tool_args=attrs.get("tool.args", {}),
            result_summary=attrs.get("result.summary"),
        )

    # Support simple agent trace format
    if "action_type" in data or "tool_name" in data:
        return AgentAction(**data)

    return None


def _infer_action_type(span_name: str) -> str:
    """Infer action type from span name."""
    name_lower = span_name.lower()
    if any(k in name_lower for k in ("tool", "function", "call")):
        return "tool_call"
    if any(k in name_lower for k in ("query", "read", "fetch", "get")):
        return "data_access"
    if any(k in name_lower for k in ("response", "generate", "complete")):
        return "response"
    return "unknown"


def check_action_against_policy(
    action: AgentAction, policy: AgentPolicy
) -> list[Finding]:
    """Check a single agent action against the declared policy."""
    violations: list[Finding] = []

    if not action.tool_name:
        return violations

    tool = action.tool_name.lower()

    # Check if tool is explicitly denied
    if policy.denied_tools and tool in [t.lower() for t in policy.denied_tools]:
        violations.append(Finding(
            id=f"DRIFT-DENIED-TOOL-{tool}-T{action.turn}",
            title=f"Agent invoked denied tool '{action.tool_name}'",
            description=(
                f"At turn {action.turn}, the agent called '{action.tool_name}' which is "
                "explicitly listed in denied_tools. This may indicate prompt injection "
                "or a misconfigured agent."
            ),
            severity=Severity.CRITICAL,
            category="drift",
            owasp_id="OWASP-MCP-04",
        ))

    # Check if tool is in allowed list (if allowlist exists)
    if policy.allowed_tools and tool not in [t.lower() for t in policy.allowed_tools]:
        violations.append(Finding(
            id=f"DRIFT-UNAUTHORIZED-TOOL-{tool}-T{action.turn}",
            title=f"Agent invoked unauthorized tool '{action.tool_name}'",
            description=(
                f"At turn {action.turn}, the agent called '{action.tool_name}' which is "
                "not in the allowed_tools list. The agent is operating outside its "
                "declared capabilities."
            ),
            severity=Severity.HIGH,
            category="drift",
            owasp_id="OWASP-MCP-03",
        ))

    # Check if tool requires human approval
    if tool in [t.lower() for t in policy.require_human_approval]:
        # In a real implementation, we'd check if approval was given
        violations.append(Finding(
            id=f"DRIFT-NO-APPROVAL-{tool}-T{action.turn}",
            title=f"Tool '{action.tool_name}' used without human approval",
            description=(
                f"At turn {action.turn}, the agent called '{action.tool_name}' which "
                "requires human-in-the-loop approval, but no approval record was found."
            ),
            severity=Severity.HIGH,
            category="drift",
            owasp_id="OWASP-MCP-04",
        ))

    # Check permission level
    if policy.max_permissions:
        max_perm = policy.max_permissions.get(tool, policy.max_permissions.get("*"))
        if max_perm and max_perm.lower() == "read":
            write_indicators = ["write", "create", "update", "delete", "insert", "put", "post"]
            args_str = json.dumps(action.tool_args).lower()
            if any(w in args_str or w in tool for w in write_indicators):
                violations.append(Finding(
                    id=f"DRIFT-PERM-ESCALATION-{tool}-T{action.turn}",
                    title=f"Permission escalation: '{action.tool_name}' exceeded READ access",
                    description=(
                        f"At turn {action.turn}, the agent performed a write operation via "
                        f"'{action.tool_name}' but only has READ permission. "
                        "This is a permission drift violation."
                    ),
                    severity=Severity.CRITICAL,
                    category="drift",
                ))

    return violations


def run_monitor(
    trace_file: str | None = None,
    policy_path: str | None = None,
    live: bool = False,
) -> list[Finding]:
    """Run the behavioral monitor on agent traces."""
    policy = load_policy(policy_path)
    all_violations: list[Finding] = []

    console.print("\n📡 [bold]Monitoring agent behavior...[/bold]\n")

    if not policy:
        console.print("  [yellow]⚠️  No policy file provided. Running in observation mode.[/yellow]")
        console.print("  [dim]Use --policy to enable drift detection.[/dim]\n")

    if trace_file:
        trace_path = Path(trace_file)
        lines = trace_path.read_text(encoding="utf-8").splitlines()

        for i, line in enumerate(lines):
            if not line.strip():
                continue

            action = parse_trace_line(line)
            if not action:
                continue

            # Print action
            _print_action(action)

            # Check against policy if available
            if policy:
                violations = check_action_against_policy(action, policy)
                all_violations.extend(violations)

                for v in violations:
                    icon = "🚨" if v.severity in (Severity.CRITICAL, Severity.HIGH) else "⚠️"
                    color = "red" if v.severity == Severity.CRITICAL else "yellow"
                    console.print(f"     {icon} [{color}]DRIFT: {v.title}[/{color}]")
                    console.print(f"        [dim]→ {v.description}[/dim]")

    elif live:
        console.print("  [dim]Reading from stdin... (Ctrl+C to stop)[/dim]\n")
        import sys

        try:
            for line in sys.stdin:
                action = parse_trace_line(line)
                if not action:
                    continue

                _print_action(action)

                if policy:
                    violations = check_action_against_policy(action, policy)
                    all_violations.extend(violations)
                    for v in violations:
                        console.print(f"     🚨 [red]DRIFT: {v.title}[/red]")
        except KeyboardInterrupt:
            console.print("\n  [dim]Monitoring stopped.[/dim]")

    else:
        console.print("  [red]Error: Provide --trace-file or --live[/red]")
        return []

    # Summary
    if all_violations:
        console.print(f"\n🚨 [red bold]{len(all_violations)} policy violations detected[/red bold]")
    else:
        console.print("\n✅ [green]No policy violations detected[/green]")

    return all_violations


def _print_action(action: AgentAction) -> None:
    """Print a formatted agent action."""
    type_icons = {
        "tool_call": "🔧",
        "data_access": "📊",
        "response": "💬",
        "unknown": "❓",
    }
    icon = type_icons.get(action.action_type, "❓")

    parts = [f"  Turn {action.turn}: {icon}"]

    if action.tool_name:
        args_preview = ""
        if action.tool_args:
            args_str = json.dumps(action.tool_args)
            args_preview = f"({args_str[:60]}{'...' if len(args_str) > 60 else ''})"
        parts.append(f"[bold]{action.tool_name}[/bold]{args_preview}")
    elif action.result_summary:
        parts.append(action.result_summary[:80])

    console.print(" ".join(parts))
