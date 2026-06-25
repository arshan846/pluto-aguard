# Scan Results Methodology

## Dataset: 1,200 Public MCP Configs

**Collection date:** June 25, 2026  
**Scanner version:** pluto-aguard v0.9.2

### How configs were collected

1. Used GitHub Code Search API via `gh` CLI to find MCP config files across public repositories
2. Search queries targeted: `claude_desktop_config.json`, `.mcp.json`, `mcp_config.json`, `settings.json` with `mcpServers` key
3. Downloaded raw file content and validated as valid MCP config (must contain `mcpServers` or `mcp_servers` dict with ≥1 server)
4. De-duplicated by content hash (SHA-256)
5. Capped at 3 configs per repo to avoid single-repo bias

### Inclusion criteria

- Public GitHub repository
- Valid JSON with `mcpServers` or `mcp_servers` key containing at least one server entry
- Unique content hash (no duplicates)

### Scan methodology

- Each config scanned using `scan_mcp_config()` directly (no subprocess overhead)
- Findings categorized by: secrets, permissions, authentication, transport, context_safety
- Severity assigned per rule: CRITICAL, HIGH, MEDIUM
- Risk score: `min(100, critical_high_count × 25)`

### What we DON'T claim

- This is not a representative sample of all MCP users (only those who commit configs publicly)
- Configs committed to public repos may be examples/demos rather than production configs
- We cannot distinguish "intentionally insecure for testing" from "accidentally insecure"
- Context safety findings (response/session limits) are advisory — no MCP standard mandates them yet

### Popular servers subset

The 11 most popular MCP servers were identified by GitHub star count as of June 25, 2026. Example configs were sourced from each project's official README or documentation.

| Server | Repository | Stars |
|---|---|---|
| Context7 | upstash/context7 | 58,057 |
| Chrome DevTools | ChromeDevTools/chrome-devtools-mcp | 44,422 |
| Playwright | microsoft/playwright-mcp | 34,339 |
| GitHub MCP | github/github-mcp-server | 30,963 |
| Serena | oraios/serena | 25,785 |
| FastMCP | PrefectHQ/fastmcp | 25,791 |
| Activepieces | activepieces/activepieces | 22,985 |
| n8n-mcp | czlonkowski/n8n-mcp | 21,961 |
| Google Toolbox | googleapis/mcp-toolbox | 15,710 |
| Figma MCP | GLips/Figma-Context-MCP | 15,230 |
| mcp-chrome | hangwin/mcp-chrome | 11,985 |
