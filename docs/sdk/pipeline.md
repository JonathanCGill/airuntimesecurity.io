# Security Pipeline

The `SecurityPipeline` orchestrates all three layers into a single evaluation flow. It is the main entry point for integrating AIRS into your application.

## Building a Pipeline

```python
from airs.runtime import (
    SecurityPipeline, GuardrailChain, RegexGuardrail,
    ContentPolicyGuardrail, CircuitBreaker, PACEController,
)
from airs.runtime.judge import RuleBasedJudge
from airs.runtime.pipeline import PipelineConfig

pipeline = SecurityPipeline(
    guardrails=GuardrailChain([
        RegexGuardrail(),
        ContentPolicyGuardrail(blocked_terms=["classified"]),
    ]),
    judge=RuleBasedJudge(),
    circuit_breaker=CircuitBreaker(),
    pace=PACEController(),
    config=PipelineConfig(
        input_guardrails=True,     # Run guardrails on input
        output_guardrails=True,    # Run guardrails on output
        judge_enabled=True,        # Enable judge evaluation
        pace_enabled=True,         # Let PACE control judge sampling
        block_on_review=False,     # True = block on REVIEW, False = log only
        fallback_response="Service temporarily unavailable.",
    ),
)
```

## Evaluation Flow

The pipeline does **not** call your AI model. It provides two methods — `evaluate_input()` and `evaluate_output()` — that you call *around* your own model call. This keeps AIRS model-agnostic: it works with any provider, framework, or architecture.

```python
from airs.core.models import AIRequest, AIResponse

# 1. Evaluate input
request = AIRequest(
    input_text=user_input,
    user_id="user_123",
    session_id="sess_abc",
    model="gpt-4o",
)
input_result = await pipeline.evaluate_input(request)

if not input_result.allowed:
    return error_response(input_result)

# 2. Call your model
ai_output = await your_model(request.input_text)

# 3. Evaluate output
response = AIResponse(
    request_id=request.request_id,
    output_text=ai_output,
    model="gpt-4o",
)
output_result = await pipeline.evaluate_output(request, response)

if not output_result.allowed:
    return error_response(output_result)

# 4. Return to user
return ai_output
```

### Input Evaluation

`evaluate_input()` runs these checks in order:

1. **Circuit breaker** — if OPEN, immediately return blocked
2. **Input guardrails** — run the guardrail chain on input text
3. If blocked by guardrails → record failure on circuit breaker, return blocked

### Output Evaluation

`evaluate_output()` runs these checks in order:

1. **Output guardrails** — run the guardrail chain on output text
2. **Judge** — if PACE sampling triggers (or guardrail flagged), evaluate with judge
3. **Human approval** — if PACE state requires human approval, return pending
4. If all pass → record success on circuit breaker, return allowed

## Pipeline Result

Both methods return a `PipelineResult`:

```python
result = await pipeline.evaluate_output(request, response)

result.allowed          # bool — should this be delivered?
result.pace_state       # PACEState — current PACE posture
result.blocked_by       # ControlLayer | None — which layer blocked
result.layer_results    # list[LayerResult] — each layer's result
result.total_latency_ms # float — total evaluation time

# Convenience accessors
result.guardrail_result  # LayerResult for guardrails
result.judge_result      # LayerResult for judge
```

### Handling Blocked Responses

```python
if not result.allowed:
    if result.blocked_by == ControlLayer.CIRCUIT_BREAKER:
        # System is in emergency mode
        return {"error": "Service unavailable", "retry_after": 300}

    elif result.blocked_by == ControlLayer.GUARDRAIL:
        # Known-bad pattern detected
        log.warning("Guardrail block: %s", result.guardrail_result.reason)
        return {"error": "Request could not be processed"}

    elif result.blocked_by == ControlLayer.JUDGE:
        # Policy violation detected
        log.warning("Judge escalation: %s", result.judge_result.reason)
        return {"error": "Response withheld pending review"}

    elif result.blocked_by == ControlLayer.HUMAN:
        # PACE requires human approval
        await queue_for_review(request, response)
        return {"status": "pending_review"}
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `input_guardrails` | `True` | Run guardrails on input |
| `output_guardrails` | `True` | Run guardrails on output |
| `judge_enabled` | `True` | Enable judge evaluation |
| `pace_enabled` | `True` | Let PACE control judge behavior |
| `block_on_review` | `False` | Block when judge returns REVIEW (vs. just logging) |
| `fallback_response` | `"Service temporarily unavailable..."` | Response when circuit breaker is open |

### Choosing `block_on_review`

- **`False` (default)** — REVIEW verdicts are logged but the response is delivered. Appropriate for most deployments. Review flagged items asynchronously.
- **`True`** — REVIEW verdicts block the response until a human reviews it. Appropriate for HIGH/CRITICAL risk tiers where any uncertainty should halt delivery.

## Callbacks

Register callbacks for blocked and escalated requests:

```python
def on_block(result: PipelineResult):
    """Called when any layer blocks a request."""
    metrics.increment("airs.blocked", tags={
        "layer": result.blocked_by.value,
        "pace_state": result.pace_state.value,
    })

def on_escalate(result: PipelineResult):
    """Called when the judge escalates or returns REVIEW."""
    send_to_review_queue(result)
    if result.judge_result.verdict == "escalate":
        alert_security_team(result)

pipeline = SecurityPipeline(
    on_block=on_block,
    on_escalate=on_escalate,
)
```

## PACE Integration

When `pace_enabled=True`, the PACE state controls:

- **Judge sampling rate** — Primary samples 5%, Alternate evaluates 100%
- **Human approval** — Contingency and Emergency require human approval for all outputs
- **Automatic escalation** — Judge `ESCALATE` verdicts trigger PACE escalation

```python
# Pipeline automatically escalates PACE on judge escalation:
# 1. Judge returns ESCALATE
# 2. Pipeline calls pace.escalate()
# 3. PACE moves Primary → Alternate
# 4. All subsequent requests get 100% judge evaluation
```

## Minimal Pipeline

For the simplest possible setup (Fast Lane):

```python
pipeline = SecurityPipeline(
    guardrails=GuardrailChain([RegexGuardrail()]),
    config=PipelineConfig(
        judge_enabled=False,  # No judge needed for LOW risk
        pace_enabled=False,   # No PACE degradation
    ),
)
```

This gives you:

- Prompt injection detection on input
- PII detection on output
- Circuit breaker monitoring
- No judge latency, no external dependencies
