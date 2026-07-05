"""Tests for the permission scanner."""

from pathlib import Path

from pluto_aguard.models import Severity
from pluto_aguard.scanners.permission_scanner import (
    calculate_permission_risk_score,
    scan_agent_permissions,
)


class TestPermissionScanner:
    """Tests for agent permission analysis."""

    def test_flags_missing_permissions(self, tmp_path: Path) -> None:
        config = {
            "name": "test-agent",
            "tools": ["sql_query", "file_write"],
            # No permissions declared
        }
        findings = scan_agent_permissions(tmp_path / "agent.yaml", config)
        assert any("no declared permissions" in f.title.lower() for f in findings)

    def test_flags_dangerous_tools_without_hitl(self, tmp_path: Path) -> None:
        config = {
            "name": "test-agent",
            "tools": ["execute", "file_write", "shell"],
            "permissions": {"execute": {"scope": "full"}},
        }
        findings = scan_agent_permissions(tmp_path / "agent.yaml", config)
        assert any("without human approval" in f.title.lower() for f in findings)

    def test_flags_broad_data_access(self, tmp_path: Path) -> None:
        config = {
            "name": "test-agent",
            "tools": ["sql_query"],
            "data_access_rules": {
                "production_db": "all",
            },
        }
        findings = scan_agent_permissions(tmp_path / "agent.yaml", config)
        assert any("unrestricted" in f.title.lower() for f in findings)

    def test_flags_no_limits(self, tmp_path: Path) -> None:
        config = {
            "name": "test-agent",
            "tools": ["sql_query"],
        }
        findings = scan_agent_permissions(tmp_path / "agent.yaml", config)
        assert any("timeout" in f.title.lower() or "rate limit" in f.title.lower() for f in findings)

    def test_clean_config(self, tmp_path: Path) -> None:
        config = {
            "name": "safe-agent",
            "tools": ["sql_query"],
            "permissions": {"sql_query": {"scope": "read"}},
            "require_human_approval": ["execute", "file_write"],
            "timeout": 300,
            "rate_limit": {"calls_per_minute": 100},
        }
        findings = scan_agent_permissions(tmp_path / "agent.yaml", config)
        # Should have no high-severity findings
        high_or_above = [f for f in findings if f.severity in (Severity.CRITICAL, Severity.HIGH)]
        assert len(high_or_above) == 0


class TestRiskScoring:
    """Tests for permission risk score calculation."""

    def test_empty_config_low_score(self) -> None:
        score = calculate_permission_risk_score({})
        assert score == 0.0

    def test_dangerous_tools_high_score(self) -> None:
        config = {
            "tools": ["execute", "shell", "file_write"],
        }
        score = calculate_permission_risk_score(config)
        assert score > 50

    def test_hitl_reduces_score(self) -> None:
        base_config = {
            "tools": ["execute", "shell"],
        }
        hitl_config = {
            "tools": ["execute", "shell"],
            "require_human_approval": ["execute", "shell"],
        }
        base_score = calculate_permission_risk_score(base_config)
        hitl_score = calculate_permission_risk_score(hitl_config)
        assert hitl_score < base_score

    def test_scoped_permissions_reduce_score(self) -> None:
        base_config = {
            "tools": ["sql_query"],
        }
        scoped_config = {
            "tools": ["sql_query"],
            "permissions": {"sql_query": {"scope": "read"}},
        }
        base_score = calculate_permission_risk_score(base_config)
        scoped_score = calculate_permission_risk_score(scoped_config)
        assert scoped_score < base_score

    def test_read_only_access_reduces_score(self) -> None:
        base_config = {"tools": ["sql_query"]}
        readonly_config = {
            "tools": ["sql_query"],
            "permissions": {"sql_query": {"access": "read"}},
        }
        base_score = calculate_permission_risk_score(base_config)
        readonly_score = calculate_permission_risk_score(readonly_config)
        assert readonly_score < base_score

    def test_extended_schema_fields_not_penalized_when_unused(self) -> None:
        """A config that never touches network/runtime/auth/permission_model
        must not be penalized for lacking AgentGuard-specific vocabulary it
        was never told about."""
        without_extended = {
            "tools": ["sql_query"],
            "permissions": {"sql_query": {"scope": "read", "access": "read"}},
            "require_human_approval": ["sql_query"],
            "timeout": 300,
            "rate_limit": {"calls_per_minute": 50},
        }
        score = calculate_permission_risk_score(without_extended)
        assert score < 5.0

    def test_extended_schema_field_penalized_once_adopted(self) -> None:
        """Once a config engages with e.g. runtime.sandbox, an unsatisfied
        value there should count against the score."""
        base_config = {
            "tools": ["sql_query"],
            "permissions": {"sql_query": {"scope": "read", "access": "read"}},
            "require_human_approval": ["sql_query"],
            "timeout": 300,
            "rate_limit": {"calls_per_minute": 50},
        }
        adopted_but_unsandboxed = {**base_config, "runtime": {"sandbox": False}}
        adopted_and_sandboxed = {**base_config, "runtime": {"sandbox": True}}

        base_score = calculate_permission_risk_score(base_config)
        unsandboxed_score = calculate_permission_risk_score(adopted_but_unsandboxed)
        sandboxed_score = calculate_permission_risk_score(adopted_and_sandboxed)

        assert unsandboxed_score > base_score
        assert sandboxed_score < unsandboxed_score

    def test_well_configured_agent_scores_low(self) -> None:
        """Regression guard: a genuinely well-configured agent must score
        in the low-risk band, not be penalized into a false-high score by
        the fixed hardening-category baseline."""
        config = {
            "tools": ["sql_query"],
            "permissions": {"sql_query": {"scope": "read", "access": "read"}},
            "require_human_approval": ["sql_query"],
            "timeout": 300,
            "rate_limit": {"calls_per_minute": 50},
        }
        assert calculate_permission_risk_score(config) < 5.0
