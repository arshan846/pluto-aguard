"""Tests for the behavioral monitor."""

import json
from pathlib import Path

from pluto_aguard.models import AgentPolicy, ApprovalEvent, Severity
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

    def test_parses_approval_event(self) -> None:
        line = json.dumps({
            "action_type": "approval",
            "tool_name": "file_write",
            "approved_by": "alice",
            "approval_id": "appr-123",
        })
        action = parse_trace_line(line)
        assert isinstance(action, ApprovalEvent)
        assert action.tool_name == "file_write"
        assert action.approved_by == "alice"


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
            "tool_args": {"path": "data.csv"},
        })
        action = parse_trace_line(line)
        assert action is not None
        violations = check_action_against_policy(action, self.policy)
        assert any("approval" in v.title.lower() for v in violations)

    def test_valid_approval_suppresses_violation(self) -> None:
        line = json.dumps({
            "turn": 1,
            "action_type": "tool_call",
            "tool_name": "file_write",
            "tool_args": {"path": "data.csv"},
        })
        action = parse_trace_line(line)
        assert action is not None
        violations = check_action_against_policy(
            action,
            self.policy,
            approvals={"file_write": ApprovalEvent(tool_name="file_write", approved_by="alice")},
        )
        assert not any("approval" in v.title.lower() for v in violations)

    def test_detects_expired_approval(self) -> None:
        line = json.dumps({
            "turn": 1,
            "action_type": "tool_call",
            "tool_name": "file_write",
            "tool_args": {"path": "data.csv"},
        })
        action = parse_trace_line(line)
        assert action is not None
        violations = check_action_against_policy(
            action,
            self.policy,
            approvals={"file_write": ApprovalEvent(tool_name="file_write", expired=True)},
        )
        assert any("expired approval" in v.title.lower() for v in violations)

    def test_detects_mismatched_approval(self) -> None:
        line = json.dumps({
            "turn": 1,
            "action_type": "tool_call",
            "tool_name": "file_write",
            "tool_args": {"path": "data.csv"},
        })
        action = parse_trace_line(line)
        assert action is not None
        violations = check_action_against_policy(
            action,
            self.policy,
            approvals={"deploy": ApprovalEvent(tool_name="deploy", approved_by="alice")},
        )
        assert any("mismatched approval" in v.title.lower() for v in violations)

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

    def test_read_query_with_create_substring_not_flagged(self) -> None:
        """SELECT of a 'created_at' column must not trip the write-word check."""
        line = json.dumps({
            "turn": 1,
            "action_type": "tool_call",
            "tool_name": "sql_query",
            "tool_args": {"query": "SELECT created_at FROM orders"},
        })
        action = parse_trace_line(line)
        assert action is not None
        violations = check_action_against_policy(action, self.policy)
        assert not any("escalation" in v.title.lower() for v in violations)

    def test_postgres_connection_string_not_flagged_as_post(self) -> None:
        """A 'postgres://' connection string must not trip the 'post' write-word check."""
        line = json.dumps({
            "turn": 1,
            "action_type": "tool_call",
            "tool_name": "sql_query",
            "tool_args": {"connection": "postgres://readonly_user@db/analytics"},
        })
        action = parse_trace_line(line)
        assert action is not None
        violations = check_action_against_policy(action, self.policy)
        assert not any("escalation" in v.title.lower() for v in violations)
