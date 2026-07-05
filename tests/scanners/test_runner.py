"""Tests for scan runner output formats and CI gates."""

import json
from pathlib import Path

import pytest

from pluto_aguard.scanners.runner import run_scan


class TestScanRunner:
    """Tests for end-to-end scan runner behavior."""

    def test_generates_sarif_report(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "mcp.json").write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "remote": {
                            "url": "https://remote.example.com",
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        output_path = tmp_path / "results.sarif"

        result = run_scan(str(project_dir), output_format="sarif", output_path=str(output_path))

        assert result.findings
        assert output_path.exists()
        sarif = json.loads(output_path.read_text(encoding="utf-8"))
        assert sarif["version"] == "2.1.0"
        assert sarif["runs"][0]["tool"]["driver"]["name"] == "pluto-aguard"

    def test_fail_on_threshold_exits_nonzero(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "mcp.json").write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "remote": {
                            "url": "https://remote.example.com",
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        with pytest.raises(SystemExit) as exc_info:
            run_scan(str(project_dir), output_format="json", fail_on="high")

        assert exc_info.value.code == 1

    def test_max_risk_threshold_exits_nonzero(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "mcp.json").write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "remote": {
                            "url": "https://remote.example.com",
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        with pytest.raises(SystemExit) as exc_info:
            run_scan(str(project_dir), output_format="text", max_risk=1.0)

        assert exc_info.value.code == 1

    def test_aguard_yaml_suppresses_findings(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "mcp.json").write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "remote": {
                            "url": "https://remote.example.com",
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        unsuppressed = run_scan(str(project_dir), output_format="json", quiet=True)
        assert unsuppressed.findings
        assert unsuppressed.suppressed_count == 0

        (project_dir / ".aguard.yaml").write_text(
            "ignore:\n  - rule: 'AUTH-MISSING'\n", encoding="utf-8"
        )

        suppressed = run_scan(str(project_dir), output_format="json", quiet=True)
        assert suppressed.suppressed_count == len(unsuppressed.findings) - len(suppressed.findings)
        assert not any(f.id.startswith("AUTH-MISSING") for f in suppressed.findings)

        forced = run_scan(str(project_dir), output_format="json", quiet=True, no_suppress=True)
        assert len(forced.findings) == len(unsuppressed.findings)
