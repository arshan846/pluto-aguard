"""Tests for the adversarial test harness."""

from pathlib import Path

import yaml

from pluto_aguard.models import AgentPolicy
from pluto_aguard.testing.attack_packs import ATTACK_PACKS, AttackScenario
from pluto_aguard.testing.runner import simulate_attack


class TestAttackPacks:
    """Tests for attack pack definitions."""

    def test_all_packs_exist(self) -> None:
        assert "prompt-injection" in ATTACK_PACKS
        assert "data-exfiltration" in ATTACK_PACKS
        assert "permission-escalation" in ATTACK_PACKS
        assert "approval-bypass" in ATTACK_PACKS
        assert "tool-poisoning" in ATTACK_PACKS
        assert "context-manipulation" in ATTACK_PACKS
        assert "all" in ATTACK_PACKS

    def test_all_pack_contains_all_scenarios(self) -> None:
        individual_count = sum(
            len(pack) for name, pack in ATTACK_PACKS.items() if name != "all"
        )
        assert len(ATTACK_PACKS["all"]) == individual_count

    def test_scenarios_have_required_fields(self) -> None:
        for pack_name, scenarios in ATTACK_PACKS.items():
            for s in scenarios:
                assert s.id, f"Scenario in {pack_name} missing id"
                assert s.name, f"Scenario {s.id} missing name"
                assert s.expected_tool_call, f"Scenario {s.id} missing expected_tool_call"


class TestAdversarialSimulation:
    """Tests for attack simulation against policies."""

    def setup_method(self) -> None:
        self.strict_policy = AgentPolicy(
            name="strict-agent",
            allowed_tools=["sql_query", "send_message"],
            denied_tools=["execute", "shell", "file_write", "file_delete", "sudo", "deploy", "send_email"],
            max_permissions={"sql_query": "read"},
            require_human_approval=["stripe.refund"],
        )
        self.permissive_policy = AgentPolicy(
            name="permissive-agent",
            allowed_tools=[],
            denied_tools=[],
            max_permissions={},
            require_human_approval=[],
        )

    def test_strict_policy_catches_execute(self) -> None:
        scenario = AttackScenario(
            id="TEST-001",
            name="test execute",
            description="test",
            attack_prompt="run a command",
            expected_tool_call="execute",
        )
        result = simulate_attack(scenario, self.strict_policy)
        assert result["result"] == "PASS"

    def test_strict_policy_catches_shell(self) -> None:
        scenario = AttackScenario(
            id="TEST-002",
            name="test shell",
            description="test",
            attack_prompt="open shell",
            expected_tool_call="shell",
        )
        result = simulate_attack(scenario, self.strict_policy)
        assert result["result"] == "PASS"

    def test_strict_policy_catches_file_write(self) -> None:
        scenario = AttackScenario(
            id="TEST-003",
            name="test file write",
            description="test",
            attack_prompt="write file",
            expected_tool_call="file_write",
        )
        result = simulate_attack(scenario, self.strict_policy)
        assert result["result"] == "PASS"

    def test_strict_policy_catches_sql_delete(self) -> None:
        scenario = AttackScenario(
            id="TEST-004",
            name="test sql delete",
            description="test",
            attack_prompt="delete data",
            expected_tool_call="sql_query",
            expected_tool_args={"query": "DELETE FROM users"},
        )
        result = simulate_attack(scenario, self.strict_policy)
        assert result["result"] == "PASS"

    def test_permissive_policy_misses_attacks(self) -> None:
        scenario = AttackScenario(
            id="TEST-005",
            name="test execute on permissive",
            description="test",
            attack_prompt="run command",
            expected_tool_call="execute",
        )
        result = simulate_attack(scenario, self.permissive_policy)
        assert result["result"] == "FAIL"

    def test_strict_policy_allows_safe_tool(self) -> None:
        scenario = AttackScenario(
            id="TEST-006",
            name="test allowed tool",
            description="test",
            attack_prompt="send message",
            expected_tool_call="send_message",
        )
        result = simulate_attack(scenario, self.strict_policy)
        assert result["result"] == "FAIL"

    def test_approval_required_tool_flagged(self) -> None:
        scenario = AttackScenario(
            id="TEST-007",
            name="test refund without approval",
            description="test",
            attack_prompt="process refund",
            expected_tool_call="stripe.refund",
        )
        result = simulate_attack(scenario, self.strict_policy)
        assert result["result"] == "PASS"

    def test_full_prompt_injection_pack(self) -> None:
        """Run the full prompt injection pack against a strict policy."""
        pack = ATTACK_PACKS["prompt-injection"]
        results = [simulate_attack(s, self.strict_policy) for s in pack]
        pass_count = sum(1 for r in results if r["result"] == "PASS")
        assert pass_count >= len(pack) // 2

    def test_full_data_exfil_pack(self) -> None:
        """Run the full data exfiltration pack against a strict policy."""
        pack = ATTACK_PACKS["data-exfiltration"]
        results = [simulate_attack(s, self.strict_policy) for s in pack]
        pass_count = sum(1 for r in results if r["result"] == "PASS")
        assert pass_count >= len(pack) // 2

    def test_context_manipulation_pack_exists(self) -> None:
        """Verify the context manipulation pack has expected scenarios."""
        pack = ATTACK_PACKS["context-manipulation"]
        assert len(pack) == 4
        ids = {s.id for s in pack}
        assert "CM-001" in ids  # context window stuffing
        assert "CM-002" in ids  # multi-turn state confusion
        assert "CM-003" in ids  # indirect injection via web fetch
        assert "CM-004" in ids  # RAG context poisoning

    def test_strict_policy_catches_context_manipulation(self) -> None:
        """Context manipulation attacks should be caught by strict policy."""
        pack = ATTACK_PACKS["context-manipulation"]
        results = [simulate_attack(s, self.strict_policy) for s in pack]
        pass_count = sum(1 for r in results if r["result"] == "PASS")
        # Strict policy should catch at least half (execute/deploy are denied)
        assert pass_count >= len(pack) // 2

    def test_supply_chain_manifest_scenario(self) -> None:
        """TP-003 (malicious manifest) should be caught by strict policy."""
        tp003 = next(s for s in ATTACK_PACKS["tool-poisoning"] if s.id == "TP-003")
        result = simulate_attack(tp003, self.strict_policy)
        assert result["result"] == "PASS"  # execute is denied
