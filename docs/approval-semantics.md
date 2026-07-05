# Approval Semantics

`aguard monitor` treats a human approval as authorizing exactly one tool
call, not the tool for the rest of the trace. This page covers what that
means and how matching works.

## Single-use

Each approval event is consumed the first time it's matched against a
qualifying action. A second call to the same tool needs its own approval —
it won't be silently blessed by the first one.

```json
{"turn": 1, "action_type": "approval", "tool_name": "file_write", "approved_by": "alice"}
{"turn": 2, "action_type": "tool_call", "tool_name": "file_write", "tool_args": {"path": "report1.csv"}}
{"turn": 3, "action_type": "tool_call", "tool_name": "file_write", "tool_args": {"path": "report2.csv"}}
```

Turn 2 uses the approval. Turn 3 raises `DRIFT-NO-APPROVAL` — the approval
from turn 1 was already spent. See
[examples/approval-reuse-attack.jsonl](../examples/approval-reuse-attack.jsonl),
verified end-to-end with `aguard monitor --trace-file examples/approval-reuse-attack.jsonl --policy examples/approval-policy.yaml`.

If multiple approvals for the same tool are pending, they're consumed
oldest-first (FIFO) -- with one exception: a non-expired approval is always
preferred over an expired one, even if the expired one is older. An expired
record sitting ahead of a valid one in the queue doesn't preempt the valid
one; expiry only surfaces once there's nothing usable left to consume.

## Exact binding via call_id

If both the approval and the action carry a matching `gen_ai.tool.call.id`
(or `call_id`), that specific approval is used regardless of FIFO order —
this is the strongest binding a trace can offer, since it ties the approval
to one specific call rather than "the next call to this tool name." When
`call_id` isn't present (most traces today), matching falls back to FIFO by
tool name.

## Backdated approvals

An approval must precede the action it authorizes. If both the approval's
`approved_at` and the action's `timestamp` are parseable and the approval
is timestamped *after* the action, `aguard monitor` raises
`DRIFT-BACKDATED-APPROVAL` (CRITICAL) — this indicates either a reordered/
tampered trace, or a process where the action actually ran before approval
was granted. Timestamps are compared as best-effort: ISO 8601 strings and
OTel's integer epoch (s/ms/us/ns, auto-detected by magnitude) are both
supported. If either side's timestamp is missing or unparseable, this
check is skipped rather than guessing — no false positive from a format
mismatch.

## What this doesn't do

This is still trace-replay analysis, not a live approval gate — `aguard
monitor` tells you after the fact whether the trace's approval records
line up with what actually ran. It can't stop an action from happening;
that's the MCP client's job. What it can do is catch the case where the
*audit trail itself* doesn't hold up: reused approvals, mismatched tools,
expired credentials, or out-of-order timestamps.
