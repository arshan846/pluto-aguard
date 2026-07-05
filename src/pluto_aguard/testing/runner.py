"""Policy coverage linter for agent policies.

For each named attack scenario, checks whether the tool it names is in the
policy's denied_tools or require_human_approval list -- via the same
check_action_against_policy used by the live monitor. This is tool-name
membership testing, not adversarial simulation: no prompt is executed, no
LLM is involved, and scenario.attack_prompt is never read here.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml
from rich.console import Console
from rich.table import Table

from pluto_aguard.models import AgentAction, AgentPolicy
from pluto_aguard.monitor.runner import check_action_against_policy
from pluto_aguard.testing.attack_packs import ATTACK_PACKS, AttackScenario

console = Console()


def load_policy(policy_path: str) -> AgentPolicy:
    """Load agent policy from YAML file."""
    path = Path(policy_path)
    content = path.read_text(encoding="utf-8")
    data = yaml.safe_load(content) or {}
    return AgentPolicy(**data)


def simulate_attack(scenario: AttackScenario, policy: AgentPolicy) -> dict[str, Any]:
    """Check one scenario's expected_tool_call against a policy's tool lists.

    scenario.attack_prompt is documentation only and is not read here --
    this is a tool-name lookup, not an evaluation of the attack narrative.

    Returns a dict with:
    - scenario: the attack scenario
    - action: the simulated agent action
    - violations: list of policy violations detected
    - result: "PASS" if policy catches it, "FAIL" if policy misses it
    """
    action = AgentAction(
        turn=0,
        action_type="tool_call",
        tool_name=scenario.expected_tool_call,
        tool_args=scenario.expected_tool_args,
    )

    violations = check_action_against_policy(action, policy)
    result = "PASS" if violations else "FAIL"

    return {
        "scenario": scenario,
        "action": action,
        "violations": violations,
        "result": result,
    }


def run_test(
    policy_path: str,
    attack_pack: str = "all",
    fail_on_miss: bool = False,
) -> None:
    """Run adversarial tests against an agent policy."""
    policy = load_policy(policy_path)

    console.print("\n🎯 [bold]Adversarial Policy Test[/bold]\n")
    console.print(f"  Policy: {policy_path}")
    console.print(f"  Agent: {policy.name}")
    console.print(f"  Attack pack: {attack_pack}")

    if attack_pack not in ATTACK_PACKS:
        available = ", ".join(ATTACK_PACKS.keys())
        console.print(f"\n  [red]Unknown attack pack: {attack_pack}[/red]")
        console.print(f"  Available packs: {available}")
        return

    scenarios = ATTACK_PACKS[attack_pack]
    console.print(f"  Scenarios: {len(scenarios)}\n")

    results = []
    for scenario in scenarios:
        result = simulate_attack(scenario, policy)
        results.append(result)

    table = Table(show_header=True, header_style="bold")
    table.add_column("Result", width=8)
    table.add_column("ID", width=8)
    table.add_column("Attack Scenario", width=40)
    table.add_column("Tool Attempted", width=18)
    table.add_column("Policy Verdict", width=30)

    pass_count = 0
    fail_count = 0

    for item in results:
        scenario = item["scenario"]
        if item["result"] == "PASS":
            pass_count += 1
            result_icon = "[green]✅ PASS[/green]"
            verdict = "[green]Blocked by policy[/green]"
            if item["violations"]:
                verdict = f"[green]{item['violations'][0].title[:28]}[/green]"
        else:
            fail_count += 1
            result_icon = "[red]❌ FAIL[/red]"
            verdict = "[red]Policy would NOT catch this[/red]"

        table.add_row(
            result_icon,
            scenario.id,
            scenario.name,
            scenario.expected_tool_call,
            verdict,
        )

    console.print(table)

    total = len(results)
    console.print(
        f"\n  📊 Results: [green]{pass_count} blocked[/green] · [red]{fail_count} missed[/red] · {total} total"
    )

    if fail_count == 0:
        console.print("  ✅ [green bold]All attacks blocked by policy[/green bold]")
    else:
        pct = (fail_count / total) * 100
        console.print(f"  ⚠️  [red bold]{fail_count} attacks ({pct:.0f}%) would succeed against this policy[/red bold]")

        console.print("\n  [bold]Recommended fixes:[/bold]")
        seen_tools: set[str] = set()
        denied_tools = [tool.lower() for tool in policy.denied_tools]
        approval_required = [tool.lower() for tool in policy.require_human_approval]
        allowed_tools = [tool.lower() for tool in policy.allowed_tools]

        for item in results:
            if item["result"] == "FAIL":
                tool = item["scenario"].expected_tool_call
                tool_lower = tool.lower()
                if tool in seen_tools:
                    continue

                seen_tools.add(tool)
                if tool_lower not in denied_tools:
                    console.print(f"    → Add [bold]{tool}[/bold] to denied_tools")
                if tool_lower not in allowed_tools and policy.allowed_tools:
                    pass
                if tool_lower not in approval_required:
                    console.print(f"    → Add [bold]{tool}[/bold] to require_human_approval")

    console.print()

    if fail_on_miss and fail_count > 0:
        sys.exit(1)
