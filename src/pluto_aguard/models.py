"""Core data models for Pluto AgentGuard."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Severity levels for findings."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Finding(BaseModel):
    """A security finding from a scan or monitor session."""

    id: str
    title: str
    description: str
    severity: Severity
    category: str
    owasp_id: str | None = None
    file_path: str | None = None
    line_number: int | None = None
    evidence: str | None = None
    remediation: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class RiskScore(BaseModel):
    """Risk score for an agent configuration."""

    overall: float = Field(ge=0, le=100)
    breakdown: dict[str, float] = Field(default_factory=dict)
    finding_count: dict[Severity, int] = Field(default_factory=dict)


class PolicyChange(BaseModel):
    """A proposed policy change for What-If simulation."""

    id: str
    description: str
    category: str
    reasoning: str | None = None
    expected_impact: dict[str, Any] = Field(default_factory=dict)


class SimulationResult(BaseModel):
    """Result of a What-If policy simulation."""

    original_score: RiskScore
    new_score: RiskScore
    applied_policies: list[PolicyChange]
    score_delta: float
    score_delta_pct: float
    recommendations: list[str] = Field(default_factory=list)


class AgentAction(BaseModel):
    """A recorded agent action from monitoring."""

    turn: int
    timestamp: str | None = None
    action_type: str  # tool_call, response, data_access
    tool_name: str | None = None
    tool_args: dict[str, Any] = Field(default_factory=dict)
    result_summary: str | None = None
    call_id: str | None = None  # e.g. gen_ai.tool.call.id -- binds to a specific ApprovalEvent
    violations: list[Finding] = Field(default_factory=list)


class AgentPolicy(BaseModel):
    """Declared policy/permissions for an agent."""

    name: str
    allowed_tools: list[str] = Field(default_factory=list)
    denied_tools: list[str] = Field(default_factory=list)
    max_permissions: dict[str, str] = Field(default_factory=dict)  # tool -> permission level
    require_human_approval: list[str] = Field(default_factory=list)  # actions needing approval
    data_access_rules: dict[str, str] = Field(default_factory=dict)  # resource -> access level


class ApprovalEvent(BaseModel):
    """A recorded approval for a tool invocation."""

    tool_name: str
    approved_by: str | None = None
    approval_id: str | None = None
    approved_at: str | None = None
    expired: bool = False
    call_id: str | None = None  # matches AgentAction.call_id for exact binding, if known


class ScanResult(BaseModel):
    """Complete result of a security scan."""

    project_path: str
    findings: list[Finding] = Field(default_factory=list)
    risk_score: RiskScore
    scanned_files: int = 0
    scan_duration_ms: int = 0
    suppressed_count: int = 0


class ControlResult(BaseModel):
    """An OWASP-aligned control check result."""

    control_id: str  # e.g., AGC-MCP01-001
    owasp_refs: list[str] = Field(default_factory=list)  # e.g., ["MCP01:2025"]
    title: str
    status: str  # pass, fail, warning, not_tested
    command: str  # scan, monitor, whatif, evidence, baseline, test
    findings: list[Finding] = Field(default_factory=list)
    remediation: str = ""
