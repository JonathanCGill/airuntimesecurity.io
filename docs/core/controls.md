---
description: "The three-layer control model for AI runtime security: guardrails for known-bad, Model-as-Judge (LLM or distilled SLM) for unknown-bad, and human oversight for high-consequence decisions."
---

# Controls: Guardrails, Judge, and Human Oversight

## 1. Guardrails

Real-time controls that block known-bad inputs and outputs.

### Input Guardrails

| Control | What It Catches |
|---------|-----------------|
| **Injection detection** | Attempts to override system prompt |
| **Encoding detection** | Obfuscated attacks (Base64, hex, Unicode) |
| **PII detection** | Personal data in prompts |
| **Content policy** | Prohibited request types |
| **Rate limiting** | Abuse, enumeration |
| **Length limits** | Context stuffing |

**Processing flow:**

![Input Processing Flow](../images/input-processing-flow.svg)

### Output Guardrails

| Control | What It Catches |
|---------|-----------------|
| **Content filtering** | Harmful/inappropriate content |
| **PII detection** | Personal data leakage |
| **Grounding check** | Hallucination |
| **Format validation** | Malformed responses |

### Limitations

Guardrails catch **known patterns**. They miss:
- Novel techniques
- Semantic variations
- Context-dependent violations
- Subtle policy violations

This is why the Judge provides the second layer.

> For practical implementation guidance - international PII detection, RAG ingestion filtering, secrets scanning, alerting design, and guardrail exception governance - see **[Practical Guardrails](../insights/practical-guardrails.md)**.

## 2. Model-as-Judge

Evaluation of interactions for quality and policy compliance. The Judge can be a large LLM (for async assurance and complex reasoning) or a [distilled SLM](../extensions/technical/distill-judge-slm.md) (for inline, real-time action screening). Both approaches can be combined: an SLM screens every action in under 50ms, while a large LLM audits a sample asynchronously.

→ For model selection guidance, see [Judge Model Selection](../extensions/technical/judge-model-selection.md)

### What the Judge Does

| Function | Description |
|----------|-------------|
| Policy compliance | Did the AI follow guidelines? |
| Quality assessment | Accurate, helpful, appropriate? |
| Anomaly detection | Unusual patterns? |
| Risk flagging | What needs human review? |

### What the Judge Does NOT Do

- Block transactions in real-time
- Make final decisions
- Replace human judgment

**The Judge surfaces findings. Humans decide actions.**

### Architecture

![Judge Architecture - Simple and Two-Tier](../images/judge-simple-flow.svg)

### Evaluation Criteria

| Criterion | Scoring |
|-----------|---------|
| Policy adherence | Pass / Minor / Major violation |
| Accuracy | Verified / Unverified / Incorrect |
| Appropriateness | Appropriate / Borderline / Inappropriate |
| Safety | Safe / Uncertain / Concerning |

**Output:** PASS / REVIEW / ESCALATE

### Deployment Phases

| Phase | Action on Findings |
|-------|-------------------|
| **Shadow** | Log only, measure accuracy |
| **Advisory** | Surface to humans, learn from feedback |
| **Operational** | Findings drive workflows |

**Start in shadow mode.** Validate accuracy before acting.

### Accuracy

The Judge will make mistakes.

| Error | Impact | Mitigation |
|-------|--------|------------|
| False positive | Unnecessary review | Tune prompts |
| False negative | Missed violations | Human sampling |

**Target:** >90% agreement with human reviewers.

## 3. Human Oversight (HITL)

Humans review findings, make decisions, remain accountable.

![HITL Architecture](../images/hitl-architecture.svg)

### Triggers

| Trigger | Response |
|---------|----------|
| Judge flag | Review interaction |
| Guardrail block | Review if legitimate |
| User escalation | Human takes over |
| Sampling | Quality assurance |
| Threshold breach | Investigate pattern |

### Queue Design

| Queue | SLA | Reviewer |
|-------|-----|----------|
| Critical | 1h | Senior + expert |
| High | 4h | Domain expert |
| Standard | 24h | Trained reviewer |
| Sampling | 72h | QA team |

### Actions

| Action | When |
|--------|------|
| Approve | Interaction appropriate |
| Correct | Minor issue, fixable |
| Escalate | Needs senior review |
| Block user | Abuse detected |
| Tune | False positive |

### Prevent Rubber-Stamping

| Control | Purpose |
|---------|---------|
| Canary cases | Verify reviewers catch known-bad |
| Time tracking | Flag too-fast reviews |
| Volume limits | Prevent fatigue |
| Inter-rater checks | Measure consistency |

## Going Deeper

| Topic | Document |
|-------|----------|
| What these controls cost in production | [Cost & Latency](../extensions/technical/cost-and-latency.md) - latency budgets, sampling strategies, tiered evaluation cascade |
| Judge accuracy, drift, and adversarial failure | [Judge Assurance](judge-assurance.md) · [When the Judge Can Be Fooled](when-the-judge-can-be-fooled.md) |
| Practical guardrail configurations | [Practical Guardrails](../insights/practical-guardrails.md) - what to turn on first, encoding detection, international PII |
| When HITL doesn't scale | [Humans in the Business Process](../extensions/technical/humans-in-the-business-process.md) - using existing business process checkpoints as a detection layer |
| Controls for multi-agent systems | [MASO Framework](../maso/) - 128 controls across 7 domains for agent orchestration |
| Controls for reasoning models (o1, etc.) | [Reasoning Model Controls](reasoning-model-controls.md) - trace scanning, instruction adherence, consistency checks |
| Session-level and pre-action evaluation | [Output Evaluator](../extensions/technical/output-evaluator.md) - session-aware, pre-action evaluation architecture for agentic systems |

## Implementation Order

1. **Logging** - Can't evaluate what you don't capture
2. **Basic guardrails** - Block obvious attacks
3. **Judge in shadow** - Evaluate without action
4. **HITL queues** - Somewhere for findings
5. **Judge advisory** - Surface to humans
6. **Enhanced guardrails** - Add ML detection
7. **Judge operational** - Drive workflows
8. **Continuous tuning** - Improve from findings

