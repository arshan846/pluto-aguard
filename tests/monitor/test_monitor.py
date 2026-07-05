"""Tests for the behavioral monitor."""

import json
from pathlib import Path

from pluto_aguard.models import AgentAction, AgentPolicy, ApprovalEvent, Severity
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

    def test_parses_otel_genai_semantic_convention(self) -> None:
        """Real exporters (OpenLIT, OTel-native LangChain) use gen_ai.* names,
        not this project's ad-hoc tool.name/tool.args -- and OTel attribute
        values must be primitives, so structured arguments are typically a
        JSON-encoded string, not a nested object."""
        line = json.dumps({
            "name": "execute_tool sql_query",
            "attributes": {
                "gen_ai.operation.name": "execute_tool",
                "gen_ai.tool.name": "sql_query",
                "gen_ai.tool.call.id": "call_1",
                "gen_ai.tool.call.arguments": json.dumps({"query": "SELECT * FROM users"}),
            },
        })
        action = parse_trace_line(line)
        assert isinstance(action, AgentAction)
        assert action.tool_name == "sql_query"
        assert action.action_type == "tool_call"
        assert action.tool_args == {"query": "SELECT * FROM users"}

    def test_coerces_integer_otel_timestamp(self) -> None:
        """startTimeUnixNano is an integer in real OTel spans; the model
        stores timestamp as a string."""
        line = json.dumps({
            "name": "execute_tool sql_query",
            "attributes": {"gen_ai.tool.name": "sql_query", "gen_ai.operation.name": "execute_tool"},
            "startTimeUnixNano": 1730000000000000000,
        })
        action = parse_trace_line(line)
        assert isinstance(action, AgentAction)
        assert action.timestamp == "1730000000000000000"

    def test_default_turn_used_when_absent(self) -> None:
        """Real traces have no 'turn' attribute -- the caller supplies a
        fallback (auto-incremented per action by _process_trace_lines)."""
        line = json.dumps({
            "name": "execute_tool sql_query",
            "attributes": {"gen_ai.tool.name": "sql_query", "gen_ai.operation.name": "execute_tool"},
        })
        action = parse_trace_line(line, default_turn=3)
        assert isinstance(action, AgentAction)
        assert action.turn == 3

    def test_explicit_turn_overrides_default(self) -> None:
        line = json.dumps({
            "name": "sql_query",
            "attributes": {"turn": 7, "tool.name": "sql_query", "action_type": "tool_call"},
        })
        action = parse_trace_line(line, default_turn=3)
        assert isinstance(action, AgentAction)
        assert action.turn == 7


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
            approvals={"file_write": [ApprovalEvent(tool_name="file_write", approved_by="alice")]},
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
            approvals={"file_write": [ApprovalEvent(tool_name="file_write", expired=True)]},
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
            approvals={"deploy": [ApprovalEvent(tool_name="deploy", approved_by="alice")]},
        )
        assert any("mismatched approval" in v.title.lower() for v in violations)

    def test_approval_is_single_use(self) -> None:
        """One approval must not bless every subsequent call to the same tool."""
        approvals: dict[str, list[ApprovalEvent]] = {
            "file_write": [ApprovalEvent(tool_name="file_write", approved_by="alice")]
        }
        first_call = AgentAction(turn=1, action_type="tool_call", tool_name="file_write", tool_args={})
        second_call = AgentAction(turn=2, action_type="tool_call", tool_name="file_write", tool_args={})

        first_violations = check_action_against_policy(first_call, self.policy, approvals=approvals)
        assert not any("approval" in v.title.lower() for v in first_violations)

        second_violations = check_action_against_policy(second_call, self.policy, approvals=approvals)
        assert any("without human approval" in v.title.lower() for v in second_violations)

    def test_call_id_binds_exact_approval(self) -> None:
        """An action referencing a specific call_id should consume the
        matching approval even if it isn't first in the queue."""
        approvals: dict[str, list[ApprovalEvent]] = {
            "file_write": [
                ApprovalEvent(tool_name="file_write", approved_by="alice", call_id="call_A"),
                ApprovalEvent(tool_name="file_write", approved_by="bob", call_id="call_B"),
            ]
        }
        action_b = AgentAction(
            turn=1, action_type="tool_call", tool_name="file_write", tool_args={}, call_id="call_B"
        )
        violations = check_action_against_policy(action_b, self.policy, approvals=approvals)
        assert not any("approval" in v.title.lower() for v in violations)
        # call_A's approval must still be pending -- only call_B's was consumed
        assert len(approvals["file_write"]) == 1
        assert approvals["file_write"][0].call_id == "call_A"

    def test_backdated_approval_detected(self) -> None:
        """An approval timestamped after the action it's supposed to cover
        indicates a reordered trace or an action that ran before approval."""
        approvals: dict[str, list[ApprovalEvent]] = {
            "file_write": [
                ApprovalEvent(tool_name="file_write", approved_by="alice", approved_at="2026-01-01T12:00:00Z")
            ]
        }
        action = AgentAction(
            turn=1,
            action_type="tool_call",
            tool_name="file_write",
            tool_args={},
            timestamp="2026-01-01T11:00:00Z",
        )
        violations = check_action_against_policy(action, self.policy, approvals=approvals)
        assert any("recorded after the action ran" in v.title.lower() for v in violations)
        assert any(v.severity == Severity.CRITICAL for v in violations)

    def test_missing_timestamps_not_flagged_as_backdated(self) -> None:
        """Without parseable timestamps on both sides, don't guess -- no
        false-positive backdated finding."""
        approvals: dict[str, list[ApprovalEvent]] = {
            "file_write": [ApprovalEvent(tool_name="file_write", approved_by="alice")]
        }
        action = AgentAction(turn=1, action_type="tool_call", tool_name="file_write", tool_args={})
        violations = check_action_against_policy(action, self.policy, approvals=approvals)
        assert not any("backdated" in v.id.lower() for v in violations)

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
