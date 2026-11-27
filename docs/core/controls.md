---
as_at: "2026-07-04"
description: "The three-layer control model for AI runtime security: guardrails for known-bad patterns, a reviewing layer (semantic firewall for known-bad intent, Model-as-Judge for unknown-bad behaviour) at increasing depth, and human oversight for high-consequence decisions. A circuit breaker sits behind the three as containment, not a behavioural layer, and maps to PACE Emergency."
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
| **Rate limiting** | Abuse, enumeration, and query-series probing for model extraction, model inversion or membership inference (throttle per identity to hinder experimentation, not just to protect capacity) |
| **Length limits** | Context stuffing |
| **Per-request compute budget** | Inputs crafted to make one request far more expensive than normal: runaway reasoning, recursive tool loops, oversized generations. Abort when the time, token or cost budget is exceeded |

**Processing flow:**

![Input Processing Flow](../images/input-processing-flow.svg){ .arch-diagram }

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

## Semantic Firewall

Part of the Reviewing Controls layer, alongside the Judge: intent-level enforcement that sits between Guardrails and Model-as-Judge in the request path. Where Guardrails block known-bad *patterns* and the Judge evaluates unknown-bad *content*, the semantic firewall catches known-bad *intent* expressed in wording neither has seen before - a request reworded, translated, or indirected to mean the same prohibited thing.

| Layer | Catches | Speed |
| --- | --- | --- |
| Guardrails | Known patterns | ~10ms |
| Semantic Firewall | Known intent, novel wording | ~15-30ms |
| Model-as-Judge | Unknown-bad, context-dependent | 10ms-5s by tier |

It classifies inbound requests against a declared taxonomy of authorised and prohibited topics/intents using an embedding classifier or distilled intent model - not a general-purpose LLM call. This makes it cheap enough to run on every request, narrowing what actually needs to reach the Judge.

**It does not replace the Judge.** It routes: pass straight through, escalate to Judge evaluation, or reject outright for high-confidence matches against the prohibited taxonomy.

→ Full detail, build options, and limitations: [Semantic Firewall](controls/semantic-firewall.md)

## 2. Model-as-Judge

Evaluation of interactions for quality and policy compliance. The Judge can be a large LLM (for async assurance and complex reasoning) or a [distilled SLM](../extensions/technical/distill-judge-slm.md) (for inline, real-time action screening). Both approaches can be combined: an SLM screens every action in under 50ms, while a large LLM audits a sample asynchronously.

→ For model selection guidance, see [Model-as-Judge Selection](../extensions/technical/judge-model-selection.md)

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

![Judge Architecture - Simple and Two-Tier](../images/judge-simple-flow.svg){ .arch-diagram }

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

![HITL Architecture](../images/hitl-architecture.svg){ .arch-diagram }

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

## Operating the Layers Together

The three layers are not independent. They share inputs, they feed each other, and they all wear out. Four practices keep them working as a system.

### Detect Probing, Not Just Volume

Some attacks look like ordinary use, one query at a time. **Model extraction** rebuilds a copy of your model from its answers. **Model inversion** reconstructs training data from outputs. **Membership inference** works out whether a specific record was in the training set. None of these needs a malicious-looking prompt, so input guardrails will not see them. They show up only in the *series* of queries from one identity.

| Signal (per identity, over time) | Possible attack |
|----------------------------------|-----------------|
| Queries spread systematically across the input space, too uniform or too random for real use | Model extraction |
| Long runs of near-identical inputs with small, steady changes | Model inversion, evasion search |
| Repeated queries about specific records or individuals, with attention to confidence or exact wording | Membership inference, training data extraction |
| Sustained volume just under the rate limit | Any of the above, deliberately paced |

Two consequences for control design:

- **Throttle to hinder experimentation, not just to protect capacity.** A rate limit sized for load will be far too generous to stop someone running thousands of probes over a week. Set per-identity limits on experimentation separately from capacity limits, and look at windows of days as well as minutes.
- **Give away less.** Withholding confidence scores, probabilities and other detail the user does not need makes all three attacks slower and less accurate.

This matters most when the model is proprietary or fine-tuned, or when its training or fine-tuning data includes personal or confidential records. For a general-purpose hosted model with no custom training, the provider carries most of this risk.

### Test the Stack as a Set

Changing one layer changes what the others see. A stricter input guardrail alters the traffic the Judge is calibrated on. A new output filter can remove the signal anomaly detection relies on. A tighter rate limit pushes attackers into slower probing that a short detection window misses. Retraining a model to resist one attack can make it weaker against another.

When any layer changes, re-run the full regression set (known-bad cases, legitimate traffic, Judge agreement checks) against the whole stack, not just the layer that changed. Treat guardrail rules, firewall taxonomies, Judge prompts and thresholds as versioned configuration, so you can tell which change caused a shift.

### Every Control Decays

Models drift, and so do the controls around them. Guardrail classifiers, semantic firewall intent models and Judges are all models or rule sets tuned to a moment in time. Attackers adapt to them, traffic shifts, and vendors update the models underneath. A control that blocked 95% of a known attack at launch may block much less a year later with nothing in your logs to show it.

Track the effectiveness of each layer, not just its activity:

| Layer | Effectiveness measure | Method |
|-------|----------------------|--------|
| Guardrails | Detection rate on a held-back known-bad set; false positive rate on real traffic | Replay the labelled set on a schedule and after every rule or model change |
| Semantic firewall | Intent classification accuracy | Same, with paraphrased and translated variants |
| Judge | Agreement with human labels | See [Judge Assurance](judge-assurance.md) |
| Human oversight | Canary catch rate, review time | See *Prevent Rubber-Stamping* above |

A fall in block rate is ambiguous: it can mean fewer attacks or a weaker control. Only replaying a fixed labelled set tells you which. Revalidate before putting any retuned or replaced control back into service. See [Temporal Decay](../insights/temporal-decay.md) and [Safety Cases and Oversight Durability](controls/safety-cases-and-oversight-durability.md).

### Attack or Failure?

The controls respond to behaviour, whatever caused it. That is the right default: a harmful output is blocked whether an attacker caused it or not. But once an incident is contained, the cause decides the fix, so incident handling needs an explicit triage step.

| Likely cause | Typical evidence | Response |
|--------------|-----------------|----------|
| **Attack** (injection, poisoning, probing) | Crafted inputs, unusual sources, concentrated on certain identities or content, correlated with other security events | Contain, preserve evidence, hunt for related activity, treat through security incident process |
| **Drift or staleness** | Gradual change across all users, correlates with time or a model or data update | Revalidate, retune or roll back |
| **Data or engineering defect** | Starts at a deployment or pipeline change, reproducible | Fix and redeploy through change control |
| **Excessive agency** | Agent acted within its permissions but outside intent | Reduce scope and permissions; redesign the task |
| **Overreliance** | Output was flagged or uncertain but acted on by users | Change the interface, training or approval design |

Poisoning in particular can look like drift for a long time. If a shift cannot be explained by a known change, investigate it as a possible attack before writing it off as drift.

## Going Deeper

| Topic | Document |
|-------|----------|
| What these controls cost in production | [Cost & Latency](../extensions/technical/cost-and-latency.md) - latency budgets, sampling strategies, tiered evaluation cascade |
| Judge accuracy, drift, and adversarial failure | [Judge Assurance](judge-assurance.md) · [When the Judge Can Be Fooled](when-the-judge-can-be-fooled.md) |
| Semantic firewall detail, build options, and limitations | [Semantic Firewall](controls/semantic-firewall.md) - intent-level boundary enforcement between Guardrails and the Judge |
| Practical guardrail configurations | [Practical Guardrails](../insights/practical-guardrails.md) - what to turn on first, encoding detection, international PII |
| When HITL doesn't scale | [Humans in the Business Process](../extensions/technical/humans-in-the-business-process.md) - using existing business process checkpoints as a detection layer |
| Controls for multi-agent systems | [MASO (Multi-Agent Security Operations) Framework](../maso/README.md) - controls across 11 domains for agent orchestration |
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
9. **Stack regression testing** - Replay labelled sets against all layers on a schedule and after any change



---

*At fleet scale:* these three layers extend into the space between agents. See [MASO](../maso/README.md) for the multi-agent version.

!!! info "References"
    - [ISO/IEC 27090:2026, Addressing security threats and compromises to AI systems](https://www.iso.org/standard/27090) (see [ISO/IEC 27090 Alignment](../extensions/regulatory/iso-27090-alignment.md))
