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
            owasp_id="OWASP-MCP-03",
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
            owasp_id="OWASP-MCP-04",
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


def calculate_permission_risk_score(config: dict[str, Any]) -> float:
    """Calculate a risk score (0-100) based on agent permissions.

    Higher scores indicate more permissive (riskier) configurations.
    """
    score = 0.0
    max_possible = 0.0

    tools = config.get("tools", config.get("allowed_tools", []))
    permissions = config.get("permissions", {})
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

        # Reduce if scoped permissions exist
        tool_perms = permissions.get(tool_name, {})
        if isinstance(tool_perms, dict) and tool_perms.get("scope"):
            tool_risk *= 0.5

        score += tool_risk

    # Factor in missing controls
    if tools:  # Only penalize missing controls if agent has tools
        if not config.get("timeout"):
            score += 5
            max_possible += 5
        if not config.get("rate_limit"):
            score += 5
            max_possible += 5
        if not permissions and tools:
            score += 10
            max_possible += 10

    if max_possible == 0:
        return 0.0 if not tools else 0.0

    return min(100.0, (score / max_possible) * 100)


def load_agent_config(file_path: Path) -> dict[str, Any]:
    """Load an agent configuration file."""
    content = file_path.read_text(encoding="utf-8")
    if file_path.suffix == ".json":
        import json
        return json.loads(content)  # type: ignore[no-any-return]
    return yaml.safe_load(content) or {}  # type: ignore[no-any-return]
