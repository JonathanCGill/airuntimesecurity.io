---
description: "Candidate MASO risk and controls — Token exhaustion as a dual failure path affecting both agent performance and detection capability."
status: "candidate"
---

# Candidate Risk: Token Exhaustion as a Dual Failure Path

> **Status:** Candidate for inclusion in the [MASO Emergent Risk Register](risk-register.md).
> Proposed for the **Operational Risks** category.

## Risk Summary

| Field | Value |
|-------|-------|
| **Proposed ID** | OP-04 |
| **Risk** | Token exhaustion causing correlated agent and detection failure |
| **Category** | Operational Risks |
| **OWASP Mapping** | LLM10 (Unbounded Consumption) — partial; the dual-failure-path dimension has no OWASP equivalent |

## Risk Description

As agents process information, their context windows fill. This causes progressive degradation in instruction-following, constraint adherence, hallucination rate, and output quality. Unlike other operational risks, token exhaustion creates a **correlated dual failure**: the task agent degrades *and* the LLM-as-Judge monitoring it degrades simultaneously if both are consuming context at comparable rates.

This correlated failure undermines the independence assumption of the three-layer defence model. Layer 1 (guardrails) remains unaffected (deterministic rules do not degrade with token load). But Layer 2 (LLM-as-Judge) degrades in tandem with the agents it evaluates. A degraded Judge reviewing degraded agent output produces a false assurance signal — the system reports "pass" when it should escalate.

## Scenario

A multi-agent research system processes a large corpus. Agent A ingests documents, Agent B analyses them, Agent C compiles findings. Over a long session:

1. Agent B's context fills with document excerpts, intermediate analysis, and tool outputs.
2. Agent B begins producing subtly lower-quality analysis — simplified reasoning, dropped qualifiers, relaxed constraints.
3. The Judge, which has been evaluating Agent B's outputs throughout the session, also has a full context — evaluation history, prior assessments, agent outputs.
4. The Judge's evaluation quality degrades. It approves outputs it would have flagged with a fresh context.
5. Agent C receives degraded analysis that was approved by a degraded Judge. The final output contains errors that passed two layers of review.
6. No alert fires. No PACE transition triggers. The system reports normal operation.

The failure looks like success.

## Risk Table Entry

| ID | Risk | Scenario | Prevent | Detect | Judge/Challenger Role | MASO Status | Control |
|----|------|----------|---------|--------|----------------------|-------------|---------|
| OP-04 | **Token exhaustion — dual failure path** | Agent context fills during long-running or complex tasks. Quality degrades gradually. Judge context fills concurrently, degrading detection capability. Two defence layers fail simultaneously without triggering alerts. Adversarial exploitation becomes easier as prompt-based constraints weaken under context pressure. | Token budget management as operational control: context rotation with structured state checkpointing, input volume caps, retry limits, session time-boxing. Judge context isolation — Judge manages its own budget independently and evaluates in fresh or rotation-managed context. Structured fields (typed JSON) for checkpointed state to prevent semantic drift during rotation. | Per-agent token consumption monitoring with tiered alerts (warning at 70%, critical at 85%, exhaustion at 95%). Quality regression signals: format violations, constraint drift, hallucination rate changes. Independent Judge budget monitoring — Judge approaching threshold is a detection-layer degradation event. | Judge must manage its own context independently. Judge approaching its capacity threshold is itself a PACE trigger. Judge should evaluate in rotation-managed context, not accumulate unbounded review history. | **Gap.** EC-3.4 (time-boxing) caps duration but not context consumption. OB-2.2 (behavioral monitoring) detects pattern changes but not gradual quality regression from context pressure. No control addresses the correlated failure of agent and Judge context exhaustion. | See proposed controls below. |

## Proposed Controls

### OP-C04a: Token Budget Monitoring and Alerting

**Tier:** 1+ (monitoring), 2+ (automated response)

Token consumption per agent must be monitored as a first-class operational metric. Alert thresholds must be defined per agent and per tier:

- **Warning** (e.g., 70%): Log and notify operator.
- **Critical** (e.g., 85%): At Tier 2+, initiate context rotation. At Tier 3, automatic PACE P→A transition.
- **Exhaustion** (e.g., 95%+): Fail-closed on affected agent. At Tier 2+, PACE transition. At Tier 3, if both agent and Judge are at exhaustion, Contingency minimum.

**Rationale:** Token exhaustion is gradual and invisible without explicit monitoring. Without thresholds, the system operates in a degraded state with no triggering event for PACE.

### OP-C04b: Context Rotation with Structured State Preservation

**Tier:** 2+

Agents approaching token budget thresholds must support context rotation: checkpoint essential structured state, flush the context window, and resume with a clean context.

Checkpointed state must include:
- Original task and goal specification
- Active constraints (as typed fields, not natural language)
- Decisions made and their rationale
- Current step in plan
- Uncertainty metadata
- Assumption register

Checkpointed state must use **structured formats** (JSON schemas, typed fields) to prevent semantic drift during the rotation process. Free-text summarization of constraints is insufficient — "must not exceed 5%" must survive rotation as a typed constraint, not degrade to "keep low."

**Rationale:** Context rotation is the primary operational mitigation for token exhaustion. Without structured checkpointing, rotation itself introduces semantic drift (EP-05).

### OP-C04c: Judge Context Isolation

**Tier:** 2+

The LLM-as-Judge must manage its own context budget independently from task agents. The Judge must not accumulate unbounded evaluation history. It should:

- Evaluate agent outputs in fresh or rotation-managed context
- Track its own token consumption
- Trigger a PACE escalation if it approaches its own capacity threshold — this is a **detection-layer degradation** event, distinct from an agent-layer degradation event

If both agent and Judge approach exhaustion simultaneously, this constitutes a **correlated dual-layer failure** and must trigger a PACE transition appropriate to the tier:
- Tier 2: P→A minimum (tighten scope, human approval for writes)
- Tier 3: P→C minimum (human-in-the-loop for all decisions)

**Rationale:** The three-layer defence model assumes layer independence. If the Judge degrades in tandem with the agents it monitors, the independence assumption fails silently. Judge context isolation preserves detection capability even when agents are under pressure.

### OP-C04d: Retry Budget Caps

**Tier:** 1+

Each agent must have a maximum retry count per task (recommended: 3). If an agent cannot succeed within the retry budget, it must escalate rather than continue retrying.

**Rationale:** Retry loops are the fastest path to context exhaustion. Each failed attempt adds error messages, failed tool outputs, and correction attempts to the context — making the agent worse at each retry, not better. Retry caps prevent the degradation spiral.

## Interaction with Existing Controls

| Existing Control | Interaction |
|-----------------|-------------|
| EC-3.4 (time-boxing) | Complementary. Time-boxing caps duration; OP-C04 caps context consumption. An agent can exhaust its context well within a time limit. |
| OB-2.2 (behavioral monitoring) | OP-C04 adds token-specific monitoring signals. OB-2.2 catches behavioral drift; OP-C04 catches the resource condition that causes it. |
| EC-2.5 (LLM-as-Judge) | OP-C04c directly protects Judge effectiveness. Without it, EC-2.5's value degrades silently under context pressure. |
| EP-C05 (constraint fidelity) | OP-C04b's structured checkpointing is the rotation-time equivalent of EP-C05's handoff-time constraint checking. |
| OB-2.1 (decision chain) | Decision chain logs should include token consumption data points to support post-incident analysis of exhaustion-related failures. |

## Prioritisation Assessment

**Priority: HIGH**

- Token exhaustion is an expected operational condition, not an edge case, for any long-running multi-agent system.
- It produces a correlated failure across two defence layers — violating the independence assumption that underpins the three-layer model.
- The failure mode is silent — no crash, no error, no existing PACE trigger. Without explicit controls, the system degrades with no alert.
- Prevention and detection controls are straightforward to implement (monitoring, thresholds, rotation). The gap is in formalization, not feasibility.
