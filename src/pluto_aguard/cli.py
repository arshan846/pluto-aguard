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
@click.option("--format", "output_format", type=click.Choice(["text", "json", "html"]), default="text")
@click.option("--output", "-o", type=click.Path(), help="Output file path for report")
@click.option("--rules", type=click.Path(exists=True), help="Custom rules file (YAML)")
def scan(path: str, output_format: str, output: str | None, rules: str | None) -> None:
    """🔍 Scan agent project for security vulnerabilities.

    Analyzes MCP server configs, environment files, and agent definitions
    for security issues mapped to the OWASP MCP Top 10.
    """
    from pluto_aguard.scanners.runner import run_scan

    run_scan(path, output_format=output_format, output_path=output, rules_path=rules)


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


if __name__ == "__main__":
    main()
