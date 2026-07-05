# Config Schema: What's Standard vs. What's AgentGuard's

`aguard scan` reads several different kinds of files. Some checks apply to
the actual MCP client config format; others require metadata that only
exists in AgentGuard's own schema. This page draws that line explicitly, so
a scan of a real, unmodified `claude_desktop_config.json` doesn't leave you
wondering why certain checks never fire.

## 1. Real MCP client config (`mcpServers` block)

A bare `claude_desktop_config.json` / `.mcp.json` — the format Claude
Desktop, Cursor, and most other MCP clients actually write — looks like
this:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    },
    "remote-example": {
      "url": "https://example.com/mcp",
      "headers": { "Authorization": "Bearer ${TOKEN}" }
    }
  }
}
```

The only fields present are `command`, `args`, `env`, and — for remote/SSE
servers — `url`, `headers`, `auth`. There is no `permissions`, `scope`, or
`tools` (with a `description`) on a server entry; the MCP spec doesn't
define those there.

Checks that operate on these real fields, and therefore fire on any
unmodified config:

| Check | Fields used |
|---|---|
| Insecure HTTP transport | `url` |
| Missing / weak authentication | `auth`, `headers`, `url` |
| Hardcoded secrets in `env` | `env` |
| Connection strings with embedded credentials | `args`, `env` |
| Known dangerous server packages (awareness) | `command`, `args`, `url` |
| External-content-fetch / indirect-injection risk (awareness) | `command`, `args` |

See [examples/claude_desktop_config.json](../examples/claude_desktop_config.json)
for a fixture built entirely from real fields — `aguard scan` against it
produces exactly the checks in the table above and nothing from the
sections below.

## 2. AgentGuard's extended per-server metadata

`_check_server_permissions` (wildcard/broad permissions, dangerous tool
names) and `_check_tool_definitions` (tool-poisoning via a `description`
field) look for `permissions` / `scope` / `access` / `tools` directly on an
`mcpServers.*` entry. These aren't part of the MCP spec — some enterprise
MCP gateways or proxies add this kind of governance metadata themselves,
and if yours does, these checks apply. On a bare client config, they simply
won't find anything to flag; that's expected, not a missed detection.

`examples/insecure-agent-config.yaml` and `examples/secure-agent-config.yaml`
add this metadata deliberately, to demonstrate the checks — see the notes
at the top of those files.

## 3. AgentGuard's agent-config schema (top-level keys)

Separately, `whatif`, `evidence`, `monitor --policy`, and `baseline` consume
a top-level schema that isn't MCP-related at all — it's AgentGuard's own
representation of an agent's declared policy:

```yaml
name: my-agent
tools: [sql_query, file_write]
permissions:
  sql_query: { access: read }
require_human_approval: [file_write]
data_access_rules: { customer_db: read }
timeout: 300
rate_limit: { calls_per_minute: 100 }
network: { egress: allowlist }
runtime: { sandbox: true }
auth: { token_type: ephemeral }
permission_model: allowlist
```

This is the schema `permission_scanner.py`'s `calculate_permission_risk_score`
and the `whatif` simulator's built-in policies read and write. It has no
equivalent in the MCP spec — it's the format you write yourself (or
generate) to describe an agent's policy for AgentGuard to score and
simulate against.
