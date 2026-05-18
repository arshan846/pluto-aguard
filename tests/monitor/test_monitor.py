"""Tests for the behavioral monitor."""

import json
from pathlib import Path

from pluto_aguard.models import AgentPolicy, Severity
from pluto_aguard.monitor.runner import (
    check_action_against_policy,
    parse_trace_line,
)


class TestTraceParser:
    """Tests for trace line parsing."""

    def test_parses_otel_format(self) -> None:
        line = json.dumps({
            "name": "sql_query",
            "attributes": {
                "turn": 1,
                "action_type": "tool_call",
                "tool.name": "sql_query",
                "tool.args": {"query": "SELECT * FROM users"},
            },
        })
        action = parse_trace_line(line)
        assert action is not None
        assert action.tool_name == "sql_query"
        assert action.turn == 1

    def test_parses_simple_format(self) -> None:
        line = json.dumps({
            "turn": 2,
            "action_type": "tool_call",
            "tool_name": "file_write",
            "tool_args": {"path": "/tmp/out.csv"},
        })
        action = parse_trace_line(line)
        assert action is not None
        assert action.tool_name == "file_write"

    def test_handles_invalid_json(self) -> None:
        action = parse_trace_line("not valid json")
        assert action is None

    def test_handles_empty_line(self) -> None:
        action = parse_trace_line("")
        assert action is None


class TestPolicyChecker:
    """Tests for checking actions against policies."""

    def setup_method(self) -> None:
        self.policy = AgentPolicy(
            name="test-agent",
            allowed_tools=["sql_query", "send_message"],
            denied_tools=["execute", "shell"],
            max_permissions={"sql_query": "read"},
            require_human_approval=["file_write"],
        )

    def test_detects_denied_tool(self) -> None:
        line = json.dumps({
            "turn": 1,
            "action_type": "tool_call",
            "tool_name": "execute",
            "tool_args": {"command": "rm -rf /"},
        })
        action = parse_trace_line(line)
        assert action is not None
        violations = check_action_against_policy(action, self.policy)
        assert any(v.severity == Severity.CRITICAL for v in violations)

    def test_detects_unauthorized_tool(self) -> None:
        line = json.dumps({
            "turn": 1,
            "action_type": "tool_call",
            "tool_name": "deploy",
            "tool_args": {},
        })
        action = parse_trace_line(line)
        assert action is not None
        violations = check_action_against_policy(action, self.policy)
        assert any("unauthorized" in v.title.lower() for v in violations)

    def test_detects_missing_approval(self) -> None:
        line = json.dumps({
            "turn": 1,
            "action_type": "tool_call",
            "tool_name": "file_write",
            "tool_args": {"path": "/tmp/data.csv"},
        })
        action = parse_trace_line(line)
        assert action is not None
        violations = check_action_against_policy(action, self.policy)
        assert any("approval" in v.title.lower() for v in violations)

    def test_allowed_tool_no_violations(self) -> None:
        line = json.dumps({
            "turn": 1,
            "action_type": "tool_call",
            "tool_name": "sql_query",
            "tool_args": {"query": "SELECT count(*) FROM orders"},
        })
        action = parse_trace_line(line)
        assert action is not None
        violations = check_action_against_policy(action, self.policy)
        assert len(violations) == 0

    def test_detects_permission_escalation(self) -> None:
        line = json.dumps({
            "turn": 1,
            "action_type": "tool_call",
            "tool_name": "sql_query",
            "tool_args": {"query": "DELETE FROM users WHERE id = 1"},
        })
        action = parse_trace_line(line)
        assert action is not None
        violations = check_action_against_policy(action, self.policy)
        assert any("escalation" in v.title.lower() for v in violations)
