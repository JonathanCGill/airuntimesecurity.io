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

**Orchestrators influence outcomes through decisions, not tools.** A compromised orchestrator doesn't need tool access to cause harm. It causes harm through task decomposition, agent selection, and result interpretation. Existing controls (IA-2.5, tool scoping) don't address this class of threat because the orchestrator's power is in planning, not execution.

**Evaluators are single points of trust.** The Model-as-Judge approves or blocks every task agent output. If Judge criteria drift, or the Judge model is compromised, Layer 2 collapses silently - every output passes because the standard has shifted. The system reports healthy while the controls are effectively disabled.

**Observers with kill switch authority can be weaponised.** An over-sensitive observer repeatedly triggers emergency shutdowns, degrading the system into permanent contingency. Operators disable it to restore service. The system now runs without its safety net - and nobody formally accepted that risk.

**Nested orchestration multiplies these risks.** In hierarchical topologies, a compromised sub-orchestrator affects its entire agent cluster. Per-agent blast radius caps don't contain aggregate harm from a coordinated sub-tree.

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
| **PA-2.4** Judge disagreement protocol | When multiple validators disagree (EC-3.3), a defined resolution procedure activates | Procedure defines: who arbitrates, within what timeframe, with what evidence, and how the resolution is documented. Default: human escalation within 15 minutes. |
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
| PA-T2.4 | Observer false positive | Review observer escalation history. False positive rate is below threshold (< 5%). |
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

**Building a meta-judge to watch the Judge.** The recursion problem is real but the solution is not more layers. It's calibration - periodic injection of known test cases to verify that each privileged agent is still performing as expected. Red team testing breaks the "who watches the watchmen" loop.

## Relationship to Other Domains

| Domain | Relationship |
|--------|-------------|
| [Identity & Access](identity-and-access.md) | PA extends IA-2.5 (orchestrator privilege separation) to cover orchestrator decision-making, not just tool access. PA-3.2 extends IA-2.4 (no transitive permissions) to nested orchestration levels. |
| [Execution Control](execution-control.md) | PA extends EC-2.5 (Model-as-Judge gate) with Judge governance - calibration, criteria versioning, disagreement procedures. PA-3.3 extends EC-2.3 (blast radius caps) to orchestration sub-trees. |
| [Observability](observability.md) | PA extends OB-3.3 (independent observability agent) with observer self-test, precision monitoring, and kill switch dual authorisation. |
| [Prompt, Goal & Epistemic Integrity](prompt-goal-and-epistemic-integrity.md) | PA-2.1 (orchestrator intent verification) complements PG-2.2 (goal integrity monitoring) by applying intent verification to the orchestrator's own decisions, not just task agents. |

