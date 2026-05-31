# Changelog

All notable changes to Pluto AgentGuard will be documented in this file.

## [0.9.2] — 2026-05-31

### Fixed
- **action.yml**: Version pin updated from 0.9.0 → 0.9.2 (was installing wrong version)
- **action.yml**: Description and input labels updated to use "OWASP-inspired" and "policy coverage testing" language
- **action.yml**: Added `context-manipulation` to attack pack list
- **README.md**: Replaced non-existent competitor names (AgentShield, ship-safe) with verified projects (Invariant guardrails, AgentSeal)
- **CHANGELOG.md**: Corrected test count (87 → 95), updated terminology
- **pyproject.toml**: Updated description for PyPI page accuracy

### Added
- **GitHub topics**: mcp, ai-security, mcp-security, agent-security, owasp, llm-security, mcp-server, claude, cursor

## [0.9.1] — 2026-05-30

### Added

**New Attack Scenarios (5 new → 22 total across 6 packs)**
- `CM-001` — Context window stuffing: oversized payloads to overflow agent context
- `CM-002` — Multi-turn state confusion: exploiting conversation history for escalation
- `CM-003` — Indirect injection via web fetch: poisoned external content injected into context
- `CM-004` — RAG context poisoning: malicious content planted in retrieval pipelines
- `TP-003` — Malicious manifest packages: supply chain attacks via MCP server metadata
- New `context-manipulation` attack pack (6th pack)

**Scanner Enhancements**
- Dangerous MCP package detection — flags `filesystem`, `postgres`, `sqlite`, `playwright` servers without human-in-the-loop approval
- Env var secret detection — 10+ patterns with multi-language placeholder filtering (English, Portuguese, Spanish, Arabic)
- Connection string credential detection — `postgres://`, `mongodb://`, `mysql://` in args and env vars
- Content-aware config detection — catches renamed/prefixed MCP config files (not just exact filenames)
- Custom dangerous server name detection — `powershell-commander`, `file-commander`, etc.

**Context Safety Heuristics (bridge until runtime proxy)**
- External content fetch detection — flags web fetch, playwright, RAG, search, crawl servers
- Missing response size limits warning — context stuffing risk
- Missing session/turn limits warning — multi-turn confusion risk

### Changed
- Roadmap reprioritized based on community feedback:
  - v1.0 → Runtime MCP proxy (was adapters)
  - v1.1 → Framework adapters (was proxy)
  - v1.2 → Live policy testing with runtime probes
- OWASP control matrix updated for MCP03, MCP04, MCP06 coverage
- README updated: 22 scenarios, 6 attack packs

### Validated
- Scanned 30 real `claude_desktop_config.json` files from public GitHub repos
- Before v0.9.1: 2 findings
- After v0.9.1: 79 findings (1 critical, 15 high, 63 medium)
- 27% of configs have HIGH+ findings; 100% have at least one finding
- 95 tests passing

## [0.9.0] — 2026-05-21

### Added
- `aguard scan` — Static security scanner for MCP configs, secrets, Dockerfiles, dependencies
- `aguard monitor` — Behavioral trace replay with policy violation detection
- `aguard whatif` — Policy change impact simulator with risk score delta
- `aguard test` — Policy coverage testing with 17 attack scenarios across 5 packs
- `aguard owasp` — OWASP MCP Top 10 + LLM Top 10 control coverage reports
- `aguard evidence` — Launch readiness packet generation with approval checklists
- `aguard baseline` — Security baseline snapshots and drift detection
- SARIF output format for CI integration
- `--fail-on` and `--max-risk` CI gate flags
- GitHub Action for automated scanning
- OWASP control registry with 20 controls mapped
- Apache-2.0 license

[0.9.1]: https://github.com/arpitha-dhanapathi/pluto-aguard/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/arpitha-dhanapathi/pluto-aguard/releases/tag/v0.9.0
