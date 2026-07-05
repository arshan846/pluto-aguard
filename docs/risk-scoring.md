# Risk Scoring Methodology

Pluto AgentGuard uses a heuristic risk score from 0-100 to summarize the security posture of an agent project.

## Overall formula

The overall score blends two inputs:

- **70% findings risk** — detected vulnerabilities and misconfigurations
- **30% permission risk** — how dangerous the configured tool access is even before a finding triggers

Formula:

```text
overall_score = min(100, (finding_score * 0.7) + (permission_risk_score * 0.3))
```

## Findings score

Each finding contributes a severity-weighted value:

- Critical = 25
- High = 15
- Medium = 8
- Low = 3
- Info = 1

Formula:

```text
finding_score =
  critical_count * 25 +
  high_count * 15 +
  medium_count * 8 +
  low_count * 3 +
  info_count * 1
```

This means a small number of critical issues can dominate the final score, which is intentional.

## Permission risk score

Permission risk estimates how dangerous the tool configuration is even if the scanner has not yet found an explicit vulnerability.

### Tool type weights

Current default tool weights:

- `execute` = 1.0
- `shell` = 1.0
- `file_write` = 0.9
- `file_delete` = 0.9
- `database_write` = 0.8
- `database_delete` = 0.8
- `network_outbound` = 0.7
- `api_call` = 0.5
- `file_read` = 0.4
- `database_read` = 0.4
- unknown tools = 0.3

### Risk reductions

For each configured tool:

- **Human-in-the-loop (HITL)** reduces tool risk to **0.3x**
- **Scoped permissions** (`permissions.<tool>.scope` set) reduce tool risk to **0.5x**
- **Read-only access** (`permissions.<tool>.access` is `read`/`readonly`/`read-only`) reduces tool risk to **0.4x**

These reductions stack multiplicatively. For example, a `file_write` tool with HITL and a scope gets:

```text
0.9 * 0.3 * 0.5 = 0.135
```

### Missing control penalties

If the agent has tools configured, the denominator (`max_possible`) is a fixed
worst-case baseline: these categories always contribute to it, so closing a
gap always moves the ratio rather than shrinking the denominator along with
the numerator.

- missing `timeout` = +5 (always counted)
- missing `rate_limit` = +5 (always counted)
- no explicit `permissions` declared = +10 (always counted)

Four more categories are AgentGuard's own extended policy vocabulary —
`network.egress`, `runtime.sandbox`, `auth.token_type`, `permission_model` —
which no config format has by convention. These are **adoption-gated**: each
only counts toward the score (in either direction) if the config actually
declares that key at all. A config that's never touched `runtime.sandbox`
isn't penalized for lacking it; one that sets `runtime.sandbox: false` is.
Each of these four is worth +5 when present-but-unsatisfied.

The raw permission score is then normalized against the total of whichever
categories actually counted, to a 0-100 scale.

## Example calculation

Sample config:

```yaml
name: data-agent
tools:
  - execute
  - file_write
  - database_read
require_human_approval:
  - file_write
permissions:
  file_write:
    scope: reports/*
```

Assume there are also findings:

- 1 critical
- 2 high
- 1 medium

### Step 1: findings score

```text
finding_score = 1*25 + 2*15 + 1*8 = 63
findings_component = 63 * 0.7 = 44.1
```

### Step 2: permission risk

Tool risk:

- `execute` = 1.0
- `file_write` = 0.9 * 0.3 * 0.5 = 0.135
- `database_read` = 0.4

Base subtotal:

```text
1.0 + 0.135 + 0.4 = 1.535
```

Missing controls:

- no `timeout` = +5
- no `rate_limit` = +5
- explicit `permissions` exists, so no +10 penalty (but +10 still counts toward the denominator)
- config has no `network`/`runtime`/`auth`/`permission_model` keys, so none of those four categories count toward either the score or the denominator (adoption-gated)

Raw permission score:

```text
1.535 + 5 + 5 + 0 = 11.535
```

Normalization denominator (tool weights + the three always-counted categories; the four extended categories are absent from this config, so they contribute nothing):

```text
max_possible = (1.0 + 0.9 + 0.4) + 5 + 5 + 10 = 22.3
permission_risk_score = (11.535 / 22.3) * 100 = 51.7
permissions_component = 51.7 * 0.3 = 15.5
```

### Step 3: overall score

```text
overall_score = min(100, 44.1 + 15.5) = 59.6
```

Rounded output:

```text
59.6 / 100
```

Verified by running `calculate_permission_risk_score` against this exact config: it returns `51.7`, matching Step 2 above.

## CI threshold guidance

Suggested interpretations for automation and release gates:

- **<25** = low risk
- **25-49** = moderate risk
- **50-74** = high risk
- **>=75** = critical risk

Typical CI patterns:

- warn only for moderate risk
- block pull requests at 50+
- block releases at 75+
- fail immediately on any critical finding for sensitive workloads

## Limitations

- This is **heuristic scoring**, not a formal risk assessment
- Scores are **opinionated defaults**, not universal truth
- Different environments may need different weights and thresholds
- Findings are only as good as the scanner coverage and available artifacts
- Business impact, data sensitivity, and compensating controls are not fully modeled

Use the score as a prioritization aid for engineering and CI, not as the sole source of truth for security decisions.
