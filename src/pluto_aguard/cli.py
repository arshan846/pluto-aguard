"""CLI entry point for Pluto AgentGuard."""

import click
from rich.console import Console

from pluto_aguard import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="pluto-aguard")
def main() -> None:
    """🛡️ Pluto AgentGuard — AI Agent Security Scanner.

    Scan, monitor, and simulate security policies for AI agents.
    """


@main.command()
@click.argument("path", type=click.Path(exists=True), default=".")
@click.option("--format", "output_format", type=click.Choice(["text", "json", "html", "sarif"]), default="text")
@click.option("--output", "-o", type=click.Path(), help="Output file path for report")
@click.option("--max-risk", type=float, help="Exit with code 1 if risk score exceeds this threshold")
@click.option(
    "--fail-on",
    type=click.Choice(["critical", "high", "medium", "low"]),
    help="Exit with code 1 if findings at or above this severity exist",
)
def scan(
    path: str,
    output_format: str,
    output: str | None,
    max_risk: float | None,
    fail_on: str | None,
) -> None:
    """🔍 Scan agent project for security vulnerabilities.

    Analyzes MCP server configs, environment files, and agent definitions
    for security issues mapped to the OWASP MCP Top 10.
    """
    from pluto_aguard.scanners.runner import run_scan

    run_scan(
        path,
        output_format=output_format,
        output_path=output,
        max_risk=max_risk,
        fail_on=fail_on,
    )


@main.command()
@click.option("--trace-file", type=click.Path(exists=True), help="OpenTelemetry trace file (JSONL)")
@click.option("--policy", type=click.Path(exists=True), help="Agent policy file (YAML)")
@click.option("--live", is_flag=True, help="Monitor in real-time (stdin)")
def monitor(trace_file: str | None, policy: str | None, live: bool) -> None:
    """📡 Monitor agent behavior and detect policy violations.

    Ingests OpenTelemetry traces or live agent output and flags
    unauthorized tool calls, permission drift, and data access violations.
    """
    from pluto_aguard.monitor.runner import run_monitor

    run_monitor(trace_file=trace_file, policy_path=policy, live=live)


@main.command()
@click.option("--config", type=click.Path(exists=True), required=True, help="Agent config file (YAML)")
@click.option("--policy", type=click.Path(exists=True), help="Policy changes to simulate (YAML)")
@click.option("--interactive", "-i", is_flag=True, help="Interactive mode")
def whatif(config: str, policy: str | None, interactive: bool) -> None:
    """🔮 Simulate policy changes and see risk score impact.

    Model the effect of security policy changes before applying them.
    Shows risk score deltas and recommends optimal policy combinations.
    """
    from pluto_aguard.simulator.runner import run_whatif

    run_whatif(config_path=config, policy_path=policy, interactive=interactive)


@main.command()
@click.argument("path", type=click.Path(exists=True), default=".")
@click.option("--config", type=click.Path(exists=True), help="Agent config file (YAML)")
@click.option("--policy", type=click.Path(exists=True), help="Agent policy file (YAML)")
@click.option("--output", "-o", type=click.Path(), help="Output file path", default="launch-readiness.md")
def evidence(path: str, config: str | None, policy: str | None, output: str) -> None:
    """📋 Generate a launch readiness packet for agent review.

    Combines scan findings, policy analysis, and risk assessment into
    a single document for security review before shipping an agent.
    """
    from pluto_aguard.evidence.runner import run_evidence

    run_evidence(path, config_path=config, policy_path=policy, output_path=output)


@main.group()
def baseline() -> None:
    """📏 Manage security baselines for drift detection."""


@baseline.command("create")
@click.argument("path", type=click.Path(exists=True), default=".")
@click.option("--output", "-o", type=click.Path(), default=".aguard-baseline.json", help="Baseline output file")
def baseline_create(path: str, output: str) -> None:
    """Create a security baseline snapshot of the current state."""
    from pluto_aguard.baseline.runner import create_baseline

    create_baseline(path, output_path=output)


@baseline.command("compare")
@click.argument("path", type=click.Path(exists=True), default=".")
@click.option(
    "--baseline-file",
    "-b",
    type=click.Path(exists=True),
    default=".aguard-baseline.json",
    help="Baseline file to compare against",
)
@click.option("--fail-on-drift", is_flag=True, help="Exit with code 1 if drift detected")
def baseline_compare(path: str, baseline_file: str, fail_on_drift: bool) -> None:
    """Compare current state against a saved baseline to detect drift."""
    from pluto_aguard.baseline.runner import compare_baseline

    compare_baseline(path, baseline_path=baseline_file, fail_on_drift=fail_on_drift)


if __name__ == "__main__":
    main()
