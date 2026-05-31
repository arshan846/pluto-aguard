# Using Pluto AgentGuard as a GitHub Action

## Quick Start

Add to any workflow:

```yaml
- name: Agent Security Gate
  uses: arpitha-dhanapathi/pluto-aguard@v0.9.1
  with:
    path: '.'
    max-risk: '50'
    fail-on: 'high'
```

## Full Example with SARIF Upload

```yaml
name: Agent Security
on: [push, pull_request]

jobs:
  security-gate:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4

      - name: Run AgentGuard
       uses: arpitha-dhanapathi/pluto-aguard@v0.9.1
        with:
          path: '.'
          max-risk: '50'
          fail-on: 'high'
          sarif-output: 'aguard-results.sarif'

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: aguard-results.sarif
```

## With Policy Coverage Testing

```yaml
- name: Run AgentGuard with policy tests
  uses: arpitha-dhanapathi/pluto-aguard@v0.9.1
  with:
    path: '.'
    max-risk: '50'
    fail-on: 'high'
    policy: 'agent-policy.yaml'
    attack-pack: 'all'
```

## Inputs

| Input | Description | Default |
|---|---|---|
| `path` | Path to scan | `.` |
| `max-risk` | Maximum risk score (0-100) | — |
| `fail-on` | Minimum severity to fail (`critical`, `high`, `medium`, `low`) | — |
| `format` | Output format (`text`, `json`, `html`, `sarif`) | `text` |
| `policy` | Path to policy file for policy coverage testing | — |
| `attack-pack` | Attack pack to run | — |
| `sarif-output` | Path for SARIF file | — |
