"""AI framework configuration scanner.

Scans for security issues in AI/ML project configurations that are
common across LangChain, CrewAI, AutoGen, OpenAI SDK, and other frameworks.
"""

from __future__ import annotations

import re
from pathlib import Path

from pluto_aguard.models import Finding, Severity


def scan_ai_configs(directory: Path) -> list[Finding]:
    """Scan for AI-specific security issues beyond MCP configs."""
    findings: list[Finding] = []

    findings.extend(_scan_openai_configs(directory))
    findings.extend(_scan_langchain_configs(directory))
    findings.extend(_scan_docker_configs(directory))
    findings.extend(_scan_env_files(directory))
    findings.extend(_scan_requirements_for_pinned_versions(directory))

    return findings


def _scan_openai_configs(directory: Path) -> list[Finding]:
    """Detect insecure OpenAI/LLM API usage patterns."""
    findings: list[Finding] = []
    insecure_api_base_pattern = re.compile(r"(?:api_base|base_url)\s*[=:]\s*['\"]http://", re.IGNORECASE)
    browser_pattern = re.compile(r"dangerouslyAllowBrowser\s*[:=]\s*true", re.IGNORECASE)
    insecure_tls_pattern = re.compile(
        r"(?:verify|ssl_verify|rejectUnauthorized)\s*[:=]\s*(?:False|false)",
        re.IGNORECASE,
    )

    for ext in ["*.py", "*.js", "*.ts"]:
        for file_path in directory.rglob(ext):
            if _should_skip(file_path):
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if len(content) > 500_000:
                    continue

                for line_num, line in enumerate(content.splitlines(), start=1):
                    if insecure_api_base_pattern.search(line):
                        findings.append(
                            Finding(
                                id=f"AI-INSECURE-API-BASE-{file_path.name}-L{line_num}",
                                title="Insecure LLM API base URL over HTTP",
                                description=(
                                    f"Code in {file_path.name} configures an LLM API base URL over HTTP "
                                    f"at line {line_num}. Unencrypted transport can expose prompts, "
                                    "responses, and credentials in transit."
                                ),
                                severity=Severity.HIGH,
                                category="ai_config",
                                owasp_id="MCP07:2025",
                                file_path=str(file_path),
                                line_number=line_num,
                                remediation="Use HTTPS endpoints for model providers and internal gateways.",
                            )
                        )

                    if browser_pattern.search(line):
                        findings.append(
                            Finding(
                                id=f"AI-BROWSER-KEY-{file_path.name}-L{line_num}",
                                title="OpenAI browser access enabled",
                                description=(
                                    f"Code in {file_path.name} enables browser-side API access at line {line_num}. "
                                    "This can expose model credentials to end users and browser tooling."
                                ),
                                severity=Severity.HIGH,
                                category="ai_config",
                                owasp_id="MCP01:2025",
                                file_path=str(file_path),
                                line_number=line_num,
                                remediation=(
                                    "Keep provider API keys server-side and proxy browser requests "
                                    "through a backend."
                                ),
                            )
                        )

                    if insecure_tls_pattern.search(line):
                        findings.append(
                            Finding(
                                id=f"AI-INSECURE-TLS-{file_path.name}-L{line_num}",
                                title="LLM client TLS verification disabled",
                                description=(
                                    f"Code in {file_path.name} disables TLS verification at line {line_num}. "
                                    "This makes model traffic vulnerable to interception and man-in-the-middle attacks."
                                ),
                                severity=Severity.HIGH,
                                category="ai_config",
                                owasp_id="MCP07:2025",
                                file_path=str(file_path),
                                line_number=line_num,
                                remediation="Enable certificate validation and trust only approved CA bundles.",
                            )
                        )

                _check_system_prompt_leaks(file_path, content, findings)
                _check_unsafe_llm_output_execution(file_path, content, findings)
            except OSError:
                continue

    return findings


def _check_system_prompt_leaks(file_path: Path, content: str, findings: list[Finding]) -> None:
    """Check for sensitive information in system prompts."""
    system_prompt_patterns = [
        re.compile(
            r"(?:system_prompt|system_message|system_content)\s*=\s*(?:f?[\"']|\"\"\")(.*?)(?:[\"']|\"\"\")",
            re.DOTALL | re.IGNORECASE,
        ),
        re.compile(
            r"\{[\"']role[\"']\s*:\s*[\"']system[\"']\s*,\s*[\"']content[\"']\s*:\s*(?:f?[\"'])(.*?)(?:[\"'])",
            re.DOTALL,
        ),
    ]

    sensitive_patterns = [
        (r"(?:api[_-]?key|password|secret|token)\s*[:=]", "credential in system prompt"),
        (
            r"(?:internal|confidential|private)\s+(?:api|endpoint|url|server)",
            "internal infrastructure reference in system prompt",
        ),
        (r"(?:database|db)://", "database connection string in system prompt"),
    ]

    for sp_pattern in system_prompt_patterns:
        for match in sp_pattern.finditer(content):
            prompt_text = match.group(1)
            for sens_pattern, description in sensitive_patterns:
                if re.search(sens_pattern, prompt_text, re.IGNORECASE):
                    line_num = content[: match.start()].count("\n") + 1
                    findings.append(
                        Finding(
                            id=f"AI-SYSTEMPROMPT-LEAK-{file_path.name}-L{line_num}",
                            title=f"Potential {description}",
                            description=(
                                f"A system prompt in {file_path.name} appears to contain sensitive information "
                                f"({description}). System prompts can be extracted through prompt injection attacks."
                            ),
                            severity=Severity.HIGH,
                            category="ai_config",
                            owasp_id="MCP10:2025",
                            file_path=str(file_path),
                            line_number=line_num,
                            remediation=(
                                "Move sensitive information out of system prompts. Use environment variables "
                                "for credentials and avoid referencing internal infrastructure in prompts."
                            ),
                        )
                    )
                    break


def _check_unsafe_llm_output_execution(file_path: Path, content: str, findings: list[Finding]) -> None:
    """Check for dangerous patterns where LLM output is executed."""
    dangerous_patterns = [
        (
            re.compile(r"eval\s*\(\s*(?:response|output|result|completion|message|content)", re.IGNORECASE),
            "eval() on LLM output",
        ),
        (
            re.compile(r"exec\s*\(\s*(?:response|output|result|completion|message|content)", re.IGNORECASE),
            "exec() on LLM output",
        ),
        (
            re.compile(r"subprocess\.\w+\(\s*(?:response|output|result|completion|message|content)", re.IGNORECASE),
            "subprocess with LLM output",
        ),
        (
            re.compile(r"os\.system\s*\(\s*(?:response|output|result|completion|message|content)", re.IGNORECASE),
            "os.system() with LLM output",
        ),
    ]

    for line_num, line in enumerate(content.splitlines(), start=1):
        for pattern, description in dangerous_patterns:
            if pattern.search(line):
                findings.append(
                    Finding(
                        id=f"AI-UNSAFE-EXEC-{file_path.name}-L{line_num}",
                        title=f"Unsafe execution of LLM output: {description}",
                        description=(
                            f"Code in {file_path.name} at line {line_num} appears to execute LLM-generated output "
                            f"using {description}. This is a critical code injection vulnerability — an attacker "
                            "can craft prompts that cause the LLM to generate malicious code."
                        ),
                        severity=Severity.CRITICAL,
                        category="ai_config",
                        owasp_id="MCP05:2025",
                        file_path=str(file_path),
                        line_number=line_num,
                        remediation=(
                            "Never execute LLM output directly. Use allowlists, sandboxed execution environments, "
                            "or structured output parsing instead."
                        ),
                    )
                )


def _scan_langchain_configs(directory: Path) -> list[Finding]:
    """Detect LangChain-specific security issues."""
    findings: list[Finding] = []

    for py_file in directory.rglob("*.py"):
        if _should_skip(py_file):
            continue
        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            if len(content) > 500_000:
                continue

            for line_num, line in enumerate(content.splitlines(), start=1):
                if re.search(r"(?:Agent|AgentExecutor|initialize_agent)\s*\(.*verbose\s*=\s*True", line):
                    findings.append(
                        Finding(
                            id=f"AI-LANGCHAIN-VERBOSE-{py_file.name}-L{line_num}",
                            title="LangChain agent verbose mode enabled",
                            description=(
                                f"Agent in {py_file.name} has verbose=True, which exposes internal reasoning, "
                                "tool calls, and intermediate outputs. In production, this can leak sensitive "
                                "information through logs or user-facing output."
                            ),
                            severity=Severity.MEDIUM,
                            category="ai_config",
                            file_path=str(py_file),
                            line_number=line_num,
                            remediation=(
                                "Set verbose=False for production deployments. Use callbacks "
                                "for structured logging instead."
                            ),
                        )
                    )

                if re.search(r"allow_dangerous_requests\s*=\s*True", line):
                    findings.append(
                        Finding(
                            id=f"AI-LANGCHAIN-DANGEROUS-{py_file.name}-L{line_num}",
                            title="LangChain dangerous requests explicitly allowed",
                            description=(
                                f"Code in {py_file.name} explicitly allows dangerous requests. "
                                "This disables safety guardrails that prevent potentially harmful operations."
                            ),
                            severity=Severity.HIGH,
                            category="ai_config",
                            owasp_id="MCP05:2025",
                            file_path=str(py_file),
                            line_number=line_num,
                            remediation=(
                                "Remove allow_dangerous_requests=True unless absolutely required, "
                                "and add compensating controls."
                            ),
                        )
                    )
        except OSError:
            continue

    return findings


def _scan_docker_configs(directory: Path) -> list[Finding]:
    """Detect security issues in Dockerfiles used for AI agents."""
    findings: list[Finding] = []

    for dockerfile in directory.rglob("Dockerfile*"):
        if _should_skip(dockerfile):
            continue
        try:
            content = dockerfile.read_text(encoding="utf-8", errors="ignore")

            has_user_directive = bool(re.search(r"^USER\s+(?!root)", content, re.MULTILINE))
            if not has_user_directive and "FROM" in content:
                findings.append(
                    Finding(
                        id=f"AI-DOCKER-ROOT-{dockerfile.name}",
                        title=f"Agent container runs as root ({dockerfile.name})",
                        description=(
                            f"Dockerfile {dockerfile.name} does not set a non-root USER. "
                            "AI agents running as root in containers have unrestricted access "
                            "to the filesystem and can escape container isolation more easily."
                        ),
                        severity=Severity.MEDIUM,
                        category="ai_config",
                        file_path=str(dockerfile),
                        remediation="Add 'USER nonroot' or 'USER 1000' to run the agent as a non-root user.",
                    )
                )

            for line_num, line in enumerate(content.splitlines(), start=1):
                if re.search(r"^ENV\s+\w*(?:KEY|SECRET|TOKEN|PASSWORD|PASS)\w*\s*=", line, re.IGNORECASE):
                    findings.append(
                        Finding(
                            id=f"AI-DOCKER-SECRET-{dockerfile.name}-L{line_num}",
                            title=f"Secret in Dockerfile ENV ({dockerfile.name})",
                            description=(
                                f"Dockerfile {dockerfile.name} sets a secret via ENV at line {line_num}. "
                                "ENV values are baked into image layers and visible to anyone with image access."
                            ),
                            severity=Severity.HIGH,
                            category="ai_config",
                            owasp_id="MCP01:2025",
                            file_path=str(dockerfile),
                            line_number=line_num,
                            remediation=(
                                "Use Docker secrets, runtime environment variables, or a secrets "
                                "manager instead of ENV."
                            ),
                        )
                    )
        except OSError:
            continue

    return findings


def _scan_env_files(directory: Path) -> list[Finding]:
    """Check for .env files that shouldn't be committed."""
    findings: list[Finding] = []

    for env_file in directory.rglob(".env"):
        if _should_skip(env_file):
            continue

        gitignore_path = directory / ".gitignore"
        env_in_gitignore = False
        if gitignore_path.exists():
            gitignore_content = gitignore_path.read_text(encoding="utf-8", errors="ignore")
            env_in_gitignore = any(
                line.strip() in (".env", "*.env", ".env*")
                for line in gitignore_content.splitlines()
            )

        if not env_in_gitignore:
            findings.append(
                Finding(
                    id=f"AI-ENV-NOT-GITIGNORED-{env_file.parent.name}",
                    title=".env file not in .gitignore",
                    description=(
                        f"Found .env file at {env_file} but .env is not listed in .gitignore. "
                        "This means secrets in .env may be committed to version control."
                    ),
                    severity=Severity.HIGH,
                    category="ai_config",
                    owasp_id="MCP01:2025",
                    file_path=str(env_file),
                    remediation=(
                        "Add '.env' to your .gitignore file immediately. Rotate any secrets "
                        "that may have been committed."
                    ),
                )
            )

    return findings


def _scan_requirements_for_pinned_versions(directory: Path) -> list[Finding]:
    """Check if AI/ML dependencies have pinned versions."""
    findings: list[Finding] = []

    ai_packages = {
        "openai",
        "anthropic",
        "langchain",
        "langchain-core",
        "langchain-openai",
        "crewai",
        "autogen",
        "transformers",
        "torch",
        "tensorflow",
        "pinecone-client",
        "chromadb",
        "weaviate-client",
        "cohere",
        "huggingface-hub",
        "litellm",
        "guidance",
        "semantic-kernel",
    }

    for req_file in directory.rglob("requirements*.txt"):
        if _should_skip(req_file):
            continue
        try:
            content = req_file.read_text(encoding="utf-8", errors="ignore")
            unpinned: list[str] = []

            for line in content.splitlines():
                stripped_line = line.strip()
                if not stripped_line or stripped_line.startswith("#") or stripped_line.startswith("-"):
                    continue

                pkg_name = re.split(r"[>=<!\[]", stripped_line)[0].strip().lower()
                if pkg_name in ai_packages and "==" not in stripped_line and ">=" not in stripped_line:
                    unpinned.append(pkg_name)

            if unpinned:
                unique_unpinned = sorted(set(unpinned))
                findings.append(
                    Finding(
                        id=f"AI-UNPINNED-DEPS-{req_file.name}",
                        title=f"Unpinned AI dependencies in {req_file.name}",
                        description=(
                            f"AI/ML packages without pinned versions: {', '.join(unique_unpinned)}. "
                            "Unpinned dependencies can introduce breaking changes or supply chain attacks."
                        ),
                        severity=Severity.MEDIUM,
                        category="ai_config",
                        owasp_id="MCP04:2025",
                        file_path=str(req_file),
                        remediation=(
                            f"Pin versions for: {', '.join(unique_unpinned)} (e.g., openai==1.30.0)."
                        ),
                    )
                )
        except OSError:
            continue

    return findings


def _should_skip(path: Path) -> bool:
    """Check if a path should be skipped during scanning."""
    skip_dirs = {
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        ".tox",
        ".mypy_cache",
        ".pytest_cache",
        "dist",
        "build",
        ".eggs",
    }
    return any(part in skip_dirs for part in path.parts)
