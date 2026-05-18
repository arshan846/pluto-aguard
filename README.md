# 🛡️ Pluto AgentGuard

**Open-source AI Agent Security Scanner — "OWASP ZAP for AI Agents"**

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

Guardrails tell an LLM what not to say. **Pluto AgentGuard watches what the agent actually does.**

Existing tools (Azure AI Content Safety, NeMo Guardrails, Guardrails AI) protect LLM inputs and outputs. But modern AI agents don't just generate text — they call tools, access databases, write files, and chain actions across systems via MCP and other protocols. **Nobody is auditing that behavior.**

Pluto AgentGuard fills the gap *above* guardrails:

- 🔍 **Scan** MCP server configs for vulnerabilities (OWASP MCP Top 10)
- 📡 **Monitor** agent behavior across turns — tool calls, data access, permission usage
- 🚨 **Detect** permission drift — agents exceeding their declared capabilities
- 🔮 **Simulate** policy changes — "What if I restrict this tool?" → see risk score change instantly

## Quick Start

```bash
pip install pluto-aguard

# Scan an agent project for security issues
aguard scan ./my-agent-project/

# Monitor agent behavior in real-time
aguard monitor --trace-file traces.jsonl

# Simulate policy changes
aguard whatif --config agent-config.yaml
```

## Features

### `aguard scan` — Static Security Analysis

Scans your agent project for vulnerabilities mapped to the [OWASP MCP Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/):

```
$ aguard scan ./my-agent-project/

🔍 Scanning MCP configurations...
  ⚠️  CRITICAL: mcp-server-postgres has wildcard permissions (OWASP-MCP-03)
  ⚠️  HIGH: API key hardcoded in .env (OWASP-MCP-07)
  ⚠️  MEDIUM: mcp-server-github uses long-lived token (OWASP-MCP-05)
  ✅ mcp-server-slack: permissions scoped correctly

📊 Risk Score: 72/100 (High)
📄 Full report: ./aguard-report.html
```

### `aguard monitor` — Runtime Behavioral Audit

Monitors agent sessions and detects unauthorized behavior:

```
$ aguard monitor --trace-file traces.jsonl

📡 Monitoring agent session...
  Turn 1: User asked about Q2 revenue
  Turn 2: Agent called tool: sql_query("SELECT * FROM financials")
  Turn 3: ⚠️ DRIFT: Agent called tool: file_write("/tmp/export.csv")
          → Agent has READ permission only. Write action unauthorized.
  Turn 4: Agent returned response with PII (SSN detected)

🚨 2 policy violations detected in 4 turns
```

### `aguard whatif` — Policy Impact Simulator

Simulate the effect of security policy changes *before* applying them:

```
$ aguard whatif --config agent-config.yaml

Current Risk Score: 82/100

Simulating policy changes:
  ✅ "Restrict SQL tool to SELECT-only"     → Score: 68 (-17%)
  ✅ "Add human-in-the-loop for file ops"   → Score: 54 (-34%)
  ✅ "Rotate API key to ephemeral tokens"   → Score: 48 (-41%)

💡 Top recommendation: Apply all 3 → Risk drops to 38/100 (-54%)
```

## Why Pluto AgentGuard?

| Capability | Content Safety / Guardrails | Cisco MCP Scanner | **Pluto AgentGuard** |
|---|---|---|---|
| Content filtering | ✅ | — | — (not the point) |
| PII/DLP | ✅ | — | — (not the point) |
| MCP config scanning | — | Basic | **Deep + OWASP mapped** |
| Agent behavioral audit | — | — | **✅ Core feature** |
| Permission drift detection | — | — | **✅ Core feature** |
| What-If policy simulation | — | — | **✅ Unique** |
| Framework agnostic | Vendor-specific | MCP only | **All frameworks** |

## Supported Frameworks

- **MCP** (Model Context Protocol) servers and clients
- **LangChain** / **LangGraph** agents
- **CrewAI** multi-agent systems
- **AutoGen** agents
- **Azure AI Foundry** agents
- **Custom agents** (via OpenTelemetry traces)

## Architecture

```
┌─────────────────────────────────────────────┐
│                 aguard CLI                   │
├─────────────┬──────────────┬────────────────┤
│   Scanner   │   Monitor    │   Simulator    │
│             │              │                │
│ • MCP config│ • OTel trace │ • Risk scoring │
│ • Secrets   │   ingestion  │ • Policy graph │
│ • Perms     │ • Drift      │ • What-If      │
│ • OWASP map │   detection  │   engine       │
├─────────────┴──────────────┴────────────────┤
│              Rules Engine                    │
│         (YAML-based, extensible)             │
├─────────────────────────────────────────────┤
│           Report Generator                   │
│        (HTML / JSON / SARIF)                 │
└─────────────────────────────────────────────┘
```

## Development

```bash
# Clone and install in development mode
git clone https://github.com/arpitha-dhanapathi/pluto-aguard.git
cd pluto-aguard
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/
```

## Roadmap

- [x] **v0.1** — MCP config scanner + secret detection + OWASP MCP Top 10 rules
- [ ] **v0.2** — Runtime behavioral monitor with OpenTelemetry trace ingestion
- [ ] **v0.3** — Permission drift detection engine
- [ ] **v0.4** — What-If policy simulator with risk scoring
- [ ] **v0.5** — HTML report generator with interactive visualizations
- [ ] **v1.0** — Multi-framework support (LangChain, CrewAI, AutoGen, Foundry)

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

*Built by [Arpitha Dhanapathi](https://github.com/arpitha-dhanapathi) — PM who builds.*
