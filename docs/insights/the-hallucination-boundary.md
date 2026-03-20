---
description: When an LLM hallucination is a nuisance and when it becomes catastrophic. A risk-based framework for hallucination tolerance tied to decision authority and blast radius.
og_title: The Hallucination Boundary - AI Runtime Security
og_description: Analysis of when LLM hallucinations cross from tolerable to catastrophic, with a risk curve showing how decision authority and multi-agent amplification shift the consequence.
---

# The Hallucination Boundary: When a Wrong Answer Spells the End

*A confident hallucination passes every safety check. No harmful content detected. Follows system prompt instructions. Judge rates it as helpful and appropriate. Contains fabricated facts. The question is not whether hallucinations happen. It is when they matter.*

## The Same Hallucination, Different Consequences

An LLM fabricates a fact. In an internal chatbot drafting meeting notes, someone catches it during review and corrects it. Minor inconvenience. No lasting harm.

The same fabrication in a clinical decision support system excludes a viable treatment option because the model hallucinated a drug interaction that does not exist. A patient receives suboptimal care. In an autonomous credit decision engine, the model fabricates revenue figures and a loan is approved on the basis of financial data that never existed. Regulatory exposure, financial loss, and reputational damage follow.

The hallucination is identical. The consequence is not. What changed is not the model or the output. What changed is the **decision authority** the system holds and the **blast radius** of a wrong answer.

![The Hallucination Risk Curve](../images/insight-hallucination-risk.svg)

## Three Variables That Determine Hallucination Tolerance

### 1. Decision authority

The [use case definition](../strategy/use-case-definition.md) guidance identifies four levels of decision authority, and hallucination tolerance drops sharply across them:

| Authority Level | Role of the LLM | Hallucination Impact | Tolerance |
| --- | --- | --- | --- |
| **Advisory** | Suggests; human decides independently | Human catches errors in normal workflow | High |
| **Influential** | Recommends; human usually follows | Human may not verify before acting | Moderate |
| **Determinative** | Decides; human reviews after the fact | Error is acted upon before detection | Low |
| **Autonomous** | Decides and executes; no human in path | Error becomes action with no checkpoint | Near zero |

The use case definition document flags the critical self-deception in this spectrum:

> *"Many use cases claim to be 'advisory' when they're functionally 'autonomous.' If the human reviewer accepts the AI recommendation 95% of the time without independent analysis, the system is influential regardless of what the process document says."*

If the human in the loop is not genuinely evaluating outputs, the system's effective decision authority is one level higher than documented. And so is its hallucination risk.

### 2. Blast radius

A hallucination that affects one internal user has a different consequence profile from one that affects ten thousand customers. The [risk tier](../core/risk-tiers.md) classification captures this through scope:

| Scope | Blast Radius | Example Hallucination |
| --- | --- | --- |
| Single user, internal | One person's workflow | Wrong summary of a meeting |
| Single user, external | One customer relationship | Wrong product specification in a support response |
| Multiple users, batch | Many decisions or interactions | Incorrect compliance guidance applied to a portfolio |
| System-wide, automated | All downstream processes | Fabricated data point propagated through analytics pipeline |

Blast radius determines whether a hallucination is a correction task or an incident. The distinction between correcting one email and recalling ten thousand is not incremental. It is categorical.

### 3. Reversibility

Some hallucination consequences can be undone. Others cannot.

| Reversibility | Example | Recovery |
| --- | --- | --- |
| **Fully reversible** | Wrong draft text in an internal document | Delete and rewrite |
| **Reversible with effort** | Incorrect information sent to a customer | Correction, apology, minor relationship cost |
| **Partially reversible** | Wrong financial advice acted upon | Financial remediation, regulatory reporting, legal exposure |
| **Irreversible** | Hallucinated clinical contraindication excludes treatment | Patient harm cannot be undone |

When the output is irreversible, the tolerance for hallucination approaches zero. This is why the framework requires [grounding checks and citation validation](../core/risk-tiers.md) at CRITICAL tier. It is not caution. It is the mathematical consequence of irreversibility.

## The Multi-Agent Amplification Problem

Single-agent hallucinations are bad. Multi-agent hallucinations are worse, and they are worse in a specific, structural way.

The [epistemic integrity](../maso/controls/prompt-goal-and-epistemic-integrity.md) controls identify the mechanism:

**Hallucination amplification.** Agent A hallucinates a fact. Agent B receives it as input and treats it as established data. Agent C elaborates on it. By the time a human sees the output, it has been cited, cross-referenced, and presented with the confidence of a verified finding.

**Synthetic corroboration.** Agent B is asked to verify Agent A's claim. It retrieves Agent A's output from shared memory or a message bus. One source masquerades as two. The system reports "multiple agents agree" when in fact a single hallucination has been counted twice.

**Uncertainty stripping.** Agent A reports a finding with "70% confidence." Agent B passes it along as "likely." Agent C receives it as "is the case." The confidence metadata was lost in translation, and a tentative finding became an established fact.

The [MASO risk register](../maso/controls/risk-register.md) identifies these as the highest-priority gap in current multi-agent security:

> *"The most dangerous failure modes produce outputs that look correct, are well-formatted, and have multi-agent 'agreement' - but are wrong."*

These failures require no attacker. They arise from normal agent interaction dynamics. And they produce the most convincing hallucinations of all, because the output has been processed, refined, and agreed upon by multiple independent-looking agents.

## When Is a Hallucination Acceptable?

It is never safe to call a hallucination acceptable in the absolute. But hallucination tolerance is a function of what happens next. A hallucination is tolerable when every one of these conditions is met:

1. **A human reviews the output** before it influences any decision, and the human has the expertise and time to catch errors
2. **The blast radius is bounded** to a single user or a small internal scope
3. **The consequence is reversible** at low cost
4. **The system is not the source of record** for the information it generates
5. **No downstream system consumes the output** without independent verification

When all five conditions hold, a hallucination is an inconvenience. When any one fails, the risk profile changes. When multiple fail simultaneously, the hallucination becomes the system's defining failure mode.

This maps directly to the framework's [risk tiers](../core/risk-tiers.md):

| Tier | Hallucination Tolerance | Required Detection |
| --- | --- | --- |
| **LOW** | Highest - human always in path, internal only, read-only | Basic content filtering |
| **MEDIUM** | Moderate - customer-facing but human-reviewed | Basic grounding check, 5-10% judge sampling |
| **HIGH** | Low - significant decision influence | Grounding check required, 20-50% judge evaluation |
| **CRITICAL** | Near zero - autonomous or regulated decisions | Grounding + citation validation, 100% judge evaluation |

## The Verification Problem

The [verification gap](the-verification-gap.md) analysis identifies a structural challenge: the tools available to detect hallucinations have different accuracy profiles, and none of them are complete.

| Detection Method | Accuracy | What It Catches | What It Misses |
| --- | --- | --- | --- |
| Token-level detection (HaluGate) | ~96% | Whether fact-checking is needed | Does not verify the facts themselves |
| Knowledge graph grounding | ~92% | Domain-specific factual claims | Claims outside the knowledge graph |
| Formal verification | ~99% | Policy compliance | Factual accuracy beyond policy scope |
| Self-consistency checking | ~80% | Contradictory responses | Consistently wrong responses |
| Model-as-Judge | ~80% | Style, safety, appropriateness | Factual accuracy |

The critical finding: **Model-as-Judge evaluation, which is the second layer of the framework's architecture, is not effective at detecting factual hallucinations.** It catches policy violations, harmful content, and style issues. It does not independently verify whether claims are true.

This means hallucination detection for HIGH and CRITICAL tier systems cannot rely on the judge layer alone. It requires independent verification against authoritative sources: knowledge graphs, database lookups, document retrieval with citation matching, or human domain expertise.

## Controls That Actually Work

The framework's [epistemic integrity controls](../maso/controls/prompt-goal-and-epistemic-integrity.md) address the structural causes of hallucination amplification. The four most important for production systems:

**Claim provenance enforcement (PG-2.5).** Every claim carries metadata: `{source: "tool|rag|agent-generated", verified: bool}`. An agent-generated claim that has not been verified against a primary source cannot be presented as established fact. This prevents hallucinations from being laundered through agent chains.

**Self-referential evidence prohibition (PG-2.6).** No agent may cite another agent's output as primary evidence. Verification must use primary sources. This breaks the synthetic corroboration loop where Agent B "confirms" Agent A by retrieving Agent A's own output.

**Uncertainty preservation (PG-2.7).** The message schema includes `{confidence: float, assumptions: [], unknowns: []}`. Downstream agents must carry forward the confidence level. A claim that enters the chain at 70% confidence cannot exit at 100%. This prevents uncertainty stripping.

**Consensus diversity gate (PG-2.4).** Unanimous agreement from agents that share data sources triggers escalation, not approval. Independent agreement requires independent evidence. If three agents agree but all drew from the same source, that is one data point counted three times, not corroboration.

## The PACE Response to Hallucination Failure

When hallucination detection itself fails, the [PACE resilience model](../PACE-RESILIENCE.md) provides structured degradation:

| PACE Phase | Hallucination Response |
| --- | --- |
| **Primary** | All verification layers active. Grounding checks, judge evaluation, and citation validation operating normally |
| **Alternate** | One verification layer degraded. Reduce model autonomy. Present outputs as drafts requiring human confirmation |
| **Contingency** | Multiple verification layers down. Switch to retrieval-only mode. Return source documents. Do not generate |
| **Emergency** | Confirmed hallucination caused downstream harm. Disable generative capability entirely. Activate incident response |

The progression is deliberate. Each phase removes a degree of freedom from the model. The final phase removes generation entirely. If you cannot verify what the model produces, stop the model from producing.

## Key Takeaways

1. **Hallucination risk is not about the model. It is about the use case.** The same hallucination is a nuisance in one context and a catastrophe in another. Decision authority, blast radius, and reversibility determine which.

2. **Multi-agent systems amplify hallucinations structurally.** Hallucination amplification, synthetic corroboration, and uncertainty stripping produce outputs that look more reliable than single-agent errors. No attacker is required.

3. **The judge layer does not catch factual hallucinations.** Model-as-Judge evaluation achieves approximately 80% accuracy on style and safety but is not designed for factual verification. HIGH and CRITICAL systems need independent grounding against authoritative sources.

4. **Tolerance is conditional, not categorical.** A hallucination is tolerable when a competent human reviews it, the blast radius is bounded, the consequence is reversible, the system is not the source of record, and no downstream system consumes it without verification. Remove any one condition and tolerance drops.

5. **When verification fails, stop generating.** The PACE degradation path for hallucination failure ends at retrieval-only mode. If you cannot verify the output, do not produce it.

6. **Epistemic controls are structural, not behavioral.** Telling a model "do not hallucinate" is an instruction. Requiring claim provenance, prohibiting self-referential evidence, and preserving uncertainty metadata through the message schema is infrastructure. [Infrastructure beats instructions](infrastructure-beats-instructions.md).

## Related

- [The Verification Gap](the-verification-gap.md) - why current safety approaches cannot confirm ground truth
- [The Constraint Curve](the-constraint-curve.md) - when constraints themselves become counterproductive
- [Prompt, Goal and Epistemic Integrity](../maso/controls/prompt-goal-and-epistemic-integrity.md) - the full epistemic control set for multi-agent systems
- [Judge Assurance](../core/judge-assurance.md) - measuring whether the judge is actually detecting what it should
- [Risk Tiers](../core/risk-tiers.md) - how classification drives control selection
- [PACE Resilience](../PACE-RESILIENCE.md) - structured degradation when controls fail
- [The First Control](the-first-control.md) - when AI is not the right tool for the problem

