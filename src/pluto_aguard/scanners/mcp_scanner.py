"""MCP configuration scanner.

Scans MCP server configuration files for security vulnerabilities
including over-permissioned tools, hardcoded secrets, insecure transports,
and tool poisoning indicators.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from pluto_aguard.models import Finding, Severity


# Patterns that indicate hardcoded secrets
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}", re.IGNORECASE)),
    ("AWS Secret Key", re.compile(r"(?:aws_secret_access_key|secret_key)\s*[=:]\s*['\"]?[A-Za-z0-9/+=]{40}", re.IGNORECASE)),
    ("Generic API Key", re.compile(r"(?:api[_-]?key|apikey)\s*[=:]\s*['\"]?[A-Za-z0-9_\-]{20,}", re.IGNORECASE)),
    ("Bearer Token", re.compile(r"[Bb]earer\s+[A-Za-z0-9\-._~+/]+=*")),
    ("Private Key", re.compile(r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----")),
    ("GitHub Token", re.compile(r"gh[ps]_[A-Za-z0-9_]{20,}")),
    ("OpenAI Key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("Azure Key", re.compile(r"(?:AccountKey|SharedAccessKey)\s*=\s*[A-Za-z0-9+/=]{40,}")),
    ("Connection String", re.compile(r"(?:mongodb|postgres|postgresql|mysql|redis)://[^\s\"']*:[^\s\"']*@")),
    ("Slack Token", re.compile(r"xox[bpors]-[A-Za-z0-9\-]+")),
]

# Dangerous permission patterns in MCP configs
WILDCARD_PERMISSION_PATTERNS = [
    re.compile(r'"permissions"\s*:\s*\[\s*"\*"\s*\]'),
    re.compile(r"permissions:\s*\n\s*-\s*['\"]?\*['\"]?"),
    re.compile(r'"scope"\s*:\s*"all"'),
    re.compile(r'"access"\s*:\s*"full"'),
    re.compile(r'"readWrite"\s*:\s*true'),
]


def scan_file_for_secrets(file_path: Path, content: str) -> list[Finding]:
    """Scan a single file for hardcoded secrets."""
    findings: list[Finding] = []

    for line_num, line in enumerate(content.splitlines(), start=1):
        for secret_name, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                match = pattern.search(line)
                matched_text = match.group() if match else ""

                # Skip if the matched secret itself looks like a placeholder
                if any(placeholder in matched_text.lower() for placeholder in [
                    "example", "placeholder", "your_", "xxx", "changeme", "todo",
                    "<your", "${", "{{",
                ]):
                    continue

                findings.append(Finding(
                    id=f"SECRET-{secret_name.upper().replace(' ', '-')}-{file_path.name}-L{line_num}",
                    title=f"Hardcoded {secret_name} detected",
                    description=(
                        f"A {secret_name} pattern was found in {file_path.name} at line {line_num}. "
                        "Hardcoded secrets in agent configurations can be extracted through "
                        "prompt injection or log exposure."
                    ),
                    severity=Severity.HIGH,
                    category="secrets",
                    owasp_id="OWASP-MCP-07",
                    file_path=str(file_path),
                    line_number=line_num,
                    evidence=_redact_secret(line.strip()),
                    remediation=(
                        "Use environment variables or a secrets manager (e.g., Azure Key Vault, "
                        "AWS Secrets Manager) instead of hardcoding credentials. "
                        "Rotate this credential immediately."
                    ),
                ))

    return findings


def scan_mcp_config(file_path: Path, config: dict[str, Any]) -> list[Finding]:
    """Scan a parsed MCP configuration for security issues."""
    findings: list[Finding] = []

    # Check for MCP servers section
    servers = config.get("mcpServers", config.get("mcp_servers", config.get("servers", {})))
    if not isinstance(servers, dict):
        return findings

    for server_name, server_config in servers.items():
        if not isinstance(server_config, dict):
            continue

        findings.extend(_check_server_permissions(file_path, server_name, server_config))
        findings.extend(_check_server_transport(file_path, server_name, server_config))
        findings.extend(_check_server_auth(file_path, server_name, server_config))
        findings.extend(_check_tool_definitions(file_path, server_name, server_config))

    return findings


def _check_server_permissions(
    file_path: Path, server_name: str, config: dict[str, Any]
) -> list[Finding]:
    """Check for over-permissioned server configurations."""
    findings: list[Finding] = []

    # Check for wildcard or overly broad permissions
    permissions = config.get("permissions", config.get("scope", config.get("access", [])))

    if isinstance(permissions, list) and "*" in permissions:
        findings.append(Finding(
            id=f"PERM-WILDCARD-{server_name}",
            title=f"Wildcard permissions on MCP server '{server_name}'",
            description=(
                f"MCP server '{server_name}' has wildcard (*) permissions, granting unrestricted "
                "access to all tools and resources. This violates the principle of least privilege "
                "and increases blast radius if the server is compromised."
            ),
            severity=Severity.CRITICAL,
            category="permissions",
            owasp_id="OWASP-MCP-03",
            file_path=str(file_path),
            remediation=(
                f"Restrict permissions for '{server_name}' to only the specific tools and "
                "resources required. Use an explicit allowlist instead of wildcards."
            ),
        ))

    if isinstance(permissions, str) and permissions.lower() in ("all", "full", "*"):
        findings.append(Finding(
            id=f"PERM-BROAD-{server_name}",
            title=f"Overly broad permissions on MCP server '{server_name}'",
            description=(
                f"MCP server '{server_name}' has '{permissions}' access level. "
                "Broad access increases the attack surface for privilege escalation."
            ),
            severity=Severity.HIGH,
            category="permissions",
            owasp_id="OWASP-MCP-03",
            file_path=str(file_path),
            remediation="Scope permissions to the minimum required access level.",
        ))

    # Check for dangerous tool permissions
    tools = config.get("tools", [])
    if isinstance(tools, list):
        dangerous_tools = {"execute", "shell", "eval", "exec", "run_command", "file_write", "sudo"}
        for tool in tools:
            tool_name = tool if isinstance(tool, str) else tool.get("name", "")
            if tool_name.lower() in dangerous_tools:
                findings.append(Finding(
                    id=f"PERM-DANGEROUS-TOOL-{server_name}-{tool_name}",
                    title=f"Dangerous tool '{tool_name}' enabled on '{server_name}'",
                    description=(
                        f"MCP server '{server_name}' has the '{tool_name}' tool enabled. "
                        "This tool can execute arbitrary commands and should require "
                        "human-in-the-loop approval."
                    ),
                    severity=Severity.HIGH,
                    category="permissions",
                    owasp_id="OWASP-MCP-04",
                    file_path=str(file_path),
                    remediation=(
                        f"Add human-in-the-loop approval for the '{tool_name}' tool, "
                        "or remove it if not strictly required."
                    ),
                ))

    return findings


def _check_server_transport(
    file_path: Path, server_name: str, config: dict[str, Any]
) -> list[Finding]:
    """Check for insecure transport configurations."""
    findings: list[Finding] = []

    url = config.get("url", config.get("endpoint", config.get("uri", "")))
    if isinstance(url, str) and url.startswith("http://"):
        findings.append(Finding(
            id=f"TRANSPORT-HTTP-{server_name}",
            title=f"Insecure HTTP transport on MCP server '{server_name}'",
            description=(
                f"MCP server '{server_name}' uses unencrypted HTTP ({url}). "
                "Agent communications may be intercepted or tampered with."
            ),
            severity=Severity.HIGH,
            category="transport",
            owasp_id="OWASP-MCP-06",
            file_path=str(file_path),
            remediation="Use HTTPS with TLS 1.2+ for all MCP server connections.",
        ))

    return findings


def _check_server_auth(
    file_path: Path, server_name: str, config: dict[str, Any]
) -> list[Finding]:
    """Check for missing or weak authentication."""
    findings: list[Finding] = []

    auth = config.get("auth", config.get("authentication", config.get("credentials", None)))
    transport = config.get("transport", config.get("type", ""))

    # Remote servers without auth are a problem
    url = config.get("url", config.get("endpoint", ""))
    is_remote = isinstance(url, str) and url.startswith(("http://", "https://"))

    if is_remote and auth is None:
        findings.append(Finding(
            id=f"AUTH-MISSING-{server_name}",
            title=f"No authentication on remote MCP server '{server_name}'",
            description=(
                f"Remote MCP server '{server_name}' ({url}) has no authentication configured. "
                "Unauthenticated MCP servers can be exploited by any network-adjacent attacker."
            ),
            severity=Severity.CRITICAL,
            category="authentication",
            owasp_id="OWASP-MCP-01",
            file_path=str(file_path),
            remediation=(
                "Add authentication (API key, OAuth, mTLS) to the MCP server. "
                "Use short-lived, scoped credentials."
            ),
        ))

    # Check for long-lived tokens
    if isinstance(auth, dict):
        token = auth.get("token", auth.get("api_key", ""))
        if isinstance(token, str) and len(token) > 20 and not token.startswith(("${", "{{")):
            findings.append(Finding(
                id=f"AUTH-STATIC-TOKEN-{server_name}",
                title=f"Static long-lived token on MCP server '{server_name}'",
                description=(
                    f"MCP server '{server_name}' uses a static, long-lived authentication token. "
                    "Long-lived tokens increase risk if leaked through logs or prompt injection."
                ),
                severity=Severity.MEDIUM,
                category="authentication",
                owasp_id="OWASP-MCP-05",
                file_path=str(file_path),
                remediation=(
                    "Use ephemeral, short-lived tokens with automatic rotation. "
                    "Consider OAuth 2.0 client credentials flow or managed identity."
                ),
            ))

    return findings


def _check_tool_definitions(
    file_path: Path, server_name: str, config: dict[str, Any]
) -> list[Finding]:
    """Check tool definitions for poisoning indicators."""
    findings: list[Finding] = []

    tools = config.get("tools", [])
    if not isinstance(tools, list):
        return findings

    for tool in tools:
        if not isinstance(tool, dict):
            continue

        tool_name = tool.get("name", "unknown")
        description = tool.get("description", "")

        # Check for suspicious instructions in tool descriptions (tool poisoning)
        poisoning_indicators = [
            "ignore previous",
            "disregard",
            "override",
            "system prompt",
            "you are now",
            "forget your instructions",
            "act as",
            "pretend to be",
        ]
        desc_lower = description.lower()
        for indicator in poisoning_indicators:
            if indicator in desc_lower:
                findings.append(Finding(
                    id=f"POISON-TOOL-DESC-{server_name}-{tool_name}",
                    title=f"Possible tool poisoning in '{tool_name}' on '{server_name}'",
                    description=(
                        f"Tool '{tool_name}' description contains suspicious text "
                        f"('{indicator}') that may indicate tool poisoning — a technique "
                        "where malicious instructions are embedded in tool metadata to "
                        "manipulate agent behavior."
                    ),
                    severity=Severity.CRITICAL,
                    category="tool_poisoning",
                    owasp_id="OWASP-MCP-02",
                    file_path=str(file_path),
                    evidence=description[:200],
                    remediation=(
                        "Review and sanitize all tool descriptions. Use a trusted tool registry "
                        "and verify tool integrity before integration."
                    ),
                ))
                break

    return findings


def scan_directory(directory: Path) -> list[Finding]:
    """Scan a directory for MCP configurations and secrets."""
    findings: list[Finding] = []

    # File patterns to scan
    config_patterns = [
        "mcp.json", "mcp.yaml", "mcp.yml",
        ".mcp.json", ".mcp.yaml",
        "mcp-config.json", "mcp-config.yaml",
        "claude_desktop_config.json",
        "agent-config.yaml", "agent-config.yml",
        "agent.yaml", "agent.yml",
    ]
    secret_scan_patterns = [
        "*.env", "*.json", "*.yaml", "*.yml", "*.toml",
        "*.py", "*.js", "*.ts",
    ]

    # Scan MCP config files
    for pattern in config_patterns:
        for config_file in directory.rglob(pattern):
            if _should_skip(config_file):
                continue
            try:
                content = config_file.read_text(encoding="utf-8")
                if config_file.suffix == ".json":
                    config = json.loads(content)
                else:
                    config = yaml.safe_load(content)

                if isinstance(config, dict):
                    findings.extend(scan_mcp_config(config_file, config))
                findings.extend(scan_file_for_secrets(config_file, content))
            except (json.JSONDecodeError, yaml.YAMLError, OSError):
                continue

    # Scan other files for secrets
    for pattern in secret_scan_patterns:
        for file_path in directory.rglob(pattern):
            if _should_skip(file_path):
                continue
            # Skip already-scanned config files
            if file_path.name in config_patterns:
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if len(content) > 500_000:  # Skip very large files
                    continue
                findings.extend(scan_file_for_secrets(file_path, content))
            except OSError:
                continue

    return findings


def _should_skip(path: Path) -> bool:
    """Check if a path should be skipped during scanning."""
    skip_dirs = {
        ".git", "node_modules", "__pycache__", ".venv", "venv",
        ".tox", ".mypy_cache", ".pytest_cache", "dist", "build",
        ".eggs", "*.egg-info",
    }
    return any(part in skip_dirs for part in path.parts)


def _redact_secret(line: str) -> str:
    """Redact most of a secret value, showing only first/last 4 chars."""
    # Simple redaction — show structure but hide the value
    for name, pattern in SECRET_PATTERNS:
        match = pattern.search(line)
        if match:
            secret = match.group()
            if len(secret) > 8:
                redacted = secret[:4] + "****" + secret[-4:]
                return line.replace(secret, redacted)
    return line[:80] + "..." if len(line) > 80 else line
