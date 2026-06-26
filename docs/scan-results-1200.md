# Pluto AgentGuard — 1,200 GitHub MCP Config Scan Results

> Generated: 2026-06-25 | Scanner: pluto-aguard v0.9.2
> Previous scan: 2026-06-01 | This report is LOCAL ONLY — not committed to git.

## Summary

- **Configs scanned**: 1200
- **Total findings**: 2904
- **CRITICAL**: 88
- **HIGH**: 280
- **MEDIUM**: 2536
- **Configs with CRITICAL max**: 75
- **Configs with HIGH max**: 173
- **Configs with MEDIUM max**: 952
- **% with CRITICAL or HIGH**: 20.7%

## Findings by Category

| Category | Count |
|---|---|
| context_safety | 2535 |
| permissions | 145 |
| secrets | 121 |
| authentication | 74 |
| transport | 29 |

## Top 30 Rules Triggered

| # | Rule | Count | Severity |
|---|---|---|---|
| 1 | `CONTEXT-NO-RESPONSE-LIMIT` | 1200 | MEDIUM |
| 2 | `CONTEXT-NO-SESSION-LIMIT` | 1191 | MEDIUM |
| 3 | `DANGEROUS-PKG-filesystem-filesystem` | 63 | HIGH |
| 4 | `DANGEROUS-PKG-playwright-browser-automation` | 31 | HIGH |
| 5 | `CONTEXT-INJECT-context7` | 16 | MEDIUM |
| 6 | `CONTEXT-EXT-FETCH-fetch` | 14 | MEDIUM |
| 7 | `CONTEXT-EXT-FETCH-puppeteer` | 14 | MEDIUM |
| 8 | `CONTEXT-EXT-FETCH-brave-search` | 10 | MEDIUM |
| 9 | `DANGEROUS-POPULAR-serena-shell-execution` | 9 | CRITICAL |
| 10 | `CONTEXT-EXT-FETCH-playwright` | 9 | MEDIUM |
| 11 | `DANGEROUS-PKG-postgres-database` | 8 | HIGH |
| 12 | `ENV-SECRET-supabase-SUPABASE_ACCESS_TOKEN` | 5 | HIGH |
| 13 | `CONTEXT-EXT-FETCH-firecrawl` | 4 | MEDIUM |
| 14 | `DANGEROUS-PKG-sqlite-database` | 3 | HIGH |
| 15 | `DANGEROUS-PKG-chrome-devtools-browser-control` | 3 | CRITICAL |
| 16 | `CONTEXT-EXT-FETCH-crawl4ai` | 3 | MEDIUM |
| 17 | `DANGEROUS-PKG-github-source-control` | 3 | HIGH |
| 18 | `CONTEXT-INJECT-Context7` | 3 | MEDIUM |
| 19 | `ENV-SECRET-agent-kit-OPENAI_API_KEY` | 3 | HIGH |
| 20 | `CONTEXT-EXT-FETCH-tavily` | 2 | MEDIUM |
| 21 | `CONTEXT-EXT-FETCH-puppeteer-hisma` | 2 | MEDIUM |
| 22 | `DANGEROUS-PKG-n8n-workflow-execution` | 2 | HIGH |
| 23 | `CONTEXT-EXT-FETCH-firecrawl-mcp` | 2 | MEDIUM |
| 24 | `AUTH-MISSING-Figma` | 2 | CRITICAL |
| 25 | `AUTH-MISSING-supabase` | 2 | CRITICAL |
| 26 | `CONN-STRING-ARGS-postgres` | 2 | HIGH |
| 27 | `CONN-STRING-ENV-postgres-POSTGRES_CONNECTION_STRING` | 2 | HIGH |
| 28 | `ENV-SECRET-github-GITHUB_PERSONAL_ACCESS_TOKEN` | 2 | HIGH |
| 29 | `CONTEXT-EXT-FETCH-filesystem` | 2 | MEDIUM |
| 30 | `ENV-SECRET-TestSprite-API_KEY` | 2 | HIGH |

---

## Detailed Results by Config

### Legend
- **Max Sev**: Highest severity finding in the config
- **Risk**: Risk score (0-100, capped)
- **C/H/M**: Count of Critical / High / Medium findings
- **Servers**: Number of MCP servers configured (with names)
- **Notable Findings**: Non-trivial findings (excludes ubiquitous context-limit rules)

### CRITICAL Configs (75)

| # | Repo | Config Path | Servers | C | H | M | Risk | Notable Findings |
|---|---|---|---|---|---|---|---|---|
| 1 | [alpsla/codequal](https://github.com/alpsla/codequal) | `.claude/claude_desktop_config.json` | 4 (ref, semgrep, serena +1 more) | 1 | 3 | 3 | 100 | HIGH: `ENV-SECRET-ref-REF_API_KEY`; HIGH: `ENV-SECRET-semgrep-SEMGREP_APP_TOKEN`; CRITICAL: `DANGEROUS-POPULAR-serena-shell-execution`; HIGH: `ENV-SECRET-tavily-TAVILY_API_KEY`; MEDIUM: `CONTEXT-EXT-FETCH-tavily` |
| 2 | [AIUELAB/001-final-hourglass](https://github.com/AIUELAB/001-final-hourglass) | `mcp-config/claude_desktop_config.json` | 32 (serena, filesystem, github +29 more) | 1 | 3 | 7 | 100 | CRITICAL: `DANGEROUS-POPULAR-serena-shell-execution`; HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-fetch`; MEDIUM: `CONTEXT-EXT-FETCH-brave-search`; HIGH: `DANGEROUS-PKG-playwright-browser-automation` (+4 more) |
| 3 | [AIUELAB/docker-claude-code-template](https://github.com/AIUELAB/docker-claude-code-template) | `mcp-config/claude_desktop_config.json` | 60 (serena, augments, sequential-thinking +57 more) | 3 | 5 | 7 | 100 | CRITICAL: `DANGEROUS-POPULAR-serena-shell-execution`; CRITICAL: `DANGEROUS-POPULAR-serena-local-shell-execution`; CRITICAL: `DANGEROUS-POPULAR-serena-docker-shell-execution`; HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-fetch` (+8 more) |
| 4 | [sumik5/dotfiles](https://github.com/sumik5/dotfiles) | `claude-code-desktop/claude_desktop_config.json` | 20 (context7, serena, playwright +17 more) | 2 | 2 | 5 | 100 | MEDIUM: `CONTEXT-INJECT-context7`; CRITICAL: `DANGEROUS-POPULAR-serena-shell-execution`; HIGH: `DANGEROUS-PKG-playwright-browser-automation`; CRITICAL: `DANGEROUS-PKG-chrome-devtools-browser-control`; MEDIUM: `CONTEXT-EXT-FETCH-puppeteer` (+2 more) |
| 5 | [cleerox-svg/trust-radar](https://github.com/cleerox-svg/trust-radar) | `.mcp.json` | 5 (averrow, playwright, chrome-devtools +2 more) | 3 | 2 | 3 | 100 | CRITICAL: `AUTH-MISSING-averrow`; HIGH: `DANGEROUS-PKG-playwright-browser-automation`; MEDIUM: `CONTEXT-EXT-FETCH-playwright`; CRITICAL: `DANGEROUS-PKG-chrome-devtools-browser-control`; HIGH: `TRANSPORT-HTTP-figma-dev-mode` (+1 more) |
| 6 | [Elogic360/software-factory](https://github.com/Elogic360/software-factory) | `integrations/claude-skills-secondsky/plugins/cloudflare-mcp-server/skills/cloudflare-mcp-server/templates/claude_desktop_config.json` | 3 (my-mcp-server-local, my-mcp-server-remote, my-mcp-oauth-server) | 2 | 1 | 2 | 75 | HIGH: `TRANSPORT-HTTP-my-mcp-server-local`; CRITICAL: `AUTH-MISSING-my-mcp-server-local`; CRITICAL: `AUTH-MISSING-my-mcp-server-remote` |
| 7 | [TeamSparkAI/mcp-inspect](https://github.com/TeamSparkAI/mcp-inspect) | `mcp.json` | 3 (fetch, filesystem, everything) | 1 | 2 | 3 | 75 | MEDIUM: `CONTEXT-EXT-FETCH-fetch`; HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `TRANSPORT-HTTP-everything`; CRITICAL: `AUTH-MISSING-everything` |
| 8 | [narrative-io/narrative-skills-marketplace](https://github.com/narrative-io/narrative-skills-marketplace) | `plugins/narrative-common/.claude-plugin/plugin.json` | 3 (narrative-mcp, narrative-knowledge-base, narrative-agent-gateway) | 3 | 0 | 3 | 75 | CRITICAL: `AUTH-MISSING-narrative-mcp`; CRITICAL: `AUTH-MISSING-narrative-knowledge-base`; MEDIUM: `CONTEXT-EXT-FETCH-narrative-knowledge-base`; CRITICAL: `AUTH-MISSING-narrative-agent-gateway` |
| 9 | [kriskimmerle/mcplint](https://github.com/kriskimmerle/mcplint) | `examples/insecure.json` | 12 (filesystem-full, shell-exec, github-leaky +9 more) | 1 | 2 | 2 | 75 | HIGH: `DANGEROUS-PKG-filesystem-full-filesystem`; HIGH: `TRANSPORT-HTTP-http-no-auth`; CRITICAL: `AUTH-MISSING-http-no-auth` |
| 10 | [alex1976/EntangoApiMinimal](https://github.com/alex1976/EntangoApiMinimal) | `McpServer/claude_desktop_config.json` | 3 (pricelist-local, pricelist-http, pricelist-https) | 2 | 1 | 2 | 75 | HIGH: `TRANSPORT-HTTP-pricelist-http`; CRITICAL: `AUTH-MISSING-pricelist-http`; CRITICAL: `AUTH-MISSING-pricelist-https` |
| 11 | [AlperAykac2015/MCP-Servers](https://github.com/AlperAykac2015/MCP-Servers) | `nasa_news_files/claude_desktop_config.json` | 4 (maven, nasa-apod, nasa-apod-tr-port +1 more) | 2 | 1 | 2 | 75 | HIGH: `TRANSPORT-HTTP-nasa-apod-tr-port`; CRITICAL: `AUTH-MISSING-nasa-apod-tr-port`; CRITICAL: `AUTH-MISSING-neows-remote` |
| 12 | [shengjun89/card-generating-animation](https://github.com/shengjun89/card-generating-animation) | `mcp.json` | 2 (Figma, Zapier) | 2 | 1 | 2 | 75 | HIGH: `TRANSPORT-HTTP-Figma`; CRITICAL: `AUTH-MISSING-Figma`; CRITICAL: `AUTH-MISSING-Zapier` |
| 13 | [prakashwagle/mcp-whatsapp-business-api](https://github.com/prakashwagle/mcp-whatsapp-business-api) | `claude_desktop_config.json` | 1 (whatsapp-business) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-whatsapp-business`; CRITICAL: `AUTH-MISSING-whatsapp-business` |
| 14 | [Eleutherios-project/Eleutherios-docker](https://github.com/Eleutherios-project/Eleutherios-docker) | `examples/claude_desktop_config.json` | 1 (aegis-insight) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-aegis-insight`; CRITICAL: `AUTH-MISSING-aegis-insight` |
| 15 | [HeyGarrison/cf-mcp](https://github.com/HeyGarrison/cf-mcp) | `claude_desktop_config.json` | 1 (cf-mcp) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-cf-mcp`; CRITICAL: `AUTH-MISSING-cf-mcp` |
| 16 | [shanekid72/TisAI](https://github.com/shanekid72/TisAI) | `MCP.json` | 1 (worldAPI) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-worldAPI`; CRITICAL: `AUTH-MISSING-worldAPI` |
| 17 | [go-training/mcp-workshop](https://github.com/go-training/mcp-workshop) | `mcp.json` | 2 (default-stdio-server, default-http-server) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-default-http-server`; CRITICAL: `AUTH-MISSING-default-http-server` |
| 18 | [niklashellberg/umlDesigner](https://github.com/niklashellberg/umlDesigner) | `.mcp.json` | 1 (uml-designer) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-uml-designer`; CRITICAL: `AUTH-MISSING-uml-designer` |
| 19 | [bolovemei99-code/my-robot](https://github.com/bolovemei99-code/my-robot) | `mcp.json` | 3 (local-llm, grok-api, openai-proxy) | 2 | 0 | 2 | 50 | CRITICAL: `AUTH-MISSING-grok-api`; CRITICAL: `AUTH-MISSING-openai-proxy` |
| 20 | [danilomartinelli/cursor-kit](https://github.com/danilomartinelli/cursor-kit) | `mcp.json` | 9 (context7, sequential-thinking, memory +6 more) | 1 | 1 | 4 | 50 | MEDIUM: `CONTEXT-INJECT-context7`; HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-firecrawl`; CRITICAL: `AUTH-MISSING-figma` |
| 21 | [launchdarkly/launchdarkly-kiro-power](https://github.com/launchdarkly/launchdarkly-kiro-power) | `mcp.json` | 2 (LaunchDarkly Feature Management, LaunchDarkly AI Configs) | 2 | 0 | 2 | 50 | CRITICAL: `AUTH-MISSING-LaunchDarkly Feature Management`; CRITICAL: `AUTH-MISSING-LaunchDarkly AI Configs` |
| 22 | [namuan/openrouter-proxy-ui](https://github.com/namuan/openrouter-proxy-ui) | `.roo/mcp.json` | 1 (trello-task-manager) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-trello-task-manager`; CRITICAL: `AUTH-MISSING-trello-task-manager` |
| 23 | [sibyllinesoft/hydra](https://github.com/sibyllinesoft/hydra) | `mcp-servers.json` | 7 (git, serena, sequential-thinking +4 more) | 1 | 1 | 3 | 50 | CRITICAL: `DANGEROUS-POPULAR-serena-shell-execution`; HIGH: `DANGEROUS-PKG-playwright-browser-automation`; MEDIUM: `CONTEXT-EXT-FETCH-playwright` |
| 24 | [vampire1337/memory_engine](https://github.com/vampire1337/memory_engine) | `claude_desktop_config.json` | 1 (fastapi-mem0-memory) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-fastapi-mem0-memory`; CRITICAL: `AUTH-MISSING-fastapi-mem0-memory` |
| 25 | [himihiromu/python_useful_function](https://github.com/himihiromu/python_useful_function) | `.devcontainer/claude_desktop_config.json` | 3 (playwright, fetch, serena) | 1 | 1 | 3 | 50 | HIGH: `DANGEROUS-PKG-playwright-browser-automation`; MEDIUM: `CONTEXT-EXT-FETCH-fetch`; CRITICAL: `DANGEROUS-POPULAR-serena-shell-execution` |
| 26 | [qualitymaterial/Stratum-Sports](https://github.com/qualitymaterial/Stratum-Sports) | `mcp/claude_desktop_config.json` | 1 (stratum-sports) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-stratum-sports`; CRITICAL: `AUTH-MISSING-stratum-sports` |
| 27 | [qlawmarq/dotfiles-macos](https://github.com/qlawmarq/dotfiles-macos) | `modules/claude/claude_desktop_config.json` | 3 (context7, chrome-devtools, playwright) | 1 | 1 | 3 | 50 | MEDIUM: `CONTEXT-INJECT-context7`; CRITICAL: `DANGEROUS-PKG-chrome-devtools-browser-control`; HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 28 | [amornpan/2025-langflow-mcp-main](https://github.com/amornpan/2025-langflow-mcp-main) | `sse-mcp-loan-hr-customerservice-safety/pyrag-sse/claude_desktop_config.json` | 1 (pyragdoc-sse) | 1 | 1 | 3 | 50 | HIGH: `TRANSPORT-HTTP-pyragdoc-sse`; CRITICAL: `AUTH-MISSING-pyragdoc-sse`; MEDIUM: `CONTEXT-EXT-FETCH-pyragdoc-sse` |
| 29 | [valeriofantozzi/homework-AIFileSystem](https://github.com/valeriofantozzi/homework-AIFileSystem) | `server/config/claude_desktop_config.json` | 1 (ai-filesystem) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-ai-filesystem`; CRITICAL: `AUTH-MISSING-ai-filesystem` |
| 30 | [ZhaoLLe/mcp-bridge](https://github.com/ZhaoLLe/mcp-bridge) | `claude_desktop_config.json` | 1 (mcp-bridge) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-mcp-bridge`; CRITICAL: `AUTH-MISSING-mcp-bridge` |
| 31 | [joemunene-by/ghostloop](https://github.com/joemunene-by/ghostloop) | `examples/claude_desktop_config.json` | 6 (ghostloop-mock, ghostloop-mujoco, ghostloop-real-arm +3 more) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-ghostloop-remote-http`; CRITICAL: `AUTH-MISSING-ghostloop-remote-http` |
| 32 | [MuftahFree/Agencybazar](https://github.com/MuftahFree/Agencybazar) | `docs/integration/claude_desktop_config.json` | 1 (agencybazar) | 1 | 1 | 1 | 50 | HIGH: `TRANSPORT-HTTP-agencybazar`; CRITICAL: `AUTH-MISSING-agencybazar` |
| 33 | [VibeCoding6-JC/TestMCP](https://github.com/VibeCoding6-JC/TestMCP) | `client/claude_desktop_config.json` | 1 (simple-mcp-server) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-simple-mcp-server`; CRITICAL: `AUTH-MISSING-simple-mcp-server` |
| 34 | [ChaoYue0307/mcp-guard](https://github.com/ChaoYue0307/mcp-guard) | `examples/unsafe-claude_desktop_config.json` | 4 (filesystem-all-home, shell-installer, docker-host-control +1 more) | 1 | 1 | 2 | 50 | HIGH: `DANGEROUS-PKG-filesystem-all-home-filesystem`; CRITICAL: `AUTH-MISSING-remote-prod` |
| 35 | [GRChetanReddy/mcp](https://github.com/GRChetanReddy/mcp) | `claude_desktop_config.json` | 3 (internal-data, internal-data-stdio, internal-data-http) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-internal-data-http`; CRITICAL: `AUTH-MISSING-internal-data-http` |
| 36 | [Imsharad/gmail-mcp-server](https://github.com/Imsharad/gmail-mcp-server) | `claude_desktop_config.json` | 1 (gmail) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-gmail`; CRITICAL: `AUTH-MISSING-gmail` |
| 37 | [Userology-Inc/userology-mcp-server](https://github.com/Userology-Inc/userology-mcp-server) | `claude_desktop_config.json` | 1 (userology) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-userology`; CRITICAL: `AUTH-MISSING-userology` |
| 38 | [Ilenburg1993/chatgpt-docker-puppeteer](https://github.com/Ilenburg1993/chatgpt-docker-puppeteer) | `docs/integration/examples/claude_desktop_config.json` | 1 (chatgpt-docker) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-chatgpt-docker`; CRITICAL: `AUTH-MISSING-chatgpt-docker` |
| 39 | [NineWorlds/serenity-android](https://github.com/NineWorlds/serenity-android) | `mcp.json` | 1 (android_studio_mcp) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-android_studio_mcp`; CRITICAL: `AUTH-MISSING-android_studio_mcp` |
| 40 | [magnushammar/ch-fsharp](https://github.com/magnushammar/ch-fsharp) | `.mcp.json` | 1 (doc-searcher) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-doc-searcher`; CRITICAL: `AUTH-MISSING-doc-searcher` |
| 41 | [seer-engg/seer](https://github.com/seer-engg/seer) | `.mcp.json` | 4 (seer, langfuse, metabase-mcp +1 more) | 1 | 1 | 2 | 50 | HIGH: `TRANSPORT-HTTP-playwright`; CRITICAL: `AUTH-MISSING-playwright` |
| 42 | [rodobedrossian/product-pulse](https://github.com/rodobedrossian/product-pulse) | `mcp/claude_desktop_config.json.example` | 2 (product-pulse-local, product-pulse) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-product-pulse` |
| 43 | [zenkogg/zenko-whitelist](https://github.com/zenkogg/zenko-whitelist) | `.claude/claude_desktop_config.json` | 1 (Figma) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-Figma` |
| 44 | [virtualsms-io/mcp-server](https://github.com/virtualsms-io/mcp-server) | `examples/03-claude-desktop-config/claude_desktop_config.json` | 1 (virtualsms) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-virtualsms` |
| 45 | [vapagentmedia/vap-showcase](https://github.com/vapagentmedia/vap-showcase) | `examples/claude_desktop_config.json` | 1 (vap) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-vap` |
| 46 | [sudhanshubliz/asm-mcp-materials-platform](https://github.com/sudhanshubliz/asm-mcp-materials-platform) | `.well-known/claude_desktop_config.json` | 1 (materials-platform) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-materials-platform` |
| 47 | [mohamedo-ohany/portfolio](https://github.com/mohamedo-ohany/portfolio) | `mpc.json` | 1 (Astro docs) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-Astro docs` |
| 48 | [ovftank/system-monitor](https://github.com/ovftank/system-monitor) | `.mcp.json` | 1 (deepwiki) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-deepwiki` |
| 49 | [mahi0331/FinSage](https://github.com/mahi0331/FinSage) | `mcp.json` | 1 (fi_mcp) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-fi_mcp` |
| 50 | [citedy/citedy-cursor-plugin](https://github.com/citedy/citedy-cursor-plugin) | `mcp.json` | 1 (citedy) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-citedy` |
| 51 | [raisely/cursor-plugin](https://github.com/raisely/cursor-plugin) | `mcp.json` | 1 (Raisely) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-Raisely` |
| 52 | [stunt-double/stuntdouble-mcp](https://github.com/stunt-double/stuntdouble-mcp) | `mcp.json` | 1 (stuntdouble) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-stuntdouble` |
| 53 | [BetterStackHQ/cursor-plugin](https://github.com/BetterStackHQ/cursor-plugin) | `mcp.json` | 1 (better-stack) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-better-stack` |
| 54 | [pateta-murcho/cachorro-melo](https://github.com/pateta-murcho/cachorro-melo) | `mcp.json` | 1 (supabase) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-supabase` |
| 55 | [ChatPRD/cursor-plugin](https://github.com/ChatPRD/cursor-plugin) | `mcp.json` | 1 (ChatPRD) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-ChatPRD` |
| 56 | [sfc-gh-praj/basic_mcp_spcs](https://github.com/sfc-gh-praj/basic_mcp_spcs) | `mcp.json` | 1 (spcs-mcp) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-spcs-mcp` |
| 57 | [mao-family/claude-me](https://github.com/mao-family/claude-me) | `mcp.json` | 2 (notion, notebooklm) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-notion` |
| 58 | [sjhallo07/rag-agentic-ai-capstone-project](https://github.com/sjhallo07/rag-agentic-ai-capstone-project) | `mcp.json` | 2 (gradio-docs, gradio-docs-claude) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-gradio-docs` |
| 59 | [joai-plugins/multiversx](https://github.com/joai-plugins/multiversx) | `mcp.json` | 1 (joai-multiversx) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-joai-multiversx` |
| 60 | [KamarLimaog/comfyprotocol](https://github.com/KamarLimaog/comfyprotocol) | `mcp.json` | 1 (Inco-mcp) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-Inco-mcp` |
| 61 | [openaccountants/marketplace](https://github.com/openaccountants/marketplace) | `plugins/openaccountants-vertical-medical-professional/.mcp.json` | 1 (openaccountants) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-openaccountants` |
| 62 | [Stacks-du-Beurre/nxt](https://github.com/Stacks-du-Beurre/nxt) | `claude_desktop_config.json` | 1 (nxt) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-nxt` |
| 63 | [Acidni-LLC/jobmaster-mcp](https://github.com/Acidni-LLC/jobmaster-mcp) | `examples/claude_desktop_config.json` | 3 (jobmaster-hosted, jobmaster-self-host, jobmaster-local-only) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-jobmaster-hosted` |
| 64 | [jasonxkensei/xproof-examples](https://github.com/jasonxkensei/xproof-examples) | `multiversx-mcp/claude_desktop_config.json` | 2 (multiversx-sc, xproof) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-xproof` |
| 65 | [Rawgrowth-Consulting/rawclaw](https://github.com/Rawgrowth-Consulting/rawclaw) | `claude_desktop_config.json` | 1 (rawgrowth-aios) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-rawgrowth-aios` |
| 66 | [matthewnyc2/LLM](https://github.com/matthewnyc2/LLM) | `.claude_desktop_config.json` | 7 (playwright, ref, desktop-commander +4 more) | 1 | 0 | 3 | 25 | MEDIUM: `CONTEXT-EXT-FETCH-playwright`; CRITICAL: `AUTH-MISSING-sequential-thinking` |
| 67 | [karohakrij/pinnybinny-mcp](https://github.com/karohakrij/pinnybinny-mcp) | `examples/claude_desktop_config.json` | 1 (pinnybinny) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-pinnybinny` |
| 68 | [ariffazil/oo0-STATE](https://github.com/ariffazil/oo0-STATE) | `arifOS/codebase/templates/claude_desktop_config.json` | 1 (arifos-production) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-arifos-production` |
| 69 | [timescale/pg-aiguide](https://github.com/timescale/pg-aiguide) | `mcp.json` | 1 (pg-aiguide) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-pg-aiguide` |
| 70 | [HonzaHezina/algo-trader](https://github.com/HonzaHezina/algo-trader) | `.mcp.json` | 1 (github) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-github` |
| 71 | [zerlake/thesisai-philippines](https://github.com/zerlake/thesisai-philippines) | `amp.json` | 1 (serena) | 1 | 0 | 2 | 25 | CRITICAL: `DANGEROUS-POPULAR-serena-shell-execution` |
| 72 | [NiksheyYadav/ic1101](https://github.com/NiksheyYadav/ic1101) | `.mcp.json` | 1 (Sentry) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-Sentry` |
| 73 | [Verone2021/Template_dev](https://github.com/Verone2021/Template_dev) | `.mcp.json` | 6 (supabase, context7, serena +3 more) | 1 | 0 | 3 | 25 | MEDIUM: `CONTEXT-INJECT-context7`; CRITICAL: `DANGEROUS-POPULAR-serena-shell-execution` |
| 74 | [CypherAi-hub/Netwatch](https://github.com/CypherAi-hub/Netwatch) | `.mcp.json` | 1 (supabase) | 1 | 0 | 2 | 25 | CRITICAL: `AUTH-MISSING-supabase` |
| 75 | [DivitMittal/playbooks-4-windows](https://github.com/DivitMittal/playbooks-4-windows) | `.mcp.json` | 2 (ansible, serena) | 1 | 0 | 2 | 25 | CRITICAL: `DANGEROUS-POPULAR-serena-shell-execution` |

### HIGH Configs (173)

| # | Repo | Config Path | Servers | C | H | M | Risk | Notable Findings |
|---|---|---|---|---|---|---|---|---|
| 1 | [mokemoke0821/claude-mcp-integration](https://github.com/mokemoke0821/claude-mcp-integration) | `stable_claude_desktop_config.json` | 4 (filesystem, playwright, enhanced_file_commander +1 more) | 0 | 4 | 3 | 100 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `DANGEROUS-PKG-playwright-browser-automation`; MEDIUM: `CONTEXT-EXT-FETCH-playwright`; HIGH: `DANGEROUS-CUSTOM-enhanced_file_commander-filesystem`; HIGH: `DANGEROUS-CUSTOM-powershell-commander-shell` |
| 2 | [aksh9dyrs/postgres-extension-mcp-server](https://github.com/aksh9dyrs/postgres-extension-mcp-server) | `backend/claude_desktop_config.json` | 1 (postgres-extensions) | 0 | 6 | 2 | 100 | HIGH: `ENV-SECRET-postgres-extensions-SAMBANOVA_API_KEY`; HIGH: `CONN-STRING-ENV-postgres-extensions-DATABASE_URL`; HIGH: `CONN-STRING-ENV-postgres-extensions-DATABASE_URL2`; HIGH: `CONN-STRING-ENV-postgres-extensions-DATABASE_URL3`; HIGH: `CONN-STRING-ENV-postgres-extensions-DATABASE_URL4` (+1 more) |
| 3 | [TSGCFO/dev-box](https://github.com/TSGCFO/dev-box) | `claude_desktop_config.json` | 21 (filesystem, sequential-thinking, browserbase +18 more) | 0 | 5 | 5 | 100 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `ENV-SECRET-browserbase-BROWSERBASE_API_KEY`; MEDIUM: `CONTEXT-EXT-FETCH-fetch`; MEDIUM: `CONTEXT-EXT-FETCH-fetch-save`; MEDIUM: `CONTEXT-EXT-FETCH-puppeteer` (+3 more) |
| 4 | [victorlps/fabrica-ia](https://github.com/victorlps/fabrica-ia) | `.mcp.json` | 4 (filesystem, git, postgres +1 more) | 0 | 3 | 2 | 75 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `DANGEROUS-PKG-postgres-database`; HIGH: `CONN-STRING-ARGS-postgres` |
| 5 | [Monjyu1101/Monjyu2025](https://github.com/Monjyu1101/Monjyu2025) | `_config/claude_desktop_config.json` | 3 (filesystem, perplexity-ask, playwright) | 0 | 3 | 2 | 75 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `ENV-SECRET-perplexity-ask-PERPLEXITY_API_KEY`; HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 6 | [aegntic/ae-co-system](https://github.com/aegntic/ae-co-system) | `LeeGen/claude/claude_desktop_config.json` | 13 (filesystem, git, postgresql +10 more) | 0 | 3 | 5 | 75 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `DANGEROUS-PKG-postgresql-database`; HIGH: `CONN-STRING-ARGS-postgresql`; MEDIUM: `CONTEXT-EXT-FETCH-web-search`; MEDIUM: `CONTEXT-EXT-FETCH-crawl4ai` (+1 more) |
| 7 | [horizoncoder/claude-setup-dev](https://github.com/horizoncoder/claude-setup-dev) | `config/claude_desktop_config.json` | 5 (memory, sequential-thinking, postgres +2 more) | 0 | 3 | 2 | 75 | HIGH: `CONN-STRING-ENV-postgres-POSTGRES_CONNECTION_STRING`; HIGH: `ENV-SECRET-playwright-PLAYWRIGHT_MCP_EXTENSION_TOKEN`; HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 8 | [arturo-ebuck/claude-code-complete-setup](https://github.com/arturo-ebuck/claude-code-complete-setup) | `config/claude-code/claude_desktop_config.json` | 19 (filesystem, github, postgres +16 more) | 0 | 3 | 5 | 75 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `DANGEROUS-PKG-github-source-control`; HIGH: `DANGEROUS-PKG-postgres-database`; MEDIUM: `CONTEXT-EXT-FETCH-puppeteer`; MEDIUM: `CONTEXT-EXT-FETCH-exa` (+1 more) |
| 9 | [Cordycepsers/vscode-claude-setup-2025](https://github.com/Cordycepsers/vscode-claude-setup-2025) | `claude_desktop_config.json` | 16 (filesystem, git, github +13 more) | 0 | 3 | 5 | 75 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-fetch`; MEDIUM: `CONTEXT-EXT-FETCH-brave-search`; HIGH: `DANGEROUS-PKG-postgres-database`; HIGH: `CONN-STRING-ENV-postgres-POSTGRES_CONNECTION_STRING` (+1 more) |
| 10 | [duksosleepy/dotfiles](https://github.com/duksosleepy/dotfiles) | `claude_desktop_config.json` | 10 (github, sequential-thinking, postgres +7 more) | 0 | 3 | 4 | 75 | HIGH: `ENV-SECRET-github-GITHUB_PERSONAL_ACCESS_TOKEN`; HIGH: `DANGEROUS-PKG-postgres-database`; HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-fetch`; MEDIUM: `CONTEXT-EXT-FETCH-puppeteer` |
| 11 | [miketui/Man](https://github.com/miketui/Man) | `claude_desktop_config.json` | 8 (terragonnmcp, filesystem, brave-search +5 more) | 0 | 2 | 5 | 50 | MEDIUM: `CONTEXT-INJECT-terragonnmcp`; MEDIUM: `CONTEXT-EXT-FETCH-terragonnmcp`; HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-brave-search`; HIGH: `DANGEROUS-PKG-sqlite-database` |
| 12 | [glaucia86/weather-mcp-server](https://github.com/glaucia86/weather-mcp-server) | `claude_desktop_config.json.text` | 1 (weather-mcp) | 0 | 2 | 2 | 50 | HIGH: `ENV-SECRET-weather-mcp-WEATHER_API_KEY`; HIGH: `CONN-STRING-ENV-weather-mcp-DATABASE_URL` |
| 13 | [EricTechPro/fitbox](https://github.com/EricTechPro/fitbox) | `claude_desktop_config.json` | 3 (supabase-fitbox, shadcn, playwright) | 0 | 2 | 3 | 50 | HIGH: `ENV-SECRET-supabase-fitbox-SUPABASE_ACCESS_TOKEN`; HIGH: `DANGEROUS-PKG-playwright-browser-automation`; MEDIUM: `CONTEXT-EXT-FETCH-playwright` |
| 14 | [AgentaOS/guardian-wallet](https://github.com/AgentaOS/guardian-wallet) | `examples/mcp/claude_desktop_config.json` | 1 (guardian) | 0 | 2 | 2 | 50 | HIGH: `ENV-SECRET-guardian-GUARDIAN_API_SECRET`; HIGH: `ENV-SECRET-guardian-GUARDIAN_API_KEY` |
| 15 | [asatake/dotfiles](https://github.com/asatake/dotfiles) | `shared/claude/claude_desktop_config.json` | 10 (claude_code, canva, POKER ROOM redash +7 more) | 0 | 2 | 3 | 50 | HIGH: `ENV-SECRET-POKER ROOM redash-REDASH_API_KEY`; HIGH: `ENV-SECRET-shortcut-SHORTCUT_API_TOKEN`; MEDIUM: `CONTEXT-EXT-FETCH-awslabs.bedrock-kb-retrieval-mcp-server` |
| 16 | [applejxd/windows-setup](https://github.com/applejxd/windows-setup) | `config/claude_desktop_config.json` | 8 (desktop-commander, Context7, deepwiki +5 more) | 0 | 2 | 3 | 50 | MEDIUM: `CONTEXT-INJECT-Context7`; HIGH: `DANGEROUS-PKG-playwright-browser-automation`; HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 17 | [jordangarrison/nix-config](https://github.com/jordangarrison/nix-config) | `users/jordangarrison/tools/claude-desktop/claude_desktop_config.json` | 2 (filesystem, logseq) | 0 | 2 | 2 | 50 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `ENV-SECRET-logseq-LOGSEQ_API_TOKEN` |
| 18 | [Abady001/claude-template](https://github.com/Abady001/claude-template) | `mcp.json` | 6 (filesystem, memory, git +3 more) | 0 | 2 | 2 | 50 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `DANGEROUS-PKG-postgres-database` |
| 19 | [DaveIW2034/FastApi100](https://github.com/DaveIW2034/FastApi100) | `mcp.json` | 4 (filesystem, openapi, git +1 more) | 0 | 2 | 2 | 50 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `CONN-STRING-ARGS-sql` |
| 20 | [DonCitron/-chantal-website-finish](https://github.com/DonCitron/-chantal-website-finish) | `mcp.json` | 7 (brave-search, github, sequential-thinking +4 more) | 0 | 2 | 6 | 50 | HIGH: `ENV-SECRET-brave-search-BRAVE_API_KEY`; MEDIUM: `CONTEXT-EXT-FETCH-brave-search`; HIGH: `ENV-SECRET-github-GITHUB_TOKEN`; MEDIUM: `CONTEXT-EXT-FETCH-puppeteer`; MEDIUM: `CONTEXT-INJECT-context7` (+1 more) |
| 21 | [bogdanticu88/mcp-map](https://github.com/bogdanticu88/mcp-map) | `examples/claude_desktop_config.json` | 4 (filesystem, bash, browser +1 more) | 0 | 2 | 2 | 50 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `DANGEROUS-PKG-browser-browser-automation` |
| 22 | [aski-p/kakao-skill-webhook](https://github.com/aski-p/kakao-skill-webhook) | `claude_desktop_config.json` | 4 (firebase, filesystem, supabase +1 more) | 0 | 2 | 2 | 50 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 23 | [markus41/AdvisorOS](https://github.com/markus41/AdvisorOS) | `.claude/claude_desktop_config.json` | 43 (advisoros-context, tenant-validator, zen-mcp-server +40 more) | 0 | 2 | 4 | 50 | HIGH: `DANGEROUS-PKG-postgresql-mcp-database`; HIGH: `CONN-STRING-ENV-postgresql-mcp-POSTGRES_CONNECTION_STRING`; MEDIUM: `CONTEXT-EXT-FETCH-browser-mcp`; MEDIUM: `CONTEXT-EXT-FETCH-playwright-mcp` |
| 24 | [cemini23/Cybersecurity-wiki](https://github.com/cemini23/Cybersecurity-wiki) | `claude_desktop_config.json.example` | 4 (filesystem, brave-search, playwright +1 more) | 0 | 2 | 4 | 50 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-brave-search`; HIGH: `DANGEROUS-PKG-playwright-browser-automation`; MEDIUM: `CONTEXT-INJECT-context7` |
| 25 | [foodixsas/th_app_base_datos_colaboradores](https://github.com/foodixsas/th_app_base_datos_colaboradores) | `claude_desktop_config.json` | 4 (colaboradores-foodix, filesystem, fetch +1 more) | 0 | 2 | 3 | 50 | HIGH: `ENV-SECRET-colaboradores-foodix-AIRTABLE_API_KEY`; HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-fetch` |
| 26 | [urib94/Clinical-Trial-AWS](https://github.com/urib94/Clinical-Trial-AWS) | `.claude/claude_desktop_config.json` | 6 (aws-clinical-trial, postgres-clinical, github-clinical +3 more) | 0 | 2 | 3 | 50 | HIGH: `DANGEROUS-PKG-postgres-clinical-database`; HIGH: `DANGEROUS-PKG-filesystem-clinical-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-brave-search` |
| 27 | [yangsi7/wearable-analyzer](https://github.com/yangsi7/wearable-analyzer) | `claude_desktop_config.json` | 14 (brave-search, supabase, memory +11 more) | 0 | 2 | 6 | 50 | MEDIUM: `CONTEXT-EXT-FETCH-brave-search`; MEDIUM: `CONTEXT-INJECT-context7`; HIGH: `ENV-SECRET-n8n-local-N8N_WEBHOOK_PASSWORD`; HIGH: `DANGEROUS-PKG-n8n-local-workflow-execution`; MEDIUM: `CONTEXT-EXT-FETCH-crawl4ai-rag` (+1 more) |
| 28 | [toolate28/kenl](https://github.com/toolate28/kenl) | `claude_desktop_config.json` | 4 (filesystem, git, cloudflare +1 more) | 0 | 2 | 2 | 50 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `ENV-SECRET-cloudflare-CLOUDFLARE_API_TOKEN` |
| 29 | [yamamoto7/.dotfiles](https://github.com/yamamoto7/.dotfiles) | `lib/claude_desktop_config.json` | 7 (figma-developer-mcp, filesystem, git +4 more) | 0 | 2 | 3 | 50 | HIGH: `ENV-SECRET-figma-developer-mcp-FIGMA_API_KEY`; MEDIUM: `CONTEXT-INJECT-figma-developer-mcp`; HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 30 | [ankur-acceldata/xdp-mcp-server](https://github.com/ankur-acceldata/xdp-mcp-server) | `claude_desktop_config.json` | 1 (xdp) | 0 | 2 | 3 | 50 | HIGH: `ENV-SECRET-xdp-XDP_ACCESS_KEY`; HIGH: `ENV-SECRET-xdp-XDP_SECRET_KEY`; MEDIUM: `CONTEXT-EXT-FETCH-xdp` |
| 31 | [dandacompany/dantelabs-mcp-n8n-fastcampus](https://github.com/dandacompany/dantelabs-mcp-n8n-fastcampus) | `Part4_n8n_based_MCP_PJT/claude_desktop_config.json` | 10 (Playwright, DesktopCommander, SequentialThinking +7 more) | 0 | 2 | 4 | 50 | HIGH: `DANGEROUS-PKG-Playwright-browser-automation`; MEDIUM: `CONTEXT-EXT-FETCH-DataCrawler`; HIGH: `CONN-STRING-ARGS-PostgreSQL`; MEDIUM: `CONTEXT-EXT-FETCH-RAGMaker` |
| 32 | [syedazharmbnr1/ClaudeMCPServer](https://github.com/syedazharmbnr1/ClaudeMCPServer) | `claude_desktop_config.json` | 7 (filesystem, github, screen +4 more) | 0 | 2 | 2 | 50 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `ENV-SECRET-github-GITHUB_PERSONAL_ACCESS_TOKEN` |
| 33 | [Surya-KF/Enterprise-Expense-Automation-System-using-MCP-NLP](https://github.com/Surya-KF/Enterprise-Expense-Automation-System-using-MCP-NLP) | `claude_desktop_config.json` | 2 (personal-expense-tracker, company-expense-tracker) | 0 | 2 | 2 | 50 | HIGH: `ENV-SECRET-personal-expense-tracker-GEMINI_API_KEY`; HIGH: `ENV-SECRET-company-expense-tracker-GEMINI_API_KEY` |
| 34 | [Amitkumarracha/mcp-multi-tool-agent](https://github.com/Amitkumarracha/mcp-multi-tool-agent) | `claude_desktop_config.json` | 3 (news, currency, math) | 0 | 2 | 2 | 50 | HIGH: `ENV-SECRET-news-NEWS_API_KEY`; HIGH: `ENV-SECRET-currency-CURRENCY_API_KEY` |
| 35 | [craigoj/dayton-business-directory](https://github.com/craigoj/dayton-business-directory) | `mcp-server/claude_desktop_config.json` | 2 (supabase, brightdata) | 0 | 2 | 2 | 50 | HIGH: `ENV-SECRET-supabase-SUPABASE_ACCESS_TOKEN`; HIGH: `ENV-SECRET-brightdata-API_TOKEN` |
| 36 | [nimazasinich/DreammakerCryptoSignalAndTrader_2](https://github.com/nimazasinich/DreammakerCryptoSignalAndTrader_2) | `claude_desktop_config.json` | 12 (filesystem, git, github +9 more) | 0 | 2 | 4 | 50 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `DANGEROUS-PKG-sqlite-database`; MEDIUM: `CONTEXT-EXT-FETCH-puppeteer`; MEDIUM: `CONTEXT-EXT-FETCH-brave-search` |
| 37 | [joelbcastillo/dotfiles](https://github.com/joelbcastillo/dotfiles) | `tools/mcp/claude_desktop_config.json.template` | 5 (notion, google-drive, linear +2 more) | 0 | 2 | 2 | 50 | HIGH: `ENV-SECRET-notion-NOTION_API_KEY`; HIGH: `ENV-SECRET-google-drive-GOOGLE_DRIVE_OAUTH_CREDENTIALS` |
| 38 | [jkilelo/ai_apps](https://github.com/jkilelo/ai_apps) | `claude_desktop_config.json.example` | 6 (filesystem, git, sqlite +3 more) | 0 | 2 | 3 | 50 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `DANGEROUS-PKG-playwright-browser-automation`; MEDIUM: `CONTEXT-EXT-FETCH-playwright` |
| 39 | [girdav01/TV1-MINIO](https://github.com/girdav01/TV1-MINIO) | `mcp/claude_desktop_config.json.example` | 1 (tv1-minio-integration) | 0 | 2 | 2 | 50 | HIGH: `ENV-SECRET-tv1-minio-integration-MINIO_ACCESS_KEY`; HIGH: `ENV-SECRET-tv1-minio-integration-MINIO_SECRET_KEY` |
| 40 | [shivamkumar-kimbal/claude-rib-cage](https://github.com/shivamkumar-kimbal/claude-rib-cage) | `mcp.json` | 4 (filesystem, github, postgres +1 more) | 0 | 2 | 3 | 50 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; HIGH: `DANGEROUS-PKG-postgres-database`; MEDIUM: `CONTEXT-EXT-FETCH-brave-search` |
| 41 | [Anshu666666/mcp](https://github.com/Anshu666666/mcp) | `mcp.json` | 3 (playwright, filesystem, github) | 0 | 2 | 2 | 50 | HIGH: `DANGEROUS-PKG-playwright-browser-automation`; HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 42 | [prayanks/mcp-sqlite-server](https://github.com/prayanks/mcp-sqlite-server) | `claude_desktop_config.json.sample` | 4 (playwright, toolbase-proxy, sqlite_mcp_server_sdio +1 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 43 | [sendaifun/solana-mcp](https://github.com/sendaifun/solana-mcp) | `claude_desktop_config.json` | 1 (agent-kit) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-agent-kit-OPENAI_API_KEY` |
| 44 | [moode774/-Claude-Firebase-ai](https://github.com/moode774/-Claude-Firebase-ai) | `claude_desktop_config.json.exampl` | 2 (filesystem, firestore) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 45 | [TalkStudioLLC/AGI](https://github.com/TalkStudioLLC/AGI) | `merged_claude_desktop_config.json` | 2 (filesystems, agi-server) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystems-filesystem` |
| 46 | [okgoogle13/careercopilot](https://github.com/okgoogle13/careercopilot) | `tools/config/claude_desktop_config.json.backup` | 6 (filesystem, git, task-router +3 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 47 | [JFinchy/morning-pod](https://github.com/JFinchy/morning-pod) | `claude_desktop_config.json` | 4 (sequential-thinking, playwright, Context7 +1 more) | 0 | 1 | 4 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation`; MEDIUM: `CONTEXT-EXT-FETCH-playwright`; MEDIUM: `CONTEXT-INJECT-Context7` |
| 48 | [Dar-Blockchain/talentai](https://github.com/Dar-Blockchain/talentai) | `.claude_desktop_config.json` | 1 (motiff) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-motiff-MOTIFF_TOKEN` |
| 49 | [Icekabob/Mast_Query](https://github.com/Icekabob/Mast_Query) | `claude_desktop_config.json` | 3 (JWST, weather, filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 50 | [rmnanney/PAWS360](https://github.com/rmnanney/PAWS360) | `config/claude_desktop_config.json` | 1 (jira-pgb) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-jira-pgb-JIRA_API_KEY` |
| 51 | [hugoles/langfuse-mcp](https://github.com/hugoles/langfuse-mcp) | `examples/claude_desktop_config.json` | 1 (langfuse) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-langfuse-LANGFUSE_SECRET_KEY` |
| 52 | [guscherer/pubg-coach-ai](https://github.com/guscherer/pubg-coach-ai) | `claude_desktop_config.json` | 4 (pubg-coach, github, fetch +1 more) | 0 | 1 | 3 | 25 | MEDIUM: `CONTEXT-EXT-FETCH-fetch`; HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 53 | [macdroidapps/mcp-weather-test](https://github.com/macdroidapps/mcp-weather-test) | `claude_desktop_config.json` | 1 (weather) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-weather-YANDEX_WEATHER_API_KEY` |
| 54 | [BoisAuLit/langchain-anthropic-mcp](https://github.com/BoisAuLit/langchain-anthropic-mcp) | `claude_desktop_config.json` | 3 (filesystem, research, fetch) | 0 | 1 | 3 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-fetch` |
| 55 | [AntonioKOD/mcp-starter](https://github.com/AntonioKOD/mcp-starter) | `claude_desktop_config.json` | 1 (mcp-starter) | 0 | 1 | 2 | 25 | HIGH: `CONN-STRING-ENV-mcp-starter-DATABASE_URL` |
| 56 | [asem187/mcp-tools](https://github.com/asem187/mcp-tools) | `claude_desktop_config.json` | 4 (docker, github, brave-search +1 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-github-source-control` |
| 57 | [Monjyu1101/Monjyu2025](https://github.com/Monjyu1101/Monjyu2025) | `claude_desktop_config.json` | 2 (filesystem, helloworld) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 58 | [bennypollak/agent-mcp](https://github.com/bennypollak/agent-mcp) | `claude_desktop_config.json` | 2 (automation, clock_mcp) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-automation-ASK_TOKENS_PATH` |
| 59 | [chatman-media/timeline-studio](https://github.com/chatman-media/timeline-studio) | `claude_desktop_config.json.example` | 9 (sequential-thinking, github, memory +6 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 60 | [Arturo-Quiroga-MSFT/DBMS_Assistant_SK](https://github.com/Arturo-Quiroga-MSFT/DBMS_Assistant_SK) | `MssqlMcp/Node/src/samples/contoso_claude_desktop_config.json` | 1 (mssql-contoso) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-mssql-contoso-SQL_PASSWORD` |
| 61 | [mac999/infra_ai_agent_tutorials](https://github.com/mac999/infra_ai_agent_tutorials) | `08_AI_Agent/4_llm_mcp_app/claude_desktop_config.json` | 5 (filesystem, blender, simple-calc +2 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 62 | [AndreChuabio/mcp-yfinance-server](https://github.com/AndreChuabio/mcp-yfinance-server) | `claude_desktop_config.json` | 1 (mcp-yfinance-server) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-mcp-yfinance-server-paper_API_KEY` |
| 63 | [up1/demo-mcp-notion](https://github.com/up1/demo-mcp-notion) | `demo-mcp/claude_desktop_config.json` | 1 (file-notion-mcp) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-file-notion-mcp-NOTION_API_KEY` |
| 64 | [1ndoryu/task](https://github.com/1ndoryu/task) | `mcp/claude_desktop_config.json` | 1 (glory-tareas) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-glory-tareas-GLORY_WP_PASSWORD` |
| 65 | [PedroHSGuimaraes/nuvem-shop-mcp-server](https://github.com/PedroHSGuimaraes/nuvem-shop-mcp-server) | `claude_desktop_config.json` | 1 (tiendanube) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-tiendanube-TIENDANUBE_ACCESS_TOKEN` |
| 66 | [tomkat-cr/abstractgo](https://github.com/tomkat-cr/abstractgo) | `mcp-server/claude_desktop_config.json` | 1 (abstractgo) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-abstractgo-AG_API_KEY` |
| 67 | [goooichi51/claudecode_test2](https://github.com/goooichi51/claudecode_test2) | `.claude/claude_desktop_config.json` | 1 (filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 68 | [saabiqsaha/agentic_transaction_protocol](https://github.com/saabiqsaha/agentic_transaction_protocol) | `mcp_server/claude_desktop_config.json` | 1 (cowrie) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-cowrie-AGENT_PRIVATE_KEY` |
| 69 | [sylweriusz/mcp-neo4j-memory-server](https://github.com/sylweriusz/mcp-neo4j-memory-server) | `claude_desktop_config.json` | 1 (graph-memory) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-graph-memory-NEO4J_PASSWORD` |
| 70 | [willowduster/cave-crawler](https://github.com/willowduster/cave-crawler) | `claude_desktop_config.json` | 4 (filesystem, git, godot +1 more) | 0 | 1 | 5 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-git`; MEDIUM: `CONTEXT-EXT-FETCH-godot` |
| 71 | [samihalawa/tally-mcp-server](https://github.com/samihalawa/tally-mcp-server) | `claude_desktop_config.json` | 1 (tally-mcp-smithery) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-tally-mcp-smithery-TALLY_API_KEY` |
| 72 | [jimiryquai/power-platform-orchestration-agent](https://github.com/jimiryquai/power-platform-orchestration-agent) | `testing/mcp-testing/claude_desktop_config.json` | 1 (power-platform-orchestrator) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-power-platform-orchestrator-AZURE_CLIENT_SECRET` |
| 73 | [yoichiojima-2/mcp-servers](https://github.com/yoichiojima-2/mcp-servers) | `examples/config/claude-desktop/claude_desktop_config.json` | 4 (composite, filesystem, memory +1 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 74 | [fikriaf/ordo](https://github.com/fikriaf/ordo) | `ordo-digital-assist/examples/mcp/agent-kit-mcp-server/claude_desktop_config.json` | 1 (agent-kit) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-agent-kit-OPENAI_API_KEY` |
| 75 | [ellingtonsp/evonexus-agents](https://github.com/ellingtonsp/evonexus-agents) | `Lead-Enrichment-Demo/evonexus-demo/brewops/setup/templates/claude_desktop_config.json` | 2 (notion, filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 76 | [canjrgultekin/DevKit](https://github.com/canjrgultekin/DevKit) | `mcp-server/src/claude_desktop_config.json` | 3 (devkit, playwright, windows-mcp) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 77 | [GuilhermeAlbert/awesome-ai-conventions](https://github.com/GuilhermeAlbert/awesome-ai-conventions) | `examples/model-context-protocol/claude_desktop_config.json` | 2 (project-files, memory) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-project-files-filesystem` |
| 78 | [RamonMiguel717/automato](https://github.com/RamonMiguel717/automato) | `docs/claude_desktop_config.json` | 1 (filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 79 | [AaryansNepal/TigerLite](https://github.com/AaryansNepal/TigerLite) | `mcp-server/claude_desktop_config.json` | 1 (tigerlite) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-tigerlite-AWS_SECRET_ACCESS_KEY` |
| 80 | [p3LZ3r/kontist-eur-report-generator](https://github.com/p3LZ3r/kontist-eur-report-generator) | `.mcp.json` | 2 (task-master-ai, playwright) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 81 | [Web4application/Goldhawk](https://github.com/Web4application/Goldhawk) | `Mcp.json` | 1 (filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 82 | [binchenz/omaha-ontocenter-v2](https://github.com/binchenz/omaha-ontocenter-v2) | `.mcp.json` | 1 (omaha) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-omaha-OMAHA_API_KEY` |
| 83 | [dylanapplegate/my-hermes-agent](https://github.com/dylanapplegate/my-hermes-agent) | `mcp.json` | 2 (firecrawl-mcp, docker) | 0 | 1 | 3 | 25 | HIGH: `ENV-SECRET-firecrawl-mcp-FIRECRAWL_API_KEY`; MEDIUM: `CONTEXT-EXT-FETCH-firecrawl-mcp` |
| 84 | [skwldwld/Individual-Research](https://github.com/skwldwld/Individual-Research) | `mcp.json` | 1 (filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 85 | [RgbGuy-Yx/mentorship-platform](https://github.com/RgbGuy-Yx/mentorship-platform) | `mcp.json` | 1 (TestSprite) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-TestSprite-API_KEY` |
| 86 | [nadavyigal/ResumeBuilder-AI](https://github.com/nadavyigal/ResumeBuilder-AI) | `mcp.json` | 1 (playwright) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 87 | [kasiperumal/misc](https://github.com/kasiperumal/misc) | `mcp.json` | 6 (jira, confluence, oracle +3 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 88 | [nikhiltidke101/mcpo-sanity](https://github.com/nikhiltidke101/mcpo-sanity) | `mcp.json` | 1 (sanity) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-sanity-SANITY_API_TOKEN` |
| 89 | [Karunpahwa/x](https://github.com/Karunpahwa/x) | `mcp.json` | 1 (ui-helper-ai) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-ui-helper-ai-OPENAI_API_KEY` |
| 90 | [bbakus/LayersAI---Job-Seeker](https://github.com/bbakus/LayersAI---Job-Seeker) | `mcp.json` | 3 (supabase, context7, shadcn-ui) | 0 | 1 | 3 | 25 | HIGH: `ENV-SECRET-supabase-SUPABASE_ACCESS_TOKEN`; MEDIUM: `CONTEXT-INJECT-context7` |
| 91 | [Dominik7231/techcompare](https://github.com/Dominik7231/techcompare) | `mcp.json` | 1 (TestSprite) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-TestSprite-API_KEY` |
| 92 | [JohnSoltann/talanor003](https://github.com/JohnSoltann/talanor003) | `mcp.json` | 1 (filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 93 | [harshitpambhar/Travel-Guide](https://github.com/harshitpambhar/Travel-Guide) | `mcp.json` | 1 (supabase) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-supabase-SUPABASE_ACCESS_TOKEN` |
| 94 | [gamasenninn/ptt](https://github.com/gamasenninn/ptt) | `ptt-box/mcp_config.json` | 5 (filesystem, time, memory +2 more) | 0 | 1 | 3 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-tavily` |
| 95 | [matkoson/zzz](https://github.com/matkoson/zzz) | `.config/claude-desktop/claude_desktop_config.json.mustache` | 31 (jetbrains, github, sequential-thinking +28 more) | 0 | 1 | 6 | 25 | MEDIUM: `CONTEXT-EXT-FETCH-puppeteer`; HIGH: `DANGEROUS-PKG-playwright-browser-automation`; MEDIUM: `CONTEXT-EXT-FETCH-playwright`; MEDIUM: `CONTEXT-EXT-FETCH-mcp-server-fetch`; MEDIUM: `CONTEXT-EXT-FETCH-mcp-doc-scraper` |
| 96 | [Jony2176/Fotolibros-Argentina-](https://github.com/Jony2176/Fotolibros-Argentina-) | `claude_desktop_config.json` | 1 (browserbase-local) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-browserbase-local-OPENROUTER_API_KEY` |
| 97 | [sharedtable/SharedTableMobile](https://github.com/sharedtable/SharedTableMobile) | `claude_desktop_config.json` | 1 (figma) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-figma-FIGMA_PERSONAL_ACCESS_TOKEN` |
| 98 | [eyer-development/MCP](https://github.com/eyer-development/MCP) | `claude_desktop_config.json` | 2 (Eyer, filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 99 | [kozyocho/ai-search-engine](https://github.com/kozyocho/ai-search-engine) | `claude_desktop_config.json` | 2 (ai-search-engine-supabase, supabase) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-supabase-SUPABASE_DB_PASSWORD` |
| 100 | [jsliapark/brandvoice-mcp](https://github.com/jsliapark/brandvoice-mcp) | `examples/claude_desktop_config.json` | 1 (brandvoice) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-brandvoice-ANTHROPIC_API_KEY` |
| 101 | [okgoogle13/careercopilot](https://github.com/okgoogle13/careercopilot) | `.ai-audit-archive/claude_desktop_config.json.stale-20260406-005638` | 5 (filesystem, git, task-router +2 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 102 | [Pheelsyp/claude-vault-mcp-connect](https://github.com/Pheelsyp/claude-vault-mcp-connect) | `claude_desktop_config.json` | 1 (vault) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-vault-VAULT_TOKEN` |
| 103 | [r488it/claude_hands](https://github.com/r488it/claude_hands) | `claude_desktop_config.json` | 3 (claude_code_docker, tavily-mcp, playwright) | 0 | 1 | 3 | 25 | MEDIUM: `CONTEXT-EXT-FETCH-tavily-mcp`; HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 104 | [hyun-young/slack-mcp-pepeBot](https://github.com/hyun-young/slack-mcp-pepeBot) | `claude_desktop_config.json` | 1 (slack-mcp) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-slack-mcp-SLACK_BOT_TOKEN` |
| 105 | [foursquare/foursquare-places-mcp](https://github.com/foursquare/foursquare-places-mcp) | `fsq-server-python/claude_desktop_config.json` | 1 (foursquare) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-foursquare-FOURSQUARE_SERVICE_TOKEN` |
| 106 | [visweshwar/mcp-demo](https://github.com/visweshwar/mcp-demo) | `mcp-configs/claude/claude_desktop_config.json` | 3 (paychex-mcp, filesystem, git) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 107 | [bahaaldine/moltler](https://github.com/bahaaldine/moltler) | `mcp-bridge/claude_desktop_config.json` | 1 (moltler-skills) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-moltler-skills-ES_PASSWORD` |
| 108 | [islomar/my-notes](https://github.com/islomar/my-notes) | `AI/mcp-course-by-anthropic/claude_desktop_config.json` | 3 (filesystem, research, fetch) | 0 | 1 | 3 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-fetch` |
| 109 | [gunjanjp/powershell-mcp](https://github.com/gunjanjp/powershell-mcp) | `claude_desktop_config.json` | 1 (powershell) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-CUSTOM-powershell-shell` |
| 110 | [huckncatch/config](https://github.com/huckncatch/config) | `xdg-config/claude/claude_desktop_config.json` | 4 (kagi, mailmate, memory-files +1 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-memory-files-filesystem` |
| 111 | [repr0bated/op-dbus-staging](https://github.com/repr0bated/op-dbus-staging) | `docs/claude_desktop_config.json` | 3 (operation-dbus, filesystem, memory) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 112 | [toolate28/kenl](https://github.com/toolate28/kenl) | `modules/KENL3-dev/claude-code-setup/claude_desktop_config.json` | 3 (cloudflare, filesystem, git) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 113 | [MuhammadRaza-dev713/Tracking-MCP-Server](https://github.com/MuhammadRaza-dev713/Tracking-MCP-Server) | `claude_desktop_config.json` | 1 (conversion-debugger) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-conversion-debugger-GHL_API_KEY` |
| 114 | [BlueShapes/station-sign-generator](https://github.com/BlueShapes/station-sign-generator) | `.claude/claude_desktop_config.json` | 1 (playwright) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 115 | [SquadBotApp/quasaros-core](https://github.com/SquadBotApp/quasaros-core) | `claude_desktop_config.json` | 9 (n8n, aws-iac, chatgpt-cli +6 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-n8n-workflow-execution` |
| 116 | [djklmr2025/ELEMIA-v4-arkaios](https://github.com/djklmr2025/ELEMIA-v4-arkaios) | `claude_desktop_config.json` | 1 (elemia) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-elemia-ELEMIA_HTTP_TOKEN` |
| 117 | [mokemoke0821/claude-mcp-integration](https://github.com/mokemoke0821/claude-mcp-integration) | `fixed_claude_desktop_config.json` | 2 (filesystem, enhanced_development_commander) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 118 | [tier4/palladium-automation](https://github.com/tier4/palladium-automation) | `docs/claude_desktop_config.json.example.desktop` | 3 (etx-automation, github, local-filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-local-filesystem-filesystem` |
| 119 | [ariffazil/oo0-STATE](https://github.com/ariffazil/oo0-STATE) | `arifOS/aaa_mcp/claude_desktop_config.json` | 9 (arifos-kernel, arifos-filesystem, arifos-memory +6 more) | 0 | 1 | 4 | 25 | HIGH: `DANGEROUS-PKG-arifos-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-arifos-fetch`; MEDIUM: `CONTEXT-EXT-FETCH-arifos-brave-search` |
| 120 | [ECUCONDORSASBIC/DEVALTA](https://github.com/ECUCONDORSASBIC/DEVALTA) | `claude_desktop_config.json` | 9 (filesystem, memory, nextjs-turbopack-expert +6 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 121 | [rockcairn/claude-mcp-ah](https://github.com/rockcairn/claude-mcp-ah) | `claude_desktop_config.json` | 1 (filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 122 | [ephrin/openapi-mcp-bridge](https://github.com/ephrin/openapi-mcp-bridge) | `examples/claude-desktop/claude_desktop_config.json` | 1 (museum-api) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-museum-api-MUSEUM_API_PASSWORD` |
| 123 | [andalik/andalik-weather-mcp](https://github.com/andalik/andalik-weather-mcp) | `claude_desktop_config.json` | 1 (Andalik Weather MCP) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-Andalik Weather MCP-OPENWEATHER_API_KEY` |
| 124 | [rajveeerr/Hyperpersona](https://github.com/rajveeerr/Hyperpersona) | `mcp_server/examples/claude_desktop_config.json` | 1 (hyperpersona) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-hyperpersona-HYPERPERSONA_PASSWORD` |
| 125 | [angelargd8/proyecto1-redes](https://github.com/angelargd8/proyecto1-redes) | `config/claude_desktop_config.json` | 2 (filesystem, git-local) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 126 | [Themis128/my-portfolio-aws](https://github.com/Themis128/my-portfolio-aws) | `integrations/claude_desktop_config.json` | 9 (claude-copilot-bridge, claude-agent-orchestrator, portfolio-dev-tools +6 more) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-documentation-server-GEMINI_API_KEY` |
| 127 | [HostSuite455/mind-wander-flow](https://github.com/HostSuite455/mind-wander-flow) | `claude_desktop_config.json` | 2 (supabase, github) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-supabase-SUPABASE_ACCESS_TOKEN` |
| 128 | [bjkemp/mcp-midi](https://github.com/bjkemp/mcp-midi) | `examples/claude_desktop_config.json` | 3 (filesystem, desktop-commander, midi) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 129 | [ariffazil/wealth](https://github.com/ariffazil/wealth) | `claude_desktop_config.json` | 8 (arifos, geox, wealth +5 more) | 0 | 1 | 3 | 25 | HIGH: `DANGEROUS-PKG-mcp_filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-mcp_fetch` |
| 130 | [DanielaGuitz/MCP-Y-A2A](https://github.com/DanielaGuitz/MCP-Y-A2A) | `claude_desktop_config.json` | 2 (filesystem, github) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 131 | [PriyaVeerabomma/Intro-to-MCP](https://github.com/PriyaVeerabomma/Intro-to-MCP) | `code/claude_desktop_config.json.example` | 4 (llamacloud, filesystem, fetch +1 more) | 0 | 1 | 3 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-fetch` |
| 132 | [taop1988/ai_virtual_character_backend](https://github.com/taop1988/ai_virtual_character_backend) | `ai_virtual_character_backend/claude_desktop_config.json` | 2 (MiniMax, Supabase) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-MiniMax-MINIMAX_API_KEY` |
| 133 | [aigentone/Solana-Accelerate](https://github.com/aigentone/Solana-Accelerate) | `project-5/agent-kit-mcp-server/claude_desktop_config.json` | 1 (agent-kit) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-agent-kit-OPENAI_API_KEY` |
| 134 | [madhusudhanrao-ppm/code-assets](https://github.com/madhusudhanrao-ppm/code-assets) | `OWNMCP/claude_desktop_config.json` | 3 (filesystem, sqlcl, oracle-generative-ai) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 135 | [kongo97/simple-mcp-server](https://github.com/kongo97/simple-mcp-server) | `docs/claude_desktop_config.json` | 2 (filesystem, simple-mcp-server) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 136 | [gabriellsanabria/mcp-weather-server](https://github.com/gabriellsanabria/mcp-weather-server) | `claude_desktop_config.json` | 1 (weather-files) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-weather-files-WEATHER_API_KEY` |
| 137 | [archive-superdisco/zepai-graphiti](https://github.com/archive-superdisco/zepai-graphiti) | `config/mcp/claude_desktop_config.json` | 2 (graphiti-memory, @21st-dev/magic) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-@21st-dev/magic-API_KEY` |
| 138 | [bobinzuks/n8n-marketing-hub](https://github.com/bobinzuks/n8n-marketing-hub) | `marketing/mcp-server/claude_desktop_config.json` | 1 (8n8-marketing) | 0 | 1 | 2 | 25 | HIGH: `CONN-STRING-ENV-8n8-marketing-DATABASE_URL` |
| 139 | [lokavinashh2004/infinite-assessment](https://github.com/lokavinashh2004/infinite-assessment) | `claude_desktop_config.json` | 1 (claimcopilot) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-claimcopilot-OPENROUTER_API_KEY` |
| 140 | [W3JDev/ultimate-mcp-system](https://github.com/W3JDev/ultimate-mcp-system) | `config/claude_desktop_config.json` | 1 (ultimate-mcp-hub) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-ultimate-mcp-hub-N8N_API_KEY` |
| 141 | [RedAkasha/ProjetoFinalIBGE](https://github.com/RedAkasha/ProjetoFinalIBGE) | `claude_desktop_config.json` | 1 (ibge-pnad) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-ibge-pnad-DB_PASSWORD` |
| 142 | [geondongkim/geond-agent-protocol](https://github.com/geondongkim/geond-agent-protocol) | `examples/mcp_clients/claude_desktop_config.json` | 1 (geond) | 0 | 1 | 2 | 25 | HIGH: `CONN-STRING-ENV-geond-GEOND_DATABASE_URL` |
| 143 | [jegelstaff/formulize](https://github.com/jegelstaff/formulize) | `claude_desktop_config.json` | 1 (formulize) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-formulize-FORMULIZE_API_KEY` |
| 144 | [yannabadie/nexus-evidence](https://github.com/yannabadie/nexus-evidence) | `examples/claude_desktop_config.json` | 1 (nexus-evidence) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-nexus-evidence-ANTHROPIC_API_KEY` |
| 145 | [kamzouj-cloudguard/openproject-mcp-fastmcp](https://github.com/kamzouj-cloudguard/openproject-mcp-fastmcp) | `claude_desktop_config.json` | 1 (openproject-mcp) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-openproject-mcp-OPENPROJECT_API_KEY` |
| 146 | [Trollz1004/ANTIGRAVITY](https://github.com/Trollz1004/ANTIGRAVITY) | `infra/claude-desktop/claude_desktop_config.json` | 8 (brain-mcp, antigravity-sentry, paperclip +5 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 147 | [Denyme24/CaseCanopy](https://github.com/Denyme24/CaseCanopy) | `mcp_server/claude_desktop_config.json` | 1 (case-canopy-legal) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-case-canopy-legal-OPENAI_API_KEY` |
| 148 | [aksdevops/PlaywrightMCP](https://github.com/aksdevops/PlaywrightMCP) | `agent/mcp-configs/claude_desktop_config.json` | 1 (playwright) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 149 | [jadecli/platform-manager](https://github.com/jadecli/platform-manager) | `bootstrap/claude-config/claude-desktop/claude_desktop_config.json` | 4 (filesystem, github, memory +1 more) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 150 | [alongor666/daylyreport](https://github.com/alongor666/daylyreport) | `归档文件/claude_desktop_config.json` | 3 (filesystem, excel, excel-python) | 0 | 1 | 4 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-filesystem`; MEDIUM: `CONTEXT-EXT-FETCH-excel-python` |
| 151 | [lo-ucif/market-web](https://github.com/lo-ucif/market-web) | `frontend/claude_desktop_config.json` | 1 (filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 152 | [Iridium40/roam-platform](https://github.com/Iridium40/roam-platform) | `claude_desktop_config.json` | 2 (twilio, resend) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-resend-RESEND_API_KEY` |
| 153 | [emsi/MyManus](https://github.com/emsi/MyManus) | `windows_claude_desktop_config.json` | 3 (@automatalabs-mcp-server-playwright, sandbox, filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 154 | [zzkoro/newdawn-repos](https://github.com/zzkoro/newdawn-repos) | `study03/week02/claude_desktop_config.json.sample` | 7 (Demo, Echo, ElevenLabs +4 more) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-ElevenLabs-ELEVENLABS_API_KEY` |
| 155 | [wplaunchify/fluent-community-mcp](https://github.com/wplaunchify/fluent-community-mcp) | `claude_desktop_config.json.example` | 1 (wordpress) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-wordpress-WORDPRESS_PASSWORD` |
| 156 | [JasonFLee/jason-ai-toolkit](https://github.com/JasonFLee/jason-ai-toolkit) | `configs/claude-desktop/claude_desktop_config.json.example` | 1 (n8n-mcp) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-n8n-mcp-workflow-execution` |
| 157 | [IntuitivePhella/mcp-evolution-api](https://github.com/IntuitivePhella/mcp-evolution-api) | `examples/claude_desktop_config.json` | 1 (evolution-api) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-evolution-api-EVOLUTION_API_KEY` |
| 158 | [patakuti/local-knowledge-rag-mcp](https://github.com/patakuti/local-knowledge-rag-mcp) | `examples/claude_desktop_config.json` | 1 (local-knowledge-rag) | 0 | 1 | 3 | 25 | HIGH: `CONN-STRING-ENV-local-knowledge-rag-DATABASE_URL`; MEDIUM: `CONTEXT-EXT-FETCH-local-knowledge-rag` |
| 159 | [yannabadie/bulleoapp-gcp-mcp](https://github.com/yannabadie/bulleoapp-gcp-mcp) | `mcp-config/claude_desktop_config.json` | 2 (firebase-bulleoapp, gcp-vertex-ai) | 0 | 1 | 3 | 25 | MEDIUM: `CONTEXT-EXT-FETCH-firebase-bulleoapp`; HIGH: `ENV-SECRET-gcp-vertex-ai-GOOGLE_APPLICATION_CREDENTIALS` |
| 160 | [ajeetraina/talk-demos](https://github.com/ajeetraina/talk-demos) | `mcp-demo/postgres/claude_desktop_config.json` | 1 (postgres) | 0 | 1 | 2 | 25 | HIGH: `CONN-STRING-ARGS-postgres` |
| 161 | [alidurmus/kalite-kontrol](https://github.com/alidurmus/kalite-kontrol) | `claude_desktop_config.json` | 1 (ElevenLabs) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-ElevenLabs-ELEVENLABS_API_KEY` |
| 162 | [BrooksIan/SSB-MCP-Server](https://github.com/BrooksIan/SSB-MCP-Server) | `claude_desktop_config.json` | 2 (apache-flink, ssb-mcp-server) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-ssb-mcp-server-KNOX_TOKEN` |
| 163 | [tkhongsap/mcp-concept](https://github.com/tkhongsap/mcp-concept) | `config/claude_desktop_config.json` | 2 (nws-weather, playwright) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation` |
| 164 | [agam04/mcp-postgres-toolkit](https://github.com/agam04/mcp-postgres-toolkit) | `claude_desktop_config.json` | 1 (postgres) | 0 | 1 | 2 | 25 | HIGH: `CONN-STRING-ENV-postgres-MCP_PG_DATABASE_URL` |
| 165 | [AbuMareBear/dotfiles](https://github.com/AbuMareBear/dotfiles) | `claude_desktop_config.json` | 1 (filesystem) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-filesystem-filesystem` |
| 166 | [Aayushchaudry/MCP_gmail](https://github.com/Aayushchaudry/MCP_gmail) | `claude_desktop_config.json` | 1 (gmail_mcp_server) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-gmail_mcp_server-GOOGLE_APPLICATION_CREDENTIALS` |
| 167 | [elvmalrds/vtiger-mcp-server](https://github.com/elvmalrds/vtiger-mcp-server) | `claude_desktop_config.json` | 1 (vtiger) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-vtiger-VTIGER_ACCESS_KEY` |
| 168 | [B0LK13/obsidian-agent](https://github.com/B0LK13/obsidian-agent) | `obsidian-agent-apps/obsidian-mcp/claude_desktop_config.json` | 1 (obsidian) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-obsidian-OBSIDIAN_API_TOKEN` |
| 169 | [hellotinah/MCP](https://github.com/hellotinah/MCP) | `claude_desktop_config.json` | 1 (gsheets) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-gsheets-GOOGLE_CREDENTIALS_PATH` |
| 170 | [Tai-DT/mcp-ui-expo-tamagui](https://github.com/Tai-DT/mcp-ui-expo-tamagui) | `claude_desktop_config.json` | 1 (mcp-ui-expo-tamagui) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-mcp-ui-expo-tamagui-GEMINI_API_KEY` |
| 171 | [Web4application/pilot_ai](https://github.com/Web4application/pilot_ai) | `Mcp.json` | 1 (github) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-github-source-control` |
| 172 | [dlstudiodev/bb-backend](https://github.com/dlstudiodev/bb-backend) | `.mcp.json` | 1 (supabase) | 0 | 1 | 2 | 25 | HIGH: `ENV-SECRET-supabase-SUPABASE_ACCESS_TOKEN` |
| 173 | [jtuttas/Softwareentwicklung_KI](https://github.com/jtuttas/Softwareentwicklung_KI) | `.mcp.json` | 2 (sqlite, playwright) | 0 | 1 | 2 | 25 | HIGH: `DANGEROUS-PKG-playwright-browser-automation` |

### MEDIUM Configs (952)

| # | Repo | Config Path | Servers | C | H | M | Risk | Notable Findings |
|---|---|---|---|---|---|---|---|---|
| 1 | [confluentinc/mcp-confluent](https://github.com/confluentinc/mcp-confluent) | `example.claude_desktop_config.json` | 1 (confluent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 2 | [rifaterdemsahin/mcp](https://github.com/rifaterdemsahin/mcp) | `symbol_claude_desktop_config.json` | 1 (python-runner) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 3 | [yk-takemoto/smarthome-agent-mcp](https://github.com/yk-takemoto/smarthome-agent-mcp) | `packages/devctl_server/claude_desktop_config.json.template` | 1 (devctl_server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 4 | [tom-miy/dotfiles](https://github.com/tom-miy/dotfiles) | `home/dot_config/claude/claude_desktop_config.json.tmpl` | 2 (context7, awslabs.aws-documentation-mcp-server) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-INJECT-context7` |
| 5 | [Dezocode/mcp-system](https://github.com/Dezocode/mcp-system) | `configs/claude_desktop_config.json.backup.1755278943` | 1 (mcp-system) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 6 | [Yazaven/CloudThrift](https://github.com/Yazaven/CloudThrift) | `claude_desktop_config.json.example` | 2 (cloudthrift-demo, cloudthrift) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 7 | [timothywarner-org/context-engineering](https://github.com/timothywarner-org/context-engineering) | `config/claude_desktop_config.json` | 1 (warnerco-schematica) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 8 | [akornmeier/dotfiles](https://github.com/akornmeier/dotfiles) | `claude/claude_desktop_config.json.template` | 1 (sequential-thinking) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 9 | [dujiepeng/easemob-mcp-server](https://github.com/dujiepeng/easemob-mcp-server) | `claude_desktop_config.json` | 1 (easemob-im-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 10 | [start-trek/Obsidian-Spec-MCP](https://github.com/start-trek/Obsidian-Spec-MCP) | `examples/claude_desktop_config.json` | 1 (obsidian-spec) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 11 | [Dr-xu193/claude-desktop-deepseek-use](https://github.com/Dr-xu193/claude-desktop-deepseek-use) | `claude_desktop_config.json` | 3 (github, wsl-exec, browser-use) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 12 | [hsp1978/stock_ai](https://github.com/hsp1978/stock_ai) | `claude_desktop_config.json` | 1 (stock-ai) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 13 | [jheun66/aladin-book-recommendation](https://github.com/jheun66/aladin-book-recommendation) | `claude_desktop_config.json` | 1 (aladin) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 14 | [jeannier/homebrew-mcp](https://github.com/jeannier/homebrew-mcp) | `claude_desktop_config.json` | 1 (homebrew-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 15 | [curdx/coding-simple-mcp](https://github.com/curdx/coding-simple-mcp) | `claude_desktop_config.json` | 1 (coding-simple-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 16 | [andrei-shtanakov/arbiter](https://github.com/andrei-shtanakov/arbiter) | `config/claude_desktop_config.json` | 1 (arbiter) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 17 | [getnimbus/spice](https://github.com/getnimbus/spice) | `claude_desktop_config.json` | 1 (spice) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 18 | [E-equals-mcsquare/ai_architecture_governance_agent](https://github.com/E-equals-mcsquare/ai_architecture_governance_agent) | `sample_claude_desktop_config.json` | 9 (aws-api-gateway, aws-lambda, aws-ses +6 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 19 | [kanishka-namdeo/spec-architect](https://github.com/kanishka-namdeo/spec-architect) | `config/claude_desktop_config.json` | 1 (spec-architect) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 20 | [bpsarthur/proxmark-mcp](https://github.com/bpsarthur/proxmark-mcp) | `examples/claude_desktop_config.json` | 1 (proxmark3) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 21 | [Niwa-Yume/Crypto-MCP-api-CoinTelegraph](https://github.com/Niwa-Yume/Crypto-MCP-api-CoinTelegraph) | `claude_desktop_config.json` | 1 (crypto-leaderboard) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 22 | [adii9/Agent-Makr1](https://github.com/adii9/Agent-Makr1) | `claude_desktop_config.json` | 1 (github-mcp-agent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 23 | [umermansoor/lever-ats-mcp](https://github.com/umermansoor/lever-ats-mcp) | `claude_desktop_config.json` | 1 (lever-ats) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 24 | [TheTam2703/Pet-Hospital-System-Demo-OOP-Project-2026-](https://github.com/TheTam2703/Pet-Hospital-System-Demo-OOP-Project-2026-) | `claude_desktop_config.json` | 1 (PetHospital) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 25 | [randygiorgio-pixel/Giorgio4](https://github.com/randygiorgio-pixel/Giorgio4) | `claude_desktop_config.json` | 6 (supabase, slack, composio +3 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 26 | [EthelEz/mcp_fhir_integration](https://github.com/EthelEz/mcp_fhir_integration) | `claude_desktop_config.json` | 1 (fhir-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 27 | [anatoly314/mcp-server-starter](https://github.com/anatoly314/mcp-server-starter) | `claude_desktop_config.json` | 1 (mcp-server-starter) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 28 | [anteriovieira/osc-mcp-server](https://github.com/anteriovieira/osc-mcp-server) | `claude_desktop_config.json` | 1 (osc) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 29 | [vignankamarthi/Claude-Parallel-AI-Bridge](https://github.com/vignankamarthi/Claude-Parallel-AI-Bridge) | `claude_desktop_config.json.example` | 1 (parallel-research) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 30 | [mnthe/claude-agent-mcp-server](https://github.com/mnthe/claude-agent-mcp-server) | `claude_desktop_config.json.example` | 1 (claude-agent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 31 | [metinuslu/mcp-demonstration](https://github.com/metinuslu/mcp-demonstration) | `cfg/claude_desktop_config.json` | 5 (weather, Stock Price Server, Stock Price Server-2 +2 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 32 | [VIKAS9793/AndroJack-mcp](https://github.com/VIKAS9793/AndroJack-mcp) | `config/claude_desktop_config.json` | 1 (androjack) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 33 | [IngeniousIdiocy/Consumer-Complaint-Database-MCP](https://github.com/IngeniousIdiocy/Consumer-Complaint-Database-MCP) | `claude_desktop_config.json` | 1 (Banking Complaints) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 34 | [kazunori-Ohashi/MCP-ndl-search](https://github.com/kazunori-Ohashi/MCP-ndl-search) | `claude_desktop_config.json` | 1 (ndl-search) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 35 | [swa34/snarky-devil-mcp](https://github.com/swa34/snarky-devil-mcp) | `claude_desktop_config.json` | 1 (snarky-devil) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 36 | [Lawiak/docker-mcp-raspi](https://github.com/Lawiak/docker-mcp-raspi) | `config/claude_desktop_config.json` | 1 (docker-server-raspi) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 37 | [timowhite88/Farnsworth](https://github.com/timowhite88/Farnsworth) | `claude_desktop_config.json.example` | 1 (farnsworth) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 38 | [QuocHiep123/english-speaking-app](https://github.com/QuocHiep123/english-speaking-app) | `mcp/claude_desktop_config.json` | 1 (vietspeak-pronunciation) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 39 | [haasonsaas/claude-code-browser-mcp-setup](https://github.com/haasonsaas/claude-code-browser-mcp-setup) | `claude_desktop_config.json` | 1 (chrome-devtools) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 40 | [eka-care/eka-mcp-sdk](https://github.com/eka-care/eka-mcp-sdk) | `examples/claude_desktop_config.json` | 1 (eka-care) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 41 | [tonyredondo/debugger-mcp-server](https://github.com/tonyredondo/debugger-mcp-server) | `claude_desktop_config.json` | 3 (debugger-local, debugger-remote, debugger-docker) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 42 | [Titration/MCP_demo](https://github.com/Titration/MCP_demo) | `config/claude_desktop_config.json` | 1 (my-api-mcp-proxy) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 43 | [ismailkerimov/math-logic-mcp](https://github.com/ismailkerimov/math-logic-mcp) | `deploy/claude_desktop_config.json` | 1 (math-logic) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 44 | [Vintaragroup/PL-MCP](https://github.com/Vintaragroup/PL-MCP) | `claude_desktop_config.json` | 1 (frontend-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 45 | [sumitrevolt/flash-loan-arbitrage-system](https://github.com/sumitrevolt/flash-loan-arbitrage-system) | `config/claude_desktop_config.json` | 7 (flash-loan-arbitrage, flash-loan-system, minimal-flash-loan +4 more) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-flash-loan-arbitrage` |
| 46 | [luanntd/2A202600204-Day26-Track3](https://github.com/luanntd/2A202600204-Day26-Track3) | `config/claude_desktop_config.json` | 1 (sales-db) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 47 | [Herwi/gtavbrowser-mcp](https://github.com/Herwi/gtavbrowser-mcp) | `examples/claude_desktop_config.json` | 1 (gtavbrowser) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 48 | [Burton-David/ResearchAssistantMCP](https://github.com/Burton-David/ResearchAssistantMCP) | `examples/claude_desktop_config.json` | 1 (research-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 49 | [MarvinHauke/dotfiles-mcp](https://github.com/MarvinHauke/dotfiles-mcp) | `examples/claude_desktop_config.json` | 1 (dotfiles) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 50 | [hhauschild/camunda-mcp-server](https://github.com/hhauschild/camunda-mcp-server) | `examples/claude_desktop_config.json` | 1 (camunda-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 51 | [mlobo2012/Claude_Desktop_API_USE_VIA_MCP](https://github.com/mlobo2012/Claude_Desktop_API_USE_VIA_MCP) | `claude_desktop_config.json` | 1 (claude-api) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 52 | [boregan/PaceTrace](https://github.com/boregan/PaceTrace) | `claude_desktop_config.json.example` | 1 (pacetrace) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 53 | [hkshitesh/MCP-SERVER-DS](https://github.com/hkshitesh/MCP-SERVER-DS) | `claude_desktop_config.json` | 1 (my-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 54 | [asccclass/kanbanX](https://github.com/asccclass/kanbanX) | `claude_desktop_config.json` | 1 (kanbanx) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 55 | [rjamoriz/Sistema-Corporativo-Documental-con-Capacidades-de-IA](https://github.com/rjamoriz/Sistema-Corporativo-Documental-con-Capacidades-de-IA) | `claude_desktop_config.json` | 1 (tefinancia-ontology) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 56 | [damon-williams/fairydust](https://github.com/damon-williams/fairydust) | `claude_desktop_config.json` | 1 (fairydust) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 57 | [o-ouma/gcp-mcp](https://github.com/o-ouma/gcp-mcp) | `claude_desktop_config.json` | 1 (github_ops) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 58 | [solace1221/digital-twin-nextjs](https://github.com/solace1221/digital-twin-nextjs) | `claude_desktop_config.json` | 4 (digital-twin-lovely, bootcamp-rag, tech-bootcamp-consultations +1 more) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-bootcamp-rag` |
| 59 | [MOHAMMEDFAISALSM/mcp-multi-agent-claude](https://github.com/MOHAMMEDFAISALSM/mcp-multi-agent-claude) | `claude_desktop_config.json` | 1 (multi-agent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 60 | [yz174/MCP-server-](https://github.com/yz174/MCP-server-) | `claude_desktop_config.json` | 1 (educhain-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 61 | [CNDvn/dbhubMCP](https://github.com/CNDvn/dbhubMCP) | `claude_desktop_config.json` | 1 (dbhub) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 62 | [Rushalkraj/mcp_ibmi](https://github.com/Rushalkraj/mcp_ibmi) | `claude_desktop_config.json` | 1 (buildmate-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 63 | [faith-tools/daily-verse-mcp](https://github.com/faith-tools/daily-verse-mcp) | `claude_desktop_config.json` | 1 (prayer-verse-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 64 | [Devashis7/springAI-mcp](https://github.com/Devashis7/springAI-mcp) | `claude_desktop_config.json` | 2 (spring-mcp, employee-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 65 | [Letiiciia/tarologa-calil-services](https://github.com/Letiiciia/tarologa-calil-services) | `claude_desktop_config.json` | 1 (tarologa-calil) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 66 | [Lochan09/Employee-task-manager-using-MCP-with-CLAUDE](https://github.com/Lochan09/Employee-task-manager-using-MCP-with-CLAUDE) | `claude_desktop_config.json` | 1 (task-management) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 67 | [alperduzgun/flutter-mcpilot-server](https://github.com/alperduzgun/flutter-mcpilot-server) | `claude_desktop_config.json` | 1 (flutter-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 68 | [dschuler36/reaper-mcp-server](https://github.com/dschuler36/reaper-mcp-server) | `setup/claude_desktop_config.json` | 1 (reaper) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 69 | [contextform/freecad-mcp](https://github.com/contextform/freecad-mcp) | `config/claude_desktop_config.json` | 1 (freecad-copilot) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 70 | [hitanshu-dhawan/Model-Context-Protocol-Playground](https://github.com/hitanshu-dhawan/Model-Context-Protocol-Playground) | `weather-server/claude_desktop_config.json` | 1 (weather-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 71 | [finstacklabs/finstack-mcp](https://github.com/finstacklabs/finstack-mcp) | `claude_desktop_config.json.example` | 1 (finstack) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 72 | [matthewhand/mcp-openapi-proxy](https://github.com/matthewhand/mcp-openapi-proxy) | `examples/elevenlabs-claude_desktop_config.json` | 1 (elevenlabs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 73 | [Life-Ambassadors-International/TEQUMSA_EMERGE](https://github.com/Life-Ambassadors-International/TEQUMSA_EMERGE) | `configuration/windows_claude_desktop_config.json` | 4 (tequmsa-quantum, tequmsa-consciousness, tequmsa-self-recognizing +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 74 | [mangopudding/mcp-server-knowbe4-graphql-api](https://github.com/mangopudding/mcp-server-knowbe4-graphql-api) | `config/claude_desktop_config.json.example` | 1 (knowbe4-graphql) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 75 | [brunoborges/jvm-diagnostics-mcp](https://github.com/brunoborges/jvm-diagnostics-mcp) | `claude_desktop_config.json` | 1 (jvm-diagnostics) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 76 | [saasus-platform/saasus-api-mcp-server](https://github.com/saasus-platform/saasus-api-mcp-server) | `claude/claude_desktop_config.json` | 1 (saasusapis) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 77 | [OMCHOKSI108/MCP-SERVER](https://github.com/OMCHOKSI108/MCP-SERVER) | `MCP_6/claude_desktop_config.json` | 1 (excalidraw) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 78 | [wwwzhouhui/jimeng-mcp-server](https://github.com/wwwzhouhui/jimeng-mcp-server) | `claude_desktop_config.json` | 1 (jimeng) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 79 | [FeiWangHub/playground](https://github.com/FeiWangHub/playground) | `ai-playground/harry-potter-api/openAPI-nodejs-mcp-server/example_js_claude_desktop_config.json` | 1 (harry-nodejs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 80 | [fuzzylabs/apollo-mcp](https://github.com/fuzzylabs/apollo-mcp) | `claude_desktop_config.json` | 1 (apollo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 81 | [Prounckk/mcp-skills-agents](https://github.com/Prounckk/mcp-skills-agents) | `mcp/youtrack-js/claude_desktop_config.json.example` | 2 (youtrack, _youtrack_explicit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 82 | [keides2/roam-research-mcp-setup-guide](https://github.com/keides2/roam-research-mcp-setup-guide) | `config/claude_desktop_config.json.example` | 1 (roam-research) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 83 | [xch1tbllc/storm-mcp](https://github.com/xch1tbllc/storm-mcp) | `examples/claude_desktop_config.json` | 1 (storm) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 84 | [weniv/mcp_book_source](https://github.com/weniv/mcp_book_source) | `ko/2.3/claude_desktop_config.json` | 3 (tutorial_1, tutorial_2, tutorial_3) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 85 | [lamemind/mcp-coding-server-demo-app](https://github.com/lamemind/mcp-coding-server-demo-app) | `mcp-server/claude_desktop_config.json` | 2 (filesystem, git) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 86 | [sulaiman013/Fabric-SQL-Assistant](https://github.com/sulaiman013/Fabric-SQL-Assistant) | `claude_desktop_config.json` | 1 (fabric-sql-assistant) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 87 | [wsekete/pybaseball-MCP](https://github.com/wsekete/pybaseball-MCP) | `claude_desktop_config.json` | 1 (pybaseball) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 88 | [Emilio-Ramirez/Dotfiles](https://github.com/Emilio-Ramirez/Dotfiles) | `Claude/claude_desktop_config.json` | 1 (shadcn-ui) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 89 | [irinabuht12-oss/google-meta-ads-ga4-mcp](https://github.com/irinabuht12-oss/google-meta-ads-ga4-mcp) | `configs/claude_desktop_config.json` | 1 (google-meta-ads-ga4) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 90 | [Jonathan97480/McpHomeAssistant](https://github.com/Jonathan97480/McpHomeAssistant) | `examples/claude_desktop_config.json` | 1 (homeassistant) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 91 | [seggit/tempo-mcp-server](https://github.com/seggit/tempo-mcp-server) | `examples/claude_desktop_config.json` | 1 (tempo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 92 | [isaqueseneda/central-44](https://github.com/isaqueseneda/central-44) | `mcp/claude_desktop_config.json` | 1 (central44) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 93 | [awee1453/RSS-MCP](https://github.com/awee1453/RSS-MCP) | `configs/claude_desktop_config.json` | 1 (rss-news) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 94 | [kusibehan/SQLAny_DelphiMCP](https://github.com/kusibehan/SQLAny_DelphiMCP) | `DelphiMCP/claude_desktop_config.json` | 1 (CalculatorService) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 95 | [tizee/dotfiles](https://github.com/tizee/dotfiles) | `claude/claude_desktop_config.json` | 6 (unix-manual, fetch, ietf-doc +3 more) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-fetch` |
| 96 | [gornskew/skewed-emacs](https://github.com/gornskew/skewed-emacs) | `mcp/claude_desktop_config.json` | 6 (genworks-gdl-enterprise-non-smp, genworks-gdl-enterprise-smp, cyclops +3 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 97 | [PedroGiudice/lex-vector](https://github.com/PedroGiudice/lex-vector) | `legal-workbench/ferramentas/trello-mcp/configs/claude_desktop_config.json` | 1 (trello) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 98 | [xun123456/jlink-mcp](https://github.com/xun123456/jlink-mcp) | `claude_desktop_config.json` | 1 (jlink-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 99 | [RubenReyesss/mcp-nlp-analytics](https://github.com/RubenReyesss/mcp-nlp-analytics) | `config/claude_desktop_config.json` | 1 (sentiment-tracker) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 100 | [kuaizhongqiang/AgentRouter](https://github.com/kuaizhongqiang/AgentRouter) | `agents/continue/manual-testing-sandbox/claude_desktop_config.json` | 1 (linear) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 101 | [varunkumar/lightroom-mcp](https://github.com/varunkumar/lightroom-mcp) | `claude_desktop_config.json` | 1 (lightroom) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 102 | [makeralchemy/claude-desktop-mcp-sqlite](https://github.com/makeralchemy/claude-desktop-mcp-sqlite) | `claude_desktop_config.json` | 1 (sqlite) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 103 | [okisnateamdev7/Ecoskiller](https://github.com/okisnateamdev7/Ecoskiller) | `Operations-20260324T064152Z-3-001/Operations/Mcp-Server/Job_Service/Job_Service/claude_desktop_config.json` | 1 (ecoskiller-job-service) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 104 | [Luney-Industries/farty-bobo](https://github.com/Luney-Industries/farty-bobo) | `claude-desktop/claude_desktop_config.json` | 7 (linear, dbt, awslabs.redshift-mcp-server +4 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 105 | [agiletortoise/drafts-mcp-server](https://github.com/agiletortoise/drafts-mcp-server) | `Support/Claude/claude_desktop_config.json` | 1 (drafts) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 106 | [ForAllSecure/mcp-server-mapi](https://github.com/ForAllSecure/mcp-server-mapi) | `claude_desktop_config.json` | 1 (mapi) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 107 | [Newton4Gravity/SwiftCoderMCP](https://github.com/Newton4Gravity/SwiftCoderMCP) | `claude_desktop_config.json` | 1 (swift-coder) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 108 | [ly2xxx/aisoft](https://github.com/ly2xxx/aisoft) | `mcp/claude_desktop_config.json` | 3 (claude-code-developer, gemini-qa-agent, MCP_DOCKER) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 109 | [gHashTag/trinity](https://github.com/gHashTag/trinity) | `deploy/trinity-nexus/tools/mcp/claude_desktop_config.json` | 1 (igla-swe-agent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 110 | [jiayuwee/advanced-tools-navigation](https://github.com/jiayuwee/advanced-tools-navigation) | `config/development/claude_desktop_config.json` | 1 (context7) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-INJECT-context7` |
| 111 | [insinuateai/prova-mcp](https://github.com/insinuateai/prova-mcp) | `examples/claude_desktop_config.json` | 1 (prova) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 112 | [bdc-miteshb/Cognixia--GenAI-GCP-](https://github.com/bdc-miteshb/Cognixia--GenAI-GCP-) | `Week_7_labs/Lab - MCP_server/claude_desktop_config.json` | 1 (local-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 113 | [vincent119/VictoriaLogs-mcp](https://github.com/vincent119/VictoriaLogs-mcp) | `configs/claude_desktop_config.json` | 1 (victorialogs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 114 | [weniv/mcp_book_source](https://github.com/weniv/mcp_book_source) | `en/2.2/claude_desktop_config.json` | 2 (tutorial_1, tutorial_2) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 115 | [mekanixms/sqlite-mcp-server](https://github.com/mekanixms/sqlite-mcp-server) | `claude_desktop_config.json` | 1 (sqlite_mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 116 | [ntanwir10/codesage-algolia-challenge](https://github.com/ntanwir10/codesage-algolia-challenge) | `claude_desktop_config.json` | 1 (codesage-mcp-first) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 117 | [russell-qca/sketchup-mcp](https://github.com/russell-qca/sketchup-mcp) | `claude_desktop_config.json` | 1 (sketchup) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 118 | [msaltnet/excel-search-mcp](https://github.com/msaltnet/excel-search-mcp) | `claude_desktop_config.json` | 1 (excel-search-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 119 | [Micka33/ask_scientist](https://github.com/Micka33/ask_scientist) | `config/claude_desktop_config.json` | 1 (ask_scientist) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 120 | [KalininGroup/mic_hackathon_2](https://github.com/KalininGroup/mic_hackathon_2) | `projects/H-059/code/claude_desktop_config.json` | 1 (ferrosim) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 121 | [hakilee/opencode-mcp-bridge](https://github.com/hakilee/opencode-mcp-bridge) | `examples/claude_desktop_config.json` | 1 (opencode) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 122 | [yoitsyoung/yt-dlp-mcp](https://github.com/yoitsyoung/yt-dlp-mcp) | `claude_desktop_config.json` | 1 (youtube) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-youtube` |
| 123 | [carquiza/RoslynMCP](https://github.com/carquiza/RoslynMCP) | `claude_desktop_config.json` | 1 (roslyn-code-navigator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 124 | [nanocentury-ai/supersimpleMCP](https://github.com/nanocentury-ai/supersimpleMCP) | `claude_desktop_config.json` | 1 (simple-character-counter) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 125 | [format37/ssh-mcp](https://github.com/format37/ssh-mcp) | `claude_desktop_config.json` | 1 (ssh) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 126 | [spboyer/slidemaker](https://github.com/spboyer/slidemaker) | `docs/mcp-configs/claude_desktop_config.json` | 1 (slidemaker) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 127 | [gHashTag/trios-mcp](https://github.com/gHashTag/trios-mcp) | `examples/claude_desktop_config.json` | 1 (trios) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 128 | [EvezArt/evez-platform](https://github.com/EvezArt/evez-platform) | `plugin/claude_desktop_config.json` | 1 (evez) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 129 | [niradler/dependency-mcp](https://github.com/niradler/dependency-mcp) | `claude_desktop_config.json` | 1 (dependency-checker) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 130 | [Abdullah-Maqbool1/web-action-gateway](https://github.com/Abdullah-Maqbool1/web-action-gateway) | `claude_desktop_config.json` | 1 (web-action-gateway) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 131 | [cleozhang-symplectic/ai-hackday-2025](https://github.com/cleozhang-symplectic/ai-hackday-2025) | `claude_desktop_config.json` | 1 (expense-tracker) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 132 | [happycastle114/dorico-mcp-server](https://github.com/happycastle114/dorico-mcp-server) | `examples/claude_desktop_config.json` | 1 (dorico) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 133 | [IBM/chuk-mcp-open-meteo](https://github.com/IBM/chuk-mcp-open-meteo) | `examples/claude_desktop_config.json` | 1 (open-meteo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 134 | [mubashir1osmani/litellm-mcp](https://github.com/mubashir1osmani/litellm-mcp) | `claude_desktop_config.json` | 1 (litellm) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 135 | [aravinditte/japanese-language-mcp](https://github.com/aravinditte/japanese-language-mcp) | `claude_desktop_config.json` | 1 (japanese-language-tools) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 136 | [happyren/mcp-servers](https://github.com/happyren/mcp-servers) | `telegram_mcp_server/claude_desktop_config.json` | 1 (telegram-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 137 | [deepakjd2004/akamai-mcp-server](https://github.com/deepakjd2004/akamai-mcp-server) | `claude_desktop_config.json` | 2 (tfmcp, akamai) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 138 | [aidenmak0624/HR-Intelligence-platform](https://github.com/aidenmak0624/HR-Intelligence-platform) | `claude_desktop_config.json` | 2 (hr-agent-platform, bamboohr) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 139 | [Reneromero08/agent-governance-system](https://github.com/Reneromero08/agent-governance-system) | `CAPABILITY/MCP/claude_desktop_config.json` | 1 (ags) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 140 | [FelipeMira/device-automation-ia](https://github.com/FelipeMira/device-automation-ia) | `config/claude_desktop_config.json` | 1 (agent-device) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 141 | [josedab/needle](https://github.com/josedab/needle) | `examples/claude_desktop_config.json` | 1 (needle) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-needle` |
| 142 | [drquandary/mcp-academic-editor](https://github.com/drquandary/mcp-academic-editor) | `examples/claude_desktop_config.json` | 1 (academic-editor) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 143 | [sujayshah3011/devcontext](https://github.com/sujayshah3011/devcontext) | `agent/claude_desktop_config.json` | 3 (devcontext-github, devcontext-codebase, devcontext-journal) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 144 | [silkyclouds/PMDA](https://github.com/silkyclouds/PMDA) | `integrations/pmda-agent-toolkit/examples/claude_desktop_config.json` | 1 (pmda) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 145 | [mlanini/kadas-ai-integration](https://github.com/mlanini/kadas-ai-integration) | `examples/claude_desktop_config.json` | 6 (kadas-map, kadas-geodata, kadas-analysis +3 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 146 | [kiskander/mcp-splunk-meraki](https://github.com/kiskander/mcp-splunk-meraki) | `claude_desktop_config.json` | 2 (splunk, meraki) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 147 | [sparesparrow/rust-network-mgr](https://github.com/sparesparrow/rust-network-mgr) | `mcp-config/claude_desktop_config.json` | 1 (network-mgr) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 148 | [opazyniuk/ai-engineering](https://github.com/opazyniuk/ai-engineering) | `hw/hw016/claude_desktop_config.json` | 1 (mavka-nova) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 149 | [daugustin/icinga2-mcp](https://github.com/daugustin/icinga2-mcp) | `examples/claude_desktop_config.json` | 1 (icinga2) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 150 | [okisnateamdev7/Ecoskiller](https://github.com/okisnateamdev7/Ecoskiller) | `Operations-20260324T064152Z-3-001/Operations/Mcp-Server/mcp-skill-evaluation-engine/mcp-skill-evaluation-engine/claude_desktop_config.json` | 1 (mcp-skill-evaluation-engine) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 151 | [Spydrcode/local-ai](https://github.com/Spydrcode/local-ai) | `mcp-server/claude_desktop_config.json` | 1 (local-ai) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 152 | [kimghw/KR365](https://github.com/kimghw/KR365) | `entrypoints/configs/local/claude_desktop_config.json` | 6 (mail-query-server, enrollment-server, onenote-server +3 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 153 | [ReexpressAI/reexpress_labs](https://github.com/ReexpressAI/reexpress_labs) | `labs/ibm/code/mcp_v2_preview/setup/claude_desktop_config.json` | 1 (reexpress) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 154 | [Jktfe/serveMyAPI](https://github.com/Jktfe/serveMyAPI) | `examples/claude_desktop_config.json` | 1 (serveMyAPI) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 155 | [Akhilucky/EquationX](https://github.com/Akhilucky/EquationX) | `mcp-config/claude_desktop_config.json` | 1 (equationx) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 156 | [edujbarrios/multi-api-bench-mcp](https://github.com/edujbarrios/multi-api-bench-mcp) | `claude_desktop_config.json` | 1 (multi-api-bench) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 157 | [KubeDev/maratona-devops-ia](https://github.com/KubeDev/maratona-devops-ia) | `03-ia/claude_desktop_config.json` | 3 (filesystem, kubernetes, prometheus) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 158 | [keshavjha123/DockerhubMCP](https://github.com/keshavjha123/DockerhubMCP) | `claude_desktop_config.json` | 1 (dockerhub) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 159 | [Garblesnarff/gemini-mcp-server](https://github.com/Garblesnarff/gemini-mcp-server) | `examples/claude_desktop_config.json` | 1 (gemini-image) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 160 | [dkuwcreator/azure-mcp-python](https://github.com/dkuwcreator/azure-mcp-python) | `examples/claude_desktop_config.json` | 1 (azure) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 161 | [xupeiwust/AutoEDA11](https://github.com/xupeiwust/AutoEDA11) | `src/server/mcp/claude_desktop_config.json` | 1 (mcp-eda-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 162 | [tyson-swetnam/epihack-2026](https://github.com/tyson-swetnam/epihack-2026) | `mcp/inaturalist-mcp/examples/claude_desktop_config.json` | 1 (inaturalist) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 163 | [Jiraiya8/memos-mcp](https://github.com/Jiraiya8/memos-mcp) | `examples/claude_desktop_config.json` | 1 (memos) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 164 | [okisnateamdev7/Ecoskiller](https://github.com/okisnateamdev7/Ecoskiller) | `Operations-20260324T064152Z-3-001/Operations/Mcp-Server/royalty-ledger-mcp-server/royalty-ledger-mcp-server (1)/claude_desktop_config.json` | 1 (mcp-royalty-ledger-ecoskiller) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 165 | [AbrahamOO/senior-design-director-mcp](https://github.com/AbrahamOO/senior-design-director-mcp) | `Support/Claude/claude_desktop_config.json` | 1 (senior-design-director) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 166 | [temporalio/edu-durable-mcp-tutorial-template](https://github.com/temporalio/edu-durable-mcp-tutorial-template) | `claude_desktop_config.json` | 1 (weather) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 167 | [Skyfall-Research/world-of-workflows](https://github.com/Skyfall-Research/world-of-workflows) | `submodules/servicenow-mcp/examples/claude_desktop_config.json` | 1 (servicenow) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 168 | [eatenbywo1ves/studious-chainsaw](https://github.com/eatenbywo1ves/studious-chainsaw) | `development/mcp/config/claude_desktop_config.json` | 6 (catalytic-deployment, catalytic-github, catalytic-slack +3 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 169 | [JosephLin11/jupyter-mcp-server](https://github.com/JosephLin11/jupyter-mcp-server) | `examples/claude_desktop_config.json` | 1 (jupyter) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 170 | [carrell-ncl/football-news-agent](https://github.com/carrell-ncl/football-news-agent) | `mcp_dev/claude_desktop_config.json` | 1 (football) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 171 | [dev-eloper-365/NeerSetuFinale](https://github.com/dev-eloper-365/NeerSetuFinale) | `claude_desktop_config.json` | 1 (vercel) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 172 | [iddv/mcp-example](https://github.com/iddv/mcp-example) | `examples/configs/claude_desktop_config.json` | 2 (basic-example, filesystem) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 173 | [akirapham/mcptrustmap](https://github.com/akirapham/mcptrustmap) | `examples/configs/claude_desktop_config.json` | 2 (files, weather) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 174 | [adi2355/MCP-Resume-Editor](https://github.com/adi2355/MCP-Resume-Editor) | `claude_desktop_config.json` | 2 (LibreOfficeResumeEditor, JDKeywordExtractor) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 175 | [ankurxbatta/AI-driven-penetration-testing](https://github.com/ankurxbatta/AI-driven-penetration-testing) | `claude_desktop_config.json` | 2 (kali-pentest, MCP_DOCKER) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 176 | [SonnyC56/openroad](https://github.com/SonnyC56/openroad) | `claude_desktop_config.json` | 1 (puppeteer) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-puppeteer` |
| 177 | [armand0e/perplexica-mcp](https://github.com/armand0e/perplexica-mcp) | `examples/claude_desktop_config.json` | 1 (perplexica) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 178 | [geneialco/synTOPia-data-gen](https://github.com/geneialco/synTOPia-data-gen) | `claude_desktop_config.json` | 1 (syntopia) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 179 | [zenyr/mcp-pty](https://github.com/zenyr/mcp-pty) | `docs/examples/claude_desktop_config.json` | 1 (mcp-pty) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 180 | [sunetoft/mcp-saxobank](https://github.com/sunetoft/mcp-saxobank) | `claude_desktop_config.json` | 1 (saxo-trading) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 181 | [ADRIANDLT/FinWise](https://github.com/ADRIANDLT/FinWise) | `client-apps-config/Claude-Client-App/claude_desktop_config.json` | 2 (FinWise-MCP-Server-Azure, DISABLED-FinWise-MCP-Server-Local) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 182 | [RodinIgor/STB2026](https://github.com/RodinIgor/STB2026) | `config/claude_desktop_config.json` | 1 (Revit_STB2026) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 183 | [Teeny-Tech-Trek/Claude-learning](https://github.com/Teeny-Tech-Trek/Claude-learning) | `MCP-servers-build/04-audio-analysis-toolkit/claude_desktop_config.json` | 1 (audio-analysis-toolkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 184 | [ADeravi/zotero-mcp-claude-codex](https://github.com/ADeravi/zotero-mcp-claude-codex) | `claude_desktop_config.json` | 1 (zotero-mcp-claude-codex) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 185 | [younwony/mcp](https://github.com/younwony/mcp) | `claude_desktop_config.json` | 1 (weather-calculator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 186 | [lhrasko/snacks](https://github.com/lhrasko/snacks) | `claude_desktop_config.json` | 1 (stripe) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 187 | [dealgo-systems/dealgo-mcp-server](https://github.com/dealgo-systems/dealgo-mcp-server) | `claude_desktop_config.json` | 1 (dealgo-csc) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 188 | [CodelyTV/mcp_servers-course](https://github.com/CodelyTV/mcp_servers-course) | `04-tools/1-tool/etc/config/claude_desktop_config.json` | 1 (codely-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 189 | [BayInl/Dida-MCP](https://github.com/BayInl/Dida-MCP) | `claude_desktop_config.json` | 1 (dida365) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 190 | [keyton-weissinger/llmcosts-mcp](https://github.com/keyton-weissinger/llmcosts-mcp) | `local_bridge_example/claude_desktop_config.json` | 1 (llmcosts) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 191 | [Matt2012/MCPNotificationServer](https://github.com/Matt2012/MCPNotificationServer) | `claude_desktop_config.json` | 1 (twilio-sms) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 192 | [OldBigBuddha/dotfiles](https://github.com/OldBigBuddha/dotfiles) | `claude-macos/.claude/claude_desktop_config.json` | 2 (gce, Context7) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-INJECT-Context7` |
| 193 | [osauer/hyperserve](https://github.com/osauer/hyperserve) | `examples/mcp-stdio/claude_desktop_config.json` | 1 (hyperserve-local) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 194 | [lnbits/LNbits-MCP-Server](https://github.com/lnbits/LNbits-MCP-Server) | `claude_desktop_config.json` | 1 (LNbits) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 195 | [AIS2Lab/MCPSecBench](https://github.com/AIS2Lab/MCPSecBench) | `code/claude_desktop_config.json` | 4 (malicious, compute, check +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 196 | [The-Thought-Magician/enhanced-browser-mcp](https://github.com/The-Thought-Magician/enhanced-browser-mcp) | `claude_desktop_config.json` | 1 (enhanced-browser-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 197 | [carloskvasir/fetcher](https://github.com/carloskvasir/fetcher) | `claude_desktop_config.json` | 1 (fetcher) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 198 | [armoryworks/drive-mcp](https://github.com/armoryworks/drive-mcp) | `examples/claude_desktop_config.json` | 1 (armoryworks-drive) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 199 | [lavakush07/vulnerable-agent-samples](https://github.com/lavakush07/vulnerable-agent-samples) | `configs/claude_desktop_config.json` | 9 (prompt-injection-server, tool-shadowing-server, suspicious-words-server +6 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 200 | [Alby2007/PLTM-Claude-repost-](https://github.com/Alby2007/PLTM-Claude-repost-) | `mcp_server/claude_desktop_config.json` | 1 (pltm-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 201 | [tanopaterno/MCPDemo](https://github.com/tanopaterno/MCPDemo) | `99 - Claude Desktop config/claude_desktop_config.json` | 1 (demo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 202 | [FrancescoXX/mcp-server](https://github.com/FrancescoXX/mcp-server) | `claude_desktop_config.json` | 1 (roma-demo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 203 | [sankar1v/mcp](https://github.com/sankar1v/mcp) | `mcp_payment_langgraph/claude_desktop_config.json` | 1 (payment-transaction-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 204 | [paulpreibisch/AgentVibes](https://github.com/paulpreibisch/AgentVibes) | `mcp-server/examples/claude_desktop_config.json` | 1 (agentvibes) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 205 | [vitorlm/pytoolkit](https://github.com/vitorlm/pytoolkit) | `src/mcp_server/claude_desktop_config.json` | 1 (pytoolkit-management) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 206 | [stier1ba/licensespring-mcp](https://github.com/stier1ba/licensespring-mcp) | `docs/claude_desktop_config.json` | 2 (licensespring-license-api, licensespring-management-api) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 207 | [VibeCodingNights/reverse-engineering](https://github.com/VibeCodingNights/reverse-engineering) | `setup/claude_desktop_config.json` | 1 (ghidra) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 208 | [bitlab-tech/mcp](https://github.com/bitlab-tech/mcp) | `email-mcp/config/claude_desktop_config.json` | 1 (email-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 209 | [shalabhraj1990/GenAIDeveloment](https://github.com/shalabhraj1990/GenAIDeveloment) | `swiggy-mcp/claude_desktop_config.json` | 3 (time, hello-mcp, swiggy-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 210 | [94aharris/coach-ai](https://github.com/94aharris/coach-ai) | `claude_desktop_config.json` | 1 (coach-ai) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 211 | [LA3D/mcp_vocabulary_service](https://github.com/LA3D/mcp_vocabulary_service) | `claude_desktop_config.json` | 1 (earth616-vocab) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 212 | [AndresDev28/e-commerce-relojes-bv-beni](https://github.com/AndresDev28/e-commerce-relojes-bv-beni) | `Support/Claude/claude_desktop_config.json` | 1 (linear) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 213 | [acd19ml/portfoliomind](https://github.com/acd19ml/portfoliomind) | `claude_desktop_config.json` | 1 (portfoliomind) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 214 | [apidav44/mcp-mab-nov2025](https://github.com/apidav44/mcp-mab-nov2025) | `configurations/claude_desktop_config.json` | 3 (weather, shell, traducteur) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 215 | [SadhakKumar/ZK_location_verifier](https://github.com/SadhakKumar/ZK_location_verifier) | `newagentkit/agentkit/typescript/examples/model-context-protocol-smart-wallet-server/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 216 | [swordffish/EDA-agent](https://github.com/swordffish/EDA-agent) | `.mcp.json` | 1 (orfs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 217 | [danroblewis/g1_uart_mcp](https://github.com/danroblewis/g1_uart_mcp) | `mcp.json` | 1 (g1-device-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 218 | [jambonz/ultravox-warm-transfer](https://github.com/jambonz/ultravox-warm-transfer) | `app.json` | 2 (description, type) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 219 | [iota-uz/sheets-mcp](https://github.com/iota-uz/sheets-mcp) | `.mcp.json` | 1 (sheets) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 220 | [kyong0612/voice-notify-mcp](https://github.com/kyong0612/voice-notify-mcp) | `dxt.json` | 1 (voice-notify) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 221 | [tabletman/boom-warehouse](https://github.com/tabletman/boom-warehouse) | `mcp.json` | 3 (honcho-meta, honcho, context7) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-INJECT-context7` |
| 222 | [weiwarren/ai-dlc](https://github.com/weiwarren/ai-dlc) | `dev.json` | 4 (aws-nx-mcp, amzn-mcp, awslabs.aws-pricing-mcp-server +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 223 | [daedalus/mcp-pcapy-ng](https://github.com/daedalus/mcp-pcapy-ng) | `mcp.json` | 1 (mcp-pcapy-ng) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 224 | [Sandeeprdy1729/timps-swarm](https://github.com/Sandeeprdy1729/timps-swarm) | `mcp.json` | 1 (timps-swarm) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 225 | [aaravjj2/TechBuddy](https://github.com/aaravjj2/TechBuddy) | `.mcp.json` | 2 (github, playwright) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 226 | [JarryCheessers/flashcard](https://github.com/JarryCheessers/flashcard) | `mcp.json` | 1 (github) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 227 | [BoomRepublic/SocialMotive](https://github.com/BoomRepublic/SocialMotive) | `.mcp.json` | 1 (telerik-blazor-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 228 | [vbandi/mcp-realtime-poc](https://github.com/vbandi/mcp-realtime-poc) | `mcp.json` | 1 (calculator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 229 | [amitpo23/medici-monitor-](https://github.com/amitpo23/medici-monitor-) | `.mcp.json` | 1 (medici-monitor) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 230 | [james5101/terraform-standards-mcp](https://github.com/james5101/terraform-standards-mcp) | `mcp.json` | 1 (terraform-standards) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 231 | [nuyoah-byte/random-caller](https://github.com/nuyoah-byte/random-caller) | `mcp.json` | 1 (edgeone-pages-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 232 | [mariaiontseva/3-Step-KYC-Onboarding-Flow](https://github.com/mariaiontseva/3-Step-KYC-Onboarding-Flow) | `mcp.json` | 1 (TalkToFigma) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 233 | [AndyXT/ast-grep-mcp](https://github.com/AndyXT/ast-grep-mcp) | `mcp.json` | 1 (ast-grep) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 234 | [lrferr/mysql-mcp-server](https://github.com/lrferr/mysql-mcp-server) | `mcp.json` | 1 (mysql-monitor) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 235 | [esxr/bob_old](https://github.com/esxr/bob_old) | `mcp.json` | 3 (bob-memory, bob-observability, bob-ability) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 236 | [734ai/NocturneRecon](https://github.com/734ai/NocturneRecon) | `mcp.json` | 1 (nocturnerecon) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 237 | [sgx-labs/statelessagent](https://github.com/sgx-labs/statelessagent) | `mcp.json` | 1 (same) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 238 | [eprislac/mcp1](https://github.com/eprislac/mcp1) | `mcp.json` | 1 (calculator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 239 | [pyoclaw/pyoway](https://github.com/pyoclaw/pyoway) | `mcp.json` | 1 (github) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 240 | [baljinder0630/Gym-Management](https://github.com/baljinder0630/Gym-Management) | `gym.json` | 1 (gym) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 241 | [Killerquenn84/aerocloud-engine](https://github.com/Killerquenn84/aerocloud-engine) | `mcp.json` | 1 (multi-ai-router) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 242 | [SurveySensei/SurveySensei-Agents](https://github.com/SurveySensei/SurveySensei-Agents) | `mcp.json` | 1 (mcp-template) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 243 | [Create-State/cursor-plugin](https://github.com/Create-State/cursor-plugin) | `mcp.json` | 1 (create-state) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 244 | [shitada/ghcpsdknotify](https://github.com/shitada/ghcpsdknotify) | `mcp.json` | 1 (workiq) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 245 | [AprovanLabs/hardcopy](https://github.com/AprovanLabs/hardcopy) | `mcp.json` | 1 (hardcopy) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 246 | [glindberg2000/SuperAgent-n8n](https://github.com/glindberg2000/SuperAgent-n8n) | `mcp.json` | 5 (discord, filesystem, postgres +2 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 247 | [0800tim/customer-portal-starter](https://github.com/0800tim/customer-portal-starter) | `mcp.json` | 1 (aiva) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 248 | [kaichen/mterm](https://github.com/kaichen/mterm) | `mcp.json` | 2 (fetch, memory) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-fetch` |
| 249 | [Accular/tripplin-fresh](https://github.com/Accular/tripplin-fresh) | `mcp.json` | 1 (firebase) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 250 | [cheezcake/aidderall_mcp](https://github.com/cheezcake/aidderall_mcp) | `mcp.json` | 1 (aidderall) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 251 | [omozousha/DNOFlow](https://github.com/omozousha/DNOFlow) | `mcp.json` | 1 (supabase) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 252 | [Raghav-56/flexoki-mcp-server](https://github.com/Raghav-56/flexoki-mcp-server) | `mcp.json` | 1 (flexoki) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 253 | [jagoanbunda/laravel](https://github.com/jagoanbunda/laravel) | `mcp.json` | 1 (nakes-boost) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 254 | [xiaodye/rune-code](https://github.com/xiaodye/rune-code) | `mcp.json` | 1 (context7) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-INJECT-context7` |
| 255 | [kararha/menu](https://github.com/kararha/menu) | `mcp.json` | 1 (stitch) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 256 | [jh0rman/my-toolbox-mcp](https://github.com/jh0rman/my-toolbox-mcp) | `mcp.json` | 1 (my-toolbox) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 257 | [paghpaghak/survey-flow-builder-studio123](https://github.com/paghpaghak/survey-flow-builder-studio123) | `mcp.json` | 1 (context7) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-INJECT-context7` |
| 258 | [encoredev/cursor-plugin](https://github.com/encoredev/cursor-plugin) | `mcp.json` | 1 (encore-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 259 | [rolling-codes/codex-mcp](https://github.com/rolling-codes/codex-mcp) | `mcp.json` | 1 (codex-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 260 | [SemperFidelis0510/mtg-builder](https://github.com/SemperFidelis0510/mtg-builder) | `mcp.json` | 1 (mtg-cards) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 261 | [1Ayush-Petwal/MCP](https://github.com/1Ayush-Petwal/MCP) | `mcp.json` | 2 (mail-tool, issue-tool) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 262 | [sesunda/AI-CODE-REVIEWER](https://github.com/sesunda/AI-CODE-REVIEWER) | `mcp.json` | 1 (ai-code-reviewer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 263 | [Digigit24/AIOS](https://github.com/Digigit24/AIOS) | `mcp.json` | 1 (notion) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 264 | [SauBeoo/backend_realestate](https://github.com/SauBeoo/backend_realestate) | `mcp.json` | 1 (mysql-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 265 | [rswingle/blackarch_mcp](https://github.com/rswingle/blackarch_mcp) | `mcp.json` | 1 (blackarch-linux-tools) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 266 | [bsangars/mcp](https://github.com/bsangars/mcp) | `mcp_config.json` | 1 (mpo-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 267 | [DiogoGraciano/CalendarNow-Laravel](https://github.com/DiogoGraciano/CalendarNow-Laravel) | `src/.mcp.json` | 1 (laravel-boost) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 268 | [GeorgeDoors888/GB-Power-Market-JJ](https://github.com/GeorgeDoors888/GB-Power-Market-JJ) | `openclaw-skills/skills/cwyhkyochen-a11y/content-ops/config/mcporter.json` | 3 (xiaohongshu-mcp, reddit, social-media-engine) | 0 | 0 | 3 | 0 | MEDIUM: `DANGEROUS-POPULAR-xiaohongshu-mcp-social-media` |
| 269 | [thijskuilman/papersome](https://github.com/thijskuilman/papersome) | `.junie/mcp/mcp.json` | 2 (laravel-boost, herd) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 270 | [0xranx/OpenContext](https://github.com/0xranx/OpenContext) | `mcp.example.json` | 1 (opencontext) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 271 | [sfc-gh-miwhitaker/sfe-public](https://github.com/sfc-gh-miwhitaker/sfe-public) | `_archive/guide-ai-tool-rollout/reference/mcp-github-1password.json` | 1 (github) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 272 | [favstats/docex](https://github.com/favstats/docex) | `.claude-plugin/plugin.json` | 1 (docex) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 273 | [Memekitchen/memekitchen-mcp](https://github.com/Memekitchen/memekitchen-mcp) | `mcp_install.json` | 1 (memekitchen) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 274 | [renato0307/go-mcp-rest](https://github.com/renato0307/go-mcp-rest) | `claude_desktop_config.json.sample` | 1 (mcp-books) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 275 | [ozand/ayga-mcp-nodejs](https://github.com/ozand/ayga-mcp-nodejs) | `claude_desktop_config.json.example` | 1 (ayga-nodejs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 276 | [JasonMs17/personal-nextjs-saham_viewer](https://github.com/JasonMs17/personal-nextjs-saham_viewer) | `claude_desktop_config.json` | 1 (emiten-database) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 277 | [Adnaan1806/CSVFileReaderCodeCrunch](https://github.com/Adnaan1806/CSVFileReaderCodeCrunch) | `claude_desktop_config.json` | 1 (data_explore) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 278 | [Shoaib1M/AI-CLINIC](https://github.com/Shoaib1M/AI-CLINIC) | `claude_desktop_config.json.json` | 1 (june-cohort) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 279 | [MilesP46/FlowiseAI-MCP](https://github.com/MilesP46/FlowiseAI-MCP) | `claude_desktop_config.json.example` | 1 (flowiseai) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 280 | [edan-ais/Rangler-Info](https://github.com/edan-ais/Rangler-Info) | `COPY-THIS-claude_desktop_config.json` | 1 (metabase) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 281 | [sbsong-git/gcp-fitness-mcp](https://github.com/sbsong-git/gcp-fitness-mcp) | `claude_desktop_config.json` | 1 (google-fitness) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 282 | [mlobo2012/Claude_Desktop_API_USE_VIA_MCP](https://github.com/mlobo2012/Claude_Desktop_API_USE_VIA_MCP) | `config/claude_desktop_config.json` | 2 (github, claude-api) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 283 | [SweaDev/dcs](https://github.com/SweaDev/dcs) | `mcp/claude_desktop_config.json` | 1 (dev-challenge-submissions) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 284 | [hapins/figma-mcp](https://github.com/hapins/figma-mcp) | `example/claude_desktop_config.json` | 1 (figma) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 285 | [luo-gary/ByteBuddies](https://github.com/luo-gary/ByteBuddies) | `old/claude_desktop_config.json` | 1 (guess) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 286 | [mggger/ews-mcp](https://github.com/mggger/ews-mcp) | `examples/claude_desktop_config.json` | 6 (ews, ews-local-build, ews-local +3 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 287 | [adrianlerer/CRIMINAL-AND-LABOR-LAW-EPISTEMOLOGICAL-CLERGIES](https://github.com/adrianlerer/CRIMINAL-AND-LABOR-LAW-EPISTEMOLOGICAL-CLERGIES) | `claude_desktop_config.json` | 1 (legal-evolution-unified) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 288 | [kieran-ohara/dotfiles](https://github.com/kieran-ohara/dotfiles) | `config/claude-desktop/claude_desktop_config.json.tmpl` | 4 (1mcp-core, 1mcp-dev, 1mcp-business +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 289 | [rintaro-s/sisterd_lite](https://github.com/rintaro-s/sisterd_lite) | `config/claude_desktop_config.json` | 1 (systerd) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 290 | [kyong0612/deepseek-ocr-agent](https://github.com/kyong0612/deepseek-ocr-agent) | `config/claude_desktop_config.json` | 1 (deepseek-ocr) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 291 | [baddif/mcp-server-gmail-send](https://github.com/baddif/mcp-server-gmail-send) | `claude_desktop_config.json` | 1 (gmail-send) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 292 | [weniv/mcp_book_source](https://github.com/weniv/mcp_book_source) | `ko/2.5/claude_desktop_config.json` | 5 (tutorial_1, tutorial_2, tutorial_3 +2 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 293 | [AnmolRajpoot25/MCP_server_architecture](https://github.com/AnmolRajpoot25/MCP_server_architecture) | `servers/terminal_server/claude_desktop_config.json.windows.example` | 1 (terminal) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 294 | [ctrimm/uswds-local-mcp-server](https://github.com/ctrimm/uswds-local-mcp-server) | `examples/claude_desktop_config.json` | 2 (uswds-vanilla, uswds-react) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 295 | [aryu1217/notion-worklog-mcp](https://github.com/aryu1217/notion-worklog-mcp) | `examples/claude_desktop_config.json` | 1 (worklog) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 296 | [dazzaji/filesystem](https://github.com/dazzaji/filesystem) | `claude_desktop_config.json` | 1 (filesystem) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 297 | [Ravenium22/megaeth-analytics-mcp](https://github.com/Ravenium22/megaeth-analytics-mcp) | `claude_desktop_config.json` | 1 (megaeth-analytics) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 298 | [sarahliuakl/sarasecondhandstaff](https://github.com/sarahliuakl/sarasecondhandstaff) | `mcp/claude_desktop_config.json` | 1 (ecommerce-api) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 299 | [HackWGaveesh/VaaniSetu_Prototype](https://github.com/HackWGaveesh/VaaniSetu_Prototype) | `claude_desktop_config.json` | 1 (Lossless_AI_For_Bharath Docs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 300 | [swapnilpuri/firstadkagent](https://github.com/swapnilpuri/firstadkagent) | `claude_desktop_config.json` | 1 (employee-email-agent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 301 | [eJNIK/mcp-server-stack](https://github.com/eJNIK/mcp-server-stack) | `claude_desktop_config.json` | 1 (aws-docs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 302 | [greatbody/mcp-mssql-node](https://github.com/greatbody/mcp-mssql-node) | `src/samples/claude_desktop_config.json` | 1 (mssql) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 303 | [wavewand/wand](https://github.com/wavewand/wand) | `claude_desktop_config.json` | 1 (wand) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 304 | [nandangupta-security/CloudSecAIBot](https://github.com/nandangupta-security/CloudSecAIBot) | `claude_desktop_config.json` | 5 (cloud-sec-ai-bot-AWS, cloud-sec-ai-bot-Azure, cloud-sec-ai-bot-GCP +2 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 305 | [mhsu2112/fr2052a-policy-as-code](https://github.com/mhsu2112/fr2052a-policy-as-code) | `mcp/claude_desktop_config.json` | 1 (fr2052a) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 306 | [Java-Techie-jt/shopping-cart-mcp](https://github.com/Java-Techie-jt/shopping-cart-mcp) | `claude_desktop_config.json` | 1 (shopping-cart-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 307 | [hjyuh/MathsSTuff](https://github.com/hjyuh/MathsSTuff) | `tools/claude_desktop_config.json` | 3 (robloxstudio-mcp, axle, aristotle) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 308 | [BSec/MCP-Demo-Server](https://github.com/BSec/MCP-Demo-Server) | `python/claude_desktop_config.json` | 1 (mcp-demo-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 309 | [zhewenzhang/tushare_MCP](https://github.com/zhewenzhang/tushare_MCP) | `claude_desktop_config.json` | 1 (tushare) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 310 | [auto-res2/test-kumagai-20250731-v2](https://github.com/auto-res2/test-kumagai-20250731-v2) | `.claude/claude_desktop_config.json` | 1 (airas) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-airas` |
| 311 | [Arunosaur/ninaivalaigal](https://github.com/Arunosaur/ninaivalaigal) | `configs/claude_desktop_config.json` | 1 (ninaivalaigal) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 312 | [venki0552/slg-cli](https://github.com/venki0552/slg-cli) | `configs/claude_desktop_config.json` | 1 (slg) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 313 | [Local-AI-Workflows/Praktikantenamt-AI-Assistant](https://github.com/Local-AI-Workflows/Praktikantenamt-AI-Assistant) | `mcp-tools/company-lookup/claude_desktop_config.json` | 1 (company-lookup) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 314 | [wangguoqing123/xhs_create_v3](https://github.com/wangguoqing123/xhs_create_v3) | `.claude/claude_desktop_config.json` | 2 (context7, browsermcp) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-INJECT-context7` |
| 315 | [cgize/claude-mcp-think-tool](https://github.com/cgize/claude-mcp-think-tool) | `claude_desktop_config.json` | 1 (think-tool) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 316 | [Sushant1976/MyRepo](https://github.com/Sushant1976/MyRepo) | `claude_desktop_config.json` | 1 (count-r) | 0 | 0 | 1 | 0 | _context-limit rules only_ |
| 317 | [Igormartinssilva/TCC](https://github.com/Igormartinssilva/TCC) | `claude_desktop_config.json` | 2 (Demo, Kubectl) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 318 | [Vibhor7-7/Cortex-CxC](https://github.com/Vibhor7-7/Cortex-CxC) | `docs/claude_desktop_config.json` | 1 (cortex-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 319 | [carlosgutierrezch/mcp_component](https://github.com/carlosgutierrezch/mcp_component) | `claude_desktop_config.json` | 1 (azure-sql) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 320 | [mandible9/nifinova](https://github.com/mandible9/nifinova) | `claude_desktop_config.json` | 1 (kite) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 321 | [edgarcordovat/agente_qgis_ver_complemento](https://github.com/edgarcordovat/agente_qgis_ver_complemento) | `claude_desktop_config.json` | 1 (qgis) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 322 | [Gianloko/salesforce-claude-mcp](https://github.com/Gianloko/salesforce-claude-mcp) | `claude_desktop_config.json` | 1 (salesforce-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 323 | [xilu0/mcp-plantuml-server](https://github.com/xilu0/mcp-plantuml-server) | `claude_desktop_config.json` | 1 (plantuml) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 324 | [agustinissidoro/bach-mcp](https://github.com/agustinissidoro/bach-mcp) | `claude_desktop_config.json` | 1 (bach-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 325 | [ivossos/newcashflow-agent](https://github.com/ivossos/newcashflow-agent) | `claude_desktop_config.json` | 1 (cashflow-forecast) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 326 | [AishSoni/Imagyn](https://github.com/AishSoni/Imagyn) | `claude_desktop_config.json` | 1 (imagyn) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 327 | [CERVIII/mcp-adk-ap2-agent-pokemon](https://github.com/CERVIII/mcp-adk-ap2-agent-pokemon) | `claude_desktop_config.json` | 1 (pokemon) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 328 | [Mohamedcreativecloud/infrastructure-copilot](https://github.com/Mohamedcreativecloud/infrastructure-copilot) | `claude_desktop_config.json` | 1 (infrastructure-copilot) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 329 | [tanayshah11/travel-mcp-server](https://github.com/tanayshah11/travel-mcp-server) | `claude_desktop_config.json` | 1 (travel) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 330 | [AfeiFun/ASR](https://github.com/AfeiFun/ASR) | `claude_desktop_config.json` | 1 (asr-transcriber) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 331 | [matamalaortiz/tercer-mcp](https://github.com/matamalaortiz/tercer-mcp) | `~/Library/Application Support/Claude/claude_desktop_config.json` | 1 (tercer-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 332 | [CarreteroSamuel/MCP_server_get_info_CV](https://github.com/CarreteroSamuel/MCP_server_get_info_CV) | `claude_desktop_config.json` | 1 (mcp-cv-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 333 | [V-Manish-Kumar/Unified-MCP-Server](https://github.com/V-Manish-Kumar/Unified-MCP-Server) | `claude_desktop_config.json` | 2 (mysql, Zapier) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 334 | [pbulbule13/mcpwithgoogle](https://github.com/pbulbule13/mcpwithgoogle) | `config/claude_desktop_config.json` | 1 (google-workspace) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 335 | [ZhenyaPav/jellyfin_mcp](https://github.com/ZhenyaPav/jellyfin_mcp) | `examples/claude_desktop_config.json` | 1 (jellyfin) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 336 | [landmaster135/devbox](https://github.com/landmaster135/devbox) | `.config/claude/mcp_win/claude_desktop_config.json` | 17 (arithmetic_calculator, datetime_calculator, http_request +14 more) | 0 | 0 | 1 | 0 | _context-limit rules only_ |
| 337 | [EmilianoMierUjed/scjn-jurisprudencia_mx](https://github.com/EmilianoMierUjed/scjn-jurisprudencia_mx) | `install/claude_desktop_config.json` | 1 (scjn-jurisprudencia) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 338 | [ChnMig/Vdoc-mcp](https://github.com/ChnMig/Vdoc-mcp) | `examples/claude_desktop_config.json` | 1 (vdoc) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 339 | [pere94/mcp_amazon_affiliate](https://github.com/pere94/mcp_amazon_affiliate) | `DOC/claude_desktop_config.json` | 1 (enterprise-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 340 | [anajuliabit/aeon](https://github.com/anajuliabit/aeon) | `examples/mcp/claude_desktop_config.json` | 1 (aeon) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 341 | [danstrem2/clawdbot-skill-master-pack](https://github.com/danstrem2/clawdbot-skill-master-pack) | `skills/gold-price-mcp/claude_desktop_config.json` | 1 (gold-price) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 342 | [bitlab-tech/mcp](https://github.com/bitlab-tech/mcp) | `news-mcp/config/claude_desktop_config.json` | 1 (news-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 343 | [gigapipehq/gigapipe-traces-mcp](https://github.com/gigapipehq/gigapipe-traces-mcp) | `examples/claude-desktop/claude_desktop_config.json` | 1 (temposerver) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 344 | [cortex-works/cortex-act](https://github.com/cortex-works/cortex-act) | `labs/terminal_extension/mcp-server/claude_desktop_config.json` | 1 (terminal-master) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 345 | [pmarkowsky/santa-mcp](https://github.com/pmarkowsky/santa-mcp) | `claude_desktop_config.json` | 1 (santa-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 346 | [jedeee-ei/Digital-twin](https://github.com/jedeee-ei/Digital-twin) | `claude_desktop_config.json` | 1 (digital-twin) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 347 | [Marshal-AM/fireglobe](https://github.com/Marshal-AM/fireglobe) | `agentkit/typescript/create-onchain-agent/templates/mcp/src/agentkit/svm/cdp/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 348 | [SalesforceCommerceCloud/pwa-kit](https://github.com/SalesforceCommerceCloud/pwa-kit) | `packages/pwa-kit-mcp/claude_desktop_config.json` | 1 (pwa-kit-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 349 | [docling-project/docling-mcp](https://github.com/docling-project/docling-mcp) | `docs/integrations/claude_desktop_config.json` | 1 (docling) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 350 | [matthewhand/mcp-openapi-proxy](https://github.com/matthewhand/mcp-openapi-proxy) | `examples/wolframalpha-claude_desktop_config.json` | 1 (wolframalpha) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 351 | [LokiMCPUniverse/git-mcp-server](https://github.com/LokiMCPUniverse/git-mcp-server) | `examples/example_claude_desktop_config.json` | 1 (git-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 352 | [savir2010/course-generator](https://github.com/savir2010/course-generator) | `claude_desktop_config.json` | 1 (course-generator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 353 | [ForeverYoungJay/DAMASK-MCP](https://github.com/ForeverYoungJay/DAMASK-MCP) | `examples/claude_desktop_config.json` | 1 (damask) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 354 | [zadarastorage/zadara-mcp](https://github.com/zadarastorage/zadara-mcp) | `claude_desktop_config.json.example` | 1 (zadara-storage) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-zadara-storage` |
| 355 | [hanisaf/mcp_demo](https://github.com/hanisaf/mcp_demo) | `mac_claude_desktop_config.json` | 2 (santa, research assistant) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 356 | [rodrigo-loayza/kg-mcp-server](https://github.com/rodrigo-loayza/kg-mcp-server) | `CLAUDE_DESKTOP_CONFIG.json` | 1 (academic-cs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 357 | [ly2xxx/aidev](https://github.com/ly2xxx/aidev) | `claude_desktop_config.json` | 4 (claude-code-developer, gemini-qa-agent, MCP_DOCKER +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 358 | [Kratugautam99/Agentic-AI-and-Generative-AI-Practice](https://github.com/Kratugautam99/Agentic-AI-and-Generative-AI-Practice) | `MCP_Server_Tools/sample_claude_desktop_config.json` | 1 (toy-database) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 359 | [sunormesky-max/TetraMem-XL-v12](https://github.com/sunormesky-max/TetraMem-XL-v12) | `integrations/claude_desktop_config.json` | 1 (tetramem) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 360 | [dmitryanchikov/mcp-optimizer](https://github.com/dmitryanchikov/mcp-optimizer) | `examples/integration/claude_desktop_config.json` | 3 (mcp-optimizer, mcp-optimizer-local, mcp-optimizer-production) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 361 | [pillar-wang/AuditAI](https://github.com/pillar-wang/AuditAI) | `AuditAI.McpServer/Docs/claude_desktop_config.json` | 1 (auditai) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 362 | [auntiehomie/homiehouse](https://github.com/auntiehomie/homiehouse) | `mcp-server/claude_desktop_config.json` | 1 (1481393129444737075) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 363 | [pratiksinghlad/PythonFastApi](https://github.com/pratiksinghlad/PythonFastApi) | `claude_desktop_config.json` | 2 (weather, fastapi-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 364 | [ujjwalredd/PromptPatch](https://github.com/ujjwalredd/PromptPatch) | `examples/claude_desktop_config.json` | 1 (promptpatch) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 365 | [ChaoYue0307/mcp-guard](https://github.com/ChaoYue0307/mcp-guard) | `examples/safe-claude_desktop_config.json` | 1 (project-filesystem) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 366 | [GUEPARD98/MCP-POWERSHELL](https://github.com/GUEPARD98/MCP-POWERSHELL) | `claude_desktop_config.json` | 1 (ssh-powershell) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 367 | [meghal86/stacksignal](https://github.com/meghal86/stacksignal) | `.agents/skills/meshtastic/references/claude_desktop_config.json` | 1 (meshtastic) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 368 | [pyember/ember](https://github.com/pyember/ember) | `integrations/mcp/examples/claude_desktop_config.json` | 2 (ember, ember-advanced) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 369 | [cdmx-in/itop-mcp](https://github.com/cdmx-in/itop-mcp) | `claude_desktop_config.json.example` | 1 (itop) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 370 | [MCPVOT/xpequi-api](https://github.com/MCPVOT/xpequi-api) | `packages/mcp-server/examples/claude_desktop_config.json` | 1 (pequi) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 371 | [bflaven/ia_usages](https://github.com/bflaven/ia_usages) | `ia_using_claude/ia_claude_mcp_python/claude_desktop_config/001_example_claude_desktop_config.json` | 4 (greeter, filecounter, conversationsaver +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 372 | [JoyGhoshs/vulnerable-mcp-server](https://github.com/JoyGhoshs/vulnerable-mcp-server) | `claude_desktop_config.json` | 1 (vulnerable-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 373 | [Diwakar-SV/MCP-WEB-APPLICATION](https://github.com/Diwakar-SV/MCP-WEB-APPLICATION) | `project/mcp_server/claude_desktop_config.json` | 1 (ticket-system) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 374 | [dissoc/dissoc-dotfiles](https://github.com/dissoc/dissoc-dotfiles) | `claude-desktop/.config/Claude/claude_desktop_config.json` | 2 (clojure-mcp-7888, clojure-mcp-8888-8889) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 375 | [adityaditya/Zerodha_AI](https://github.com/adityaditya/Zerodha_AI) | `claude_desktop_config.json` | 1 (trade) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 376 | [ayaka209/assets-gen-mcp](https://github.com/ayaka209/assets-gen-mcp) | `examples/claude_desktop_config.json` | 1 (assets-gen) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 377 | [gpt-cmdr/ras-commander-mcp](https://github.com/gpt-cmdr/ras-commander-mcp) | `claude_desktop_config.json` | 1 (hecras) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 378 | [WaroonRagwongsiri/OOP_Project](https://github.com/WaroonRagwongsiri/OOP_Project) | `claude_desktop_config.json` | 1 (oop-project) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 379 | [mikeysrecipes/onepassword-mcp-server](https://github.com/mikeysrecipes/onepassword-mcp-server) | `claude_desktop_config.json.example` | 1 (1Password) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 380 | [matthewhand/mcp-openapi-proxy](https://github.com/matthewhand/mcp-openapi-proxy) | `examples/wordpress-claude_desktop_config.json` | 1 (wordpress) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 381 | [Shutaru/Smart-Trade-MCP](https://github.com/Shutaru/Smart-Trade-MCP) | `claude_desktop_config.json` | 1 (smart-trade) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 382 | [IvanMazeppa/PlasmaDXR](https://github.com/IvanMazeppa/PlasmaDXR) | `agents/pix-debug/claude_desktop_config.json` | 1 (pix-debug) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 383 | [ly2xxx/aidev](https://github.com/ly2xxx/aidev) | `archive/wsl_claude_desktop_config.json` | 2 (claude-code-developer, gemini-qa-agent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 384 | [Ching-Chiang/comsol-mcp](https://github.com/Ching-Chiang/comsol-mcp) | `examples/claude_desktop_config.json` | 1 (comsol-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 385 | [robbrad/homeassistant-mcp](https://github.com/robbrad/homeassistant-mcp) | `examples/claude_desktop_config.json` | 1 (homeassistant) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 386 | [marc-hanheide/qdrant_file_scanner](https://github.com/marc-hanheide/qdrant_file_scanner) | `claude_desktop_config.json` | 1 (rag-documents) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-rag-documents` |
| 387 | [aswinthulasir/mcp-selenium](https://github.com/aswinthulasir/mcp-selenium) | `claude_desktop_config.json` | 1 (selenium) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 388 | [k2jama/LexLogicAI_LogoGen](https://github.com/k2jama/LexLogicAI_LogoGen) | `claude_desktop_config.json` | 1 (lexlogic-comfyui-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 389 | [VirtoCommerce/vc-module-mcp-server](https://github.com/VirtoCommerce/vc-module-mcp-server) | `claude_desktop_config.json` | 1 (virtocommerce) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 390 | [Dodhon/message-analysis-mcp](https://github.com/Dodhon/message-analysis-mcp) | `claude_desktop_config.json` | 1 (imessage-analysis) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 391 | [hetpatel-11/Tableau-MCP](https://github.com/hetpatel-11/Tableau-MCP) | `claude_desktop_config.json` | 1 (tableau-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 392 | [Siyeolryu/ica-SYR-](https://github.com/Siyeolryu/ica-SYR-) | `backend/mcp_servers/claude_desktop_config.json` | 2 (while-you-were-sleeping-stocks, while-you-were-sleeping-briefing) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 393 | [macnishio/ragmcp](https://github.com/macnishio/ragmcp) | `docs/claude_desktop_config.json` | 1 (ragmcp) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-ragmcp` |
| 394 | [codeprimate/math-mcp](https://github.com/codeprimate/math-mcp) | `docs/claude_desktop_config.json` | 1 (math-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 395 | [astrayel/kids-tasks-ha-card](https://github.com/astrayel/kids-tasks-ha-card) | `claude_desktop_config.json` | 1 (playwright) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 396 | [quiknode-labs/qn-guide-examples](https://github.com/quiknode-labs/qn-guide-examples) | `AI/solana-mcp/claude_desktop_config.json` | 1 (solana) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 397 | [dweigend/mcp-tamplate](https://github.com/dweigend/mcp-tamplate) | `examples/claude_desktop_config.json` | 1 (mcp-template) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 398 | [lynnlangit/precision-medicine-mcp](https://github.com/lynnlangit/precision-medicine-mcp) | `servers/mcp-perturbation/claude_desktop_config.json` | 2 (mcp-perturbation-local, mcp-perturbation-remote) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 399 | [SaranyaM15/SystemDesign_Critic](https://github.com/SaranyaM15/SystemDesign_Critic) | `.claude/worktrees/flamboyant-bhaskara/claude_desktop_config.json` | 1 (syscritic) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 400 | [yusuferenkt/mcp-database](https://github.com/yusuferenkt/mcp-database) | `claude_desktop_config.json` | 1 (json-database) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 401 | [tdisawas0github/mcp](https://github.com/tdisawas0github/mcp) | `claude_desktop_config.json` | 6 (spotify-mcp-server, apple-music-mcp-server, notes-mcp-server +3 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 402 | [tink3rtanner/mcp_time](https://github.com/tink3rtanner/mcp_time) | `claude_desktop_config.json` | 1 (timeserver) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 403 | [dolphinsue319/AppleDocCrawler](https://github.com/dolphinsue319/AppleDocCrawler) | `claude_desktop_config.json` | 1 (apple-docs) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-apple-docs` |
| 404 | [bejaminjones/bear-notes-mcp](https://github.com/bejaminjones/bear-notes-mcp) | `deployment/claude_desktop_config.json` | 1 (bear-notes) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 405 | [MetaMove/move-agent-kit](https://github.com/MetaMove/move-agent-kit) | `examples/mcp-server/claude_desktop_config.json` | 1 (agent-kit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 406 | [pyang2045/twsemcp](https://github.com/pyang2045/twsemcp) | `examples/claude_desktop_config.json` | 1 (twse) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 407 | [sebascrugu/finanzas-email-tracker](https://github.com/sebascrugu/finanzas-email-tracker) | `claude_desktop_config.json` | 1 (finanzas-tracker) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 408 | [brunseba/tools-vmware-vra-cli](https://github.com/brunseba/tools-vmware-vra-cli) | `examples/claude_desktop_config.json` | 1 (vmware-vra) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 409 | [sc4rfurry/RedQuanta-MCP](https://github.com/sc4rfurry/RedQuanta-MCP) | `claude_desktop_config.json` | 1 (redquanta-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 410 | [MikaelTHEoret/mastermind-os-v3-fresh](https://github.com/MikaelTHEoret/mastermind-os-v3-fresh) | `scripts/mcp/claude_desktop_config.json` | 1 (mastermind-terminal) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 411 | [SaidurIUT/github-mcp-server](https://github.com/SaidurIUT/github-mcp-server) | `claude_desktop_config.json` | 1 (github-explorer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 412 | [oyjs1989/mcp_ui_automator](https://github.com/oyjs1989/mcp_ui_automator) | `mcp_server/configs/claude_desktop_config.json` | 1 (android-ui-automator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 413 | [riccardo-enr/ros2-docs-mcp](https://github.com/riccardo-enr/ros2-docs-mcp) | `examples/claude_desktop_config.json` | 1 (ros2-docs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 414 | [Ja1Denis/Kronos](https://github.com/Ja1Denis/Kronos) | `claude_desktop_config.json` | 1 (kronos) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 415 | [esminc/ghostwriter-ai-system](https://github.com/esminc/ghostwriter-ai-system) | `config/claude_desktop_config.json` | 2 (slack, esa) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 416 | [bkakadiya/agentic-ai-mcp](https://github.com/bkakadiya/agentic-ai-mcp) | `config/sample_claude_desktop_config.json` | 9 (stock_data, corporate_actions, earnings +6 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 417 | [iamvalenciia/zero-sum](https://github.com/iamvalenciia/zero-sum) | `claude_desktop_config.json` | 1 (zero-sum-lds) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 418 | [bharat98/MemFlow](https://github.com/bharat98/MemFlow) | `src/claude_desktop_config.json` | 1 (memflow) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-memflow` |
| 419 | [vonzelle-vzt/tradestack-mcp](https://github.com/vonzelle-vzt/tradestack-mcp) | `examples/claude_desktop_config.json` | 1 (tradestack) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 420 | [ADIITJ/threadline](https://github.com/ADIITJ/threadline) | `examples/claude_desktop_config.json` | 1 (threadline) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 421 | [imthebreezy247/MCP-Server](https://github.com/imthebreezy247/MCP-Server) | `claude_desktop_config.json` | 1 (gmail) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 422 | [stevenmcsorley/trello-mcp-server](https://github.com/stevenmcsorley/trello-mcp-server) | `claude_desktop_config.json` | 1 (trello) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 423 | [ly2xxx/aidev](https://github.com/ly2xxx/aidev) | `archive/windows_venv_claude_desktop_config.json` | 3 (claude-code-developer, gemini-qa-agent, MCP_DOCKER) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 424 | [YmClash/vegapunk](https://github.com/YmClash/vegapunk) | `mcp-server/claude_desktop_config.json` | 1 (vegapunk-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 425 | [guangliangyang/mcp4Interview](https://github.com/guangliangyang/mcp4Interview) | `claude_desktop_config.json` | 1 (job-applier) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 426 | [danielbokor-cognizant/intro-into-model-context-protocol](https://github.com/danielbokor-cognizant/intro-into-model-context-protocol) | `claude_desktop_config.json` | 1 (demo-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 427 | [Ridvan-bot/mcp](https://github.com/Ridvan-bot/mcp) | `claude_desktop_config.json` | 1 (weather) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 428 | [ps-wiki/ps-wiki.github.io](https://github.com/ps-wiki/ps-wiki.github.io) | `mcp/examples/claude_desktop_config.json` | 1 (pswiki) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 429 | [mccorkel/mnr-hackathon](https://github.com/mccorkel/mnr-hackathon) | `fhir-mcp/claude_desktop_config.json` | 1 (fasten-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 430 | [lyndonkl/graphragmcp](https://github.com/lyndonkl/graphragmcp) | `examples/claude_desktop_config.json` | 1 (graphrag-mcp) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-graphrag-mcp` |
| 431 | [rydersd/ill_tool](https://github.com/rydersd/ill_tool) | `claude_desktop_config.json` | 1 (adobe_mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 432 | [ThreatFlux/YaraFlux](https://github.com/ThreatFlux/YaraFlux) | `examples/claude_desktop_config.json` | 1 (yaraflux-mcp-server) | 0 | 0 | 1 | 0 | _context-limit rules only_ |
| 433 | [camilla-m/mcp-docker-toolkit](https://github.com/camilla-m/mcp-docker-toolkit) | `claude_desktop_config.json` | 1 (docker-mcp-gateway) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 434 | [adamanz/podcast-generator-mcp](https://github.com/adamanz/podcast-generator-mcp) | `examples/claude_desktop_config.json` | 1 (podcast-generator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 435 | [gatchan0807/tokyo-ai-hackathon-server](https://github.com/gatchan0807/tokyo-ai-hackathon-server) | `claude_desktop_config.json` | 1 (health-calculator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 436 | [eyeou/Network_Collab](https://github.com/eyeou/Network_Collab) | `claude_desktop_config.json` | 3 (arxiv-server, arvix-neo4j, pdf-reader-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 437 | [jiangpeipei327/renyimen](https://github.com/jiangpeipei327/renyimen) | `claude_desktop_config.json` | 1 (navigation) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 438 | [martinchen448/searxng-mcp-server](https://github.com/martinchen448/searxng-mcp-server) | `examples/claude_desktop_config.json` | 1 (searxng) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 439 | [LeoDuchen/ModelosOptimizacion1-TP](https://github.com/LeoDuchen/ModelosOptimizacion1-TP) | `claude_desktop_config.json` | 1 (simplex) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 440 | [tricodex/TEEfecta](https://github.com/tricodex/TEEfecta) | `typescript-agenkit/create-onchain-agent/templates/mcp/src/agentkit/evm/privy/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 441 | [samaritan0/dfir-agentic-suite](https://github.com/samaritan0/dfir-agentic-suite) | `mcp-config/claude_desktop_config.json` | 4 (dfir-threatintel, dfir-siem, dfir-case-mgmt +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 442 | [DevquasarX9/mcp-gitlab](https://github.com/DevquasarX9/mcp-gitlab) | `examples/clients/claude_desktop_config.json` | 1 (gitlab) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 443 | [kbarbel640-del/skills](https://github.com/kbarbel640-del/skills) | `skills/hakureirm/longport-mcp/claude_desktop_config.json` | 1 (longport-trading) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 444 | [LoggerApp/Nutrient_db_MCP](https://github.com/LoggerApp/Nutrient_db_MCP) | `claude_desktop_config.json` | 1 (usda) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 445 | [anshull-saxena/dating-app-prompt-skill-mcp](https://github.com/anshull-saxena/dating-app-prompt-skill-mcp) | `claude/claude_desktop_config.json` | 1 (dating-prompt-writer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 446 | [manifoldfrs/dotfiles](https://github.com/manifoldfrs/dotfiles) | `mcp/claude_desktop_config.json.example` | 2 (RepoPrompt, posthog) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 447 | [bitnovo/mcp-bitnovo-pay](https://github.com/bitnovo/mcp-bitnovo-pay) | `configs/claude_desktop_config.json` | 1 (bitnovo-pay) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 448 | [AgiMaulana/HuaweiAppGalleryMcp](https://github.com/AgiMaulana/HuaweiAppGalleryMcp) | `claude_desktop_config.json` | 1 (huawei-appgallery) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 449 | [abdushakurob/citekit](https://github.com/abdushakurob/citekit) | `examples/study-companion/claude_desktop_config.json` | 1 (citekit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 450 | [KajiMaster/curriculum-designer](https://github.com/KajiMaster/curriculum-designer) | `mcp-server/claude_desktop_config.json` | 1 (curriculum-designer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 451 | [libyyu/MyBlueprintEditor](https://github.com/libyyu/MyBlueprintEditor) | `docs/claude_desktop_config.json` | 1 (blueprint) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 452 | [sarthak078/FairLease-AI](https://github.com/sarthak078/FairLease-AI) | `claude_desktop_config.json` | 1 (tavily-search) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-tavily-search` |
| 453 | [arthurfantaci/qlik-mcp-server](https://github.com/arthurfantaci/qlik-mcp-server) | `examples/claude_desktop_config.json` | 1 (qlik-sense) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 454 | [sizips32/backtester](https://github.com/sizips32/backtester) | `mcp_server/claude_desktop_config.json` | 1 (portfolio-backtester) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 455 | [isaacakalanne1/phraseflow-chinese](https://github.com/isaacakalanne1/phraseflow-chinese) | `PhraseFlow Chinese/claude_desktop_config.json` | 3 (composio-server-00fc9365-6441-48ae-8907-8dc106d9798a-mcp, FlowTale Jira, composio-server-ef4bc574-002f-45ab-bb7e-da9b763e235d-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 456 | [vladsadovsky/llm-aggregator.ts](https://github.com/vladsadovsky/llm-aggregator.ts) | `build/claude/config/claude_desktop_config.json` | 1 (conversation-history) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 457 | [Masa1984a/MCP_Driven_UX_Template](https://github.com/Masa1984a/MCP_Driven_UX_Template) | `claude_desktop_config.json` | 1 (TicketManagementSystem) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 458 | [uysalserkan/openlibrary-mcp](https://github.com/uysalserkan/openlibrary-mcp) | `claude_desktop_config.json` | 1 (openlibrary-search) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 459 | [dzivkovi/mock-api](https://github.com/dzivkovi/mock-api) | `examples/claude_desktop_config.json` | 3 (sequential-thinking, teamcenter, sqlite) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 460 | [cleberfarias/AutoFlow-main](https://github.com/cleberfarias/AutoFlow-main) | `server/mcp/claude_desktop_config.json` | 1 (autoflow) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 461 | [RiccardoCeccaroni/ORA-Chatbot](https://github.com/RiccardoCeccaroni/ORA-Chatbot) | `ora-mcp/demo/claude_desktop_config.json` | 1 (ora) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 462 | [kongo97/fast-mcp-server](https://github.com/kongo97/fast-mcp-server) | `docs/claude_desktop_config.json` | 1 (simple-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 463 | [agoncal/agoncal-sample-azure-mcp](https://github.com/agoncal/agoncal-sample-azure-mcp) | `mcp-server-azure-resourcemanager-resources/src/main/mcp/claude_desktop_config.json` | 1 (azure-mgt-resources) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 464 | [jpitc-ca/palo-mcp](https://github.com/jpitc-ca/palo-mcp) | `002-sec-policies/claude_desktop_config.json` | 1 (palo-alto) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 465 | [nurdymuny/gigi-mcp](https://github.com/nurdymuny/gigi-mcp) | `examples/claude_desktop_config.json` | 1 (gigi) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 466 | [Tanishbelel/PaisaAI](https://github.com/Tanishbelel/PaisaAI) | `claude_desktop_config.json` | 1 (paisaai) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 467 | [Joseph19820124/composio-mcp-server-config](https://github.com/Joseph19820124/composio-mcp-server-config) | `claude_desktop_config.json` | 2 (composio, composio-remote) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 468 | [Synaps-Squad/gitlab-mr-mcp](https://github.com/Synaps-Squad/gitlab-mr-mcp) | `plugins/gitlab-mr-review/examples/claude_desktop_config.json` | 1 (gitlab) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 469 | [machapraveen/lanforge-mcp](https://github.com/machapraveen/lanforge-mcp) | `claude_desktop_config.json` | 1 (lanforge) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 470 | [haruki10041999/SALESFORCE-AI-COMPANY](https://github.com/haruki10041999/SALESFORCE-AI-COMPANY) | `claude_desktop_config.json` | 1 (salesforce-ai-company) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 471 | [Sanvith6/My_auto_browser](https://github.com/Sanvith6/My_auto_browser) | `examples/claude_desktop_config.json` | 1 (auto-browser) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 472 | [AkiroKazuki/mcp-server-gh-antigravity](https://github.com/AkiroKazuki/mcp-server-gh-antigravity) | `examples/claude_desktop_config.json` | 3 (antigravity-memory, antigravity-copilot, antigravity-analytics) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 473 | [okgoogle13/career-pilot](https://github.com/okgoogle13/career-pilot) | `docs/archive_legacy_reports/claude_desktop_config.json` | 8 (orchestrator, gemini, documentation +5 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 474 | [Nourimabrouk/Een](https://github.com/Nourimabrouk/Een) | `config/claude_desktop_config.json` | 6 (een-unity-mathematics, een-consciousness-field, een-quantum-unity +3 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 475 | [gjeodnd12165/deepauto-intern-assignment](https://github.com/gjeodnd12165/deepauto-intern-assignment) | `example/claude_desktop_config.json` | 2 (deepauto-intern-assignment, deepauto-intern-assignment-docker) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 476 | [THAMIZH-ARASU/MCP-For-Manim](https://github.com/THAMIZH-ARASU/MCP-For-Manim) | `claude_desktop_config.json` | 1 (FastMCP) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 477 | [temporal-community/durable-async-mcp](https://github.com/temporal-community/durable-async-mcp) | `durable_sync_mcp/claude_desktop_config.json` | 1 (invoice_processor) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 478 | [Prathamesh0009M/POC](https://github.com/Prathamesh0009M/POC) | `claude_desktop_config.json` | 1 (hydraulic-agent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 479 | [like-me-like/integrations](https://github.com/like-me-like/integrations) | `integrations/claude-desktop/claude_desktop_config.json` | 1 (like-me-like) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 480 | [hafnium49/aloha-lite](https://github.com/hafnium49/aloha-lite) | `so101_mcp_server/claude_desktop_config.json` | 1 (so101-robot) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 481 | [SkyyRoseLLC/DevSkyy](https://github.com/SkyyRoseLLC/DevSkyy) | `claude_desktop_config.json` | 1 (devskyy) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 482 | [hanmarco/pyside-calc-gui-test](https://github.com/hanmarco/pyside-calc-gui-test) | `claude_desktop_config.json` | 1 (calculator-test-runner) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 483 | [Abel-Git2103/padelHUB](https://github.com/Abel-Git2103/padelHUB) | `claude_desktop_config.json` | 3 (padelhub, playwright, figma) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-playwright` |
| 484 | [mukul975/mcp-windows-automation](https://github.com/mukul975/mcp-windows-automation) | `config/claude_desktop_config.json` | 1 (unified-windows-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 485 | [ShilinYang123/PG-GMO](https://github.com/ShilinYang123/PG-GMO) | `tools/MCP/collaboration/word-mcp/claude_desktop_config.json` | 1 (word-document-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 486 | [Dhenenjay/Axion-MCP](https://github.com/Dhenenjay/Axion-MCP) | `claude_desktop_config.json` | 1 (earth-engine) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 487 | [Tamoghna12/obsidian-revolutionary-intelligence](https://github.com/Tamoghna12/obsidian-revolutionary-intelligence) | `fastmcp-server/claude_desktop_config.json` | 1 (obsidian-revolutionary) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 488 | [IamP5/fiap-challenge-ford](https://github.com/IamP5/fiap-challenge-ford) | `agent-poc/app/mcp/claude_desktop_config.json` | 1 (app-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 489 | [GerardRojas/NGM_REVIT](https://github.com/GerardRojas/NGM_REVIT) | `mcp/claude_desktop_config.json` | 1 (ngm-revit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 490 | [Ashar20/coinbase](https://github.com/Ashar20/coinbase) | `master-agent/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 491 | [parmacalcio1913/event-data-chatbot](https://github.com/parmacalcio1913/event-data-chatbot) | `examples/claude_desktop_config.json` | 1 (event-data-chatbot) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 492 | [MikaelTHEoret/mastermind-os-v3-fresh](https://github.com/MikaelTHEoret/mastermind-os-v3-fresh) | `claude_desktop_config.json` | 1 (mastermind-terminal) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 493 | [Unlock-MCP/local-research-server](https://github.com/Unlock-MCP/local-research-server) | `examples/claude_desktop_config.json` | 1 (local-researcher) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 494 | [thruthesky/mcp-test](https://github.com/thruthesky/mcp-test) | `claude_desktop_config.json` | 1 (travel-advisory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 495 | [devopsexpertlearning/mcp-search-server](https://github.com/devopsexpertlearning/mcp-search-server) | `clients/claude-config/claude_desktop_config.json` | 3 (browser-search-ollama, browser-search-enhanced, browser-search-fallback) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 496 | [chigwell/telegram-mcp](https://github.com/chigwell/telegram-mcp) | `claude_desktop_config.json` | 1 (telegram-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 497 | [freshtechbro/Vibe-Coder-MCP](https://github.com/freshtechbro/Vibe-Coder-MCP) | `example_claude_desktop_config.json` | 1 (vibe-coder-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 498 | [getzep/zep](https://github.com/getzep/zep) | `mcp/zep-mcp-server/examples/claude-desktop/claude_desktop_config.json` | 1 (zep) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 499 | [keides2/futurevuls-mcp](https://github.com/keides2/futurevuls-mcp) | `templates/claude_desktop_config.json.template` | 1 (futurevuls) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 500 | [brownrl/datatables-mcp](https://github.com/brownrl/datatables-mcp) | `claude_desktop_config.json.example` | 1 (datatables) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 501 | [WatchTowerBenefits/primevue-mcp](https://github.com/WatchTowerBenefits/primevue-mcp) | `claude_desktop_config.json.template` | 2 (primevue-dev, primevue-prod) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 502 | [ssmanji89/postgres-mcp-tools](https://github.com/ssmanji89/postgres-mcp-tools) | `config/claude_desktop_config.json.example` | 1 (postgres_memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 503 | [joshylchen/zettelkasten](https://github.com/joshylchen/zettelkasten) | `claude_desktop_config.json` | 1 (zettelkasten-assistant) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 504 | [Shivansh12t/terminal-agent-mcp-pythonsdk](https://github.com/Shivansh12t/terminal-agent-mcp-pythonsdk) | `docker_claude_desktop_config.json` | 1 (terminal_server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 505 | [clarifyhealth/cms-datagov-mcp-server](https://github.com/clarifyhealth/cms-datagov-mcp-server) | `CLAUDE_DESKTOP_CONFIG.json` | 1 (cms-datagov) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 506 | [toni-ramchandani/sapient-mcp](https://github.com/toni-ramchandani/sapient-mcp) | `claude_desktop_config.json` | 1 (sapient) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 507 | [coderjun/shaka-packager-mcp-server](https://github.com/coderjun/shaka-packager-mcp-server) | `example_claude_desktop_config.json` | 2 (filesystem, shaka-packager) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 508 | [mallanisp/ajv-validator-mcp-server](https://github.com/mallanisp/ajv-validator-mcp-server) | `claude_desktop_config.json.example` | 1 (vera) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 509 | [mroshdy91/RevitAtlas](https://github.com/mroshdy91/RevitAtlas) | `docs/config-examples/claude_desktop_config.json` | 1 (Revit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 510 | [twoLoop-40/HwpAutomation](https://github.com/twoLoop-40/HwpAutomation) | `claude_desktop_config.json` | 1 (hwp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 511 | [jamesfpate/dotfiles](https://github.com/jamesfpate/dotfiles) | `symlinks/claude-desktop/Library/Application Support/Claude/claude_desktop_config.json` | 1 (mcp-domain-availability) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 512 | [silverdevelopper/voice2textGroq](https://github.com/silverdevelopper/voice2textGroq) | `claude_desktop_config.json` | 1 (groq-audio-transcription) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 513 | [Spicy-Sashimizy/sfu-library-mcp](https://github.com/Spicy-Sashimizy/sfu-library-mcp) | `claude_desktop_config.json` | 3 (business-plan, sfu-library, pommel) | 0 | 0 | 5 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-business-plan`; MEDIUM: `CONTEXT-EXT-FETCH-sfu-library`; MEDIUM: `CONTEXT-EXT-FETCH-pommel` |
| 514 | [0x0Glitch/Agent-action3](https://github.com/0x0Glitch/Agent-action3) | `agentkit/typescript/examples/model-context-protocol-cdp-server/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 515 | [gabriel-chiappa/LumenLink](https://github.com/gabriel-chiappa/LumenLink) | `agents/coinbase/lumenlink-agent/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 516 | [aIrseneO/garage](https://github.com/aIrseneO/garage) | `jenkins/claude_desktop_config.json` | 1 (gitlab) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-gitlab` |
| 517 | [faustyu1/ton-agent-jobs](https://github.com/faustyu1/ton-agent-jobs) | `mcp/claude_desktop_config.json` | 1 (ton-agent-jobs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 518 | [AngDrew/todoist-mcp](https://github.com/AngDrew/todoist-mcp) | `claude_desktop_config.json` | 1 (todoist) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 519 | [vyqno/0xstoa](https://github.com/vyqno/0xstoa) | `apps/mcp-server/examples/claude_desktop_config.json` | 1 (stoa) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 520 | [lastbattle/WzImg-MCP-Server](https://github.com/lastbattle/WzImg-MCP-Server) | `example_claude_desktop_config.json` | 1 (wzimg) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 521 | [sg3t41/coincheck-mcp](https://github.com/sg3t41/coincheck-mcp) | `config/claude_desktop_config.json.example` | 1 (coincheck) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 522 | [Ak-Khandu-Baba/Learning-Agentic-AI](https://github.com/Ak-Khandu-Baba/Learning-Agentic-AI) | `claude_desktop_config.json` | 1 (newtation-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 523 | [Murat-Selim/Devs_Backend](https://github.com/Murat-Selim/Devs_Backend) | `claude_desktop_config.json` | 1 (devs-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 524 | [Cursedpotential/TheBigOne](https://github.com/Cursedpotential/TheBigOne) | `archive/04_Utilities/UNS-MCP-main/example_claude_desktop_config.json` | 1 (UNS_MCP) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 525 | [youneselfakir0/Twisterlab](https://github.com/youneselfakir0/Twisterlab) | `config/claude_desktop_config.json` | 1 (twisterlab) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 526 | [hitanshu-dhawan/Model-Context-Protocol-Playground](https://github.com/hitanshu-dhawan/Model-Context-Protocol-Playground) | `calculator/claude_desktop_config.json` | 1 (calculator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 527 | [Devdas-gupta/instagram-mcp](https://github.com/Devdas-gupta/instagram-mcp) | `configs/claude_desktop_config.json` | 1 (instagram-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 528 | [BugMentor/playwright-mcp-demo-example](https://github.com/BugMentor/playwright-mcp-demo-example) | `claude_desktop_config.json` | 1 (playwright) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 529 | [Saksham1387/Claude-weather-MCP](https://github.com/Saksham1387/Claude-weather-MCP) | `claude_desktop_config.json` | 1 (weather) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 530 | [alexrwilliam/playwright-mcp-server](https://github.com/alexrwilliam/playwright-mcp-server) | `examples/claude_desktop_config.json` | 2 (playwright, playwright-headed) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 531 | [TaylorBeeston/semantic-memory-search](https://github.com/TaylorBeeston/semantic-memory-search) | `claude_desktop_config.json` | 1 (semantic-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 532 | [SERGE3-g/mcp-server](https://github.com/SERGE3-g/mcp-server) | `claude_desktop_config.json` | 1 (mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 533 | [lgpearson1771/Memory-Bank-MCP](https://github.com/lgpearson1771/Memory-Bank-MCP) | `docs/examples/claude_desktop_config.json` | 1 (memory-bank-generator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 534 | [ChiragKottary/mcp_ibmi](https://github.com/ChiragKottary/mcp_ibmi) | `claude_desktop_config.json` | 1 (buildmate-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 535 | [Brahim820/MCP_Odoo1](https://github.com/Brahim820/MCP_Odoo1) | `claude_desktop_config.json` | 1 (odoo-perusahaan) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 536 | [GTalksTech/netops-toolkit](https://github.com/GTalksTech/netops-toolkit) | `scripts/netmiko/mcp-network-assistant/claude_desktop_config.json` | 1 (network-assistant) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 537 | [daemon-blockint-tech/MORDOR](https://github.com/daemon-blockint-tech/MORDOR) | `mcp_config/claude_desktop_config.json` | 5 (ghidra, radare2, pay +2 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 538 | [robotlearning123/mujoco-mcp](https://github.com/robotlearning123/mujoco-mcp) | `mcp-testing/configs/claude-desktop/claude_desktop_config.json` | 1 (mujoco-mcp) | 0 | 0 | 1 | 0 | _context-limit rules only_ |
| 539 | [kitconcept/matomo-mcp](https://github.com/kitconcept/matomo-mcp) | `claude_desktop_config.json` | 1 (matomo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 540 | [Fahim-Azwad/simple-obspy](https://github.com/Fahim-Azwad/simple-obspy) | `claude_desktop_config.json` | 1 (obspy-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 541 | [EternalKingss/jarvis](https://github.com/EternalKingss/jarvis) | `jarvis-mcp/claude_desktop_config.json` | 1 (windows_jarvis) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 542 | [sbraind/excel-mcp-server](https://github.com/sbraind/excel-mcp-server) | `claude_desktop_config.json` | 1 (excel) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 543 | [pepo1275/mcp4gva](https://github.com/pepo1275/mcp4gva) | `typescript/claude_desktop_config.json` | 1 (mcp4gva-typescript) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 544 | [ondrejsindelka/praetor-mcp](https://github.com/ondrejsindelka/praetor-mcp) | `examples/claude_desktop_config.json` | 1 (praetor) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 545 | [CaptainJi/cli_executor](https://github.com/CaptainJi/cli_executor) | `examples/claude_desktop_config.json` | 1 (cli-executor) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 546 | [luiztools/node-misc-examples](https://github.com/luiztools/node-misc-examples) | `mcp-server-example/claude_desktop_config.json` | 1 (binance) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 547 | [sugukurukabe/koko-call-mcp](https://github.com/sugukurukabe/koko-call-mcp) | `examples/jgrants-integration/claude_desktop_config.json` | 2 (jp-bids, jgrants) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 548 | [Ashfaqbs/apache-flink-mcp-server](https://github.com/Ashfaqbs/apache-flink-mcp-server) | `clients/claude/claude_desktop_config.json` | 1 (Flink-Mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 549 | [abhich2507/geant4-mcp](https://github.com/abhich2507/geant4-mcp) | `claude_desktop_config.json` | 1 (geant4-simulation) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 550 | [coinbase/agentkit](https://github.com/coinbase/agentkit) | `typescript/create-onchain-agent/templates/mcp/src/agentkit/custom-emv/viem/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 551 | [tyson-swetnam/epihack-2026](https://github.com/tyson-swetnam/epihack-2026) | `mcp/adhs-mcp/examples/claude_desktop_config.json` | 1 (adhs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 552 | [BLKOUTUK/blkout-event-agent](https://github.com/BLKOUTUK/blkout-event-agent) | `claude_desktop_config.json` | 6 (blkout-campaign, sendfox-integration, heartbeat-integration +3 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 553 | [blakechasteen/hello-world](https://github.com/blakechasteen/hello-world) | `infra/config/claude_desktop_config.json` | 4 (hololoom-hybrid-memory, expertloom, atlassian-jira +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 554 | [dyussekeyev/jumal-mcp](https://github.com/dyussekeyev/jumal-mcp) | `bridge/claude_desktop_config.json` | 1 (jumal-analyzer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 555 | [Choizapp/choiz-meta-ads-mcp](https://github.com/Choizapp/choiz-meta-ads-mcp) | `examples/claude_desktop_config.json` | 1 (meta-ads) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 556 | [washyu/homelab_mcp](https://github.com/washyu/homelab_mcp) | `claude_desktop_config.json` | 1 (homelab) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 557 | [Rajdoll/MCP_Cybersecurity](https://github.com/Rajdoll/MCP_Cybersecurity) | `claude_desktop_config.json` | 3 (puppeteer, external-recon, zap-integration) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-puppeteer` |
| 558 | [lazniak/infakt-mcp](https://github.com/lazniak/infakt-mcp) | `claude_desktop_config.json` | 1 (infakt) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 559 | [PradeepLoganathan/akka-agentic-triage-demo](https://github.com/PradeepLoganathan/akka-agentic-triage-demo) | `evidence-mcp-server/claude_desktop_config.json` | 1 (evidence-tools) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 560 | [commoncrawl/cc-vec](https://github.com/commoncrawl/cc-vec) | `claude_desktop_config.json` | 1 (cc-vec) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 561 | [peguesi/strategy_agents](https://github.com/peguesi/strategy_agents) | `screenpipe/config/claude_desktop_config.json` | 1 (screenpipe-strategy) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 562 | [yamadatarousan/projectanalysis-mcp](https://github.com/yamadatarousan/projectanalysis-mcp) | `claude_desktop_config.json` | 1 (projectanalysis) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 563 | [prcodex/MCP](https://github.com/prcodex/MCP) | `code/client/claude_desktop_config.json` | 1 (spyder-books-ec2) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 564 | [Excelsior-Technologies-Community/Laravel_Claude_Agent_Integration-Sujal_savsani](https://github.com/Excelsior-Technologies-Community/Laravel_Claude_Agent_Integration-Sujal_savsani) | `.claude/claude_desktop_config.json` | 1 (laravel-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 565 | [wavewand/wand](https://github.com/wavewand/wand) | `examples/claude_desktop_config.json` | 1 (mcp-automation-api) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-mcp-automation-api` |
| 566 | [CodeHalwell/Agent-Gantry](https://github.com/CodeHalwell/Agent-Gantry) | `examples/protocols/claude_desktop_config.json` | 1 (agent-gantry) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 567 | [DryRainEnt/GreeumMCP](https://github.com/DryRainEnt/GreeumMCP) | `docs/claude_desktop_config.json` | 1 (greeum_mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 568 | [cortex-io/cortex-platform](https://github.com/cortex-io/cortex-platform) | `services/cortex-bridge/claude_desktop_config.json` | 1 (cortex-fabric) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 569 | [zyntx-lab/periphery-mcp-server](https://github.com/zyntx-lab/periphery-mcp-server) | `examples/claude_desktop_config.json` | 1 (periphery) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 570 | [dislovelhl/crypto-ai-explorer](https://github.com/dislovelhl/crypto-ai-explorer) | `services/mcp-server/claude_desktop_config.json` | 1 (cryptoai-explorer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 571 | [tyson-swetnam/epihack-2026](https://github.com/tyson-swetnam/epihack-2026) | `mcp/whispers-mcp/examples/claude_desktop_config.json` | 1 (whispers) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 572 | [rishigundakaram/cadquery-mcp-server](https://github.com/rishigundakaram/cadquery-mcp-server) | `claude_desktop_config.json` | 1 (cad-verification) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 573 | [mick-gsk/drift](https://github.com/mick-gsk/drift) | `examples/vibe-coding/claude_desktop_config.json` | 1 (drift) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 574 | [0x000NULL/FleetPulse](https://github.com/0x000NULL/FleetPulse) | `mcp-server/claude_desktop_config.json` | 1 (fleetpulse) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 575 | [walksoda/crawl-mcp](https://github.com/walksoda/crawl-mcp) | `configs/claude_desktop_config.json` | 1 (crawl4ai) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-crawl4ai` |
| 576 | [Nileneb/Game-Mcp](https://github.com/Nileneb/Game-Mcp) | `claude_desktop_config.json` | 1 (game-mining) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 577 | [ottit-code/AI-Agent](https://github.com/ottit-code/AI-Agent) | `examples/claude_desktop_config.json` | 1 (emailbison) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-emailbison` |
| 578 | [CarreteroSamuel/MCP_server_cv](https://github.com/CarreteroSamuel/MCP_server_cv) | `claude_desktop_config.json` | 1 (cv-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 579 | [Positronic-AI/jira-mcp](https://github.com/Positronic-AI/jira-mcp) | `examples/claude_desktop_config.json` | 2 (jira-company, jira-personal) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 580 | [telegraph-it/timescaledb-mcp-server](https://github.com/telegraph-it/timescaledb-mcp-server) | `claude_desktop_config.json` | 1 (timescaledb) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 581 | [stgmt/crawl4ai-mcp](https://github.com/stgmt/crawl4ai-mcp) | `examples/claude_desktop_config.json` | 1 (crawl4ai-local) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-crawl4ai-local` |
| 582 | [emmanuellawal/ebay-extract](https://github.com/emmanuellawal/ebay-extract) | `mcp_server/claude_desktop_config.json` | 1 (ebay-api) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 583 | [surajrimal07/NepseAPI-Unofficial](https://github.com/surajrimal07/NepseAPI-Unofficial) | `claude_desktop_config.json` | 1 (nepseapi-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 584 | [robaita/gen_ai_tutorials](https://github.com/robaita/gen_ai_tutorials) | `code/lecture-15/claude_desktop_config.json` | 1 (filesystem) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 585 | [ajeetraina/talk-demos](https://github.com/ajeetraina/talk-demos) | `mcp-demo/neo4j-kubernetes-github/claude_desktop_config.json` | 3 (github, neo4j, kubernetes) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 586 | [Trushtonfactory/anthropic-admin-mcp](https://github.com/Trushtonfactory/anthropic-admin-mcp) | `examples/claude_desktop_config.json` | 3 (anthropic-admin, anthropic-admin-readonly, anthropic-admin-sandbox-only) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 587 | [southleft/linkedin-mcp](https://github.com/southleft/linkedin-mcp) | `examples/claude_desktop_config.json` | 1 (linkedin) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 588 | [theperfectbean/diabetes-buddy](https://github.com/theperfectbean/diabetes-buddy) | `claude_desktop_config.json` | 1 (diabetes-buddy) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 589 | [wasonisgood/legel-mcp](https://github.com/wasonisgood/legel-mcp) | `claude_desktop_config.json` | 1 (taiwan-law) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 590 | [mhsu2112/fr2052a-policy-as-code](https://github.com/mhsu2112/fr2052a-policy-as-code) | `claude_desktop_config.json` | 1 (fr2052a) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 591 | [anitaguptaoffice/pob-mcp-market](https://github.com/anitaguptaoffice/pob-mcp-market) | `pob-docker-mcp/assets/examples/claude_desktop_config.json` | 1 (pob) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 592 | [vkfolio/orio-search](https://github.com/vkfolio/orio-search) | `mcp-server/claude_desktop_config.json` | 1 (oriosearch) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 593 | [AnthonyPuggs/ausecon-mcp-server](https://github.com/AnthonyPuggs/ausecon-mcp-server) | `examples/claude_desktop_config.json` | 1 (ausecon) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 594 | [vcat-archived/pion-bot-public](https://github.com/vcat-archived/pion-bot-public) | `emcee-spec/claude_desktop_config.json` | 4 (picsum, reSmush, dummyImage +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 595 | [IrkenInvader/mssql-mcp](https://github.com/IrkenInvader/mssql-mcp) | `SQL-AI-samples/MssqlMcp/Node/src/samples/claude_desktop_config.json` | 1 (mssql) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 596 | [Vikramb1/past](https://github.com/Vikramb1/past) | `people-mcp/claude_desktop_config.json` | 1 (people-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 597 | [sanheensethi/PC-Manager-Ai-Agent](https://github.com/sanheensethi/PC-Manager-Ai-Agent) | `claude_desktop_config.json` | 1 (PC-Manager) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 598 | [Santhoshkumard11/smart-code-reviewer-mcp](https://github.com/Santhoshkumard11/smart-code-reviewer-mcp) | `claude_desktop_config.json` | 1 (smart-code-reviewer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 599 | [joakimeriksson/reknir](https://github.com/joakimeriksson/reknir) | `mcp-server/claude_desktop_config.json` | 1 (reknir) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 600 | [fatdinhero/verifiable-ai-stack](https://github.com/fatdinhero/verifiable-ai-stack) | `cognitum/docs/claude_desktop_config.json` | 1 (cognitum) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 601 | [start-trek/nicegui-mcp](https://github.com/start-trek/nicegui-mcp) | `examples/claude_desktop_config.json` | 1 (nicegui-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 602 | [Sanidhya14321/SKILLS-PROJECT-1](https://github.com/Sanidhya14321/SKILLS-PROJECT-1) | `mcp-server/claude_desktop_config.json` | 1 (neuralhire) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 603 | [3uLLd0gs/msstate-mcp](https://github.com/3uLLd0gs/msstate-mcp) | `examples/claude_desktop_config.json` | 1 (msstate-policies) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 604 | [VVikingsson/mcp-server](https://github.com/VVikingsson/mcp-server) | `resources/claude_desktop_config.json` | 1 (dbschenker-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 605 | [delhoume/mo5_bmp](https://github.com/delhoume/mo5_bmp) | `.mcp-templates/claude_desktop_config.json` | 1 (mo5-rag) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-mo5-rag` |
| 606 | [ringo380/claude-google-sheets-mcp](https://github.com/ringo380/claude-google-sheets-mcp) | `examples/claude_desktop_config.json` | 1 (google-sheets) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 607 | [halim-abz/netwitness](https://github.com/halim-abz/netwitness) | `netwitness-mcp-server/files_to_copy/claude_desktop_config.json` | 1 (netwitness) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 608 | [tifa365/berlin-opendata-mcp](https://github.com/tifa365/berlin-opendata-mcp) | `claude_desktop_config.json` | 1 (berlin-opendata) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 609 | [robotlearning123/mujoco-mcp](https://github.com/robotlearning123/mujoco-mcp) | `configs/claude_desktop_config.json` | 1 (mujoco-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 610 | [igorilic/obsidian-mcp](https://github.com/igorilic/obsidian-mcp) | `examples/claude_desktop_config.json` | 1 (obsidian) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 611 | [ShilinYang123/PG-GMO](https://github.com/ShilinYang123/PG-GMO) | `tools/MCP/servers/windows-system/claude_desktop_config.json` | 1 (windows-system) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 612 | [kolide/device-trust-mcp-server](https://github.com/kolide/device-trust-mcp-server) | `.claude.example/claude_desktop_config.json` | 1 (kolide) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 613 | [adisagar2003/ShipITRevenueCat](https://github.com/adisagar2003/ShipITRevenueCat) | `claude_desktop_config.json` | 1 (mcp-unity) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 614 | [Christophenolans/train_Project](https://github.com/Christophenolans/train_Project) | `claude_desktop_config.json` | 1 (train-project) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 615 | [ncinotimo/Salesforce-Analyser-Py](https://github.com/ncinotimo/Salesforce-Analyser-Py) | `claude_desktop_config.json` | 1 (salesforce-analyzer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 616 | [macsymwang/hello-mcp-server](https://github.com/macsymwang/hello-mcp-server) | `examples/claude_desktop_config.json` | 1 (hello-world) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 617 | [vahapogut/nexarion](https://github.com/vahapogut/nexarion) | `examples/claude-desktop/claude_desktop_config.json` | 1 (nexarion) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 618 | [tom-viviano/edgelake-mcp-server](https://github.com/tom-viviano/edgelake-mcp-server) | `examples/claude_desktop_config.json` | 1 (edgelake) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 619 | [Mihai-Codes/openbrain](https://github.com/Mihai-Codes/openbrain) | `config/claude_desktop_config.json` | 1 (agent-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 620 | [conorcmack/cryptlz](https://github.com/conorcmack/cryptlz) | `tools/vault-mcp-server/claude_desktop_config.json` | 1 (vault-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 621 | [pradeepmisal/ClashGuard-MCP](https://github.com/pradeepmisal/ClashGuard-MCP) | `docs/claude_desktop_config.json` | 1 (clashguard) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 622 | [JasonHHouse/MovieMCP](https://github.com/JasonHHouse/MovieMCP) | `claude_desktop_config.json` | 1 (movie-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 623 | [Anonymous6214/config](https://github.com/Anonymous6214/config) | `claude/claude_desktop_config.json` | 2 (windows-cli, text-editor) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 624 | [ssql2014/mcp4eda](https://github.com/ssql2014/mcp4eda) | `verible-mcp/examples/claude_desktop_config.json` | 1 (verible) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 625 | [coinbase/agentkit](https://github.com/coinbase/agentkit) | `typescript/create-onchain-agent/templates/mcp/src/agentkit/evm/viem/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 626 | [nickweedon/partsbox_mcp](https://github.com/nickweedon/partsbox_mcp) | `claude_desktop_config.json.example` | 1 (partsbox) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-partsbox` |
| 627 | [glazperle/kimai_mcp](https://github.com/glazperle/kimai_mcp) | `examples/claude_desktop_config.json` | 1 (kimai) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 628 | [MarioDeFelipe/sap-datasphere-mcp](https://github.com/MarioDeFelipe/sap-datasphere-mcp) | `examples/claude_desktop_config.json` | 1 (sap-datasphere) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 629 | [sonicaj/tn_mcp](https://github.com/sonicaj/tn_mcp) | `claude_desktop_config.json` | 1 (truenas-docs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 630 | [azender1/SafeAgent](https://github.com/azender1/SafeAgent) | `claude_desktop_config.json` | 1 (safeagent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 631 | [Harrish-Selvarajah/currency_mcp](https://github.com/Harrish-Selvarajah/currency_mcp) | `claude_desktop_config.json` | 1 (currency) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 632 | [APIBrasil/apibrasil-mcp-client](https://github.com/APIBrasil/apibrasil-mcp-client) | `clientes-ai/claude_desktop_config.json` | 1 (apibrasil) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 633 | [xkiranj/playwright-universal-mcp](https://github.com/xkiranj/playwright-universal-mcp) | `examples/claude_desktop_config.json` | 1 (browser) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 634 | [bountyyfi/ProjectMemory](https://github.com/bountyyfi/ProjectMemory) | `config/claude_desktop_config.json` | 1 (project-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 635 | [can-acar/rust-linkedin-mcp-branch](https://github.com/can-acar/rust-linkedin-mcp-branch) | `claude_desktop_config.json` | 1 (linkedin) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 636 | [pathcosmos/take_this_red_pill](https://github.com/pathcosmos/take_this_red_pill) | `python/claude_desktop_config.json` | 1 (weather-python) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 637 | [ttjslbz001/akshare_mcp_server](https://github.com/ttjslbz001/akshare_mcp_server) | `claude_desktop_config.json` | 1 (akshare-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 638 | [k3nn3dy-ai/screenshot_mcp](https://github.com/k3nn3dy-ai/screenshot_mcp) | `claude_desktop_config.json.example` | 1 (screenshot-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 639 | [zach22-1999/lingxing-mcp](https://github.com/zach22-1999/lingxing-mcp) | `mcp-servers/lingxing-openapi/packages/windows-teammate-kit/04_claude_desktop_config.json` | 1 (lingxing_mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 640 | [Bmcbob76/ECHO-PRIME-OMEGA](https://github.com/Bmcbob76/ECHO-PRIME-OMEGA) | `servers/ARCHIVE_CLEANUP/claude_desktop_config.json` | 3 (epcp30-desktop-commander-xv4, windows-api-bridge, crystal-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 641 | [akartb/computer-use](https://github.com/akartb/computer-use) | `config/claude_desktop_config.json` | 1 (computer-use) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 642 | [mnisenbaum/2026-academy-days](https://github.com/mnisenbaum/2026-academy-days) | `arquivos-de-configuracao/claude-desktop/claude_desktop_config.json` | 1 (Cisco Modeling Labs (CML)) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 643 | [sakashita44/portable-node-mcp-runner](https://github.com/sakashita44/portable-node-mcp-runner) | `examples/claude_desktop_config.json` | 2 (local-mcp, remote-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 644 | [jamesburton/AspireMcpServer](https://github.com/jamesburton/AspireMcpServer) | `claude_desktop_config.json` | 2 (aspire, aspire-dev) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 645 | [bala-2305/echo-mcp](https://github.com/bala-2305/echo-mcp) | `claude_desktop_config.json` | 1 (echo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 646 | [kdjordan/voip-accelerator](https://github.com/kdjordan/voip-accelerator) | `.claude/claude_desktop_config.json` | 2 (supabase, stripe) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 647 | [hanzdi/mcp-research-server](https://github.com/hanzdi/mcp-research-server) | `claude_desktop_config.json` | 1 (research-paper-analyzer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 648 | [kmaurinjones/flux-mcp](https://github.com/kmaurinjones/flux-mcp) | `examples/claude_desktop_config.json` | 1 (flux-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 649 | [czirakim/Netscaler.MCP.server](https://github.com/czirakim/Netscaler.MCP.server) | `claude_desktop_config.json` | 1 (NetscalerMcpServer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 650 | [henrardo/llm-graph-builder-mcp](https://github.com/henrardo/llm-graph-builder-mcp) | `claude_desktop_config.json` | 2 (llm-graph-builder, neo4j-cypher) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 651 | [tenable/mcp-blog](https://github.com/tenable/mcp-blog) | `claude_desktop_config.json` | 1 (tenable_mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 652 | [tinatuazon/ai-agent-dev-setup-tina](https://github.com/tinatuazon/ai-agent-dev-setup-tina) | `mcp-configs/claude_desktop_config.json` | 3 (bootcamp-rag, tech-bootcamp-consultations, rolldice) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-bootcamp-rag` |
| 653 | [JacquesGariepy/game-assistant-mcp](https://github.com/JacquesGariepy/game-assistant-mcp) | `claude_desktop_config.json` | 1 (game-assistant) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 654 | [silvermete0r/local_mcp_pypi_packages_audit](https://github.com/silvermete0r/local_mcp_pypi_packages_audit) | `claude_desktop_config.json` | 1 (gradio) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 655 | [tky0065/springdocs-mcp](https://github.com/tky0065/springdocs-mcp) | `claude_desktop_config.json` | 1 (spring-docs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 656 | [pkarpovich/environment](https://github.com/pkarpovich/environment) | `dotfiles/claude_desktop_config.json` | 1 (mcpjungle) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 657 | [Adarsh-codesOP/ACE](https://github.com/Adarsh-codesOP/ACE) | `claude_desktop_config.json` | 1 (ace-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 658 | [ChaseKolozsy/AnkiChat](https://github.com/ChaseKolozsy/AnkiChat) | `claude_desktop_config.json` | 1 (anki-api) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 659 | [MaterializeInc/materialize-mcp-server](https://github.com/MaterializeInc/materialize-mcp-server) | `developers/example_configs/claude_desktop_config.json` | 1 (materialize) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 660 | [RezaRazm/eBay-mcp](https://github.com/RezaRazm/eBay-mcp) | `examples/claude_desktop_config.json` | 1 (ebay) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 661 | [Picom-code/mcp](https://github.com/Picom-code/mcp) | `claude_desktop_config.json` | 3 (weather, web-search, github2) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 662 | [yevhen-kalyna/autoria-mcp](https://github.com/yevhen-kalyna/autoria-mcp) | `examples/claude_desktop_config.json` | 1 (autoria) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 663 | [aigovops-foundation/aigovops-beacon](https://github.com/aigovops-foundation/aigovops-beacon) | `mcp/claude_desktop_config.json` | 1 (aigovops-beacon) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 664 | [praj-tarun/langchain-mcp-server](https://github.com/praj-tarun/langchain-mcp-server) | `claude_desktop_config.json` | 1 (simple-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 665 | [roccho-dev/home](https://github.com/roccho-dev/home) | `.config/claudedesktop/claude_desktop_config.json` | 3 (desktop_commander, llm_functions, excel) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 666 | [dimitrov-d/solana-limit-order-mcp](https://github.com/dimitrov-d/solana-limit-order-mcp) | `claude_desktop_config.json` | 1 (solana-limit-order-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 667 | [Horace-Maxwell/horosa-skill](https://github.com/Horace-Maxwell/horosa-skill) | `horosa-skill/examples/clients/claude_desktop_config.json` | 1 (horosa) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 668 | [andresublime/frz_fruit](https://github.com/andresublime/frz_fruit) | `Export-Data/claude_desktop_config.json` | 1 (peru-exports) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 669 | [cata-g/anaf-mcp-server](https://github.com/cata-g/anaf-mcp-server) | `examples/claude_desktop_config.json` | 1 (anaf-company-data) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 670 | [jeremiasdavison/ai-onboarding-agent](https://github.com/jeremiasdavison/ai-onboarding-agent) | `claude_desktop_config.json` | 1 (ai-onboarding-agent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 671 | [Bedrockdude10/Booker](https://github.com/Bedrockdude10/Booker) | `agent-demo/booker_mcp/claude_desktop_config.json` | 1 (booker) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 672 | [oogalieboogalie/OogalieBoogalies-MCP-MonoRepo-Extravaganza](https://github.com/oogalieboogalie/OogalieBoogalies-MCP-MonoRepo-Extravaganza) | `examples/claude_desktop_config.json` | 2 (jules, supabase) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 673 | [cerinawithasea1/sanctuarytreethatbreathes](https://github.com/cerinawithasea1/sanctuarytreethatbreathes) | `mcp/telegram-mcp/claude_desktop_config.json` | 1 (telegram-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 674 | [Meer-Abdulrehman/Scholar-Ai-Web-application](https://github.com/Meer-Abdulrehman/Scholar-Ai-Web-application) | `mcp_server/claude_desktop_config.json` | 1 (student-advisor) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 675 | [chrishm00/efs-ai-analyzer](https://github.com/chrishm00/efs-ai-analyzer) | `config/claude_desktop_config.json` | 1 (efs-ai-analyzer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 676 | [hijaz/postmancer](https://github.com/hijaz/postmancer) | `examples/claude_desktop_config.json` | 1 (postmancer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 677 | [sburdges-eng/KmiDi](https://github.com/sburdges-eng/KmiDi) | `_archive/KmiDi_FINAL/python/mcp_todo/configs/claude_desktop_config.json` | 1 (mcp-todo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 678 | [marc-hanheide/redact_mcp](https://github.com/marc-hanheide/redact_mcp) | `claude_desktop_config.json` | 1 (pdf-redaction) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 679 | [likerberi/ridge_exam_mcp](https://github.com/likerberi/ridge_exam_mcp) | `claude_desktop_config.json` | 1 (ridge-analysis) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 680 | [darshan-sharma4/DataLens](https://github.com/darshan-sharma4/DataLens) | `claude_desktop_config.json` | 1 (datalens-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 681 | [vidhi1203/life-os](https://github.com/vidhi1203/life-os) | `claude_desktop_config.json` | 4 (meal, workout, finance +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 682 | [dmorav1/MCP-Demo](https://github.com/dmorav1/MCP-Demo) | `claude_desktop_config.json` | 1 (conversational-data) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 683 | [cs97jjm3/ba-workflow-tools](https://github.com/cs97jjm3/ba-workflow-tools) | `claude_desktop_config.json` | 1 (ba-workflow-tools) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 684 | [southern-dust/duckduckgo-mcp-server-py](https://github.com/southern-dust/duckduckgo-mcp-server-py) | `examples/claude_desktop_config.json` | 3 (duckduckgo-search-stdio, duckduckgo-search-http, duckduckgo-search-docker) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 685 | [ThinkWithOps/ai-devops-systems-lab](https://github.com/ThinkWithOps/ai-devops-systems-lab) | `projects/03-ai-devops-mcp-server/config/claude_desktop_config.json` | 1 (ai-devops) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 686 | [horustechltd/horus-flow-mcp](https://github.com/horustechltd/horus-flow-mcp) | `configs/claude_desktop_config.json` | 1 (horus-flow) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 687 | [levythelearner/mcp_demo](https://github.com/levythelearner/mcp_demo) | `claude_desktop_config.json` | 2 (math-demo, weather-demo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 688 | [AndriiOzemko/MCP-Server-Test](https://github.com/AndriiOzemko/MCP-Server-Test) | `claude_desktop_config.json` | 1 (notes) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 689 | [Rahulgillella22/multichannel_distribution](https://github.com/Rahulgillella22/multichannel_distribution) | `grabon_mcp/claude_desktop_config.json` | 1 (grabon-deal-distributor) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 690 | [TomAs-1226/mcp-guard](https://github.com/TomAs-1226/mcp-guard) | `fixtures/configs/claude_desktop_config.json` | 1 (hello-http) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 691 | [wilcor7190/mcp-microservice-poc](https://github.com/wilcor7190/mcp-microservice-poc) | `demo-mcp-3-standards-validator_nodejs/claude_desktop_config.json` | 1 (nodejs-validator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 692 | [Pauloeduspbr/viralanalyzer-cli](https://github.com/Pauloeduspbr/viralanalyzer-cli) | `claude_desktop_config.json` | 1 (viralanalyzer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 693 | [semcod/sumd](https://github.com/semcod/sumd) | `examples/mcp/claude_desktop_config.json` | 1 (sumd) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 694 | [BjornMelin/mcp-search-hub](https://github.com/BjornMelin/mcp-search-hub) | `examples/claude-config/claude_desktop_config.json` | 1 (mcp-search-hub) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 695 | [bangoc123/protonx-agent-01-class](https://github.com/bangoc123/protonx-agent-01-class) | `Day-4/resource-demo/claude_desktop_config.json` | 1 (myapp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 696 | [razeevascx/trading212-mcp](https://github.com/razeevascx/trading212-mcp) | `claude_desktop_config.json` | 1 (trading212) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 697 | [reasoner-com/mcp-server](https://github.com/reasoner-com/mcp-server) | `claude_desktop_config.json` | 1 (mind-reasoner) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 698 | [PWereh/claude-mcp-get](https://github.com/PWereh/claude-mcp-get) | `templates/claude_desktop_config.json` | 4 (filesystem, github, memory +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 699 | [fstrauf/pageseeds-cli](https://github.com/fstrauf/pageseeds-cli) | `packages/seo-content-cli/claude_desktop_config.json` | 1 (seo-content) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 700 | [MacHu-GWU/learn_mcp-project](https://github.com/MacHu-GWU/learn_mcp-project) | `claude_desktop_config.json` | 1 (weather) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 701 | [dgenio/contextweaver](https://github.com/dgenio/contextweaver) | `examples/recipes/claude_desktop_config.json` | 1 (contextweaver-gateway) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 702 | [iowarp/clio-kit](https://github.com/iowarp/clio-kit) | `claude_desktop_config.json` | 21 (clio-adios, clio-arxiv, clio-chronolog +18 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 703 | [Paretofilm/amplify-docs-mcp-server](https://github.com/Paretofilm/amplify-docs-mcp-server) | `claude_desktop_config.json` | 1 (amplify-gen-2-nextjs-docs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 704 | [baraluga/sprout-headless](https://github.com/baraluga/sprout-headless) | `claude_desktop_config.json` | 1 (engie-hr) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 705 | [StevenGeller/youtube-transcriber-mcp](https://github.com/StevenGeller/youtube-transcriber-mcp) | `claude_desktop_config.json` | 1 (youtube-transcriber-enhanced) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 706 | [julianpinedayyz/wealth-finder-claude-mcp](https://github.com/julianpinedayyz/wealth-finder-claude-mcp) | `docs/claude_desktop_config.json` | 1 (wealth-finder-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 707 | [amberyu1227/pfSense-MCPserver-Wazuh-server](https://github.com/amberyu1227/pfSense-MCPserver-Wazuh-server) | `01-AI-Threat-Hunter/setup/claude_desktop_config.json` | 1 (wazuh) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 708 | [Ayush-Mishra-7/MCP-server-Cisco](https://github.com/Ayush-Mishra-7/MCP-server-Cisco) | `claude_desktop_config.json` | 1 (cisco-docs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 709 | [pim97/mcp-server-scrappey](https://github.com/pim97/mcp-server-scrappey) | `claude_desktop_config.json` | 1 (scrappey) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 710 | [kofujimura/obniz-led-skill](https://github.com/kofujimura/obniz-led-skill) | `claude_desktop_config.json` | 1 (obniz-led) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 711 | [abhifetch/python-google-calendar-mcp](https://github.com/abhifetch/python-google-calendar-mcp) | `python-calendar-mcp-uagents/claude_desktop_config.json` | 1 (google-calendar) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 712 | [gwyer/hybrid-rag-project](https://github.com/gwyer/hybrid-rag-project) | `config/claude_desktop_config.json` | 1 (hybrid-rag) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-hybrid-rag` |
| 713 | [myownipgit/procurement-database-etl](https://github.com/myownipgit/procurement-database-etl) | `config/claude_desktop_config.json` | 2 (sqlite-operational, sqlite-analytics) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 714 | [anilbolke/PRODEMS](https://github.com/anilbolke/PRODEMS) | `WebContent/claude/claude_desktop_config.json` | 1 (cashfree) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 715 | [khuynh22/mcp-wireshark](https://github.com/khuynh22/mcp-wireshark) | `docs/mcp_configs/claude_desktop_config.json` | 1 (wireshark) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 716 | [Tiosa205g/Open-AutoGLM-mcp](https://github.com/Tiosa205g/Open-AutoGLM-mcp) | `claude_desktop_config.json` | 1 (phone-agent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 717 | [joaogabriel43/java-mcp-hub](https://github.com/joaogabriel43/java-mcp-hub) | `claude_desktop_config.json` | 1 (JavaMCPHub) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 718 | [BLKOUTUK/blkout-event-agent](https://github.com/BLKOUTUK/blkout-event-agent) | `mcp-server/claude_desktop_config.json` | 2 (weather, file-system) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 719 | [awmatheson/dh-mcp](https://github.com/awmatheson/dh-mcp) | `claude_desktop_config.json` | 1 (mtb-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 720 | [gaixen/CredTech](https://github.com/gaixen/CredTech) | `data_ingestion/claude_desktop_config.json` | 1 (yfinance) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 721 | [er-pritamdas/AI-Automation](https://github.com/er-pritamdas/AI-Automation) | `03. MCP Server with AgentPass AI/claude_desktop_config.json` | 1 (Demo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 722 | [micsapp/micstec-skills](https://github.com/micsapp/micstec-skills) | `mcp-servers/mcp-excalidraw/claude_desktop_config.json` | 1 (mcp_excalidraw) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 723 | [anudeepadi/personal-brain-mcp](https://github.com/anudeepadi/personal-brain-mcp) | `claude_desktop_config.json` | 1 (personal-brain) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 724 | [ry-ops/DriveIQ](https://github.com/ry-ops/DriveIQ) | `mcp/claude_desktop_config.json` | 1 (driveiq) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 725 | [daffy0208/ai-dev-standards](https://github.com/daffy0208/ai-dev-standards) | `.claude/claude_desktop_config.json` | 54 (framework-content, framework-orchestrator, 3d-asset-manager-mcp +51 more) | 0 | 0 | 5 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-vector-database-mcp`; MEDIUM: `CONTEXT-EXT-FETCH-knowledge-base-mcp`; MEDIUM: `CONTEXT-EXT-FETCH-domain-memory-agent` |
| 726 | [Lepochi/superkraftmat_memorygraph](https://github.com/Lepochi/superkraftmat_memorygraph) | `mcp-server/claude_desktop_config.json` | 1 (superkraft-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 727 | [asfalanoij/csirt-command-center](https://github.com/asfalanoij/csirt-command-center) | `~/.claude/claude_desktop_config.json` | 1 (react-bits) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 728 | [pr1m8/wraquant](https://github.com/pr1m8/wraquant) | `mcp/examples/claude_desktop_config.json` | 3 (wraquant, openbb, duckdb) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 729 | [dasein108/freqtrade_dev_mcp](https://github.com/dasein108/freqtrade_dev_mcp) | `examples/claude_desktop_config.json` | 1 (freqtrade) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 730 | [SAM18-Bot/AI-Context-Switcher](https://github.com/SAM18-Bot/AI-Context-Switcher) | `aics-mcp-server/claude_desktop_config.json` | 1 (aics-context) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 731 | [wsekete/PDFParseV2](https://github.com/wsekete/PDFParseV2) | `claude_desktop_config.json` | 1 (pdf-field-modifier) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 732 | [aussiearef/mcp-acp](https://github.com/aussiearef/mcp-acp) | `mcp/examples/config/claude_desktop_config.json` | 2 (weather, Greetings) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 733 | [jx-codes/mcp-rpc-bridge](https://github.com/jx-codes/mcp-rpc-bridge) | `claude_desktop_config.json` | 1 (mcp-rpc-bridge) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 734 | [3phraimY/Claude-Tool-Example](https://github.com/3phraimY/Claude-Tool-Example) | `claude_desktop_config.json` | 1 (file-writer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 735 | [tran196/mcp-starter-kit](https://github.com/tran196/mcp-starter-kit) | `examples/claude_desktop_config.json` | 1 (mcp-starter-kit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 736 | [modbender/skill-library-mcp](https://github.com/modbender/skill-library-mcp) | `data/meshtastic-skill/references/claude_desktop_config.json` | 1 (meshtastic) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 737 | [samfreeman/claude-home](https://github.com/samfreeman/claude-home) | `claude_desktop_config.json` | 3 (pbi-mcp-server, bitbucket-mcp-server, youtube-transcript) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 738 | [up2itnow0822/agentpay-mcp](https://github.com/up2itnow0822/agentpay-mcp) | `claude_desktop_config.json` | 1 (clawpay) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 739 | [Copystrike/universal-mcp-rag](https://github.com/Copystrike/universal-mcp-rag) | `claude_desktop_config.json` | 3 (ui-library, auth-library, db-library) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 740 | [vjsingh1984/victor](https://github.com/vjsingh1984/victor) | `examples/claude_desktop_config.json` | 5 (victor, victor-coding, victor-safe +2 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 741 | [bmsvinci1729/mcp-stock-analyzer](https://github.com/bmsvinci1729/mcp-stock-analyzer) | `claude_desktop_config.json` | 3 (stock-scraping, twitter, database) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 742 | [DmitriyMutagen/mcp-swiss-ephemeris](https://github.com/DmitriyMutagen/mcp-swiss-ephemeris) | `examples/claude_desktop_config.json` | 1 (swiss-ephemeris) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 743 | [Yosef-Ali/compasstio-ai](https://github.com/Yosef-Ali/compasstio-ai) | `claude_desktop_config.json` | 4 (mcp-installer, mcp-youtube, desktop-commander +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 744 | [Misterbra/fusion360-claude-ultimate](https://github.com/Misterbra/fusion360-claude-ultimate) | `AppDataRoamingClaude/claude_desktop_config.json` | 1 (fusion_mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 745 | [TarekRaafat/skalex](https://github.com/TarekRaafat/skalex) | `examples/mcp-agent-server/claude_desktop_config.json` | 1 (skalex) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 746 | [Dezocode/mcp-system](https://github.com/Dezocode/mcp-system) | `configs/claude_desktop_config.json` | 1 (mcp-system) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 747 | [cpateldev/TodoMCPServer](https://github.com/cpateldev/TodoMCPServer) | `ClaudeDesktopConfig/claude_desktop_config.json` | 1 (TodoMcpHttpServer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 748 | [anjijava16/mcp_servers](https://github.com/anjijava16/mcp_servers) | `claude_desktop_config.json` | 2 (greeter, weather) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 749 | [Kshitijbhatt1998/SourceGuard](https://github.com/Kshitijbhatt1998/SourceGuard) | `mcp_server/claude_desktop_config.json` | 1 (sourceguard) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 750 | [aarav-12/DevOPS-AI-Agent](https://github.com/aarav-12/DevOPS-AI-Agent) | `claude_desktop_config.json` | 1 (devops-demo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 751 | [SadhakKumar/ZK_location_verifier](https://github.com/SadhakKumar/ZK_location_verifier) | `newagentkit/agentkit/typescript/create-onchain-agent/templates/mcp/src/agentkit/evm/viem/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 752 | [Tanishq67m/VisionAPI](https://github.com/Tanishq67m/VisionAPI) | `claude_desktop_config.json` | 1 (vision-api) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 753 | [BryanTheLai/anydesk-agent](https://github.com/BryanTheLai/anydesk-agent) | `examples/claude_desktop_config.json` | 1 (remoteuse) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 754 | [adolfo-martin/angular-projects](https://github.com/adolfo-martin/angular-projects) | `2025-06-02 MCP Pokemon/claude_desktop_config.json` | 1 (pokeapi) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 755 | [RajAbey68/DeepSeekHermes](https://github.com/RajAbey68/DeepSeekHermes) | `mcp-stdio/examples/claude_desktop_config.json` | 1 (deephermes) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 756 | [thammuio/xtractic-ai](https://github.com/thammuio/xtractic-ai) | `mcp/examples/smm-mcp/claude_desktop_config.json` | 1 (ssm-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 757 | [akashsp7/jobhunt-email-mcp](https://github.com/akashsp7/jobhunt-email-mcp) | `claude_desktop_config.json` | 1 (jobhunt-email-intelligence) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 758 | [FOX2920/Aplus-MCP](https://github.com/FOX2920/Aplus-MCP) | `claude_desktop_config.json` | 1 (wework-task-analysis) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 759 | [qinx18/compiler-mcp-server](https://github.com/qinx18/compiler-mcp-server) | `claude_desktop_config.json` | 1 (compiler) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 760 | [mauryaland/rlm-claude-desktop](https://github.com/mauryaland/rlm-claude-desktop) | `config/claude_desktop_config.json` | 1 (rlm) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 761 | [eyoel-feleke/cognitive-canvas](https://github.com/eyoel-feleke/cognitive-canvas) | `claude_desktop_config.json` | 1 (contentgraph-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 762 | [modellers/mcp-duffel-travels](https://github.com/modellers/mcp-duffel-travels) | `claude_desktop_config.json` | 1 (duffel-travels) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 763 | [mrvollger/dotfiles](https://github.com/mrvollger/dotfiles) | `.config/claude-desktop/claude_desktop_config.json` | 1 (basic-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 764 | [Saudadeeee/Godot-x-Aseprite-MCP-all](https://github.com/Saudadeeee/Godot-x-Aseprite-MCP-all) | `Godot-MCP/claude_desktop_config.json` | 1 (godot-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 765 | [Mbanksbey/TEQUMSA_NEXUS](https://github.com/Mbanksbey/TEQUMSA_NEXUS) | `claude_desktop_config.json` | 2 (tequmsa-consciousness-cascade, tequmsa-zpe-dna) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 766 | [yesserkira/Advanced-blender-mcp-bridge](https://github.com/yesserkira/Advanced-blender-mcp-bridge) | `examples/claude_desktop_config.json` | 1 (blender) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 767 | [NovaAI-innovation/csv-mcp-server](https://github.com/NovaAI-innovation/csv-mcp-server) | `claude_desktop_config.json` | 1 (csv-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 768 | [YunhaoDou/mcp-weread](https://github.com/YunhaoDou/mcp-weread) | `example/claude_desktop_config.json` | 1 (weread) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 769 | [avwsolutions/example-security-scan-elasticsearch-mcp](https://github.com/avwsolutions/example-security-scan-elasticsearch-mcp) | `sample_config/claude_desktop_config.json` | 1 (elasticsearch-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 770 | [wilcor7190/mcp-microservice-poc](https://github.com/wilcor7190/mcp-microservice-poc) | `demo-mcp-3-standards-validatororquestador/claude_desktop_config.json` | 1 (standards-orchestrator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 771 | [FRESHSK/mcp_onenote](https://github.com/FRESHSK/mcp_onenote) | `claude_desktop_config.json` | 1 (onenote) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 772 | [brainupgrade-in/mcp-server-typescript-starter](https://github.com/brainupgrade-in/mcp-server-typescript-starter) | `examples/claude_desktop_config.json` | 1 (greeting) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 773 | [NanoNets/docstrange](https://github.com/NanoNets/docstrange) | `mcp_server_module/claude_desktop_config.json` | 1 (docstrange) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 774 | [gaebalai/gieok](https://github.com/gaebalai/gieok) | `templates/mcp/claude_desktop_config.json.template` | 1 (gieok-wiki) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 775 | [Sena-Services/frappe-mcp-server](https://github.com/Sena-Services/frappe-mcp-server) | `claude_desktop_config.json.example` | 1 (frappe) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 776 | [dgallula/lab9-mcp-server-crewai](https://github.com/dgallula/lab9-mcp-server-crewai) | `Demos/4 - MCP/claude_desktop_config.json` | 2 (getWeatherServer, nameOriginServer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 777 | [anoushka45/NextJs-Portfolio](https://github.com/anoushka45/NextJs-Portfolio) | `public/docs/ck docs/mcp_claude_desktop_config.json` | 1 (cortexkitchen) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 778 | [sandraschi/virtualization-mcp](https://github.com/sandraschi/virtualization-mcp) | `claude_desktop_config.json` | 1 (virtualization-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 779 | [deachne/WL8-pkm](https://github.com/deachne/WL8-pkm) | `mcp/wl8-docs/updated_claude_desktop_config.json` | 1 (wl8-docs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 780 | [hanisaf/mcp_demo](https://github.com/hanisaf/mcp_demo) | `windows_claude_desktop_config.json` | 2 (santa, research assistant) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 781 | [itisaby/Meridian](https://github.com/itisaby/Meridian) | `mcp-server/claude_desktop_config.json` | 1 (meridian-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 782 | [umuterturk/mcp-proto](https://github.com/umuterturk/mcp-proto) | `go-version/mcp_config_examples/claude_desktop_config.json` | 1 (proto-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 783 | [dionysuzx/forkcast-data](https://github.com/dionysuzx/forkcast-data) | `agent/mcp-configs/claude_desktop_config.json` | 1 (forkcast) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 784 | [ThomasRohde/llm-wasm-sandbox](https://github.com/ThomasRohde/llm-wasm-sandbox) | `examples/mcp_claude_desktop_config.json` | 1 (llm-wasm-sandbox) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 785 | [rexresurreccionhome/mcp-servers](https://github.com/rexresurreccionhome/mcp-servers) | `hello-world/example-claude_desktop_config.json` | 1 (hello-world) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 786 | [Saudadeeee/Godot-x-Aseprite-MCP-all](https://github.com/Saudadeeee/Godot-x-Aseprite-MCP-all) | `claude_desktop_config.json` | 2 (aseprite, godot-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 787 | [alch3mistdev/obsidian-mcp-ultra](https://github.com/alch3mistdev/obsidian-mcp-ultra) | `examples/claude_desktop_config.json` | 1 (obsidian-mcp-ultra) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 788 | [cloudyuga/mastering-genai-w-python](https://github.com/cloudyuga/mastering-genai-w-python) | `Module-13-Model-Context-Protocol/1-Claude_Desktop_Integration/claude_desktop_config.json` | 3 (weather, news_weather, hr) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 789 | [binwalmanish/sample-mq-mcp](https://github.com/binwalmanish/sample-mq-mcp) | `claude_desktop_config.json` | 1 (mq-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 790 | [addodelgrossi/reitbrazil](https://github.com/addodelgrossi/reitbrazil) | `examples/claude_desktop_config.json` | 1 (reitbrazil) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 791 | [goPluto-ai/gopluto-ai-mcp](https://github.com/goPluto-ai/gopluto-ai-mcp) | `clients/claude_desktop_config.json.example` | 1 (gopluto) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 792 | [pursky7468/mcp-command-execution-server](https://github.com/pursky7468/mcp-command-execution-server) | `claude_desktop_config.json` | 1 (command-execution) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 793 | [mustafagadi/MCP](https://github.com/mustafagadi/MCP) | `claude_desktop_config.json` | 1 (outlook) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 794 | [Razpines/UnityRAG](https://github.com/Razpines/UnityRAG) | `examples/claude_desktop_config.json` | 1 (unity-docs) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-unity-docs` |
| 795 | [Akshat-Gupta04/CodeMind-AI-Powered-Code-Knowledge-Retrieval-System](https://github.com/Akshat-Gupta04/CodeMind-AI-Powered-Code-Knowledge-Retrieval-System) | `claude_desktop_config.json` | 1 (CodeMind) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 796 | [rocket-martue/wordpress-handbook-mcp](https://github.com/rocket-martue/wordpress-handbook-mcp) | `claude_desktop_config.json.example` | 1 (wordpress-handbook) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 797 | [alejandroBallesterosC/document-edit-mcp](https://github.com/alejandroBallesterosC/document-edit-mcp) | `claude_desktop_config.json` | 1 (document_operations) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 798 | [aiexplorations/docx-mcp](https://github.com/aiexplorations/docx-mcp) | `claude_desktop_config.json` | 1 (docx-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 799 | [bmaranan75/shopping-assistant-mcp](https://github.com/bmaranan75/shopping-assistant-mcp) | `examples/claude_desktop_config.json` | 1 (shopping-assistant) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 800 | [Mulisa007/main](https://github.com/Mulisa007/main) | `claude_config/claude_desktop_config.json` | 1 (memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 801 | [essences/CodeInterpreterTS_MCP](https://github.com/essences/CodeInterpreterTS_MCP) | `config/claude_desktop_config.json` | 1 (typescript-code-interpreter) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 802 | [inspirehep/inspirehep-mcp](https://github.com/inspirehep/inspirehep-mcp) | `claude_desktop_config.json.example` | 1 (inspirehep) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 803 | [wybaeb/edu_mcp_telegram](https://github.com/wybaeb/edu_mcp_telegram) | `claude_desktop_config.json` | 1 (educational-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 804 | [ajeetraina/talk-demos](https://github.com/ajeetraina/talk-demos) | `mcp-demo/neo4j/claude_desktop_config.json` | 1 (neo4j) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 805 | [blake365/macrostrat-mcp](https://github.com/blake365/macrostrat-mcp) | `claude_desktop_config.json` | 1 (macrostrat) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 806 | [matiasvagli/mcp-server-travel](https://github.com/matiasvagli/mcp-server-travel) | `claude_desktop_config.json.example` | 1 (travel) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 807 | [turnono/sim](https://github.com/turnono/sim) | `claude_desktop_config.json` | 1 (firebase) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 808 | [definite-app/definite-mcp](https://github.com/definite-app/definite-mcp) | `claude_desktop_config.json` | 1 (definite-api) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 809 | [NotAwar/mcp-demo](https://github.com/NotAwar/mcp-demo) | `claude_desktop_config.json` | 2 (weather, airbnb) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 810 | [AyushRatan1/Mcp-polymarket](https://github.com/AyushRatan1/Mcp-polymarket) | `~/Library/Application Support/Claude/claude_desktop_config.json` | 1 (polymarket-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 811 | [kenwalger/mcp-forensic-analyzer](https://github.com/kenwalger/mcp-forensic-analyzer) | `claude_desktop_config.json` | 1 (forensic-analyser) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 812 | [ARMeeru/vps-mcp](https://github.com/ARMeeru/vps-mcp) | `templates/claude_desktop_config.json` | 1 (vps-manager) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 813 | [Zaaacqwq/BalatroMCP](https://github.com/Zaaacqwq/BalatroMCP) | `mcp_configs/claude_desktop_config.json` | 1 (balatro) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 814 | [jhl-labs/sepilot-cli](https://github.com/jhl-labs/sepilot-cli) | `sepilot/mcp/claude_desktop_config.json.template` | 1 (sepilot) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 815 | [daffy0208/ai-dev-standards](https://github.com/daffy0208/ai-dev-standards) | `.claude/claude_desktop_config.json.new` | 49 (3d-asset-manager-mcp, accessibility-checker-mcp, agent-orchestrator-mcp +46 more) | 0 | 0 | 4 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-knowledge-base-mcp`; MEDIUM: `CONTEXT-EXT-FETCH-vector-database-mcp` |
| 816 | [efij/secure-claude-code](https://github.com/efij/secure-claude-code) | `runtimes/claude-desktop/claude_desktop_config.json.tmpl` | 1 (stallion) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 817 | [makkader/mcp-tube-transcriber](https://github.com/makkader/mcp-tube-transcriber) | `template_claude_desktop_config.json` | 1 (mcp-tube-transcriber) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 818 | [BenjaminWolfe/dotfiles](https://github.com/BenjaminWolfe/dotfiles) | `claude/claude_desktop_config.json.template` | 1 (obsidian) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 819 | [juliantorr-es/Anigma](https://github.com/juliantorr-es/Anigma) | `anigma/Docs/LLM/claude_desktop_config.json.template` | 1 (anigma) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 820 | [nixlim/zetmem](https://github.com/nixlim/zetmem) | `config/claude_desktop_config.json` | 1 (zetmem-augmented) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 821 | [CoreAspectStu/claude-context-manager](https://github.com/CoreAspectStu/claude-context-manager) | `config/claude_desktop_config.json` | 1 (minima) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 822 | [ry-ops/k3s-mcp-server](https://github.com/ry-ops/k3s-mcp-server) | `CLAUDE_DESKTOP_CONFIG.json` | 1 (k3s) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 823 | [Mergoth/Presentations-local-MCP](https://github.com/Mergoth/Presentations-local-MCP) | `docs/claude_desktop_config.json` | 1 (markdown-to-pptx) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 824 | [zackradisic/mcpdbg](https://github.com/zackradisic/mcpdbg) | `claude_desktop_config.json` | 1 (mcp-debugger) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 825 | [AnmolRajpoot25/MCP_server_architecture](https://github.com/AnmolRajpoot25/MCP_server_architecture) | `servers/terminal_server/claude_desktop_config.json.macos.example` | 1 (terminal-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 826 | [cote/chatdm](https://github.com/cote/chatdm) | `template-claude_desktop_config.json` | 1 (chatdm) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 827 | [cefavn/vuln-analysis-RAG](https://github.com/cefavn/vuln-analysis-RAG) | `claude_desktop_config.json` | 2 (ida-pro-mcp, rag-knowledge-gd2) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-ida-pro-mcp`; MEDIUM: `CONTEXT-EXT-FETCH-rag-knowledge-gd2` |
| 828 | [cargofy/ATLAS](https://github.com/cargofy/ATLAS) | `claude_desktop_config.json` | 1 (atlas) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 829 | [PeterChen12/ff-brand-studio](https://github.com/PeterChen12/ff-brand-studio) | `claude_desktop_config.json` | 1 (ff-brand-studio) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 830 | [abhchoug/chim-mcp](https://github.com/abhchoug/chim-mcp) | `claude_desktop_config.json` | 1 (chim) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 831 | [hamzameer/ncbi-mcp-server](https://github.com/hamzameer/ncbi-mcp-server) | `claude_desktop_config.json` | 1 (NCBI Research Assistant) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-NCBI Research Assistant` |
| 832 | [matthieubosquet/solid-mcp](https://github.com/matthieubosquet/solid-mcp) | `claude_desktop_config.json` | 1 (solid-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 833 | [yaboyshades/super-alita](https://github.com/yaboyshades/super-alita) | `claude_desktop_config.json` | 1 (super-alita) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 834 | [guillaumegay13/fieldflow](https://github.com/guillaumegay13/fieldflow) | `claude_config_example/claude_desktop_config.json.bak` | 1 (pokeapi) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 835 | [sacahan/CasualMarket](https://github.com/sacahan/CasualMarket) | `examples/claude_desktop_config.json` | 1 (casual-market) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 836 | [oguzhan/bundestag-mcp](https://github.com/oguzhan/bundestag-mcp) | `examples/claude_desktop_config.json` | 1 (bundestag) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 837 | [iheb147/PoweredCodeReview](https://github.com/iheb147/PoweredCodeReview) | `claude_desktop_config.json` | 1 (pcr_mcp) | 0 | 0 | 1 | 0 | _context-limit rules only_ |
| 838 | [zygou-31/immich-mcp-broken](https://github.com/zygou-31/immich-mcp-broken) | `sample_claude_desktop_config.json` | 1 (immich) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 839 | [maxparez/electron_app](https://github.com/maxparez/electron_app) | `claude_desktop_config.json` | 4 (context7, github, sequential-thinking +1 more) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 840 | [trillium/ralph-cli](https://github.com/trillium/ralph-cli) | `claude_desktop_config.json` | 1 (ralph-cli) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 841 | [jeremyklein/claude-todo-app](https://github.com/jeremyklein/claude-todo-app) | `claude_desktop_config.json` | 1 (django-todo) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 842 | [serhabdel/hiel_excel_mcp](https://github.com/serhabdel/hiel_excel_mcp) | `claude_desktop_config.json` | 1 (hiel-excel-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 843 | [27priyanshu/MCP-Server-for-DevOps-on-WSL](https://github.com/27priyanshu/MCP-Server-for-DevOps-on-WSL) | `claude_desktop_config.json` | 2 (LeaveManagement, wsl-devops-management) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 844 | [jasondsmith72/Browser-use-claude-mcp](https://github.com/jasondsmith72/Browser-use-claude-mcp) | `claude_desktop_config.json` | 1 (browser-use-claude-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 845 | [moeloubani/visidata-mcp](https://github.com/moeloubani/visidata-mcp) | `claude_desktop_config.json` | 1 (visidata-local) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 846 | [jameshung2015/mcp_agent](https://github.com/jameshung2015/mcp_agent) | `claude_desktop_config.json` | 1 (github-stars) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 847 | [bahakizil/slack_mcp](https://github.com/bahakizil/slack_mcp) | `claude_desktop_config.json` | 1 (slack-ai-assistant) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 848 | [Borealin/ilspy-mcp-server](https://github.com/Borealin/ilspy-mcp-server) | `claude_desktop_config.json` | 1 (ilspy) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 849 | [JMartinCreuzburg/gns3_over_mcp](https://github.com/JMartinCreuzburg/gns3_over_mcp) | `examples/claude_desktop_config.json` | 1 (gns3) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 850 | [ecodelearn/MCP_SERVERS](https://github.com/ecodelearn/MCP_SERVERS) | `claude_desktop_config.json` | 2 (evolution_api, perplexity-ask) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 851 | [srinath1510/alltrails-mcp-server](https://github.com/srinath1510/alltrails-mcp-server) | `examples/claude_desktop_config.json` | 1 (alltrails_mcp_server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 852 | [matthewholliday/mcp-dice-roller](https://github.com/matthewholliday/mcp-dice-roller) | `examples/claude_desktop_config.json` | 1 (dice-roller) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 853 | [SobieskiCodes/claude-desktop-mcp-to-claude-agent](https://github.com/SobieskiCodes/claude-desktop-mcp-to-claude-agent) | `claude_desktop_config.json` | 2 (claude-code-bridge, mcp-server-chart) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 854 | [lynnlangit/precision-medicine-mcp](https://github.com/lynnlangit/precision-medicine-mcp) | `docs/getting-started/desktop-configs/claude_desktop_config.json` | 18 (fgbio, spatialtools, openimagedata +15 more) | 0 | 0 | 1 | 0 | _context-limit rules only_ |
| 855 | [dante1989/mcp-ccxt](https://github.com/dante1989/mcp-ccxt) | `examples/claude_desktop_config.json` | 1 (ccxt) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 856 | [DISSC-yale/dissc-agent-tooling](https://github.com/DISSC-yale/dissc-agent-tooling) | `tasks/claude_desktop_config.json` | 1 (data-visualization) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 857 | [VMSemchenko/mcp-notes-server-hometask](https://github.com/VMSemchenko/mcp-notes-server-hometask) | `claude_desktop_config.json` | 1 (notes) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 858 | [Jeevajk21/AI-Agent-for-apply-jobs](https://github.com/Jeevajk21/AI-Agent-for-apply-jobs) | `.claude/claude_desktop_config.json` | 1 (linkedin) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 859 | [tzf1003/skillmesh-client](https://github.com/tzf1003/skillmesh-client) | `mcp/client-config-examples/claude_desktop_config.json` | 1 (skillmesh) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 860 | [CharmingSteve/mcp-sefaria-server](https://github.com/CharmingSteve/mcp-sefaria-server) | `claude_desktop_config.json` | 1 (sefaria_jewish_library) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 861 | [imsupershy111/Hybrid-Rag-Project](https://github.com/imsupershy111/Hybrid-Rag-Project) | `config/config/claude_desktop_config.json` | 1 (hybrid-rag) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-hybrid-rag` |
| 862 | [hitakaha/mcp-server-nso](https://github.com/hitakaha/mcp-server-nso) | `claude_desktop_config.json` | 1 (nso) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 863 | [SALL911/BrandOS-Infrastructure](https://github.com/SALL911/BrandOS-Infrastructure) | `.claude/claude_desktop_config.json` | 1 (notion) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 864 | [mishrole/first-mcp-server](https://github.com/mishrole/first-mcp-server) | `claude_desktop_config.json` | 1 (fetch-weather) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 865 | [luis0794/mcp-python-server](https://github.com/luis0794/mcp-python-server) | `claude_desktop_config.json` | 1 (terminal_server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 866 | [atef-ataya/context-layer-part2b](https://github.com/atef-ataya/context-layer-part2b) | `mcp-configs/claude_desktop_config.json` | 1 (graphiti-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 867 | [DrBaher/sign-cli](https://github.com/DrBaher/sign-cli) | `integrations/claude-desktop/claude_desktop_config.json` | 1 (sign-cli) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 868 | [Deesmo/arch-tools-claude-desktop](https://github.com/Deesmo/arch-tools-claude-desktop) | `claude_desktop_config.json` | 1 (arch-tools) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 869 | [seemethere/cargo-mcp](https://github.com/seemethere/cargo-mcp) | `examples/claude_desktop_config.json` | 1 (cargo-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 870 | [glaucia86/swapi-mcp-server-app](https://github.com/glaucia86/swapi-mcp-server-app) | `claude_desktop_config.json` | 1 (swapi-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 871 | [keithballinger/proofcheck](https://github.com/keithballinger/proofcheck) | `mcp/claude_desktop_config.json` | 1 (proofcheck) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 872 | [ar4mirez/maia](https://github.com/ar4mirez/maia) | `examples/mcp-integration/claude_desktop_config.json` | 1 (maia) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 873 | [Joseph19820124/first_sse](https://github.com/Joseph19820124/first_sse) | `src/amazon-sns-sqs-mcp-server/claude_desktop_config.json` | 1 (amazon-sns-sqs) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 874 | [MrTimkms/MCP1C](https://github.com/MrTimkms/MCP1C) | `mcp_client_settings/claude_desktop/claude_desktop_config.json` | 1 (1c-server-stdio) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 875 | [coderXcode/mcp-forger](https://github.com/coderXcode/mcp-forger) | `plugins/claude_desktop_config.json` | 1 (mcp-forge) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 876 | [petitan/IronBase](https://github.com/petitan/IronBase) | `mcp-server/claude_desktop_config.json` | 1 (ironbase) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 877 | [Well-Polaris/2025-hackathon](https://github.com/Well-Polaris/2025-hackathon) | `team-codecrusaders/claude_desktop_config.json` | 2 (fhir, env) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 878 | [krzemienski/shannon-ios](https://github.com/krzemienski/shannon-ios) | `.claude/claude_desktop_config.json` | 3 (context7, playwright, sequential-thinking) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-INJECT-context7` |
| 879 | [dvcrn/openclaw-skills-marketplace](https://github.com/dvcrn/openclaw-skills-marketplace) | `plugins/krunkosaurus--sogni-gen/skills/sogni-gen/Support/Claude/claude_desktop_config.json` | 1 (sogni) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 880 | [yosh3289/jcr_mcp](https://github.com/yosh3289/jcr_mcp) | `claude_desktop_config.json` | 1 (jcr-partition) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 881 | [YCSE/nanobanana-mcp](https://github.com/YCSE/nanobanana-mcp) | `claude_desktop_config.json` | 1 (nanobanana-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 882 | [Ganil151/Devops](https://github.com/Ganil151/Devops) | `02-intermediate/03-phase-3/04-mcp/clients/claude_desktop_config.json.example` | 2 (devops-assistant, sre-typescript) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 883 | [brianbancroft/switchboard-flags](https://github.com/brianbancroft/switchboard-flags) | `apps/mcp/examples/claude_desktop_config.json` | 1 (switchboard) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 884 | [engramforge/project-memory-mcp](https://github.com/engramforge/project-memory-mcp) | `examples/claude_desktop_config.json` | 1 (project-memory) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 885 | [sandhia75/figmaaaa-mcp](https://github.com/sandhia75/figmaaaa-mcp) | `mcp-figma-server/claude_desktop_config.json` | 1 (figma) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 886 | [ganeshpatil0112/GenAI](https://github.com/ganeshpatil0112/GenAI) | `MCP/mcppractical/mcppractical/claude_desktop_config.json` | 3 (google-services, postgresql-db, mongodb) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 887 | [LLemonStack/llemonstack](https://github.com/LLemonStack/llemonstack) | `services/crawl4ai/claude_desktop_config.json` | 1 (crawl4ai) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-crawl4ai` |
| 888 | [Hydraallen/Weather_MCP_Server](https://github.com/Hydraallen/Weather_MCP_Server) | `claude_desktop_config.json` | 1 (weather-docker) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 889 | [wei979/DetectWed_lay](https://github.com/wei979/DetectWed_lay) | `web_lab/claude_desktop_config.json` | 1 (mysql) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 890 | [MTrajK/dotnet-projects](https://github.com/MTrajK/dotnet-projects) | `DotNet.MCP/LocalTimeMCPServer/claude_desktop_config.json` | 1 (local-time-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 891 | [badbat75/easyeda-pro-analyzer](https://github.com/badbat75/easyeda-pro-analyzer) | `examples/claude_desktop_config.json` | 1 (easyeda-pro-analyzer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 892 | [jhlee111/mssql-mcp-server](https://github.com/jhlee111/mssql-mcp-server) | `src/samples/claude_desktop_config.json` | 1 (mssql) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 893 | [MofaggolHoshen/dev-assist-mcp-server](https://github.com/MofaggolHoshen/dev-assist-mcp-server) | `examples/claude-desktop/claude_desktop_config.json` | 1 (dev-assist-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 894 | [organvm/agentic-titan](https://github.com/organvm/agentic-titan) | `examples/claude_desktop_config.json` | 1 (titan) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 895 | [xxipv6/IDA-PRO-MCP-multiple](https://github.com/xxipv6/IDA-PRO-MCP-multiple) | `claude_desktop_config.json` | 1 (ida-auto) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 896 | [SadhakKumar/ZK_location_verifier](https://github.com/SadhakKumar/ZK_location_verifier) | `newagentkit/agentkit/typescript/create-onchain-agent/templates/mcp/src/agentkit/svm/privy/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 897 | [mikeheilmann1024/g-gremlin-salesforce-mcp](https://github.com/mikeheilmann1024/g-gremlin-salesforce-mcp) | `examples/claude_desktop_config.json` | 1 (g-gremlin-sfdc) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 898 | [techiepartneragent/codriver](https://github.com/techiepartneragent/codriver) | `mcp-server/claude_desktop_config.json` | 1 (codriver) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 899 | [Joint-Photon-Sciences-Institute/xraylarch-mcp](https://github.com/Joint-Photon-Sciences-Institute/xraylarch-mcp) | `examples/claude_desktop_config.json` | 1 (xraylarch) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 900 | [sugukurukabe/japan-real-estate-intel-mcp](https://github.com/sugukurukabe/japan-real-estate-intel-mcp) | `examples/claude_desktop_config.json` | 1 (japan-real-estate-intel) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 901 | [JamieWonderchild/claude-gemini-mcp](https://github.com/JamieWonderchild/claude-gemini-mcp) | `claude_desktop_config.json` | 1 (gemini-collaboration) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 902 | [eagurin/fastdev](https://github.com/eagurin/fastdev) | `examples/claude_desktop_config.json` | 1 (fastdev) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 903 | [tam159/generative_ai](https://github.com/tam159/generative_ai) | `llm/notebook/mcp/claude_desktop_config.json` | 1 (langgraph-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 904 | [deus-h/claudeus-wp-mcp](https://github.com/deus-h/claudeus-wp-mcp) | `claude_desktop_config.json.example` | 1 (claudeus-wordpress) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 905 | [Nishu0/move-agent-kit-mcp-server](https://github.com/Nishu0/move-agent-kit-mcp-server) | `examples/mcp-server/claude_desktop_config.json` | 1 (agent-kit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 906 | [tengmmvp/Seedream_MCP](https://github.com/tengmmvp/Seedream_MCP) | `docs/claude_desktop_config.json` | 1 (seedream) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 907 | [mshk/mcp-rss-crawler](https://github.com/mshk/mcp-rss-crawler) | `claude_desktop_config.json.example` | 1 (rss-crawler) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-rss-crawler` |
| 908 | [temple-slope/dotfiles](https://github.com/temple-slope/dotfiles) | `Library/Application Support/private_Claude/private_claude_desktop_config.json.tmpl` | 1 (tradingview-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 909 | [XenoThanBird/Portfolio](https://github.com/XenoThanBird/Portfolio) | `08_agentic_ai/mcp_server/claude_desktop_config.json` | 1 (mcp-template) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 910 | [vannet/gotfreefax-mcp](https://github.com/vannet/gotfreefax-mcp) | `examples/claude_desktop_config.json` | 1 (gotfreefax) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 911 | [Thanush-41/NeoKisan-BhoomiSetu](https://github.com/Thanush-41/NeoKisan-BhoomiSetu) | `claude_desktop_config.json` | 1 (bhoomisetu) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 912 | [christseng89/mcp-BuildAgents](https://github.com/christseng89/mcp-BuildAgents) | `claude_desktop_config.json` | 1 (analysis-templates) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 913 | [gocutover/cutover-mcp-public](https://github.com/gocutover/cutover-mcp-public) | `claude_desktop_config.json.example` | 1 (cutover-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 914 | [joeblew999/wellknown](https://github.com/joeblew999/wellknown) | `examples/claude_desktop_config.json` | 1 (pocketbase) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 915 | [bnchubb/ai-in-pd-spring2026](https://github.com/bnchubb/ai-in-pd-spring2026) | `MP3/Part B/mcp_server/host_configs/claude_desktop_config.json` | 1 (miniclaw-knowledge) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 916 | [jinyanghe1/vibeedit](https://github.com/jinyanghe1/vibeedit) | `claude_desktop_config.json` | 3 (yahoo-finance, realtime-stock-cn, alpha-vantage) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 917 | [ly2xxx/aisoft](https://github.com/ly2xxx/aisoft) | `mcp/windows_claude_desktop_config.json` | 2 (claude-code-developer, gemini-qa-agent) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 918 | [ma-pony/mcp-playwright](https://github.com/ma-pony/mcp-playwright) | `examples/claude_desktop_config.json` | 1 (playwright) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 919 | [weniv/mcp](https://github.com/weniv/mcp) | `claude_desktop_config.json` | 2 (pyhub.mcptools, mcp_custom_server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 920 | [lancejames221b/agent-hivemind](https://github.com/lancejames221b/agent-hivemind) | `examples/configs/claude_desktop_config.json` | 2 (haivemind-local, haivemind-remote) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 921 | [fuzzylabs/breathehr-mcp](https://github.com/fuzzylabs/breathehr-mcp) | `claude_desktop_config.json` | 1 (breathe-hr) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 922 | [gleb-roma/mcp_file_system](https://github.com/gleb-roma/mcp_file_system) | `~/Library/Application Support/Claude/claude_desktop_config.json` | 1 (mcp-file-system) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 923 | [RomanKuk/ai-engineering-course](https://github.com/RomanKuk/ai-engineering-course) | `homework-mcp/claude_desktop_config.json` | 1 (notes) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 924 | [yusufbaykal/Customer-MCP-MongoDB](https://github.com/yusufbaykal/Customer-MCP-MongoDB) | `claude_desktop_config.json` | 1 (product-manager) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 925 | [0x0Glitch/Agent-action3](https://github.com/0x0Glitch/Agent-action3) | `agentkit/typescript/create-onchain-agent/templates/mcp/src/agentkit/svm/solana-keypair/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 926 | [Arsalan7861/ModelContextProtocol](https://github.com/Arsalan7861/ModelContextProtocol) | `claude_desktop_config.json` | 1 (my-tool) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 927 | [yashsonawane25/NotionOps-AI](https://github.com/yashsonawane25/NotionOps-AI) | `claude_desktop_config.json` | 1 (devops-brain) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 928 | [J12-Kyrie/MultiAgent_FPGA](https://github.com/J12-Kyrie/MultiAgent_FPGA) | `mcp4eda/verilator-mcp/examples/claude_desktop_config.json` | 1 (verilator) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 929 | [Marshal-AM/fireglobe](https://github.com/Marshal-AM/fireglobe) | `agentkit/typescript/create-onchain-agent/templates/mcp/src/agentkit/svm/solana-keypair/claude_desktop_config.json` | 1 (agentkit) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 930 | [prizmPrograms/excel-mcp-server](https://github.com/prizmPrograms/excel-mcp-server) | `claude_desktop_config.json.example` | 1 (excel) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 931 | [getAlby/opentimestamps-mcp](https://github.com/getAlby/opentimestamps-mcp) | `claude_desktop_config.json` | 1 (opentimestamps) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 932 | [agoncal/agoncal-sample-azure-mcp](https://github.com/agoncal/agoncal-sample-azure-mcp) | `mcp-server-azure-resourcemanager-storage/src/main/mcp/claude_desktop_config.json` | 1 (azure-mgt-storage) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-azure-mgt-storage` |
| 933 | [cultureamp/step-templates-buildkite-plugin](https://github.com/cultureamp/step-templates-buildkite-plugin) | `.mcp.json` | 1 (context7) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-INJECT-context7` |
| 934 | [pranavkantgaur/msr_data_layer](https://github.com/pranavkantgaur/msr_data_layer) | `mcp.json` | 1 (msr-data-layer) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 935 | [itsminhz/memoagent](https://github.com/itsminhz/memoagent) | `mcp.json` | 1 (Runware) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 936 | [Robaina/chemSearch](https://github.com/Robaina/chemSearch) | `.mcp.json` | 1 (chemsearch) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 937 | [HugzDEV/Buy-Printz](https://github.com/HugzDEV/Buy-Printz) | `mcp.json` | 1 (konva-documentation) | 0 | 0 | 3 | 0 | MEDIUM: `CONTEXT-EXT-FETCH-konva-documentation` |
| 938 | [gridi-ai/cowork-bridge](https://github.com/gridi-ai/cowork-bridge) | `.mcp.json` | 1 (cowork-bridge) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 939 | [mater1996/sketch-mcp-server](https://github.com/mater1996/sketch-mcp-server) | `mcp.json` | 1 (sketch-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 940 | [Axle-Bucamp/mcp-hub-codeagentic](https://github.com/Axle-Bucamp/mcp-hub-codeagentic) | `mcp.json` | 8 (developer, intlayer, desktop-commander +5 more) | 0 | 0 | 1 | 0 | _context-limit rules only_ |
| 941 | [famasya/betterhn](https://github.com/famasya/betterhn) | `.mcp.json` | 2 (browsermcp, coderabbitai) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 942 | [rudraptpsingh/oversight](https://github.com/rudraptpsingh/oversight) | `.mcp.json` | 1 (oversight) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 943 | [davidParedesO/IOT](https://github.com/davidParedesO/IOT) | `mcp.json` | 1 (iot-leds) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 944 | [daro/drawDB](https://github.com/daro/drawDB) | `aaa.json` | 1 (qdrant) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 945 | [EmilioFunes/SUPER-GELATTO](https://github.com/EmilioFunes/SUPER-GELATTO) | `mcp.json` | 1 (supabase-mcp) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 946 | [mehuldil/ai_sdlc_platform](https://github.com/mehuldil/ai_sdlc_platform) | `mcp.json` | 3 (AzureDevOps, wikijs, elasticsearch) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 947 | [thepeacefulprogrammer/terminal_mcp_server](https://github.com/thepeacefulprogrammer/terminal_mcp_server) | `mcp.json` | 1 (terminal-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 948 | [hasnaintypes/highchart-mcp-server](https://github.com/hasnaintypes/highchart-mcp-server) | `mcp.json` | 1 (highchart-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 949 | [FabianSchurig/bitbucket-cli](https://github.com/FabianSchurig/bitbucket-cli) | `mcp.json` | 1 (bitbucket) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 950 | [DavidDelOjo/kiro-power-aws-security](https://github.com/DavidDelOjo/kiro-power-aws-security) | `mcp.json` | 1 (well-architected-security-mcp-server) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 951 | [windyakin/soeji](https://github.com/windyakin/soeji) | `.mcp.json` | 1 (primevue) | 0 | 0 | 2 | 0 | _context-limit rules only_ |
| 952 | [nirmal84/aws-arch-drawio-plugin](https://github.com/nirmal84/aws-arch-drawio-plugin) | `mcp.json` | 2 (drawio, awslabs-iac) | 0 | 0 | 2 | 0 | _context-limit rules only_ |

---

## Appendix: All Rules Triggered

| Rule | Severity | Count | Description (from first occurrence) |
|---|---|---|---|
| `CONTEXT-NO-RESPONSE-LIMIT` | MEDIUM | 1200 | None of the configured MCP servers declare a response size limit (max_tokens, max_response_length). Without limits, a... |
| `CONTEXT-NO-SESSION-LIMIT` | MEDIUM | 1191 | No maximum turn count or session timeout is configured. In long-running conversations, agents can gradually lose trac... |
| `DANGEROUS-PKG-filesystem-filesystem` | HIGH | 63 | MCP server 'filesystem' uses '@modelcontextprotocol/server-filesystem' which grants filesystem access. Grants read/wr... |
| `DANGEROUS-PKG-playwright-browser-automation` | HIGH | 31 | MCP server 'playwright' uses '@playwright/mcp' which grants browser-automation access. Full browser automation — navi... |
| `CONTEXT-INJECT-context7` | MEDIUM | 16 | MCP server 'context7' uses '@upstash/context7-mcp' which injects external content directly into the LLM context windo... |
| `CONTEXT-EXT-FETCH-fetch` | MEDIUM | 14 | MCP server 'fetch' has web fetching capabilities, meaning it retrieves content from external sources and passes it in... |
| `CONTEXT-EXT-FETCH-puppeteer` | MEDIUM | 14 | MCP server 'puppeteer' has web scraping capabilities, meaning it retrieves content from external sources and passes i... |
| `CONTEXT-EXT-FETCH-brave-search` | MEDIUM | 10 | MCP server 'brave-search' has web search capabilities, meaning it retrieves content from external sources and passes ... |
| `DANGEROUS-POPULAR-serena-shell-execution` | CRITICAL | 9 | MCP server 'serena' matches a known high-risk server pattern. Serena — unrestricted shell execution and filesystem ac... |
| `CONTEXT-EXT-FETCH-playwright` | MEDIUM | 9 | MCP server 'playwright' has browser automation capabilities, meaning it retrieves content from external sources and p... |
| `DANGEROUS-PKG-postgres-database` | HIGH | 8 | MCP server 'postgres' uses '@modelcontextprotocol/server-postgres' which grants database access. Grants direct SQL ac... |
| `ENV-SECRET-supabase-SUPABASE_ACCESS_TOKEN` | HIGH | 5 | MCP server 'supabase' has env var 'SUPABASE_ACCESS_TOKEN' set to a literal value instead of an environment variable r... |
| `CONTEXT-EXT-FETCH-firecrawl` | MEDIUM | 4 | MCP server 'firecrawl' has web crawling capabilities, meaning it retrieves content from external sources and passes i... |
| `DANGEROUS-PKG-sqlite-database` | HIGH | 3 | MCP server 'sqlite' uses '@modelcontextprotocol/server-sqlite' which grants database access. Grants direct SQL access... |
| `DANGEROUS-PKG-chrome-devtools-browser-control` | CRITICAL | 3 | MCP server 'chrome-devtools' uses 'chrome-devtools-mcp' which grants browser-control access. Full Chrome DevTools Pro... |
| `CONTEXT-EXT-FETCH-crawl4ai` | MEDIUM | 3 | MCP server 'crawl4ai' has web crawling capabilities, meaning it retrieves content from external sources and passes it... |
| `DANGEROUS-PKG-github-source-control` | HIGH | 3 | MCP server 'github' uses 'github-mcp-server' which grants source-control access. GitHub write access — can create/mer... |
| `CONTEXT-INJECT-Context7` | MEDIUM | 3 | MCP server 'Context7' uses '@upstash/context7-mcp' which injects external content directly into the LLM context windo... |
| `ENV-SECRET-agent-kit-OPENAI_API_KEY` | HIGH | 3 | MCP server 'agent-kit' has env var 'OPENAI_API_KEY' set to a literal value instead of an environment variable referen... |
| `CONTEXT-EXT-FETCH-tavily` | MEDIUM | 2 | MCP server 'tavily' has web search capabilities, meaning it retrieves content from external sources and passes it int... |
| `CONTEXT-EXT-FETCH-puppeteer-hisma` | MEDIUM | 2 | MCP server 'puppeteer-hisma' has web scraping capabilities, meaning it retrieves content from external sources and pa... |
| `DANGEROUS-PKG-n8n-workflow-execution` | HIGH | 2 | MCP server 'n8n' uses 'n8n-mcp' which grants workflow-execution access. Creates and executes n8n workflows including ... |
| `CONTEXT-EXT-FETCH-firecrawl-mcp` | MEDIUM | 2 | MCP server 'firecrawl-mcp' has web crawling capabilities, meaning it retrieves content from external sources and pass... |
| `AUTH-MISSING-Figma` | CRITICAL | 2 | Remote MCP server 'Figma' (http://127.0.0.1:3845/sse) has no authentication configured. Unauthenticated MCP servers c... |
| `AUTH-MISSING-supabase` | CRITICAL | 2 | Remote MCP server 'supabase' (https://mcp.supabase.com/mcp) has no authentication configured. Unauthenticated MCP ser... |
| `CONN-STRING-ARGS-postgres` | HIGH | 2 | MCP server 'postgres' has a connection string with embedded credentials passed as a command-line argument. These cred... |
| `CONN-STRING-ENV-postgres-POSTGRES_CONNECTION_STRING` | HIGH | 2 | Env var 'POSTGRES_CONNECTION_STRING' on MCP server 'postgres' contains a connection string with embedded credentials. |
| `ENV-SECRET-github-GITHUB_PERSONAL_ACCESS_TOKEN` | HIGH | 2 | MCP server 'github' has env var 'GITHUB_PERSONAL_ACCESS_TOKEN' set to a literal value instead of an environment varia... |
| `CONTEXT-EXT-FETCH-filesystem` | MEDIUM | 2 | MCP server 'filesystem' has web crawling capabilities, meaning it retrieves content from external sources and passes ... |
| `ENV-SECRET-TestSprite-API_KEY` | HIGH | 2 | MCP server 'TestSprite' has env var 'API_KEY' set to a literal value instead of an environment variable reference. Ha... |
| `ENV-SECRET-ElevenLabs-ELEVENLABS_API_KEY` | HIGH | 2 | MCP server 'ElevenLabs' has env var 'ELEVENLABS_API_KEY' set to a literal value instead of an environment variable re... |
| `CONTEXT-EXT-FETCH-bootcamp-rag` | MEDIUM | 2 | MCP server 'bootcamp-rag' has RAG/retrieval capabilities, meaning it retrieves content from external sources and pass... |
| `CONTEXT-EXT-FETCH-hybrid-rag` | MEDIUM | 2 | MCP server 'hybrid-rag' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes... |
| `CONTEXT-EXT-FETCH-vector-database-mcp` | MEDIUM | 2 | MCP server 'vector-database-mcp' has RAG/retrieval capabilities, meaning it retrieves content from external sources a... |
| `CONTEXT-EXT-FETCH-knowledge-base-mcp` | MEDIUM | 2 | MCP server 'knowledge-base-mcp' has RAG/retrieval capabilities, meaning it retrieves content from external sources an... |
| `ENV-SECRET-ref-REF_API_KEY` | HIGH | 1 | MCP server 'ref' has env var 'REF_API_KEY' set to a literal value instead of an environment variable reference. Hardc... |
| `ENV-SECRET-semgrep-SEMGREP_APP_TOKEN` | HIGH | 1 | MCP server 'semgrep' has env var 'SEMGREP_APP_TOKEN' set to a literal value instead of an environment variable refere... |
| `ENV-SECRET-tavily-TAVILY_API_KEY` | HIGH | 1 | MCP server 'tavily' has env var 'TAVILY_API_KEY' set to a literal value instead of an environment variable reference.... |
| `DANGEROUS-POPULAR-serena-local-shell-execution` | CRITICAL | 1 | MCP server 'serena-local' matches a known high-risk server pattern. Serena — unrestricted shell execution and filesys... |
| `DANGEROUS-POPULAR-serena-docker-shell-execution` | CRITICAL | 1 | MCP server 'serena-docker' matches a known high-risk server pattern. Serena — unrestricted shell execution and filesy... |
| `DANGEROUS-PKG-file-system-filesystem` | HIGH | 1 | MCP server 'file-system' uses '@modelcontextprotocol/server-filesystem' which grants filesystem access. Grants read/w... |
| `AUTH-MISSING-averrow` | CRITICAL | 1 | Remote MCP server 'averrow' (https://averrow-mcp.cleerox.workers.dev/mcp) has no authentication configured. Unauthent... |
| `TRANSPORT-HTTP-figma-dev-mode` | HIGH | 1 | MCP server 'figma-dev-mode' uses unencrypted HTTP (http://127.0.0.1:3845/mcp). Agent communications may be intercepte... |
| `AUTH-MISSING-figma-dev-mode` | CRITICAL | 1 | Remote MCP server 'figma-dev-mode' (http://127.0.0.1:3845/mcp) has no authentication configured. Unauthenticated MCP ... |
| `TRANSPORT-HTTP-my-mcp-server-local` | HIGH | 1 | MCP server 'my-mcp-server-local' uses unencrypted HTTP (http://localhost:8788/sse). Agent communications may be inter... |
| `AUTH-MISSING-my-mcp-server-local` | CRITICAL | 1 | Remote MCP server 'my-mcp-server-local' (http://localhost:8788/sse) has no authentication configured. Unauthenticated... |
| `AUTH-MISSING-my-mcp-server-remote` | CRITICAL | 1 | Remote MCP server 'my-mcp-server-remote' (https://my-mcp-server.your-account.workers.dev/sse) has no authentication c... |
| `TRANSPORT-HTTP-everything` | HIGH | 1 | MCP server 'everything' uses unencrypted HTTP (http://localhost:6969/sse). Agent communications may be intercepted or... |
| `AUTH-MISSING-everything` | CRITICAL | 1 | Remote MCP server 'everything' (http://localhost:6969/sse) has no authentication configured. Unauthenticated MCP serv... |
| `AUTH-MISSING-narrative-mcp` | CRITICAL | 1 | Remote MCP server 'narrative-mcp' (https://mcp.narrative.io/mcp) has no authentication configured. Unauthenticated MC... |
| `AUTH-MISSING-narrative-knowledge-base` | CRITICAL | 1 | Remote MCP server 'narrative-knowledge-base' (https://docs.narrative.io/mcp) has no authentication configured. Unauth... |
| `CONTEXT-EXT-FETCH-narrative-knowledge-base` | MEDIUM | 1 | MCP server 'narrative-knowledge-base' has RAG/retrieval capabilities, meaning it retrieves content from external sour... |
| `AUTH-MISSING-narrative-agent-gateway` | CRITICAL | 1 | Remote MCP server 'narrative-agent-gateway' (https://narrative.support/mcp) has no authentication configured. Unauthe... |
| `DANGEROUS-PKG-filesystem-full-filesystem` | HIGH | 1 | MCP server 'filesystem-full' uses '@modelcontextprotocol/server-filesystem' which grants filesystem access. Grants re... |
| `TRANSPORT-HTTP-http-no-auth` | HIGH | 1 | MCP server 'http-no-auth' uses unencrypted HTTP (http://internal-api.example.com:3000/mcp). Agent communications may ... |
| `AUTH-MISSING-http-no-auth` | CRITICAL | 1 | Remote MCP server 'http-no-auth' (http://internal-api.example.com:3000/mcp) has no authentication configured. Unauthe... |
| `TRANSPORT-HTTP-pricelist-http` | HIGH | 1 | MCP server 'pricelist-http' uses unencrypted HTTP (http://localhost:5099/mcp). Agent communications may be intercepte... |
| `AUTH-MISSING-pricelist-http` | CRITICAL | 1 | Remote MCP server 'pricelist-http' (http://localhost:5099/mcp) has no authentication configured. Unauthenticated MCP ... |
| `AUTH-MISSING-pricelist-https` | CRITICAL | 1 | Remote MCP server 'pricelist-https' (https://localhost:7099/mcp) has no authentication configured. Unauthenticated MC... |
| `TRANSPORT-HTTP-nasa-apod-tr-port` | HIGH | 1 | MCP server 'nasa-apod-tr-port' uses unencrypted HTTP (http://localhost:8088/sse). Agent communications may be interce... |
| `AUTH-MISSING-nasa-apod-tr-port` | CRITICAL | 1 | Remote MCP server 'nasa-apod-tr-port' (http://localhost:8088/sse) has no authentication configured. Unauthenticated M... |
| `AUTH-MISSING-neows-remote` | CRITICAL | 1 | Remote MCP server 'neows-remote' (https://localhost:8087/sse) has no authentication configured. Unauthenticated MCP s... |
| `TRANSPORT-HTTP-Figma` | HIGH | 1 | MCP server 'Figma' uses unencrypted HTTP (http://127.0.0.1:3845/sse). Agent communications may be intercepted or tamp... |
| `AUTH-MISSING-Zapier` | CRITICAL | 1 | Remote MCP server 'Zapier' (https://mcp.zapier.com/api/mcp/s/Y2ZjYjNhMmQtYmUyOC00YWZjLTliY2QtZGQzZGUwNWIxY2MyOjMzOWY1... |
| `TRANSPORT-HTTP-whatsapp-business` | HIGH | 1 | MCP server 'whatsapp-business' uses unencrypted HTTP (http://localhost:3000/mcp/sse). Agent communications may be int... |
| `AUTH-MISSING-whatsapp-business` | CRITICAL | 1 | Remote MCP server 'whatsapp-business' (http://localhost:3000/mcp/sse) has no authentication configured. Unauthenticat... |
| `TRANSPORT-HTTP-aegis-insight` | HIGH | 1 | MCP server 'aegis-insight' uses unencrypted HTTP (http://localhost:8001/mcp). Agent communications may be intercepted... |
| `AUTH-MISSING-aegis-insight` | CRITICAL | 1 | Remote MCP server 'aegis-insight' (http://localhost:8001/mcp) has no authentication configured. Unauthenticated MCP s... |
| `TRANSPORT-HTTP-cf-mcp` | HIGH | 1 | MCP server 'cf-mcp' uses unencrypted HTTP (http://localhost:8787/mcp). Agent communications may be intercepted or tam... |
| `AUTH-MISSING-cf-mcp` | CRITICAL | 1 | Remote MCP server 'cf-mcp' (http://localhost:8787/mcp) has no authentication configured. Unauthenticated MCP servers ... |
| `TRANSPORT-HTTP-worldAPI` | HIGH | 1 | MCP server 'worldAPI' uses unencrypted HTTP (http://worldapi.block9.ai:8000/sse). Agent communications may be interce... |
| `AUTH-MISSING-worldAPI` | CRITICAL | 1 | Remote MCP server 'worldAPI' (http://worldapi.block9.ai:8000/sse) has no authentication configured. Unauthenticated M... |
| `TRANSPORT-HTTP-default-http-server` | HIGH | 1 | MCP server 'default-http-server' uses unencrypted HTTP (http://localhost:8080/mcp). Agent communications may be inter... |
| `AUTH-MISSING-default-http-server` | CRITICAL | 1 | Remote MCP server 'default-http-server' (http://localhost:8080/mcp) has no authentication configured. Unauthenticated... |
| `TRANSPORT-HTTP-uml-designer` | HIGH | 1 | MCP server 'uml-designer' uses unencrypted HTTP (http://localhost:3000/api/mcp). Agent communications may be intercep... |
| `AUTH-MISSING-uml-designer` | CRITICAL | 1 | Remote MCP server 'uml-designer' (http://localhost:3000/api/mcp) has no authentication configured. Unauthenticated MC... |
| `AUTH-MISSING-grok-api` | CRITICAL | 1 | Remote MCP server 'grok-api' (https://api.x.ai/v1/chat/completions) has no authentication configured. Unauthenticated... |
| `AUTH-MISSING-openai-proxy` | CRITICAL | 1 | Remote MCP server 'openai-proxy' (https://api.openai.com/v1/chat/completions) has no authentication configured. Unaut... |
| `AUTH-MISSING-figma` | CRITICAL | 1 | Remote MCP server 'figma' (https://mcp.figma.com/mcp) has no authentication configured. Unauthenticated MCP servers c... |
| `AUTH-MISSING-LaunchDarkly Feature Management` | CRITICAL | 1 | Remote MCP server 'LaunchDarkly Feature Management' (https://mcp.launchdarkly.com/mcp/fm) has no authentication confi... |
| `AUTH-MISSING-LaunchDarkly AI Configs` | CRITICAL | 1 | Remote MCP server 'LaunchDarkly AI Configs' (https://mcp.launchdarkly.com/mcp/aiconfigs) has no authentication config... |
| `TRANSPORT-HTTP-trello-task-manager` | HIGH | 1 | MCP server 'trello-task-manager' uses unencrypted HTTP (http://localhost:8050/sse). Agent communications may be inter... |
| `AUTH-MISSING-trello-task-manager` | CRITICAL | 1 | Remote MCP server 'trello-task-manager' (http://localhost:8050/sse) has no authentication configured. Unauthenticated... |
| `TRANSPORT-HTTP-fastapi-mem0-memory` | HIGH | 1 | MCP server 'fastapi-mem0-memory' uses unencrypted HTTP (http://localhost:8051/mcp). Agent communications may be inter... |
| `AUTH-MISSING-fastapi-mem0-memory` | CRITICAL | 1 | Remote MCP server 'fastapi-mem0-memory' (http://localhost:8051/mcp) has no authentication configured. Unauthenticated... |
| `TRANSPORT-HTTP-stratum-sports` | HIGH | 1 | MCP server 'stratum-sports' uses unencrypted HTTP (http://localhost:8001/sse). Agent communications may be intercepte... |
| `AUTH-MISSING-stratum-sports` | CRITICAL | 1 | Remote MCP server 'stratum-sports' (http://localhost:8001/sse) has no authentication configured. Unauthenticated MCP ... |
| `TRANSPORT-HTTP-pyragdoc-sse` | HIGH | 1 | MCP server 'pyragdoc-sse' uses unencrypted HTTP (http://localhost:9000/sse). Agent communications may be intercepted ... |
| `AUTH-MISSING-pyragdoc-sse` | CRITICAL | 1 | Remote MCP server 'pyragdoc-sse' (http://localhost:9000/sse) has no authentication configured. Unauthenticated MCP se... |
| `CONTEXT-EXT-FETCH-pyragdoc-sse` | MEDIUM | 1 | MCP server 'pyragdoc-sse' has RAG/retrieval capabilities, meaning it retrieves content from external sources and pass... |
| `TRANSPORT-HTTP-ai-filesystem` | HIGH | 1 | MCP server 'ai-filesystem' uses unencrypted HTTP (http://localhost:8000/mcp). Agent communications may be intercepted... |
| `AUTH-MISSING-ai-filesystem` | CRITICAL | 1 | Remote MCP server 'ai-filesystem' (http://localhost:8000/mcp) has no authentication configured. Unauthenticated MCP s... |
| `TRANSPORT-HTTP-mcp-bridge` | HIGH | 1 | MCP server 'mcp-bridge' uses unencrypted HTTP (http://localhost:3000/sse). Agent communications may be intercepted or... |
| `AUTH-MISSING-mcp-bridge` | CRITICAL | 1 | Remote MCP server 'mcp-bridge' (http://localhost:3000/sse) has no authentication configured. Unauthenticated MCP serv... |
| `TRANSPORT-HTTP-ghostloop-remote-http` | HIGH | 1 | MCP server 'ghostloop-remote-http' uses unencrypted HTTP (http://your-robot-host.local:8765/mcp). Agent communication... |
| `AUTH-MISSING-ghostloop-remote-http` | CRITICAL | 1 | Remote MCP server 'ghostloop-remote-http' (http://your-robot-host.local:8765/mcp) has no authentication configured. U... |
| `TRANSPORT-HTTP-agencybazar` | HIGH | 1 | MCP server 'agencybazar' uses unencrypted HTTP (http://localhost:8011/mcp/v1/endpoint). Agent communications may be i... |
| `AUTH-MISSING-agencybazar` | CRITICAL | 1 | Remote MCP server 'agencybazar' (http://localhost:8011/mcp/v1/endpoint) has no authentication configured. Unauthentic... |
| `TRANSPORT-HTTP-simple-mcp-server` | HIGH | 1 | MCP server 'simple-mcp-server' uses unencrypted HTTP (http://103.164.191.212:6969/sse). Agent communications may be i... |
| `AUTH-MISSING-simple-mcp-server` | CRITICAL | 1 | Remote MCP server 'simple-mcp-server' (http://103.164.191.212:6969/sse) has no authentication configured. Unauthentic... |
| `DANGEROUS-PKG-filesystem-all-home-filesystem` | HIGH | 1 | MCP server 'filesystem-all-home' uses '@modelcontextprotocol/server-filesystem' which grants filesystem access. Grant... |
| `AUTH-MISSING-remote-prod` | CRITICAL | 1 | Remote MCP server 'remote-prod' (https://mcp.example.com/sse) has no authentication configured. Unauthenticated MCP s... |
| `TRANSPORT-HTTP-internal-data-http` | HIGH | 1 | MCP server 'internal-data-http' uses unencrypted HTTP (http://localhost:3100/mcp). Agent communications may be interc... |
| `AUTH-MISSING-internal-data-http` | CRITICAL | 1 | Remote MCP server 'internal-data-http' (http://localhost:3100/mcp) has no authentication configured. Unauthenticated ... |
| `TRANSPORT-HTTP-gmail` | HIGH | 1 | MCP server 'gmail' uses unencrypted HTTP (http://localhost:8001/mcp). Agent communications may be intercepted or tamp... |
| `AUTH-MISSING-gmail` | CRITICAL | 1 | Remote MCP server 'gmail' (http://localhost:8001/mcp) has no authentication configured. Unauthenticated MCP servers c... |
| `TRANSPORT-HTTP-userology` | HIGH | 1 | MCP server 'userology' uses unencrypted HTTP (http://localhost:9000/sse). Agent communications may be intercepted or ... |
| `AUTH-MISSING-userology` | CRITICAL | 1 | Remote MCP server 'userology' (http://localhost:9000/sse) has no authentication configured. Unauthenticated MCP serve... |
| `TRANSPORT-HTTP-chatgpt-docker` | HIGH | 1 | MCP server 'chatgpt-docker' uses unencrypted HTTP (http://localhost:3008/api/mcp). Agent communications may be interc... |
| `AUTH-MISSING-chatgpt-docker` | CRITICAL | 1 | Remote MCP server 'chatgpt-docker' (http://localhost:3008/api/mcp) has no authentication configured. Unauthenticated ... |
| `TRANSPORT-HTTP-android_studio_mcp` | HIGH | 1 | MCP server 'android_studio_mcp' uses unencrypted HTTP (http://localhost:64342/sse). Agent communications may be inter... |
| `AUTH-MISSING-android_studio_mcp` | CRITICAL | 1 | Remote MCP server 'android_studio_mcp' (http://localhost:64342/sse) has no authentication configured. Unauthenticated... |
| `TRANSPORT-HTTP-doc-searcher` | HIGH | 1 | MCP server 'doc-searcher' uses unencrypted HTTP (http://localhost:8765/mcp). Agent communications may be intercepted ... |
| `AUTH-MISSING-doc-searcher` | CRITICAL | 1 | Remote MCP server 'doc-searcher' (http://localhost:8765/mcp) has no authentication configured. Unauthenticated MCP se... |
| `TRANSPORT-HTTP-playwright` | HIGH | 1 | MCP server 'playwright' uses unencrypted HTTP (http://localhost:9000/mcp). Agent communications may be intercepted or... |
| `AUTH-MISSING-playwright` | CRITICAL | 1 | Remote MCP server 'playwright' (http://localhost:9000/mcp) has no authentication configured. Unauthenticated MCP serv... |
| `AUTH-MISSING-product-pulse` | CRITICAL | 1 | Remote MCP server 'product-pulse' (https://product-pulse-mcp.up.railway.app/mcp) has no authentication configured. Un... |
| `AUTH-MISSING-virtualsms` | CRITICAL | 1 | Remote MCP server 'virtualsms' (https://mcp.virtualsms.io/mcp) has no authentication configured. Unauthenticated MCP ... |
| `AUTH-MISSING-vap` | CRITICAL | 1 | Remote MCP server 'vap' (https://api.vapagent.com/mcp) has no authentication configured. Unauthenticated MCP servers ... |
| `AUTH-MISSING-materials-platform` | CRITICAL | 1 | Remote MCP server 'materials-platform' (https://asm-mcp-materials-platform.onrender.com/mcp) has no authentication co... |
| `AUTH-MISSING-Astro docs` | CRITICAL | 1 | Remote MCP server 'Astro docs' (https://mcp.docs.astro.build/mcp) has no authentication configured. Unauthenticated M... |
| `AUTH-MISSING-deepwiki` | CRITICAL | 1 | Remote MCP server 'deepwiki' (https://mcp.deepwiki.com/mcp) has no authentication configured. Unauthenticated MCP ser... |
| `AUTH-MISSING-fi_mcp` | CRITICAL | 1 | Remote MCP server 'fi_mcp' (https://mcp.fi.money:8080/mcp/stream) has no authentication configured. Unauthenticated M... |
| `AUTH-MISSING-citedy` | CRITICAL | 1 | Remote MCP server 'citedy' (https://mcp.citedy.com/mcp) has no authentication configured. Unauthenticated MCP servers... |
| `AUTH-MISSING-Raisely` | CRITICAL | 1 | Remote MCP server 'Raisely' (https://mcp.raisely.com/mcp) has no authentication configured. Unauthenticated MCP serve... |
| `AUTH-MISSING-stuntdouble` | CRITICAL | 1 | Remote MCP server 'stuntdouble' (https://app.stuntdouble.io/api/mcp) has no authentication configured. Unauthenticate... |
| `AUTH-MISSING-better-stack` | CRITICAL | 1 | Remote MCP server 'better-stack' (https://mcp.betterstack.com) has no authentication configured. Unauthenticated MCP ... |
| `AUTH-MISSING-ChatPRD` | CRITICAL | 1 | Remote MCP server 'ChatPRD' (https://app.chatprd.ai/mcp) has no authentication configured. Unauthenticated MCP server... |
| `AUTH-MISSING-spcs-mcp` | CRITICAL | 1 | Remote MCP server 'spcs-mcp' (https://demourl.snowflakecomputing.app/mcp) has no authentication configured. Unauthent... |
| `AUTH-MISSING-notion` | CRITICAL | 1 | Remote MCP server 'notion' (https://mcp.notion.com/mcp) has no authentication configured. Unauthenticated MCP servers... |
| `AUTH-MISSING-gradio-docs` | CRITICAL | 1 | Remote MCP server 'gradio-docs' (https://gradio-docs-mcp.hf.space/gradio_api/mcp/) has no authentication configured. ... |
| `AUTH-MISSING-joai-multiversx` | CRITICAL | 1 | Remote MCP server 'joai-multiversx' (https://cortex.joai.ai/mcp/apps/multiversx) has no authentication configured. Un... |
| `AUTH-MISSING-Inco-mcp` | CRITICAL | 1 | Remote MCP server 'Inco-mcp' (https://docs.inco.org/mcp) has no authentication configured. Unauthenticated MCP server... |
| `AUTH-MISSING-openaccountants` | CRITICAL | 1 | Remote MCP server 'openaccountants' (https://www.openaccountants.com/api/mcp) has no authentication configured. Unaut... |
| `AUTH-MISSING-nxt` | CRITICAL | 1 | Remote MCP server 'nxt' (https://nxt.fly.dev/sse) has no authentication configured. Unauthenticated MCP servers can b... |
| `AUTH-MISSING-jobmaster-hosted` | CRITICAL | 1 | Remote MCP server 'jobmaster-hosted' (https://mcp.jobmaster.acidni.net/sse) has no authentication configured. Unauthe... |
| `AUTH-MISSING-xproof` | CRITICAL | 1 | Remote MCP server 'xproof' (https://xproof.app/mcp) has no authentication configured. Unauthenticated MCP servers can... |
| `AUTH-MISSING-rawgrowth-aios` | CRITICAL | 1 | Remote MCP server 'rawgrowth-aios' (https://rawgrowth-aios.vercel.app/api/mcp) has no authentication configured. Unau... |
| `AUTH-MISSING-sequential-thinking` | CRITICAL | 1 | Remote MCP server 'sequential-thinking' (https://server.smithery.ai/@smithery-ai/server-sequential-thinking/mcp) has ... |
| `AUTH-MISSING-pinnybinny` | CRITICAL | 1 | Remote MCP server 'pinnybinny' (https://b.pinnybinny.com/api/mcp/v1) has no authentication configured. Unauthenticate... |
| `AUTH-MISSING-arifos-production` | CRITICAL | 1 | Remote MCP server 'arifos-production' (https://aaamcp.arif-fazil.com/mcp) has no authentication configured. Unauthent... |
| `AUTH-MISSING-pg-aiguide` | CRITICAL | 1 | Remote MCP server 'pg-aiguide' (https://mcp.tigerdata.com/docs?disable_mcp_skills=1) has no authentication configured... |
| `AUTH-MISSING-github` | CRITICAL | 1 | Remote MCP server 'github' (https://api.githubcopilot.com/mcp/) has no authentication configured. Unauthenticated MCP... |
| `AUTH-MISSING-Sentry` | CRITICAL | 1 | Remote MCP server 'Sentry' (https://mcp.sentry.dev/mcp/niksheyyadav/javascript-nextjs) has no authentication configur... |
| `DANGEROUS-CUSTOM-enhanced_file_commander-filesystem` | HIGH | 1 | MCP server 'enhanced_file_commander' appears to grant filesystem access. Grants file management capabilities. Without... |
| `DANGEROUS-CUSTOM-powershell-commander-shell` | HIGH | 1 | MCP server 'powershell-commander' appears to grant shell access. Grants PowerShell command execution. Without human-i... |
| `ENV-SECRET-postgres-extensions-SAMBANOVA_API_KEY` | HIGH | 1 | MCP server 'postgres-extensions' has env var 'SAMBANOVA_API_KEY' set to a literal value instead of an environment var... |
| `CONN-STRING-ENV-postgres-extensions-DATABASE_URL` | HIGH | 1 | Env var 'DATABASE_URL' on MCP server 'postgres-extensions' contains a connection string with embedded credentials. |
| `CONN-STRING-ENV-postgres-extensions-DATABASE_URL2` | HIGH | 1 | Env var 'DATABASE_URL2' on MCP server 'postgres-extensions' contains a connection string with embedded credentials. |
| `CONN-STRING-ENV-postgres-extensions-DATABASE_URL3` | HIGH | 1 | Env var 'DATABASE_URL3' on MCP server 'postgres-extensions' contains a connection string with embedded credentials. |
| `CONN-STRING-ENV-postgres-extensions-DATABASE_URL4` | HIGH | 1 | Env var 'DATABASE_URL4' on MCP server 'postgres-extensions' contains a connection string with embedded credentials. |
| `CONN-STRING-ENV-postgres-extensions-DATABASE_URL5` | HIGH | 1 | Env var 'DATABASE_URL5' on MCP server 'postgres-extensions' contains a connection string with embedded credentials. |
| `ENV-SECRET-browserbase-BROWSERBASE_API_KEY` | HIGH | 1 | MCP server 'browserbase' has env var 'BROWSERBASE_API_KEY' set to a literal value instead of an environment variable ... |
| `CONTEXT-EXT-FETCH-fetch-save` | MEDIUM | 1 | MCP server 'fetch-save' has web fetching capabilities, meaning it retrieves content from external sources and passes ... |
| `ENV-SECRET-mcp-server-esignatures-ESIGNATURES_SECRET_TOKEN` | HIGH | 1 | MCP server 'mcp-server-esignatures' has env var 'ESIGNATURES_SECRET_TOKEN' set to a literal value instead of an envir... |
| `ENV-SECRET-e2b-mcp-server-E2B_API_KEY` | HIGH | 1 | MCP server 'e2b-mcp-server' has env var 'E2B_API_KEY' set to a literal value instead of an environment variable refer... |
| `ENV-SECRET-e2b-js-E2B_API_KEY` | HIGH | 1 | MCP server 'e2b-js' has env var 'E2B_API_KEY' set to a literal value instead of an environment variable reference. Ha... |
| `ENV-SECRET-perplexity-ask-PERPLEXITY_API_KEY` | HIGH | 1 | MCP server 'perplexity-ask' has env var 'PERPLEXITY_API_KEY' set to a literal value instead of an environment variabl... |
| `DANGEROUS-PKG-postgresql-database` | HIGH | 1 | MCP server 'postgresql' uses '@modelcontextprotocol/server-postgres' which grants database access. Grants direct SQL ... |
| `CONN-STRING-ARGS-postgresql` | HIGH | 1 | MCP server 'postgresql' has a connection string with embedded credentials passed as a command-line argument. These cr... |
| `CONTEXT-EXT-FETCH-web-search` | MEDIUM | 1 | MCP server 'web-search' has web search capabilities, meaning it retrieves content from external sources and passes it... |
| `ENV-SECRET-playwright-PLAYWRIGHT_MCP_EXTENSION_TOKEN` | HIGH | 1 | MCP server 'playwright' has env var 'PLAYWRIGHT_MCP_EXTENSION_TOKEN' set to a literal value instead of an environment... |
| `CONTEXT-EXT-FETCH-exa` | MEDIUM | 1 | MCP server 'exa' has web crawling capabilities, meaning it retrieves content from external sources and passes it into... |
| `CONTEXT-INJECT-terragonnmcp` | MEDIUM | 1 | MCP server 'terragonnmcp' uses '@upstash/context7-mcp' which injects external content directly into the LLM context w... |
| `CONTEXT-EXT-FETCH-terragonnmcp` | MEDIUM | 1 | MCP server 'terragonnmcp' has RAG/retrieval capabilities, meaning it retrieves content from external sources and pass... |
| `ENV-SECRET-weather-mcp-WEATHER_API_KEY` | HIGH | 1 | MCP server 'weather-mcp' has env var 'WEATHER_API_KEY' set to a literal value instead of an environment variable refe... |
| `CONN-STRING-ENV-weather-mcp-DATABASE_URL` | HIGH | 1 | Env var 'DATABASE_URL' on MCP server 'weather-mcp' contains a connection string with embedded credentials. |
| `ENV-SECRET-supabase-fitbox-SUPABASE_ACCESS_TOKEN` | HIGH | 1 | MCP server 'supabase-fitbox' has env var 'SUPABASE_ACCESS_TOKEN' set to a literal value instead of an environment var... |
| `ENV-SECRET-guardian-GUARDIAN_API_SECRET` | HIGH | 1 | MCP server 'guardian' has env var 'GUARDIAN_API_SECRET' set to a literal value instead of an environment variable ref... |
| `ENV-SECRET-guardian-GUARDIAN_API_KEY` | HIGH | 1 | MCP server 'guardian' has env var 'GUARDIAN_API_KEY' set to a literal value instead of an environment variable refere... |
| `ENV-SECRET-POKER ROOM redash-REDASH_API_KEY` | HIGH | 1 | MCP server 'POKER ROOM redash' has env var 'REDASH_API_KEY' set to a literal value instead of an environment variable... |
| `ENV-SECRET-shortcut-SHORTCUT_API_TOKEN` | HIGH | 1 | MCP server 'shortcut' has env var 'SHORTCUT_API_TOKEN' set to a literal value instead of an environment variable refe... |
| `CONTEXT-EXT-FETCH-awslabs.bedrock-kb-retrieval-mcp-server` | MEDIUM | 1 | MCP server 'awslabs.bedrock-kb-retrieval-mcp-server' has RAG/retrieval capabilities, meaning it retrieves content fro... |
| `ENV-SECRET-logseq-LOGSEQ_API_TOKEN` | HIGH | 1 | MCP server 'logseq' has env var 'LOGSEQ_API_TOKEN' set to a literal value instead of an environment variable referenc... |
| `CONN-STRING-ARGS-sql` | HIGH | 1 | MCP server 'sql' has a connection string with embedded credentials passed as a command-line argument. These credentia... |
| `ENV-SECRET-brave-search-BRAVE_API_KEY` | HIGH | 1 | MCP server 'brave-search' has env var 'BRAVE_API_KEY' set to a literal value instead of an environment variable refer... |
| `ENV-SECRET-github-GITHUB_TOKEN` | HIGH | 1 | MCP server 'github' has env var 'GITHUB_TOKEN' set to a literal value instead of an environment variable reference. H... |
| `CONTEXT-EXT-FETCH-localhost-viewer` | MEDIUM | 1 | MCP server 'localhost-viewer' has web scraping capabilities, meaning it retrieves content from external sources and p... |
| `DANGEROUS-PKG-browser-browser-automation` | HIGH | 1 | MCP server 'browser' uses '@playwright/mcp' which grants browser-automation access. Full browser automation — navigat... |
| `DANGEROUS-PKG-postgresql-mcp-database` | HIGH | 1 | MCP server 'postgresql-mcp' uses '@modelcontextprotocol/server-postgres' which grants database access. Grants direct ... |
| `CONN-STRING-ENV-postgresql-mcp-POSTGRES_CONNECTION_STRING` | HIGH | 1 | Env var 'POSTGRES_CONNECTION_STRING' on MCP server 'postgresql-mcp' contains a connection string with embedded creden... |
| `CONTEXT-EXT-FETCH-browser-mcp` | MEDIUM | 1 | MCP server 'browser-mcp' has web scraping capabilities, meaning it retrieves content from external sources and passes... |
| `CONTEXT-EXT-FETCH-playwright-mcp` | MEDIUM | 1 | MCP server 'playwright-mcp' has browser automation capabilities, meaning it retrieves content from external sources a... |
| `ENV-SECRET-colaboradores-foodix-AIRTABLE_API_KEY` | HIGH | 1 | MCP server 'colaboradores-foodix' has env var 'AIRTABLE_API_KEY' set to a literal value instead of an environment var... |
| `DANGEROUS-PKG-postgres-clinical-database` | HIGH | 1 | MCP server 'postgres-clinical' uses '@modelcontextprotocol/server-postgres' which grants database access. Grants dire... |
| `DANGEROUS-PKG-filesystem-clinical-filesystem` | HIGH | 1 | MCP server 'filesystem-clinical' uses '@modelcontextprotocol/server-filesystem' which grants filesystem access. Grant... |
| `ENV-SECRET-n8n-local-N8N_WEBHOOK_PASSWORD` | HIGH | 1 | MCP server 'n8n-local' has env var 'N8N_WEBHOOK_PASSWORD' set to a literal value instead of an environment variable r... |
| `DANGEROUS-PKG-n8n-local-workflow-execution` | HIGH | 1 | MCP server 'n8n-local' uses 'n8n-mcp' which grants workflow-execution access. Creates and executes n8n workflows incl... |
| `CONTEXT-EXT-FETCH-crawl4ai-rag` | MEDIUM | 1 | MCP server 'crawl4ai-rag' has RAG/retrieval capabilities, meaning it retrieves content from external sources and pass... |
| `ENV-SECRET-cloudflare-CLOUDFLARE_API_TOKEN` | HIGH | 1 | MCP server 'cloudflare' has env var 'CLOUDFLARE_API_TOKEN' set to a literal value instead of an environment variable ... |
| `ENV-SECRET-figma-developer-mcp-FIGMA_API_KEY` | HIGH | 1 | MCP server 'figma-developer-mcp' has env var 'FIGMA_API_KEY' set to a literal value instead of an environment variabl... |
| `CONTEXT-INJECT-figma-developer-mcp` | MEDIUM | 1 | MCP server 'figma-developer-mcp' uses 'figma-developer-mcp' which injects external content directly into the LLM cont... |
| `ENV-SECRET-xdp-XDP_ACCESS_KEY` | HIGH | 1 | MCP server 'xdp' has env var 'XDP_ACCESS_KEY' set to a literal value instead of an environment variable reference. Ha... |
| `ENV-SECRET-xdp-XDP_SECRET_KEY` | HIGH | 1 | MCP server 'xdp' has env var 'XDP_SECRET_KEY' set to a literal value instead of an environment variable reference. Ha... |
| `CONTEXT-EXT-FETCH-xdp` | MEDIUM | 1 | MCP server 'xdp' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes it int... |
| `DANGEROUS-PKG-Playwright-browser-automation` | HIGH | 1 | MCP server 'Playwright' uses '@playwright/mcp' which grants browser-automation access. Full browser automation — navi... |
| `CONTEXT-EXT-FETCH-DataCrawler` | MEDIUM | 1 | MCP server 'DataCrawler' has web crawling capabilities, meaning it retrieves content from external sources and passes... |
| `CONN-STRING-ARGS-PostgreSQL` | HIGH | 1 | MCP server 'PostgreSQL' has a connection string with embedded credentials passed as a command-line argument. These cr... |
| `CONTEXT-EXT-FETCH-RAGMaker` | MEDIUM | 1 | MCP server 'RAGMaker' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes i... |
| `ENV-SECRET-personal-expense-tracker-GEMINI_API_KEY` | HIGH | 1 | MCP server 'personal-expense-tracker' has env var 'GEMINI_API_KEY' set to a literal value instead of an environment v... |
| `ENV-SECRET-company-expense-tracker-GEMINI_API_KEY` | HIGH | 1 | MCP server 'company-expense-tracker' has env var 'GEMINI_API_KEY' set to a literal value instead of an environment va... |
| `ENV-SECRET-news-NEWS_API_KEY` | HIGH | 1 | MCP server 'news' has env var 'NEWS_API_KEY' set to a literal value instead of an environment variable reference. Har... |
| `ENV-SECRET-currency-CURRENCY_API_KEY` | HIGH | 1 | MCP server 'currency' has env var 'CURRENCY_API_KEY' set to a literal value instead of an environment variable refere... |
| `ENV-SECRET-brightdata-API_TOKEN` | HIGH | 1 | MCP server 'brightdata' has env var 'API_TOKEN' set to a literal value instead of an environment variable reference. ... |
| `ENV-SECRET-notion-NOTION_API_KEY` | HIGH | 1 | MCP server 'notion' has env var 'NOTION_API_KEY' set to a literal value instead of an environment variable reference.... |
| `ENV-SECRET-google-drive-GOOGLE_DRIVE_OAUTH_CREDENTIALS` | HIGH | 1 | MCP server 'google-drive' has env var 'GOOGLE_DRIVE_OAUTH_CREDENTIALS' set to a literal value instead of an environme... |
| `ENV-SECRET-tv1-minio-integration-MINIO_ACCESS_KEY` | HIGH | 1 | MCP server 'tv1-minio-integration' has env var 'MINIO_ACCESS_KEY' set to a literal value instead of an environment va... |
| `ENV-SECRET-tv1-minio-integration-MINIO_SECRET_KEY` | HIGH | 1 | MCP server 'tv1-minio-integration' has env var 'MINIO_SECRET_KEY' set to a literal value instead of an environment va... |
| `DANGEROUS-PKG-filesystems-filesystem` | HIGH | 1 | MCP server 'filesystems' uses '@modelcontextprotocol/server-filesystem' which grants filesystem access. Grants read/w... |
| `ENV-SECRET-motiff-MOTIFF_TOKEN` | HIGH | 1 | MCP server 'motiff' has env var 'MOTIFF_TOKEN' set to a literal value instead of an environment variable reference. H... |
| `ENV-SECRET-jira-pgb-JIRA_API_KEY` | HIGH | 1 | MCP server 'jira-pgb' has env var 'JIRA_API_KEY' set to a literal value instead of an environment variable reference.... |
| `ENV-SECRET-langfuse-LANGFUSE_SECRET_KEY` | HIGH | 1 | MCP server 'langfuse' has env var 'LANGFUSE_SECRET_KEY' set to a literal value instead of an environment variable ref... |
| `ENV-SECRET-weather-YANDEX_WEATHER_API_KEY` | HIGH | 1 | MCP server 'weather' has env var 'YANDEX_WEATHER_API_KEY' set to a literal value instead of an environment variable r... |
| `CONN-STRING-ENV-mcp-starter-DATABASE_URL` | HIGH | 1 | Env var 'DATABASE_URL' on MCP server 'mcp-starter' contains a connection string with embedded credentials. |
| `ENV-SECRET-automation-ASK_TOKENS_PATH` | HIGH | 1 | MCP server 'automation' has env var 'ASK_TOKENS_PATH' set to a literal value instead of an environment variable refer... |
| `ENV-SECRET-mssql-contoso-SQL_PASSWORD` | HIGH | 1 | MCP server 'mssql-contoso' has env var 'SQL_PASSWORD' set to a literal value instead of an environment variable refer... |
| `ENV-SECRET-mcp-yfinance-server-paper_API_KEY` | HIGH | 1 | MCP server 'mcp-yfinance-server' has env var 'paper_API_KEY' set to a literal value instead of an environment variabl... |
| `ENV-SECRET-file-notion-mcp-NOTION_API_KEY` | HIGH | 1 | MCP server 'file-notion-mcp' has env var 'NOTION_API_KEY' set to a literal value instead of an environment variable r... |
| `ENV-SECRET-glory-tareas-GLORY_WP_PASSWORD` | HIGH | 1 | MCP server 'glory-tareas' has env var 'GLORY_WP_PASSWORD' set to a literal value instead of an environment variable r... |
| `ENV-SECRET-tiendanube-TIENDANUBE_ACCESS_TOKEN` | HIGH | 1 | MCP server 'tiendanube' has env var 'TIENDANUBE_ACCESS_TOKEN' set to a literal value instead of an environment variab... |
| `ENV-SECRET-abstractgo-AG_API_KEY` | HIGH | 1 | MCP server 'abstractgo' has env var 'AG_API_KEY' set to a literal value instead of an environment variable reference.... |
| `ENV-SECRET-cowrie-AGENT_PRIVATE_KEY` | HIGH | 1 | MCP server 'cowrie' has env var 'AGENT_PRIVATE_KEY' set to a literal value instead of an environment variable referen... |
| `ENV-SECRET-graph-memory-NEO4J_PASSWORD` | HIGH | 1 | MCP server 'graph-memory' has env var 'NEO4J_PASSWORD' set to a literal value instead of an environment variable refe... |
| `CONTEXT-EXT-FETCH-git` | MEDIUM | 1 | MCP server 'git' has web crawling capabilities, meaning it retrieves content from external sources and passes it into... |
| `CONTEXT-EXT-FETCH-godot` | MEDIUM | 1 | MCP server 'godot' has web crawling capabilities, meaning it retrieves content from external sources and passes it in... |
| `ENV-SECRET-tally-mcp-smithery-TALLY_API_KEY` | HIGH | 1 | MCP server 'tally-mcp-smithery' has env var 'TALLY_API_KEY' set to a literal value instead of an environment variable... |
| `ENV-SECRET-power-platform-orchestrator-AZURE_CLIENT_SECRET` | HIGH | 1 | MCP server 'power-platform-orchestrator' has env var 'AZURE_CLIENT_SECRET' set to a literal value instead of an envir... |
| `DANGEROUS-PKG-project-files-filesystem` | HIGH | 1 | MCP server 'project-files' uses '@modelcontextprotocol/server-filesystem' which grants filesystem access. Grants read... |
| `ENV-SECRET-tigerlite-AWS_SECRET_ACCESS_KEY` | HIGH | 1 | MCP server 'tigerlite' has env var 'AWS_SECRET_ACCESS_KEY' set to a literal value instead of an environment variable ... |
| `ENV-SECRET-omaha-OMAHA_API_KEY` | HIGH | 1 | MCP server 'omaha' has env var 'OMAHA_API_KEY' set to a literal value instead of an environment variable reference. H... |
| `ENV-SECRET-firecrawl-mcp-FIRECRAWL_API_KEY` | HIGH | 1 | MCP server 'firecrawl-mcp' has env var 'FIRECRAWL_API_KEY' set to a literal value instead of an environment variable ... |
| `ENV-SECRET-sanity-SANITY_API_TOKEN` | HIGH | 1 | MCP server 'sanity' has env var 'SANITY_API_TOKEN' set to a literal value instead of an environment variable referenc... |
| `ENV-SECRET-ui-helper-ai-OPENAI_API_KEY` | HIGH | 1 | MCP server 'ui-helper-ai' has env var 'OPENAI_API_KEY' set to a literal value instead of an environment variable refe... |
| `CONTEXT-EXT-FETCH-mcp-server-fetch` | MEDIUM | 1 | MCP server 'mcp-server-fetch' has web fetching capabilities, meaning it retrieves content from external sources and p... |
| `CONTEXT-EXT-FETCH-mcp-doc-scraper` | MEDIUM | 1 | MCP server 'mcp-doc-scraper' has web crawling capabilities, meaning it retrieves content from external sources and pa... |
| `ENV-SECRET-browserbase-local-OPENROUTER_API_KEY` | HIGH | 1 | MCP server 'browserbase-local' has env var 'OPENROUTER_API_KEY' set to a literal value instead of an environment vari... |
| `ENV-SECRET-figma-FIGMA_PERSONAL_ACCESS_TOKEN` | HIGH | 1 | MCP server 'figma' has env var 'FIGMA_PERSONAL_ACCESS_TOKEN' set to a literal value instead of an environment variabl... |
| `ENV-SECRET-supabase-SUPABASE_DB_PASSWORD` | HIGH | 1 | MCP server 'supabase' has env var 'SUPABASE_DB_PASSWORD' set to a literal value instead of an environment variable re... |
| `ENV-SECRET-brandvoice-ANTHROPIC_API_KEY` | HIGH | 1 | MCP server 'brandvoice' has env var 'ANTHROPIC_API_KEY' set to a literal value instead of an environment variable ref... |
| `ENV-SECRET-vault-VAULT_TOKEN` | HIGH | 1 | MCP server 'vault' has env var 'VAULT_TOKEN' set to a literal value instead of an environment variable reference. Har... |
| `CONTEXT-EXT-FETCH-tavily-mcp` | MEDIUM | 1 | MCP server 'tavily-mcp' has web search capabilities, meaning it retrieves content from external sources and passes it... |
| `ENV-SECRET-slack-mcp-SLACK_BOT_TOKEN` | HIGH | 1 | MCP server 'slack-mcp' has env var 'SLACK_BOT_TOKEN' set to a literal value instead of an environment variable refere... |
| `ENV-SECRET-foursquare-FOURSQUARE_SERVICE_TOKEN` | HIGH | 1 | MCP server 'foursquare' has env var 'FOURSQUARE_SERVICE_TOKEN' set to a literal value instead of an environment varia... |
| `ENV-SECRET-moltler-skills-ES_PASSWORD` | HIGH | 1 | MCP server 'moltler-skills' has env var 'ES_PASSWORD' set to a literal value instead of an environment variable refer... |
| `DANGEROUS-CUSTOM-powershell-shell` | HIGH | 1 | MCP server 'powershell' appears to grant shell access. Grants shell command execution. Without human-in-the-loop appr... |
| `DANGEROUS-PKG-memory-files-filesystem` | HIGH | 1 | MCP server 'memory-files' uses '@modelcontextprotocol/server-filesystem' which grants filesystem access. Grants read/... |
| `ENV-SECRET-conversion-debugger-GHL_API_KEY` | HIGH | 1 | MCP server 'conversion-debugger' has env var 'GHL_API_KEY' set to a literal value instead of an environment variable ... |
| `ENV-SECRET-elemia-ELEMIA_HTTP_TOKEN` | HIGH | 1 | MCP server 'elemia' has env var 'ELEMIA_HTTP_TOKEN' set to a literal value instead of an environment variable referen... |
| `DANGEROUS-PKG-local-filesystem-filesystem` | HIGH | 1 | MCP server 'local-filesystem' uses '@modelcontextprotocol/server-filesystem' which grants filesystem access. Grants r... |
| `DANGEROUS-PKG-arifos-filesystem-filesystem` | HIGH | 1 | MCP server 'arifos-filesystem' uses '@modelcontextprotocol/server-filesystem' which grants filesystem access. Grants ... |
| `CONTEXT-EXT-FETCH-arifos-fetch` | MEDIUM | 1 | MCP server 'arifos-fetch' has web fetching capabilities, meaning it retrieves content from external sources and passe... |
| `CONTEXT-EXT-FETCH-arifos-brave-search` | MEDIUM | 1 | MCP server 'arifos-brave-search' has web search capabilities, meaning it retrieves content from external sources and ... |
| `ENV-SECRET-museum-api-MUSEUM_API_PASSWORD` | HIGH | 1 | MCP server 'museum-api' has env var 'MUSEUM_API_PASSWORD' set to a literal value instead of an environment variable r... |
| `ENV-SECRET-Andalik Weather MCP-OPENWEATHER_API_KEY` | HIGH | 1 | MCP server 'Andalik Weather MCP' has env var 'OPENWEATHER_API_KEY' set to a literal value instead of an environment v... |
| `ENV-SECRET-hyperpersona-HYPERPERSONA_PASSWORD` | HIGH | 1 | MCP server 'hyperpersona' has env var 'HYPERPERSONA_PASSWORD' set to a literal value instead of an environment variab... |
| `ENV-SECRET-documentation-server-GEMINI_API_KEY` | HIGH | 1 | MCP server 'documentation-server' has env var 'GEMINI_API_KEY' set to a literal value instead of an environment varia... |
| `DANGEROUS-PKG-mcp_filesystem-filesystem` | HIGH | 1 | MCP server 'mcp_filesystem' uses '@modelcontextprotocol/server-filesystem' which grants filesystem access. Grants rea... |
| `CONTEXT-EXT-FETCH-mcp_fetch` | MEDIUM | 1 | MCP server 'mcp_fetch' has web fetching capabilities, meaning it retrieves content from external sources and passes i... |
| `ENV-SECRET-MiniMax-MINIMAX_API_KEY` | HIGH | 1 | MCP server 'MiniMax' has env var 'MINIMAX_API_KEY' set to a literal value instead of an environment variable referenc... |
| `ENV-SECRET-weather-files-WEATHER_API_KEY` | HIGH | 1 | MCP server 'weather-files' has env var 'WEATHER_API_KEY' set to a literal value instead of an environment variable re... |
| `ENV-SECRET-@21st-dev/magic-API_KEY` | HIGH | 1 | MCP server '@21st-dev/magic' has env var 'API_KEY' set to a literal value instead of an environment variable referenc... |
| `CONN-STRING-ENV-8n8-marketing-DATABASE_URL` | HIGH | 1 | Env var 'DATABASE_URL' on MCP server '8n8-marketing' contains a connection string with embedded credentials. |
| `ENV-SECRET-claimcopilot-OPENROUTER_API_KEY` | HIGH | 1 | MCP server 'claimcopilot' has env var 'OPENROUTER_API_KEY' set to a literal value instead of an environment variable ... |
| `ENV-SECRET-ultimate-mcp-hub-N8N_API_KEY` | HIGH | 1 | MCP server 'ultimate-mcp-hub' has env var 'N8N_API_KEY' set to a literal value instead of an environment variable ref... |
| `ENV-SECRET-ibge-pnad-DB_PASSWORD` | HIGH | 1 | MCP server 'ibge-pnad' has env var 'DB_PASSWORD' set to a literal value instead of an environment variable reference.... |
| `CONN-STRING-ENV-geond-GEOND_DATABASE_URL` | HIGH | 1 | Env var 'GEOND_DATABASE_URL' on MCP server 'geond' contains a connection string with embedded credentials. |
| `ENV-SECRET-formulize-FORMULIZE_API_KEY` | HIGH | 1 | MCP server 'formulize' has env var 'FORMULIZE_API_KEY' set to a literal value instead of an environment variable refe... |
| `ENV-SECRET-nexus-evidence-ANTHROPIC_API_KEY` | HIGH | 1 | MCP server 'nexus-evidence' has env var 'ANTHROPIC_API_KEY' set to a literal value instead of an environment variable... |
| `ENV-SECRET-openproject-mcp-OPENPROJECT_API_KEY` | HIGH | 1 | MCP server 'openproject-mcp' has env var 'OPENPROJECT_API_KEY' set to a literal value instead of an environment varia... |
| `ENV-SECRET-case-canopy-legal-OPENAI_API_KEY` | HIGH | 1 | MCP server 'case-canopy-legal' has env var 'OPENAI_API_KEY' set to a literal value instead of an environment variable... |
| `CONTEXT-EXT-FETCH-excel-python` | MEDIUM | 1 | MCP server 'excel-python' has RAG/retrieval capabilities, meaning it retrieves content from external sources and pass... |
| `ENV-SECRET-resend-RESEND_API_KEY` | HIGH | 1 | MCP server 'resend' has env var 'RESEND_API_KEY' set to a literal value instead of an environment variable reference.... |
| `ENV-SECRET-wordpress-WORDPRESS_PASSWORD` | HIGH | 1 | MCP server 'wordpress' has env var 'WORDPRESS_PASSWORD' set to a literal value instead of an environment variable ref... |
| `DANGEROUS-PKG-n8n-mcp-workflow-execution` | HIGH | 1 | MCP server 'n8n-mcp' uses 'n8n-mcp' which grants workflow-execution access. Creates and executes n8n workflows includ... |
| `ENV-SECRET-evolution-api-EVOLUTION_API_KEY` | HIGH | 1 | MCP server 'evolution-api' has env var 'EVOLUTION_API_KEY' set to a literal value instead of an environment variable ... |
| `CONN-STRING-ENV-local-knowledge-rag-DATABASE_URL` | HIGH | 1 | Env var 'DATABASE_URL' on MCP server 'local-knowledge-rag' contains a connection string with embedded credentials. |
| `CONTEXT-EXT-FETCH-local-knowledge-rag` | MEDIUM | 1 | MCP server 'local-knowledge-rag' has RAG/retrieval capabilities, meaning it retrieves content from external sources a... |
| `CONTEXT-EXT-FETCH-firebase-bulleoapp` | MEDIUM | 1 | MCP server 'firebase-bulleoapp' has RAG/retrieval capabilities, meaning it retrieves content from external sources an... |
| `ENV-SECRET-gcp-vertex-ai-GOOGLE_APPLICATION_CREDENTIALS` | HIGH | 1 | MCP server 'gcp-vertex-ai' has env var 'GOOGLE_APPLICATION_CREDENTIALS' set to a literal value instead of an environm... |
| `ENV-SECRET-ssb-mcp-server-KNOX_TOKEN` | HIGH | 1 | MCP server 'ssb-mcp-server' has env var 'KNOX_TOKEN' set to a literal value instead of an environment variable refere... |
| `CONN-STRING-ENV-postgres-MCP_PG_DATABASE_URL` | HIGH | 1 | Env var 'MCP_PG_DATABASE_URL' on MCP server 'postgres' contains a connection string with embedded credentials. |
| `ENV-SECRET-gmail_mcp_server-GOOGLE_APPLICATION_CREDENTIALS` | HIGH | 1 | MCP server 'gmail_mcp_server' has env var 'GOOGLE_APPLICATION_CREDENTIALS' set to a literal value instead of an envir... |
| `ENV-SECRET-vtiger-VTIGER_ACCESS_KEY` | HIGH | 1 | MCP server 'vtiger' has env var 'VTIGER_ACCESS_KEY' set to a literal value instead of an environment variable referen... |
| `ENV-SECRET-obsidian-OBSIDIAN_API_TOKEN` | HIGH | 1 | MCP server 'obsidian' has env var 'OBSIDIAN_API_TOKEN' set to a literal value instead of an environment variable refe... |
| `ENV-SECRET-gsheets-GOOGLE_CREDENTIALS_PATH` | HIGH | 1 | MCP server 'gsheets' has env var 'GOOGLE_CREDENTIALS_PATH' set to a literal value instead of an environment variable ... |
| `ENV-SECRET-mcp-ui-expo-tamagui-GEMINI_API_KEY` | HIGH | 1 | MCP server 'mcp-ui-expo-tamagui' has env var 'GEMINI_API_KEY' set to a literal value instead of an environment variab... |
| `CONTEXT-EXT-FETCH-flash-loan-arbitrage` | MEDIUM | 1 | MCP server 'flash-loan-arbitrage' has RAG/retrieval capabilities, meaning it retrieves content from external sources ... |
| `CONTEXT-EXT-FETCH-youtube` | MEDIUM | 1 | MCP server 'youtube' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes it... |
| `CONTEXT-EXT-FETCH-needle` | MEDIUM | 1 | MCP server 'needle' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes it ... |
| `DANGEROUS-POPULAR-xiaohongshu-mcp-social-media` | MEDIUM | 1 | MCP server 'xiaohongshu-mcp' matches a known high-risk server pattern. Xiaohongshu MCP — can publish posts, comments,... |
| `CONTEXT-EXT-FETCH-airas` | MEDIUM | 1 | MCP server 'airas' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes it i... |
| `CONTEXT-EXT-FETCH-zadara-storage` | MEDIUM | 1 | MCP server 'zadara-storage' has RAG/retrieval capabilities, meaning it retrieves content from external sources and pa... |
| `CONTEXT-EXT-FETCH-rag-documents` | MEDIUM | 1 | MCP server 'rag-documents' has RAG/retrieval capabilities, meaning it retrieves content from external sources and pas... |
| `CONTEXT-EXT-FETCH-ragmcp` | MEDIUM | 1 | MCP server 'ragmcp' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes it ... |
| `CONTEXT-EXT-FETCH-apple-docs` | MEDIUM | 1 | MCP server 'apple-docs' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes... |
| `CONTEXT-EXT-FETCH-memflow` | MEDIUM | 1 | MCP server 'memflow' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes it... |
| `CONTEXT-EXT-FETCH-graphrag-mcp` | MEDIUM | 1 | MCP server 'graphrag-mcp' has RAG/retrieval capabilities, meaning it retrieves content from external sources and pass... |
| `CONTEXT-EXT-FETCH-tavily-search` | MEDIUM | 1 | MCP server 'tavily-search' has web search capabilities, meaning it retrieves content from external sources and passes... |
| `CONTEXT-EXT-FETCH-business-plan` | MEDIUM | 1 | MCP server 'business-plan' has web search capabilities, meaning it retrieves content from external sources and passes... |
| `CONTEXT-EXT-FETCH-sfu-library` | MEDIUM | 1 | MCP server 'sfu-library' has web search capabilities, meaning it retrieves content from external sources and passes i... |
| `CONTEXT-EXT-FETCH-pommel` | MEDIUM | 1 | MCP server 'pommel' has web search capabilities, meaning it retrieves content from external sources and passes it int... |
| `CONTEXT-EXT-FETCH-gitlab` | MEDIUM | 1 | MCP server 'gitlab' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes it ... |
| `CONTEXT-EXT-FETCH-mcp-automation-api` | MEDIUM | 1 | MCP server 'mcp-automation-api' has web fetching capabilities, meaning it retrieves content from external sources and... |
| `CONTEXT-EXT-FETCH-emailbison` | MEDIUM | 1 | MCP server 'emailbison' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes... |
| `CONTEXT-EXT-FETCH-crawl4ai-local` | MEDIUM | 1 | MCP server 'crawl4ai-local' has web crawling capabilities, meaning it retrieves content from external sources and pas... |
| `CONTEXT-EXT-FETCH-mo5-rag` | MEDIUM | 1 | MCP server 'mo5-rag' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes it... |
| `CONTEXT-EXT-FETCH-partsbox` | MEDIUM | 1 | MCP server 'partsbox' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes i... |
| `CONTEXT-EXT-FETCH-domain-memory-agent` | MEDIUM | 1 | MCP server 'domain-memory-agent' has RAG/retrieval capabilities, meaning it retrieves content from external sources a... |
| `CONTEXT-EXT-FETCH-unity-docs` | MEDIUM | 1 | MCP server 'unity-docs' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passes... |
| `CONTEXT-EXT-FETCH-ida-pro-mcp` | MEDIUM | 1 | MCP server 'ida-pro-mcp' has RAG/retrieval capabilities, meaning it retrieves content from external sources and passe... |
| `CONTEXT-EXT-FETCH-rag-knowledge-gd2` | MEDIUM | 1 | MCP server 'rag-knowledge-gd2' has RAG/retrieval capabilities, meaning it retrieves content from external sources and... |
| `CONTEXT-EXT-FETCH-NCBI Research Assistant` | MEDIUM | 1 | MCP server 'NCBI Research Assistant' has RAG/retrieval capabilities, meaning it retrieves content from external sourc... |
| `CONTEXT-EXT-FETCH-rss-crawler` | MEDIUM | 1 | MCP server 'rss-crawler' has web crawling capabilities, meaning it retrieves content from external sources and passes... |
| `CONTEXT-EXT-FETCH-azure-mgt-storage` | MEDIUM | 1 | MCP server 'azure-mgt-storage' has RAG/retrieval capabilities, meaning it retrieves content from external sources and... |
| `CONTEXT-EXT-FETCH-konva-documentation` | MEDIUM | 1 | MCP server 'konva-documentation' has web crawling capabilities, meaning it retrieves content from external sources an... |

---
*Total: 1200 configs, 2904 findings across 315 unique rules.*