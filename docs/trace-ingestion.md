# Trace Ingestion

`aguard monitor` reads JSONL trace files (or stdin, with `--live`) one
event per line. It recognizes three shapes, tried in this order per line:

## 1. OTel GenAI semantic convention (real exporters)

What OpenLIT, OTel-native LangChain instrumentation, and other GenAI
observability SDKs actually emit — an OTel span (`name` + `attributes`)
using the `gen_ai.*` attribute namespace from the
[OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/):

```json
{
  "name": "execute_tool sql_query",
  "attributes": {
    "gen_ai.operation.name": "execute_tool",
    "gen_ai.tool.name": "sql_query",
    "gen_ai.tool.call.id": "call_1",
    "gen_ai.tool.call.arguments": "{\"query\": \"SELECT * FROM users\"}"
  },
  "startTimeUnixNano": 1730000000000000000
}
```

Recognized attributes:

| Attribute | Used for |
|---|---|
| `gen_ai.operation.name` | Action type (`execute_tool` → `tool_call`, `chat`/`generate_content`/`text_completion` → `response`) |
| `gen_ai.tool.name` | Tool name |
| `gen_ai.tool.call.arguments` | Tool arguments |
| `startTimeUnixNano` | Timestamp (integer nanoseconds — coerced to a string) |

There's no single stable `gen_ai.*` attribute for tool-call arguments across
the ecosystem yet, so `gen_ai.tool.arguments` and Traceloop's
`traceloop.entity.input`/`traceloop.entity.name` are also checked as
fallbacks. Since OTel span attribute values must be primitives (not nested
objects), arguments are usually a JSON-encoded string — this is parsed
automatically; a raw dict also works for callers building their own spans.

See [examples/otel-genai-traces.jsonl](../examples/otel-genai-traces.jsonl)
for a full example, verified end-to-end against `aguard monitor`.

## 2. This project's own OTel-shaped format

The same span shape, but with this project's pre-existing `tool.name` /
`tool.args` / `action_type` attributes instead of `gen_ai.*`. Still
supported for backward compatibility — see
[examples/sample-traces.jsonl](../examples/sample-traces.jsonl).

## 3. Flat simple format

A flat JSON object, no span wrapper:

```json
{"turn": 2, "action_type": "tool_call", "tool_name": "file_write", "tool_args": {"path": "/tmp/out.csv"}}
```

## Turn numbers

Finding IDs embed a turn number (e.g. `DRIFT-DENIED-TOOL-execute-T2`) to
keep them unique across a trace. `turn` is this project's own concept, not
part of any tracing standard, so real traces won't have it. When absent,
`aguard monitor` auto-assigns one per action, incrementing in the order
actions are processed. If a trace does specify `turn` explicitly, that
value is used as-is.
