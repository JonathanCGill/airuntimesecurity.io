# Beyond Security: Where This Architecture Transfers

*This framework solves AI runtime security. Its architecture isn't limited to security.*

## The Observation

This framework was built to answer a security question: how do you control AI systems that are non-deterministic, operate at scale, and can fail in ways no test suite anticipated?

The answer it arrived at was structural:

- **Layer controls independently** - rules-based detection, ML-based evaluation, human judgment - so no single failure is catastrophic.
- **Tier by impact** - decision authority, reversibility, sensitivity, audience, scale, regulation - so controls are proportionate to what's at stake.
- **Quantify residual risk** - measure what each layer catches, compound the misses, compare to appetite.
- **Define fail posture before deployment** - Primary, Alternate, Contingency, Emergency - so degradation is planned, not improvised.
- **Scale controls to risk** - more critical systems get more layers, more coverage, more formal governance.
- **Test continuously** - controls degrade. Verify they still work.

None of these principles mention security. They describe how to build reliable, layered, proportional controls for any risk domain where the thing you're controlling is uncertain and the consequences of failure vary.

## What Changes, What Doesn't

The architecture has two parts: the structural patterns and the domain content. Only the content is security-specific.

| Structural Pattern | Security Content | The Pattern Itself |
|---|---|---|
| Three independent layers | Guardrails, Judge, Human | Detection → Evaluation → Judgment |
| Risk tiering | PII, injection, policy compliance | Impact dimensions → control depth |
| Quantitative risk model | P(injection miss), P(PII leak) | P(miss₁) × P(miss₂) × P(miss₃) = residual |
| PACE resilience | Guardrail bypass → Judge primary → circuit breaker | Primary fails → alternate activates → contingency holds → emergency stops |
| Graduated complexity | LOW: guardrails only → CRITICAL: all layers at 100% | Lower risk → fewer controls; higher risk → more controls |
| Phased implementation | Classify → guardrails → judge → human → PACE → test | Foundation → controls → resilience → verification |

Swap the content. Keep the architecture. The framework still works.

## How It Reads for Other AI Risks

This section doesn't prescribe controls for drift, fairness, or explainability. It shows what the structural patterns look like when you point them at a different problem. The reader does the thinking.

### Model Drift

The problem: a model's accuracy degrades over time as the world changes. The inputs it was trained on no longer represent the inputs it receives.

**Three layers, applied:**

| Layer | Security Version | Drift Version |
|---|---|---|
| Layer 1 (Detection) | Pattern-matching guardrails catch known-bad inputs | Statistical monitors catch distribution shift beyond threshold |
| Layer 2 (Evaluation) | Model-as-Judge evaluates outputs for policy compliance | Validation pipeline evaluates predictions against labelled holdout set |
| Layer 3 (Judgment) | Human reviews escalated cases | Domain expert reviews flagged performance degradation and decides: retrain, adjust, or accept |

**PACE, applied:**

- **Primary:** Online drift detection + periodic retraining on fresh data.
- **Alternate:** Freeze model, widen uncertainty bounds, increase human review.
- **Contingency:** Revert to last validated model version.
- **Emergency:** Route to non-AI decision path.

**Tiering, applied:** An internal search tool that drifts slightly is an inconvenience. A clinical decision support model that drifts silently is dangerous. Same architecture. Different tier. Different control depth.

### Fairness

The problem: a model produces outcomes that systematically disadvantage a protected group - sometimes because the training data encoded historical bias, sometimes because a proxy variable correlates with protected attributes.

**Three layers, applied:**

| Layer | Security Version | Fairness Version |
|---|---|---|
| Layer 1 (Detection) | Guardrails block prohibited inputs | Disparity monitors flag when outcome rates diverge beyond threshold across protected groups |
| Layer 2 (Evaluation) | Judge evaluates output quality and compliance | Bias measurement pipeline evaluates model decisions against fairness metrics on sampled cohorts |
| Layer 3 (Judgment) | Human reviews escalated findings | Equity review board assesses whether statistical disparity reflects genuine bias or legitimate signal |

**PACE, applied:**

- **Primary:** Continuous disparity monitoring with automated alerts.
- **Alternate:** Freeze model retraining, flag all decisions in affected cohort for manual review.
- **Contingency:** Disable model for affected decision category, route to rule-based fallback.
- **Emergency:** Halt all automated decisions, revert to fully human process.

**Tiering, applied:** A content recommendation model with slight demographic skew is low-tier. An automated hiring screen with disparate impact on a protected class is critical-tier. The architecture scales identically.

### Explainability

The problem: a model produces a decision but cannot adequately explain why. In regulated domains, "the model said so" is not sufficient. In high-stakes domains, humans need to understand the reasoning to trust it - or override it.

**Three layers, applied:**

| Layer | Security Version | Explainability Version |
|---|---|---|
| Layer 1 (Detection) | Guardrails validate input/output format and content | Explanation validators check that every decision includes a structured rationale meeting minimum criteria |
| Layer 2 (Evaluation) | Judge evaluates output against policy | Explanation quality scorer evaluates whether the rationale is consistent, complete, and faithful to the model's actual decision factors |
| Layer 3 (Judgment) | Human reviews escalated cases | Domain expert assesses whether the explanation is genuinely interpretable - not just present, but useful |

**PACE, applied:**

- **Primary:** Full explanation generation with automated quality checks.
- **Alternate:** Simplified explanation from pre-approved rationale templates.
- **Contingency:** Flag decision as "explanation unavailable," route to manual justification.
- **Emergency:** Halt autonomous decisions, require human-authored rationale for each action.

**Tiering, applied:** An internal summarisation tool that doesn't explain its choices is fine. An autonomous loan denial that can't articulate its reasoning violates regulatory requirements. Same architecture. Different tier. Different obligation.

### Reliability

The problem: a model produces outputs that are inconsistent, contradictory, or confidently wrong - hallucination, confabulation, or simply unreliable performance under edge conditions.

**Three layers, applied:**

| Layer | Security Version | Reliability Version |
|---|---|---|
| Layer 1 (Detection) | Guardrails catch known-bad patterns | Consistency checks flag outputs that contradict source material, prior outputs, or known facts |
| Layer 2 (Evaluation) | Judge evaluates policy compliance | Grounding evaluator assesses whether outputs are supported by retrieved evidence and internally coherent |
| Layer 3 (Judgment) | Human reviews escalated findings | Domain expert reviews flagged outputs for factual accuracy and coherence |

**PACE, applied:**

- **Primary:** Real-time consistency validation against source documents.
- **Alternate:** Reduce model autonomy - present outputs as drafts requiring human confirmation.
- **Contingency:** Switch to retrieval-only mode (return source documents, don't generate).
- **Emergency:** Disable generative capability entirely.

## The Quantitative Model Transfers Directly

The [risk assessment methodology](../core/risk-assessment.md) calculates residual risk as the product of independent miss rates across layers. This calculation doesn't care what you're detecting.

For security: *What is the probability that a prompt injection passes the guardrail, is missed by the Judge, and is not caught by the human reviewer?*

For drift: *What is the probability that an accuracy degradation exceeds the threshold, is missed by the statistical monitor, is not caught by the validation pipeline, and is not flagged by the domain expert?*

For fairness: *What is the probability that a disparate impact emerges, is missed by the disparity monitor, is not caught by the bias measurement pipeline, and is not identified by the equity review board?*

Same math. Different inputs. The residual risk calculation, the severity weighting, the recalibration cycle - all of it transfers without modification.

## What This Framework Does Not Do

This framework does not provide domain-specific controls for drift, fairness, explainability, or reliability. It does not tell you which statistical test detects distribution shift, which fairness metric to use, or how to generate faithful explanations. Those are domain problems with mature, domain-specific tooling.

What it provides is the **control architecture** - the structural reasoning about how to layer defences, how to tier by impact, how to quantify what gets through, and how to degrade gracefully when controls fail. That architecture is domain-agnostic because it describes *how to control*, not *what to control*.

If you are building controls for AI risks beyond security, the framework offers a structural starting point:

1. **Classify the system** using the same [impact dimensions](../core/risk-tiers.md) - they are not security-specific.
2. **Layer your controls** so they fail independently - use different mechanisms at each layer.
3. **Quantify your residual risk** using the same [compounding model](../core/risk-assessment.md) - measure, don't assume.
4. **Define your fail posture** using the same [PACE methodology](../PACE-RESILIENCE.md) - decide before deployment what happens when controls degrade.
5. **Scale to the risk** - not every AI system needs maximum controls for every risk dimension.

The security content in this framework is one instantiation of the architecture. Drift, fairness, explainability, and reliability are others. The architecture holds.

## The Bottom Line

This framework was built for AI security. Its architecture - layered independence, proportional tiering, quantitative compounding, defined fail posture - was not built for any single risk domain. It was built for the structural problem of controlling systems that are uncertain, non-deterministic, and consequential.

Security is where we started. It is not where the architecture ends.

