"""Tests for launch readiness evidence generation."""

from pathlib import Path

from pluto_aguard.evidence.runner import run_evidence


class TestEvidenceRunner:
    """Tests for evidence report generation."""

    def test_generates_markdown_file(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "mcp.json").write_text(
            '{"mcpServers": {"remote": {"url": "https://remote.example.com"}}}',
            encoding="utf-8",
        )
        output_file = tmp_path / "launch-readiness.md"

        run_evidence(str(project_dir), output_path=str(output_file))

        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert "# Agent Launch Readiness Packet" in content

    def test_includes_risk_score(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "mcp.json").write_text(
            '{"mcpServers": {"remote": {"url": "https://remote.example.com"}}}',
            encoding="utf-8",
        )
        output_file = tmp_path / "launch-readiness.md"

        run_evidence(str(project_dir), output_path=str(output_file))

        content = output_file.read_text(encoding="utf-8")
        assert "**Overall Risk Score:**" in content
        assert "/100" in content

    def test_includes_launch_checklist(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        output_file = tmp_path / "launch-readiness.md"

        run_evidence(str(project_dir), output_path=str(output_file))

        content = output_file.read_text(encoding="utf-8")
        assert "## Launch Approval Checklist" in content
        assert "- [ ] All CRITICAL findings resolved" in content
        assert "- [ ] Behavioral monitoring enabled" in content

    def test_supports_config_and_policy_files(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        config_file = tmp_path / "agent-config.yaml"
        policy_file = tmp_path / "policy.yaml"
        output_file = tmp_path / "launch-readiness.md"

        config_file.write_text(
            """
name: review-agent
tools:
  - sql_query
  - file_write
permissions:
  sql_query:
    scope: read
  file_write:
    scope: workspace
require_human_approval:
  - file_write
timeout: 300
rate_limit:
  calls_per_minute: 100
""".strip(),
            encoding="utf-8",
        )
        policy_file.write_text(
            """
name: review-policy
allowed_tools:
  - sql_query
denied_tools:
  - execute
require_human_approval:
  - file_write
data_access_rules:
  production_db: read
""".strip(),
            encoding="utf-8",
        )

        run_evidence(
            str(project_dir),
            config_path=str(config_file),
            policy_path=str(policy_file),
            output_path=str(output_file),
        )

        content = output_file.read_text(encoding="utf-8")
        assert "`sql_query`: read" in content
        assert "**Allowed tools:** sql_query" in content
        assert "**Denied tools:** execute" in content

    def test_respects_aguard_yaml_suppression(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "mcp.json").write_text(
            '{"mcpServers": {"remote": {"url": "https://remote.example.com"}}}',
            encoding="utf-8",
        )
        (project_dir / ".aguard.yaml").write_text(
            "ignore:\n  - rule: 'AUTH-MISSING'\n", encoding="utf-8"
        )
        output_file = tmp_path / "launch-readiness.md"

        run_evidence(str(project_dir), output_path=str(output_file))

        content = output_file.read_text(encoding="utf-8")
        assert "No authentication configured" not in content

    def test_handles_missing_config_and_policy(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        output_file = tmp_path / "launch-readiness.md"

        run_evidence(str(project_dir), output_path=str(output_file))

        content = output_file.read_text(encoding="utf-8")
        assert "**Config file:** Not provided" in content
        assert "**Policy file:** Not provided" in content
        assert "- Config not provided." in content
        assert "- Policy not provided." in content
