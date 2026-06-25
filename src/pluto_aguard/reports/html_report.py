"""HTML report generator for scan results."""

from __future__ import annotations

from pluto_aguard.models import ScanResult, Severity


def generate_html(result: ScanResult) -> str:
    """Generate a standalone HTML report from scan results."""
    findings_html = ""
    for finding in sorted(result.findings, key=lambda f: list(Severity).index(f.severity)):
        sev_class = finding.severity.value
        owasp = f' <span class="owasp">{finding.owasp_id}</span>' if finding.owasp_id else ""

        findings_html += f"""
        <div class="finding {sev_class}">
            <div class="finding-header">
                <span class="severity-badge {sev_class}">{finding.severity.value.upper()}</span>
                <span class="finding-title">{finding.title}</span>
                {owasp}
            </div>
            <p class="finding-desc">{finding.description}</p>
            {"<p class='finding-file'>📄 " + finding.file_path + (f":{finding.line_number}" if finding.line_number else "") + "</p>" if finding.file_path else ""}
            {"<p class='finding-evidence'>Evidence: <code>" + finding.evidence + "</code></p>" if finding.evidence else ""}
            {"<p class='finding-remediation'>💡 " + finding.remediation + "</p>" if finding.remediation else ""}
        </div>
        """

    score = result.risk_score.overall
    score_color = "#ef4444" if score >= 75 else "#f59e0b" if score >= 50 else "#3b82f6" if score >= 25 else "#22c55e"

    counts = result.risk_score.finding_count
    critical = counts.get(Severity.CRITICAL, 0)
    high = counts.get(Severity.HIGH, 0)
    medium = counts.get(Severity.MEDIUM, 0)
    low = counts.get(Severity.LOW, 0)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pluto AgentGuard — Security Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #e2e8f0; padding: 2rem; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
        .subtitle {{ color: #94a3b8; margin-bottom: 2rem; }}
        .score-card {{ background: #1e293b; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; display: flex; align-items: center; gap: 2rem; }}
        .score-number {{ font-size: 3rem; font-weight: bold; color: {score_color}; }}
        .score-label {{ color: #94a3b8; font-size: 0.9rem; }}
        .stats {{ display: flex; gap: 1.5rem; }}
        .stat {{ text-align: center; }}
        .stat-number {{ font-size: 1.5rem; font-weight: bold; }}
        .stat-label {{ font-size: 0.75rem; color: #94a3b8; }}
        .finding {{ background: #1e293b; border-radius: 8px; padding: 1.2rem; margin-bottom: 0.8rem; border-left: 4px solid #475569; }}
        .finding.critical {{ border-left-color: #ef4444; }}
        .finding.high {{ border-left-color: #f97316; }}
        .finding.medium {{ border-left-color: #f59e0b; }}
        .finding.low {{ border-left-color: #3b82f6; }}
        .finding-header {{ display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.5rem; }}
        .severity-badge {{ padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; }}
        .severity-badge.critical {{ background: #7f1d1d; color: #fca5a5; }}
        .severity-badge.high {{ background: #7c2d12; color: #fdba74; }}
        .severity-badge.medium {{ background: #713f12; color: #fde047; }}
        .severity-badge.low {{ background: #1e3a5f; color: #93c5fd; }}
        .finding-title {{ font-weight: 600; }}
        .owasp {{ color: #94a3b8; font-size: 0.8rem; }}
        .finding-desc {{ color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.5rem; }}
        .finding-file {{ color: #64748b; font-size: 0.8rem; }}
        .finding-evidence {{ color: #64748b; font-size: 0.8rem; }}
        .finding-evidence code {{ background: #0f172a; padding: 2px 6px; border-radius: 3px; }}
        .finding-remediation {{ color: #86efac; font-size: 0.85rem; margin-top: 0.5rem; }}
        .footer {{ text-align: center; color: #475569; margin-top: 2rem; font-size: 0.8rem; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Pluto AgentGuard — Security Report</h1>
        <p class="subtitle">{result.project_path} · {result.scanned_files} files scanned · {result.scan_duration_ms}ms</p>

        <div class="score-card">
            <div>
                <div class="score-number">{score:.0f}</div>
                <div class="score-label">Risk Score / 100</div>
            </div>
            <div class="stats">
                <div class="stat"><div class="stat-number" style="color:#ef4444">{critical}</div><div class="stat-label">Critical</div></div>
                <div class="stat"><div class="stat-number" style="color:#f97316">{high}</div><div class="stat-label">High</div></div>
                <div class="stat"><div class="stat-number" style="color:#f59e0b">{medium}</div><div class="stat-label">Medium</div></div>
                <div class="stat"><div class="stat-number" style="color:#3b82f6">{low}</div><div class="stat-label">Low</div></div>
            </div>
        </div>

        {findings_html}

        <div class="footer">Generated by Pluto AgentGuard v0.9.2 · github.com/arpitha-dhanapathi/pluto-aguard</div>
    </div>
</body>
</html>"""
