---
description: "MASO controls for governing orchestrators, evaluators, and observers: securing the agents that have authority over other agents in multi-agent systems."
---

# MASO Control Domain: Privileged Agent Governance

> Part of the [MASO Framework](../README.md) · Control Specifications
> Extends: [Execution Control](execution-control.md) · [Observability](observability.md) · [Identity & Access](identity-and-access.md)
> Covers: Orchestrator security · Judge governance · Observer assurance · Nested orchestration

## Principle

Any agent with authority over other agents - to plan, evaluate, monitor, or terminate - requires controls proportionate to that authority. Orchestrators, evaluators, and observers are not exempt from the control architecture. They are subject to a version of it that matches their specific threat model.

The controls in other MASO domains secure task agents against each other and against external threats. This domain secures the system against failures in the agents that govern it.

## Why This Matters

**Orchestrators influence outcomes through decisions, not tools.** A compromised orchestrator causes harm through task decomposition, agent selection, and result interpretation. Existing controls (IA-2.5, tool scoping) don't address this because the orchestrator's power is in planning, not execution.

**Evaluators are single points of trust.** If Judge criteria drift or the Judge model is compromised, Layer 2 collapses silently: every output passes because the standard has shifted. The system reports healthy while controls are effectively disabled.

**Observers with kill switch authority can be weaponised.** An over-sensitive observer repeatedly triggers shutdowns. Operators disable it to restore service. The system now runs without its safety net, and nobody formally accepted that risk.

**Nested orchestration multiplies these risks.** A compromised sub-orchestrator affects its entire agent cluster. Per-agent blast radius caps don't contain aggregate harm from a coordinated sub-tree.

## Agent Role Classification

Before applying controls, classify each agent in the orchestration by its governance role:

| Role | Authority | Examples | Threat Profile |
|------|-----------|----------|----------------|
| **Task agent** | Executes scoped actions using tools | Analyst, writer, code executor, retriever | Tool misuse, data leakage, injection |
| **Orchestrator** | Plans, selects agents, sequences execution, interprets results | Planner, coordinator, router, aggregator | Goal subversion, malicious decomposition, selective suppression |
| **Evaluator** | Approves, blocks, or escalates other agents' outputs | Model-as-Judge, critic, reviewer, quality gate | Criteria drift, adversarial bypass, calibration decay |
| **Observer** | Monitors, scores anomalies, triggers escalation or kill switch | Monitoring agent, anomaly detector, safety agent | Miscalibration, over/under-sensitivity, weaponised shutdown |

An agent may hold multiple roles. An orchestrator that also evaluates intermediate outputs is both orchestrator and evaluator - and requires controls from both categories.

## Controls by Tier

### Tier 1 - Supervised

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **PA-1.1** Role declaration | Every agent's governance role (task, orchestrator, evaluator, observer) is explicitly declared in configuration | No implicit role assumption. An orchestrator that also evaluates must be declared as both. |
| **PA-1.2** Orchestrator plan logging | Every task decomposition and agent selection decision by the orchestrator is logged with reasoning | Enables human review of orchestrator planning decisions during supervised operation. |
| **PA-1.3** Judge decision logging | Every Judge approve/escalate/block decision is logged with the criteria applied and the reasoning | Builds the baseline data set required for Tier 2 calibration. |
| **PA-1.4** Privileged agent inventory | Maintain a register of all agents operating in orchestrator, evaluator, or observer roles | Updated when the agent topology changes. Reviewed monthly. |

**What you're building at Tier 1:** Visibility. You can answer: which agents have authority over other agents, what decisions are they making, and why?

### Tier 2 - Managed

All Tier 1 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **PA-2.1** Orchestrator intent verification | Orchestrator task decomposition is verified against the original user intent by an independent model | The model verifying orchestrator plans must not be the orchestrator itself. Catches goal subversion through malicious decomposition. |
| **PA-2.2** Judge calibration testing | Monthly calibration: present the Judge with known-good and known-bad test cases; measure detection accuracy | Minimum threshold: > 95% detection of HIGH severity violations, > 80% MEDIUM. Calibration results logged and trended. |
| **PA-2.3** Judge criteria versioning | All Judge evaluation criteria are version-controlled with change history and approval trail | Criteria changes require review by a human with domain knowledge. No silent updates to what the Judge evaluates against. |
| **PA-2.4** Judge disagreement protocol | When multiple evaluators reach conflicting verdicts on the same action or output, a defined resolution procedure activates | See [Inter-Judge Conflict Resolution](#inter-judge-conflict-resolution) below for the full protocol. Applies to both multi-model cross-validation (EC-3.3) and multi-domain evaluation (e.g. fraud judge vs. security judge vs. compliance judge evaluating the same action). |
| **PA-2.5** Observer precision monitoring | Observer false positive and false negative rates tracked and reported monthly | Target: < 5% false positive rate on PACE escalation triggers. False negatives measured through red team injection (PA-2.8). |
| **PA-2.6** Kill switch dual authorisation | Observer kill switch requires secondary confirmation: either a second independent signal or a human within a defined window | Prevents single miscalibrated observer from taking down the system. Exception: if the confirming mechanism is unavailable, the kill switch fires after the defined window (fail-safe). |
| **PA-2.7** Orchestrator behavioral baseline | Orchestrator decisions (agent selection, task decomposition patterns, retry frequency) baselined and monitored for drift | Uses the same anomaly scoring model as task agents (OB-2.2) but with orchestrator-specific signals. |
| **PA-2.8** Privileged agent red team | Quarterly adversarial testing of orchestrator, judge, and observer | Test scenarios: inject a goal-subverting decomposition plan, present the Judge with adversarial inputs designed to bypass criteria, trigger known anomalies to verify observer detection. |

**What you're building at Tier 2:** Measurement. You can answer: are our privileged agents still performing correctly, and how do we know?

### Tier 3 - Autonomous

All Tier 2 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **PA-3.1** Orchestrator output evaluation | Orchestrator's aggregated output - not just task agent outputs - is evaluated by the Judge | Catches failures smoothed over during aggregation: intermediate hallucinations, dropped caveats, selective emphasis. |
| **PA-3.2** Nested orchestration scoping | Each orchestration level has explicit permission boundaries; sub-orchestrators cannot exceed the scope delegated to them | Extends IA-2.4 (no transitive permissions) and IA-3.3 (delegation contracts) to orchestrator-to-sub-orchestrator boundaries. |
| **PA-3.3** Sub-tree blast radius | Blast radius caps apply per orchestration sub-tree, not just per individual agent | A sub-orchestrator managing 5 agents with individual caps of 100 records each does not implicitly have a 500-record aggregate cap. Sub-tree cap is defined independently. |
| **PA-3.4** Judge model rotation | Judge model is periodically rotated or supplemented with an alternative to prevent long-term adversarial adaptation | Rotation schedule based on risk tier. Prevents attackers from optimising against a static evaluator. |
| **PA-3.5** Continuous calibration | Judge calibration runs continuously (daily injection of known test cases) rather than monthly | Automated. Results feed into anomaly scoring. Calibration failure triggers PACE escalation. |
| **PA-3.6** Observer self-test | Observer runs a self-diagnostic cycle at defined intervals, injecting synthetic anomalies into its own detection pipeline | Confirms the observer's detection capability is operational. Failure to detect the synthetic anomaly triggers an alert to a human, not to the observer itself. |
| **PA-3.7** Cross-level evaluation | In nested topologies, evaluation occurs at each orchestration level, not just at the leaf (task agent) level | Each sub-orchestrator's aggregation decisions are evaluated before results flow up to the parent orchestrator. |

**What you're building at Tier 3:** Assured autonomy. Privileged agents are continuously verified, not just initially configured and assumed correct.

## Inter-Judge Conflict Resolution

When multiple judges evaluate the same action from different perspectives (fraud, security, compliance, data protection), they will disagree. This is expected. A fraud judge flags a transaction. A security judge approves it. A compliance judge blocks it. Which verdict wins?

Without a defined resolution protocol, teams either ignore conflicts (loudest judge wins) or escalate everything to humans (defeating automation). Both erode trust in the evaluation architecture.

### The Problem of Multi-Domain Evaluation

Multi-domain evaluation differs from multi-model cross-validation (EC-3.3). Cross-validation asks two models the same question. Multi-domain evaluation asks different questions about the same action:

| Evaluation Domain | Question Being Asked | Evaluation Timing |
|-------------------|---------------------|-------------------|
| **Fraud** | Is this transaction fraudulent? | Synchronous (operational) |
| **Security** | Does this action violate security policy? | Synchronous (operational) |
| **Compliance** | Does this action satisfy regulatory requirements? | Synchronous (operational) |
| **Data protection** | Does this action expose or mishandle sensitive data? | Synchronous (operational) |
| **Intent alignment** | Does this action satisfy the agent's declared OISpec? | Synchronous (operational) |
| **Ethics / bias / fairness** | Does this action align with organisational values and fairness standards? | Asynchronous (policy-driven, see [below](#policy-driven-evaluation-domains-ethics-bias-and-fairness)) |

These evaluate orthogonal concerns. A transaction can be non-fraudulent but non-compliant. Conflict between domain judges is meaningful signal, not noise.

Operational domains (fraud through intent alignment) participate in the real-time conflict resolution protocol below. Policy-driven domains (ethics, bias, fairness) run post-action and produce advisories, not blocks. See [Policy-Driven Evaluation Domains](#policy-driven-evaluation-domains-ethics-bias-and-fairness).

### Resolution Protocol

#### Step 1: Declare judge precedence at design time

Every workflow OISpec must include a **judge precedence order** that defines which evaluation domain takes priority when verdicts conflict. This is not a technical decision. It is a business and regulatory decision made by the workflow owner.

```json
{
  "judge_precedence": {
    "order": ["compliance", "data_protection", "security", "fraud", "intent_alignment"],
    "override_rules": [
      {
        "condition": "any_judge_verdict == block",
        "action": "block",
        "rationale": "Any domain can block; no domain can unblock what another has blocked"
      },
      {
        "condition": "fraud == flag AND security == approve",
        "action": "escalate",
        "rationale": "Domain disagreement on the same action requires human arbitration"
      }
    ]
  }
}
```

#### Step 2: Apply the "most restrictive wins" default

Unless the precedence order specifies otherwise: **the most restrictive verdict wins.** Any block wins. Any escalate wins over approve.

| Fraud Judge | Security Judge | Compliance Judge | Resolution |
|------------|---------------|-----------------|------------|
| Approve | Approve | Approve | **Approve** |
| Approve | Approve | Flag | **Escalate** |
| Flag | Approve | Approve | **Escalate** |
| Block | Approve | Approve | **Block** |
| Flag | Flag | Approve | **Escalate** (multi-domain concern) |
| Block | Flag | Block | **Block** |

Conservative by design. False positives from disagreement are preferable to false negatives where a legitimate concern is overridden.

#### Step 2a: Time-constrained conflicts with competing actions

The "most restrictive wins" default handles simple approve/flag/block disagreements. Harder conflicts arise when judges agree action is needed but disagree on *which* action:

| Judge | Verdict | Prescribed Action |
|-------|---------|-------------------|
| **Fraud judge** | Flag: active fraud detected | Pursue the money. Reverse the transaction. Notify the fraud team. |
| **Security judge** | Block: security violation in progress | Freeze the account. Revoke session credentials. Isolate the compromised endpoint. |
| **Compliance judge** | Block: regulatory hold required | Place transaction on hold for the maximum permissible period. Gather documentation. |

These are competing priorities with shared urgency, not contradictory verdicts. All three are legitimate, and delay harms all of them.

**Resolution for time-constrained conflicts:**

**1. Security containment takes precedence over fraud pursuit.** If a security violation is active (compromised credentials, unauthorized access, active breach), the security action executes first. You cannot pursue stolen funds through a compromised channel. Containment is the prerequisite for everything else.

**2. Parallel degraded actions where possible.** Once the security action has executed (account frozen, session revoked), the fraud and compliance actions can proceed in a degraded mode that respects the security boundary:

| After Security Containment | Degraded Fraud Action | Degraded Compliance Action |
|---------------------------|----------------------|---------------------------|
| Account frozen | Initiate recovery through the fraud team (not through the compromised agent). Compensate the customer directly if the transaction is confirmed fraudulent. | Regulatory hold is satisfied by the freeze. Documentation gathered from the immutable audit trail. |
| Session revoked | Chase the destination account through inter-bank channels. | File the required regulatory notification within the statutory window. |
| Endpoint isolated | Monitor for further exfiltration attempts from the isolated endpoint. | Preserve forensic evidence for regulatory inquiry. |

**3. Time-bounded resolution window.** When judges prescribe competing actions, the orchestrator applies a resolution window:

| Risk Level | Resolution Window | If No Resolution |
|-----------|------------------|-----------------|
| **CRITICAL** (active fraud + active breach) | Security action executes immediately. Other actions degraded within 60 seconds. | Human escalation. Transactions held at maximum permissible duration. |
| **HIGH** (suspected fraud, no active breach) | Transactions held for review. Human arbitration within 15 minutes. | Most restrictive action (hold) persists. Risk of loss accepted if no human responds. |
| **MEDIUM** | Standard escalation. Human arbitration within 1 hour. | Automated resolution per precedence order. |

**4. Accept residual risk explicitly.** If the resolution window expires without human arbitration, the system must either:

- Apply the most restrictive action and accept the operational impact (frozen accounts, delayed transactions, customer friction), or
- Release the hold and accept the risk of loss, with the decision logged and attributed to the workflow owner.

There is no silent default. The system either acts conservatively or accepts risk explicitly. It does not quietly let a hold expire.

The workflow OISpec must declare which of these two defaults applies for each risk level. This is a business decision: "We would rather freeze an innocent customer's account for 24 hours than lose $50,000 to fraud" vs. "We would rather accept a $500 loss than freeze a customer's account for more than 2 hours." Both are legitimate. Neither should be left to the orchestrator to decide at runtime.

```json
{
  "conflict_resolution": {
    "time_constrained": {
      "security_breach_active": {
        "primary_action": "security_containment",
        "parallel_degraded": true,
        "resolution_window_seconds": 60,
        "expiry_default": "most_restrictive"
      },
      "fraud_suspected_no_breach": {
        "primary_action": "hold_transaction",
        "human_arbitration_window_minutes": 15,
        "expiry_default": "accept_risk_with_logging",
        "max_hold_duration": "regulatory_maximum"
      }
    }
  }
}
```

#### Step 3: Log the conflict, not just the resolution

Every inter-judge conflict is logged with:

- All judge verdicts with reasoning
- The resolution applied (precedence rule or default)
- Whether the conflict was resolved automatically or escalated to a human
- The human's decision (if escalated) and their reasoning

This creates the data set needed to tune precedence rules over time. If a specific conflict pattern is consistently resolved the same way by humans, that resolution can be automated.

#### Step 4: Track conflict patterns

Persistent disagreement between two judges on the same class of action indicates one of three problems:

| Pattern | Likely Cause | Response |
|---------|-------------|----------|
| Fraud flags what security approves, repeatedly | Different risk thresholds or overlapping scope | Align evaluation criteria between domains |
| Compliance blocks what all other judges approve | Compliance criteria are stricter than operational policy | Business decision: tighten operational policy or accept the compliance overhead |
| Two judges consistently contradict on edge cases | Ambiguous evaluation criteria | Sharpen the OISpec for both judges |

Conflict rate is a judge health metric. A conflict rate above 15% between any two judges indicates a criteria alignment problem, not a healthy diversity of opinion.

### Policy-Driven Evaluation Domains: Ethics, Bias, and Fairness

Not all evaluation domains belong on the same decision path. Fraud, security, and compliance are **operational domains**: they have measurable criteria, they require real-time verdicts, and their thresholds are set by regulation or technical standards. A transaction either exceeds the velocity threshold or it does not. A credential is either compromised or it is not.

Ethics, bias, and fairness are different. They are **policy-driven evaluation domains** where:

- Criteria are set by organisational values, not by regulation or technical measurement
- Reasonable people disagree on what constitutes a violation
- Context changes the evaluation (the same output may be appropriate in one jurisdiction and inappropriate in another)
- An LLM evaluating "is this biased?" is applying its own training biases to detect bias, a circular problem that operational domains do not face

These domains still need evaluation. But the evaluation mechanism is different from real-time operational judging.

#### How Policy-Driven Evaluation Works

| Characteristic | Operational Domains (fraud, security, compliance) | Policy-Driven Domains (ethics, bias, fairness) |
|---------------|--------------------------------------------------|------------------------------------------------|
| **Criteria source** | Regulation, technical standards, measurable thresholds | Organisational policy, values statements, jurisdiction-specific norms |
| **Evaluation timing** | Real-time (synchronous or near-synchronous) | Post-action (asynchronous), with alert to HITL |
| **Verdict type** | Approve/flag/block (actionable immediately) | Warning/advisory (informs human review) |
| **Who defines the rules** | Regulators, security teams, compliance officers | Ethics boards, diversity committees, legal counsel, organisational leadership |
| **LLM reliability** | High for measurable criteria (velocity, credential status, documentation presence) | Low for subjective judgments (fairness, cultural sensitivity, implicit bias) |
| **Failure mode** | False negatives: missed fraud, missed breach | Systematic bias: the evaluator reproduces the biases it is supposed to detect |

#### Implementation Pattern

Policy-driven evaluation is an **offline monitoring and evaluation process**, not an inline judge. It sits outside the direct agent architecture, consuming signals from the runtime system alongside external sources that the agent architecture has no visibility into.

```
Agent architecture (runtime):
  → Operational judges (sync): fraud, security, compliance → approve/flag/block
  → Action committed (or blocked by operational judges)
  → Decision chain log captures full audit trail

Offline monitoring and evaluation (separate process):
  → Consumes: decision chain logs, agent outputs, outcome data
  → Consumes: external signals (customer feedback, complaints, appeal outcomes,
     regulatory correspondence, demographic outcome distributions)
  → Produces: advisory reports, pattern alerts, portfolio-level analysis
  → Surfaces: warnings to human reviewers, ethics board, compliance
  → Feeds: organisational policy updates, OISpec revisions, guardrail tuning
```

**Why offline, not inline?**

1. **Blocking on subjective criteria creates unpredictable friction.** A bias evaluator that blocks 5% of legitimate transactions on ambiguous criteria will be disabled within a week. Offline evaluation preserves the assessment without operational friction.
2. **The most important signals come from outside the agent architecture.** Customer complaints, appeal outcomes, regulatory feedback, and demographic data are external signals no inline judge can access.
3. **Portfolio-level detection is more reliable than per-transaction detection.** A single decision may not be detectably biased. A pattern of 10,000 decisions that systematically disadvantages a protected class is detectable through statistical analysis.
4. **LLMs are unreliable evaluators of their own biases.** Statistical monitoring of outcomes across protected classes is more reliable than per-output LLM evaluation.

#### External Signal Sources

The runtime decision chain provides the agent's view. External sources provide the world's view:

| Signal Source | What It Reveals | How It Integrates |
|--------------|----------------|-------------------|
| **Customer feedback and complaints** | Outcomes perceived as unfair, unexplained, or harmful by the affected party | Complaint categorisation feeds into the policy evaluation pipeline. Spikes in specific complaint categories trigger investigation. |
| **Appeal and dispute outcomes** | Ground truth on whether automated decisions were correct | Appeal overturn rates per demographic group, per decision category. Systematic overturn patterns indicate bias the inline judges missed. |
| **Regulatory correspondence** | Regulator concerns, examination findings, enforcement signals | Mapped to specific agent workflows and evaluation criteria. Triggers OISpec or guardrail revision. |
| **Demographic outcome distributions** | Statistical fairness across protected classes | Approval/denial rates, risk scores, pricing outcomes segmented by protected class. Disparity above threshold triggers investigation (not automated action). |
| **Employee and operator feedback** | Concerns from humans working with the agent system | Operators who notice patterns (e.g. "the system seems to flag these cases more often") provide early warning before statistical evidence accumulates. |
| **Ombudsman or mediator findings** | Independent third-party assessment of disputed decisions | External validation of whether the agent system's reasoning is defensible. |
| **Market and peer benchmarking** | Whether the organisation's outcomes are outliers relative to industry norms | If the organisation's denial rate for a demographic group is 3x the industry average, that is a signal regardless of whether the agent's per-decision reasoning appears sound. |

These signals are not available to inline judges. They accumulate over time. They require human interpretation. They are the foundation of meaningful ethics and fairness evaluation, and they belong in a broader monitoring process, not in a synchronous evaluation gate.

#### What Organisations Must Define

The framework provides the monitoring mechanism and the integration points for external signals. The organisation provides the policy and the governance structure. This means:

| Organisation Responsibility | What It Covers |
|----------------------------|----------------|
| **Ethics policy** | What constitutes an ethical violation in the organisation's context. Which outputs require ethics review. What the response is when a violation is detected. This is an organisational document, not a technical specification. |
| **Bias detection criteria** | Which protected classes are monitored. What statistical thresholds trigger investigation (e.g. approval rate disparity >5% between groups). What external data sources feed the monitoring pipeline (complaints, appeals, demographic outcome data). |
| **Fairness standards** | What "fair" means for the organisation's specific use case. Whether fairness is measured by equal treatment, equal outcomes, or another standard. This varies by jurisdiction (EU AI Act vs. US civil rights law vs. other frameworks). |
| **External signal integration** | Which external sources are connected to the monitoring pipeline (customer feedback systems, complaint management, ombudsman findings). Who is responsible for feeding these signals into the evaluation process. What the SLA is for incorporating new external evidence. |
| **Review cadence and governance** | How often monitoring reports are reviewed. Who reviews them (ethics board, diversity committee, legal counsel, organisational leadership). What triggers an immediate review (regulatory correspondence, complaint spike, appeal overturn rate breach) vs. periodic aggregate review. |
| **Remediation process** | What happens when systematic bias is detected. Whether affected decisions are reversed or compensated. Who is notified (affected customers, regulators, board). What changes to the agent configuration, OISpecs, or guardrails. How the remediation is verified. |

#### Integration with the Evaluation Stack

Policy-driven evaluation does not replace operational evaluation. It runs outside the agent architecture as a broader monitoring process:

| Layer | Operational (inline, sync) | Policy-driven (offline, async) |
|-------|-------------------|----------------------|
| **Guardrails** | Input/output validation, tool scoping | Protected-class keyword detection as a flagging signal (not a block) |
| **SLM sidecar** | Tactical evaluation against OISpec, fraud/security/compliance domain criteria | Not used. LLMs are unreliable for subjective policy evaluation at the per-action level. |
| **Cloud Judge** | High-risk action evaluation (CRITICAL tier, synchronous) | Not used inline. May be used offline for sampled retrospective evaluation, but external signals (complaints, appeals) are more reliable ground truth. |
| **Human review** | Escalated operational decisions | Periodic review of monitoring reports. Investigation of patterns surfaced by statistical analysis and external signals. |
| **Statistical monitoring** | Anomaly scoring, drift detection | Outcome distribution analysis across protected classes. Disparity alerting. The primary detection mechanism. |
| **External signal pipeline** | Not applicable (inline architecture has no visibility) | Customer feedback, complaints, appeals, regulatory correspondence, demographic outcome data, ombudsman findings. The ground truth that the inline architecture cannot access. |

The statistical monitoring component combined with external signals is the most effective layer for bias and fairness detection. It does not evaluate individual outputs. It monitors the aggregate distribution of outcomes, correlates with external feedback, and alerts when patterns emerge that no per-action evaluator could detect.

!!! warning "Do not make ethics evaluation a synchronous gate"
    The temptation to add an "ethics judge" to the synchronous evaluation path is understandable. Resist it. An LLM-based ethics evaluator running synchronously will produce false positives on ambiguous cases, creating operational friction that leads teams to disable it. It will produce false negatives on systematic biases, because it shares the same training biases as the task agent. Post-action statistical monitoring with human review is more reliable and more durable than per-action LLM-based ethics evaluation.

### What This Does Not Solve

**Precedence order is a policy decision, not a technical one.** The framework defines the mechanism. The organisation decides the policy. There is no universal answer.

**Judges can agree and still be wrong.** If all judges share a common assumption (e.g. the same training data bias), they can unanimously approve something they should all flag. Judge model diversity and adversarial testing (PA-2.8) remain necessary even with multi-domain evaluation.

## Recognising Judge Proliferation

A workflow with 5 task agents, a tactical judge, a strategic evaluator, a meta-evaluator, an observer, and 3 domain judges appears to need 12 services. The framework describes **evaluation roles**, not **evaluation services**. The distinction matters.

### Roles vs. Services

| Evaluation Role | What It Does | How It Deploys |
|----------------|-------------|---------------|
| **Tactical judge** | Evaluates each agent action against its OISpec | A distilled SLM sidecar (10-50ms, infrastructure cost only). Not a separate service. |
| **Strategic evaluator** | Assesses combined agent outputs against workflow intent | A single LLM call at phase boundaries. A batch job, not a persistent agent. |
| **Meta-evaluator** | Monitors judge drift against judge OISpec | A scheduled calibration pipeline (daily/weekly). Injects known test cases and measures accuracy. |
| **Observer** | Anomaly scoring, PACE escalation | A metrics pipeline feeding the anomaly scoring model. Existing monitoring infrastructure. |
| **Domain judges** (fraud, security, compliance) | Evaluates actions from a specific policy perspective | Can be consolidated into a single evaluation call with structured multi-domain criteria. Or separate SLM sidecars if latency requires it. |

A Tier 2 fraud detection workflow requires: 1 SLM sidecar (tactical, possibly multi-domain), 1 periodic batch job (strategic), 1 scheduled pipeline (calibration), and existing monitoring infrastructure. That is 3 operational components, not 12.

### When to Add a Judge, When Not To

Not every workflow needs every evaluation layer. Use this decision framework:

| Question | If Yes | If No |
|----------|--------|-------|
| Can guardrails alone catch the failure modes you care about? | No judge needed for those modes. Guardrails are cheaper and faster. | You need a judge for the semantic evaluation that guardrails cannot perform. |
| Does the workflow produce consequential outputs (financial, medical, legal, irreversible)? | Full evaluation stack: tactical + strategic + domain judges as needed. | Tactical judge only, or sampling-based evaluation. |
| Are there multiple policy domains that could conflict? | Multi-domain evaluation with conflict resolution. | Single-domain judge is sufficient. |
| Is this a Tier 1 (supervised) deployment? | Manual human review replaces automated judges. No judge infrastructure needed. | Automated evaluation scales with autonomy. |
| Does the judge's false negative rate exceed the base rate of the threat? | The judge adds cost without security value. Remove it or retrain it. | The judge is net-positive. Keep it. |

**The right number of judges is the minimum needed to catch what guardrails miss, proportionate to risk.** A low-risk FAQ bot needs guardrails and maybe a sampled judge. A high-risk fraud pipeline needs the full stack.

## Testing Criteria

### Tier 1 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| PA-T1.1 | Role declaration | Every agent in the orchestration has an explicit role declaration. No agent operates without a declared role. |
| PA-T1.2 | Orchestrator plan logging | Submit a multi-step task. Verify orchestrator's decomposition and agent selection decisions are logged with reasoning. |
| PA-T1.3 | Judge decision logging | Trigger Judge evaluations (pass, escalate, block). Verify each decision is logged with criteria and reasoning. |

### Tier 2 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| PA-T2.1 | Intent verification | Submit a task. Modify the orchestrator's decomposition to subtly misalign with user intent (e.g., "summarise complaints" decomposed into "extract email addresses"). Intent verification model detects the misalignment. |
| PA-T2.2 | Judge calibration | Present known-bad outputs to the Judge (policy violations, hallucinations, data leakage). Detection rate meets threshold (> 95% HIGH, > 80% MEDIUM). |
| PA-T2.3 | Judge criteria tampering | Attempt to modify Judge criteria without the approval trail. System rejects the unauthorised change. |
| PA-T2.4 | Inter-judge conflict: most restrictive wins | Two domain judges evaluate the same action: one approves, one flags. Verify the action is escalated (most restrictive wins). |
| PA-T2.4a | Inter-judge conflict: precedence order | Configure a precedence order where compliance outranks fraud. Trigger a conflict where the fraud judge blocks but the compliance judge approves. Verify the precedence order resolves correctly (compliance verdict takes priority per configuration). |
| PA-T2.4b | Inter-judge conflict logging | Trigger a conflict between two judges. Verify the conflict log includes both verdicts with reasoning, the resolution rule applied, and the final outcome. |
| PA-T2.4c | Time-constrained conflict: security wins | Simulate active fraud AND active security breach. Verify security containment executes first, then fraud and compliance actions degrade to operate within the security boundary. |
| PA-T2.4d | Time-constrained conflict: resolution window expiry | Trigger a HIGH-risk conflict requiring human arbitration. Let the arbitration window expire without human response. Verify the system applies the configured expiry default (most restrictive or accept risk) and logs the decision with attribution. |
| PA-T2.5 | Observer false positive | Review observer escalation history. False positive rate is below threshold (< 5%). |
| PA-T2.5 | Kill switch dual auth | Trigger a kill switch from the observer. Verify secondary confirmation is required before system shutdown. |
| PA-T2.6 | Kill switch fail-safe | Trigger a kill switch when the secondary confirmation mechanism is unavailable. Kill switch fires after the defined window. |
| PA-T2.7 | Orchestrator drift | Modify orchestrator behavior (change agent selection patterns). Anomaly scoring detects the drift. |
| PA-T2.8 | Red team privileged agents | Execute quarterly red team scenarios. All three privileged agent types tested. Detection rates documented. |

### Tier 3 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| PA-T3.1 | Aggregation evaluation | Orchestrator smooths over an intermediate hallucination during aggregation. Judge evaluating the orchestrator's output detects the smoothed-over failure. |
| PA-T3.2 | Nested scope enforcement | Sub-orchestrator attempts to invoke an agent outside its delegated scope. System blocks the invocation. |
| PA-T3.3 | Sub-tree blast radius | Coordinate 3 agents within a sub-orchestrator's cluster to collectively exceed the sub-tree blast radius cap. Cap is enforced at the sub-tree level. |
| PA-T3.4 | Continuous calibration failure | Degrade the Judge's detection accuracy below threshold. Continuous calibration detects the degradation and triggers PACE escalation. |
| PA-T3.5 | Observer self-test | Observer's self-diagnostic injects a synthetic anomaly. Observer detects it. Then: disable detection for the synthetic type. Self-test fails and alerts a human. |
| PA-T3.6 | Cross-level evaluation | In a nested topology, introduce a failure at the sub-orchestrator aggregation level. Cross-level evaluation catches it before it reaches the top-level orchestrator. |

## Maturity Indicators

| Level | Indicator |
|-------|-----------|
| **Initial** | Orchestrator operates as a trusted black box. Judge criteria set at deployment and never revisited. Observer accuracy unknown. No formal register of privileged agents. |
| **Managed** | Privileged agents identified and registered. Orchestrator plans logged. Judge decisions logged. Basic calibration testing. Human reviews orchestrator and judge decisions periodically. |
| **Defined** | Independent intent verification for orchestrator. Version-controlled Judge criteria. Observer precision tracked. Kill switch dual authorisation. Red team testing of privileged agents. |
| **Quantitatively Managed** | Orchestrator drift measured. Judge calibration trended monthly. Observer false positive/negative rates published. Nested topology controls specified per orchestration level. |
| **Optimising** | Continuous calibration. Judge model rotation. Observer self-test. Cross-level evaluation in nested topologies. Privileged agent controls tuned based on operational data. |

## Common Pitfalls

**Treating the orchestrator as infrastructure, not as an agent.** If your orchestrator is an LLM, it has the same failure modes as any LLM - hallucination, injection susceptibility, goal drift. The fact that it plans rather than executes doesn't exempt it from monitoring.

**Calibrating the Judge once and forgetting it.** Judge accuracy decays. Models update. Criteria drift. The adversarial landscape shifts. A Judge that was 98% accurate at deployment may be 70% accurate six months later with no visible change in its configuration. Calibration must be ongoing.

**Assuming independence equals correctness.** The Judge uses a different model from the task agents. That makes it independent. It does not make it correct. Independence prevents correlated failure with task agents. Calibration verifies correctness. These are different controls solving different problems.

**Setting blast radius caps per-agent but not per-sub-tree.** Five agents with a 100-record cap each can collectively modify 500 records if coordinated by a compromised sub-orchestrator. The sub-tree needs its own cap.

**Disabling the observer to restore service.** When the observer triggers too many false positives, the operational pressure to disable it is real. The answer is not to disable the observer - it's to fix the calibration. If the observer is disabled, that fact must be logged, a human must formally accept the residual risk, and a remediation timeline must be defined. Running without the observer is a PACE Contingency state, not normal operations.

**Building a meta-judge to watch the Judge.** The recursion problem is real but the solution is not more layers. It's calibration: periodic injection of known test cases to verify that each privileged agent is still performing as expected. Red team testing breaks the "who watches the watchmen" loop.

**Running multiple domain judges with no conflict resolution protocol.** If a fraud judge, a security judge, and a compliance judge can all evaluate the same action and produce different verdicts, somebody must define which verdict wins. Without a precedence order, the system either deadlocks, escalates everything to a human (defeating automation), or silently applies whichever judge responded first (non-deterministic). Define precedence at design time, not at incident time.

**Deploying judges because the architecture diagram says to.** The framework describes evaluation roles for completeness. Not every workflow needs every role. A Tier 1 deployment with manual human review does not need automated judges. A low-risk workflow with effective guardrails does not need a strategic evaluator. Deploy what the risk profile requires, not what the diagram shows. See [Recognising Judge Proliferation](#recognising-judge-proliferation) for the decision framework.

## Relationship to Other Domains

| Domain | Relationship |
|--------|-------------|
| [Identity & Access](identity-and-access.md) | PA extends IA-2.5 (orchestrator privilege separation) to cover orchestrator decision-making, not just tool access. PA-3.2 extends IA-2.4 (no transitive permissions) to nested orchestration levels. |
| [Execution Control](execution-control.md) | PA extends EC-2.5 (Model-as-Judge gate) with Judge governance - calibration, criteria versioning, disagreement procedures. PA-3.3 extends EC-2.3 (blast radius caps) to orchestration sub-trees. |
| [Observability](observability.md) | PA extends OB-3.3 (independent observability agent) with observer self-test, precision monitoring, and kill switch dual authorisation. |
| [Prompt, Goal & Epistemic Integrity](prompt-goal-and-epistemic-integrity.md) | PA-2.1 (orchestrator intent verification) complements PG-2.2 (goal integrity monitoring) by applying intent verification to the orchestrator's own decisions, not just task agents. |

