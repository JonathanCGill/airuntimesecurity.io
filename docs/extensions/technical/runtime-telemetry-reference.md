---
description: "End-to-end runtime telemetry reference: one transaction through every control layer with JSON events, thresholds, and evidence artefacts for a HIGH-tier AI system."
---

# Runtime Telemetry Reference

**One transaction, end-to-end. Every control layer. Every log event. Every threshold.**

> *Part of [Technical Extensions](README.md) · [AI Runtime Security](../../README.md)*

## Purpose

This document shows exactly what happens when a single request passes through the runtime control stack. It follows one transaction from user input to final response, showing the JSON event emitted at each layer, the thresholds that trigger action, and the evidence artefact each event produces.

**Scenario:** A customer asks a financial services chatbot about investment products. The system is classified HIGH tier (customer-facing, financial data, 500K transactions/year).

**Architecture:** AWS Bedrock with Claude, guardrails via Bedrock Guardrails, Judge via async evaluation, human oversight via review queue.

## The Transaction

**User input:** `"What's the best investment for my retirement savings of $450,000?"`

This input triggers five events across the control stack. Each event is logged, evaluated, and produces audit evidence.

### Event 1: Request Received (LOG-01)

The platform logs the raw request before any processing.

```json
{
  "event_type": "model_request",
  "request_id": "req-7f3a-4b2c-9d1e",
  "timestamp": "2026-02-22T14:23:01.456Z",
  "user_identity": "user:customer-8842@portal",
  "service_identity": "svc:wealth-advisor-v3",
  "session_id": "session:ws-29471",
  "model_id": "bedrock:claude-3-sonnet-v2",
  "system_prompt_hash": "sha256:e4a1c3f8...",
  "input_text": "What's the best investment for my retirement savings of $450,000?",
  "input_tokens": 18,
  "risk_tier": "HIGH",
  "metadata": {
    "temperature": 0.3,
    "max_tokens": 1024,
    "channel": "web_portal",
    "customer_segment": "retail"
  }
}
```

**Evidence produced:** Request audit trail (Art. 12 record-keeping).

### Event 2: Guardrail Evaluation (LOG-02)

Input guardrails run before the request reaches the model. Output guardrails run after.

**Input guardrail result:**

```json
{
  "event_type": "guardrail_decision",
  "request_id": "req-7f3a-4b2c-9d1e",
  "timestamp": "2026-02-22T14:23:01.478Z",
  "guardrail_id": "grd:bedrock-content-filter-v2",
  "guardrail_version": "2.1.4",
  "stage": "input",
  "checks": [
    {
      "check_type": "prompt_injection",
      "decision": "pass",
      "confidence": 0.12,
      "latency_ms": 8
    },
    {
      "check_type": "topic_restriction",
      "decision": "pass",
      "confidence": 0.04,
      "latency_ms": 3
    },
    {
      "check_type": "pii_detection",
      "decision": "flag",
      "confidence": 0.91,
      "detail": "Financial amount detected: $450,000",
      "action": "log_and_proceed",
      "latency_ms": 6
    }
  ],
  "overall_decision": "pass",
  "total_latency_ms": 22
}
```

**Output guardrail result** (after model responds):

```json
{
  "event_type": "guardrail_decision",
  "request_id": "req-7f3a-4b2c-9d1e",
  "timestamp": "2026-02-22T14:23:03.892Z",
  "guardrail_id": "grd:bedrock-content-filter-v2",
  "guardrail_version": "2.1.4",
  "stage": "output",
  "checks": [
    {
      "check_type": "financial_advice",
      "decision": "flag",
      "confidence": 0.78,
      "detail": "Response discusses investment products with specific amounts",
      "action": "add_disclaimer",
      "latency_ms": 12
    },
    {
      "check_type": "pii_leakage",
      "decision": "pass",
      "confidence": 0.03,
      "latency_ms": 5
    },
    {
      "check_type": "hallucination_pattern",
      "decision": "pass",
      "confidence": 0.15,
      "latency_ms": 9
    }
  ],
  "overall_decision": "pass_modified",
  "modification": "Regulatory disclaimer appended",
  "total_latency_ms": 31
}
```

**Thresholds that matter:**

| Check | Block Threshold | Flag Threshold | This Request |
|---|---|---|---|
| Prompt injection | confidence > 0.85 | confidence > 0.60 | 0.12 - pass |
| Financial advice | confidence > 0.95 | confidence > 0.70 | 0.78 - flag, add disclaimer |
| PII leakage | confidence > 0.80 | confidence > 0.50 | 0.03 - pass |

**Evidence produced:** Guardrail effectiveness measurement (Art. 9 risk mitigation), content modification audit trail.

### Event 3: Model Response (LOG-01 completion)

```json
{
  "event_type": "model_response",
  "request_id": "req-7f3a-4b2c-9d1e",
  "timestamp": "2026-02-22T14:23:03.861Z",
  "output_text": "For retirement savings of that size, there are several approaches worth discussing with a qualified financial adviser. Diversified index funds, target-date retirement funds, and balanced portfolios are common strategies. The right choice depends on your timeline to retirement, risk tolerance, and other income sources. I'd recommend speaking with a certified financial planner who can assess your complete financial picture.\n\n*This is general information, not personalised financial advice. Please consult a licensed financial adviser before making investment decisions.*",
  "output_tokens": 87,
  "latency_ms": 2383,
  "guardrail_actions": ["disclaimer_appended"],
  "finish_reason": "end_turn"
}
```

**Evidence produced:** Full response audit trail with model attribution (Art. 12 traceability).

### Event 4: Judge Evaluation (LOG-03)

The Judge evaluates the response asynchronously. For HIGH tier systems, 100% of responses containing flagged content are evaluated, plus 20% random sample.

**This request is evaluated because:** Output guardrail flagged financial advice content.

```json
{
  "event_type": "judge_evaluation",
  "request_id": "req-7f3a-4b2c-9d1e",
  "timestamp": "2026-02-22T14:23:06.244Z",
  "judge_model_id": "bedrock:claude-3-haiku-v2",
  "evaluation_criteria": "financial-services-v3",
  "evaluation_criteria_version": "3.2.1",
  "trigger": "guardrail_flag:financial_advice",
  "scores": {
    "policy_compliance": 0.94,
    "factual_accuracy": 0.91,
    "appropriate_disclaimers": 1.0,
    "referral_to_professional": 1.0,
    "no_specific_recommendations": 0.88
  },
  "overall_score": 0.93,
  "verdict": "acceptable",
  "reasoning": "Response appropriately redirects to professional advice. Does not recommend specific products or allocations. Disclaimer present. Minor: mentions 'index funds' and 'target-date funds' by category which could be interpreted as directional guidance.",
  "conduct_risk": "LOW",
  "recommended_action": "none",
  "latency_ms": 1380
}
```

**Thresholds that matter:**

| Verdict | Score Range | Action |
|---|---|---|
| Acceptable | overall_score ≥ 0.85 | Log only |
| Review | 0.70 ≤ overall_score < 0.85 | Route to daily review queue |
| Escalate | overall_score < 0.70 | Route to immediate review queue |
| Escalate | conduct_risk = "HIGH" | Alert compliance team immediately |

**Evidence produced:** Independent evaluation record with reasoning (Art. 14 human oversight support, Art. 15 accuracy measurement).

### Event 5: Human Oversight Routing Decision

Based on the Judge evaluation, the system decides whether human review is needed.

```json
{
  "event_type": "oversight_decision",
  "request_id": "req-7f3a-4b2c-9d1e",
  "timestamp": "2026-02-22T14:23:06.248Z",
  "judge_verdict": "acceptable",
  "judge_score": 0.93,
  "human_review_required": false,
  "reason": "Score above review threshold (0.85). No conduct risk flags.",
  "sampling_selected": false,
  "sampling_rate": 0.20
}
```

**If the Judge had scored this below 0.70**, the event would be:

```json
{
  "event_type": "oversight_decision",
  "request_id": "req-7f3a-4b2c-9d1e",
  "timestamp": "2026-02-22T14:23:06.248Z",
  "judge_verdict": "escalate",
  "judge_score": 0.58,
  "human_review_required": true,
  "review_queue": "immediate",
  "escalation_target": "compliance_team",
  "sla_hours": 2,
  "reason": "Score below escalation threshold (0.70). Possible inappropriate financial recommendation."
}
```

**Evidence produced:** Oversight decision audit trail (Art. 14 human oversight), escalation records.

## Detection Queries for This Scenario

These queries run in your SIEM against the events above.

### Detect repeated financial advice flags (Splunk)

```spl
index=ai_security event_type="guardrail_decision" stage="output"
  checks{}.check_type="financial_advice" checks{}.decision="flag"
| stats count as flag_count by user_identity, session_id
| where flag_count > 3
| eval severity=case(flag_count > 10, "high", flag_count > 5, "medium", 1=1, "low")
```

**Threshold rationale:** >3 flags in one session suggests the user is probing for specific financial advice that guardrails are catching. Investigate for social engineering.

### Detect Judge disagreement with guardrails (Sentinel)

```kql
AISecurity_CL
| where event_type_s == "guardrail_decision" and overall_decision_s == "pass"
| join kind=inner (
    AISecurity_CL
    | where event_type_s == "judge_evaluation" and overall_score_d < 0.70
  ) on request_id_s
| project TimeGenerated, request_id_s, user_identity_s, judge_score=overall_score_d
```

**What this detects:** Guardrails passed the request, but the Judge flagged it. This is a guardrail gap - the pattern the guardrail doesn't recognise. Feed these back into guardrail tuning.

### Detect escalation volume spike (Splunk)

```spl
index=ai_security event_type="oversight_decision" human_review_required="true"
| timechart span=1h count as escalations
| streamstats window=168 avg(escalations) as baseline, stdev(escalations) as stddev
| eval z_score=(escalations - baseline) / stddev
| where z_score > 3.0
```

**Threshold:** z-score > 3.0 (3 standard deviations above 7-day rolling baseline). Indicates either a model behavior change or an attack campaign.

## Evidence Artefacts Summary

Every transaction through the control stack produces evidence for five compliance requirements:

| Requirement | Evidence Artefact | Source Event | Retention |
|---|---|---|---|
| **Art. 9** Risk mitigation | Guardrail decision + Judge evaluation | LOG-02, LOG-03 | 1 year |
| **Art. 12** Record-keeping | Full request/response with correlation ID | LOG-01 | 90 days (full), 1 year (metadata) |
| **Art. 14** Human oversight | Oversight routing decision + review records | Event 5 + HITL log | 1 year |
| **Art. 15** Accuracy | Judge scores + validation metrics | LOG-03 | 1 year |
| **PACE** Resilience | Control layer health status | Platform telemetry | 1 year |

## Failure Scenario: What Changes When the Judge Goes Down

When the Judge layer becomes unavailable, PACE transitions from Primary to Alternate:

```json
{
  "event_type": "pace_transition",
  "timestamp": "2026-02-22T15:01:44.000Z",
  "service_identity": "svc:wealth-advisor-v3",
  "previous_state": "primary",
  "new_state": "alternate",
  "trigger": "judge_health_check_failed",
  "detail": "Judge model bedrock:claude-3-haiku-v2 returned 3 consecutive 503 errors",
  "actions_taken": [
    "judge_evaluation_suspended",
    "guardrail_thresholds_tightened",
    "human_sampling_rate_increased_to_1.0",
    "soc_alert_raised:severity_high"
  ],
  "risk_implication": "Guardrails only. No independent evaluation. All responses routed to human review.",
  "restoration_sla_minutes": 30
}
```

**Guardrail threshold changes during Alternate state:**

| Check | Primary Threshold | Alternate Threshold | Rationale |
|---|---|---|---|
| Financial advice | flag > 0.70 | block > 0.60 | Tighter without Judge backup |
| Prompt injection | block > 0.85 | block > 0.70 | Lower tolerance without verification |
| PII leakage | block > 0.80 | block > 0.60 | Conservative without second check |

This is the operational resilience evidence auditors look for: not just "we have controls" but "here's exactly what happens when they fail."

## Connecting to Existing Documentation

| Topic | Detailed Reference |
|---|---|
| Full field definitions for LOG-01 through LOG-10 | [Logging & Observability Controls](../../infrastructure/controls/logging-and-observability.md) |
| Complete detection rule library (8 rules, 3 SIEM platforms) | [SOC Content Pack](soc-content-pack.md) |
| Baseline establishment and z-score methodology | [Anomaly Detection Operations](anomaly-detection-ops.md) |
| Full worked example with Python code | [Customer Service AI Example](../examples/01-customer-service-ai.md) |
| PACE degradation methodology | [PACE Resilience](../../PACE-RESILIENCE.md) |
| Risk tier classification | [Risk Tiers](../../core/risk-tiers.md) |

