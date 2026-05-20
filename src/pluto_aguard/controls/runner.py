"""OWASP coverage report generator.

Evaluates which OWASP controls pass/fail based on scan findings,
and generates a coverage report.
"""

from __future__ import annotations

from pathlib import Path

from rich.console import Console

from pluto_aguard.controls.registry import CONTROLS
from pluto_aguard.models import ControlResult, Finding
from pluto_aguard.scanners.ai_config_scanner import scan_ai_configs
from pluto_aguard.scanners.mcp_scanner import scan_directory
from pluto_aguard.scanners.permission_scanner import load_agent_config, scan_agent_permissions

console = Console()

AGENT_CONFIG_FILES = [
    "agent-config.yaml",
    "agent-config.yml",
    "agent-config.json",
    "agent.yaml",
    "agent.yml",
    "agent.json",
]

OWASP_MCP_RISKS = [
    ("MCP01:2025", "Token Mismanagement & Secret Exposure"),
    ("MCP02:2025", "Privilege Escalation via Scope Creep"),
    ("MCP03:2025", "Tool Poisoning"),
    ("MCP04:2025", "Supply Chain & Dependency Tampering"),
    ("MCP05:2025", "Command Injection & Execution"),
    ("MCP06:2025", "Intent Flow Subversion"),
    ("MCP07:2025", "Insufficient Authentication & Authorization"),
    ("MCP08:2025", "Lack of Audit and Telemetry"),
    ("MCP09:2025", "Shadow MCP Servers"),
    ("MCP10:2025", "Context Injection & Over-Sharing"),
]


def evaluate_controls(all_findings: list[Finding]) -> list[ControlResult]:
    """Evaluate control results based on scan findings."""
    results: list[ControlResult] = []

    for control in CONTROLS:
        matching_findings = [finding for finding in all_findings if finding.category == control.category]

        if control.command in ("test", "monitor", "evidence", "baseline"):
            results.append(
                ControlResult(
                    control_id=control.id,
                    owasp_refs=control.owasp_refs,
                    title=control.title,
                    status="not_tested",
                    command=control.command,
                    findings=[],
                    remediation=f"Run 'aguard {control.command}' to evaluate this control.",
                )
            )
        elif matching_findings:
            results.append(
                ControlResult(
                    control_id=control.id,
                    owasp_refs=control.owasp_refs,
                    title=control.title,
                    status="fail",
                    command=control.command,
                    findings=matching_findings,
                    remediation=matching_findings[0].remediation or "",
                )
            )
        else:
            results.append(
                ControlResult(
                    control_id=control.id,
                    owasp_refs=control.owasp_refs,
                    title=control.title,
                    status="pass",
                    command=control.command,
                    findings=[],
                )
            )

    return results


def run_owasp_report(
    path: str,
    output_format: str = "text",
    output_path: str | None = None,
) -> list[ControlResult]:
    """Generate an OWASP coverage report."""
    project_path = Path(path).resolve()

    console.print("\n🛡️  [bold]OWASP Coverage Report[/bold]\n")
    console.print(f"  Project: {project_path}\n")
    console.print("  [dim]Running security scans...[/dim]")

    all_findings: list[Finding] = []
    all_findings.extend(scan_directory(project_path))
    all_findings.extend(scan_ai_configs(project_path))

    for config_name in AGENT_CONFIG_FILES:
        for config_file in project_path.rglob(config_name):
            try:
                config = load_agent_config(config_file)
                all_findings.extend(scan_agent_permissions(config_file, config))
            except (OSError, ValueError):
                continue

    control_results = evaluate_controls(all_findings)

    if output_format == "text":
        _print_text_report(control_results)
    elif output_format == "markdown":
        markdown_report = _generate_markdown_report(control_results)
        if output_path:
            Path(output_path).write_text(markdown_report, encoding="utf-8")
            console.print(f"\n  📄 Report saved to: {output_path}\n")
        else:
            console.print(markdown_report, markup=False)

    _print_summary(control_results)

    return control_results


def _print_text_report(results: list[ControlResult]) -> None:
    """Print OWASP coverage as a Rich table grouped by risk."""
    for owasp_id, owasp_name in OWASP_MCP_RISKS:
        risk_controls = [result for result in results if owasp_id in result.owasp_refs]

        if not risk_controls:
            console.print(f"  [dim]{owasp_id} {owasp_name}: [yellow]no controls[/yellow][/dim]")
            continue

        statuses = [result.status for result in risk_controls]
        if "fail" in statuses:
            risk_icon = "❌"
            risk_color = "red"
        elif all(status == "pass" for status in statuses):
            risk_icon = "✅"
            risk_color = "green"
        elif "not_tested" in statuses and "fail" not in statuses:
            risk_icon = "⚠️"
            risk_color = "yellow"
        else:
            risk_icon = "🟡"
            risk_color = "yellow"

        fail_count = statuses.count("fail")
        pass_count = statuses.count("pass")
        not_tested = statuses.count("not_tested")

        parts: list[str] = []
        if fail_count:
            parts.append(f"[red]{fail_count} failed[/red]")
        if pass_count:
            parts.append(f"[green]{pass_count} passed[/green]")
        if not_tested:
            parts.append(f"[yellow]{not_tested} not tested[/yellow]")

        console.print(f"  {risk_icon} [{risk_color}]{owasp_id}[/{risk_color}] {owasp_name}: {', '.join(parts)}")

        for control in risk_controls:
            status_icons = {
                "pass": "[green]✓[/green]",
                "fail": "[red]✗[/red]",
                "not_tested": "[yellow]○[/yellow]",
                "warning": "[yellow]![/yellow]",
            }
            icon = status_icons.get(control.status, "?")
            console.print(f"    {icon} {control.control_id}: {control.title}")
            if control.status == "fail" and control.findings:
                console.print(f"      [dim]→ {len(control.findings)} finding(s)[/dim]")

        console.print()


def _generate_markdown_report(results: list[ControlResult]) -> str:
    """Generate OWASP coverage as Markdown."""
    lines = ["# OWASP Coverage Report", "", "Generated by Pluto AgentGuard", ""]

    for owasp_id, owasp_name in OWASP_MCP_RISKS:
        risk_controls = [result for result in results if owasp_id in result.owasp_refs]
        if not risk_controls:
            lines.append(f"## {owasp_id} — {owasp_name}")
            lines.append("No controls implemented yet.")
            lines.append("")
            continue

        statuses = [result.status for result in risk_controls]
        fail_count = statuses.count("fail")
        pass_count = statuses.count("pass")
        status_label = "FAIL" if fail_count else "PASS" if pass_count == len(statuses) else "PARTIAL"

        lines.append(f"## {owasp_id} — {owasp_name} [{status_label}]")
        lines.append("")

        for control in risk_controls:
            icon = {"pass": "✅", "fail": "❌", "not_tested": "⚠️"}.get(control.status, "?")
            lines.append(f"- {icon} **{control.control_id}**: {control.title} — **{control.status.upper()}**")
            if control.status == "fail" and control.findings:
                for finding in control.findings[:3]:
                    lines.append(f"  - {finding.title}")
            if control.remediation:
                lines.append(f"  - 💡 {control.remediation}")

        lines.append("")

    return "\n".join(lines)


def _print_summary(results: list[ControlResult]) -> None:
    """Print summary statistics."""
    total = len(results)
    passed = sum(1 for result in results if result.status == "pass")
    failed = sum(1 for result in results if result.status == "fail")
    not_tested = sum(1 for result in results if result.status == "not_tested")

    covered_risks: set[str] = set()
    for result in results:
        if result.status != "not_tested":
            covered_risks.update(result.owasp_refs)
    mcp_covered = sum(1 for risk_id, _ in OWASP_MCP_RISKS if risk_id in covered_risks)

    console.print("  ─────────────────────────────────────")
    console.print("  📊 [bold]Summary[/bold]")
    console.print(f"     OWASP MCP Coverage: [bold]{mcp_covered}/10[/bold] risks")
    console.print(
        f"     Controls: [green]{passed} passed[/green] · [red]{failed} failed[/red] · "
        f"[yellow]{not_tested} not tested[/yellow] · {total} total"
    )

    if failed == 0 and not_tested == 0:
        console.print("     ✅ [green bold]All controls passed[/green bold]")
    elif failed == 0:
        console.print(f"     🟡 [yellow]No failures, but {not_tested} controls need testing[/yellow]")
    else:
        console.print(f"     ❌ [red bold]{failed} control(s) failed — see details above[/red bold]")

    console.print()
