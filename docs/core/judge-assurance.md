---
description: "How to validate Model-as-Judge accuracy against human ground truth, detect Judge drift, and prevent evaluation collapse in AI safety systems."
---

# Judge Assurance

<!-- golden-thread-nav -->
!!! tip "Part of the Golden Thread (8 of 14)"
    Previous: [The Judge Detects, Not Decides](../insights/judge-detects-not-decides.md) · Next: [When the Judge Can Be Fooled](when-the-judge-can-be-fooled.md) · [See the full sequence](../reading-paths.md#the-golden-thread-guardrails-judges-and-why-they-work-together)
<!-- golden-thread-nav -->

> Who judges the judge?

## The Problem

The three-layer pattern depends on the Model-as-Judge to detect "unknown-bad" outputs that guardrails miss. The Judge may be a large LLM running asynchronously, a [distilled SLM](../extensions/technical/distill-judge-slm.md) running inline as a sidecar, or both in a tiered arrangement. Regardless of size, the Judge is itself a model. It hallucinates. It drifts. It can be manipulated.

If you deploy a Judge without evaluating its accuracy, you have added cost and latency without knowing whether you have added safety.

## What Can Go Wrong

| Failure Mode | Impact |
|-------------|--------|
| **False negatives** | Judge approves harmful outputs - the whole point of the Judge is defeated |
| **False positives** | Judge flags benign outputs - users lose trust, teams disable the Judge |
| **Judge drift** | Judge model is updated by provider, changing evaluation behavior without notice |
| **Judge manipulation** | Adversarial inputs crafted to pass the Judge while failing for humans |
| **Evaluation collapse** | Judge uses same reasoning patterns as the generator - shared blind spots |

The last one is the most insidious. If your generator is GPT-4 and your judge is also GPT-4, they may share the same failure modes. The judge won't catch what it can't see.

## Controls

### 1. Establish a Human-Labelled Ground Truth

Before you trust the judge, measure its accuracy against human judgment.

| Step | What |
|------|------|
| Sample | Randomly select N outputs per week (N depends on volume and risk tier) |
| Label | Have qualified humans evaluate the same outputs the Judge evaluated |
| Compare | Calculate agreement rate, precision, recall, F1 |
| Track | Plot these metrics over time |

**Minimum viable metrics:**

| Metric | What It Measures | Target (adjust per risk tier) |
|--------|-----------------|-------------------------------|
| **Agreement rate** | How often Judge and human agree | >90% for HIGH, >95% for CRITICAL |
| **False negative rate** | Judge missed something human caught | <5% for HIGH, <2% for CRITICAL |
| **False positive rate** | Judge flagged something human approved | <15% (higher tolerance - better to over-flag) |
| **Inter-rater reliability** | Consistency between human evaluators | Cohen's κ > 0.7 |

### 2. Use a Different Model for the Judge

Avoid shared blind spots. If your generator uses one model family, your judge should use a different one.

| Generator | Judge Options |
|-----------|--------------|
| GPT-4 / GPT-4o | Claude, Gemini, Llama-based |
| Claude | GPT-4, Gemini, Llama-based |
| Open-source (Llama, Mistral) | Any commercial model, or a different open-source family |

This doesn't eliminate shared failures (all LLMs share some biases), but it reduces correlated failure significantly.

### 3. Calibrate Continuously

The Judge's accuracy is not static. Track it weekly.

```
Week 1: Agreement 94% | FN 3% | FP 12%
Week 2: Agreement 93% | FN 4% | FP 11%
Week 3: Agreement 87% | FN 8% | FP 14%  ← drift detected, investigate
```

**Triggers for investigation:**

| Signal | Threshold | Action |
|--------|-----------|--------|
| Agreement drops >5% week-over-week | Immediate | Investigate - possible model update or data shift |
| FN rate exceeds tier threshold | Immediate | Increase human review sample, tighten guardrails |
| FP rate exceeds 25% | Next review cycle | Re-tune Judge prompt/criteria - alert fatigue risk |

### 4. Adversarial Test the Judge

Red-team the judge the same way you'd red-team the generator.

| Test | Method |
|------|--------|
| **Known-bad passthrough** | Submit known-harmful outputs and verify the Judge catches them |
| **Subtle policy violations** | Test edge cases - outputs that are technically compliant but violate intent |
| **Judge prompt injection** | Attempt to manipulate the Judge's evaluation via crafted generator outputs |
| **Consistency** | Submit the same output multiple times - does the Judge give consistent scores? |

### 5. Fail Safe

When the Judge is unavailable, degraded, or untrusted:

| Scenario | Response |
|----------|----------|
| Judge API timeout | Apply guardrails only + increase human review sample |
| Judge accuracy below threshold | Increase human review to 100% for affected risk tier |
| Judge model deprecated by provider | Switch to backup judge model (you should have one) |
| Judge cost exceeds budget | Sample-based evaluation (see [Cost and Latency](../extensions/technical/cost-and-latency.md)) |

**Never fail open.** If the Judge can't evaluate, tighten other controls. Don't skip evaluation.

## Integration with Existing Controls

| Existing Layer | Judge Assurance Addition |
|---------------|------------------------|
| **Guardrails** | Guardrails remain the first line - Judge assurance doesn't replace them |
| **Judge** | Add meta-evaluation metrics, calibration, adversarial testing |
| **Human Oversight** | Humans now serve dual purpose - deciding edge cases AND calibrating the Judge |
| **Metrics** | Add Judge-specific metrics to your monitoring dashboard |

## When You Need a Judge (and When You Do Not)

Not every workflow needs a Model-as-Judge. A judge adds cost, latency, and a new failure mode. It is only worth deploying if it catches more risk than it creates.

### The Judge Necessity Test

Answer these five questions before deploying a judge:

| Question | If Yes | If No |
|----------|--------|-------|
| **1. Do your guardrails miss failure modes you care about?** | A judge adds semantic evaluation that guardrails cannot provide. Proceed. | Guardrails are sufficient. No judge needed for those modes. |
| **2. Are the consequences of an undetected failure material?** (Financial loss, regulatory violation, reputational harm, patient safety) | The cost of the judge is justified by the cost of the failure. | The failure is tolerable. Sample-based or post-hoc review is enough. |
| **3. Can a judge realistically catch the failure?** (Is the evaluation task within current model capability?) | Deploy the judge and calibrate it. | A judge that cannot detect the threat is security theatre. Invest in guardrails, infrastructure constraints, or human review instead. |
| **4. Is the judge's false negative rate lower than the base rate of the threat?** | The judge is net-positive for security. | The judge misses more than it catches. Retrain, replace, or remove it. |
| **5. Does the workflow have multiple policy domains that could conflict?** (Fraud, security, compliance, data protection) | Multi-domain evaluation with [conflict resolution](../maso/controls/privileged-agent-governance.md#inter-judge-conflict-resolution). | Single-domain evaluation or guardrails only. |

### Judge ROI Assessment

For each judge layer, calculate the net security value:

```
Net security value = (Threats caught × Cost per undetected threat)
                   - (Judge operating cost + False positive cost + Judge failure risk)
```

Where:

- **Threats caught** = Judge true positive rate × threat volume
- **Cost per undetected threat** = financial, regulatory, or reputational impact of the threat the judge is designed to catch
- **Judge operating cost** = infrastructure + API costs + calibration + maintenance (see [Cost and Latency](../extensions/technical/cost-and-latency.md))
- **False positive cost** = false positive rate × cost per false positive (human review time, delayed transactions, user friction)
- **Judge failure risk** = probability of judge failure × impact of false assurance (operating with a broken judge is worse than operating with no judge, because the team believes it is protected)

If the net security value is negative, the judge is not worth deploying. This does not mean the threat is unimportant. It means a different control (tighter guardrails, infrastructure constraints, human review) is a better investment for that threat.

### The Minimum Viable Evaluation Stack

For most workflows, the minimum viable evaluation stack is:

| Risk Level | Evaluation Stack |
|-----------|-----------------|
| **Low** | Guardrails only. Sampled post-hoc review (1-5%). |
| **Medium** | Guardrails + sampled judge evaluation (25-50%). |
| **High** | Guardrails + 100% tactical judge (SLM sidecar for latency). Strategic evaluator at phase boundaries. |
| **Critical** | Full stack: guardrails + synchronous tactical judge + strategic evaluator + multi-domain evaluation + meta-evaluation calibration. |

The full evaluation stack is reserved for critical-risk workflows where the cost of an undetected failure justifies the overhead. Deploying it everywhere is over-engineering. Deploying nothing on a critical workflow is negligence.

## The Honest Assessment

Even with all these controls, you cannot prove the Judge is correct. You can only measure its accuracy against human judgment, track its consistency over time, and react when it drifts.

This is the same epistemic limitation identified in [The Verification Gap](../insights/the-verification-gap.md). The Judge doesn't solve it - it manages it. Judge Assurance ensures you know how well it's managing.

## Related Documents

The Judge layer is covered across several documents. If you're here, you probably need these too:

| Document | What It Covers |
|----------|---------------|
| [When the Judge Can Be Fooled](when-the-judge-can-be-fooled.md) | Adversarial failure modes: output crafting, judge manipulation, judge limitations. Tier-specific mitigations. |
| [Cost and Latency](../extensions/technical/cost-and-latency.md) | Judge latency budgets (500ms–5s per evaluation), sync vs async guidance, sampling strategies by risk tier, tiered evaluation cascade (rule-based → small model → large model → human). |
| [Privileged Agent Governance](../maso/controls/privileged-agent-governance.md) | MASO controls for the Judge as a privileged agent: calibration testing (PA-2.2), criteria versioning (PA-2.3), model rotation (PA-3.4), continuous calibration (PA-3.5). |
| [Execution Control - EC-2.5](../maso/controls/execution-control.md) | Judge as the gate for agent actions. Action classification rules. Cross-validation at Tier 3 (EC-3.3). |
| [Distilling the Judge into an SLM](../extensions/technical/distill-judge-slm.md) | Knowledge distillation from a large Judge into a fast, local Small Language Model for inline action screening. Includes the "check the checker" validation loop. |
| [Judge Precedents](../extensions/technical/judge-precedents.md) | Worked examples of good and bad decisions that anchor judge evaluation, improve consistency, and make abstract criteria concrete. |
| [The Feedback Loops That Make It Work](../insights/feedback-loops.md) | How judge verdicts, human labels, and downstream outcomes feed back into guardrail tuning, judge calibration, and policy updates. |

