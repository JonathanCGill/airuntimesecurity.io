---
as_at: "2026-07-04"
description: "Risk tier definitions for AI systems, from LOW to CRITICAL, with control requirements scaled to impact, autonomy, and data sensitivity. Select or deselect controls based on your risk appetite and organisational context."
---

# Risk Tiers and Control Selection

Risk tiers exist so that controls are proportionate to the harm an AI system could cause. The purpose is not to impose a uniform set of requirements. It is to help AI product owners quickly identify the controls they need and consciously deselect the ones they do not, based on the risk profile of each use case and the way their organisation works.

## Tier Definitions

### CRITICAL

Direct, automated decisions affecting customers, finances, or safety.

- Autonomous decision-making with real-world impact
- Financial transactions or credit decisions
- Health, safety, or legal implications
- Minimal human review before action

**Examples:** Credit approval, fraud blocking, medical triage, automated trading

### HIGH

Significant influence on decisions or access to sensitive data.

- Recommendations typically followed
- Access to confidential customer data
- External-facing with brand impact
- Decisions affecting employment or access

**Examples:** Customer service with account access, HR screening, legal document analysis

### MEDIUM

Moderate impact, primarily internal, human review expected.

- Internal users with domain expertise
- Output is input to human decision
- Limited sensitive data access
- Recoverable errors

**Examples:** Internal Q&A, document drafting, code generation with review

### LOW

Minimal impact, non-sensitive context.

- Public information only
- No personal data access
- No decisions, just information
- Easy to verify or ignore

**Examples:** Public FAQ bot, content suggestions, general lookup

## Control Matrix

### Input Guardrails

| Control | LOW | MEDIUM | HIGH | CRITICAL |
|---------|-----|--------|------|----------|
| Injection detection | Basic | Standard | Enhanced + ML | Multi-layer |
| PII detection | - | Warn | Block | Block + alert |
| Content policy | Basic | Standard | Strict | Maximum |
| Rate limiting | Standard | Standard | Strict | Strict + anomaly |
| Per-request compute budget | Standard | Standard | Enforced + alert | Enforced + alert |
| Probing detection (per-identity query series) | - | Conditional | Conditional | Required |

**Probing detection** is conditional below CRITICAL: required when the model is proprietary or fine-tuned, or when its training data includes personal or confidential records. See [Detect Probing, Not Just Volume](controls.md#detect-probing-not-just-volume).

### Output Guardrails

| Control | LOW | MEDIUM | HIGH | CRITICAL |
|---------|-----|--------|------|----------|
| Content filtering | Basic | Standard | Enhanced | Maximum |
| PII in output | Warn | Block | Block + alert | Block + alert + log |
| Grounding check | - | Basic | Required | Required + citation |
| Confidence threshold | - | - | Required | Required + escalation |

### Judge Evaluation

| Aspect | LOW | MEDIUM | HIGH | CRITICAL |
|--------|-----|--------|------|----------|
| Coverage | 1-5% (optional) | 5-10% | 20-50% | 100% |
| Timing | - | Batch (daily) | Near real-time | Real-time |
| Depth | - | Basic quality | Full policy | Full + reasoning |
| Escalation | - | Weekly | Same-day | Immediate |

> **Note:** "Real-time" Judge evaluation for CRITICAL tier means near-real-time parallel assessment - the Judge evaluates alongside or immediately after delivery. It does not mean inline blocking, which is the Guardrail's role. Principle: **Guardrails prevent. Judge detects. Humans decide. Circuit breakers contain.**

### Human Oversight

| Aspect | LOW | MEDIUM | HIGH | CRITICAL |
|--------|-----|--------|------|----------|
| Review trigger | Exceptions | Sampling + flags | All flags | All significant |
| Review SLA | 72h | 24h | 4h | 1h |
| Reviewer | General | Domain knowledge | Expert | Senior + expert |
| Approval required | - | - | High-impact | All external |

### Logging

| Aspect | LOW | MEDIUM | HIGH | CRITICAL |
|--------|-----|--------|------|----------|
| Content | Metadata | Full | Full + context | Full + reasoning |
| Retention | 90 days | 1 year | 3 years | 7 years |
| Protection | Standard | Standard | Enhanced | Immutable |

## Domain-Specific Guardrail Tuning

The UK AI Security Institute's *Frontier AI Trends Report* (December 2025) found significant **uneven safeguard coverage** across request categories in frontier AI systems. Biological misuse was well-defended across models tested, while other risk categories - including financial advice, legal guidance, and social engineering - were far less robustly safeguarded.

This finding reinforces a critical principle: **one-size-fits-all guardrails are insufficient.** Organisations must tune guardrail configurations to the specific risk domains relevant to their use case.

| Finding | Implication for Control Selection |
|---------|----------------------------------|
| Safeguard coverage varies dramatically by category | Test guardrails against your specific risk domains, not just generic benchmarks |
| R² = 0.097 between model capability and safeguard robustness | More capable models are not inherently safer - don't reduce controls when upgrading models |
| Universal jailbreaks found in every frontier system tested | Guardrails alone are not sufficient at any tier - the three-layer pattern is essential |
| Effort required for jailbreaks increased 40x in 6 months for one category | Safeguards can improve rapidly with deliberate investment - but only for targeted categories |

**Practical guidance:**

- At **HIGH** and **CRITICAL** tiers, test guardrails specifically against the risk categories relevant to your use case - not just the provider's default test suite.
- Don't assume that a model's strong performance in one safety category (e.g., refusing to generate malware) transfers to your domain (e.g., refusing to give inappropriate financial advice).
- Schedule domain-specific red-team testing at least quarterly for HIGH tier and monthly for CRITICAL tier systems.

> **Source:** UK AI Security Institute, *Frontier AI Trends Report*, December 2025.

## Propensity Is Environment-Dependent

Capability is not the only thing that determines how a model behaves. Research on **propensity** (a model's tendency toward unsanctioned behaviour, as distinct from its capability for it) finds that the **environment a model is placed in measurably changes that propensity**, with roughly equal contributions from strategic and non-strategic factors across 23 models and 11 environments, and some evidence of increasing sensitivity to goal conflicts ([*Propensity Inference*, Järviniemi et al., arXiv:2604.21098](https://arxiv.org/abs/2604.21098)).

The practical implication reinforces tiering by **deployment context**, not model choice alone. The same model placed in a higher-conflict, higher-autonomy environment is a different risk, which is why the tier is a property of the use case and its surroundings, not just the model. It also means a model swap is not the only trigger for reassessment: a change to the agent's environment (new tools, new data sources, more autonomy) can shift propensity even with the model held constant.

> **Source:** *Propensity Inference: Environmental Contributors to Unsanctioned LLM Behaviour* (2026).

## Classification Process

### Step 1: Score Impact Dimensions

| Dimension | Question |
|-----------|----------|
| Decision authority | Makes decisions or informs them? |
| Reversibility | Can errors be undone? At what cost? |
| Data sensitivity | PII? Financial? Confidential? |
| Audience | Internal experts or external customers? |
| Scale | How many affected? |
| Regulatory | Regulated activity? |

### Step 2: Apply Highest Tier

If any dimension suggests higher tier, use it.

| Scenario | Key Factor | Tier |
|----------|------------|------|
| Internal Q&A, no PII | Low stakes | MEDIUM |
| Internal Q&A, HR data access | Sensitive data | HIGH |
| Customer chat, public info | External but low stakes | LOW |
| Customer chat, sees accounts | Sensitive data | HIGH |
| Customer chat, takes actions | Actions + external | CRITICAL |

These six dimensions pair impact with autonomy and reversibility, the same logic CSA's [Capabilities-Based Risk Assessment (CBRA)](../extensions/regulatory/csa-aicm-alignment.md) reaches independently by scoring **Criticality x Autonomy x Permission x Impact**. CBRA's point, that autonomy over reversible actions is a far lower risk than the same autonomy over financial transactions or production code, is why this scoring weights reversibility and decision authority rather than autonomy alone.

### Step 3: Document

- Tier assigned
- Driving factors
- Mitigating controls
- Review date (annual minimum)

## Simplified Tier Mapping

Some framework documents, particularly [PACE](pace-controls-section.md) and specialized controls, use a simplified **three-tier numbered system** (Tier 1/2/3). This is intentional: the three-tier system is a practical shorthand for operational contexts where the full four-tier classification adds complexity without proportionate benefit.

| Simplified Tier | Named Risk Tiers | Description |
|-----------------|-----------------|-------------|
| **Tier 1** (Low) | LOW, MEDIUM | Internal users, no regulated decisions, recoverable errors |
| **Tier 2** (Medium) | HIGH | Customer-facing, sensitive data access, human reviews before delivery |
| **Tier 3** (High) | CRITICAL | Regulated decisions, autonomous agents with write access, financial/medical/legal |

**When in doubt, use the four-tier system.** The simplified tiers are for operational guidance (PACE resilience, testing cadence, fail posture) where the distinction between LOW and MEDIUM or HIGH and CRITICAL is less material than the distinction between internal/customer-facing/regulated.

The [MASO (Multi-Agent Security Operations) Framework](../maso/README.md) also uses Tier 1/2/3 for multi-agent **autonomy levels** (Supervised → Managed → Autonomous), which is a separate dimension from risk classification.

## Related

| If you need... | Go to |
|----------------|-------|
| Low-risk systems that skip the full review | [Fast Lane](../fast-lane.md) - self-certification for internal, read-only, no regulated data |
| Cost implications of each tier | [Cost & Latency](../extensions/technical/cost-and-latency.md) - security overhead is 15–40% at Tier 2, 40–100% at Tier 3 |
| Quantitative risk scoring | [Risk Assessment](risk-assessment.md) - six-dimension scoring for board reporting |
| Multi-agent tier progression | [MASO Implementation Tiers](../maso/README.md) - Supervised → Managed → Autonomous |
| Who owns each control when you consume AI | [Shared Responsibility for AI Systems](shared-responsibility.md) - five-actor build-vs-consume model |

## Tier Changes

**Upgrade triggers:**
- Adding sensitive data access
- Adding action capability
- Moving internal → external
- Incident revealing higher risk

**Downgrade requirements:**
- 6+ months stable operation
- No significant incidents
- Reduced scope documented
- Product owner decision (documented with risk acceptance)

