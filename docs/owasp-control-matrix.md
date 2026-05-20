# OWASP Control Matrix

Pluto AgentGuard maps every finding, test, and evidence artifact to OWASP MCP Top 10 and OWASP LLM Top 10 controls.

## OWASP MCP Top 10 Coverage

| OWASP Risk | AgentGuard Controls | Commands | Evidence |
|---|---|---|---|
| **MCP01:2025** Token Mismanagement & Secret Exposure | Secret scanning (18+ patterns), static token detection, Dockerfile ENV secrets, .env gitignore check | `scan` | Finding + redacted evidence + remediation |
| **MCP02:2025** Privilege Escalation via Scope Creep | Wildcard permission detection, allowlist validation, permission risk scoring, baseline drift | `scan`, `baseline` | Risk score + drift report |
| **MCP03:2025** Tool Poisoning | Tool-description injection scan, tool-poisoning attack pack | `scan`, `test` | Finding + test results |
| **MCP04:2025** Supply Chain & Dependency Tampering | Unpinned AI dependency detection | `scan` | Finding + package list |
| **MCP05:2025** Command Injection & Execution | Dangerous tool detection, HITL checks, denied tool monitoring, eval/exec on LLM output detection | `scan`, `monitor`, `test` | Violation report + test results |
| **MCP06:2025** Intent Flow Subversion | Prompt injection attack pack (4 scenarios) | `test` | Attack test results |
| **MCP07:2025** Insufficient Authentication & Authorization | Remote server auth check, insecure HTTP transport detection | `scan` | Finding + remediation |
| **MCP08:2025** Lack of Audit and Telemetry | Behavioral monitoring, evidence packets, trace analysis | `monitor`, `evidence` | Policy coverage + audit trail |
| **MCP09:2025** Shadow MCP Servers | — | — | *Planned: v1.0* |
| **MCP10:2025** Context Injection & Over-Sharing | System prompt leak detection | `scan` | Finding + remediation |

## OWASP LLM Top 10 Coverage

| OWASP Risk | AgentGuard Controls | Commands |
|---|---|---|
| **LLM01:2025** Prompt Injection | Prompt injection attack pack, tool description scan | `test`, `scan` |
| **LLM02:2025** Sensitive Information Disclosure | Secret scanning, system prompt leak detection | `scan` |
| **LLM03:2025** Supply Chain Vulnerabilities | Unpinned dependency detection | `scan` |
| **LLM05:2025** Improper Output Handling | eval/exec on LLM output detection | `scan` |
| **LLM06:2025** Excessive Agency | Permission scanner, HITL gates, denied tools, policy testing | `scan`, `monitor`, `test` |
| **LLM08:2025** Vector & Embedding Weaknesses | — | *Planned* |
| **LLM10:2025** Unbounded Consumption | Rate limit and timeout checks | `scan` |

## Control Coverage Summary

- **OWASP MCP Top 10**: 9/10 risks covered (MCP09 planned)
- **OWASP LLM Top 10**: 6/10 risks covered
- **Total controls implemented**: 20+
- **Attack test scenarios**: 17
