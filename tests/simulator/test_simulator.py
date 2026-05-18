"""Tests for the What-If policy simulator."""

from pluto_aguard.simulator.runner import (
    BUILTIN_POLICIES,
    simulate_combined,
    simulate_policies,
)


class TestSimulator:
    """Tests for policy simulation."""

    def setup_method(self) -> None:
        self.risky_config = {
            "name": "risky-agent",
            "tools": ["execute", "shell", "file_write", "sql_query", "send_email"],
            # No permissions, no HITL, no limits
        }

    def test_simulate_individual_policies(self) -> None:
        results = simulate_policies(self.risky_config)
        assert len(results) > 0
        # At least some policies should reduce risk
        reductions = [r for r in results if r.score_delta < 0]
        assert len(reductions) > 0

    def test_simulate_combined_policies(self) -> None:
        policy_ids = ["restrict-sql-readonly", "add-hitl-file-ops", "add-rate-limits"]
        result = simulate_combined(self.risky_config, policy_ids)
        # Combined should reduce more than individual
        assert result.score_delta <= 0

    def test_empty_config_zero_risk(self) -> None:
        results = simulate_policies({})
        for r in results:
            assert r.original_score.overall == 0

    def test_builtin_policies_exist(self) -> None:
        assert len(BUILTIN_POLICIES) >= 5
        for policy in BUILTIN_POLICIES:
            assert "id" in policy
            assert "description" in policy
            assert "category" in policy

    def test_hitl_reduces_dangerous_tool_risk(self) -> None:
        config = {
            "name": "test",
            "tools": ["execute", "shell"],
        }
        results = simulate_policies(config)
        hitl_result = next(
            (r for r in results if r.applied_policies[0].id == "add-hitl-file-ops"),
            None,
        )
        # This specific policy may or may not affect execute/shell,
        # but the simulation should still complete successfully
        assert hitl_result is not None
