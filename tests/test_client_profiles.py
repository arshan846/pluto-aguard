"""Tests for client-aware severity adjustment (--client flag)."""

import json
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from pluto_aguard.cli import main
from pluto_aguard.client_profiles import (
    get_client_profile,
    list_client_names,
    should_downgrade,
)

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def dangerous_config(tmp_path: Path) -> Path:
    """Create a config with a dangerous MCP server."""
    config = {
        "mcpServers": {
            "serena": {
                "command": "npx",
                "args": ["-y", "serena"],
            }
        }
    }
    config_file = tmp_path / "mcp.json"
    config_file.write_text(json.dumps(config), encoding="utf-8")
    return tmp_path


class TestClientProfiles:
    """Tests for the client_profiles module."""

    def test_list_client_names(self) -> None:
        names = list_client_names()
        assert "claude-desktop" in names
        assert "cursor" in names
        assert "vscode-copilot" in names
        assert "custom" in names

    def test_get_known_profile(self) -> None:
        profile = get_client_profile("claude-desktop")
        assert profile is not None
        assert profile.has_hitl is True
        assert profile.display_name == "Claude Desktop"

    def test_get_custom_profile(self) -> None:
        profile = get_client_profile("custom")
        assert profile is not None
        assert profile.has_hitl is False

    def test_get_none_returns_none(self) -> None:
        profile = get_client_profile(None)
        assert profile is None

    def test_get_unknown_returns_none(self) -> None:
        profile = get_client_profile("unknown-client")
        assert profile is None

    def test_should_downgrade_with_hitl_client(self) -> None:
        profile = get_client_profile("claude-desktop")
        assert should_downgrade("DANGEROUS-PKG-serena-shell-execution", profile)
        assert should_downgrade("DANGEROUS-POPULAR-serena-shell-execution", profile)

    def test_should_not_downgrade_non_dangerous(self) -> None:
        profile = get_client_profile("claude-desktop")
        assert not should_downgrade("AUTH-MISSING-myserver", profile)
        assert not should_downgrade("CONTEXT-NO-RESPONSE-LIMIT", profile)

    def test_should_not_downgrade_custom_client(self) -> None:
        profile = get_client_profile("custom")
        assert not should_downgrade("DANGEROUS-PKG-serena-shell-execution", profile)


class TestClientCLIFlag:
    """Tests for the --client CLI flag on the scan command."""

    def test_scan_without_client_flag(self, runner: CliRunner, dangerous_config: Path) -> None:
        """Default scan (no --client) should keep original severity."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            out_path = f.name
        result = runner.invoke(
            main, ["scan", str(dangerous_config), "--format", "json", "-o", out_path]
        )
        assert result.exit_code == 0
        with open(out_path, encoding="utf-8") as f:
            data = json.load(f)
        dangerous = [
            f for f in data["findings"]
            if f["id"].startswith("DANGEROUS-")
        ]
        # Without --client, dangerous server findings should be critical or high
        for finding in dangerous:
            assert finding["severity"] in ("critical", "high")
        Path(out_path).unlink(missing_ok=True)

    def test_scan_with_claude_desktop(self, runner: CliRunner, dangerous_config: Path) -> None:
        """--client claude-desktop should downgrade DANGEROUS findings to medium."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            out_path = f.name
        result = runner.invoke(
            main, ["scan", str(dangerous_config), "--format", "json", "-o", out_path, "--client", "claude-desktop"]
        )
        assert result.exit_code == 0
        with open(out_path, encoding="utf-8") as f:
            data = json.load(f)
        dangerous = [
            f for f in data["findings"]
            if f["id"].startswith("DANGEROUS-")
        ]
        for finding in dangerous:
            assert finding["severity"] == "medium"
            assert finding["metadata"]["downgraded_by_client"] == "claude-desktop"
            assert finding["metadata"]["original_severity"] == "critical_or_high"
        Path(out_path).unlink(missing_ok=True)

    def test_scan_with_custom_client(self, runner: CliRunner, dangerous_config: Path) -> None:
        """--client custom should keep original severity."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            out_path = f.name
        result = runner.invoke(
            main, ["scan", str(dangerous_config), "--format", "json", "-o", out_path, "--client", "custom"]
        )
        assert result.exit_code == 0
        with open(out_path, encoding="utf-8") as f:
            data = json.load(f)
        dangerous = [
            f for f in data["findings"]
            if f["id"].startswith("DANGEROUS-")
        ]
        for finding in dangerous:
            assert finding["severity"] in ("critical", "high")
        Path(out_path).unlink(missing_ok=True)

    def test_auth_missing_not_downgraded(self, runner: CliRunner, tmp_path: Path) -> None:
        """AUTH-MISSING should NOT be downgraded even with HITL client."""
        config = {
            "mcpServers": {
                "myserver": {
                    "url": "https://example.com/mcp",
                }
            }
        }
        config_file = tmp_path / "mcp.json"
        config_file.write_text(json.dumps(config), encoding="utf-8")
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            out_path = f.name
        result = runner.invoke(
            main, ["scan", str(tmp_path), "--format", "json", "-o", out_path, "--client", "claude-desktop"]
        )
        assert result.exit_code == 0
        with open(out_path, encoding="utf-8") as f:
            data = json.load(f)
        auth_findings = [
            f for f in data["findings"]
            if f["id"].startswith("AUTH-MISSING")
        ]
        for finding in auth_findings:
            assert finding["severity"] == "critical"
        Path(out_path).unlink(missing_ok=True)

    def test_client_noted_in_text_output(self, runner: CliRunner, dangerous_config: Path) -> None:
        """Text output should mention the client profile."""
        result = runner.invoke(
            main, ["scan", str(dangerous_config), "--client", "claude-desktop"],
            catch_exceptions=False,
        )
        assert "Claude Desktop" in result.output
        assert "HITL" in result.output

    def test_invalid_client_rejected(self, runner: CliRunner, dangerous_config: Path) -> None:
        """Invalid --client value should be rejected by Click."""
        result = runner.invoke(
            main, ["scan", str(dangerous_config), "--client", "nonexistent"]
        )
        assert result.exit_code == 2
