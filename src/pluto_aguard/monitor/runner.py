"""Runtime behavioral monitor for AI agents.

Ingests OpenTelemetry traces or live agent output and detects:
- Unauthorized tool calls (tools not in the agent's declared permissions)
- Permission drift (behavior that exceeds declared capabilities)
- Sensitive data access violations
- Anomalous action patterns
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml
from rich.console import Console

from pluto_aguard.models import AgentAction, AgentPolicy, ApprovalEvent, Finding, Severity

console = Console()

ParsedTraceEvent = AgentAction | ApprovalEvent

# Word-boundary matching avoids false positives on substrings embedded in
# larger identifiers, e.g. "created_at" (contains "create") or "postgres"
# (contains "post").
_WRITE_INDICATOR_PATTERN = re.compile(
    r"\b(write|create|update|delete|insert|put|post)\b", re.IGNORECASE
)


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


def parse_trace_line(line: str) -> ParsedTraceEvent | None:
    """Parse a single JSONL trace line into an action or approval event."""
    try:
        data = json.loads(line.strip())
    except json.JSONDecodeError:
        return None

    if "name" in data and "attributes" in data:
        attrs = data.get("attributes", {})
        action_type = attrs.get("action_type", _infer_action_type(data["name"]))
        if action_type == "approval":
            return ApprovalEvent(
                tool_name=attrs.get("tool.name", attrs.get("approval.tool_name", data.get("name", "unknown"))),
                approved_by=attrs.get("approval.approved_by", attrs.get("approved_by")),
                approval_id=attrs.get("approval.id", attrs.get("approval_id")),
                approved_at=attrs.get("approval.approved_at", data.get("startTimeUnixNano", data.get("timestamp"))),
                expired=_as_bool(attrs.get("approval.expired", attrs.get("expired", False))),
            )

        return AgentAction(
            turn=attrs.get("turn", 0),
            timestamp=data.get("startTimeUnixNano", data.get("timestamp")),
            action_type=action_type,
            tool_name=attrs.get("tool.name", data.get("name")),
            tool_args=attrs.get("tool.args", {}),
            result_summary=attrs.get("result.summary"),
        )

    action_type = data.get("action_type")
    if action_type == "approval":
        tool_name = data.get("tool_name", data.get("approved_tool", data.get("name")))
        if not isinstance(tool_name, str) or not tool_name:
            return None
        return ApprovalEvent(
            tool_name=tool_name,
            approved_by=data.get("approved_by"),
            approval_id=data.get("approval_id"),
            approved_at=data.get("approved_at", data.get("timestamp")),
            expired=_as_bool(data.get("expired", False)),
        )

    if "action_type" in data or "tool_name" in data:
        return AgentAction(**data)

    return None


def _infer_action_type(span_name: str) -> str:
    """Infer action type from span name."""
    name_lower = span_name.lower()
    if any(k in name_lower for k in ("approval", "approve")):
        return "approval"
    if any(k in name_lower for k in ("tool", "function", "call")):
        return "tool_call"
    if any(k in name_lower for k in ("query", "read", "fetch", "get")):
        return "data_access"
    if any(k in name_lower for k in ("response", "generate", "complete")):
        return "response"
    return "unknown"


def _as_bool(value: object) -> bool:
    """Convert common truthy values to bool."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def check_action_against_policy(
    action: AgentAction,
    policy: AgentPolicy,
    approvals: dict[str, ApprovalEvent] | None = None,
) -> list[Finding]:
    """Check a single agent action against the declared policy."""
    violations: list[Finding] = []
    approvals = approvals or {}

    if not action.tool_name:
        return violations

    tool = action.tool_name.lower()
    denied_tools = [t.lower() for t in policy.denied_tools]
    allowed_tools = [t.lower() for t in policy.allowed_tools]
    approval_required = [t.lower() for t in policy.require_human_approval]

    if denied_tools and tool in denied_tools:
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
            owasp_id="MCP05:2025",
        ))

    if allowed_tools and tool not in allowed_tools:
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
            owasp_id="MCP02:2025",
        ))

    if tool in approval_required:
        approval = approvals.get(tool)
        if approval and approval.expired:
            violations.append(Finding(
                id=f"DRIFT-EXPIRED-APPROVAL-{tool}-T{action.turn}",
                title=f"Expired approval for tool '{action.tool_name}'",
                description=(
                    f"At turn {action.turn}, the agent called '{action.tool_name}' using an "
                    "approval record that is marked expired. A fresh human approval is required "
                    "before this action can proceed."
                ),
                severity=Severity.HIGH,
                category="drift",
                owasp_id="MCP05:2025",
            ))
        elif approvals and not approval:
            approved_tools = ", ".join(sorted(a.tool_name for a in approvals.values()))
            violations.append(Finding(
                id=f"DRIFT-MISMATCHED-APPROVAL-{tool}-T{action.turn}",
                title=f"Mismatched approval for tool '{action.tool_name}'",
                description=(
                    f"At turn {action.turn}, the agent called '{action.tool_name}' which requires "
                    "human approval, but the recorded approval applies to a different tool "
                    f"({approved_tools})."
                ),
                severity=Severity.HIGH,
                category="drift",
                owasp_id="MCP05:2025",
            ))
        elif not approval:
            violations.append(Finding(
                id=f"DRIFT-NO-APPROVAL-{tool}-T{action.turn}",
                title=f"Tool '{action.tool_name}' used without human approval",
                description=(
                    f"At turn {action.turn}, the agent called '{action.tool_name}' which "
                    "requires human-in-the-loop approval, but no approval record was found."
                ),
                severity=Severity.HIGH,
                category="drift",
                owasp_id="MCP05:2025",
            ))

    if policy.max_permissions:
        max_perm = policy.max_permissions.get(tool, policy.max_permissions.get("*"))
        if max_perm and max_perm.lower() == "read":
            args_str = json.dumps(action.tool_args)
            if _WRITE_INDICATOR_PATTERN.search(args_str) or _WRITE_INDICATOR_PATTERN.search(tool):
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
    approvals: dict[str, ApprovalEvent] = {}
    all_violations: list[Finding] = []

    console.print("\n📡 [bold]Monitoring agent behavior...[/bold]\n")

    if not policy:
        console.print("  [yellow]⚠️  No policy file provided. Running in observation mode.[/yellow]")
        console.print("  [dim]Use --policy to enable drift detection.[/dim]\n")

    if trace_file:
        lines = Path(trace_file).read_text(encoding="utf-8").splitlines()
        _process_trace_lines(lines, policy, approvals, all_violations)
    elif live:
        console.print("  [dim]Reading from stdin... (Ctrl+C to stop)[/dim]\n")
        import sys

        try:
            _process_trace_lines(sys.stdin, policy, approvals, all_violations)
        except KeyboardInterrupt:
            console.print("\n  [dim]Monitoring stopped.[/dim]")
    else:
        console.print("  [red]Error: Provide --trace-file or --live[/red]")
        return []

    if all_violations:
        console.print(f"\n🚨 [red bold]{len(all_violations)} policy violations detected[/red bold]")
    else:
        console.print("\n✅ [green]No policy violations detected[/green]")

    return all_violations


def _process_trace_lines(
    lines: list[str] | object,
    policy: AgentPolicy | None,
    approvals: dict[str, ApprovalEvent],
    all_violations: list[Finding],
) -> None:
    """Process a stream of trace lines and collect policy violations."""
    for line in lines:
        if not isinstance(line, str) or not line.strip():
            continue

        event = parse_trace_line(line)
        if not event:
            continue

        _print_action(event)

        if isinstance(event, ApprovalEvent):
            approvals[event.tool_name.lower()] = event
            continue

        if policy:
            violations = check_action_against_policy(event, policy, approvals)
            all_violations.extend(violations)
            _print_violations(violations)


def _print_violations(violations: list[Finding]) -> None:
    """Print policy violations."""
    for violation in violations:
        icon = "🚨" if violation.severity in (Severity.CRITICAL, Severity.HIGH) else "⚠️"
        color = "red" if violation.severity == Severity.CRITICAL else "yellow"
        console.print(f"     {icon} [{color}]DRIFT: {violation.title}[/{color}]")
        console.print(f"        [dim]→ {violation.description}[/dim]")


def _print_action(action: ParsedTraceEvent) -> None:
    """Print a formatted agent action or approval."""
    if isinstance(action, ApprovalEvent):
        status = "expired" if action.expired else "active"
        approver = f" by {action.approved_by}" if action.approved_by else ""
        console.print(f"  Approval: ✅ [bold]{action.tool_name}[/bold]{approver} [{status}]")
        return

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
