"""MCP configuration scanner.

Scans MCP server configuration files for security vulnerabilities
including over-permissioned tools, hardcoded secrets, insecure transports,
and tool poisoning indicators.

Schema note: most checks here (transport, auth, env secrets, dangerous
packages, connection strings, context-safety heuristics) operate on fields
that a real MCP client config actually has -- command/args/env, or
url/headers for remote servers. `_check_server_permissions` and
`_check_tool_definitions`, however, look for `permissions`/`scope`/`tools`
(with a `description`) directly on a server entry -- fields that don't
exist in a bare claude_desktop_config.json/.mcp.json. Those two checks only
fire against configs that add this metadata themselves (e.g. an enterprise
MCP gateway, or AgentGuard's own example fixtures) and are legitimately
inert on a stock client config -- that's expected, not a gap. See
docs/config-schema.md for the full breakdown and
examples/claude_desktop_config.json for what a real config looks like.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

from pluto_aguard.models import Finding, Severity

# Patterns that indicate hardcoded secrets
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}", re.IGNORECASE)),
    (
        "AWS Secret Key",
        re.compile(
            r"(?:aws_secret_access_key|secret_key)\s*[=:]\s*['\"]?[A-Za-z0-9/+=]{40}",
            re.IGNORECASE,
        ),
    ),
    ("Generic API Key", re.compile(r"(?:api[_-]?key|apikey)\s*[=:]\s*['\"]?[A-Za-z0-9_\-]{20,}", re.IGNORECASE)),
    ("Bearer Token", re.compile(r"[Bb]earer\s+[A-Za-z0-9\-._~+/]+=*")),
    ("Private Key", re.compile(r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----")),
    ("GitHub Token", re.compile(r"gh[ps]_[A-Za-z0-9_]{20,}")),
    ("OpenAI Key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("Anthropic Key", re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}")),
    ("Hugging Face Token", re.compile(r"hf_[A-Za-z0-9]{20,}")),
    ("Google API Key", re.compile(r"AIza[A-Za-z0-9\-_]{35}")),
    (
        "Pinecone Key",
        re.compile(
            r"(?:pinecone[_-]?(?:api[_-]?)?key)\s*[=:]\s*['\"]?[A-Za-z0-9\-]{20,}",
            re.IGNORECASE,
        ),
    ),
    (
        "Cohere Key",
        re.compile(
            r"(?:cohere[_-]?(?:api[_-]?)?key)\s*[=:]\s*['\"]?[A-Za-z0-9]{20,}",
            re.IGNORECASE,
        ),
    ),
    ("Replicate Token", re.compile(r"r8_[A-Za-z0-9]{20,}")),
    (
        "Database Password",
        re.compile(
            r"(?:db[_-]?pass(?:word)?|database[_-]?password)\s*[=:]\s*['\"]?[^\s'\"]{8,}",
            re.IGNORECASE,
        ),
    ),
    (
        "Generic Secret",
        re.compile(
            r"(?<![A-Za-z])(?:secret|password|passwd|token)(?![A-Za-z])\s*[=:]\s*['\"]?[A-Za-z0-9/+=\-_]{16,}",
            re.IGNORECASE,
        ),
    ),
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


def _shannon_entropy(value: str) -> float:
    """Compute Shannon entropy of a string in bits per character."""
    if not value:
        return 0.0
    counts = Counter(value)
    length = len(value)
    return -sum((n / length) * math.log2(n / length) for n in counts.values())


def _validate_bearer_token(match: re.Match[str]) -> bool:
    """Reject 'Bearer <word>' matches that are prose, not a credential.

    The raw regex matches any word after "bearer" (e.g. "Bearer authentication
    is a common scheme"). Real bearer tokens are long, high-entropy opaque
    strings or JWTs, so require both a minimum length and entropy above what
    common English words exhibit.
    """
    parts = match.group().split(None, 1)
    token = parts[1].rstrip("=") if len(parts) > 1 else ""
    if len(token) < 16:
        return False
    return _shannon_entropy(token) >= 3.3


# Per-pattern extra validation to suppress false positives that the regex
# alone can't rule out (e.g. prose sentences matching a loose token pattern).
_EXTRA_VALIDATORS: dict[str, Callable[[re.Match[str]], bool]] = {
    "Bearer Token": _validate_bearer_token,
}


def scan_file_for_secrets(file_path: Path, content: str) -> list[Finding]:
    """Scan a single file for hardcoded secrets."""
    findings: list[Finding] = []

    for line_num, line in enumerate(content.splitlines(), start=1):
        for secret_name, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                match = pattern.search(line)
                matched_text = match.group() if match else ""

                validator = _EXTRA_VALIDATORS.get(secret_name)
                if validator and match and not validator(match):
                    continue

                # Skip if the matched secret itself looks like a placeholder
                if any(placeholder in matched_text.lower() for placeholder in [
                    "example", "placeholder", "your_", "xxx", "changeme", "todo",
                    "<your", "${", "{{", "%{",
                ]):
                    continue

                # Skip if the surrounding line contains template variable references
                if any(tmpl in line for tmpl in ["${", "{{", "%{", "process.env.", "os.environ"]):
                    continue

                # Skip non-secret token names (pagination, CSRF, continuation)
                if any(prefix in line.lower() for prefix in [
                    "continuationtoken", "nexttoken", "pagetoken", "csrftoken",
                    "refreshtoken", "synctoken", "cursortoken", "nextpagetoken",
                    "skiptoken",
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
                    owasp_id="MCP01:2025",
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
        findings.extend(_check_env_secrets(file_path, server_name, server_config))
        findings.extend(_check_dangerous_server_packages(file_path, server_name, server_config))
        findings.extend(_check_args_connection_strings(file_path, server_name, server_config))
        findings.extend(_check_context_safety(file_path, server_name, server_config))

    # Config-level checks (applied once per file, not per server)
    findings.extend(_check_missing_context_limits(file_path, config))

    return findings


def _check_server_permissions(
    file_path: Path, server_name: str, config: dict[str, Any]
) -> list[Finding]:
    """Check for over-permissioned server configurations.

    Extended-schema check: `permissions`/`scope`/`access`/`tools` are not
    fields a bare MCP client config has on a server entry. See the module
    docstring and docs/config-schema.md.
    """
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
            owasp_id="MCP02:2025",
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
            owasp_id="MCP02:2025",
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
                    owasp_id="MCP05:2025",
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
        # Determine if this is localhost (lower practical risk)
        is_localhost = any(
            host in url for host in ("://127.0.0.1", "://localhost", "://0.0.0.0", "://[::1]")
        )
        findings.append(Finding(
            id=f"TRANSPORT-HTTP-{server_name}",
            title=f"Insecure HTTP transport on MCP server '{server_name}'",
            description=(
                f"MCP server '{server_name}' uses unencrypted HTTP ({url}). "
                + ("Since this is a localhost connection, the practical risk is lower "
                   "but local processes could still intercept traffic."
                   if is_localhost else
                   "Agent communications may be intercepted or tampered with.")
            ),
            severity=Severity.MEDIUM if is_localhost else Severity.HIGH,
            category="transport",
            owasp_id="MCP07:2025",
            file_path=str(file_path),
            remediation=(
                "Use HTTPS with TLS 1.2+ for MCP server connections."
                + (" For localhost servers, consider using a Unix domain socket or "
                   "binding to a random port with a shared secret."
                   if is_localhost else "")
            ),
        ))

    return findings


def _check_server_auth(
    file_path: Path, server_name: str, config: dict[str, Any]
) -> list[Finding]:
    """Check for missing or weak authentication."""
    findings: list[Finding] = []

    auth = config.get("auth", config.get("authentication", config.get("credentials", None)))
    headers = config.get("headers", {})
    has_auth_header = isinstance(headers, dict) and any(
        k.lower() in ("authorization", "x-api-key", "api-key") for k in headers
    )

    # Remote servers without auth are a concern
    url = config.get("url", config.get("endpoint", ""))
    is_remote = isinstance(url, str) and url.startswith(("http://", "https://"))

    if is_remote and auth is None and not has_auth_header:
        findings.append(Finding(
            id=f"AUTH-MISSING-{server_name}",
            title=f"No authentication configured for remote MCP server '{server_name}'",
            description=(
                f"Remote MCP server '{server_name}' ({url}) has no authentication configured "
                "in the client config (no 'auth', 'credentials', or Authorization header). "
                "Note: some services may be intentionally public. If this endpoint performs "
                "actions or returns sensitive data, authentication should be configured."
            ),
            severity=Severity.HIGH,
            category="authentication",
            owasp_id="MCP07:2025",
            file_path=str(file_path),
            remediation=(
                "If this endpoint requires authentication, add an API key, OAuth token, "
                "or mTLS configuration. If the service is intentionally public and read-only, "
                "this finding may be informational."
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
                owasp_id="MCP01:2025",
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
    """Check tool definitions for poisoning indicators.

    Extended-schema check: a `tools` list with `description` fields on a
    server entry is not part of a bare MCP client config -- see the module
    docstring and docs/config-schema.md.
    """
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
                    owasp_id="MCP03:2025",
                    file_path=str(file_path),
                    evidence=description[:200],
                    remediation=(
                        "Review and sanitize all tool descriptions. Use a trusted tool registry "
                        "and verify tool integrity before integration."
                    ),
                ))
                break

    return findings


# Env var names that indicate secrets
_SECRET_ENV_NAMES = re.compile(
    r"(?i)(API[_-]?KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL|AUTH[_-]?KEY|ACCESS[_-]?KEY|PRIVATE[_-]?KEY)",
)

# Placeholder patterns — values that are clearly not real secrets
_PLACEHOLDER_VALUE = re.compile(
    r"(?i)(your[_-]|placeholder|example|changeme|xxx|todo|<your|"
    r"\$\{|^\{\{|^%[A-Z]|put.*here|pon.*aqui|ضع|replace[_-]|"
    r"TU[_-]|insert[_-]|CHANGE[_-]|FILL[_-]|ENTER[_-]|"
    r"\[.*\]$|^<|>$)",
)

# Known dangerous MCP server packages that grant filesystem/shell/db access
# Organized by risk tier: CRITICAL (shell/browser with auth), HIGH (write access),
# MEDIUM (read-only external content injection)
_DANGEROUS_SERVER_PACKAGES: dict[str, tuple[str, str, Severity]] = {
    # ── CRITICAL: Browser control with authenticated sessions ──
    "mcp-chrome-bridge": (
        "browser-control",
        "Uses YOUR live authenticated Chrome browser. Can inject JS in any tab, "
        "capture network traffic including auth tokens, read browser history and "
        "cookies. Prompt injection from any web page can exfiltrate credentials "
        "from banking, email, and corporate SSO tabs.",
        Severity.CRITICAL,
    ),
    "chrome-devtools-mcp": (
        "browser-control",
        "Full Chrome DevTools Protocol access. Can attach to existing Chrome "
        "sessions, capture complete network response bodies (credentials, PII), "
        "execute JavaScript in browser context, and take screenshots.",
        Severity.CRITICAL,
    ),
    # ── CRITICAL: Arbitrary code/shell execution ──
    "serena-agent": (
        "shell-execution",
        "Grants unrestricted shell command execution via execute_shell_command, "
        "full filesystem read/write, and semantic code editing. Equivalent to "
        "giving the LLM an SSH session.",
        Severity.CRITICAL,
    ),
    # ── HIGH: Browser automation (isolated but still dangerous) ──
    "@playwright/mcp": (
        "browser-automation",
        "Full browser automation — navigate to any URL, fill forms, download "
        "files, take screenshots. Can complete multi-step destructive actions "
        "(wire money, delete cloud resources) if given access to authenticated "
        "sessions.",
        Severity.HIGH,
    ),
    "@executeautomation/playwright-mcp-server": (
        "browser-automation",
        "Grants full browser automation capabilities. An agent can navigate "
        "to arbitrary URLs, fill forms, and exfiltrate page content.",
        Severity.HIGH,
    ),
    # ── HIGH: Source control write access ──
    "github-mcp-server": (
        "source-control",
        "GitHub write access — can create/merge PRs, push code, trigger CI/CD "
        "workflows, and access job logs that may leak secrets. A prompt injection "
        "can merge backdoor code or trigger pipelines that exfiltrate repo secrets.",
        Severity.HIGH,
    ),
    # ── HIGH: Workflow/automation engines (arbitrary code via workflows) ──
    "n8n-mcp": (
        "workflow-execution",
        "Creates and executes n8n workflows including Code nodes with arbitrary "
        "JS. Can read/write/delete ALL stored credentials (API keys, OAuth tokens, "
        "database passwords). Can create persistent backdoor automations that run "
        "after the conversation ends.",
        Severity.HIGH,
    ),
    # ── HIGH: Database access ──
    "@modelcontextprotocol/server-filesystem": (
        "filesystem",
        "Grants read/write access to the local filesystem. An agent can read, "
        "create, and modify any file within the allowed directories.",
        Severity.HIGH,
    ),
    "@modelcontextprotocol/server-postgres": (
        "database",
        "Grants direct SQL access to a PostgreSQL database. An agent can "
        "read, modify, or delete data without application-level access controls.",
        Severity.HIGH,
    ),
    "@modelcontextprotocol/server-sqlite": (
        "database",
        "Grants direct SQL access to a SQLite database.",
        Severity.HIGH,
    ),
    "@toolbox-sdk/server": (
        "database",
        "Google MCP Toolbox — supports 20+ databases (Postgres, BigQuery, MySQL, "
        "MongoDB, Redis, etc.). Prebuilt mode enables unrestricted SQL execution "
        "including DROP TABLE and DELETE. BigQuery mode can run queries costing "
        "thousands in compute.",
        Severity.HIGH,
    ),
    # ── MEDIUM: Social media write access ──
    "xpzouying/xiaohongshu-mcp": (
        "social-media",
        "Can publish posts, comments, and replies on Xiaohongshu at scale. "
        "Enables automated spam, disinformation, or social engineering campaigns. "
        "Accesses local filesystem for image/video uploads.",
        Severity.MEDIUM,
    ),
}

# Patterns to match popular servers by name/args when exact package isn't used
_POPULAR_SERVER_PATTERNS: list[tuple[re.Pattern[str], str, str, Severity]] = [
    # Browser control
    (re.compile(r"@playwright/mcp", re.IGNORECASE),
     "browser-automation", "Playwright MCP — full browser automation with URL navigation, "
     "form filling, and content exfiltration capabilities.", Severity.HIGH),
    (re.compile(r"chrome-devtools-mcp", re.IGNORECASE),
     "browser-control", "Chrome DevTools MCP — attaches to live Chrome sessions with full "
     "DevTools Protocol access including JS execution and network capture.", Severity.CRITICAL),
    (re.compile(r"mcp-chrome-bridge", re.IGNORECASE),
     "browser-control", "Chrome MCP Bridge — controls your authenticated Chrome browser "
     "with JS injection, cookie access, and network debugging.", Severity.CRITICAL),
    # GitHub
    (re.compile(r"github-mcp-server|ghcr\.io/github/github-mcp-server", re.IGNORECASE),
     "source-control", "GitHub MCP — can merge PRs, push code, trigger CI/CD, "
     "and access job logs that may leak secrets.", Severity.HIGH),
    # n8n workflow
    (re.compile(r"n8n-mcp", re.IGNORECASE),
     "workflow-execution", "n8n MCP — creates workflows with arbitrary code execution, "
     "manages all stored credentials, and can deploy persistent automations.", Severity.HIGH),
    # Google DB toolbox
    (re.compile(r"@toolbox-sdk/server", re.IGNORECASE),
     "database", "Google MCP Toolbox — unrestricted SQL against 20+ database types "
     "in prebuilt mode.", Severity.HIGH),
    # Serena coding agent
    (re.compile(r"serena-agent|serena", re.IGNORECASE),
     "shell-execution", "Serena — unrestricted shell execution and filesystem access.", Severity.CRITICAL),
    # Social media
    (re.compile(r"xiaohongshu-mcp|x-mcp.*xiaohongshu", re.IGNORECASE),
     "social-media", "Xiaohongshu MCP — can publish posts, comments, and replies "
     "on the platform at scale.", Severity.MEDIUM),
]

# Context injection servers — primarily inject external content into LLM context
_CONTEXT_INJECTION_PACKAGES: dict[str, str] = {
    "@upstash/context7-mcp": (
        "Context7 — fetches external documentation from community-contributed "
        "sources and injects it directly into LLM context. A compromised library "
        "entry could inject prompt injection payloads."
    ),
    "figma-developer-mcp": (
        "Figma MCP — fetches Figma file content (node names, descriptions, text "
        "layers) into LLM context. A malicious designer could embed prompt "
        "injection instructions in node names or descriptions."
    ),
}


def _check_env_secrets(
    file_path: Path, server_name: str, config: dict[str, Any]
) -> list[Finding]:
    """Check env vars for hardcoded secrets (not references or placeholders)."""
    findings: list[Finding] = []

    env = config.get("env", {})
    if not isinstance(env, dict):
        return findings

    for key, value in env.items():
        if not isinstance(value, str) or not value:
            continue
        if not _SECRET_ENV_NAMES.search(key):
            continue
        # Skip env-var references like ${ENV_VAR}, {{VAR}}, %VAR%
        if value.startswith(("${", "{{", "%")) or value == "":
            continue
        # Skip obvious placeholders
        if _PLACEHOLDER_VALUE.search(value):
            continue
        # Remaining values with secret-like keys are likely hardcoded
        if len(value) >= 8:
            findings.append(Finding(
                id=f"ENV-SECRET-{server_name}-{key}",
                title=f"Hardcoded secret in env var '{key}' on server '{server_name}'",
                description=(
                    f"MCP server '{server_name}' has env var '{key}' set to a literal value "
                    "instead of an environment variable reference. Hardcoded secrets in "
                    "config files can be extracted through prompt injection, log exposure, "
                    "or repository scraping."
                ),
                severity=Severity.HIGH,
                category="secrets",
                owasp_id="MCP01:2025",
                file_path=str(file_path),
                evidence=f"{key} = {value[:4]}****{value[-4:]}" if len(value) > 8 else f"{key} = ****",
                remediation=(
                    f"Use an environment variable reference for '{key}' instead of a literal "
                    "value. For example: \"${env:MY_SECRET}\" or load from a secrets manager."
                ),
            ))

    return findings


def _check_dangerous_server_packages(
    file_path: Path, server_name: str, config: dict[str, Any]
) -> list[Finding]:
    """Detect well-known dangerous MCP server packages without HITL gates."""
    findings: list[Finding] = []

    args = config.get("args", [])
    if not isinstance(args, list):
        args = []

    args_str = " ".join(str(a) for a in args)
    command = str(config.get("command", ""))
    url = str(config.get("url", ""))
    combined = f"{command} {args_str} {server_name} {url}"

    matched_packages: set[str] = set()

    # Check exact package matches in args
    for package, (category, risk_desc, severity) in _DANGEROUS_SERVER_PACKAGES.items():
        if package in args_str or package in url:
            matched_packages.add(category)
            findings.append(Finding(
                id=f"DANGEROUS-PKG-{server_name}-{category}",
                title=f"High-capability MCP server '{package}' on '{server_name}'",
                description=(
                    f"MCP server '{server_name}' uses '{package}' which grants {category} "
                    f"access. {risk_desc} Note: HITL enforcement is the MCP client's "
                    "responsibility. Ensure your client prompts for approval before "
                    "executing sensitive operations from this server."
                ),
                severity=Severity.INFO,
                category="awareness",
                owasp_id="MCP05:2025",
                file_path=str(file_path),
                evidence=f"Package: {package}",
                remediation=(
                    f"Verify that your MCP client enforces human-in-the-loop approval "
                    f"for '{server_name}' operations. Consider restricting capabilities "
                    "to the minimum required."
                ),
            ))

    # Check pattern matches for popular servers (only if not already caught)
    for pattern, category, risk_desc, severity in _POPULAR_SERVER_PATTERNS:
        if category in matched_packages:
            continue
        if pattern.search(combined):
            matched_packages.add(category)
            findings.append(Finding(
                id=f"DANGEROUS-POPULAR-{server_name}-{category}",
                title=f"High-capability MCP server detected: '{server_name}' ({category})",
                description=(
                    f"MCP server '{server_name}' matches a known high-capability server pattern. "
                    f"{risk_desc} Note: HITL enforcement is the MCP client's responsibility. "
                    "Ensure your client prompts for approval before executing sensitive operations."
                ),
                severity=Severity.INFO,
                category="awareness",
                owasp_id="MCP05:2025",
                file_path=str(file_path),
                remediation=(
                    f"Verify that your MCP client enforces human-in-the-loop approval "
                    f"for '{server_name}' and restrict to the minimum required capabilities."
                ),
            ))

    # Check context injection packages
    for package, risk_desc in _CONTEXT_INJECTION_PACKAGES.items():
        if package in args_str or package in url:
            findings.append(Finding(
                id=f"CONTEXT-INJECT-{server_name}",
                title=f"External content injection server '{package}' on '{server_name}'",
                description=(
                    f"MCP server '{server_name}' uses '{package}' which injects external "
                    f"content directly into the LLM context window. {risk_desc} "
                    "This is a vector for indirect prompt injection attacks."
                ),
                severity=Severity.MEDIUM,
                category="context_safety",
                owasp_id="MCP03:2025",
                file_path=str(file_path),
                evidence=f"Package: {package}",
                remediation=(
                    "Validate and sanitize external content before injection into LLM context. "
                    "Set response size limits to prevent context window stuffing. "
                    "Consider content filtering for prompt injection patterns."
                ),
            ))

    # Also detect custom servers with dangerous names
    dangerous_name_patterns = [
        (r"powershell[_-]commander", "shell", "Grants PowerShell command execution"),
        (r"file[_-]commander", "filesystem", "Grants file management capabilities"),
        (r"shell[_-](?:server|mcp)", "shell", "Grants shell command execution"),
    ]
    for pattern, cat, desc in dangerous_name_patterns:
        if cat in matched_packages:
            continue
        if re.search(pattern, combined, re.IGNORECASE):
            findings.append(Finding(
                id=f"DANGEROUS-CUSTOM-{server_name}-{cat}",
                title=f"Dangerous custom MCP server '{server_name}' ({cat} access) without HITL",
                description=(
                    f"MCP server '{server_name}' appears to grant {cat} access. "
                    f"{desc}. Without human-in-the-loop approval, this is exploitable "
                    "through prompt injection."
                ),
                severity=Severity.HIGH,
                category="permissions",
                owasp_id="MCP05:2025",
                file_path=str(file_path),
                remediation=(
                    f"Add human-in-the-loop approval for '{server_name}' and "
                    "restrict to the minimum required capabilities."
                ),
            ))

    return findings


def _check_args_connection_strings(
    file_path: Path, server_name: str, config: dict[str, Any]
) -> list[Finding]:
    """Detect connection strings with embedded credentials in server args."""
    findings: list[Finding] = []

    args = config.get("args", [])
    if not isinstance(args, list):
        return findings

    conn_pattern = re.compile(
        r"(postgresql?|mysql|mongodb|redis)://[^:]+:[^@]+@"
    )

    for arg in args:
        if not isinstance(arg, str):
            continue
        match = conn_pattern.search(arg)
        if match:
            findings.append(Finding(
                id=f"CONN-STRING-ARGS-{server_name}",
                title=f"Connection string with credentials in args for '{server_name}'",
                description=(
                    f"MCP server '{server_name}' has a connection string with embedded "
                    "credentials passed as a command-line argument. These credentials are "
                    "visible in process listings and shell history."
                ),
                severity=Severity.HIGH,
                category="secrets",
                owasp_id="MCP01:2025",
                file_path=str(file_path),
                evidence=f"{arg[:20]}****" if len(arg) > 20 else "****",
                remediation=(
                    "Use environment variables for database credentials instead of "
                    "embedding them in connection strings. Example: "
                    "postgresql://${DB_USER}:${DB_PASS}@host/db"
                ),
            ))

    # Also check env vars for connection strings with credentials
    env = config.get("env", {})
    if isinstance(env, dict):
        for key, value in env.items():
            if not isinstance(value, str):
                continue
            match = conn_pattern.search(value)
            if match and not value.startswith(("${", "{{")):
                findings.append(Finding(
                    id=f"CONN-STRING-ENV-{server_name}-{key}",
                    title=f"Connection string with credentials in env '{key}' for '{server_name}'",
                    description=(
                        f"Env var '{key}' on MCP server '{server_name}' contains a connection "
                        "string with embedded credentials."
                    ),
                    severity=Severity.HIGH,
                    category="secrets",
                    owasp_id="MCP01:2025",
                    file_path=str(file_path),
                    evidence=f"{key} = {value[:20]}****" if len(value) > 20 else f"{key} = ****",
                    remediation=(
                        "Use environment variable references for the database password. "
                        "Do not embed credentials in connection strings."
                    ),
                ))

    return findings


# ─── Runtime Bridge Heuristics ───
# These static checks flag configurations that are vulnerable to runtime
# attacks (context stuffing, multi-turn confusion, indirect injection)
# until the runtime proxy (v1.0) provides proper detection.

# MCP server packages/patterns known to fetch external content
_EXTERNAL_FETCH_PATTERNS = [
    (re.compile(r"server-fetch|web-fetch|url-fetch", re.IGNORECASE), "web fetching"),
    (re.compile(r"server-puppeteer|puppeteer-mcp", re.IGNORECASE), "web scraping"),
    (re.compile(r"playwright-mcp|playwright-server", re.IGNORECASE), "browser automation"),
    (re.compile(r"server-brave-search|tavily|serp", re.IGNORECASE), "web search"),
    (re.compile(r"rag|retrieval|knowledge[_-]base|vector", re.IGNORECASE), "RAG/retrieval"),
    (re.compile(r"crawl|scrape|spider", re.IGNORECASE), "web crawling"),
]


def _check_context_safety(
    file_path: Path, server_name: str, config: dict[str, Any]
) -> list[Finding]:
    """Flag servers that fetch external content without context safety controls.

    External content is the primary vector for indirect prompt injection,
    context window stuffing, and retrieval-augmented injection attacks.
    """
    findings: list[Finding] = []

    args = config.get("args", [])
    args_str = " ".join(str(a) for a in args) if isinstance(args, list) else ""
    command = str(config.get("command", ""))
    combined = f"{command} {args_str} {server_name}"

    for pattern, capability in _EXTERNAL_FETCH_PATTERNS:
        if pattern.search(combined):
            findings.append(Finding(
                id=f"CONTEXT-EXT-FETCH-{server_name}",
                title=f"MCP server '{server_name}' fetches external content ({capability}) — indirect injection risk",
                description=(
                    f"MCP server '{server_name}' has {capability} capabilities, meaning it "
                    "retrieves content from external sources and passes it into the agent's "
                    "context. This is the primary vector for indirect prompt injection: "
                    "an attacker can embed adversarial instructions in web pages, documents, "
                    "or search results that the agent will treat as trusted input. "
                    "Context window stuffing attacks can also push safety constraints out "
                    "of the agent's context window via oversized responses."
                ),
                severity=Severity.MEDIUM,
                category="context_safety",
                owasp_id="MCP06:2025",
                file_path=str(file_path),
                evidence=f"Detected: {capability} in '{server_name}'",
                remediation=(
                    "1. Sanitize external content before injecting into agent context. "
                    "2. Truncate tool responses to a max token budget to prevent context stuffing. "
                    "3. Use a content safety filter on retrieved content. "
                    "4. Consider adding human-in-the-loop for actions triggered after external fetches. "
                    "5. When available, use the runtime proxy (aguard proxy) for live detection."
                ),
            ))
            break  # One finding per server is enough

    return findings


def _check_missing_context_limits(
    file_path: Path, config: dict[str, Any]
) -> list[Finding]:
    """Check MCP config for missing context window and session controls.

    These controls mitigate context stuffing and multi-turn state confusion.
    Applied at the config level (not per-server).
    """
    findings: list[Finding] = []

    servers = config.get("mcpServers", config.get("mcp_servers", config.get("servers", {})))
    if not isinstance(servers, dict) or not servers:
        return findings

    # Check for global or per-server max_tokens / max_response_length
    has_response_limits = False
    has_session_limits = False

    # Check global config level
    if config.get("max_tokens") or config.get("max_response_length") or config.get("context_limit"):
        has_response_limits = True
    if config.get("max_turns") or config.get("session_timeout") or config.get("max_conversation_turns"):
        has_session_limits = True

    # Check per-server level
    for _name, srv in servers.items():
        if not isinstance(srv, dict):
            continue
        if srv.get("max_tokens") or srv.get("max_response_length") or srv.get("maxResponseSize"):
            has_response_limits = True
        if srv.get("max_turns") or srv.get("session_timeout") or srv.get("timeout"):
            has_session_limits = True

    if not has_response_limits:
        findings.append(Finding(
            id="CONTEXT-NO-RESPONSE-LIMIT",
            title="No response size limits declared in config (informational)",
            description=(
                "None of the configured MCP servers declare a response size limit "
                "(max_tokens, max_response_length). Note: the MCP specification does not "
                "currently define a standard field for response limits. This is an "
                "awareness item — consider whether your client or application layer "
                "enforces response size constraints."
            ),
            severity=Severity.INFO,
            category="context_safety",
            owasp_id="MCP10:2025",
            file_path=str(file_path),
            remediation=(
                "If your MCP client or application layer does not enforce response size "
                "limits, consider implementing truncation at the application level. "
                "A typical safe limit is 4000-8000 tokens per tool response."
            ),
        ))

    if not has_session_limits:
        findings.append(Finding(
            id="CONTEXT-NO-SESSION-LIMIT",
            title="No session/turn limits declared in config (informational)",
            description=(
                "No maximum turn count or session timeout is configured. Note: the MCP "
                "specification does not currently define standard fields for session limits. "
                "This is an awareness item — consider whether your client or application "
                "layer enforces session boundaries."
            ),
            severity=Severity.INFO,
            category="context_safety",
            owasp_id="MCP06:2025",
            file_path=str(file_path),
            remediation=(
                "If your client does not enforce session limits, consider implementing "
                "max_turns (e.g., 20) and session_timeout (e.g., 3600 seconds) at the "
                "application layer."
            ),
        ))

    return findings


def _is_mcp_config(config: dict[str, Any]) -> bool:
    """Check if a parsed JSON/YAML dict looks like an MCP configuration."""
    return any(
        key in config
        for key in ("mcpServers", "mcp_servers", "servers")
    )


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

    scanned_configs: set[Path] = set()

    # Scan known MCP config file patterns
    for pattern in config_patterns:
        for config_file in directory.rglob(pattern):
            if _should_skip(config_file):
                continue
            scanned_configs.add(config_file.resolve())
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

    # Scan other files for secrets AND detect MCP configs by content
    for pattern in secret_scan_patterns:
        for file_path in directory.rglob(pattern):
            if _should_skip(file_path):
                continue
            if file_path.resolve() in scanned_configs:
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if len(content) > 500_000:  # Skip very large files
                    continue

                # Try to detect MCP configs by content (catches renamed/prefixed files)
                if file_path.suffix in (".json", ".yaml", ".yml"):
                    try:
                        if file_path.suffix == ".json":
                            parsed = json.loads(content)
                        else:
                            parsed = yaml.safe_load(content)
                        if isinstance(parsed, dict) and _is_mcp_config(parsed):
                            findings.extend(scan_mcp_config(file_path, parsed))
                            scanned_configs.add(file_path.resolve())
                    except (json.JSONDecodeError, yaml.YAMLError):
                        pass

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
