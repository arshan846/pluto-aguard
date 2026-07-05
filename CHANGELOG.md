# Changelog

All notable changes to Pluto AgentGuard will be documented in this file.

## [Unreleased]

## [0.9.5] — 2026-07-05

### Fixed
- **evidence/baseline/owasp**: `.aguard.yaml` and inline `# aguard-ignore` suppression, added for `scan` in 0.9.4, was never wired into these three commands — they called the scanners directly rather than through `run_scan`, so a suppressed false positive still appeared in the launch-readiness packet, still failed OWASP controls, and still showed up as drift in `baseline compare`. All three now apply the same suppression rules; `baseline` in particular now treats a newly-suppressed finding as "Resolved" on the next compare, and excludes it from a fresh snapshot.
- **whatif**: the permission risk scorer's fixed hardening-category baseline included four fields (`network.egress`, `runtime.sandbox`, `auth.token_type`, `permission_model`) that are AgentGuard's own invented policy vocabulary, not something any real config has by convention. This put an artificial ~20-30 point floor under every score regardless of how well-configured the agent actually was — the project's own best-practice `secure-agent-config.yaml` example scored 50/100. These four categories are now adoption-gated: they only count toward the score if the config actually declares that key. The same example now scores 1.5/100; a maximally locked-down single tool scores ~0.1.
- **whatif**: the adoption-gate above initially checked only whether the *parent* key (`auth`/`network`/`runtime`) was present, not the specific field each check evaluates. A config with `auth: {type: oauth2, provider: azure-ad}` — describing an auth mechanism, unrelated to token lifetime — scored 19.9 vs a 0.2 baseline (~100x) as if it had adopted-and-failed the `token_type` check. Gates now key on the specific field (`"token_type" in auth`, etc.), not the parent dict's mere presence.
- **monitor**: the approval queue's FIFO fallback could pop an *expired* approval ahead of a *valid* one sitting later in the queue, raising a false "expired approval" violation even though a usable approval was available. Non-expired approvals are now preferred; an expired one only surfaces once nothing else is usable.
- **suppressions**: the inline `# aguard-ignore: <prefix>` regex excluded `.` from the prefix character class, silently truncating any scoped suppression that included a filename (most per-instance finding IDs do, e.g. `SECRET-...-config.yaml-L12`). Dots are now allowed.
- **evidence/baseline**: neither command called `scan_ai_configs`, so Dockerfile, LangChain, and system-prompt-leak findings never appeared in a launch-readiness packet or a security baseline regardless of suppression — only `scan`/`owasp` picked those up. Both now scan the same surface.

- 174 tests passing (up from 161).

## [0.9.4] — 2026-07-05

### Fixed
- **monitor**: Read-only permission escalation check used unbounded substring matching (`"create" in "created_at"`, `"post" in "postgres"`), flagging benign SQL and connection strings as CRITICAL. Now uses word-boundary matching.
- **scan**: Bearer-token secret detection flagged any prose sentence containing the word "bearer" (e.g. "Bearer authentication is a common scheme") as a HIGH finding. Now requires length + Shannon entropy consistent with a real token.
- **whatif**: `calculate_permission_risk_score` never read `network.egress`, `runtime.sandbox`, `auth.token_type`, or `permission_model` — 4 of 7 built-in policies had zero effect on the reported score regardless of what they changed. The scorer's denominator also shrank in lockstep with the numerator when a control was fixed, so the ratio could never move once saturated at 100%. Both fixed; all 7 built-in policies now produce real, distinct deltas. Removed the `risk_reduction` fields on `BUILTIN_POLICIES`, which were never read anywhere.
- **cli**: `aguard --help` (and every command) crashed with `UnicodeEncodeError` on Windows terminals using a legacy codepage (cp1252) — this is Windows' actual default for many setups, not an edge case. Fixed by reconfiguring stdout/stderr to UTF-8 at import time (Click processes `--help`/`--version` before any command code runs).
- **monitor**: `gen_ai.*` (the real OTel GenAI semantic convention used by OpenLIT, OTel-native LangChain instrumentation, and Traceloop) was not recognized — only this project's own ad-hoc `tool.name`/`tool.args` attributes were. A genuine `gen_ai.*` trace would also have hit two more bugs: integer `startTimeUnixNano` timestamps crashed with a pydantic `ValidationError` (the model expects a string), and a trace lacking the invented `turn` field crashed the flat-format parser outright. All three fixed; `gen_ai.*` is now the primary recognized namespace, with the old names kept as fallback.
- **monitor**: approvals were keyed by tool name only, with no consumption logic — one approval event silently authorized every subsequent call to that tool for the rest of the trace, and there was no check that an approval actually preceded the action it covers (only that it appeared earlier in file order). Approvals are now a single-use, per-tool FIFO queue; an exact `call_id` match (e.g. `gen_ai.tool.call.id`) is preferred when available; and an approval timestamped after its action now raises `DRIFT-BACKDATED-APPROVAL` (CRITICAL) when both timestamps are parseable.
- **reports**: HTML and SARIF report generators hardcoded the version string and repo URL as string literals instead of reading `__version__` — every prior release had to remember to update these by hand (and several didn't). Now interpolated dynamically.
- **release**: repo URLs (README, pyproject.toml, generated reports, docs) still pointed at the pre-rename GitHub username; GitHub Action pins were two releases behind the actual PyPI version, meaning `uses: .../pluto-aguard@v0.9.2` installed a build that predates all of the above fixes.

### Added
- `.aguard.yaml` project-level ignore rules (by finding ID, ID prefix, category, or path glob) and inline `# aguard-ignore` comments for suppressing specific false positives, with `--no-suppress` to bypass. See `docs/suppressions.md`.
- `examples/claude_desktop_config.json`: a fixture built entirely from real MCP client config fields, demonstrating that `aguard scan` finds secrets/transport/auth issues but never the permission-wildcard or tool-poisoning checks on a config that doesn't declare that (non-standard) metadata itself. See `docs/config-schema.md` for what's MCP-standard vs. this project's own extended schema.
- `examples/otel-genai-traces.jsonl` and `docs/trace-ingestion.md` documenting the three trace formats `aguard monitor` accepts.
- `examples/approval-reuse-attack.jsonl` and `docs/approval-semantics.md` documenting single-use consumption, `call_id` binding, and backdated-approval detection.

### Changed
- `aguard test` reframed, in its help text and the README, as policy coverage linting (tool-name membership in `denied_tools`/`require_human_approval`) rather than adversarial testing — `attack_prompt` is documentation for a human reader and was never evaluated; two scenarios naming the same tool always got an identical verdict. No behavior changed, only how it's described.
- Deleted `rules/owasp_mcp_top10.yaml`: unreferenced anywhere in the codebase, duplicating (and drifting from) `controls/registry.py`, which is the actual runtime source of truth for OWASP control mapping.
- 161 tests passing (up from 135).

## [0.9.3] — 2026-06-17

### Fixed
- Findings re-tiered to be grounded in the MCP specification rather than an invented policy schema.
- Scan results and README claims corrected to remove inflated numbers.
- Removed accidentally committed test output.
- Version bumped to 0.9.3 (and the corresponding CLI version-flag test assertion).

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

[0.9.5]: https://github.com/arshan846/pluto-aguard/compare/v0.9.4...v0.9.5
[0.9.4]: https://github.com/arshan846/pluto-aguard/compare/v0.9.3...v0.9.4
[0.9.3]: https://github.com/arshan846/pluto-aguard/compare/v0.9.2...v0.9.3
[0.9.1]: https://github.com/arpitha-dhanapathi/pluto-aguard/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/arpitha-dhanapathi/pluto-aguard/releases/tag/v0.9.0
