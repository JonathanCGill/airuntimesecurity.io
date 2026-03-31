---
description: "Why AI models degrade over time as training cutoffs age, and why MASO architectures must treat temporal decay as a correlated failure mode across Agents, Judges, and knowledge bases."
---

# Temporal Decay Is Correlated Failure

*The model was accurate when it shipped. The world kept moving. Now every layer of your MASO architecture is confidently wrong about the same things.*

## What the Evidence Shows

Temporal decay is not speculative. Studies on GPT-4 and comparable models show measurable performance degradation on time-sensitive tasks as the gap between training cutoff and deployment widens. A 2023 Stanford study demonstrated that GPT-4's performance on specific coding and reasoning tasks changed significantly over months.

Three mechanisms drive this.

**Knowledge staleness.** The model's world model freezes at its training cutoff. The real world does not. The divergence compounds over time. Facts become wrong. References become outdated. Procedures reflect superseded versions. The model continues to answer confidently because it has no signal that its knowledge has expired.

**Distributional shift.** The language, terminology, regulations, and context the model was trained on all drift. New concepts emerge that the model has no representation of. It pattern-matches to the nearest equivalent in its training data, which introduces subtle errors that are harder to catch than outright hallucinations.

**Retrieval does not fully compensate.** RAG mitigates factual staleness by injecting current information at inference time. But the model's reasoning patterns, priors, and internal representations are still frozen. A model trained before a regulatory change can retrieve the new regulation but may still reason about it using outdated mental models of how that regulatory domain works.

There is a further mechanism that is less evidenced but reasonable to anticipate: **confidence miscalibration over time**. The model does not know what it does not know about post-cutoff reality. It cannot flag uncertainty about topics it has never encountered. It assigns the same confidence to stale knowledge as it does to current knowledge, because from its perspective, all knowledge is equally present.

## Why This Matters for MASO

The model drift problem is well understood for single-agent systems. Temporal decay introduces a specific failure mode in multi-agent architectures that drift detection alone does not address: **correlated decay across the control hierarchy**.

### Three Decay Vectors

MASO architectures have three independently decaying components, and each decays along its own timeline.

| Component | Decay Mechanism | Consequence |
|---|---|---|
| **Agent** | Training cutoff ages. World knowledge becomes stale. Reasoning patterns reflect superseded context. | Agent makes worse decisions as reality moves past its training data. |
| **Judge** | Same training cutoff ages. The behavioural constitution and evaluation criteria reflect a world that no longer exists. | Judge validates against an increasingly stale intent framework. Approves actions it should flag. |
| **Knowledge base** | Policy documents, regulatory references, and domain knowledge become outdated if not actively maintained. | Both Agent and Judge operate on stale grounding data, compounding their own decay. |

### The Correlated Failure Problem

This is the critical insight. In the standard [defence-in-depth architecture](../ARCHITECTURE.md), safety depends on independent failure across layers. If the Guardrail misses something, the Judge catches it. If the Judge misses it, the human reviewer catches it.

Temporal decay breaks that independence.

If the Judge runs on the same or a similar model as the Agent, they decay together. Their training cutoffs are the same. Their blind spots are the same. They drift in the same direction. The Judge does not catch what the Agent gets wrong, because the Judge is wrong about the same things for the same reasons.

This is correlated degradation applied to time, the most dangerous pattern in a defence-in-depth architecture. Correlated miss rate increases compound residual risk. Temporal decay is a specific, predictable driver of exactly that correlation.

### A Concrete Example

Consider a payment fraud detection system built on MASO.

Fraud patterns evolve continuously. New attack vectors emerge. Regulatory reporting requirements change. Transaction patterns shift with new payment methods and platforms.

A Judge trained on pre-2024 fraud typologies will increasingly fail to flag novel patterns. The Agent executes. The Judge approves. Both are confidently wrong, not because either component has a bug, but because neither component's training data includes the fraud pattern that just appeared six months ago.

The system's confidence remains high while its accuracy degrades. That is the failure mode.

## Designing Against Temporal Decay

### Decorrelate the Decay Curves

Judge and Agent should not run on the same model version. Using different models, or at minimum different model versions with different training cutoffs, introduces independent decay timelines. When the Agent's knowledge becomes stale in one domain, the Judge may still have coverage if its training data was more recent or drawn from different sources.

This is the same principle as [judge model selection](../extensions/technical/judge-model-selection.md): the Judge must be architecturally independent from the system it evaluates. Temporal independence is one dimension of that separation.

### Schedule Model Refresh for the Judge, Not Just the Agent

Most organisations plan model upgrades for the Agent (the user-facing component). The Behaviour Overseer is treated as infrastructure, updated less frequently if at all. This is backwards.

The Judge's accuracy is more consequential than the Agent's, because the Judge is the control that catches the Agent's failures. If the Judge decays faster or in step with the Agent, the entire control hierarchy degrades together. Judge refresh cadence should be at least as aggressive as Agent refresh cadence.

### Add a Staleness Threshold to Kill Switch Triggers

The [PACE resilience model](../PACE-RESILIENCE.md) defines escalation triggers based on observed anomalies. Temporal decay should be an explicit trigger.

If model age (time since training cutoff) exceeds a defined threshold for the domain's rate of change, the system should escalate to human review by default, regardless of whether anomaly detection has flagged anything. This is a preventive control, not a reactive one.

Domains with high rates of change (fraud, regulatory compliance, financial markets) need shorter staleness thresholds. Domains with lower rates of change (internal document summarisation, code review) can tolerate longer gaps.

### Version and Expire Knowledge Base Content

Intent declarations sourced from policy need active versioning with expiry dates. A policy document loaded into the knowledge base should carry metadata indicating when it was last validated and when it expires.

When the knowledge base contains expired content, the system should flag this to operators and, depending on the domain's risk tier, restrict operations until the content is refreshed.

### Monitor the Judge-Agent Agreement Trend

Judges ruling against Agents more frequently over time is a healthy signal if the system is working correctly. It means the Judge is catching Agent degradation.

The concern is the opposite: stable or declining disagreement rates over time, combined with increasing model age. That pattern suggests the Judge and Agent are decaying in lockstep. The divergence is going undetected because both components share the same blind spots.

Track the Judge-Agent disagreement rate as a time series. Alert on sustained decreases in disagreement that correlate with increasing model age. A Judge that never disagrees with an aging Agent is a Judge that has stopped working.

## Model Currency as a Control Input

The MASO architecture defines four control layers: Guardrails, Judge, Human Oversight, and Observability. Temporal decay suggests a fifth input that feeds into the Overseer's risk calculus: **model currency**.

Model currency tracks training cutoff age against real-world drift indicators for the specific domain. It is not a control layer itself. It is a signal that modulates the stringency of every other layer.

| Model Currency State | Response |
|---|---|
| **Current** | Model age within threshold for domain rate of change. Normal operations. Standard Judge sampling rates. |
| **Aging** | Model approaching staleness threshold. Increase Judge sampling rate. Tighten uncertainty bounds. Flag to operations team for refresh planning. |
| **Stale** | Model age exceeds threshold. Escalate all decisions to human review. Restrict autonomous actions. Initiate model refresh. |
| **Expired** | Model age significantly exceeds threshold for a high-change domain. Circuit breaker fires. System operates in degraded mode until refresh completes. |

This maps directly onto [PACE states](../PACE-RESILIENCE.md), with model currency acting as one of the inputs that drives state transitions.

## The Bottom Line

Temporal decay is not the same problem as model drift. Drift is about unexpected behavioural change. Temporal decay is about predictable knowledge obsolescence. You can measure it. You can anticipate it. You can design against it.

The specific danger for MASO is correlated decay: the Agent and Judge aging together, becoming blind to the same things at the same rate, while the system's confidence metrics remain stable. That is the failure mode to design against, and it requires deliberate architectural separation of decay timelines, active knowledge base maintenance, and staleness thresholds that trigger escalation before anomaly detection has anything to detect.

!!! info "References"
    - [Observability Controls](../maso/controls/observability.md) - Continuous monitoring to detect drift across the control hierarchy
    - [Judge Model Selection](../extensions/technical/judge-model-selection.md) - Why the Judge must be architecturally independent from the system it evaluates
    - [PACE Resilience](../PACE-RESILIENCE.md) - Structured degradation when control integrity is compromised
    - [MASO Observability Controls](../maso/controls/observability.md) - Per-agent drift detection and cross-agent correlation
    - [Behavioral Anomaly Detection](../extensions/technical/behavioral-anomaly-detection.md) - Aggregating safety signals to detect when behavior drifts from normal
    - Chen, L., Zaharia, M. & Zou, J. (2023) *How Is ChatGPT's Behavior Changing over Time?* Stanford University, arXiv:2307.09009
