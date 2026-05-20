"""OWASP-aligned control registry.

Maps every AgentGuard check to OWASP MCP Top 10 and LLM Top 10 controls.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ControlDefinition:
    """Definition of a security control aligned to OWASP."""

    id: str
    owasp_refs: list[str]
    title: str
    description: str
    command: str  # which aguard command implements this
    category: str  # finding category to match
    finding_id_prefix: str = ""  # optional: match only findings with this ID prefix
    severity: str = "high"


CONTROLS: list[ControlDefinition] = [
    ControlDefinition(
        id="AGC-MCP01-001",
        owasp_refs=["MCP01:2025", "LLM02:2025"],
        title="No hardcoded secrets in agent configurations",
        description="Detect API keys, tokens, passwords, and connection strings in config and source files.",
        command="scan",
        category="secrets",
        severity="high",
    ),
    ControlDefinition(
        id="AGC-MCP01-002",
        owasp_refs=["MCP01:2025"],
        title="No static long-lived tokens on MCP servers",
        description="Detect static authentication tokens that should be replaced with ephemeral credentials.",
        command="scan",
        category="authentication",
        severity="medium",
    ),
    ControlDefinition(
        id="AGC-MCP01-003",
        owasp_refs=["MCP01:2025"],
        title="No secrets in Dockerfile ENV directives",
        description="Detect secrets set via ENV in Dockerfiles, which are baked into image layers.",
        command="scan",
        category="ai_config",
        finding_id_prefix="AI-DOCKER-SECRET",
        severity="high",
    ),
    ControlDefinition(
        id="AGC-MCP01-004",
        owasp_refs=["MCP01:2025"],
        title=".env files excluded from version control",
        description="Verify .env files are listed in .gitignore to prevent secret commits.",
        command="scan",
        category="ai_config",
        finding_id_prefix="AI-ENV-NOT-GITIGNORED",
        severity="high",
    ),
    ControlDefinition(
        id="AGC-MCP02-001",
        owasp_refs=["MCP02:2025", "LLM06:2025"],
        title="No wildcard permissions on MCP servers",
        description="Detect MCP servers with wildcard (*) or overly broad permission grants.",
        command="scan",
        category="permissions",
        severity="critical",
    ),
    ControlDefinition(
        id="AGC-MCP02-002",
        owasp_refs=["MCP02:2025", "LLM06:2025"],
        title="Agent permissions explicitly declared",
        description="Verify agents have explicit permission declarations rather than implicit full access.",
        command="scan",
        category="permissions",
        severity="high",
    ),
    ControlDefinition(
        id="AGC-MCP02-003",
        owasp_refs=["MCP02:2025"],
        title="No permission drift from baseline",
        description="Compare current security posture against saved baseline to detect scope creep.",
        command="baseline",
        category="permissions",
        severity="high",
    ),
    ControlDefinition(
        id="AGC-MCP03-001",
        owasp_refs=["MCP03:2025"],
        title="No suspicious instructions in tool descriptions",
        description="Scan tool metadata for injection patterns (ignore previous, override, act as, etc.).",
        command="scan",
        category="tool_poisoning",
        severity="critical",
    ),
    ControlDefinition(
        id="AGC-MCP03-002",
        owasp_refs=["MCP03:2025"],
        title="Tool poisoning attack pack passes",
        description="Adversarial test: simulate tool poisoning attacks and verify policy blocks them.",
        command="test",
        category="tool_poisoning",
        severity="critical",
    ),
    ControlDefinition(
        id="AGC-MCP04-001",
        owasp_refs=["MCP04:2025", "LLM03:2025"],
        title="AI dependencies have pinned versions",
        description="Verify AI/ML packages (openai, langchain, etc.) have pinned versions in requirements.",
        command="scan",
        category="ai_config",
        finding_id_prefix="AI-UNPINNED-DEPS",
        severity="medium",
    ),
    ControlDefinition(
        id="AGC-MCP05-001",
        owasp_refs=["MCP05:2025", "LLM06:2025"],
        title="Dangerous tools require human approval",
        description="Verify execute, shell, file_write, etc. have human-in-the-loop gates.",
        command="scan",
        category="permissions",
        severity="high",
    ),
    ControlDefinition(
        id="AGC-MCP05-002",
        owasp_refs=["MCP05:2025", "LLM05:2025"],
        title="No eval/exec on LLM output",
        description="Detect code that executes LLM-generated output via eval(), exec(), subprocess, or os.system().",
        command="scan",
        category="ai_config",
        finding_id_prefix="AI-UNSAFE-EXEC",
        severity="critical",
    ),
    ControlDefinition(
        id="AGC-MCP05-003",
        owasp_refs=["MCP05:2025"],
        title="Command injection attack pack passes",
        description="Adversarial test: simulate command injection attempts and verify policy blocks them.",
        command="test",
        category="permission_escalation",
        severity="critical",
    ),
    ControlDefinition(
        id="AGC-MCP06-001",
        owasp_refs=["MCP06:2025", "LLM01:2025"],
        title="Prompt injection attack pack passes",
        description="Adversarial test: simulate prompt injection attacks and verify policy blocks them.",
        command="test",
        category="prompt_injection",
        severity="critical",
    ),
    ControlDefinition(
        id="AGC-MCP07-001",
        owasp_refs=["MCP07:2025"],
        title="Remote MCP servers have authentication",
        description="Verify all remote MCP servers have authentication configured.",
        command="scan",
        category="authentication",
        severity="critical",
    ),
    ControlDefinition(
        id="AGC-MCP07-002",
        owasp_refs=["MCP07:2025"],
        title="MCP servers use encrypted transport (HTTPS)",
        description="Verify MCP servers use HTTPS, not HTTP.",
        command="scan",
        category="transport",
        severity="high",
    ),
    ControlDefinition(
        id="AGC-MCP08-001",
        owasp_refs=["MCP08:2025"],
        title="Behavioral monitoring configured",
        description="Verify agent has behavioral monitoring with policy-based drift detection.",
        command="monitor",
        category="audit",
        severity="medium",
    ),
    ControlDefinition(
        id="AGC-MCP08-002",
        owasp_refs=["MCP08:2025"],
        title="Launch evidence packet generated",
        description="Verify a launch readiness packet has been generated with approval checklist.",
        command="evidence",
        category="audit",
        severity="medium",
    ),
    ControlDefinition(
        id="AGC-MCP10-001",
        owasp_refs=["MCP10:2025", "LLM02:2025"],
        title="No sensitive information in system prompts",
        description="Detect credentials, internal URLs, or database references in system prompts.",
        command="scan",
        category="ai_config",
        finding_id_prefix="AI-SYSTEMPROMPT-LEAK",
        severity="high",
    ),
    ControlDefinition(
        id="AGC-LLM10-001",
        owasp_refs=["LLM10:2025"],
        title="Agent has rate limits and timeouts",
        description="Verify agents have configured timeout and rate limit constraints.",
        command="scan",
        category="permissions",
        severity="medium",
    ),
]


def get_controls_by_owasp(owasp_id: str) -> list[ControlDefinition]:
    """Get all controls that map to a specific OWASP risk."""
    return [control for control in CONTROLS if owasp_id in control.owasp_refs]


def get_controls_by_command(command: str) -> list[ControlDefinition]:
    """Get all controls implemented by a specific command."""
    return [control for control in CONTROLS if control.command == command]
