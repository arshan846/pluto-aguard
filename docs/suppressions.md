# Suppressing Findings

`aguard scan`, `evidence`, `baseline`, and `owasp` all support two ways to
silence a specific finding without disabling the check for everyone else.
Both are additive: a finding is suppressed if it matches *either*
mechanism. All four commands read the same `.aguard.yaml` and inline
comments consistently, so a finding you've accepted stays accepted across
the launch-readiness packet, OWASP coverage, and drift comparisons — not
just the plain scan.

Suppressed findings are never silently dropped from the count — each
command reports how many were suppressed (`scan` additionally breaks this
down by mechanism: `N finding(s) suppressed (X via .aguard.yaml, Y
inline)`). `scan` also has `--no-suppress` to see every finding regardless
of suppression rules; `evidence`/`baseline`/`owasp` don't expose that flag
yet, since they're aggregate reports rather than a single scan pass.

One consequence worth knowing for `baseline`: a finding that becomes
suppressed today will show up as "Resolved" the next time you run
`baseline compare`, and a fresh `baseline create` will not include
suppressed findings in the snapshot at all. This is intentional — the
baseline represents what you're actually tracking, not everything the
scanners could theoretically detect.

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
