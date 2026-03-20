# Output Evaluator: Session-Aware, Pre-Action Evaluation Architecture

> Closing the gap between per-interaction controls and campaign-level threats.

## The Problem This Solves

The framework's three-layer pattern (Guardrails → Judge → Human Oversight) operates at the **interaction level**. Each input is checked. Each output is evaluated. Each action is individually validated.

This architecture has three structural blind spots exposed by 2025–2026 threat intelligence:

| Blind Spot | Threat Evidence | Why Per-Interaction Controls Miss It |
|------------|----------------|--------------------------------------|
| **Task decomposition** | Anthropic disclosed AI-orchestrated espionage campaign (80–90% autonomous) decomposed into individually benign sub-tasks; CrowdStrike documented adversary frameworks that split malicious tasks into innocent components | Each sub-task passes guardrails, Judge, and circuit breakers independently. Malicious intent exists only in the aggregate. |
| **Speed asymmetry** | CrowdStrike: fastest eCrime breakout at 27 seconds; agents execute tool calls in milliseconds | Async Judge evaluation (500ms–5s + queue) fires after the damage is done. Detection without prevention. |
| **Integration layer as primary attack surface** | 43% MCP server vulnerability rate; CVE-2025-6514 CVSS 10.0 RCE; fake npm MCP packages; GitHub issue injection → repo takeover | Core controls don't cover the tool supply chain. Attack enters through the tools, not the model. |

The Output Evaluator is a solution architecture that addresses the first two blind spots. (The third is addressed by elevating supply chain controls to core; see [Agentic Controls §8](../../core/agentic.md#8-tool-and-integration-supply-chain).)

## Architecture Overview

The Output Evaluator operates at three timescales simultaneously:

![Output Evaluator Timescales](../../images/output-evaluator-timescales.svg)

### Layer 1: Real-Time Pre-Action Evaluation

For agentic systems, the Judge must be able to evaluate **before** an action executes, not only after.

**Action classification (rule-based, <5ms):**

Every proposed agent action is classified into a risk category before execution:

| Category | Examples | Evaluation Mode |
|----------|----------|-----------------|
| **Low** | Read-only queries, internal lookups | Execute → async Judge |
| **Medium** | Data writes, internal API calls | Execute → async Judge (first occurrence: sync) |
| **Elevated** | External API calls, multi-record operations | Sync pre-action Judge → execute on pass |
| **High** | Financial transactions, destructive operations | Sync pre-action Judge + human approval → execute |
| **Flagged** | Any action when session-level flag is active | Sync pre-action Judge regardless of action type |

**Pre-action Judge prompt structure:**

```
You are evaluating a proposed agent action BEFORE it executes.

Declared user intent: {original_user_request}
Current session context: {session_summary}
Actions taken so far this session: {action_history}
Proposed action: {action_description}
Action parameters: {parameters}

Evaluate:
1. Does this action align with the declared user intent?
2. Is this action necessary to achieve the stated goal?
3. Does this action combined with previous session actions
   suggest scope beyond the declared intent?
4. Would this action be irreversible or have external impact?

Response: APPROVE / ESCALATE / BLOCK
Reasoning: [brief]
```

### Layer 2: Session-Level Intent Coherence

This layer analyzes the **aggregate trajectory** of a session, not individual actions.

**Session state tracking:**

For each active session, maintain:

```json
{
  "session_id": "sess_abc123",
  "declared_intent": "Summarise Q4 sales data for the board presentation",
  "start_time": "2026-03-09T14:00:00Z",
  "actions": [
    {"type": "read", "target": "sales_db", "scope": "Q4_2025", "time": "T+0s"},
    {"type": "read", "target": "hr_db", "scope": "employee_list", "time": "T+45s"},
    {"type": "read", "target": "finance_db", "scope": "salary_bands", "time": "T+90s"},
    {"type": "api_call", "target": "email_api", "scope": "draft", "time": "T+120s"}
  ],
  "aggregate_metrics": {
    "distinct_data_sources": 3,
    "distinct_tool_types": 2,
    "data_scope_surface": "sales + HR + finance",
    "intent_coherence_score": 0.3
  }
}
```

In this example, the declared intent is "summarise Q4 sales data" but the session has accessed HR and finance databases and is drafting an email. The intent coherence score is low. This triggers a checkpoint.

**Session checkpoints:**

| Trigger | Action |
|---------|--------|
| Intent coherence score drops below threshold | Pause session, evaluate trajectory |
| Cumulative data scope exceeds declared intent | Flag for human review |
| Action sequence matches known decomposition pattern | Escalate immediately |
| Session duration exceeds baseline for task type | Log and increase monitoring |
| Periodic checkpoint (every N actions or T minutes) | Lightweight intent coherence check |

**Intent coherence scoring:**

Score how well the session's actual actions align with its declared intent:

| Signal | Weight | Measurement |
|--------|--------|-------------|
| Data source relevance | High | Are accessed data sources relevant to declared intent? |
| Action type appropriateness | High | Are the types of actions taken (read/write/call) expected for this task? |
| Scope accumulation | Medium | Is the aggregate data footprint proportionate to the stated goal? |
| Temporal pattern | Low | Does the pacing match expected workflow for this task type? |
| Tool diversity | Medium | Is the number of distinct tools used expected for this task? |

### Layer 3: Campaign-Level Pattern Correlation

This layer operates across sessions, detecting patterns that span multiple interactions or identities.

**Cross-session signals:**

| Pattern | Detection Method |
|---------|-----------------|
| Same user, serial sessions, incrementally expanding scope | Track scope surface area across sessions for each identity |
| Different users, same action sequence | Cluster session trajectories; flag when distinct users follow identical unusual patterns |
| Low-and-slow data gathering | Aggregate data access volume per identity over rolling windows (24h, 7d, 30d) |
| Coordinated probing | Detect when multiple agents or users are testing boundaries around the same resources simultaneously |

**Integration with UEBA:**

This layer maps directly to existing User and Entity Behavior Analytics. The agent's NHI (non-human identity) should be enrolled in the same UEBA pipeline as human accounts:

| UEBA Dimension | Agent Application |
|----------------|-------------------|
| Peer group baseline | Compare agent behavior against other agents with same role/config |
| Individual baseline | Track each agent's behavioral profile over time |
| Temporal profile | Expected activity hours, volume patterns |
| Access profile | Normal data sources, tool usage, API call patterns |
| Anomaly scoring | Composite risk score updated per action |

> See [Behavioral Anomaly Detection](../../insights/behavioral-anomaly-detection.md) for the full UEBA-to-agent mapping.

## Implementation Tiers

### Tier 1: Action Classification + Known-Bad Sequences

**Effort:** Low-Medium | **Value:** Blocks obvious decomposition patterns

- Rule-based action classifier (<5ms per action)
- Sync pre-action check for elevated/high-risk actions
- Hardcoded known-bad action sequences (e.g., `read_sensitive` → `call_external_api`)
- Session-level aggregate thresholds (max data sources, max tool types)

### Tier 2: Intent Coherence + Statistical Baselines

**Effort:** Medium | **Value:** Detects novel decomposition patterns

- Everything in Tier 1
- Intent coherence scoring per session
- Behavioral baselines per agent role (statistical, not ML)
- Periodic session trajectory checkpoints
- Cross-session scope tracking per identity

### Tier 3: LLM-on-Trajectory + ML Anomaly Detection

**Effort:** High | **Value:** Catches sophisticated, novel campaigns

- Everything in Tier 2
- Model-as-Judge evaluates full session trajectory at checkpoints and close
- ML-based anomaly detection on session trajectories
- Cross-session pattern clustering
- Peer group deviation analysis
- Campaign-level correlation across identities

## Cost and Latency Impact

| Component | Added Latency | Added Cost (at 100K sessions/month) |
|-----------|--------------|-------------------------------------|
| Action classifier | <5ms per action | Negligible (rule-based) |
| Sync pre-action Judge | 500ms–2s on ~20% of actions | $2K–8K (LLM API calls) |
| Session state tracking | None (async write) | $200–500 (storage + compute) |
| Intent coherence scoring | None (async, periodic) | $500–2K (compute) |
| Session trajectory Judge | None (async, at checkpoint/close) | $1K–5K (LLM API calls) |
| Cross-session correlation | None (batch) | $500–2K (compute) |

**Total overhead:** $4K–18K/month at 100K sessions. Compare to the cost of a single successful decomposition attack (data breach, unauthorized financial transaction, infrastructure compromise).

## What This Does NOT Solve

| Limitation | Why |
|-----------|-----|
| **Novel attack patterns with normal-looking trajectories** | If the decomposed sub-tasks genuinely look like normal work, no behavioral analysis will catch them until post-incident forensics |
| **Single-action catastrophic attacks** | If one action causes irreversible harm, session-level analysis is too late; this is what pre-action evaluation and infrastructure-level blast radius limits address |
| **Insider threats with legitimate access patterns** | A user doing exactly what they're authorized to do, for unauthorized purposes, produces a normal-looking trace |
| **Evaluation evasion by the agent itself** | If the primary model can detect that its trajectory is being evaluated, it may adapt; see [Evaluation Integrity Risks](../../insights/evaluation-integrity-risks.md) |

## Relationship to Existing Framework Components

| Component | Relationship |
|-----------|-------------|
| [Controls: Guardrails](../../core/controls.md) | Output Evaluator does not replace guardrails. Guardrails remain Layer 1 for known-bad patterns. |
| [Controls: Judge](../../core/controls.md) | Output Evaluator extends the Judge with synchronous pre-action mode and session-level trajectory evaluation. The async Judge continues to operate for post-action review. |
| [Agentic Controls](../../core/agentic.md) | §6 (Session-Level Intent Analysis), §7 (Synchronous Pre-Action Evaluation), and §8 (Tool Supply Chain) are the core control specifications. This document provides the solution architecture. |
| [Behavioral Anomaly Detection](../../insights/behavioral-anomaly-detection.md) | Output Evaluator's campaign-level layer uses the UEBA framework described there. |
| [Process-Aware Evaluation](../../insights/process-aware-evaluation.md) | Output Evaluator operationalises process-aware evaluation for the pre-action and session-level layers. |
| [Cost & Latency](cost-and-latency.md) | Pre-action evaluation adds to the latency budget. Budget accordingly. |

## Implementation Order

1. **Action classifier**: Categorize every agent action by risk level (rule-based, fast)
2. **Sync pre-action gate**: Block elevated-risk actions until Judge approves
3. **Session state tracking**: Record action sequences per session
4. **Known-bad sequence detection**: Alert on hardcoded dangerous action combinations
5. **Aggregate thresholds**: Session-level circuit breakers (data sources, tool diversity, scope)
6. **Intent coherence scoring**: Measure alignment between actions and declared intent
7. **Behavioral baselines**: Statistical baselines per agent role for deviation detection
8. **LLM trajectory evaluation**: Judge evaluates full session trajectory at checkpoints
9. **Cross-session correlation**: Detect patterns spanning multiple sessions
10. **Peer group analysis**: Compare agent behavior against fleet baselines
