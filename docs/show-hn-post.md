# Show HN: I Scanned 1,187 Real MCP Configs from GitHub — 24% Have Critical/High Security Issues

I built an open-source static security scanner for MCP (Model Context Protocol) configurations and ran it against 1,187 unique configs collected from 1,162 public GitHub repos.

**Headline findings:**

- 100% of configs had at least one finding (mostly missing response/session limits — fair to call this noisy)
- **24.2% had CRITICAL or HIGH issues** — this is the real number
- **142 hardcoded secrets** (GitHub PATs, OpenAI keys, Stripe secrets, database passwords) committed to public repos
- **96 configs with CRITICAL findings** (browser hijack via Chrome DevTools, shell execution via Serena)
- 86 configs grant filesystem access, 54 use Playwright (browser automation), 48 use Context7

**Most common exposed secrets:** GitHub Personal Access Tokens (7), OpenAI API keys (5), Neo4j passwords (5), Google credentials (5), database connection strings (10).

**The uncomfortable truth:** The "100% with findings" headline is inflated by context safety heuristics (every config lacks response/session limits because no config format defines them). Strip those out and you still have **446 concrete findings across 291 configs** — nearly 1 in 4 with a real, actionable issue.

## What I built

[Pluto AgentGuard](https://github.com/arpitha-dhanapathi/pluto-aguard) (`pip install pluto-aguard`) — a static-only MCP security scanner. Key design choice: it **never executes MCP servers**. Unlike Snyk's agent-scan (which connects to servers to read tool descriptions), this is purely static analysis. Safer to run on untrusted configs, but shallower — it can't detect prompt injection in tool descriptions.

```bash
pip install pluto-aguard
aguard scan /path/to/your/config
```

It checks for: hardcoded secrets, dangerous server packages (filesystem, browser, shell, database), missing authentication, HTTP without TLS, connection strings, and context safety gaps. It also does policy coverage testing and generates OWASP-inspired control reports.

## Methodology

- Searched GitHub Code Search API for `claude_desktop_config.json` files and JSON files with `mcpServers` keys
- Downloaded 2,053 files, validated 1,843 as real MCP configs
- Deduplicated by content hash → 1,187 unique configs
- Capped at 3 configs per repository to avoid bias
- Scanned with pluto-aguard's `scan_mcp_config()` function
- No servers executed. No endpoints contacted. No credentials tested.

## What I learned

1. **Filesystem server is the #1 most popular MCP server** (86 configs, 7.2%). Developers give AI agents disk access as a default, not as a carefully considered exception.

2. **MCP security is where cloud security was in 2015.** Wide-open configs, credentials in repos, no limits. The tooling gap is real.

3. **The "100% flagged" number is honest but misleading.** Context safety rules (no response limits, no session limits) fire on everything. I report this transparently because I think honesty matters more than impressive numbers.

4. **Nobody is doing MCP config security in CI/CD yet.** I couldn't find a single repo with an MCP security scanning step in their CI pipeline.

## Links

- **GitHub:** https://github.com/arpitha-dhanapathi/pluto-aguard
- **PyPI:** https://pypi.org/project/pluto-aguard/
- **Full research report:** https://github.com/arpitha-dhanapathi/pluto-aguard/blob/master/docs/research-report.md

Happy to answer questions. This is a solo side project — feedback on both the scanner and the research methodology is welcome.
