"""Tests for security baselines and drift detection."""

import json
from pathlib import Path

import pytest

from pluto_aguard.baseline.runner import compare_baseline, create_baseline


class TestBaselineRunner:
    """Tests for baseline creation and comparison."""

    def test_create_baseline_writes_valid_json(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "mcp.json").write_text(
            '{"mcpServers": {"remote": {"url": "https://remote.example.com"}}}',
            encoding="utf-8",
        )
        baseline_file = tmp_path / ".aguard-baseline.json"

        create_baseline(str(project_dir), output_path=str(baseline_file))

        assert baseline_file.exists()
        data = json.loads(baseline_file.read_text(encoding="utf-8"))
        assert "created_at" in data
        assert data["project_path"] == str(project_dir.resolve())
        assert isinstance(data["risk_score"], float)
        assert isinstance(data["findings"], list)
        assert data["findings"]

    def test_compare_baseline_detects_new_findings(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        baseline_file = tmp_path / ".aguard-baseline.json"

        create_baseline(str(project_dir), output_path=str(baseline_file))
        (project_dir / "mcp.json").write_text(
            '{"mcpServers": {"remote": {"url": "https://remote.example.com"}}}',
            encoding="utf-8",
        )

        compare_baseline(str(project_dir), baseline_path=str(baseline_file))

        output = capsys.readouterr().out
        # Should detect new findings (auth + context safety checks)
        assert "New" in output
        assert "No authentication configured for remote MCP server 'remote'" in output

    def test_compare_baseline_detects_resolved_findings(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "mcp.json").write_text(
            '{"mcpServers": {"remote": {"url": "https://remote.example.com"}}}',
            encoding="utf-8",
        )
        baseline_file = tmp_path / ".aguard-baseline.json"

        create_baseline(str(project_dir), output_path=str(baseline_file))
        (project_dir / "mcp.json").write_text(
            '{"mcpServers": {"remote": {"url": "https://remote.example.com", "auth": {"token": "${TOKEN}"}}}}',
            encoding="utf-8",
        )

        compare_baseline(str(project_dir), baseline_path=str(baseline_file))

        output = capsys.readouterr().out
        assert "✅ Resolved (1):" in output
        assert "No authentication configured for remote MCP server 'remote'" in output

    def test_fail_on_drift_raises_system_exit(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        baseline_file = tmp_path / ".aguard-baseline.json"

        create_baseline(str(project_dir), output_path=str(baseline_file))
        (project_dir / "mcp.json").write_text(
            '{"mcpServers": {"remote": {"url": "https://remote.example.com"}}}',
            encoding="utf-8",
        )

        with pytest.raises(SystemExit) as exc_info:
            compare_baseline(
                str(project_dir),
                baseline_path=str(baseline_file),
                fail_on_drift=True,
            )

        assert exc_info.value.code == 1
