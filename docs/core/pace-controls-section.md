# Control Layer Resilience: Internal PACE

*This section defines what happens when each control layer degrades. Every control has its own PACE plan (vertical axis) in addition to the architecture-level PACE across layers (horizontal axis). See the [PACE Resilience Methodology](../PACE-RESILIENCE.md) for the full model.*

> *This document uses the simplified three-tier system (Tier 1/2/3). See [Risk Tiers - Simplified Tier Mapping](risk-tiers.md#simplified-tier-mapping) for the mapping to LOW/MEDIUM/HIGH/CRITICAL.*

## Design Principle

Every control layer will eventually fail. The question is not *whether* but *how*. Before deploying any AI system, the architect must define the fail posture for each control at the assigned risk tier. This is a mandatory design input, not an operational afterthought.

![Fail Posture Decision Tree](../images/pace-fail-posture-decision.svg)

## Guardrails - Internal PACE

Guardrails are the Primary layer: deterministic, fast, always-on. When they degrade, the system must decide instantly whether to continue serving traffic (fail-open) or stop (fail-closed). The tier determines the answer.

| PACE | Condition | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|---|
| **P** - Normal | Engine running, all filters active | Standard filters: topic, length, PII | Full suite: content filters, schema validation, injection detection, hallucination indicators | Hardened multi-layer: regulatory constraint enforcement, action-level permissions, schema-strict validation. No bypass path. |
| **A** - Degraded | Engine slow, partial filter failure, rule update pending | Pass traffic. Log which filters are degraded. Flag for next business day review. | Fall back to stricter, simpler rule set. Over-block rather than under-block. Alert on-call. | Fall back to stricter rule set. Alert on-call immediately. Increase Judge evaluation to 100% if not already. |
| **C** - Down | Engine unresponsive or returning errors | **Fail-open.** Pass traffic. Log all requests. Rely on Judge and/or human review. | **Fail-closed.** Hold all AI outputs for Judge evaluation + human review. If Judge also degraded, route to non-AI fallback. | **Fail-closed.** Block all AI traffic immediately. Route to non-AI fallback path. Incident response initiated. |
| **E** - Compromised | Evidence of guardrail tampering or adversarial bypass at infrastructure level | Disable AI feature. Alert team. | Route to non-AI fallback. Incident response. Preserve guardrail configuration for forensic analysis. | Full stop on AI operations. Non-AI fallback path active. Forensic evidence preserved. Stakeholders and regulators notified. |

### Guardrail Transition Triggers

| Transition | Recommended Triggers |
|---|---|
| P → A | Guardrail response latency >2x baseline for 5 min; any filter returning default/error responses; rule update deployed but not validated |
| A → C | Guardrail engine health check failing; >50% of filter categories non-functional; engine unresponsive for >30s |
| C → E | Evidence of configuration tampering; known vulnerability actively exploited; guardrail logs show signs of adversarial manipulation |
| Recovery: C/E → P | Engine restored, all filters validated with test suite, monitoring confirms normal operation for >15 min (Tier 1) / >1 hour (Tier 2/3) |

## Model-as-Judge - Internal PACE

The Judge is the Alternate layer: probabilistic, asynchronous, catches what guardrails miss. Its failure modes are different from guardrails - it can be slow, wrong, or manipulated - and the fallback response differs by tier.

| PACE | Condition | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|---|
| **P** - Normal | Judge evaluating outputs, scores within calibration range | Sample 10–20% of outputs. Log scores. | Evaluate 100% of outputs async. Auto-hold outputs below confidence threshold. | Evaluate 100% of outputs AND actions. Dual-model evaluation. Pre- and post-action verification for agents. |
| **A** - Degraded | Judge latency >3x baseline, or partial model errors, or score distribution drifting | Reduce sampling rate. Log coverage gap. Review gap at next business day. | Switch to priority-only evaluation: flag high-risk outputs first (customer-facing, financial, PII-containing). Accept evaluation gap on low-risk outputs. Alert on-call. | Queue all outputs. Accept increased latency rather than skipping evaluation. Alert on-call. If agent, constrain to read-only until Judge performance restored. |
| **C** - Down | Judge returning errors, nonsensical scores, or completely unresponsive | Suspend Judge. Guardrails-only operation. Increase human sampling of outputs if practical. | All outputs held for human review until Judge restored. If human review queue exceeds capacity, throttle AI throughput to match. | All AI traffic paused. Human-only operation for any in-flight work. No new AI requests accepted. |
| **E** - Compromised | Evidence of Judge model poisoning, adversarial manipulation of evaluation criteria, or score manipulation | Disable Judge. Guardrails only. Alert team. Investigate before restoring. | Activate circuit breaker. Route to non-AI fallback. Incident response. Do not trust any recent Judge scores - review outputs that passed since potential compromise. | Full stop. Forensic analysis of Judge model, evaluation prompts, and score history. All outputs evaluated by compromised Judge must be re-reviewed by humans. Regulators notified. |

### Judge Transition Triggers

| Transition | Recommended Triggers |
|---|---|
| P → A | Judge latency >3x baseline for 5 min; error rate >5% of evaluations; score distribution shifts >2 standard deviations from calibration baseline |
| A → C | Judge health check failing; >50% of evaluation requests returning errors; complete unresponsiveness for >60s |
| C → E | Anomalous score patterns (e.g., all outputs scoring identically); evidence of prompt injection in evaluation chain; Judge model integrity check fails |
| Recovery: C/E → P | Judge model reloaded from known-good checkpoint, validated against test suite, calibration confirmed against baseline, monitoring confirms normal operation for >1 hour |

## Human Oversight - Internal PACE

Human Oversight is the Contingency layer: slow, expensive, but brings judgment that automated systems lack. Its failure modes are organisational - staffing gaps, queue overflow, fatigue - not technical.

| PACE | Condition | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|---|
| **P** - Normal | Review queue staffed, items processed within SLA | Async review of flagged items. Next business day acceptable. | Dedicated reviewers with domain knowledge. SLA-bound response times. | Domain experts with regulatory knowledge. Dual approval for irreversible actions. SLA measured in minutes, not hours. |
| **A** - Degraded | Primary reviewer unavailable (leave, illness, turnover) | Flagged items queue until reviewer available. Acceptable backlog: 1–2 business days. | Escalate to secondary reviewer pool. Extend SLA by defined buffer (e.g., 2x) but don't skip review. | On-call escalation to alternate domain expert. No action proceeds without approval. If no alternate available within SLA, escalate to C. |
| **C** - Overloaded | Review queue exceeds capacity - flood of flags from Judge or guardrail changes | Throttle AI throughput to match review capacity. Extend queue SLA. | Tighten Judge thresholds to reduce flag volume (fewer borderline cases flagged). Activate additional reviewers from trained pool. If still overloaded, throttle AI throughput. | Constrain agent scope to reduce action volume. Activate crisis staffing from pre-identified pool. If still overloaded, move to Supervised phase (agent proposes, human approves every action). |
| **E** - Unavailable | No reviewers available (incident, holiday gap, mass resignation) | Disable AI features requiring review. Guardrails and Judge operate autonomously for remaining features. | Switch to automated-only: Judge must auto-approve/reject with conservative thresholds. Accept higher false-positive rate (more blocks) in exchange for no human review. Flag for urgent staffing resolution. | **Suspend all AI operations requiring human approval.** No exceptions. In-flight agent actions completed or rolled back per transaction resolution matrix. Full stop until oversight restored. |

### Human Oversight Transition Triggers

| Transition | Recommended Triggers |
|---|---|
| P → A | Primary reviewer unavailable; queue wait time >1.5x SLA |
| A → C | Queue size >3x normal; wait time >2x SLA; multiple reviewers unavailable simultaneously |
| C → E | Zero qualified reviewers available; queue wait time >5x SLA with no resolution timeline |
| Recovery: E → P | Reviewers available and confirmed; queue backlog cleared or triaged; SLA performance confirmed for >4 hours |

> **See also:** [Humans in the Business Process](../extensions/technical/humans-in-the-business-process.md) describes how existing business process checkpoints can serve as an Alternate or Contingency layer when dedicated HITL reviewers degrade - without adding new reviewers or changing the automated decision.

## Cross-Layer PACE: Architecture-Level Resilience

When individual layer PACE has been exhausted - the layer is at its Emergency state - the architecture-level PACE activates:

| Condition | Architecture Response |
|---|---|
| Guardrails at E (compromised) | Judge becomes sole automated defence. Human oversight scope expanded. Evaluate whether to activate circuit breaker based on Judge coverage and confidence. |
| Judge at E (compromised) | Guardrails continue blocking known-bad. Human oversight absorbs all quality assurance. Reduce AI throughput to match human capacity. |
| Human Oversight at E (unavailable) | Guardrails and Judge operate without human backstop. At Tier 2+, tighten all automated thresholds. At Tier 3, activate circuit breaker - automated-only operation is not acceptable for regulated decisions. |
| Two or more layers at E simultaneously | **Circuit breaker activates immediately, regardless of tier.** Route to non-AI fallback. This is a systemic failure requiring incident response. |
| Circuit breaker activated | Non-AI fallback path serves traffic. All AI components isolated. Incident response team assembled. Recovery requires layer-by-layer restoration with validation at each step. |

## The Non-AI Fallback Path

Every system at Tier 2 or above must have a documented, tested, and maintained non-AI fallback path. This is the last line of defence and must not share dependencies with the AI system.

| Aspect | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| **What it is** | The manual process the AI replaced | Rule-based system or templated responses | Staffed parallel process with trained operators |
| **Who maintains it** | Same team that runs the AI | Designated owner with quarterly review | Dedicated operational resilience function |
| **Dependencies** | Must not depend on the AI model or guardrail engine | Must not depend on any AI infrastructure component | Must not share any infrastructure with the AI system |
| **Testing** | Annually: confirm it still works | Quarterly: run production-equivalent traffic through it | Monthly: operate in parallel for a defined period |
| **Activation** | Manual (feature flag, deployment rollback) | Automated (circuit breaker with health checks) | Automated (circuit breaker) with manual confirmation within defined window |
| **Capacity** | Best effort | Must handle 100% of AI traffic at degraded quality | Must handle critical subset at production quality |

