# 🛡️ Pluto AgentGuard

**Your Claude Desktop / Cursor / VS Code MCP config may already let an AI agent call tools with no authentication, or ship a hardcoded API key. Check in 30 seconds.**

[![CI](https://github.com/arshan846/pluto-aguard/actions/workflows/ci.yml/badge.svg)](https://github.com/arshan846/pluto-aguard/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/pluto-aguard)](https://pypi.org/project/pluto-aguard/)

## 30-Second Scan

```bash
pip install pluto-aguard

# macOS Claude Desktop:
aguard scan ~/Library/Application\ Support/Claude/

# Windows Claude Desktop:
aguard scan %APPDATA%\Claude\

# Cursor / any project with a local mcp.json:
aguard scan .
```

Real output from scanning a realistic (but fictional) `claude_desktop_config.json` built entirely from real MCP fields — no invented schema, see [examples/claude_desktop_config.json](examples/claude_desktop_config.json):

```
🔍 Scanning ...

  🟠 HIGH: Hardcoded secret in env var 'GITHUB_PERSONAL_ACCESS_TOKEN' on server 'github' (MCP01:2025)
  🟠 HIGH: Insecure HTTP transport on MCP server 'internal-metrics' (MCP07:2025)
  🟠 HIGH: No authentication configured for remote MCP server 'internal-metrics' (MCP07:2025)
  🟠 HIGH: Hardcoded GitHub Token detected (MCP01:2025)

  📊 Risk Score: 44.8/100 ██████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  📋 Findings: 4 high
```

No cloud accounts, no API keys, nothing leaves your machine — it's static analysis of the config file, not a live connection to your MCP servers. False positive? See [docs/suppressions.md](docs/suppressions.md).

## There's More Than a Scanner

Once you've found a problem, the harder question is "did my fix actually help, and can I prove it to whoever signs off on shipping this agent?" That's what the rest of AgentGuard is for — the two commands below are the part no other MCP scanner does:

```bash
git clone https://github.com/arshan846/pluto-aguard.git && cd pluto-aguard

# See the risk score drop *before* you apply a fix
aguard whatif --config ./examples/insecure-agent-config.yaml

# Generate a launch-approval packet: findings + policy coverage + sign-off checklist
aguard evidence ./examples/ --config ./examples/insecure-agent-config.yaml \
  --policy ./examples/agent-policy.yaml
```

Plus policy coverage linting (`test`), an OWASP-inspired control report (`owasp`), and drift detection (`baseline`) — see [Commands](#commands) below, or the [interactive demo](docs/demo.html) for all 7 in action.

| Capability | Scanners | **AgentGuard** |
|---|---|---|
| Detect secrets & misconfigs statically (no server execution) | 🟡 Varies | ✅ `aguard scan` |
| Policy coverage linting (22 named attack scenarios) | ❌ | ✅ `aguard test` |
| "What-if" risk impact before applying changes | ❌ | ✅ `aguard whatif` |
| OWASP-inspired control coverage (20 controls) | ❌ | ✅ `aguard owasp` |
| Launch readiness evidence packets | ❌ | ✅ `aguard evidence` |
| Baseline drift detection | ❌ | ✅ `aguard baseline` |
| Behavioral trace audit with approval model | ❌ | ✅ `aguard monitor` |

MCP security scanners are multiplying fast (Snyk agent-scan, Invariant guardrails, AgentSeal) and mostly stop at config detection or runtime analysis. AgentGuard's differentiator is the pair above — quantified risk delta before you change anything, and a packet to hand whoever approves the launch — not the scanning itself, which is table stakes.

## Real-World Validation: 1,200 GitHub Configs

We scanned **1,200 real MCP configs** from public GitHub repos (1,159 unique projects) using AgentGuard:

| Metric | Result |
|---|---|
| Configs scanned | 1,200 |
| Total findings | 2,891 |
| 🔴 CRITICAL | 0 |
| 🟠 HIGH | 189 |
| 🟡 MEDIUM | 169 |
| ℹ️ INFO | 2,533 |
| Repos with HIGH findings | **156 (13%)** |

**What we actually found:**
- 189 remote MCP endpoints with no authentication configured
- 169 unencrypted HTTP on non-localhost transport
- Hardcoded secrets in a subset of configs
- 2,533 informational items (capability inventory — shell access, browser automation, etc.)

**Important context:** Capability-related findings (e.g., a server having shell tools) are reported as INFO for awareness only. Per the [MCP specification](https://modelcontextprotocol.io/specification/2025-03-26/architecture), human-in-the-loop enforcement is strictly a client/host responsibility, not the server's. See [full methodology and results](docs/scan-results-methodology.md).

## GitHub Action

```yaml
- name: Agent Security Gate
  uses: arshan846/pluto-aguard@v0.9.5
  with:
    path: '.'
    max-risk: '50'
    fail-on: 'high'
    policy: 'agent-policy.yaml'
    attack-pack: 'all'
    sarif-output: 'results.sarif'

- uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif
```

See [docs/github-action-usage.md](docs/github-action-usage.md) for full options.

---

## Commands

| Command | What It Does | Maturity |
|---|---|---|
| `aguard scan` | Static analysis — secrets, misconfigs, unsafe AI code patterns | ✅ Stable |
| `aguard test` | Policy coverage linting — 22 named attack scenarios across 6 packs | ✅ Stable |
| `aguard owasp` | OWASP-inspired control coverage report (20 controls) | ✅ Stable |
| `aguard whatif` | Policy impact simulation — risk delta before applying changes | ✅ Stable |
| `aguard evidence` | Launch readiness packet with approval checklist | 🔶 Beta |
| `aguard baseline` | Security snapshot + drift comparison over time | 🔶 Beta |
| `aguard monitor` | Behavioral trace audit — replays tool calls against policy | 🔶 Beta |

### `aguard scan`

Finds real issues in **any** AI project — no MCP configs needed. Detects eval/exec on LLM output, hardcoded secrets (18+ patterns), missing authentication on remote endpoints, Dockerfile misconfigs, unpinned AI deps, LangChain unsafe settings, system prompt leaks, and more.

```
$ aguard scan ./my-project/

  🔴 CRITICAL: Unsafe execution of LLM output: eval() (MCP05:2025)
  🟠 HIGH: Hardcoded OpenAI Key detected (MCP01:2025)
  🟠 HIGH: .env file not in .gitignore (MCP01:2025)
  🟡 MEDIUM: Unpinned AI dependencies (MCP04:2025)

  📊 Risk Score: 100/100 ██████████████████████████████████████████████████
  📋 Findings: 1 critical · 14 high · 3 medium
```

CI flags: `--max-risk 50` / `--fail-on high` / `--format sarif`

False positive? Suppress it via a `.aguard.yaml` file or an inline `# aguard-ignore` comment — see [docs/suppressions.md](docs/suppressions.md). Use `--no-suppress` to see every finding regardless of suppression rules.

Not every check applies to every config: transport/auth/secrets checks work on any real `claude_desktop_config.json`, but the permission-wildcard and tool-poisoning checks look for metadata (`permissions`, `tools[].description`) that only exists in AgentGuard's own extended schema or in gateway configs that add it themselves — see [docs/config-schema.md](docs/config-schema.md) for exactly what's standard vs. extended, and [examples/claude_desktop_config.json](examples/claude_desktop_config.json) for a scan of a real, unmodified config.

### `aguard test`

Policy coverage linting, not adversarial testing: for each of 22 named attack scenarios, checks whether the tool it would invoke is in your policy's `denied_tools` or `require_human_approval` list. Reports what gets caught vs. what gets through. No LLM needed — nothing is executed and no prompt text is evaluated. A scenario's `attack_prompt` is documentation of the threat it represents, not an input this command interprets; two scenarios that name the same tool (e.g. `execute`) get the identical verdict regardless of how different the underlying attack is.

> ⚠️ **This tests whether your *policy document* would block each attack — not whether your actual LLM agent would resist it.** Real agent resistance requires runtime testing against a live agent (planned for v1.2).

**6 attack packs:** prompt-injection, data-exfiltration, permission-escalation, approval-bypass, tool-poisoning, context-manipulation.

```
$ aguard test --policy agent-policy.yaml --attack-pack all

  ✅ PASS  PI-001  Direct instruction override        execute       Blocked
  ✅ PASS  DE-001  File export of sensitive data      file_write    Blocked
  ❌ FAIL  DE-004  SQL data dump                      sql_query     NOT caught

  📊 Results: 21 blocked · 1 missed · 22 total

  Recommended fixes:
    → Add sql_query to require_human_approval
```

CI flag: `--fail-on-miss` exits with code 1 if any attacks succeed.

### `aguard owasp`

Evaluates 20 controls mapped to an OWASP-inspired control framework. Control IDs use a project-defined `MCP01–MCP10` taxonomy that draws on OWASP LLM Top 10 and the emerging OWASP Agentic AI initiative, with MCP-specific extensions the existing standards don't yet cover.

```
$ aguard owasp ./my-project/

  ❌ MCP01:2025 Token Mismanagement: 3 failed, 1 passed
    ✗ AGC-MCP01-001: No hardcoded secrets
    ✓ AGC-MCP01-002: No static long-lived tokens
  ✅ MCP07:2025 AuthN/AuthZ: 2 passed
    ✓ AGC-MCP07-001: Remote servers have auth
    ✓ AGC-MCP07-002: HTTPS transport

  📊 Control Coverage: 9/10 risks
     Controls: 8 passed · 6 failed · 6 not tested · 20 total
```

### `aguard whatif`

Simulates policy changes and shows risk score impact *before* applying them. Output below is the real, reproducible result of running `aguard whatif --config examples/insecure-agent-config.yaml`:

```
$ aguard whatif --config examples/insecure-agent-config.yaml

  Current Risk Score: 100/100

  ✅ Restrict SQL tool to SELECT-only queries               → 56  (↓ 44%)
  ✅ Add human-in-the-loop for file operations              → 97  (↓ 3%)
  ✅ Rotate API keys to ephemeral tokens                    → 82  (↓ 18%)
  ✅ Add rate limits (100 calls/minute) and timeout (5 min) → 57  (↓ 43%)
  ✅ Restrict outbound network access to allowlisted domains → 82  (↓ 18%)
  ✅ Convert from implicit-allow to explicit tool allowlist → 82  (↓ 18%)
  ✅ Run agent in sandboxed execution environment           → 82  (↓ 18%)

  💡 Apply all 7 → Risk drops to 5 (↓95%)
```

### `aguard evidence`

Generates a launch readiness packet — risk summary, findings, tool permissions, policy coverage, required mitigations, and sign-off checklist. See [examples/sample-launch-readiness.md](examples/sample-launch-readiness.md).

### `aguard baseline`

Save a security snapshot, compare later to detect drift.

```bash
aguard baseline create .               # Save current state
aguard baseline compare .              # What changed?
aguard baseline compare . --fail-on-drift  # CI: fail if new findings
```

### `aguard monitor`

Replays agent action traces against a declared policy. Detects denied tool calls, unauthorized access, permission escalation, and missing/expired approvals.

```bash
aguard monitor --trace-file traces.jsonl --policy policy.yaml
```

Accepts real OTel GenAI semantic-convention traces (`gen_ai.tool.name`, `gen_ai.operation.name` — what OpenLIT and OTel-native LangChain instrumentation actually emit), this project's own OTel-shaped format, or a flat simple `{"tool_name": "X", "tool_args": {}}` format. See [docs/trace-ingestion.md](docs/trace-ingestion.md) and [examples/otel-genai-traces.jsonl](examples/otel-genai-traces.jsonl).

Approvals are single-use — one approval authorizes exactly one matching call, not every future call to that tool — and, when both sides carry a timestamp, an approval recorded after the action it's supposed to cover is flagged as a `DRIFT-BACKDATED-APPROVAL`. See [docs/approval-semantics.md](docs/approval-semantics.md).

---

## How It Fits

```
┌─────────────────────────────────────────────────────┐
│  LAYER 1: Content Guardrails (existing)             │
│  Azure Content Safety · NeMo · Guardrails AI        │
│  → Protects what LLMs SAY                           │
├─────────────────────────────────────────────────────┤
│  LAYER 2: Agent Security (Pluto AgentGuard)         │
│  scan · test · owasp · whatif · evidence · baseline  │
│  → Watches what agents DO                           │
└─────────────────────────────────────────────────────┘
```

## Risk Scoring

See [docs/risk-scoring.md](docs/risk-scoring.md) for the full scoring methodology — formula, weights, examples, CI threshold guidance, and limitations.

## OWASP-Inspired Control Matrix

See [docs/owasp-control-matrix.md](docs/owasp-control-matrix.md) for the complete mapping of 20 controls. Control IDs draw on OWASP LLM Top 10 (LLM01–LLM10) and introduce MCP-specific extensions (MCP01–MCP10) for risks the existing standards don't yet cover.

## Roadmap

- [x] **v0.1–v0.5** — Scanner, monitor, whatif, evidence, baseline, CI gates, SARIF, HTML reports
- [x] **v0.8** — Policy coverage testing (17 scenarios, 5 attack packs)
- [x] **v0.9** — OWASP-inspired control framework (20 controls, coverage reports)
- [x] **v0.9.1** — Context manipulation pack (context stuffing, multi-turn confusion, indirect injection, RAG poisoning), supply-chain manifest poisoning scenario
- [ ] **v1.0** — Runtime proxy / tool-call firewall (observability on live tool calls without full red-team harness)
- [ ] **v1.1** — Multi-framework adapters (LangChain, CrewAI, AutoGen). `aguard monitor` already ingests real OTel GenAI semantic-convention traces (see [docs/trace-ingestion.md](docs/trace-ingestion.md)) — a framework-specific setup adapter is what remains.
- [ ] **v1.2** — Live agent testing (send adversarial inputs to running agents)

## Project Structure

```
pluto-aguard/
├── src/pluto_aguard/
│   ├── cli.py                  # 7 CLI commands
│   ├── models.py               # Finding, RiskScore, ControlResult, etc.
│   ├── scanners/               # MCP + AI config + permission scanners
│   ├── testing/                # 22 attack scenarios across 6 packs
│   ├── controls/               # 20 OWASP-aligned control definitions
│   ├── evidence/               # Launch readiness packet generator
│   ├── baseline/               # Snapshot + drift comparison
│   ├── monitor/                # Behavioral trace audit
│   ├── simulator/              # What-If policy simulation
│   ├── suppressions.py         # .aguard.yaml + inline finding suppression
│   └── reports/                # HTML + SARIF output
├── examples/                   # Demo project + configs + traces
├── docs/                       # Risk scoring, OWASP matrix, suppressions, GitHub Action docs
├── tests/                      # 174 tests
├── action.yml                  # GitHub Action
└── SECURITY.md
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and guidelines.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
