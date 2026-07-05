"""Tests for OWASP control framework."""

from pathlib import Path

from pluto_aguard.controls.registry import CONTROLS, get_controls_by_command, get_controls_by_owasp
from pluto_aguard.controls.runner import evaluate_controls, run_owasp_report
from pluto_aguard.models import Finding, Severity


class TestControlRegistry:
    """Tests for OWASP control registry."""

    def test_controls_exist(self) -> None:
        assert len(CONTROLS) >= 15

    def test_all_controls_have_owasp_refs(self) -> None:
        for control in CONTROLS:
            assert len(control.owasp_refs) >= 1, f"Control {control.id} has no OWASP refs"

    def test_all_controls_have_ids(self) -> None:
        ids = [control.id for control in CONTROLS]
        assert len(ids) == len(set(ids)), "Duplicate control IDs found"

    def test_get_by_owasp(self) -> None:
        mcp01 = get_controls_by_owasp("MCP01:2025")
        assert len(mcp01) >= 2

    def test_get_by_command(self) -> None:
        scan_controls = get_controls_by_command("scan")
        assert len(scan_controls) >= 8


class TestControlEvaluation:
    """Tests for control evaluation logic."""

    def test_no_findings_all_pass(self) -> None:
        results = evaluate_controls([])
        scan_results = [result for result in results if result.command == "scan"]
        for result in scan_results:
            assert result.status == "pass"

    def test_secret_finding_fails_mcp01(self) -> None:
        findings = [
            Finding(
                id="test-1",
                title="Hardcoded secret",
                description="test",
                severity=Severity.HIGH,
                category="secrets",
                owasp_id="MCP01:2025",
            )
        ]
        results = evaluate_controls(findings)
        mcp01_results = [result for result in results if "MCP01:2025" in result.owasp_refs and result.command == "scan"]
        assert any(result.status == "fail" for result in mcp01_results)

    def test_permission_finding_fails_mcp02(self) -> None:
        findings = [
            Finding(
                id="PERM-WILDCARD-test-server",
                title="Wildcard permissions",
                description="test",
                severity=Severity.CRITICAL,
                category="permissions",
            )
        ]
        results = evaluate_controls(findings)
        mcp02_results = [result for result in results if "MCP02:2025" in result.owasp_refs and result.command == "scan"]
        assert any(result.status == "fail" for result in mcp02_results)

    def test_monitor_controls_not_tested(self) -> None:
        results = evaluate_controls([])
        monitor_results = [result for result in results if result.command == "monitor"]
        for result in monitor_results:
            assert result.status == "not_tested"

    def test_test_controls_not_tested(self) -> None:
        results = evaluate_controls([])
        test_results = [result for result in results if result.command == "test"]
        for result in test_results:
            assert result.status == "not_tested"


class TestOwaspReportSuppression:
    """run_owasp_report must respect .aguard.yaml, not just evaluate_controls."""

    def test_respects_aguard_yaml(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "mcp.json").write_text(
            '{"mcpServers": {"remote": {"url": "https://remote.example.com"}}}',
            encoding="utf-8",
        )

        without_suppression = run_owasp_report(str(project_dir))
        mcp07_before = [
            r for r in without_suppression if "MCP07:2025" in r.owasp_refs and r.command == "scan"
        ]
        assert any(r.status == "fail" for r in mcp07_before)

        (project_dir / ".aguard.yaml").write_text(
            "ignore:\n  - rule: 'AUTH-MISSING'\n", encoding="utf-8"
        )
        with_suppression = run_owasp_report(str(project_dir))
        auth_findings = [
            f
            for r in with_suppression
            for f in r.findings
            if f.id.startswith("AUTH-MISSING")
        ]
        assert auth_findings == []
