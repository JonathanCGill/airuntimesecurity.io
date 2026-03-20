---
description: "Security controls for AI memory and context: protecting against cross-session data leakage, context poisoning, and accumulated state attacks."
---

# Memory and Context Controls

> Securing what the model remembers - across turns, sessions, and users.
>
> *This document uses the simplified three-tier system (Tier 1/2/3). See [Risk Tiers - Simplified Tier Mapping](risk-tiers.md#simplified-tier-mapping) for the mapping to LOW/MEDIUM/HIGH/CRITICAL.*

## The Problem

The three-layer pattern evaluates individual requests and responses. But AI systems accumulate context:

- **Within a conversation** - each turn adds to the context window
- **Across conversations** - persistent memory, session history, user profiles
- **Across users** - shared embeddings, cached responses, fine-tuned models

A single request-response pair may be safe. The accumulated context may not be.

## Threat Model

| Threat | Vector | Impact |
|--------|--------|--------|
| **Gradual context poisoning** | Early turns inject instructions that influence later turns | Model behavior changes over a long conversation without triggering per-turn guardrails |
| **Cross-session leakage** | Persistent memory or shared cache surfaces User A's data for User B | Data breach - potentially regulated data |
| **Memory manipulation** | Injecting false "memories" via conversation that persist across sessions | Ongoing manipulation of model behavior for a user |
| **Context window overflow** | Filling the context with irrelevant content to push out system instructions | Guardrail bypass - system prompt "forgotten" |
| **Accumulated PII** | Individual turns are PII-free but the conversation as a whole builds a profile | Privacy violation - model holds more personal data than any individual turn reveals |

## Controls

### 1. Session Isolation

Every user session must be isolated. No shared state between users unless explicitly designed and controlled.

| Requirement | Implementation |
|-------------|---------------|
| **Separate context per user** | Each user gets their own conversation thread - no shared context window |
| **Separate memory per user** | Persistent memory is scoped to the authenticated user |
| **No shared cache for generated responses** | Response caching (if used) must be keyed to user + input, not input alone |
| **Session timeout** | Conversations expire after inactivity - context is not preserved indefinitely |

### 2. Context Window Hygiene

| Control | What It Does |
|---------|-------------|
| **System prompt anchoring** | Re-inject system instructions at intervals in long conversations, not just at the start |
| **Context summarisation** | Periodically summarise old turns and replace verbose history with summaries |
| **Turn limits** | Maximum number of turns per conversation before requiring a new session |
| **Token budget monitoring** | Alert when context window approaches capacity, because model behavior degrades near limits. This is a security control, not just a performance concern: attention dilution weakens system prompt adherence, increases hallucination rates, and degrades instruction-following. In multi-agent systems, this becomes a dual failure path when the Model-as-Judge's context also fills (see [MASO OP-04](../maso/controls/risk-register.md) for the full risk treatment). Recommended thresholds: 70% (info), 85% (warning), 95% (critical/fail-closed) |

#### Context Rotation (Tier 2+)

When token budget monitoring (above) indicates an agent is approaching context limits, **context rotation** preserves the agent's work while restoring guardrail effectiveness:

1. **Checkpoint** the essential structured state: current goal, active constraints, accumulated decisions, pending actions, as typed structured fields (JSON schema), not free-text summaries
2. **Flush** the context window
3. **Resume** with the original system prompt + structured checkpoint

The critical design decision: **use structured state, not natural language summaries.** Summarisation introduces semantic drift: "must" becomes "should," "never exceed 5%" becomes "keep low," qualifiers vanish. Requirements soften through each summarisation cycle. Typed fields preserve constraint precision.

In multi-agent systems, context rotation must be coordinated with the Model-as-Judge. If the Judge is also approaching its context limit, rotate the Judge independently, since correlated exhaustion (agent and Judge both degraded) is a PACE escalation trigger. See [MASO Execution Control EC-2.16, EC-2.17](../maso/controls/execution-control.md) for the full control specification.

### 3. Persistent Memory Controls

For systems that maintain memory across sessions (user preferences, conversation history, learned context):

| Control | What It Does |
|---------|-------------|
| **Memory content filtering** | Apply guardrails to content before it's written to persistent memory |
| **Memory access control** | Only the authenticated user (or authorised system) can read their memory |
| **Memory expiry** | Set TTLs on stored memories - not everything should persist forever |
| **Memory audit trail** | Log what's written to and read from persistent memory |
| **User memory controls** | Users can view, edit, and delete their stored memories |
| **Memory injection prevention** | Validate that persistent memories are genuine (from real conversations) not injected |
| **Semantic deduplication** | Detect and prevent accumulation of near-duplicate memory entries that could indicate poisoning; semantically similar entries are merged or flagged for review before storage |

### 4. Accumulated Context Evaluation

Don't just evaluate individual turns. Periodically evaluate the full conversation context.

| Trigger | Action |
|---------|--------|
| Every N turns (e.g., 10) | Run the Judge on the full conversation, not just the latest turn |
| Context window >50% full | Check for context poisoning patterns (repeated instructions, topic drift) |
| User requests sensitive action | Evaluate the full conversation for manipulation patterns before allowing the action |

### 5. Cross-Session Data Governance

| Requirement | Implementation |
|-------------|---------------|
| **Data classification** | Classify persistent memory content with the same scheme used for other data stores |
| **Retention policies** | Apply your existing data retention policies to conversation history and memory |
| **Right to deletion** | Implement memory deletion that actually deletes - not just soft-delete |
| **Encryption** | Encrypt persistent memory at rest and in transit - same controls as any data store |

## Architecture Patterns

### Stateless (Recommended for Tier 1–2)

No persistent memory. Each conversation starts fresh. Context exists only within the session.

- Simplest to secure
- No cross-session risks
- Users may find it frustrating for repeated tasks

### Stateful with Scoped Memory (Tier 2–3)

Persistent memory scoped to user, with explicit controls.

- Memory is a separate data store with its own access controls
- Memory content is filtered before storage and before retrieval
- Memory has TTLs and audit trails

### Shared Knowledge Base (Tier 3 - requires careful design)

Shared embeddings or knowledge that multiple users access (e.g., company FAQ, product documentation).

- Shared content must be read-only for end users
- Ingestion pipeline is controlled (see [RAG Security](../extensions/technical/rag-security.md))
- User-specific context is never written to shared stores

## Behavioral Learning and Preference Data

The controls above address what the model *remembers* - context windows, persistent memory, shared knowledge. But some systems are designed to *learn* from user behavior: adapting communication style, building preference profiles, personalising recommendations based on interaction history.

This is a different threat surface. Memory controls govern *storage and retrieval*. Behavioral learning controls govern *what you choose to extract, model, and act on*.

### The Problem

A system that learns customer preferences builds a behavioral profile. Over time, that profile becomes:

- **Quasi-identifying** - Writing style, reading patterns, product preferences, and interaction timing can re-identify a user even without explicit PII
- **Inferential** - The system can infer sensitive attributes (financial situation, health concerns, emotional state) from behavioral signals the user didn't intend to share
- **Self-reinforcing** - Recommendation engines create feedback loops: the system shows you what it thinks you want, you interact with it, and that interaction confirms its model - even if the model was wrong
- **Poisonable** - An adversary can inject false preference signals to manipulate future recommendations (showing a user competing products, biasing pricing, or shifting trust)

### Decision Framework

Before building a preference-learning system, answer these questions:

| Question | If you can't answer clearly, stop |
|----------|----------------------------------|
| **What are you learning, and why?** | "User preferences" is too vague. Define exactly which signals you extract (product categories browsed, response length preference, time-of-day patterns) and the business purpose for each |
| **Does the user know?** | Transparency isn't optional. The user should understand what the system has learned about them, in language they can read - not a JSON dump |
| **Can the user see, correct, and delete what you've learned?** | If you store a preference model, users need the ability to inspect it, dispute incorrect inferences, and request deletion. This is regulatory in many jurisdictions and good practice in all of them |
| **Is the learned data more sensitive than the raw data?** | Individual page views are low-sensitivity. An inferred health concern derived from browsing patterns is high-sensitivity. Classify the *output* of your learning, not just the input |
| **How do you detect preference poisoning?** | If an attacker can shift your model of a user by injecting interactions, your recommendation engine becomes an attack surface. Define baselines and anomaly detection for profile changes |
| **What's your feedback loop risk?** | If the system recommends → user clicks → system reinforces, you can converge on a narrow model that doesn't reflect the user's actual preferences. Build in diversity or exploration mechanisms |

### What the Framework Covers

Your existing controls from this document and the broader framework apply to the *infrastructure* of behavioral learning:

| Framework control | How it applies to preference learning |
|---|---|
| **Persistent memory controls** (Section 3 above) | Preference data is persistent memory. Apply the same controls: TTLs, access scoping, content filtering, injection prevention, user memory controls |
| **Accumulated PII** (Threat Model above) | Behavioral profiles are the canonical example. Individual interactions are low-risk; the accumulated profile is high-risk |
| **Cross-session data governance** (Section 5 above) | Preference data flows across sessions. Apply the same isolation, classification, and access controls |
| **Data retention** ([Data Retention Guidance](../extensions/templates/data-retention-guidance.md)) | Preference data needs retention limits. Define how long you keep learned preferences and how you purge them |
| **Judge evaluation** ([Controls](controls.md)) | Your Judge can evaluate whether recommendations are appropriate, whether the system is over-personalising, and whether inferred preferences are plausible |

### What the Framework Does Not Cover

The *policy decisions* - what to learn, when to ask consent, how to explain inferences - are domain-specific. The framework gives you the security and governance infrastructure. You need domain expertise and legal guidance for:

- **Consent design** - What does meaningful consent look like for behavioral learning? (Not "I agree to terms." Granular, revocable, specific.)
- **Explainability** - How do you present a learned preference model to a non-technical user in a way they can understand and act on?
- **Differential privacy** - How do you learn aggregate patterns without exposing individual behavior? (Research-stage for most enterprises, but critical at scale.)
- **Fairness and bias in recommendations** - If your preference model correlates with protected characteristics, your recommendations may discriminate. This is a fairness problem, not just a security problem.

### Offramps - Go Here Next

| Topic | Resource | Why |
|-------|----------|-----|
| **Profiling under GDPR** | [ICO Guidance on Profiling and Automated Decision-Making](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/automated-decision-making-and-profiling/) | Defines when behavioral profiling requires explicit consent, a right to object, and human review. Directly applicable if you serve UK/EU users |
| **GDPR transparency requirements** | GDPR Articles 13–14 (right to be informed), Article 15 (right of access), Article 22 (automated individual decision-making) | What you must disclose about automated profiling. Your legal team should map these to your preference learning system |
| **CCPA right to know and delete** | [California Attorney General CCPA Resources](https://oag.ca.gov/privacy/ccpa) | If you serve California residents, they have the right to know what data you've collected (including inferences) and to request deletion |
| **NIST Privacy Framework** | [NIST Privacy Framework 1.0](https://www.nist.gov/privacy-framework) | Maps privacy risk management to your existing NIST AI RMF alignment. The "Identify-P" and "Control-P" functions apply directly to preference data |
| **Recommendation system fairness** | Your AI/ML team's fairness evaluation tools (Fairlearn, AI Fairness 360, What-If Tool) | Test whether your preference model produces discriminatory recommendations. The framework's Judge can flag outliers, but fairness testing requires dedicated tooling |
| **Consent management platforms** | Your privacy/compliance team's consent management documentation (OneTrust, Cookiebot, TrustArc, or equivalent) | The mechanism for capturing, storing, and honouring user consent for behavioral learning. Don't build this from scratch |

**The framework's role:** Secure the storage, access, and lifecycle of preference data using existing memory and data protection controls. Detect anomalies in preference profiles. Evaluate recommendation quality through the Judge layer.

**Your responsibility:** Decide *what* to learn, get *informed consent*, provide *transparency and user control*, and ensure *fairness*. These are design and policy decisions, not security controls - but they determine whether your security controls are protecting the right things.

