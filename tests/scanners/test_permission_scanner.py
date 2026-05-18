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
