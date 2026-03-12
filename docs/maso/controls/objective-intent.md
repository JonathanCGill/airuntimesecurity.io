---
description: "MASO Objective Intent — developer-declared intent specifications that define what agents should accomplish, within what parameters, enabling judges and evaluation agents to assess real behavioral compliance at both tactical and strategic levels."
---

# MASO Control Domain: Objective Intent

> Part of the [MASO Framework](../README.md) · Control Specifications
> Extends: [Prompt, Goal & Epistemic Integrity](prompt-goal-and-epistemic-integrity.md) · [Observability](observability.md) · [Privileged Agent Governance](privileged-agent-governance.md)
> Cross-references: [The Intent Layer](../../insights/the-intent-layer.md) · [Judge Assurance](../../core/judge-assurance.md)

## Principle

Every agent in a multi-agent system must operate against a **declared Objective Intent** — a structured specification of what the developer expects that agent to accomplish and within what parameters. These intents are not internal documentation. They are **machine-readable contracts** consumed by judges, evaluation agents, and the observability layer to assess whether actual agent behavior aligns with declared purpose.

Without declared intent, the framework catches faults where it can — injection, tool misuse, data leakage — but cannot evaluate whether the system is doing what it was designed to do. Objective Intent is the bridge from **fault detection** to **behavioral assurance**: from catching things that go wrong to verifying that things go right.

## The Gap This Fills

The existing MASO framework provides:

- **Guardrails** that block known-bad patterns (mechanical)
- **LLM-as-Judge** that evaluates quality and safety (semantic, but reactive)
- **Observability** that detects drift from behavioral baselines (statistical)
- **The Intent Layer** that evaluates workflow-level outcomes post-execution (strategic, but coarse)

What is missing is a **formal declaration of what each agent, each judge, and the overall orchestration is supposed to achieve** — written by the developer, versioned, and used as the reference standard for continuous behavioral evaluation.

Without this:

- Judges evaluate against generic criteria, not the specific purpose the developer intended.
- Drift detection compares against statistical baselines, not declared objectives.
- Post-execution evaluation can assess coherence but not correctness relative to design intent.
- Combined agent actions produce emergent outcomes that nobody specified and nobody is evaluating against.

**Objective Intent makes the developer's expectations explicit, versioned, and evaluable.**

## Architecture

![Objective Intent Evaluation Architecture](../../images/objective-intent-architecture.svg)

The architecture operates at two levels:

### Tactical: Single-Agent Intent Compliance

Each agent has a declared Objective Intent Specification (OISpec). A **tactical judge** evaluates that individual agent's actions and outputs against its OISpec. This catches:

- An agent operating outside its declared parameters
- An agent pursuing a goal it was not assigned
- An agent exceeding its declared authority or scope
- An agent producing outputs inconsistent with its stated purpose

### Strategic: Aggregated Intent Compliance

The orchestration has a declared **Workflow Intent** — the combined objective across all agents. A **strategic evaluation agent** assesses whether the aggregate behavior of all agents satisfies the workflow intent. This catches:

- Individual agents all complying with their own intents but producing a collectively wrong outcome
- Emergent behavior that no single agent's intent anticipated
- Intent gaps — scenarios where no agent's OISpec covers a critical requirement
- Conflicting intents between agents that produce contradictory actions

### Judge Intent Monitoring

Judges themselves operate against declared intents. A judge whose behavior drifts from its declared evaluation criteria is as dangerous as a task agent that drifts from its operational intent. Judge intents specify:

- What the judge is evaluating (scope)
- What criteria it applies (standards)
- What actions it takes on findings (disposition)
- What it does NOT evaluate (explicit exclusions)

Judge intent compliance is monitored by a separate evaluator — not the judge itself and not the agents it evaluates.

## Objective Intent Specification (OISpec)

An OISpec is a structured, version-controlled document attached to every agent, judge, and workflow. It is not free-form prose — it is a typed schema that evaluation agents can programmatically consume.

### Agent OISpec

```json
{
  "oisspec_version": "1.0",
  "oisspec_id": "uuid",
  "agent_id": "agent-analyst-01",
  "agent_role": "task | orchestrator | evaluator | observer",
  "created_by": "developer-id",
  "created_at": "ISO-8601",
  "version": 3,
  "version_history": ["hash-v1", "hash-v2", "hash-v3"],

  "objective": {
    "goal": "Analyse market data and produce a risk score for the specified portfolio",
    "success_criteria": [
      "Risk score is traceable to specific data points",
      "All data sources are from the last 30 days",
      "Uncertainty above 0.3 is explicitly flagged"
    ],
    "failure_criteria": [
      "Risk score produced without citing data sources",
      "Recommendation to trade exceeding $50,000 exposure",
      "Uncertainty stripped from downstream outputs"
    ]
  },

  "parameters": {
    "permitted_tools": ["market-data-api", "news-sentiment-api"],
    "prohibited_actions": ["execute-trade", "send-email", "modify-portfolio"],
    "data_scope": "Portfolio X only. No cross-portfolio access.",
    "time_boundary": "Last 30 calendar days from execution time",
    "output_constraints": {
      "max_confidence_without_source": 0.5,
      "required_fields": ["risk_score", "data_sources", "uncertainty"],
      "prohibited_content": ["trading instructions", "personal advice"]
    }
  },

  "authority": {
    "can_delegate": false,
    "max_delegation_depth": 0,
    "can_create_agents": false,
    "can_modify_workflow": false
  },

  "risk_classification": "high",
  "evaluation_frequency": "every_action | per_phase | post_execution",
  "oisspec_hash": "sha256 of this specification"
}
```

### Judge OISpec

```json
{
  "oisspec_version": "1.0",
  "oisspec_id": "uuid",
  "agent_id": "judge-quality-01",
  "agent_role": "evaluator",
  "created_by": "developer-id",

  "objective": {
    "goal": "Evaluate task agent outputs for factual accuracy, policy compliance, and intent alignment",
    "evaluation_scope": ["agent-analyst-01", "agent-writer-01"],
    "evaluation_criteria": [
      "Output satisfies the evaluated agent's declared OISpec",
      "Factual claims are traceable to cited sources",
      "Policy constraints from the agent's OISpec are respected",
      "Uncertainty signals are preserved or increased, never decreased"
    ]
  },

  "parameters": {
    "permitted_actions": ["approve", "flag", "block", "escalate"],
    "prohibited_actions": ["modify_agent_output", "invoke_tools", "send_external"],
    "evaluation_model": "different-provider-model-id",
    "max_evaluation_latency_ms": 5000,
    "false_positive_target": 0.05,
    "false_negative_target": 0.02
  },

  "authority": {
    "can_block_output": true,
    "can_trigger_pace_escalation": true,
    "can_terminate_agent": false,
    "can_modify_agent_oisspec": false
  },

  "monitoring": {
    "calibration_frequency": "daily",
    "monitored_by": "judge-meta-evaluator-01",
    "drift_threshold": 0.15
  }
}
```

### Workflow OISpec

```json
{
  "oisspec_version": "1.0",
  "workflow_id": "uuid",
  "workflow_name": "Portfolio Risk Assessment",
  "created_by": "developer-id",

  "objective": {
    "goal": "Produce a risk assessment for portfolio X using current market data and news sentiment, with a recommendation",
    "aggregate_success_criteria": [
      "Final recommendation is traceable through all intermediate agent outputs to primary data sources",
      "No agent operated outside its declared OISpec parameters",
      "Combined agent outputs are internally consistent",
      "All uncertainty signals from intermediate agents are preserved in the final output"
    ],
    "aggregate_failure_criteria": [
      "Final output contradicts intermediate analysis without explanation",
      "Two or more agents produced conflicting assessments that were silently resolved",
      "Uncertainty was stripped at any handoff point",
      "Any agent exceeded its declared authority"
    ]
  },

  "agent_intents": [
    "oisspec-id-analyst-01",
    "oisspec-id-sentiment-01",
    "oisspec-id-combiner-01",
    "oisspec-id-writer-01"
  ],

  "judge_intents": [
    "oisspec-id-judge-quality-01",
    "oisspec-id-judge-compliance-01"
  ],

  "evaluation": {
    "tactical_evaluation": "per_agent_per_action",
    "strategic_evaluation": "per_phase_and_post_execution",
    "intent_coverage_check": true
  }
}
```

## How Evaluation Works

### Level 1: Tactical — Single Agent Against Its OISpec

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   Agent Action/      │────▶│  Tactical Judge   │────▶│  Verdict:           │
│   Output             │     │                  │     │  - OISpec compliant? │
│                     │     │  Evaluates against│     │  - Parameter breach? │
│                     │     │  agent's OISpec   │     │  - Authority exceed? │
└─────────────────────┘     └──────────────────┘     └─────────────────────┘
```

The tactical judge answers: **Did this agent do what it was supposed to do, within the parameters it was given?**

This is the monitoring of one — the individual agent against its declared contract.

### Level 2: Strategic — All Agents Against the Workflow OISpec

```
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│  Aggregate outputs   │────▶│  Strategic Evaluator  │────▶│  Verdict:           │
│  + audit trail       │     │                      │     │  - Workflow intent   │
│  + all agent OISpecs │     │  Evaluates against   │     │    satisfied?        │
│  + all judge verdicts│     │  workflow OISpec      │     │  - Emergent issues?  │
│                     │     │  + aggregated intents │     │  - Intent gaps?      │
└─────────────────────┘     └──────────────────────┘     └─────────────────────┘
```

The strategic evaluator answers: **Did the system as a whole achieve what was intended, and did the agents collectively behave as designed?**

This is the monitoring of the whole — the fleet-level behavioral assessment against the aggregated intent.

### Level 3: Judge Against Its OISpec

```
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│  Judge decisions     │────▶│  Judge Meta-Evaluator │────▶│  Verdict:           │
│  + judge OISpec      │     │                      │     │  - Criteria drift?   │
│  + calibration data  │     │  Evaluates judge     │     │  - Scope creep?      │
│                     │     │  against its OISpec   │     │  - Accuracy decay?   │
└─────────────────────┘     └──────────────────────┘     └─────────────────────┘
```

The meta-evaluator answers: **Is the judge still doing what it was configured to do, or has it drifted?**

This closes the "who watches the watchmen" loop — not through infinite recursion, but through explicit intent contracts at every level.

## Diagram: Intent Evaluation Hierarchy

```
                    ┌─────────────────────────────────┐
                    │     Workflow Objective Intent     │
                    │   (Strategic — the whole)        │
                    │                                  │
                    │  "Produce accurate risk          │
                    │   assessment for portfolio X"    │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────┴──────────────────┐
                    │    Strategic Evaluation Agent     │
                    │  Assesses aggregate compliance    │
                    │  against workflow OISpec          │
                    └──────────────┬──────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
   ┌──────────▼─────────┐  ┌──────▼──────────┐  ┌─────▼────────────┐
   │  Agent A OISpec     │  │ Agent B OISpec  │  │ Agent C OISpec   │
   │  "Retrieve market   │  │ "Analyse news   │  │ "Combine into    │
   │   data for last     │  │  sentiment for  │  │  risk score with │
   │   30 days"          │  │  portfolio X"   │  │  full tracing"   │
   └──────────┬──────────┘  └──────┬──────────┘  └─────┬────────────┘
              │                    │                    │
   ┌──────────▼─────────┐  ┌──────▼──────────┐  ┌─────▼────────────┐
   │  Tactical Judge     │  │ Tactical Judge  │  │ Tactical Judge   │
   │  (per-agent OISpec  │  │ (per-agent      │  │ (per-agent       │
   │   compliance)       │  │  OISpec check)  │  │  OISpec check)   │
   └─────────────────────┘  └─────────────────┘  └──────────────────┘
              │                    │                    │
              └────────────────────┼────────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │    Judge Meta-Evaluator          │
                    │  "Are the tactical judges still  │
                    │   evaluating per their OISpecs?" │
                    └─────────────────────────────────┘
```

**Key insight:** Intent flows downward (decomposed from workflow to agent). Evaluation flows upward (aggregated from agent to workflow). Judge monitoring is lateral — independent of both flows.

## Controls by Tier

### Tier 1 — Supervised

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **OI-1.1** Agent OISpec declaration | Every agent deployed in the orchestration must have a declared OISpec | OISpec is authored by the developer at design time, not generated by the agent. Stored as a versioned artifact alongside agent configuration. |
| **OI-1.2** Workflow OISpec declaration | Every multi-agent workflow must have a declared workflow-level OISpec | The workflow OISpec references all participating agent OISpecs and defines aggregate success/failure criteria. |
| **OI-1.3** OISpec immutability | OISpecs are read-only during execution; changes require human authorisation and create a new version | Prevents agents from modifying their own intent specifications at runtime. |
| **OI-1.4** Manual intent review | Human reviewer compares agent outputs against the agent's OISpec weekly | Builds the baseline for automated evaluation at Tier 2. |
| **OI-1.5** Intent coverage check | Before workflow execution, verify that every declared success criterion in the workflow OISpec is covered by at least one agent's OISpec | Identifies intent gaps before execution, not after. |

**What you're building at Tier 1:** Every agent has a declared purpose. Every workflow has a declared objective. Humans verify compliance manually. Intent gaps are caught before execution.

### Tier 2 — Managed

All Tier 1 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **OI-2.1** Automated tactical evaluation | Tactical judge evaluates each agent's actions against its OISpec at the frequency defined in the OISpec | Evaluation frequency scales with risk: HIGH/CRITICAL = every action; MEDIUM = per phase; LOW = post-execution. |
| **OI-2.2** Automated strategic evaluation | Strategic evaluation agent assesses aggregate outputs against workflow OISpec at phase boundaries and post-execution | Receives: workflow OISpec, all agent OISpecs, agent outputs, tactical judge verdicts, and audit trail summary. |
| **OI-2.3** Judge OISpec declaration | Every judge must have a declared OISpec specifying its evaluation scope, criteria, and permitted actions | Judge OISpecs are version-controlled with the same rigour as agent OISpecs. |
| **OI-2.4** Judge intent monitoring | Judge behavior is evaluated against its OISpec by an independent meta-evaluator | The meta-evaluator is not the judge and is not any agent the judge evaluates. |
| **OI-2.5** OISpec violation escalation | OISpec violations detected by tactical or strategic evaluators trigger defined escalation paths | HIGH risk: immediate human notification. CRITICAL: output quarantined until human review. |
| **OI-2.6** Intent alignment scoring | Each agent receives a continuous intent alignment score based on tactical evaluation verdicts | Score feeds into the anomaly scoring model (OB-2.2) as an additional signal. Trending enables detection of gradual intent drift. |
| **OI-2.7** Combined action evaluation | Strategic evaluator specifically checks for emergent outcomes that comply with individual agent OISpecs but violate the workflow OISpec | This is the control that catches "every agent did its job, but the result is wrong." |

**What you're building at Tier 2:** Automated evaluation at both tactical (per-agent) and strategic (per-workflow) levels. Judges are themselves monitored against declared intents. Combined actions are evaluated for emergent violations.

### Tier 3 — Autonomous

All Tier 2 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **OI-3.1** Continuous intent compliance | Tactical evaluation runs on every agent action in real-time, with results available within the same decision cycle | For autonomous operation, intent compliance must be synchronous enough to prevent non-compliant actions from propagating. |
| **OI-3.2** Predictive intent analysis | Strategic evaluator projects whether the current trajectory of agent actions will satisfy the workflow OISpec at completion | Catches intent drift before it produces non-compliant outputs. Uses intermediate results and tactical evaluation trends. |
| **OI-3.3** Cross-workflow intent learning | Patterns from strategic evaluation across many workflows feed into OISpec template improvement | If the strategic evaluator repeatedly flags the same type of emergent failure, the OISpec template is updated to require coverage of that failure mode. |
| **OI-3.4** Judge rotation with intent continuity | When judge models are rotated (PA-3.4), the replacement judge is validated against the same OISpec before assuming the role | Ensures judge rotation doesn't silently change evaluation criteria. |
| **OI-3.5** Adversarial intent testing | Red team exercises include attempts to satisfy the letter of an OISpec while violating its spirit | Findings feed into OISpec specification improvements — making success and failure criteria more precise. |
| **OI-3.6** Intent decomposition validation | When an orchestrator decomposes a workflow OISpec into agent OISpecs, an independent evaluator verifies the decomposition is faithful and complete | Prevents goal subversion through malicious or flawed intent decomposition. |

**What you're building at Tier 3:** Real-time intent compliance, predictive analysis, and continuous improvement of the intent specification process itself.

## Risk Classification and Evaluation Frequency

Objective Intent evaluation intensity scales with risk classification:

| Risk Tier | Tactical Evaluation | Strategic Evaluation | Judge Monitoring | OISpec Review |
|-----------|--------------------|--------------------|-----------------|---------------|
| **LOW** | Post-execution | Post-execution | Monthly calibration | Quarterly |
| **MEDIUM** | Per phase | Post-execution | Monthly calibration | Monthly |
| **HIGH** | Every action | Per phase + post-execution | Weekly calibration | Monthly |
| **CRITICAL** | Every action (synchronous) | Per phase + post-execution (output quarantined) | Daily calibration | On every OISpec change |

**HIGH and CRITICAL risk classifications are where Objective Intent matters most.** At these tiers, the cost of non-compliance with declared intent is material — financial loss, regulatory violation, patient harm, or irreversible action. The OISpec is the reference standard that makes compliance measurable.

## Relationship to Existing Controls

| Existing Control | How Objective Intent Extends It |
|-----------------|-------------------------------|
| **PG-1.3** Immutable task specification | OISpec is more granular — per-agent, per-judge, and per-workflow, with typed success/failure criteria |
| **PG-2.2** Goal integrity monitoring | OISpec provides the formal reference standard that goal integrity is measured against |
| **PA-2.1** Orchestrator intent verification | OISpec verification is continuous, not just at decomposition time |
| **PA-2.2** Judge calibration | Judge OISpecs make calibration criteria explicit and evaluable, not just accuracy targets |
| **OB-2.2** Anomaly scoring | Intent alignment score becomes an additional signal in the anomaly scoring vector |
| **The Intent Layer** (post-execution evaluation) | OISpec provides the structured "Intent Specification" that the post-execution judge evaluates against, now extended to every agent and every judge |

## What This Does Not Solve

**1. Intent is hard to write well.**

Specifying what an agent should do in sufficient detail for machine evaluation is non-trivial. Vague OISpecs ("produce good analysis") are unevaluable. Overly specific OISpecs ("respond with exactly these fields in this order") are brittle. The right level of specificity depends on the use case and risk tier.

**Mitigation:** Start with HIGH/CRITICAL risk workflows. Use the cross-workflow learning feedback loop (OI-3.3) to improve OISpec templates over time. Accept that for LOW risk, minimal OISpecs are appropriate.

**2. An agent can satisfy the letter of its OISpec while violating the spirit.**

An agent told "cite all sources" can cite sources that don't support the claim. An agent told "flag uncertainty above 0.3" can present everything at 0.29.

**Mitigation:** Adversarial intent testing (OI-3.5) probes for this. Strategic evaluation (OI-2.2) catches cases where individual compliance produces aggregate non-compliance. Failure criteria in the OISpec are as important as success criteria.

**3. The meta-evaluator can also drift.**

The judge meta-evaluator operates against its own OISpec. Who evaluates the meta-evaluator? At some point, the chain terminates in sampled human review (the same answer as PA and the Intent Layer).

**Mitigation:** Sampled human review of meta-evaluator verdicts. Calibration testing of the meta-evaluator. The recursion stops at humans, not at more agents.

**4. OISpec maintenance is an ongoing cost.**

As agents evolve, tools change, and requirements shift, OISpecs must be updated. Stale OISpecs produce false positives (flagging correct behavior that doesn't match outdated criteria) or false negatives (missing violations of updated requirements).

**Mitigation:** OISpec versioning with change tracking. Alerts when agent behavior consistently triggers evaluation but human reviewers override. This signal indicates the OISpec needs updating, not the agent.

## Testing Criteria

### Tier 1 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| OI-T1.1 | OISpec completeness | Every agent in the orchestration has a declared OISpec with all required fields populated. |
| OI-T1.2 | Workflow OISpec coverage | Intent coverage check confirms every workflow success criterion is covered by at least one agent's OISpec. |
| OI-T1.3 | OISpec immutability | Attempt to modify an OISpec during execution. Modification is rejected. |
| OI-T1.4 | Manual compliance review | Human reviewer identifies at least one agent action that would constitute an OISpec violation in a test scenario. |

### Tier 2 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| OI-T2.1 | Tactical evaluation accuracy | Present agent actions that violate the agent's OISpec. Tactical judge detection rate ≥ 90% for HIGH severity violations. |
| OI-T2.2 | Strategic evaluation — emergent failure | Individual agents comply with their OISpecs. Combined output violates the workflow OISpec. Strategic evaluator detects the violation. |
| OI-T2.3 | Judge intent monitoring | Shift judge evaluation criteria away from its OISpec. Meta-evaluator detects the drift within one calibration cycle. |
| OI-T2.4 | OISpec violation escalation | Trigger an OISpec violation at HIGH risk. Verify human is notified within the defined SLA. |
| OI-T2.5 | Combined action judge | Two agents each comply with their OISpecs individually. Judge evaluating combined actions flags the inconsistency. |

### Tier 3 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| OI-T3.1 | Real-time intent compliance | Agent action violates OISpec. Tactical evaluation detects it before the action propagates to the next agent. |
| OI-T3.2 | Predictive intent analysis | Halfway through a workflow, intermediate results indicate the workflow OISpec will not be satisfied. Strategic evaluator flags before completion. |
| OI-T3.3 | Adversarial intent satisfaction | Red team satisfies OISpec letter while violating spirit. Adversarial testing identifies the loophole. OISpec is updated. |
| OI-T3.4 | Intent decomposition validation | Orchestrator decomposes workflow OISpec into agent OISpecs. Independent evaluator detects when decomposition drops a success criterion. |

## Maturity Indicators

| Level | Indicator |
|-------|-----------|
| **Initial** | Agents deployed without declared intent. Goals implied by system prompts but not formally specified. No evaluation against stated objectives. |
| **Managed** | OISpecs declared for all agents and workflows. Manual review compares behavior against intent. Intent coverage checked before execution. |
| **Defined** | Automated tactical and strategic evaluation operational. Judges have declared OISpecs. Judge intent monitoring active. Intent alignment scoring feeds anomaly detection. |
| **Quantitatively Managed** | Tactical evaluation accuracy measured. Strategic evaluation false positive/negative rates tracked. Intent alignment scores trended. OISpec coverage metrics published. |
| **Optimising** | Real-time intent compliance. Predictive intent analysis. Cross-workflow learning improving OISpec templates. Adversarial intent testing refining specifications. Judge rotation validated against OISpecs. |

## Common Pitfalls

**Writing OISpecs after deployment, not before.** If the OISpec is written to match existing agent behavior rather than to declare intended behavior, it becomes a description, not a contract. OISpecs must be authored at design time and agents must be built to satisfy them.

**Declaring intent for task agents but not for judges.** A judge without a declared OISpec is a black box with authority. Its evaluation criteria are implicit, its scope is undefined, and its drift is undetectable. Judges need OISpecs as much as task agents do.

**Evaluating individual agents but not combined actions.** The most dangerous failures in multi-agent systems are emergent — they only appear when individually correct actions combine into collectively wrong outcomes. The strategic evaluation layer exists specifically to catch these.

**Treating OISpec compliance as binary.** Intent alignment is a spectrum. An agent at 95% compliance over 100 actions is different from an agent at 100% compliance over 10 actions. The intent alignment score (OI-2.6) must be continuous and trended, not just pass/fail.

**Assuming the OISpec captures everything that matters.** No specification is complete. OISpecs will always miss edge cases, novel scenarios, and failure modes nobody anticipated. This is why strategic evaluation, adversarial testing, and sampled human review exist — they catch what the specification doesn't cover.

**Building the meta-evaluation chain without a termination point.** The recursion of "who evaluates the evaluator" must stop somewhere. In this framework, it stops at sampled human review. The human doesn't evaluate every action — that doesn't scale. But they evaluate a sample, and that sample calibrates every automated evaluator in the chain.
