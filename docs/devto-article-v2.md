# I Scanned 1,200 MCP Server Configs from GitHub — Here's What I Found

## TL;DR

I built [Pluto AgentGuard](https://github.com/arshan846/pluto-aguard), an open-source MCP security scanner, and ran it against 1,200 real MCP server configurations from public GitHub repos.

The key finding: **13% expose remote endpoints with zero authentication.**

---

## Why This Matters

MCP (Model Context Protocol) is how AI agents connect to tools — databases, file systems, APIs, browsers. A misconfigured MCP server is an unauthenticated backdoor into your infrastructure.

But not all misconfigurations are equal. I built a scanner to separate real risks from noise.

---

## The Results

| Severity | Count | What it means |
|----------|-------|---------------|
| HIGH | 189 | Remote endpoints with no authentication |
| MEDIUM | 169 | Unencrypted HTTP on non-localhost transport |
| INFO | 2,533 | Capability inventory (shell access, network fetch, etc.) |

**156 repos (13%) had at least one HIGH-severity finding** — 189 unauthenticated remote endpoints across those repos.

---

## The Three Things That Actually Matter

### 1. Remote endpoints without authentication (13%)

If your MCP server listens on a network address with no auth, anyone on that network can invoke your tools. No exploit needed — just a well-formed JSON-RPC request.

```json
{
  "mcpServers": {
    "my-server": {
      "url": "https://api.example.com/mcp"
    }
  }
}
```

No `Authorization` header. No API key. Wide open.

### 2. Hardcoded secrets in configs

API keys, tokens, and database passwords committed directly in JSON. Environment variable references (`${API_KEY}`) exist for a reason.

### 3. eval() on LLM output

Rare, but when present — catastrophic. Server implementations that pass model-generated strings directly to `eval()`. Textbook remote code execution.

---

## What's NOT a Vulnerability

One thing I learned building this scanner: **not everything that looks scary is actually a security issue.**

- **"Server has shell-execution tools"** — That's a feature. The [MCP spec](https://modelcontextprotocol.io/specification/2025-03-26/architecture) puts enforcement responsibility on the client/host: *"The host process enforces security policies and consent requirements."* Claude Desktop, Cursor, and other mainstream clients prompt before executing.

- **"No response size limits"** — The MCP spec has no standard field for this. Flagging its absence is a tautology.

- **"Dangerous package detected"** — Filesystem access, browser automation, shell execution — these are the *reason* MCP servers exist. The scanner reports them for awareness, not as vulnerabilities.

---

## How the Scanner Works

Pluto AgentGuard performs static analysis on MCP configuration files (JSON/YAML):

- **Auth detection** — checks for `headers`, API keys, token references
- **Transport analysis** — flags remote HTTP without TLS
- **Secret scanning** — regex patterns for hardcoded credentials
- **Capability inventory** — catalogs what tools are exposed (informational)

No runtime required. No server access needed. Just point it at your config directory.

---

## Grounded in Standards

Findings are mapped to established security frameworks:

| Finding | OWASP Agentic AI Threat |
|---------|------------------------|
| AUTH-MISSING | **Tool Misuse** — unauthenticated endpoints allow unauthorized tool invocation |
| TRANSPORT-HTTP | **Insecure Communication** — unencrypted channels expose data in transit |
| SECRET-HARDCODED | **Credential Leakage** — secrets in config files end up in version control |
| EVAL-INJECTION | **Prompt Injection → Code Execution** — LLM output passed to eval() |

The scanner also references the [NSA Cybersecurity Information Sheet on AI systems](https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4235509/) (May 2025) and the [MCP Architecture Specification](https://modelcontextprotocol.io/specification/2025-03-26/architecture) for trust boundary guidance.

---

## Try It

```bash
pip install pluto-aguard
pluto-aguard scan ./my-mcp-configs/ --format table
```

Or scan a single config:

```bash
pluto-aguard scan ~/.cursor/mcp.json
```

[GitHub → pluto-aguard](https://github.com/arshan846/pluto-aguard) | Open source, MIT licensed.

---

## Key Takeaways

1. **Add authentication to remote MCP endpoints.** Even a bearer token header blocks drive-by invocations.
2. **Never commit secrets in MCP configs.** Use `${ENV_VAR}` references.
3. **Understand the trust boundary.** MCP servers provide capabilities; clients enforce approval. A server with shell access isn't a vulnerability if your client prompts before executing.
4. **Scan your configs.** 13% of public repos got this wrong. You might be one of them.
