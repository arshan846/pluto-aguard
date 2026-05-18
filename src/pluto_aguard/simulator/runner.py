"""What-If Policy Simulator.

Simulates the impact of security policy changes on an agent's risk score
BEFORE applying them. Enables data-driven security investment decisions.

This is the unique differentiator of Pluto AgentGuard — no other tool
(commercial or open-source) offers policy impact simulation for AI agents.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from rich.console import Console
from rich.table import Table

from pluto_aguard.models import PolicyChange, RiskScore, SimulationResult
from pluto_aguard.scanners.permission_scanner import (
    calculate_permission_risk_score,
    load_agent_config,
    scan_agent_permissions,
)

console = Console()

# Built-in policy change catalog
BUILTIN_POLICIES: list[dict[str, Any]] = [
    {
        "id": "restrict-sql-readonly",
        "description": "Restrict SQL tool to SELECT-only queries",
        "category": "permissions",
        "transforms": {
            "tools.sql_query.permissions": "read",
            "tools.database.permissions": "read",
        },
        "risk_reduction": {
            "permissions": 0.6,  # Reduces permission risk by 40%
        },
    },
    {
        "id": "add-hitl-file-ops",
        "description": "Add human-in-the-loop for file operations",
        "category": "permissions",
        "transforms": {
            "require_human_approval": ["file_write", "file_delete"],
        },
        "risk_reduction": {
            "permissions": 0.5,
        },
    },
    {
        "id": "ephemeral-tokens",
        "description": "Rotate API keys to ephemeral tokens",
        "category": "secrets",
        "transforms": {
            "auth.token_type": "ephemeral",
            "auth.rotation_seconds": 3600,
        },
        "risk_reduction": {
            "secrets": 0.3,
        },
    },
    {
        "id": "add-rate-limits",
        "description": "Add rate limits (100 calls/minute) and timeout (5 min)",
        "category": "permissions",
        "transforms": {
            "rate_limit": {"calls_per_minute": 100},
            "timeout": 300,
        },
        "risk_reduction": {
            "permissions": 0.8,
        },
    },
    {
        "id": "restrict-network-egress",
        "description": "Restrict outbound network access to allowlisted domains",
        "category": "permissions",
        "transforms": {
            "network.egress": "allowlist",
        },
        "risk_reduction": {
            "permissions": 0.7,
        },
    },
    {
        "id": "add-tool-allowlist",
        "description": "Convert from implicit-allow to explicit tool allowlist",
        "category": "permissions",
        "transforms": {
            "permission_model": "allowlist",
        },
        "risk_reduction": {
            "permissions": 0.5,
        },
    },
    {
        "id": "sandbox-execution",
        "description": "Run agent in sandboxed execution environment",
        "category": "isolation",
        "transforms": {
            "runtime.sandbox": True,
            "runtime.network_isolation": True,
        },
        "risk_reduction": {
            "permissions": 0.4,
            "secrets": 0.6,
        },
    },
]


def _apply_policy_to_config(
    config: dict[str, Any], policy: dict[str, Any]
) -> dict[str, Any]:
    """Apply a policy's transforms to a config (copy), return modified config."""
    import copy

    modified = copy.deepcopy(config)
    transforms = policy.get("transforms", {})

    for key, value in transforms.items():
        parts = key.split(".")
        target = modified
        skip = False
        for part in parts[:-1]:
            if not isinstance(target, dict):
                skip = True
                break
            if part not in target:
                target[part] = {}
            target = target[part]

        if skip or not isinstance(target, dict):
            continue

        last_key = parts[-1]
        if isinstance(value, list) and isinstance(target.get(last_key), list):
            target[last_key] = list(set(target[last_key] + value))
        else:
            target[last_key] = value

    return modified


def simulate_policies(
    config: dict[str, Any],
    policies: list[dict[str, Any]] | None = None,
) -> list[SimulationResult]:
    """Simulate each policy change individually and return results."""
    if policies is None:
        policies = BUILTIN_POLICIES

    original_findings = scan_agent_permissions(Path("agent-config.yaml"), config)
    original_risk = calculate_permission_risk_score(config)
    original_score = RiskScore(
        overall=original_risk,
        breakdown={"permissions": original_risk},
        finding_count={},
    )

    results: list[SimulationResult] = []

    for policy_def in policies:
        modified_config = _apply_policy_to_config(config, policy_def)
        new_risk = calculate_permission_risk_score(modified_config)

        new_score = RiskScore(
            overall=new_risk,
            breakdown={"permissions": new_risk},
            finding_count={},
        )

        delta = new_risk - original_risk
        delta_pct = (delta / original_risk * 100) if original_risk > 0 else 0

        policy_change = PolicyChange(
            id=policy_def["id"],
            description=policy_def["description"],
            category=policy_def["category"],
        )

        results.append(SimulationResult(
            original_score=original_score,
            new_score=new_score,
            applied_policies=[policy_change],
            score_delta=round(delta, 1),
            score_delta_pct=round(delta_pct, 1),
        ))

    return results


def simulate_combined(
    config: dict[str, Any],
    policy_ids: list[str],
    policies: list[dict[str, Any]] | None = None,
) -> SimulationResult:
    """Simulate applying multiple policies together."""
    if policies is None:
        policies = BUILTIN_POLICIES

    original_risk = calculate_permission_risk_score(config)
    original_score = RiskScore(
        overall=original_risk,
        breakdown={"permissions": original_risk},
        finding_count={},
    )

    modified_config = config
    applied: list[PolicyChange] = []

    for pid in policy_ids:
        policy_def = next((p for p in policies if p["id"] == pid), None)
        if policy_def:
            modified_config = _apply_policy_to_config(modified_config, policy_def)
            applied.append(PolicyChange(
                id=policy_def["id"],
                description=policy_def["description"],
                category=policy_def["category"],
            ))

    new_risk = calculate_permission_risk_score(modified_config)
    new_score = RiskScore(
        overall=new_risk,
        breakdown={"permissions": new_risk},
        finding_count={},
    )

    delta = new_risk - original_risk
    delta_pct = (delta / original_risk * 100) if original_risk > 0 else 0

    # Generate recommendations
    recommendations = []
    if delta_pct < -30:
        recommendations.append(
            f"Applying these {len(applied)} policies reduces risk by {abs(delta_pct):.0f}% — "
            "strong security improvement with manageable operational impact."
        )
    if any(p.category == "permissions" for p in applied):
        recommendations.append(
            "Permission restrictions are the highest-impact changes. "
            "Implement these first."
        )

    return SimulationResult(
        original_score=original_score,
        new_score=new_score,
        applied_policies=applied,
        score_delta=round(delta, 1),
        score_delta_pct=round(delta_pct, 1),
        recommendations=recommendations,
    )


def run_whatif(
    config_path: str,
    policy_path: str | None = None,
    interactive: bool = False,
) -> None:
    """Run the What-If policy simulator."""
    config = load_agent_config(Path(config_path))
    original_risk = calculate_permission_risk_score(config)

    console.print("\n🔮 [bold]What-If Policy Simulator[/bold]\n")
    console.print(f"  Agent config: {config_path}")
    console.print(f"  Current Risk Score: [bold]{original_risk:.0f}/100[/bold]\n")

    # Load custom policies if provided
    custom_policies = None
    if policy_path:
        policy_content = Path(policy_path).read_text(encoding="utf-8")
        custom_policies = yaml.safe_load(policy_content)
        if isinstance(custom_policies, dict):
            custom_policies = custom_policies.get("policies", [])

    # Simulate individual policies
    console.print("  [bold]Simulating policy changes:[/bold]\n")
    results = simulate_policies(config, custom_policies)

    table = Table(show_header=True, header_style="bold")
    table.add_column("Policy", style="dim", width=50)
    table.add_column("New Score", justify="right")
    table.add_column("Change", justify="right")

    effective_policies = []
    for result in results:
        policy = result.applied_policies[0]
        new_score = result.new_score.overall

        if result.score_delta_pct < 0:
            change_str = f"[green]↓ {abs(result.score_delta_pct):.0f}%[/green]"
            effective_policies.append(policy.id)
        elif result.score_delta_pct > 0:
            change_str = f"[red]↑ {result.score_delta_pct:.0f}%[/red]"
        else:
            change_str = "[dim]—[/dim]"

        table.add_row(
            f"  ✅ {policy.description}",
            f"{new_score:.0f}",
            change_str,
        )

    console.print(table)

    # Show combined impact of effective policies
    if len(effective_policies) > 1:
        console.print(f"\n  [bold]Combined impact (all {len(effective_policies)} effective policies):[/bold]")
        combined = simulate_combined(config, effective_policies, custom_policies)
        console.print(
            f"  💡 Risk drops from {combined.original_score.overall:.0f} → "
            f"[green bold]{combined.new_score.overall:.0f}[/green bold] "
            f"([green]↓ {abs(combined.score_delta_pct):.0f}%[/green])"
        )

        for rec in combined.recommendations:
            console.print(f"  📌 {rec}")

    console.print()
