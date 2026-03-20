# Telemetry & Audit

Structured security event emission for SOC integration, compliance, and observability.

## The Problem

Without structured telemetry, security events end up as unstructured log strings scattered across services. This makes it impossible to:

- Correlate events across a multi-agent chain
- Build dashboards for guardrail hit rates or judge decisions
- Feed a SIEM with machine-readable security data
- Trace a blocked request back to its root cause

## Event Schema

Every security-relevant action emits an `AISecurityEvent`, a typed, self-contained record:

```python
from airs.telemetry import AISecurityEvent, EventType

event = AISecurityEvent(
    event_type=EventType.GUARDRAIL_INPUT,
    correlation_id="abc123",           # ties all events in one request
    request_id="req_456",
    user_id="user_1",
    agent_chain=["orchestrator", "retriever"],
    delegation_depth=1,
    allowed=False,
    verdict="block",
    reason="Prompt injection pattern detected",
    layer="guardrail",
    pace_state="primary",
)

# Machine-readable output
print(event.to_json())
print(event.to_dict())
```

### Event Types

| Type | When It's Emitted |
|------|------------------|
| `guardrail.input` | Input guardrail evaluates a request |
| `guardrail.output` | Output guardrail evaluates a response |
| `judge.decision` | Model-as-Judge makes a verdict |
| `tool.policy` | Tool policy engine allows/denies a tool call |
| `delegation` | Agent-to-agent delegation is checked |
| `pace.transition` | PACE state changes (e.g. Primary → Alternate) |
| `circuit_breaker.state_change` | Circuit breaker opens, closes, or half-opens |
| `pipeline.input` | Full pipeline input evaluation completes |
| `pipeline.output` | Full pipeline output evaluation completes |

### Event Fields

Every event includes:

| Field | Purpose |
|-------|---------|
| `event_id` | Unique ID for this event |
| `event_type` | One of the types above |
| `timestamp` | When it happened |
| `correlation_id` | Ties events across an entire agent chain |
| `request_id` | Ties events to a specific AIRequest |
| `user_id` | The originating user |
| `agent_chain` | List of agent IDs that touched this request |
| `delegation_depth` | How deep in the delegation chain |
| `allowed` | Whether the action was permitted |
| `verdict` | Layer-specific verdict (pass/block/flag/escalate) |
| `reason` | Human-readable explanation |
| `confidence` | Judge confidence score (0.0–1.0) |
| `layer` | Which control layer (guardrail/judge/circuit_breaker) |
| `tool_name` | For tool policy events |
| `pace_state` | Current PACE state |
| `metadata` | Arbitrary key-value pairs |

## Audit Sinks

Events are sent to **audit sinks**, pluggable destinations. Register one or more:

### Log Sink (structured JSON to Python logging)

```python
from airs.telemetry import LogAuditSink
from airs.telemetry.events import register_sink

register_sink(LogAuditSink(logger_name="airs.audit"))
```

Output (one JSON line per event):
```json
{"event_id":"a1b2c3","event_type":"pipeline.input","allowed":true,"user_id":"user_1","agent_chain":["orch"],...}
```

### Callback Sink (custom handler)

```python
from airs.telemetry import CallbackAuditSink
from airs.telemetry.events import register_sink

def send_to_siem(event):
    # Send to Splunk, Elastic, Sentinel, etc.
    requests.post(SIEM_URL, json=event.to_dict())

register_sink(CallbackAuditSink(send_to_siem))
```

### Buffer Sink (in-memory, for testing or batch export)

```python
from airs.telemetry.audit import BufferAuditSink
from airs.telemetry.events import register_sink

sink = BufferAuditSink(max_size=10_000)
register_sink(sink)

# After running your pipeline...
for event in sink.events:
    print(event.event_type, event.allowed, event.reason)

sink.clear()
```

### Custom Sink

Implement the `AuditSink` interface:

```python
from airs.telemetry import AuditSink, AISecurityEvent

class MyDatabaseSink(AuditSink):
    def handle(self, event: AISecurityEvent) -> None:
        db.insert("security_events", event.to_dict())
```

## Automatic Pipeline Telemetry

The `SecurityPipeline` emits `pipeline.input` and `pipeline.output` events automatically. If an `AgentContext` is attached to the request, agent chain info is included:

```python
from airs.agents import AgentIdentity, AgentContext
from airs.core.models import AIRequest
from airs.runtime import SecurityPipeline
from airs.telemetry.audit import BufferAuditSink
from airs.telemetry.events import register_sink

# Capture events
sink = BufferAuditSink()
register_sink(sink)

# Build request with agent context
ctx = AgentContext(
    user_id="user_1",
    origin_agent=AgentIdentity(agent_id="orch"),
)
request = AIRequest(input_text="Hello", agent_context=ctx)

# Pipeline emits events automatically
pipeline = SecurityPipeline()
await pipeline.evaluate_input(request)

event = sink.events[0]
print(event.user_id)         # "user_1"
print(event.agent_chain)     # ["orch"]
print(event.correlation_id)  # matches ctx.correlation_id
```

## SOC Integration Pattern

For production, pipe events to your SIEM:

```python
import logging
from airs.telemetry import LogAuditSink
from airs.telemetry.events import register_sink

# Configure a dedicated logger that ships to your log aggregator
audit_logger = logging.getLogger("airs.audit")
audit_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address="/dev/log")
audit_logger.addHandler(handler)

# Register the sink - all pipeline events now go to syslog
register_sink(LogAuditSink(logger_name="airs.audit"))
```

From there, your SIEM can parse the JSON events and build:

- **Dashboards**: guardrail block rates, judge escalation trends, PACE state over time
- **Alerts**: circuit breaker trips, delegation depth anomalies, denied tool calls
- **Audit trails**: full request trace from user → agent chain → decision → action
