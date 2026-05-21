# 🛡️ Pluto AgentGuard

**OWASP-aligned launch gate for AI agents. Other tools scan configs — AgentGuard tests your policy against adversarial attacks, simulates risk impact, maps results to OWASP MCP Top 10, and generates launch evidence.**

[![CI](https://github.com/arpitha-dhanapathi/pluto-aguard/actions/workflows/ci.yml/badge.svg)](https://github.com/arpitha-dhanapathi/pluto-aguard/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/pluto-aguard)](https://pypi.org/project/pluto-aguard/)

## What Makes This Different

MCP security scanners are multiplying fast (Cisco, AgentShield, ship-safe, mcp-scan). **Most focus on config detection.** AgentGuard adds policy simulation, OWASP control reporting, drift detection, and launch evidence:

| Capability | Scanners | **AgentGuard** |
|---|---|---|
| Detect secrets & misconfigs | ✅ | ✅ |
| Adversarial policy simulation (17 attack scenarios) | ❌ | ✅ `aguard test` |
| "What-if" risk impact before applying changes | ❌ | ✅ `aguard whatif` |
| OWASP MCP Top 10 control coverage (20 controls) | ❌ | ✅ `aguard owasp` |
| Launch readiness evidence packets | ❌ | ✅ `aguard evidence` |
| Baseline drift detection | ❌ | ✅ `aguard baseline` |
| Behavioral trace audit with approval model | ❌ | ✅ `aguard monitor` |

## Quick Start (60 seconds)

```bash
pip install pluto-aguard

# Clone for examples
git clone https://github.com/arpitha-dhanapathi/pluto-aguard.git && cd pluto-aguard

# Scan a realistic insecure AI project — finds 18 real issues
aguard scan ./examples/demo-agent-project/

# Test your policy against 17 adversarial attacks
aguard test --policy ./examples/agent-policy.yaml --attack-pack all

# Generate OWASP MCP Top 10 coverage report
aguard owasp ./examples/demo-agent-project/

# Simulate policy changes — see risk drop before applying
aguard whatif --config ./examples/insecure-agent-config.yaml

# Generate launch readiness evidence packet
aguard evidence ./examples/ --config ./examples/insecure-agent-config.yaml \
  --policy ./examples/agent-policy.yaml

# Save baseline, detect drift later
aguard baseline create ./examples/
aguard baseline compare ./examples/
```

No cloud accounts. No API keys. Runs entirely locally.

## GitHub Action

```yaml
- name: Agent Security Gate
  uses: arpitha-dhanapathi/pluto-aguard@v0.9.0
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
| `aguard test` | Adversarial policy simulation — 17 attack scenarios across 5 packs | ✅ Stable |
| `aguard owasp` | OWASP MCP Top 10 control coverage report (20 controls) | ✅ Stable |
| `aguard whatif` | Policy impact simulation — risk delta before applying changes | ✅ Stable |
| `aguard evidence` | Launch readiness packet with approval checklist | 🔶 Beta |
| `aguard baseline` | Security snapshot + drift comparison over time | 🔶 Beta |
| `aguard monitor` | Behavioral trace audit — replays tool calls against policy | 🔶 Beta |

### `aguard scan`

Finds real issues in **any** AI project — no MCP configs needed. Detects eval/exec on LLM output, hardcoded secrets (18+ patterns), Dockerfile misconfigs, unpinned AI deps, LangChain unsafe settings, system prompt leaks, and more.

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

### `aguard test`

Simulates 17 adversarial attacks against your declared policy. Reports what gets caught vs. what gets through. Pure policy simulation — no LLM needed.

**5 attack packs:** prompt-injection, data-exfiltration, permission-escalation, approval-bypass, tool-poisoning.

```
$ aguard test --policy agent-policy.yaml --attack-pack all

  ✅ PASS  PI-001  Direct instruction override        execute       Blocked
  ✅ PASS  DE-001  File export of sensitive data      file_write    Blocked
  ❌ FAIL  DE-004  SQL data dump                      sql_query     NOT caught

  📊 Results: 16 blocked · 1 missed · 17 total

  Recommended fixes:
    → Add sql_query to require_human_approval
```

CI flag: `--fail-on-miss` exits with code 1 if any attacks succeed.

### `aguard owasp`

Evaluates 20 controls mapped to OWASP MCP Top 10 and LLM Top 10. Each control uses precise finding-ID matching.

```
$ aguard owasp ./my-project/

  ❌ MCP01:2025 Token Mismanagement: 3 failed, 1 passed
    ✗ AGC-MCP01-001: No hardcoded secrets
    ✓ AGC-MCP01-002: No static long-lived tokens
  ✅ MCP07:2025 AuthN/AuthZ: 2 passed
    ✓ AGC-MCP07-001: Remote servers have auth
    ✓ AGC-MCP07-002: HTTPS transport

  📊 OWASP MCP Mapped: 9/10 risks
     Controls: 8 passed · 6 failed · 6 not tested · 20 total
```

### `aguard whatif`

Simulates policy changes and shows risk score impact *before* applying them.

```
$ aguard whatif --config agent-config.yaml

  Current Risk Score: 100/100

  ✅ Restrict SQL to SELECT-only              → 68  (↓ 17%)
  ✅ Add human-in-the-loop for file ops       → 54  (↓ 34%)
  ✅ Add rate limits + timeout                → 48  (↓ 41%)

  💡 Apply all 3 → Risk drops to 38 (↓54%)
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

Accepts OpenTelemetry JSONL or simple `{"tool_name": "X", "tool_args": {}}` format.

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

## OWASP Control Matrix

See [docs/owasp-control-matrix.md](docs/owasp-control-matrix.md) for the complete mapping of 20 controls to OWASP MCP Top 10 and LLM Top 10.

## Roadmap

- [x] **v0.1–v0.5** — Scanner, monitor, whatif, evidence, baseline, CI gates, SARIF, HTML reports
- [x] **v0.8** — Adversarial policy simulation (17 scenarios, 5 attack packs)
- [x] **v0.9** — OWASP control framework (20 controls, coverage reports)
- [ ] **v1.0** — Multi-framework adapters (LangChain, CrewAI, AutoGen)
- [ ] **v1.1** — Live agent testing (send attacks to running agents)
- [ ] **v1.2** — Runtime proxy / tool-call firewall

## Project Structure

```
pluto-aguard/
├── src/pluto_aguard/
│   ├── cli.py                  # 7 CLI commands
│   ├── models.py               # Finding, RiskScore, ControlResult, etc.
│   ├── scanners/               # MCP + AI config + permission scanners
│   ├── testing/                # 17 adversarial attack scenarios
│   ├── controls/               # 20 OWASP-aligned control definitions
│   ├── evidence/               # Launch readiness packet generator
│   ├── baseline/               # Snapshot + drift comparison
│   ├── monitor/                # Behavioral trace audit
│   ├── simulator/              # What-If policy simulation
│   └── reports/                # HTML + SARIF output
├── examples/                   # Demo project + configs + traces
├── docs/                       # Risk scoring, OWASP matrix, GitHub Action docs
├── tests/                      # 84 tests
├── action.yml                  # GitHub Action
└── SECURITY.md
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and guidelines.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
