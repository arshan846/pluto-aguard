"""Permission scanner for agent configurations.

Analyzes agent permission configurations to detect over-permissioning,
privilege escalation paths, and missing access controls.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from pluto_aguard.models import Finding, Severity

# Risk weights for different permission types
PERMISSION_RISK_WEIGHTS: dict[str, float] = {
    "execute": 1.0,
    "shell": 1.0,
    "file_write": 0.9,
    "file_delete": 0.9,
    "database_write": 0.8,
    "database_delete": 0.8,
    "network_outbound": 0.7,
    "file_read": 0.4,
    "database_read": 0.4,
    "api_call": 0.5,
}


def scan_agent_permissions(file_path: Path, config: dict[str, Any]) -> list[Finding]:
    """Analyze agent permission configuration for security issues."""
    findings: list[Finding] = []

    agent_name = config.get("name", config.get("agent_name", "unknown"))
    tools = config.get("tools", config.get("allowed_tools", []))
    permissions = config.get("permissions", {})

    # Check for missing permission declarations
    if not permissions and tools:
        findings.append(Finding(
            id=f"PERM-UNDECLARED-{agent_name}",
            title=f"Agent '{agent_name}' has tools but no declared permissions",
            description=(
                f"Agent '{agent_name}' has {len(tools)} tools configured but no explicit "
                "permission declarations. Without declared permissions, drift detection "
                "is impossible and the agent may operate with implicit full access."
            ),
            severity=Severity.HIGH,
            category="permissions",
            owasp_id="MCP02:2025",
            file_path=str(file_path),
            remediation=(
                "Add an explicit 'permissions' section declaring the minimum required "
                "access level for each tool. Use the principle of least privilege."
            ),
        ))

    # Check for no human-in-the-loop on dangerous operations
    hitl_actions = config.get("require_human_approval", config.get("human_in_the_loop", []))
    dangerous_without_hitl = []

    for tool in tools:
        tool_name = tool if isinstance(tool, str) else tool.get("name", "")
        if tool_name.lower() in {"execute", "shell", "file_write", "file_delete", "sudo",
                                  "database_delete", "send_email", "deploy", "publish"}:
            if tool_name not in hitl_actions:
                dangerous_without_hitl.append(tool_name)

    if dangerous_without_hitl:
        findings.append(Finding(
            id=f"PERM-NO-HITL-{agent_name}",
            title=f"Dangerous tools without human approval on '{agent_name}'",
            description=(
                f"Agent '{agent_name}' can invoke dangerous tools "
                f"({', '.join(dangerous_without_hitl)}) without requiring human approval. "
                "These tools can cause irreversible changes and should have a "
                "human-in-the-loop gate."
            ),
            severity=Severity.HIGH,
            category="permissions",
            owasp_id="MCP05:2025",
            file_path=str(file_path),
            remediation=(
                "Add these tools to the 'require_human_approval' list: "
                f"{', '.join(dangerous_without_hitl)}"
            ),
        ))

    # Check for overly broad data access
    data_access = config.get("data_access", config.get("data_access_rules", {}))
    if isinstance(data_access, dict):
        for resource, access_level in data_access.items():
            if isinstance(access_level, str) and access_level.lower() in ("all", "full", "*"):
                findings.append(Finding(
                    id=f"PERM-BROAD-DATA-{agent_name}-{resource}",
                    title=f"Unrestricted data access to '{resource}' on '{agent_name}'",
                    description=(
                        f"Agent '{agent_name}' has unrestricted access to '{resource}'. "
                        "Broad data access increases blast radius in case of compromise."
                    ),
                    severity=Severity.HIGH,
                    category="permissions",
                    file_path=str(file_path),
                    remediation=(
                        f"Restrict access to '{resource}' to only the specific "
                        "tables/collections/paths required."
                    ),
                ))

    # Check for missing timeout/rate limits
    if not config.get("timeout") and not config.get("rate_limit"):
        findings.append(Finding(
            id=f"PERM-NO-LIMITS-{agent_name}",
            title=f"No timeout or rate limits on agent '{agent_name}'",
            description=(
                f"Agent '{agent_name}' has no timeout or rate limit configured. "
                "Without limits, a compromised or misbehaving agent can consume "
                "unbounded resources or execute an unlimited number of actions."
            ),
            severity=Severity.MEDIUM,
            category="permissions",
            file_path=str(file_path),
            remediation=(
                "Add 'timeout' (e.g., 300 seconds) and 'rate_limit' (e.g., 100 calls/minute) "
                "to constrain agent behavior."
            ),
        ))

    return findings


_HARDENING_WEIGHT = 5.0
_PERMISSIONS_DECLARED_WEIGHT = 10.0
_EPHEMERAL_TOKEN_TYPES = ("ephemeral", "short-lived", "rotating")
_READ_ONLY_ACCESS_LEVELS = ("read", "readonly", "read-only")


def calculate_permission_risk_score(config: dict[str, Any]) -> float:
    """Calculate a risk score (0-100) based on agent permissions.

    Higher scores indicate more permissive (riskier) configurations.

    The denominator (max_possible) is a fixed worst-case baseline for the
    controls any agent config is expected to have (timeout, rate limit,
    declared permissions): these always contribute to it once the agent
    has tools, so closing a gap (e.g. adding a timeout) always moves the
    ratio, rather than shrinking the denominator in lockstep with the
    numerator and leaving it unchanged.

    network.egress/runtime.sandbox/auth.token_type/permission_model are
    AgentGuard's own extended policy vocabulary -- no config format has
    these by convention. They're only scored once a config declares the
    *specific field the check evaluates*, not merely the parent key: an
    `auth: {type: oauth2}` block describes an auth mechanism and has
    nothing to do with token_type, so it must not be treated as having
    adopted-and-failed that check. Gating on the parent dict's presence
    instead of the field itself would do exactly that. A config that's
    never set runtime.sandbox at all isn't penalized for lacking it; one
    that sets runtime.sandbox=false is. Without this gate, every
    real-world config (including a genuinely well-configured one) would
    carry a large fixed penalty just for not using fields specific to
    this project.
    """
    score = 0.0
    max_possible = 0.0

    tools = config.get("tools", config.get("allowed_tools", []))
    permissions = config.get("permissions", {})
    if not isinstance(permissions, dict):
        permissions = {}
    hitl = config.get("require_human_approval", [])

    for tool in tools:
        tool_name = (tool if isinstance(tool, str) else tool.get("name", "")).lower()
        weight = PERMISSION_RISK_WEIGHTS.get(tool_name, 0.3)
        max_possible += weight

        # Base risk from having the permission
        tool_risk = weight

        # Reduce if human-in-the-loop is required
        if tool_name in hitl:
            tool_risk *= 0.3

        tool_perms = permissions.get(tool_name, {})
        if isinstance(tool_perms, dict):
            # Reduce if scoped permissions exist
            if tool_perms.get("scope"):
                tool_risk *= 0.5
            # Reduce if the tool is restricted to read-only access
            if str(tool_perms.get("access", "")).lower() in _READ_ONLY_ACCESS_LEVELS:
                tool_risk *= 0.4

        score += tool_risk

    if tools:  # Only penalize missing controls if agent has tools
        if not config.get("timeout"):
            score += _HARDENING_WEIGHT
        max_possible += _HARDENING_WEIGHT

        if not config.get("rate_limit"):
            score += _HARDENING_WEIGHT
        max_possible += _HARDENING_WEIGHT

        if not permissions:
            score += _PERMISSIONS_DECLARED_WEIGHT
        max_possible += _PERMISSIONS_DECLARED_WEIGHT

        # Extended hardening controls: only counted if the config declares
        # the *specific field the check evaluates*, not just the parent
        # key -- e.g. `auth: {type: oauth2}` describes an auth mechanism
        # and has nothing to do with token_type. Gating on the parent
        # dict's mere presence would penalize that config for a field it
        # never touched, exactly the problem adoption-gating exists to
        # avoid (see docstring).
        network = config.get("network")
        if isinstance(network, dict) and "egress" in network:
            if str(network.get("egress", "")).lower() != "allowlist":
                score += _HARDENING_WEIGHT
            max_possible += _HARDENING_WEIGHT

        runtime = config.get("runtime")
        if isinstance(runtime, dict) and "sandbox" in runtime:
            if not runtime.get("sandbox"):
                score += _HARDENING_WEIGHT
            max_possible += _HARDENING_WEIGHT

        auth = config.get("auth")
        if isinstance(auth, dict) and "token_type" in auth:
            if str(auth.get("token_type", "")).lower() not in _EPHEMERAL_TOKEN_TYPES:
                score += _HARDENING_WEIGHT
            max_possible += _HARDENING_WEIGHT

        if "permission_model" in config:
            if str(config.get("permission_model", "")).lower() != "allowlist":
                score += _HARDENING_WEIGHT
            max_possible += _HARDENING_WEIGHT

    if max_possible == 0:
        return 0.0

    return min(100.0, (score / max_possible) * 100)


def load_agent_config(file_path: Path) -> dict[str, Any]:
    """Load an agent configuration file."""
    content = file_path.read_text(encoding="utf-8")
    if file_path.suffix == ".json":
        import json
        return json.loads(content)  # type: ignore[no-any-return]
    return yaml.safe_load(content) or {}  # type: ignore[no-any-return]
