---
description: "Stakeholder review of MASO's judge architecture: does the framework create 'judge hell' where multiple evaluation agents proliferate uncontrollably, and how does it cope?"
---

# Stakeholder Review: Judge Proliferation

**The "judge hell" problem, examined from five business perspectives.**

> *Review of [MASO Framework](../README.md) · [Objective Intent](../controls/objective-intent.md) · [Privileged Agent Governance](../controls/privileged-agent-governance.md) · [Judge Assurance](../../core/judge-assurance.md)*

## The Question

A fraud detection workflow using MASO requires agents to detect fraud. Those agents need judges to decide whether the detected fraud is real. The judges need monitoring to confirm they are judging correctly. That monitoring needs its own validation. At what point does this become **judge hell**: an uncontrollable proliferation of evaluation agents that costs more than the fraud it prevents?

This review examines the problem from five stakeholder perspectives, assesses how MASO addresses it today, and identifies where gaps remain.

## What MASO Actually Requires

Before examining stakeholder concerns, here is what MASO specifies for a fraud detection workflow at Tier 2 (Managed):

| Component | Role | Required? |
|-----------|------|-----------|
| **Task agents** (e.g. 3 fraud analysts) | Detect fraud patterns, score transactions, gather evidence | Yes |
| **Tactical judge** | Evaluates each agent's actions against its OISpec | Yes (OI-2.1) |
| **Strategic evaluator** | Assesses whether combined agent outputs satisfy the workflow objective | Yes (OI-2.2) |
| **Judge meta-evaluator** | Monitors judge drift against the judge's own OISpec | Yes (OI-2.4) |
| **Observer** | Anomaly scoring, PACE escalation triggers | Yes (OB-2.2) |
| **Orchestrator** | Plans, routes, aggregates | Likely |

For 3 task agents, MASO requires up to 4 additional privileged agents. That is a ratio of roughly 1.3 evaluation agents per task agent. At 10 task agents the ratio improves (judges can be shared across agents), but the concern is real: MASO's evaluation architecture is not lightweight.

## Stakeholder Perspectives

### 1. CISO: "Does this actually reduce risk, or just move it?"

**The concern:** Every judge is itself a model. It hallucinates, drifts, and can be manipulated. Adding judges adds attack surface. If the judge is wrong about a fraud case, you have a false sense of security that is worse than having no judge at all.

**What MASO gets right:**

- The framework explicitly acknowledges this. Judge Assurance states: "If you deploy a Judge without evaluating its accuracy, you have added cost and latency without knowing whether you have added safety."
- Model diversity (different provider for judge vs. task agent) reduces correlated failure.
- Continuous calibration with known test cases (PA-2.2, PA-3.5) catches judge drift before it becomes dangerous.
- The recursion explicitly terminates at sampled human review, not at more agents. The Objective Intent document is clear: "The recursion stops at humans, not at more agents."

**Addressed:** [Judge Assurance](../../core/judge-assurance.md#when-you-need-a-judge-and-when-you-do-not) now includes a **Judge Necessity Test** (five questions to determine whether a judge is warranted) and a **Judge ROI Assessment** formula that calculates net security value per evaluation layer. If the judge's false negative rate exceeds the base rate of the threat, the formula returns a negative value, making the case for removal or retraining explicit.

### 2. CFO: "What does this cost at scale?"

**The concern:** Every judge is an LLM call. At Tier 2 with 25-50% sampling, the judge cost is already 15-40% of generator cost. At Tier 3 with 100% evaluation plus a meta-evaluator, the overhead could exceed the cost of the task agents themselves. For fraud detection processing millions of transactions, judge costs compound fast.

**What MASO gets right:**

- The Cost and Latency document provides concrete budgeting: $10K-50K/month for judge evaluation at 1M requests.
- Tiered evaluation (rule-based first, then small model, then large model, then human) reduces cost by 60-80%.
- Distilled SLMs eliminate per-token API costs for routine screening, with near-flat cost scaling: ~$350-700/month at 1M evaluations vs. $10K-50K for cloud judges.
- Sampling strategies mean not every transaction needs full evaluation. Low-risk transactions get 5-10% judge sampling.

**Where the gap is:**

The cost analysis covers a single judge layer. It does not model the **compound cost of the full evaluation stack**: tactical judge + strategic evaluator + meta-evaluator + observer. For a fraud detection workflow at Tier 3:

| Component | Evaluation rate | Estimated monthly cost (1M transactions) |
|-----------|----------------|------------------------------------------|
| Task agents (3) | 100% | Base cost |
| Tactical judge | 100% of agent actions | $10K-50K (or ~$500 with SLM) |
| Strategic evaluator | Per-phase + post-execution | $1K-5K |
| Meta-evaluator | Daily calibration samples | $500-2K |
| Observer | Continuous (lightweight) | $500-1K |
| **Total evaluation overhead** | | **$12K-58K** (or **$2.5K-8.5K** with SLM) |

The SLM approach dramatically changes the economics.

**Addressed:** [Cost and Latency](../../extensions/technical/cost-and-latency.md#total-cost-of-evaluation-multi-agent-workflows) now includes a **Total Cost of Evaluation** section modelling the full stack: tactical judge + domain judges + strategic evaluator + meta-evaluator + observer. Two scenarios (cloud judge vs. SLM sidecar) are worked through for a fraud detection workflow at 1M transactions/month. The SLM scenario shows 95-97% cost reduction at that volume.

### 3. Head of Engineering: "How do I build and operate this?"

**The concern:** Operating 4 evaluation agents per workflow is a significant engineering burden. Each needs deployment, monitoring, versioning, calibration, and incident response. The OISpec for each must be authored at design time, version-controlled, and updated as requirements change. This is not a one-time build; it is ongoing operational overhead.

**What MASO gets right:**

- Implementation tiers allow incremental adoption. Tier 1 requires only manual review against OISpecs, no automated judges.
- Judges can be shared across agents. A single tactical judge can evaluate multiple task agents if they share an evaluation model.
- The distilled SLM sidecar pattern (one model, deployed alongside task agents) consolidates the tactical judge into infrastructure rather than a separate service.
- OISpecs are structured JSON, not free-form prose, making them automatable.

**Where the gap is:**

MASO does not address **judge consolidation patterns**. In practice, a fraud detection workflow does not need a separate judge instance per task agent. It needs:

- One tactical evaluation model (possibly an SLM sidecar) that evaluates all task agents against their respective OISpecs.
- One strategic evaluation pass (could be a single LLM call post-workflow, not a persistent agent).
- One meta-evaluation process (a scheduled calibration job, not a persistent agent).

The framework describes these as conceptually distinct roles, which is correct for the security model. But they can be **operationally consolidated** into far fewer running services than the architecture diagrams suggest.

**Addressed:** [Execution Control](../controls/execution-control.md#deployment-topology-evaluation-roles-vs-services) now includes a **Deployment Topology** section distinguishing evaluation roles from evaluation services. It maps the conceptual architecture to actual infrastructure: a fraud detection workflow's "9 components" deploys as 3 pods + 1 serverless function + 1 scheduled job + existing monitoring. Context isolation requirements are specified to ensure consolidation does not compromise security.

### 4. Head of Compliance: "Can I audit this?"

**The concern:** Regulators expect explainable decisions. If a fraud detection system flags a transaction, the compliance team needs to trace: which agent flagged it, what evidence it used, whether the judge agreed, and what criteria the judge applied. With multiple evaluation layers, the audit trail becomes complex.

**What MASO gets right:**

- Immutable decision chain logs (OB-1.1) capture the full reasoning and action history.
- Judge decision logging (PA-1.3) records criteria and reasoning for every approve/escalate/block decision.
- OISpecs provide the reference standard: the auditor can compare what the agent *did* against what it was *supposed to do*, with both documented in structured, versioned artifacts.
- The three-level evaluation (tactical, strategic, meta) creates a layered audit trail, not a black box.

**Where the gap is:**

**Addressed:** [Observability](../controls/observability.md#decision-trace-consolidated-audit-view) now defines a **Decision Trace** format that collapses the multi-layer evaluation chain into a single auditable JSON document per decision. It includes the agent chain, all judge verdicts with reasoning, inter-judge conflict resolution (if any), strategic evaluation, meta-evaluation status, human decision (if escalated), and regulatory mapping. Generated on demand or at trigger points (escalation, PACE transition, inter-judge conflict, regulated decision).

### 5. Head of Fraud Operations: "Does this slow down detection?"

**The concern:** Fraud detection is time-sensitive. A synchronous judge adding 500ms-5s per evaluation can mean the difference between blocking a fraudulent transaction in real-time and blocking it after the money has moved. Multiple evaluation layers compound this latency.

**What MASO gets right:**

- The SLM sidecar adds only 10-50ms per evaluation, making inline evaluation feasible without breaking latency budgets.
- Async evaluation is the default for non-critical assessments. The large judge runs post-action for most cases.
- Strategic evaluation runs per-phase and post-execution, not per-transaction.
- The meta-evaluator runs on a scheduled basis (daily calibration), adding zero latency to the transaction path.

**Where the gap is:**

The latency analysis does not model the **critical path** through the full evaluation stack for a fraud detection use case. In practice:

| On the critical path (synchronous) | Off the critical path (async) |
|-------------------------------------|-------------------------------|
| Guardrails (5-20ms) | Strategic evaluator (post-phase) |
| SLM tactical evaluation (10-50ms) | Large judge (1% sample, async) |
| | Meta-evaluator (daily calibration) |
| | Observer (continuous, non-blocking) |

**Total synchronous overhead: 15-70ms.** That is well within fraud detection latency requirements.

**Addressed:** [Cost and Latency](../../extensions/technical/cost-and-latency.md#critical-path-latency-for-time-sensitive-workflows) now includes a **Critical-Path Latency** section showing which evaluation components are synchronous vs. asynchronous. Fraud detection example: 10-50ms on the critical path (SLM sidecar), everything else async. Trading compliance example at CRITICAL risk: 1.1-4.6s when the cloud judge runs synchronously.

## The Inter-Judge Conflict Problem

Judge proliferation is not just about cost and latency. It creates a coordination problem: when multiple judges evaluate the same action from different perspectives, they will disagree.

### A Concrete Example

A fraud detection workflow flags a $12,000 wire transfer. Three domain judges evaluate it:

| Judge | Verdict | Reasoning |
|-------|---------|-----------|
| **Fraud judge** | Flag | Velocity pattern matches known card-testing behaviour. Geo-mismatch between IP and billing address. |
| **Security judge** | Approve | Transaction originates from an authenticated session. No credential anomalies. MFA completed. |
| **Compliance judge** | Block | Transaction exceeds the documentation threshold for this customer tier. Missing source-of-funds declaration. |

Which verdict wins? Without a defined protocol, the system either deadlocks, escalates everything to a human (defeating automation), or applies whichever judge responded first (non-deterministic and unauditable).

### How MASO Now Handles This

[Privileged Agent Governance](../controls/privileged-agent-governance.md#inter-judge-conflict-resolution) now includes a full inter-judge conflict resolution protocol:

**1. Precedence order declared at design time.** Every workflow OISpec includes a `judge_precedence` field specifying which evaluation domain takes priority. This is a business and regulatory decision, not a technical one. In financial services, compliance typically outranks fraud, which outranks security.

**2. "Most restrictive wins" as the default.** If any judge says block, the action is blocked. If any judge says flag while others approve, the action is escalated. This is conservative by design: false positives from multi-domain disagreement are preferable to false negatives where a legitimate concern is overridden.

**3. Time-constrained conflicts with competing actions.** The harder problem is not approve vs. block, it is when judges agree that action is needed but prescribe *different* actions. Active fraud with an active security breach: the fraud judge wants to chase the money, the security judge wants to contain the breach, the compliance judge wants to hold the transaction. The protocol handles this:

- **Security containment executes first.** You cannot pursue stolen funds through a compromised channel. Containment is the prerequisite.
- **Parallel degraded actions follow.** Once contained, fraud and compliance actions proceed in a degraded mode within the security boundary: compensate the customer directly for confirmed loss, chase the destination through inter-bank channels, file regulatory notifications.
- **Time-bounded resolution windows.** CRITICAL conflicts resolve in 60 seconds (security acts, others degrade). HIGH conflicts hold transactions for up to 15 minutes pending human arbitration.
- **Explicit residual risk acceptance.** If the resolution window expires with no human, the workflow OISpec declares the default: either apply the most restrictive action (frozen accounts, customer friction) or accept the risk of loss with full logging and attribution. There is no silent expiry.

**4. Conflicts are logged with full context.** Every inter-judge disagreement records all verdicts with reasoning, the resolution rule applied, whether it was resolved automatically or escalated to a human, and the human's decision if escalated. This creates the data set needed to tune precedence rules over time.

**5. Conflict rate is a judge health metric.** Persistent disagreement above 15% between two judges indicates misaligned evaluation criteria, not healthy diversity. The framework specifies three root cause patterns (threshold mismatch, scope overlap, ambiguous criteria) with specific remediation for each.

### What This Means for Stakeholders

For the **CISO**: inter-judge conflicts are signal, not noise. Two judges disagreeing on the same transaction surfaces a risk that a single judge would miss entirely. The conflict itself has security value.

For the **CFO**: conflicts that consistently resolve the same way should be automated. If the fraud judge and security judge disagree on velocity-pattern transactions and humans always side with the fraud judge, that resolution becomes a rule. Fewer escalations, lower cost.

For **Compliance**: the Decision Trace format now includes an `inter_judge_conflict` section documenting the disagreement and its resolution. This is the audit trail regulators need for explainability requirements.

For **Fraud Operations**: the "most restrictive wins" default means fraud flags are never overridden by another domain's approval without human intervention. This protects the fraud team's detection capability while giving compliance and security their own voice.

## Policy-Driven Evaluation: Ethics, Bias, and Fairness

Not every evaluation domain belongs in the synchronous judge stack. Fraud, security, and compliance have measurable criteria and require real-time verdicts. Ethics, bias, and fairness are different: they are defined by organisational policy, they vary by jurisdiction and context, and an LLM evaluating "is this biased?" is applying its own training biases to detect bias.

[Privileged Agent Governance](../controls/privileged-agent-governance.md#policy-driven-evaluation-domains-ethics-bias-and-fairness) now distinguishes **operational domains** (synchronous, measurable, regulatory) from **policy-driven domains** (offline, advisory, organisational):

- Ethics/bias/fairness evaluation runs as an **offline monitoring and evaluation process**, outside the direct agent architecture, not as an inline judge
- The monitoring pipeline consumes **signals from both the runtime system and external sources** that the agent architecture has no visibility into: customer feedback, complaints, appeal outcomes, regulatory correspondence, demographic outcome distributions, ombudsman findings, market benchmarking
- **Portfolio-level statistical monitoring** combined with external signals is more reliable than per-action LLM evaluation. A single decision may not be detectably biased. A pattern of 10,000 decisions with a 3x denial rate disparity across protected classes is detectable, especially when correlated with a spike in customer complaints
- **Organisations define the policy**: what constitutes an ethical violation, which protected classes are monitored, what statistical thresholds trigger investigation, what fairness standard applies (equal treatment, equal outcomes, jurisdiction-specific), which external signal sources feed the monitoring pipeline
- The framework provides the monitoring mechanism and the integration points. It does not prescribe ethics policy, because that is an organisational decision, not a technical one.

The key insight: making an "ethics judge" a synchronous inline gate will fail. It will produce false positives on ambiguous cases (teams disable it) and false negatives on systematic biases (it shares the task agent's training biases). Offline monitoring with external signals and human governance is more reliable and more durable, because the most important evidence (customer complaints, appeal outcomes, regulatory findings) is not available to any inline judge.

## How MASO Addresses Judge Hell

MASO has five mechanisms that prevent evaluation from becoming an unbounded recursion:

### 1. The chain terminates at humans

The Objective Intent document is explicit: "The recursion of 'who evaluates the evaluator' must stop somewhere. In this framework, it stops at sampled human review." There is no meta-meta-evaluator. The meta-evaluator is validated through periodic human calibration, not through more agents.

### 2. Calibration replaces recursion

The Privileged Agent Governance common pitfalls section states: "The recursion problem is real but the solution is not more layers. It's calibration: periodic injection of known test cases to verify that each privileged agent is still performing as expected." Known-good and known-bad test cases injected into the evaluation pipeline confirm accuracy without requiring additional judges.

### 3. Evaluation frequency scales with risk

Not every transaction gets full evaluation. The risk classification table in Objective Intent specifies:

- **LOW risk:** Post-execution evaluation only, monthly judge calibration
- **MEDIUM risk:** Per-phase evaluation, monthly calibration
- **HIGH risk:** Every-action evaluation, weekly calibration
- **CRITICAL risk:** Synchronous every-action evaluation, daily calibration

Most fraud transactions are LOW or MEDIUM risk (known patterns, small amounts). Only HIGH/CRITICAL transactions (unusual patterns, large amounts) trigger the full evaluation stack.

### 4. SLM distillation collapses the tactical judge into infrastructure

A distilled SLM running as a sidecar is not an "agent" in the operational sense. It is a model loaded into the same process or pod as the task agent, adding 10-50ms per evaluation. This eliminates the most expensive and highest-volume evaluation layer (tactical) from the "judge proliferation" concern.

### 5. Conceptual roles do not require separate services

The strategic evaluator can be a single LLM call at phase boundaries. The meta-evaluator can be a scheduled calibration job. The observer can be a metrics pipeline. These are evaluation *functions*, not necessarily evaluation *agents* requiring their own infrastructure.

## Gaps Identified and Addressed

| Gap | Where It Is Now | Benefits |
|-----|----------------|----------|
| No judge ROI assessment | [Judge Assurance: When You Need a Judge](../../core/judge-assurance.md#when-you-need-a-judge-and-when-you-do-not) | CISOs can justify (or reject) each layer with data |
| No compound cost model | [Cost and Latency: Total Cost of Evaluation](../../extensions/technical/cost-and-latency.md#total-cost-of-evaluation-multi-agent-workflows) | CFOs get one number for the full stack, not per-layer fragments |
| No deployment topology guidance | [Execution Control: Deployment Topology](../controls/execution-control.md#deployment-topology-evaluation-roles-vs-services) | Engineers build 3 services, not 9 |
| No consolidated audit view | [Observability: Decision Trace](../controls/observability.md#decision-trace-consolidated-audit-view) | Compliance teams trace decisions in one document |
| No critical-path latency model | [Cost and Latency: Critical-Path Latency](../../extensions/technical/cost-and-latency.md#critical-path-latency-for-time-sensitive-workflows) | Fraud ops teams see 10-50ms, not "500ms-5s" |
| No judge necessity criteria | [Judge Assurance: Judge Necessity Test](../../core/judge-assurance.md#when-you-need-a-judge-and-when-you-do-not) | Prevents unnecessary judges on low-risk workflows |
| No inter-judge conflict resolution | [Privileged Agent Governance: Inter-Judge Conflict Resolution](../controls/privileged-agent-governance.md#inter-judge-conflict-resolution) | Defined precedence, most-restrictive-wins default, conflict logging |
| No judge proliferation recognition | [Privileged Agent Governance: Recognising Judge Proliferation](../controls/privileged-agent-governance.md#recognising-judge-proliferation) | Teams distinguish evaluation roles from services before panicking |
| No guidance on ethics/bias/fairness evaluation | [Privileged Agent Governance: Policy-Driven Evaluation Domains](../controls/privileged-agent-governance.md#policy-driven-evaluation-domains-ethics-bias-and-fairness) | Async post-action evaluation with portfolio monitoring, not a synchronous "ethics judge" |

## The Honest Answer

Judge hell is a real risk if you implement MASO mechanically: deploying every evaluation layer at maximum intensity for every workflow regardless of risk. The framework provides the tools to avoid this (tiered evaluation, risk-based frequency, SLM consolidation, human-terminated recursion), but it does not make the "right-sizing" guidance prominent enough.

For a fraud detection workflow at Tier 2 with SLM sidecars:

- **Synchronous overhead:** 15-70ms per transaction (SLM tactical evaluation)
- **Async overhead:** Strategic evaluation per batch, meta-evaluation daily
- **Cost overhead:** $2.5K-8.5K/month at 1M transactions (with SLM), vs. $12K-58K without
- **Agents to operate:** 1 SLM sidecar (infrastructure, not a service), 1 strategic evaluation job (batch), 1 calibration pipeline (scheduled)
- **Recursion depth:** 3 levels max, terminating at human calibration samples

That is not judge hell. That is a manageable evaluation architecture. But MASO needs to make this operational reality clearer, because the conceptual architecture diagrams suggest a complexity that the actual deployment does not require.

!!! info "References"
    - [MASO Framework](../README.md)
    - [Objective Intent Controls](../controls/objective-intent.md)
    - [Privileged Agent Governance](../controls/privileged-agent-governance.md)
    - [Judge Assurance](../../core/judge-assurance.md)
    - [Cost and Latency](../../extensions/technical/cost-and-latency.md)
    - [Distilling the Judge into an SLM](../../extensions/technical/distill-judge-slm.md)
    - [MASO 2.0 Anticipated Changes](../maso-2.0-anticipated-changes.md)
