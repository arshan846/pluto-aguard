"""Tests for finding suppression: .aguard.yaml and inline comments."""

from pathlib import Path

from pluto_aguard.models import Finding, Severity
from pluto_aguard.suppressions import apply_suppressions, load_ignore_rules


def _finding(
    id: str,
    category: str = "secrets",
    file_path: str | None = None,
    line_number: int | None = None,
) -> Finding:
    return Finding(
        id=id,
        title="Test finding",
        description="Test finding",
        severity=Severity.HIGH,
        category=category,
        file_path=file_path,
        line_number=line_number,
    )


class TestConfigSuppression:
    """Tests for .aguard.yaml-based suppression."""

    def test_no_ignore_file_suppresses_nothing(self, tmp_path: Path) -> None:
        findings = [_finding("SECRET-FOO-a.py-L1")]
        result = apply_suppressions(findings, tmp_path)
        assert result.kept == findings
        assert result.suppressed_count == 0

    def test_exact_id_match(self, tmp_path: Path) -> None:
        (tmp_path / ".aguard.yaml").write_text(
            "ignore:\n  - id: 'SECRET-FOO-a.py-L1'\n", encoding="utf-8"
        )
        findings = [_finding("SECRET-FOO-a.py-L1"), _finding("SECRET-FOO-b.py-L2")]
        result = apply_suppressions(findings, tmp_path)
        assert [f.id for f in result.kept] == ["SECRET-FOO-b.py-L2"]
        assert len(result.suppressed_by_config) == 1

    def test_rule_prefix_match(self, tmp_path: Path) -> None:
        (tmp_path / ".aguard.yaml").write_text(
            "ignore:\n  - rule: 'CONTEXT-NO-SESSION-LIMIT'\n", encoding="utf-8"
        )
        findings = [_finding("CONTEXT-NO-SESSION-LIMIT"), _finding("CONTEXT-NO-RESPONSE-LIMIT")]
        result = apply_suppressions(findings, tmp_path)
        assert [f.id for f in result.kept] == ["CONTEXT-NO-RESPONSE-LIMIT"]

    def test_category_match(self, tmp_path: Path) -> None:
        (tmp_path / ".aguard.yaml").write_text(
            "ignore:\n  - category: 'context_safety'\n", encoding="utf-8"
        )
        findings = [
            _finding("A", category="context_safety"),
            _finding("B", category="secrets"),
        ]
        result = apply_suppressions(findings, tmp_path)
        assert [f.id for f in result.kept] == ["B"]

    def test_path_glob_match(self, tmp_path: Path) -> None:
        (tmp_path / ".aguard.yaml").write_text(
            "ignore:\n  - path: 'tests/fixtures/*'\n", encoding="utf-8"
        )
        fixture_dir = tmp_path / "tests" / "fixtures"
        fixture_dir.mkdir(parents=True)
        fixture_file = fixture_dir / "sample.py"
        fixture_file.write_text("x = 1\n", encoding="utf-8")
        real_file = tmp_path / "app.py"
        real_file.write_text("y = 2\n", encoding="utf-8")

        findings = [
            _finding("A", file_path=str(fixture_file), line_number=1),
            _finding("B", file_path=str(real_file), line_number=1),
        ]
        result = apply_suppressions(findings, tmp_path)
        assert [f.id for f in result.kept] == ["B"]

    def test_malformed_yaml_does_not_crash(self, tmp_path: Path) -> None:
        (tmp_path / ".aguard.yaml").write_text("ignore: [this is not: valid: yaml", encoding="utf-8")
        rules = load_ignore_rules(tmp_path)
        assert rules == []


class TestInlineSuppression:
    """Tests for inline 'aguard-ignore' comment suppression."""

    def test_unscoped_marker_suppresses_all_findings_on_line(self, tmp_path: Path) -> None:
        source = tmp_path / "app.py"
        source.write_text('api_key = "sk-live-abc123"  # aguard-ignore\n', encoding="utf-8")
        findings = [_finding("SECRET-A", file_path=str(source), line_number=1)]
        result = apply_suppressions(findings, tmp_path)
        assert result.kept == []
        assert len(result.suppressed_inline) == 1

    def test_scoped_marker_only_suppresses_matching_prefix(self, tmp_path: Path) -> None:
        source = tmp_path / "app.py"
        source.write_text(
            'api_key = "sk-live-abc123"  # aguard-ignore: SECRET-OPENAI-KEY\n', encoding="utf-8"
        )
        matching = _finding("SECRET-OPENAI-KEY-app.py-L1", file_path=str(source), line_number=1)
        other = _finding("SECRET-GENERIC-SECRET-app.py-L1", file_path=str(source), line_number=1)
        result = apply_suppressions([matching, other], tmp_path)
        assert [f.id for f in result.kept] == ["SECRET-GENERIC-SECRET-app.py-L1"]
        assert len(result.suppressed_inline) == 1

    def test_scoped_marker_handles_dotted_finding_id(self, tmp_path: Path) -> None:
        """Per-instance finding IDs embed the filename (e.g. config.yaml),
        which contains a dot -- the inline scoping regex must not truncate
        the prefix at the first dot."""
        source = tmp_path / "config.yaml"
        source.write_text(
            'secret: "abc123def456"  # aguard-ignore: SECRET-GENERIC-SECRET-config.yaml-L1\n',
            encoding="utf-8",
        )
        finding = _finding("SECRET-GENERIC-SECRET-config.yaml-L1", file_path=str(source), line_number=1)
        result = apply_suppressions([finding], tmp_path)
        assert result.kept == []
        assert len(result.suppressed_inline) == 1

    def test_no_marker_on_line_is_not_suppressed(self, tmp_path: Path) -> None:
        source = tmp_path / "app.py"
        source.write_text('api_key = "sk-live-abc123"\n', encoding="utf-8")
        findings = [_finding("SECRET-A", file_path=str(source), line_number=1)]
        result = apply_suppressions(findings, tmp_path)
        assert len(result.kept) == 1

    def test_missing_file_does_not_crash(self, tmp_path: Path) -> None:
        findings = [_finding("SECRET-A", file_path=str(tmp_path / "missing.py"), line_number=1)]
        result = apply_suppressions(findings, tmp_path)
        assert len(result.kept) == 1
