# Circuit Breaker & PACE — Resilience

Two mechanisms ensure your AI system degrades safely when things go wrong:

- **Circuit Breaker** — emergency stop that blocks all AI traffic when failure rates spike
- **PACE Controller** — structured degradation through four operational postures

## Circuit Breaker

The circuit breaker monitors request success/failure rates and trips when thresholds are exceeded. When tripped, all AI traffic is blocked and a non-AI fallback serves requests.

### Basic Usage

```python
from airs.runtime import CircuitBreaker

breaker = CircuitBreaker()

# In your request handler
if breaker.allow_request():
    try:
        response = await call_ai_model(input)
        breaker.record_success()
    except Exception as e:
        breaker.record_failure(str(e))
        response = fallback_response()
else:
    response = fallback_response()
```

### Configuration

```python
from airs.runtime.circuit_breaker import CircuitBreakerConfig

breaker = CircuitBreaker(
    config=CircuitBreakerConfig(
        failure_threshold=5,         # trip after 5 failures...
        window_seconds=60.0,         # ...within a 60-second window
        recovery_timeout=300.0,      # wait 5 min before testing recovery
        block_rate_threshold=0.20,   # also trip if >20% of requests fail
        half_open_max_requests=3,    # allow 3 test requests during recovery
    ),
)
```

### Circuit States

![Circuit Breaker States](../images/sdk-circuit-breaker-states.svg)

| State | AI Traffic | Description |
|-------|-----------|-------------|
| **CLOSED** | Flowing | Normal operation. Failures are being counted. |
| **OPEN** | Blocked | Threshold exceeded. All AI requests go to fallback. |
| **HALF_OPEN** | Limited | Recovery test. A few requests are allowed through. If they succeed, the breaker closes. If any fail, it re-opens. |

### Manual Controls

```python
# Emergency stop
breaker.trip("Incident #1234 — confirmed attack")

# Resume after incident resolution
breaker.reset()

# Check status
stats = breaker.stats()
# {
#     "state": "closed",
#     "total_events": 142,
#     "failures": 3,
#     "failure_rate": 0.021,
#     "threshold": 5,
#     "block_rate_threshold": 0.20,
# }
```

### State Change Callbacks

Get notified when the circuit breaker changes state:

```python
def on_state_change(old_state, new_state):
    if new_state == CircuitState.OPEN:
        send_pagerduty_alert(f"Circuit breaker tripped: {old_state} → {new_state}")
    elif new_state == CircuitState.CLOSED:
        send_slack_message("Circuit breaker recovered — AI traffic resumed")

breaker = CircuitBreaker(on_state_change=on_state_change)
```

---

## PACE Controller

PACE provides structured degradation — instead of binary on/off, your system moves through four postures with defined behaviors at each level.

### The Four States

| State | When | Judge | Human Approval | Autonomy |
|-------|------|-------|---------------|----------|
| **Primary** | Normal operation | 5% sampling | No | Full |
| **Alternate** | One control degraded | 100% evaluation | No | Reduced (no new tools) |
| **Contingency** | Multiple controls degraded | 100% evaluation | Yes — all outputs | Minimal (read-only) |
| **Emergency** | Confirmed compromise | Disabled (AI off) | Yes | None (circuit breaker fires) |

### Basic Usage

```python
from airs.runtime import PACEController

pace = PACEController()

# Normal operation
assert pace.state == "primary"
assert pace.requires_human_approval() == False

# Something degrades → escalate one level
pace.escalate("Judge service timeout — falling back to rule-based")
assert pace.state == "alternate"

# Getting worse → escalate again
pace.escalate("Guardrail block rate >30%")
assert pace.state == "contingency"
assert pace.requires_human_approval() == True

# Confirmed compromise → jump to emergency
pace.emergency("Confirmed prompt injection bypassing all guardrails")
assert pace.state == "emergency"
```

### Escalation Rules

- **Escalation is one-directional** during an incident: P → A → C → E
- **You can jump directly to Emergency** with `pace.emergency()`
- **You cannot escalate past Emergency** — calling `escalate()` at Emergency is a no-op

### Recovery

Recovery requires explicit human authorization. No automatic recovery:

```python
# Recovery steps down one level at a time
pace.recover(authorized_by="admin@company.com")  # E → C
pace.recover(authorized_by="admin@company.com")  # C → A
pace.recover(authorized_by="admin@company.com")  # A → P

# Or jump straight to Primary
pace.full_recovery(authorized_by="admin@company.com")

# Recovery without authorization raises an error
pace.recover()  # ValueError: Recovery requires authorized_by
```

### Querying PACE Policy

Check the current posture's policy to control your application behavior:

```python
policy = pace.current_policy()
# {
#     "judge_mode": "sampling",      # or "all" or "disabled"
#     "judge_sample_rate": 0.05,     # 5% at Primary
#     "human_approval_required": False,
#     "max_autonomy": "full",
# }

# Convenience methods
if pace.requires_human_approval():
    await queue_for_review(request)

if pace.should_judge():
    result = await judge.evaluate(input_text, output_text)
```

### Custom PACE Policy

Override the default posture behavior:

```python
from airs.runtime.pace import PACEPolicy

policy = PACEPolicy(
    primary={
        "judge_mode": "sampling",
        "judge_sample_rate": 0.10,       # 10% instead of 5%
        "human_approval_required": False,
        "max_autonomy": "full",
    },
    alternate={
        "judge_mode": "all",
        "judge_sample_rate": 1.0,
        "human_approval_required": False,
        "max_autonomy": "reduced",
        "alert_level": "warning",        # custom fields
    },
    contingency={
        "judge_mode": "all",
        "judge_sample_rate": 1.0,
        "human_approval_required": True,
        "max_autonomy": "read_only",
        "alert_level": "critical",
    },
    emergency={
        "judge_mode": "disabled",
        "judge_sample_rate": 0.0,
        "human_approval_required": True,
        "max_autonomy": "none",
        "alert_level": "emergency",
    },
)

pace = PACEController(policy=policy)
```

### Transition Callbacks

Get notified on every state transition:

```python
from airs.runtime.pace import PACETransition

def on_transition(transition: PACETransition):
    log.info(
        "PACE %s → %s | reason: %s | by: %s",
        transition.from_state,
        transition.to_state,
        transition.reason,
        transition.authorized_by,
    )
    if transition.to_state == "emergency":
        trigger_incident_response(transition.reason)

pace = PACEController(on_transition=on_transition)
```

### Audit Trail

Every transition is recorded:

```python
for t in pace.history:
    print(f"{t.timestamp}: {t.from_state} → {t.to_state} ({t.reason}, by {t.authorized_by})")
```

## Using Together

In the `SecurityPipeline`, the circuit breaker and PACE work together:

- PACE controls the **judge sampling rate** and **human approval requirements**
- The circuit breaker controls whether **any AI traffic flows at all**
- Judge escalations automatically trigger PACE escalation
- When PACE reaches EMERGENCY, the circuit breaker should be tripped

```python
from airs.runtime import SecurityPipeline, CircuitBreaker, PACEController

pipeline = SecurityPipeline(
    circuit_breaker=CircuitBreaker(
        on_state_change=lambda old, new: alert_team(old, new),
    ),
    pace=PACEController(
        on_transition=lambda t: log_transition(t),
    ),
)
```

See [Pipeline](pipeline.md) for the full orchestration details.
