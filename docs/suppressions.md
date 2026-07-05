# Suppressing Findings

`aguard scan` supports two ways to silence a specific finding without
disabling the check for everyone else. Both are additive: a finding is
suppressed if it matches *either* mechanism.

Suppressed findings are never silently dropped from the count — the scan
summary always reports how many were suppressed and by which mechanism
(`N finding(s) suppressed (X via .aguard.yaml, Y inline)`). Use
`--no-suppress` to see every finding regardless of suppression rules.

## 1. Project-level: `.aguard.yaml`

Place a `.aguard.yaml` (or `.aguard.yml`) file at the root of the scanned
project:

```yaml
ignore:
  # Exact match against a specific Finding.id
  - id: "SECRET-GENERIC-SECRET-config.yaml-L12"
    reason: "rotated test fixture, not a real credential"

  # Prefix match against Finding.id — suppresses every instance of a rule
  - rule: "CONTEXT-NO-SESSION-LIMIT"
    reason: "session limits are enforced by the MCP client, not this config"

  # Match against Finding.category
  - category: "context_safety"
    reason: "not applicable to this deployment model"

  # fnmatch-style glob against the file path, relative to the project root
  - path: "tests/fixtures/**"
    reason: "test fixtures, not real configuration"
```

Each entry needs exactly one of `id`, `rule`, `category`, or `path`. `reason`
is optional but recommended — it's for your team, not enforced by the tool.

## 2. Inline: `aguard-ignore` comments

For findings tied to a specific file and line, add a comment on that line:

```python
api_key = "sk-live-abc123"  # aguard-ignore
```

This suppresses every finding on that line. To scope it to specific rule(s),
add a colon and a comma-separated list of `Finding.id` prefixes:

```python
api_key = "sk-live-abc123"  # aguard-ignore: SECRET-OPENAI-KEY
```

The marker is language-agnostic — it's matched as plain text, so `#`, `//`,
or any other comment syntax works.

## Finding IDs and rule prefixes

Finding IDs are visible in `--format json` output, or in the terminal report
next to each finding. Some IDs are unique per instance (e.g.
`SECRET-GENERIC-SECRET-config.yaml-L12`, one per file/line hit); others are
already rule-level (e.g. `CONTEXT-NO-SESSION-LIMIT`). A `rule:` prefix match
works for both — it just needs to match the start of the ID.
