"""Scan runner — orchestrates all scanners and produces results."""

from __future__ import annotations

import sys
import time
from pathlib import Path

from rich.console import Console

from pluto_aguard.models import Finding, RiskScore, ScanResult, Severity
from pluto_aguard.scanners.mcp_scanner import scan_directory
from pluto_aguard.scanners.permission_scanner import (
    calculate_permission_risk_score,
    load_agent_config,
    scan_agent_permissions,
)

console = Console()

# Agent config file names to look for
AGENT_CONFIG_FILES = [
    "agent-config.yaml", "agent-config.yml", "agent-config.json",
    "agent.yaml", "agent.yml", "agent.json",
    "agents.yaml", "agents.yml",
]


def run_scan(
    path: str,
    output_format: str = "text",
    output_path: str | None = None,
    max_risk: float | None = None,
    fail_on: str | None = None,
) -> ScanResult:
    """Run a full security scan on the given path."""
    start_time = time.monotonic()
    project_path = Path(path).resolve()

    console.print(f"\n🔍 [bold]Scanning[/bold] {project_path}...\n")

    all_findings: list[Finding] = []
    scanned_files = 0

    # Run MCP config + secrets scanner
    console.print("  [dim]Scanning MCP configurations and secrets...[/dim]")
    mcp_findings = scan_directory(project_path)
    all_findings.extend(mcp_findings)

    # Run permission scanner on agent configs
    console.print("  [dim]Scanning agent permission configurations...[/dim]")
    perm_risk_scores: list[float] = []

    for config_name in AGENT_CONFIG_FILES:
        for config_file in project_path.rglob(config_name):
            try:
                config = load_agent_config(config_file)
                perm_findings = scan_agent_permissions(config_file, config)
                all_findings.extend(perm_findings)
                perm_risk_scores.append(calculate_permission_risk_score(config))
                scanned_files += 1
            except (OSError, ValueError):
                continue

    # Count scanned files
    scan_patterns = ["*.json", "*.yaml", "*.yml", "*.env", "*.py", "*.js", "*.ts", "*.toml"]
    for pattern in scan_patterns:
        scanned_files += len(list(project_path.rglob(pattern)))

    # Calculate overall risk score
    risk_score = _calculate_risk_score(all_findings, perm_risk_scores)

    elapsed_ms = int((time.monotonic() - start_time) * 1000)

    result = ScanResult(
        project_path=str(project_path),
        findings=all_findings,
        risk_score=risk_score,
        scanned_files=scanned_files,
        scan_duration_ms=elapsed_ms,
    )

    # Output results
    if output_format == "text":
        _print_text_report(result)
    elif output_format == "json":
        _print_json_report(result, output_path)
    elif output_format == "html":
        _generate_html_report(result, output_path)
    elif output_format == "sarif":
        _generate_sarif_report(result, output_path)

    _enforce_ci_gates(result, max_risk=max_risk, fail_on=fail_on)
    return result


def _calculate_risk_score(
    findings: list[Finding], perm_scores: list[float]
) -> RiskScore:
    """Calculate overall risk score from findings and permission analysis."""
    severity_counts = {s: 0 for s in Severity}
    for f in findings:
        severity_counts[f.severity] += 1

    # Weighted scoring
    finding_score = (
        severity_counts[Severity.CRITICAL] * 25
        + severity_counts[Severity.HIGH] * 15
        + severity_counts[Severity.MEDIUM] * 8
        + severity_counts[Severity.LOW] * 3
        + severity_counts[Severity.INFO] * 1
    )

    # Combine with permission risk scores
    avg_perm_score = sum(perm_scores) / len(perm_scores) if perm_scores else 0

    overall = min(100.0, (finding_score * 0.7) + (avg_perm_score * 0.3))

    return RiskScore(
        overall=round(overall, 1),
        breakdown={
            "findings": round(finding_score * 0.7, 1),
            "permissions": round(avg_perm_score * 0.3, 1),
        },
        finding_count=severity_counts,
    )


def _severity_color(severity: Severity) -> str:
    """Get Rich color for a severity level."""
    return {
        Severity.CRITICAL: "red bold",
        Severity.HIGH: "red",
        Severity.MEDIUM: "yellow",
        Severity.LOW: "blue",
        Severity.INFO: "dim",
    }[severity]


def _severity_icon(severity: Severity) -> str:
    """Get icon for a severity level."""
    return {
        Severity.CRITICAL: "🔴",
        Severity.HIGH: "🟠",
        Severity.MEDIUM: "🟡",
        Severity.LOW: "🔵",
        Severity.INFO: "⚪",
    }[severity]


def _risk_color(score: float) -> str:
    """Get color for a risk score."""
    if score >= 75:
        return "red bold"
    if score >= 50:
        return "yellow"
    if score >= 25:
        return "blue"
    return "green"


def _print_text_report(result: ScanResult) -> None:
    """Print scan results as formatted text."""
    if not result.findings:
        console.print("\n  ✅ [green bold]No security issues found![/green bold]\n")
        console.print(f"  📂 Scanned {result.scanned_files} files in {result.scan_duration_ms}ms")
        return

    # Print findings grouped by severity
    for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]:
        severity_findings = [f for f in result.findings if f.severity == severity]
        if not severity_findings:
            continue

        for finding in severity_findings:
            icon = _severity_icon(finding.severity)
            color = _severity_color(finding.severity)
            owasp = f" ({finding.owasp_id})" if finding.owasp_id else ""

            console.print(f"  {icon} [{color}]{finding.severity.value.upper()}[/{color}]: {finding.title}{owasp}")

            if finding.file_path:
                loc = finding.file_path
                if finding.line_number:
                    loc += f":{finding.line_number}"
                console.print(f"     [dim]📄 {loc}[/dim]")

            if finding.evidence:
                console.print(f"     [dim]Evidence: {finding.evidence}[/dim]")

    # Summary
    console.print()
    score = result.risk_score.overall
    color = _risk_color(score)

    # Risk score bar
    bar_filled = int(score / 2)
    bar_empty = 50 - bar_filled
    bar = "█" * bar_filled + "░" * bar_empty
    console.print(f"  📊 Risk Score: [{color}]{score}/100[/{color}] [{color}]{bar}[/{color}]")

    # Finding counts
    counts = result.risk_score.finding_count
    parts = []
    for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
        count = counts.get(sev, 0)
        if count > 0:
            parts.append(f"[{_severity_color(sev)}]{count} {sev.value}[/{_severity_color(sev)}]")
    if parts:
        console.print(f"  📋 Findings: {' · '.join(parts)}")

    console.print(f"  📂 Scanned {result.scanned_files} files in {result.scan_duration_ms}ms\n")


def _print_json_report(result: ScanResult, output_path: str | None) -> None:
    """Print or save scan results as JSON."""
    import json

    data = result.model_dump(mode="json")
    json_str = json.dumps(data, indent=2)

    if output_path:
        Path(output_path).write_text(json_str, encoding="utf-8")
        console.print(f"\n  📄 JSON report saved to: {output_path}\n")
    else:
        console.print(json_str)


def _generate_html_report(result: ScanResult, output_path: str | None) -> None:
    """Generate an HTML report."""
    from pluto_aguard.reports.html_report import generate_html

    output = output_path or "aguard-report.html"
    html = generate_html(result)
    Path(output).write_text(html, encoding="utf-8")
    console.print(f"\n  📄 HTML report saved to: {output}\n")


def _generate_sarif_report(result: ScanResult, output_path: str | None) -> None:
    """Generate a SARIF report."""
    from pluto_aguard.reports.sarif_report import generate_sarif

    output = output_path or "aguard-results.sarif"
    sarif_str = generate_sarif(result)
    Path(output).write_text(sarif_str, encoding="utf-8")
    console.print(f"\n  📄 SARIF report saved to: {output}\n")


def _enforce_ci_gates(result: ScanResult, max_risk: float | None, fail_on: str | None) -> None:
    """Apply CI failure thresholds after report generation."""
    if max_risk is not None and result.risk_score.overall > max_risk:
        console.print(
            f"  ❌ Risk score {result.risk_score.overall:.1f} exceeds --max-risk threshold of {max_risk:.1f}"
        )
        sys.exit(1)

    if not fail_on:
        return

    severity_order = {
        Severity.CRITICAL: 4,
        Severity.HIGH: 3,
        Severity.MEDIUM: 2,
        Severity.LOW: 1,
        Severity.INFO: 0,
    }
    threshold = Severity(fail_on)
    if any(severity_order[finding.severity] >= severity_order[threshold] for finding in result.findings):
        console.print(
            f"  ❌ Findings meeting --fail-on threshold '{fail_on}' were detected"
        )
        sys.exit(1)
