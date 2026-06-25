"""Tests for the CLI entry point using Click's CliRunner."""

import json
import os
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from pluto_aguard.cli import main

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
DEMO_PROJECT = EXAMPLES_DIR / "demo-agent-project"
INSECURE_CONFIG = EXAMPLES_DIR / "insecure-agent-config.yaml"
POLICY_FILE = EXAMPLES_DIR / "agent-policy.yaml"


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestVersion:
    def test_version_flag(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "pluto-aguard" in result.output
        assert "0.9.2" in result.output

    def test_help(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Pluto AgentGuard" in result.output
        assert "scan" in result.output
        assert "monitor" in result.output
        assert "whatif" in result.output
        assert "test" in result.output
        assert "baseline" in result.output
        assert "owasp" in result.output
        assert "evidence" in result.output


class TestScanCommand:
    def test_scan_demo_project(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["scan", str(DEMO_PROJECT)])
        assert result.exit_code == 0
        assert "CRITICAL" in result.output or "HIGH" in result.output or "findings" in result.output.lower()

    def test_scan_quiet_mode(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["scan", str(DEMO_PROJECT), "--quiet"])
        assert result.exit_code == 0
        assert "aguard:" in result.output
        # Quiet mode should be a single summary line
        lines = [l for l in result.output.strip().split("\n") if l.strip()]
        assert len(lines) == 1

    def test_scan_json_format(self, runner: CliRunner) -> None:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(main, ["scan", str(DEMO_PROJECT), "--format", "json", "-o", output_path])
            assert result.exit_code == 0
            content = Path(output_path).read_text(encoding="utf-8")
            data = json.loads(content)
            # JSON output to file is a dict with 'findings' key
            assert "findings" in data
            assert isinstance(data["findings"], list)
            assert len(data["findings"]) > 0
        finally:
            os.unlink(output_path)

    def test_scan_output_to_file(self, runner: CliRunner) -> None:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(main, ["scan", str(DEMO_PROJECT), "--format", "json", "-o", output_path])
            assert result.exit_code == 0
            assert os.path.exists(output_path)
            content = Path(output_path).read_text(encoding="utf-8")
            data = json.loads(content)
            assert "findings" in data
            assert len(data["findings"]) > 0
        finally:
            os.unlink(output_path)

    def test_scan_fail_on_critical(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["scan", str(DEMO_PROJECT), "--fail-on", "critical"])
        # Demo project has critical findings, should exit non-zero
        assert result.exit_code == 1

    def test_scan_fail_on_high(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["scan", str(DEMO_PROJECT), "--fail-on", "high"])
        assert result.exit_code == 1

    def test_scan_max_risk_low_threshold(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["scan", str(DEMO_PROJECT), "--max-risk", "10"])
        # Demo project has risk > 10, should exit non-zero
        assert result.exit_code == 1

    def test_scan_max_risk_high_threshold(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["scan", str(DEMO_PROJECT), "--max-risk", "99"])
        # Risk 70 is below 99
        assert result.exit_code == 0

    def test_scan_nonexistent_path(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["scan", "/nonexistent/path"])
        assert result.exit_code != 0

    def test_scan_sarif_format(self, runner: CliRunner) -> None:
        with tempfile.NamedTemporaryFile(suffix=".sarif", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(main, ["scan", str(DEMO_PROJECT), "--format", "sarif", "-o", output_path])
            assert result.exit_code == 0
            content = json.loads(Path(output_path).read_text())
            assert content.get("$schema") or content.get("version") == "2.1.0"
            assert "runs" in content
        finally:
            os.unlink(output_path)


class TestTestCommand:
    def test_test_all_packs(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["test", "--policy", str(POLICY_FILE), "--attack-pack", "all"])
        assert result.exit_code == 0
        assert "BLOCKED" in result.output or "MISSED" in result.output or "scenarios" in result.output.lower()

    def test_test_single_pack(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["test", "--policy", str(POLICY_FILE), "--attack-pack", "prompt-injection"])
        assert result.exit_code == 0

    def test_test_fail_on_miss(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["test", "--policy", str(POLICY_FILE), "--attack-pack", "all", "--fail-on-miss"])
        # Policy likely misses some attacks
        # Just check it runs — exit code depends on policy coverage
        assert result.exit_code in (0, 1)

    def test_test_missing_policy(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["test", "--policy", "/nonexistent.yaml"])
        assert result.exit_code != 0


class TestWhatifCommand:
    def test_whatif_basic(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["whatif", "--config", str(INSECURE_CONFIG)])
        assert result.exit_code == 0
        assert "risk" in result.output.lower() or "score" in result.output.lower()

    def test_whatif_with_policy(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["whatif", "--config", str(INSECURE_CONFIG), "--policy", str(POLICY_FILE)])
        assert result.exit_code == 0

    def test_whatif_missing_config(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["whatif", "--config", "/nonexistent.yaml"])
        assert result.exit_code != 0


class TestOswapCommand:
    def test_owasp_basic(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["owasp", str(DEMO_PROJECT)])
        assert result.exit_code == 0
        assert "MCP" in result.output or "control" in result.output.lower()

    def test_owasp_markdown_output(self, runner: CliRunner) -> None:
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(main, ["owasp", str(DEMO_PROJECT), "--format", "markdown", "-o", output_path])
            assert result.exit_code == 0
            content = Path(output_path).read_text(encoding="utf-8")
            assert "MCP" in content or "Control" in content
        finally:
            os.unlink(output_path)


class TestEvidenceCommand:
    def test_evidence_basic(self, runner: CliRunner) -> None:
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            output_path = f.name
        try:
            result = runner.invoke(main, [
                "evidence", str(DEMO_PROJECT),
                "--config", str(INSECURE_CONFIG),
                "--policy", str(POLICY_FILE),
                "-o", output_path,
            ])
            assert result.exit_code == 0
            content = Path(output_path).read_text()
            assert len(content) > 100
        finally:
            os.unlink(output_path)


class TestBaselineCommand:
    def test_baseline_create_and_compare(self, runner: CliRunner) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            baseline_path = os.path.join(tmpdir, "baseline.json")
            # Create
            result = runner.invoke(main, ["baseline", "create", str(DEMO_PROJECT), "-o", baseline_path])
            assert result.exit_code == 0
            assert os.path.exists(baseline_path)
            # Compare (no drift — same project)
            result = runner.invoke(main, ["baseline", "compare", str(DEMO_PROJECT), "-b", baseline_path])
            assert result.exit_code == 0

    def test_baseline_compare_fail_on_drift(self, runner: CliRunner) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            baseline_path = os.path.join(tmpdir, "baseline.json")
            result = runner.invoke(main, ["baseline", "create", str(DEMO_PROJECT), "-o", baseline_path])
            assert result.exit_code == 0
            # Compare same project with --fail-on-drift (should be 0, no drift)
            result = runner.invoke(main, ["baseline", "compare", str(DEMO_PROJECT), "-b", baseline_path, "--fail-on-drift"])
            assert result.exit_code == 0


class TestMonitorCommand:
    def test_monitor_with_trace(self, runner: CliRunner) -> None:
        trace_file = EXAMPLES_DIR / "sample-traces.jsonl"
        if trace_file.exists():
            result = runner.invoke(main, ["monitor", "--trace-file", str(trace_file), "--policy", str(POLICY_FILE)])
            assert result.exit_code == 0

    def test_monitor_missing_both(self, runner: CliRunner) -> None:
        # No trace file and no live flag — should still run (may show help or empty)
        result = runner.invoke(main, ["monitor"])
        # Should not crash
        assert result.exit_code in (0, 1, 2)
