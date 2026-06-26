# We Scanned 1,187 Real MCP Configs from Public GitHub Repos — Here's What We Found

**A security analysis of real-world Model Context Protocol configurations**

*May 31, 2026 · Arpitha Dhanapathi*

---

## TL;DR

We collected **1,187 unique MCP configuration files** from **1,162 public GitHub repositories** and ran a static security scan against every one of them. The results:

- **100%** of configs had at least one security finding
- **24.2%** had CRITICAL or HIGH severity issues
- **142 hardcoded secrets** (API keys, passwords, database credentials) committed to public repos
- **96 configs** with CRITICAL findings (browser hijack, shell execution, exposed databases)
- **2,990 total findings** across 5 categories

No configs were exploited. No servers were executed. Every finding is from static analysis only — we never connected to any MCP server.

---

## Why We Did This

The Model Context Protocol (MCP) is exploding. Anthropic's open standard for connecting AI agents to tools has been adopted by Claude, Cursor, VS Code, Windsurf, Gemini CLI, and dozens more. There are now 10,000+ MCP servers published across GitHub, npm, and PyPI.

But MCP configs are also where the security risks live. Every `claude_desktop_config.json` file tells an AI agent which tools it can use, which servers to connect to, and what credentials to pass. A misconfigured MCP setup can give an AI agent access to your filesystem, your browser, your database, or your shell — often with no authentication and no limits.

We wanted to know: **How are people actually configuring MCP in the real world? And how many of those configs have security issues?**

So we built a scanner and pointed it at GitHub.

---

## Methodology

### Collection

We used the GitHub Code Search API to find MCP configuration files across public repositories. Our search queries targeted:

- Files named `claude_desktop_config.json`
- JSON files containing `mcpServers` or `mcp_servers` keys
- Config files referencing popular MCP servers (Playwright, Context7, Serena, etc.)

For each result, we downloaded the raw file, validated it was a parseable MCP config (containing a servers section with at least one server definition), and deduplicated by content hash.

**Collection stats:**
- 2,200 GitHub search results examined
- 2,053 files downloaded
- 1,843 validated as MCP configs
- **1,187 unique configs** after deduplication (by content hash)
- From **1,162 distinct repositories**
- Max 3 configs per repository (to avoid repo-specific bias)

### Scanning

We scanned every config using [Pluto AgentGuard](https://github.com/arpitha-dhanapathi/pluto-aguard) (`pluto-aguard` on PyPI), an open-source static security scanner for MCP configurations. The scanner checks for:

1. **Hardcoded secrets** — API keys, passwords, tokens, and credentials in environment variables
2. **Dangerous server packages** — Servers with filesystem access, browser control, shell execution, or database access
3. **Missing authentication** — Servers exposed over HTTP/SSE without auth configuration
4. **Transport security** — HTTP connections without TLS
5. **Context safety** — Missing response limits, session limits, and external content fetching without sandboxing

**Important limitations:**
- This is purely static analysis. We never executed any MCP server or connected to any endpoint.
- We cannot detect prompt injection in tool descriptions (that requires executing the server).
- "Missing response limit" and "missing session limit" are heuristic checks — the absence of a config field doesn't prove the server lacks the capability.
- Some "secrets" may be placeholder values (like `your-api-key-here`). We flag any environment variable matching known secret patterns.

---

## Results Overview

| Metric | Value |
|---|---|
| Configs scanned | 1,187 |
| Configs with at least one finding | 1,187 (100%) |
| Total findings | 2,990 |
| CRITICAL findings | 128 |
| HIGH findings | 318 |
| MEDIUM findings | 2,544 |
| Configs with CRITICAL or HIGH (max severity) | 291 (24.2%) |
| Total MCP servers defined | 2,351 |
| Hardcoded secrets found | 142 |
| Unique repositories | 1,162 |

### Findings by Category

| Category | Findings | % of Total |
|---|---|---|
| Context safety (missing limits, external fetch) | 2,544 | 85.1% |
| Permissions (dangerous server packages) | 169 | 5.7% |
| Secrets (hardcoded API keys & passwords) | 142 | 4.7% |
| Authentication (missing auth on HTTP servers) | 104 | 3.5% |
| Transport (HTTP without TLS) | 31 | 1.0% |

---

## Finding 1: The Filesystem Server Is Everywhere

The most common dangerous pattern is the **MCP filesystem server** — a server that gives an AI agent direct read/write access to your disk.

**86 configs (7.2%)** include a filesystem server. That's 1 in every 14 configs giving an AI agent the ability to read, write, create, and delete files on the host machine.

The MCP filesystem server (`@modelcontextprotocol/server-filesystem`) is the 1st most popular server in our dataset. It typically grants access to specific directories:

```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
}
```

The security risk: a prompt injection attack could instruct the agent to read `~/.ssh/id_rsa`, `~/.aws/credentials`, or any file within the granted path. The server itself has no defense against this — it faithfully serves whatever the agent requests.

---

## Finding 2: 142 Hardcoded Secrets in Public Repos

We found **142 hardcoded secrets** across **99 configs** (8.3% of all configs). These are real API keys, passwords, tokens, and credentials committed to public GitHub repositories in plaintext.

### Most Common Exposed Secret Types

| Secret Type | Count |
|---|---|
| GitHub Personal Access Tokens | 7 |
| OpenAI API Keys | 5 |
| Neo4j Database Passwords | 5 |
| Google Application Credentials | 5 |
| Brave Search API Keys | 4 |
| Gemini API Keys | 4 |
| Weather API Keys | 3 |
| OpenRouter API Keys | 3 |
| E2B API Keys | 3 |
| Supabase Access Tokens | 3 |
| Database Passwords (various) | 6 |
| Anthropic API Keys | 2 |
| Stripe Secret Keys | 2 |
| Salesforce Passwords/Tokens | 3 |
| Other API keys/tokens | 87 |

**10 configs contained database connection strings** with embedded credentials (PostgreSQL, MySQL, Redis URLs with passwords inline).

Some of these may be intentional placeholders or test credentials. But GitHub Personal Access Tokens and Stripe Secret Keys are not the kind of values people typically use as placeholders.

**If you recognize your credentials in this description:** rotate them immediately. These configs are on public GitHub repos indexed by search engines and scraped by credential scanners.

---

## Finding 3: 96 Configs with CRITICAL Severity Issues

**96 configs (8.1%)** have at least one CRITICAL finding. These represent the highest-risk configurations — servers with browser hijacking capability, shell execution, or critical exposed credentials.

### CRITICAL Findings Breakdown

| Risk | Description | Configs |
|---|---|---|
| **Browser control** | Chrome DevTools MCP — full browser hijacking via DevTools Protocol | 11 |
| **Shell execution** | Serena — server that can execute arbitrary shell commands | 11 |
| **Browser automation** | Playwright MCP — programmatic browser control, can navigate to any URL, extract any page content | 37 |
| **Hardcoded credentials** | Critical secrets (database passwords, private keys, webhook secrets) | 37+ |

Chrome DevTools MCP (`@anthropic/chrome-devtools-mcp`) connects to Chrome's DevTools Protocol, giving an AI agent the ability to:
- Navigate to any URL (including `file://` and internal network addresses)
- Read page content, cookies, and local storage
- Execute arbitrary JavaScript in the browser context
- Take screenshots

Serena gives an AI agent the ability to execute shell commands on the host machine. Combined with the lack of response limits, this creates a remote code execution surface controlled by natural language.

---

## Finding 4: What Developers Are Actually Using

Across 1,187 configs, we catalogued **2,351 MCP server instances** spanning hundreds of unique servers. Here are the 20 most popular:

| Rank | Server | Configs | Category |
|---|---|---|---|
| 1 | **filesystem** | 86 | File system access |
| 2 | **playwright** | 54 | Browser automation |
| 3 | **github** | 52 | Source control |
| 4 | **context7** | 48 | Documentation lookup |
| 5 | **sequential-thinking** | 35 | Reasoning tool |
| 6 | **memory** | 26 | Persistent memory |
| 7 | **supabase** | 25 | Database (BaaS) |
| 8 | **fetch** | 18 | Web fetching |
| 9 | **brave-search** | 18 | Web search |
| 10 | **puppeteer** | 17 | Browser automation |
| 11 | **weather** | 14 | Weather data |
| 12 | **sqlite** | 12 | Database |
| 13 | **serena** | 11 | Code assistant (shell exec) |
| 14 | **chrome-devtools** | 11 | Browser control |
| 15 | **git** | 10 | Version control |
| 16 | **desktop-commander** | 10 | Desktop control |
| 17 | **postgres** | 10 | Database |
| 18 | **agentkit** | 10 | Agent framework |
| 19 | **laravel-boost** | 10 | Laravel dev tools |
| 20 | **time** | 9 | Time/date utilities |

**Key insight:** 4 of the top 5 most popular servers involve external access (filesystem, browser, GitHub, web docs). Developers are giving AI agents broad access to their environment as a default, not as a carefully considered exception.

### Config Complexity Distribution

| Servers per config | Configs | % |
|---|---|---|
| 1 server | 901 | 75.1% |
| 2–5 servers | 227 | 18.9% |
| 6–10 servers | 54 | 4.5% |
| 11+ servers | 18 | 1.5% |

75% of configs define just a single MCP server. But the tail is long — one config had **49 servers**, giving a single AI agent access to 49 different tools simultaneously.

---

## Finding 5: 79 Configs Expose Servers Without Authentication

**79 configs (6.6%)** connect to MCP servers over HTTP or SSE **without any authentication configuration**. This means the MCP server endpoint is accessible to anyone who can reach it — no API key, no token, no auth header.

**30 of these** also use plain HTTP (not HTTPS), meaning the connection has no transport encryption either. An attacker on the same network could intercept all communication between the AI agent and the MCP server.

Servers exposed without auth include: Supabase, Context7, Figma, Grafana, Sentry, Linear, Stripe, and various custom servers.

---

## What This Means

### The Good News
MCP is working as designed. Developers are connecting AI agents to real tools — filesystems, databases, browsers, APIs — and getting productive value from it. The protocol itself isn't broken.

### The Bad News
The default security posture is **wide open**. Not a single config in our dataset of 1,187 included response limits or session limits. 8.3% have hardcoded secrets on public GitHub. 24.2% have CRITICAL or HIGH severity issues.

This mirrors the early days of cloud computing, when S3 buckets were routinely left public, or the early days of Docker, when images were routinely run as root. The tooling exists to do better — developers just haven't adopted security practices for MCP yet.

### The Uncomfortable Truth
Most of these findings are MEDIUM severity (context safety). The scanner flags every config that lacks response limits and session limits. You could argue this is noise — that these limits should be the server's responsibility, not the config's.

That's a fair criticism. If we exclude context safety findings and focus only on CRITICAL, HIGH, and concrete secrets:

- **446 non-context findings** across **291 configs (24.2%)**
- Still nearly 1 in 4 configs with a real, actionable security issue
- 142 hardcoded secrets that should never be in a public repo

---

## Recommendations

### For Individual Developers

1. **Never commit MCP configs with real credentials.** Use environment variable references (`${GITHUB_TOKEN}`) instead of inline values. Add `claude_desktop_config.json` to your `.gitignore`.

2. **Audit which servers you're running.** Do you really need filesystem + browser + shell access for your current task? Principle of least privilege applies to AI agents too.

3. **Scan your config.** Run `pip install pluto-aguard && aguard scan .` on any project with MCP configs. It takes 5 seconds and catches the issues described in this report.

### For MCP Server Authors

1. **Document the security implications of your server.** If your server grants filesystem/browser/shell access, say so prominently. Users should make informed decisions about what they're enabling.

2. **Support authentication by default.** Servers exposed via HTTP/SSE should require an auth token out of the box, not as an optional configuration.

3. **Implement response limits.** A malicious prompt shouldn't be able to exfiltrate unlimited data through your server.

### For Platform Teams

1. **Add MCP config scanning to CI/CD.** Treat MCP configs like infrastructure-as-code — they define what your AI agents can do, and they deserve the same security review.

2. **Write a security policy for AI agent tools.** Define which MCP servers are approved, what credentials they can use, and what access patterns are acceptable.

3. **Monitor for config drift.** Developers add MCP servers incrementally. What starts as a single filesystem server can grow to 49 servers without anyone reviewing the security implications.

---

## Reproduce This Research

Everything used in this analysis is open source:

```bash
# Install the scanner
pip install pluto-aguard

# Scan your own MCP configs
aguard scan /path/to/your/configs

# Scan with JSON output for automation
aguard scan . --format json

# Generate an OWASP-inspired control coverage report
aguard owasp .
```

**Scanner:** [github.com/arpitha-dhanapathi/pluto-aguard](https://github.com/arpitha-dhanapathi/pluto-aguard)
**PyPI:** [pypi.org/project/pluto-aguard](https://pypi.org/project/pluto-aguard/)

The collection and scanning scripts, raw metadata, and aggregated results from this study will be published separately. Individual config files and repository names are not published to avoid exposing specific developers' credentials.

---

## Limitations & Disclosure

- **Static analysis only.** We never executed any MCP server, connected to any endpoint, or tested any credential. All findings are from parsing configuration files.

- **Public repos only.** Every config analyzed is from a public GitHub repository, indexed by GitHub's code search.

- **No names published.** We do not identify specific developers, repositories, or organizations. The statistics are aggregated.

- **Scanner limitations.** The scanner uses pattern matching and heuristics. False positives are possible (placeholder values flagged as secrets, test configs flagged as production). False negatives are certain (we cannot detect prompt injection in tool descriptions without executing the server).

- **Selection bias.** Our dataset skews toward `claude_desktop_config.json` files (the most common MCP config filename). Configs for other clients (Cursor, VS Code, Windsurf) may have different patterns.

- **Context safety is noisy.** The "missing response limit" and "missing session limit" rules fire on every config because no standard config format currently includes these fields. We report them for completeness but acknowledge they inflate the "100% with findings" headline.

---

## About

This research was conducted by [Arpitha Dhanapathi](https://github.com/arpitha-dhanapathi) using [Pluto AgentGuard](https://github.com/arpitha-dhanapathi/pluto-aguard), an open-source, OWASP-inspired security scanner for AI agent configurations.

Pluto AgentGuard scans MCP configs statically (no server execution, no API keys required), tests security policies against 22 attack scenarios, and generates compliance evidence for AI governance. It runs offline, in CI/CD, or as a GitHub Action.

*Have questions or feedback? Open an issue on [GitHub](https://github.com/arpitha-dhanapathi/pluto-aguard/issues) or reach out on [LinkedIn](https://linkedin.com/in/arpitha-dhanapathi).*

---

*Published May 31, 2026. Data collected and analyzed on the same date.*
