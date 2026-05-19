"""Security baseline creation and drift detection."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console

from pluto_aguard.models import Finding, Severity
from pluto_aguard.scanners.mcp_scanner import scan_directory
from pluto_aguard.scanners.permission_scanner import (
    calculate_permission_risk_score,
    load_agent_config,
    scan_agent_permissions,
)
from pluto_aguard.scanners.runner import AGENT_CONFIG_FILES, _calculate_risk_score

console = Console()


def create_baseline(path: str, output_path: str = ".aguard-baseline.json") -> None:
    """Create a security baseline snapshot for a project."""
    project_path = Path(path).resolve()
    console.print("\n📏 [bold]Creating security baseline[/bold]\n")
    console.print(f"  [dim]Scanning project:[/dim] {project_path}")

    findings, permission_scores = _collect_project_state(project_path)
    risk_score = _calculate_risk_score(findings, permission_scores)

    baseline = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "project_path": str(project_path),
        "risk_score": risk_score.overall,
        "findings": [_serialize_finding(finding) for finding in findings],
        "finding_counts": {
            severity.value: int(risk_score.finding_count.get(severity, 0))
            for severity in Severity
        },
    }

    output_file = Path(output_path)
    output_file.write_text(json.dumps(baseline, indent=2), encoding="utf-8")
    console.print(f"\n  ✅ Baseline saved to [bold]{output_file}[/bold]\n")


def compare_baseline(path: str, baseline_path: str, fail_on_drift: bool = False) -> None:
    """Compare a project against a saved baseline and report drift."""
    project_path = Path(path).resolve()
    baseline_file = Path(baseline_path)
    baseline = json.loads(baseline_file.read_text(encoding="utf-8"))

    current_findings, permission_scores = _collect_project_state(project_path)
    current_risk_score = _calculate_risk_score(current_findings, permission_scores)

    baseline_findings = baseline.get("findings", [])
    baseline_by_id = {
        str(finding.get("id")): finding
        for finding in baseline_findings
        if isinstance(finding, dict) and finding.get("id")
    }
    current_by_id = {finding.id: finding for finding in current_findings}

    new_ids = sorted(set(current_by_id) - set(baseline_by_id))
    resolved_ids = sorted(set(baseline_by_id) - set(current_by_id))
    unchanged_ids = sorted(set(current_by_id) & set(baseline_by_id))

    baseline_score = float(baseline.get("risk_score", 0.0))
    current_score = current_risk_score.overall
    delta = round(current_score - baseline_score, 1)

    console.print("\n📏 [bold]Baseline Drift Report[/bold]\n")
    created_at = str(baseline.get("created_at", "unknown"))[:10]
    console.print(f"Baseline: {baseline_file} (created {created_at})\n")
    console.print(f"Risk Score: {baseline_score:.1f} → {current_score:.1f} ({_format_delta(delta)})\n")

    _print_findings_section("✅ Resolved", resolved_ids, baseline_by_id)
    _print_findings_section("🆕 New", new_ids, current_by_id)
    _print_findings_section("➡️ Unchanged", unchanged_ids, current_by_id)

    console.print(
        f"Summary: {len(resolved_ids)} resolved, {len(new_ids)} new, {len(unchanged_ids)} unchanged\n"
    )

    if fail_on_drift and new_ids:
        sys.exit(1)


def _collect_project_state(project_path: Path) -> tuple[list[Finding], list[float]]:
    findings = scan_directory(project_path)
    permission_scores: list[float] = []

    for config_name in AGENT_CONFIG_FILES:
        for config_file in project_path.rglob(config_name):
            try:
                config = load_agent_config(config_file)
            except (OSError, ValueError):
                continue

            findings.extend(scan_agent_permissions(config_file, config))
            permission_scores.append(calculate_permission_risk_score(config))

    return findings, permission_scores


def _serialize_finding(finding: Finding) -> dict[str, Any]:
    return {
        "id": finding.id,
        "title": finding.title,
        "severity": finding.severity.value,
        "category": finding.category,
        "owasp_id": finding.owasp_id,
        "file_path": finding.file_path,
    }


def _print_findings_section(title: str, finding_ids: list[str], findings: dict[str, Any]) -> None:
    console.print(f"{title} ({len(finding_ids)}):")
    if not finding_ids:
        console.print("  - None\n")
        return

    for finding_id in finding_ids:
        finding = findings[finding_id]
        console.print(f"  - {_format_finding(finding)}")
    console.print()


def _format_finding(finding: Any) -> str:
    if isinstance(finding, Finding):
        location = finding.file_path or "unknown location"
        if finding.line_number:
            location = f"{location}:{finding.line_number}"
        return f"{finding.title} in {location}"

    if isinstance(finding, dict):
        title = str(finding.get("title", finding.get("id", "Unknown finding")))
        file_path = finding.get("file_path")
        if file_path:
            return f"{title} in {file_path}"
        return title

    return str(finding)


def _format_delta(delta: float) -> str:
    if delta < 0:
        return f"↓ {abs(delta):.1f} points"
    if delta > 0:
        return f"↑ {delta:.1f} points"
    return "no change"
