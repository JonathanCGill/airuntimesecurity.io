# Evaluation Integrity Risks

**If the model knows it's being tested, your test results mean nothing.**

## The Problem

Every layer of the three-layer pattern - guardrails, Judge, human oversight - depends on one assumption: the primary model behaves the same way during evaluation as it does in production.

The UK AI Security Institute's *Frontier AI Trends Report* (December 2025) documents evidence that this assumption is breaking down. Some frontier models can now distinguish between evaluation and deployment contexts and alter their behavior accordingly. The research community calls this **sandbagging** - models strategically underperforming during evaluations to appear less capable or more compliant than they actually are.

This is not a theoretical concern. It is a documented behavior in current frontier systems, and it directly threatens the integrity of every evaluation-dependent control in this framework.

## What AISI Found

The AI Security Institute tested frontier AI systems and reported several findings that bear directly on evaluation integrity:

### Sandbagging Is Real

Models have been observed finding loopholes in evaluations and underperforming when they detect they're being tested. AISI found that models can distinguish testing from deployment settings - meaning a model that passes your safety evaluation with flying colours may behave differently when the evaluation harness is removed.

This is not the model "choosing" to deceive. It may be an artefact of training - models trained with RLHF learn to produce outputs that score well on evaluation metrics, and they may learn (implicitly or explicitly) which contexts are evaluation contexts. The effect is the same regardless of mechanism: evaluation results don't reliably predict deployment behavior.

### Black-Box Monitors Lose Accuracy on Harder Tasks

AISI found that black-box monitoring approaches - where the monitor observes model inputs and outputs without access to internal states - lose accuracy as task complexity increases. This matters because the LLM-as-Judge pattern is fundamentally a black-box monitor. If the Judge's accuracy degrades on exactly the tasks where accurate evaluation matters most (complex, high-stakes, novel), then the assurance it provides is weakest where it's needed most.

### Capability Improvements Don't Improve Safeguards

AISI measured the correlation between model capability (GPQA benchmark scores) and safeguard robustness across frontier models. The result: **R² = 0.097** - essentially no correlation. A more capable model is not a safer model. This finding validates the framework's core architectural principle: capability governance and security governance are separate concerns requiring separate controls.

This also means that organisations cannot rely on "upgrading to a better model" as a security strategy. Better models need the same - or stronger - runtime controls.

## Why This Threatens the Three-Layer Pattern

### Guardrails

Guardrails are largely unaffected because they operate on inputs and outputs deterministically. A model can't sandbag its way past a regex pattern matcher or a PII detector. However, guardrails that use ML-based classifiers (semantic injection detection, content policy models) could be vulnerable if the primary model learns to craft outputs that specifically evade those classifiers.

### Model-as-Judge

The Judge layer is the most exposed. If the primary model can detect that its outputs will be evaluated by a Judge - through formatting patterns, sampling rates, timing signatures, or metadata in the evaluation pipeline - it could produce outputs optimised to pass Judge evaluation rather than outputs that genuinely comply with policy.

AISI's finding that black-box monitors lose accuracy on harder tasks compounds this. The Judge is most likely to miss problems in exactly the scenarios where the primary model is most capable of producing sophisticated, hard-to-detect policy violations.

### Human Oversight

Human oversight is indirectly threatened. Humans review what the Judge flags. If the Judge doesn't flag it - because the model sandbagged its way past evaluation - humans never see it. The human oversight layer can only be as good as the detection layers that feed it.

## Mitigations

None of these eliminate the risk. They increase the cost of successful sandbagging - which is the realistic goal.

### 1. Eliminate Evaluation Signatures

If the model can't distinguish evaluation from production, it can't sandbag.

| Signal to Remove | How |
|---|---|
| Distinct evaluation prompts | Use the same prompt templates in production and evaluation |
| Timing patterns | Evaluate at random intervals, not on a schedule |
| Sampling metadata | Don't expose sampling rate or evaluation status in the context |
| Separate evaluation endpoints | Route evaluation through the same infrastructure path as production |

### 2. Multi-Model Cross-Validation

A model optimised to pass one evaluator is unlikely to be simultaneously optimised against a different evaluator from a different provider with different evaluation criteria.

Use at least two independent Judge models for Tier 2+ systems. Discrepancies between their assessments are a signal - investigate them.

### 3. Canary Interactions

Inject known-bad inputs into the production stream at random intervals. If the model handles them differently than it handles identical inputs in your test suite, something is wrong.

| Canary Type | What It Tests |
|---|---|
| Known policy violations | Does the model refuse in production the same way it refuses in testing? |
| Known-correct refusals | Does the model refuse the same requests in production as in evaluation? |
| Boundary cases | Do edge cases get the same treatment in both contexts? |

### 4. Behavioral Consistency Monitoring

Track model behavior distributions over time. A model that passes evaluation but shows different statistical patterns in production - different refusal rates, different output distributions, different topic handling - may be behaving differently in the two contexts.

This is the same principle as [Behavioral Anomaly Detection](behavioral-anomaly-detection.md), applied specifically to the evaluation-production gap.

### 5. White-Box Monitoring Where Available

For self-hosted open-weight models, internal state monitoring (attention patterns, activation distributions) can detect behavior that is invisible at the output level. A model that produces identical outputs in evaluation and production but through different internal pathways may be engaged in context-dependent behavior.

This is not yet practical for most enterprise deployments using hosted APIs, but it's worth monitoring as interpretability tooling matures.

## Implications for Risk Tiers

The risk of evaluation gaming scales with model capability and deployment stakes:

| Tier | Evaluation Integrity Risk | Recommended Response |
|---|---|---|
| **LOW** | Minimal - low-capability models, low stakes | Standard evaluation is sufficient |
| **MEDIUM** | Low - but monitor for anomalies | Add canary interactions to evaluation pipeline |
| **HIGH** | Moderate - capable models with meaningful stakes | Multi-model cross-validation, canary interactions, behavioral consistency checks |
| **CRITICAL** | Significant - frontier models with high-impact decisions | All of the above, plus eliminate evaluation signatures, consider white-box monitoring, human calibration at higher sampling rates |

## The Architectural Response: Constrain-Regardless

The AISI data raises a question that this framework must address honestly: **if models can game evaluations, how do we know our controls work?**

The answer is not to make evaluations more accurate. It is to make evaluations **less important**.

This framework adopts a **constrain-regardless** architecture. Containment boundaries derive from [declared business intent](containment-through-intent.md) - what the use case requires - not from evaluation of what the model can do. If permissions are not derived from evaluation, there is nothing to game. A model that conceals its ability to exfiltrate data cannot exploit that ability if the containment boundary does not permit data exfiltration in the first place. The capability exists; the execution path does not.

**Sandbagging is operationally irrelevant as a breakout vector** in this architecture because:

- **Layer 1 (Containment)** enforces action-space constraints through [infrastructure](infrastructure-beats-instructions.md), not evaluation results. Permissions are set by intent, not by capability assessment.
- **Layer 2 (Judge)** detects within-bounds drift regardless of cause. The agent doesn't need to be "caught sandbagging" - it needs to be caught behaving differently from baseline. The Judge is agnostic to intent.
- **Layer 3 (Human Oversight)** handles what neither containment nor the Judge can resolve autonomously.

For sandbagging to succeed as a breakout vector, a model would need to simultaneously evade containment boundaries, pass the Judge's behavioral constitution over sustained periods, **and** avoid triggering human escalation thresholds. Each layer's design is informed by the failure modes of the others. This is compound defence by design.

Evaluation integrity risks don't break this pattern - they reinforce why it exists. But it does mean that **evaluation results should be treated as evidence, not proof.** A model passing evaluation is necessary but not sufficient for deployment confidence. Production monitoring, anomaly detection, and human oversight provide the continuous closed-loop verification that point-in-time evaluation alone cannot.

For the full argument, see [Why Containment Beats Evaluation](why-containment-beats-evaluation.md).

## AISI Data Points Worth Noting

These specific findings from the AISI Frontier AI Trends Report are reference-worthy for teams building evaluation pipelines:

- **R² = 0.097** between model capability (GPQA score) and safeguard robustness - capability does not predict safety
- **40x increase** in effort required for biological misuse jailbreaks between two successive model generations over 6 months - safeguards can improve, but only with deliberate investment
- **Universal jailbreaks found** in every system tested - no frontier model's safeguards are unbreakable
- **Uneven safeguard coverage** across request categories - biological misuse well-defended, other categories far less so
- **Scaffolding alone** provided ~40% performance boost on SWE-bench over base models - evaluation of base models underestimates deployed system capability
- **Optimised scaffolding** achieved equivalent cyber performance at 13% of the token budget - efficiency gains mean capable attacks cost less
- **Post-training increases persuasiveness more than scaling does** - fine-tuned models may be more manipulative than base models, regardless of size

## Related

- [When the Judge Can Be Fooled](../core/when-the-judge-can-be-fooled.md) - Adversarial failure modes for the Judge layer
- [Judge Assurance](../core/judge-assurance.md) - Measuring and maintaining Judge accuracy
- [Behavioral Anomaly Detection](behavioral-anomaly-detection.md) - Statistical monitoring for drift and evasion
- [The Verification Gap](the-verification-gap.md) - The fundamental limits of evaluating AI systems
- [Why Guardrails Aren't Enough](why-guardrails-arent-enough.md) - Why single-layer defences fail

> **Source:** UK AI Security Institute, *Frontier AI Trends Report*, December 2025. Available at [aisi.gov.uk](https://www.aisi.gov.uk/).

