"""SARIF report generator for GitHub Advanced Security integration."""

from __future__ import annotations

import json

from pluto_aguard.models import ScanResult, Severity

SARIF_SEVERITY_MAP = {
    Severity.CRITICAL: "error",
    Severity.HIGH: "error",
    Severity.MEDIUM: "warning",
    Severity.LOW: "note",
    Severity.INFO: "note",
}


def generate_sarif(result: ScanResult) -> str:
    """Generate a SARIF 2.1.0 report from scan results."""
    rules = []
    rule_ids_seen: set[str] = set()
    results_list = []

    for finding in result.findings:
        rule_id = finding.owasp_id or finding.category
        if rule_id not in rule_ids_seen:
            rule_ids_seen.add(rule_id)
            rules.append(
                {
                    "id": rule_id,
                    "name": finding.category.replace("_", " ").title(),
                    "shortDescription": {"text": finding.title},
                    "helpUri": "https://owasp.org/www-project-mcp-top-10/",
                    "defaultConfiguration": {
                        "level": SARIF_SEVERITY_MAP.get(finding.severity, "warning"),
                    },
                }
            )

        sarif_result: dict = {
            "ruleId": rule_id,
            "level": SARIF_SEVERITY_MAP.get(finding.severity, "warning"),
            "message": {"text": finding.description},
        }

        if finding.file_path:
            location: dict = {
                "physicalLocation": {
                    "artifactLocation": {"uri": finding.file_path.replace("\\", "/")},
                }
            }
            if finding.line_number:
                location["physicalLocation"]["region"] = {
                    "startLine": finding.line_number,
                }
            sarif_result["locations"] = [location]

        if finding.remediation:
            sarif_result["fixes"] = [{"description": {"text": finding.remediation}}]

        results_list.append(sarif_result)

    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "pluto-aguard",
                        "version": "0.9.2",
                        "informationUri": "https://github.com/arpitha-dhanapathi/pluto-aguard",
                        "rules": rules,
                    }
                },
                "results": results_list,
            }
        ],
    }

    return json.dumps(sarif, indent=2)
