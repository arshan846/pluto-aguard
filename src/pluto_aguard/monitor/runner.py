"""Runtime behavioral monitor for AI agents.

Ingests OpenTelemetry traces or live agent output and detects:
- Unauthorized tool calls (tools not in the agent's declared permissions)
- Permission drift (behavior that exceeds declared capabilities)
- Sensitive data access violations
- Anomalous action patterns

Trace formats: this recognizes the OTel GenAI semantic convention's
gen_ai.* attribute namespace (gen_ai.tool.name, gen_ai.operation.name,
gen_ai.tool.call.arguments) -- what real exporters like OpenLIT, Traceloop
OpenLLMetry, and OTel-native LangChain instrumentation actually emit -- as
well as this project's own ad-hoc tool.name/tool.args attributes and a flat
simple-JSON format. See docs/trace-ingestion.md.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

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

# OTel GenAI semantic convention: gen_ai.operation.name identifies the kind
# of span. Only the values relevant to policy checking are mapped here.
_GENAI_OPERATION_ACTION_TYPES = {
    "execute_tool": "tool_call",
    "chat": "response",
    "generate_content": "response",
    "text_completion": "response",
}

# Attribute names carrying tool-call arguments, tried in priority order.
# There's no single stable gen_ai.* attribute for this across the ecosystem
# yet, so real exporters vary (Traceloop's OpenLLMetry uses its own
# traceloop.* namespace for tool I/O). Values are often JSON-encoded
# strings, since OTel span attributes must be primitives, not nested
# objects -- a raw dict is only valid for this project's own trace format.
_TOOL_ARG_ATTRS = (
    "gen_ai.tool.call.arguments",
    "gen_ai.tool.arguments",
    "traceloop.entity.input",
    "tool.args",
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


def parse_trace_line(line: str, default_turn: int = 0) -> ParsedTraceEvent | None:
    """Parse a single JSONL trace line into an action or approval event.

    default_turn is used when the trace has no explicit turn number, which
    is normal for real OTel GenAI traces -- "turn" is this project's own
    concept for numbering actions, not part of any tracing standard.
    """
    try:
        data = json.loads(line.strip())
    except json.JSONDecodeError:
        return None

    if "name" in data and "attributes" in data:
        attrs = data.get("attributes", {})
        action_type = attrs.get("action_type", _infer_action_type(data["name"], attrs))
        if action_type == "approval":
            return ApprovalEvent(
                tool_name=_extract_tool_name(attrs, data.get("name")) or "unknown",
                approved_by=attrs.get("approval.approved_by", attrs.get("approved_by")),
                approval_id=attrs.get("approval.id", attrs.get("approval_id")),
                approved_at=_stringify(
                    attrs.get("approval.approved_at", data.get("startTimeUnixNano", data.get("timestamp")))
                ),
                expired=_as_bool(attrs.get("approval.expired", attrs.get("expired", False))),
            )

        return AgentAction(
            turn=attrs.get("turn", default_turn),
            timestamp=_stringify(data.get("startTimeUnixNano", data.get("timestamp"))),
            action_type=action_type,
            tool_name=_extract_tool_name(attrs, data.get("name")),
            tool_args=_extract_tool_args(attrs),
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
        data.setdefault("turn", default_turn)
        return AgentAction(**data)

    return None


def _extract_tool_name(attrs: dict[str, Any], span_name: str | None) -> str | None:
    """Resolve the tool name, preferring the OTel GenAI semantic convention."""
    return (
        attrs.get("gen_ai.tool.name")
        or attrs.get("tool.name")
        or attrs.get("approval.tool_name")
        or attrs.get("traceloop.entity.name")
        or span_name
    )


def _extract_tool_args(attrs: dict[str, Any]) -> dict[str, Any]:
    """Resolve tool-call arguments, checking known attribute names in order.

    OTel span attribute values must be primitives, so real exporters
    typically JSON-encode structured arguments as a string.
    """
    for key in _TOOL_ARG_ATTRS:
        if key not in attrs:
            continue
        value = attrs[key]
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                return {"raw": value}
            return parsed if isinstance(parsed, dict) else {"raw": value}
    return {}


def _infer_action_type(span_name: str, attrs: dict[str, Any] | None = None) -> str:
    """Infer action type from span name, or gen_ai.operation.name if present."""
    if attrs:
        operation = attrs.get("gen_ai.operation.name")
        if operation in _GENAI_OPERATION_ACTION_TYPES:
            return _GENAI_OPERATION_ACTION_TYPES[operation]

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


def _stringify(value: object) -> str | None:
    """Coerce a timestamp-like value to str.

    Real OTel spans carry startTimeUnixNano as an integer; the models here
    store timestamps as strings.
    """
    if value is None or isinstance(value, str):
        return value
    return str(value)


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
    # Real traces rarely carry an explicit turn number -- auto-assign one
    # per action so finding IDs (which embed the turn) stay unique.
    turn_counter = 0
    for line in lines:
        if not isinstance(line, str) or not line.strip():
            continue

        event = parse_trace_line(line, default_turn=turn_counter)
        if not event:
            continue

        _print_action(event)

        if isinstance(event, ApprovalEvent):
            approvals[event.tool_name.lower()] = event
            continue

        turn_counter += 1

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
