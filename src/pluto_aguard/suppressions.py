"""Finding suppression: project-level ignore rules and inline comments.

Two ways to silence a finding without disabling the check for everyone:

1. A `.aguard.yaml` (or `.aguard.yml`) file at the project root:

   ignore:
     - id: "SECRET-GENERIC-SECRET-config.yaml-L12"   # exact Finding.id
       reason: "rotated test fixture, not a real credential"
     - rule: "CONTEXT-NO-SESSION-LIMIT"               # Finding.id prefix match
       reason: "session limits enforced by the MCP client, not this config"
     - category: "context_safety"                     # Finding.category match
     - path: "tests/fixtures/**"                       # fnmatch against file_path
                                                        # relative to project root

2. An inline comment on the offending line, for findings tied to a specific
   file/line:

     api_key = "sk-live-abc123"  # aguard-ignore
     api_key = "sk-live-abc123"  # aguard-ignore: SECRET-OPENAI-KEY

   With no rule listed, all findings on that line are suppressed. With a
   comma-separated list, only findings whose id starts with one of the
   given prefixes are suppressed.

Suppressed findings are never silently dropped from the numbers reported by
`aguard scan` -- callers get a count of what was suppressed and why.
"""

from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from pluto_aguard.models import Finding

_IGNORE_FILENAMES = (".aguard.yaml", ".aguard.yml")

_INLINE_MARKER = re.compile(r"aguard-ignore(?::\s*([\w,\-]+))?", re.IGNORECASE)


@dataclass
class IgnoreRule:
    """A single entry from a `.aguard.yaml` ignore list."""

    id: str | None = None
    rule: str | None = None
    category: str | None = None
    path: str | None = None
    reason: str | None = None


@dataclass
class SuppressionResult:
    """Findings split into kept vs. suppressed, with the reason for each."""

    kept: list[Finding] = field(default_factory=list)
    suppressed_by_config: list[Finding] = field(default_factory=list)
    suppressed_inline: list[Finding] = field(default_factory=list)

    @property
    def suppressed_count(self) -> int:
        return len(self.suppressed_by_config) + len(self.suppressed_inline)


def load_ignore_rules(project_path: Path) -> list[IgnoreRule]:
    """Load ignore rules from `.aguard.yaml`/`.aguard.yml` at the project root."""
    for filename in _IGNORE_FILENAMES:
        config_file = project_path / filename
        if not config_file.exists():
            continue
        try:
            data = yaml.safe_load(config_file.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError):
            return []
        if not isinstance(data, dict):
            return []
        raw_rules = data.get("ignore", [])
        if not isinstance(raw_rules, list):
            return []
        return [
            IgnoreRule(
                id=raw.get("id"),
                rule=raw.get("rule"),
                category=raw.get("category"),
                path=raw.get("path"),
                reason=raw.get("reason"),
            )
            for raw in raw_rules
            if isinstance(raw, dict)
        ]
    return []


def _relative_path(finding: Finding, project_path: Path) -> str:
    if not finding.file_path:
        return ""
    try:
        rel = Path(finding.file_path).resolve().relative_to(project_path.resolve())
    except (OSError, ValueError):
        return finding.file_path.replace("\\", "/")
    return str(rel).replace("\\", "/")


def _matches_rule(finding: Finding, rule: IgnoreRule, project_path: Path) -> bool:
    if rule.id and finding.id == rule.id:
        return True
    if rule.rule and finding.id.startswith(rule.rule):
        return True
    if rule.category and finding.category == rule.category:
        return True
    if rule.path and finding.file_path:
        if fnmatch.fnmatch(_relative_path(finding, project_path), rule.path):
            return True
    return False


def _inline_suppression_prefixes(line: str) -> list[str] | None:
    """None = no marker on this line. [] = unscoped (suppress everything).

    A non-empty list scopes suppression to findings whose id starts with
    one of the given prefixes.
    """
    match = _INLINE_MARKER.search(line)
    if not match:
        return None
    if not match.group(1):
        return []
    return [prefix.strip() for prefix in match.group(1).split(",") if prefix.strip()]


def _is_inline_suppressed(finding: Finding, line_cache: dict[str, list[str]]) -> bool:
    if not finding.file_path or not finding.line_number:
        return False

    lines = line_cache.get(finding.file_path)
    if lines is None:
        try:
            lines = Path(finding.file_path).read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            lines = []
        line_cache[finding.file_path] = lines

    index = finding.line_number - 1
    if index < 0 or index >= len(lines):
        return False

    prefixes = _inline_suppression_prefixes(lines[index])
    if prefixes is None:
        return False
    if not prefixes:
        return True
    return any(finding.id.startswith(prefix) for prefix in prefixes)


def apply_suppressions(findings: list[Finding], project_path: Path) -> SuppressionResult:
    """Split findings into kept vs. suppressed based on config + inline rules."""
    rules = load_ignore_rules(project_path)
    result = SuppressionResult()
    line_cache: dict[str, list[str]] = {}

    for finding in findings:
        if any(_matches_rule(finding, rule, project_path) for rule in rules):
            result.suppressed_by_config.append(finding)
            continue
        if _is_inline_suppressed(finding, line_cache):
            result.suppressed_inline.append(finding)
            continue
        result.kept.append(finding)

    return result
