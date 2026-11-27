---
as_at: "2026-11-27"
description: "How ISO/IEC 27090:2026, the international guidance on AI security threats and compromises, lines up with AI Runtime Security: clause-by-clause alignment, where the framework goes further, and the gaps the standard exposes."
---

# ISO/IEC 27090:2026 Alignment

**How the ISO/IEC guidance on AI security threats maps onto AI Runtime Security, and what it tells us to strengthen.**

*Part of [Regulatory Alignment](README.md) · Review date: November 2026*

!!! warning "About this page"
    ISO/IEC 27090 is a copyrighted ISO/IEC publication. This page summarises its structure and themes in our own words and points to clause numbers so you can find the source text. It does not reproduce the standard. If you need to evidence alignment, buy a copy from ISO or your national standards body and work from the original.

## What the standard is

**ISO/IEC 27090:2026** (*Cybersecurity, Artificial intelligence, Addressing security threats and compromises to AI systems*) was published in October 2026 by ISO/IEC JTC 1/SC 27, the committee responsible for the ISO/IEC 27000 family. It is guidance, not a requirements standard, so there is nothing to certify against. It is written to sit inside an existing information security programme built on ISO/IEC 27001 and 27002, and it repeatedly points to ISO/IEC 42001 for AI management and to ISO/IEC 27091 for AI privacy.

The standard is organised around a threat catalogue. For each type of compromise it describes the attack, the resulting failure, how to detect it, and how to mitigate it, including which zero trust principles apply.

| Part | What it covers | Relevance to AIRS |
|------|----------------|-------------------|
| Clause 5 | Applying information security to AI: governance, zero trust, engineering practice, supply chain, threat modelling, red teaming | High. Zero trust for agents (5.3) is close to our IAM and agentic model |
| Clause 6.2 to 6.10 | Nine compromise types, each with failure, detection and mitigation | Mixed. Prompt injection, sensitive output and output injection are core runtime concerns. Evasion and training-time poisoning are mostly outside runtime scope |
| Clause 6.11 | Data limitation, controlling unwanted behaviour in operation, provenance | High. 6.11.3 is the most runtime-focused part of the standard |
| Clause 7 | How mitigations interact, decay and are operated: logging, input filtering, throttling | High. This is where the standard's thinking is closest to ours |
| Annex A | Mapping attacks to life cycle stages and to ML assets | Useful for scoping which threats need runtime controls |
| Annex B | AI-specific variants of conventional attacks: resource exhaustion, supply chain, backdoors, model theft, data leaks | Medium. Resource exhaustion and input leakage through RAG matter at runtime |
| Annex C | Federated machine learning | Low |

## Where the standard and the framework agree

The overlap is substantial. Read alongside AIRS, 27090 reinforces several positions the framework already takes.

### Zero trust applied to models and agents

Clause 5.3 extends conventional zero trust into AI: verify the source of training data, authorise each inference request against the capability it uses, authorise each RAG retrieval separately, verify each agent action on its own merits, grant agents just-in-time access that expires when the task ends, baseline normal behaviour, and treat every prompt as untrusted regardless of who sent it.

Each of those has a direct counterpart in AIRS:

| 27090 theme (5.3) | AIRS control |
|-------------------|--------------|
| Per-request authorisation of model capabilities | [IAM Governance](../../core/iam-governance.md) |
| Per-retrieval authorisation in RAG | [RAG Security](../technical/rag-security.md), [Data Provenance and Authority Boundaries](../../core/controls/data-provenance-and-authority-boundaries.md) |
| Per-action verification and expiring agent permissions | [Agentic controls](../../core/agentic.md), [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md) |
| Behavioural baselines and deviation alerts | [Behavioural Anomaly Detection](../technical/behavioral-anomaly-detection.md) |
| All input treated as untrusted | [Input guardrails](../../core/controls.md) |

### Least privilege for agents

Clause 6.11.3.3 is the standard's most concrete material on agents. It says privileges should be task-specific, time-bound, delegated with clear identity boundaries, and scaled to the impact of the operation. It also says agents should hold their own identity rather than inherit the user's full permissions. It distinguishes three implementation patterns: API-integrated agents need mediated access with checks before execution, computer-use agents need restricted environments with explicit action allow-lists, and orchestrators need strong isolation between components. It calls for verifiable agent identity, context-aware authorisation, audit trails, and graduated intervention that narrows privileges when behaviour looks anomalous.

AIRS covers all of this. Graduated intervention is what [PACE](../../core/pace-controls-section.md) does, and agent identity and delegation are covered in [IAM Governance](../../core/iam-governance.md) and [Delegation Chains](../../infrastructure/agentic/delegation-chains.md). Organisations already following AIRS at the appropriate [risk tier](../../core/risk-tiers.md) should find little to add here.

### Guardrails have limits, and human oversight has its own failure modes

Clause 6.11.3.2 makes the same two points the framework does. Guardrails cannot fully specify what good or bad behaviour looks like, so they are never complete. Human oversight is slower and more expensive but brings judgement, and it degrades when people are out of the loop or get used to clicking "confirm". The standard also names **overreliance** and **excessive agency** as causes of unwanted behaviour in their own right, alongside attacks.

See [Controls: Guardrails, Judge, and Human Oversight](../../core/controls.md), [Why Guardrails Aren't Enough](../../insights/why-guardrails-arent-enough.md) and [The Oversight Readiness Problem](../../core/oversight-readiness-problem.md).

### Model output is untrusted

Clauses 6.8 and 6.10 treat model output as something to inspect before it is shown or acted on: filter recognisable sensitive data, and apply standard output encoding and validation because output can carry conventional injection payloads such as cross-site scripting. This is the AIRS output guardrail layer.

### Retrieval data is a security asset on par with training data

Two points in the standard are worth stating plainly because many organisations miss them. Clause 6.2.1 notes that a RAG corpus can be poisoned to corrupt outputs even when the model itself is clean. Clause 7.6 argues that a RAG repository plays the same role as training data, because it steers model behaviour, so it should get the same protection. Annex B.7 adds that whatever is retrieved into a prompt should match the access rights of the person who will see the output. AIRS makes the same case in [RAG Is Your Biggest Attack Surface](../../insights/rag-is-your-biggest-attack-surface.md).

### Logging and provenance

Clause 7.5 recommends logging model use so incidents can be reconstructed and abuse patterns detected, and lists the minimum record: who called, when, what went in, what came out, and which model version answered. Clause 6.11.4 asks for a provenance record covering datasets, dependencies, configuration and pipelines, protected with signatures, with immutable logs of versions, deployments and security events.

The AIRS [flight recorder](../../insights/the-flight-recorder-problem.md) and [Provenance and Attestation](../../core/controls/provenance-and-attestation.md) controls meet and exceed this. For agentic systems the 27090 minimum is not enough on its own: you also need tool calls, Judge verdicts, approvals and PACE state changes to reconstruct what happened.

### Supply chain

Clause 5.5 and Annex B.3 and B.4 cover poisoned pre-trained models, trojaned models, malicious dependencies and misrepresented provenance. Mitigations include signed models and datasets, trusted repositories, dependency scanning, scanning model weight files for embedded code, and safe weight formats that cannot execute code on load. See [Supply Chain](../technical/supply-chain.md) and [MASO Supply Chain](../../maso/controls/supply-chain.md).

## Where AIRS goes further

27090 is a broad threat catalogue for all AI, including image classifiers and predictive models. Its depth on runtime control of generative and agentic systems is limited. AIRS adds:

| Area | 27090 | AIRS |
|------|-------|------|
| Prompt injection defence | Classifiers, keyword filtering (which the standard itself says is of limited value), and separating untrusted content in the prompt with markers (6.9.4) | Treats prompt-level separation as a hint the model may ignore. Untrusted content is tagged as data at the boundary and never promoted to instruction, enforced outside the model. See [Data Provenance and Authority Boundaries](../../core/controls/data-provenance-and-authority-boundaries.md) and [Semantic Firewall](../../core/controls/semantic-firewall.md) |
| Model-as-Judge | Mentions using LLMs to detect induced responses (6.9.3) | Full Judge architecture with accuracy measurement and calibration. See [Judge Assurance](../../core/judge-assurance.md) |
| Degraded operation | Not covered | [PACE](../../core/pace-controls-section.md) defines how the system fails safe as controls fail |
| Multi-agent systems | Orchestrators mentioned in one sentence | [MASO](../../maso/README.md) |
| Memory and context | Not covered beyond continuous learning | [Memory and Context](../../core/memory-and-context.md) covers persistent memory poisoning across sessions |
| Risk-proportionate control selection | Risk-based approach recommended but not structured | [Risk Tiers](../../core/risk-tiers.md) |

## Gaps the standard exposes in AIRS

These are areas where 27090 makes a point the framework does not yet make clearly enough.

### 1. Query-pattern abuse detection

Model exfiltration (6.5), model inversion (6.6) and membership inference (6.4) all work through legitimate-looking queries. The standard's detection advice for all three is per-caller analysis of query series: frequency, ordering, diversity, coverage of the input space, and sequences of small perturbations with rising confidence (6.4.3, 6.5.3, 6.6.3, 7.7.2). Clause 7.8 makes a distinction worth adopting: **throttling to hinder experimentation** is a security control, separate from rate limiting to prevent overload, and should be tuned per user.

AIRS lists rate limiting as an input control for "abuse, enumeration" but does not treat probing for the model, its training data or its weaknesses as a distinct pattern. The fix is to add per-identity query-series analytics to [Behavioural Anomaly Detection](../technical/behavioral-anomaly-detection.md) and to set experimentation thresholds separately from capacity limits, at least for systems that serve proprietary or fine-tuned models or were trained on personal data.

### 2. Mitigations interfere with each other

Clause 7.2 points out that adding a mitigation can weaken another or degrade performance, and recommends re-verifying the whole set of mitigations each time one is added. Clause 7.3 adds that related mitigations at different life cycle stages have to be consistent with each other, for example training data checks and inference-time filtering.

The standard is thinking of mitigations that involve retraining. The same applies to runtime layers. A stricter input guardrail changes what the Judge sees, a new output filter can mask the signal anomaly detection relies on, and a tighter rate limit can push attackers into slower probing that escapes per-window detection. AIRS should state that the control stack is tested as a set, not one layer at a time, when any layer changes.

### 3. Controls decay

Clause 7.4 says mitigation effectiveness deteriorates over time just as model performance does, and calls for operational monitoring of mitigation effectiveness and revalidation before redeployment. This supports [Temporal Decay](../../insights/temporal-decay.md) and the treatment of oversight as a depreciating asset in [Safety Cases and Oversight Durability](../../core/controls/safety-cases-and-oversight-durability.md). It is worth making explicit that guardrail classifiers and Judge models are mitigations in exactly this sense and need the same effectiveness monitoring as the primary model.

### 4. Resource-exhaustion inputs

Annex B.2 describes inputs crafted to make each query far more expensive in time or energy than normal, which generic denial-of-service detection will not catch. The standard recommends per-query time or energy monitoring, aborting queries that exceed a budget, and sizing for worst-case rather than average cost. It notes this has to be designed in, not bolted on. [Economic Governance](../technical/economic-governance.md) and [Token Economics](../technical/token-economics.md) cover cost control, but per-request compute budgets should be listed as a security control too, especially for reasoning models and agent loops.

### 5. Attack or failure?

Clause 6.11.3.1 recommends deciding whether unwanted behaviour has a security cause before choosing a response, and lists the common non-attack causes: poor training data, model drift, engineering mistakes, overreliance and excessive agency. AIRS controls respond to behaviour regardless of cause, which is the right default at runtime. The incident process should still include an explicit triage step, because the remediation is different: an attack calls for containment and threat hunting, while drift or excessive agency calls for redesign.

### 6. Transparency versus attacker reconnaissance

Clauses 6.3.4 and 6.11.2.5 caution that publishing technical detail about an AI system helps attackers tailor their attacks, and that this has to be balanced against transparency obligations. This is a real tension for organisations that publish system cards or detailed control descriptions, and it belongs in [Framework Tensions](../../strategy/framework-tensions.md).

## Threat coverage summary

How each 27090 compromise type relates to runtime controls. Training-time threats need controls earlier in the life cycle. AIRS runtime controls detect their effects but cannot prevent them.

| 27090 compromise type | Clause | Where it is primarily addressed | AIRS runtime role |
|-----------------------|--------|-------------------------------|-------------------|
| Data poisoning | 6.2 | Data governance, training pipeline | Detect behavioural shift, protect RAG and memory stores |
| Evasion | 6.3 | Model robustness | Input anomaly detection, Judge cross-check |
| Membership inference | 6.4 | Training (differential privacy, minimisation) | Query-pattern detection, throttling, output restriction |
| Model exfiltration | 6.5 | Access control, output minimisation | Query-pattern detection, throttling |
| Model inversion | 6.6 | Training (privacy techniques) | Query-pattern detection, throttling |
| Direct model poisoning | 6.7 | Supply chain, development environment | Behavioural monitoring, provenance and attestation |
| Sensitive model output | 6.8 | Runtime | Output guardrails, DLP |
| Prompt injection | 6.9 | Runtime | Input guardrails, authority boundaries, semantic firewall, Judge, least privilege |
| Output contains injection | 6.10 | Runtime and consuming application | Output validation and encoding |
| Resource exhaustion | B.2 | Runtime | Per-request budgets, circuit breakers |
| Model input leak | B.7 | Runtime | Retrieval authorisation, DLP, encryption |

## Using this alongside your ISMS

If you run an ISO/IEC 27001 ISMS, 27090 is the natural reference for extending your risk assessment to AI threats, and its threat catalogue can seed AI threat modelling (5.6). AIRS supplies the runtime controls that treat those risks once systems are in production. A practical sequence:

1. Use the 27090 compromise types and Annex A asset mapping to extend your ISMS risk register to each AI system.
2. Classify each system with [AIRS risk tiers](../../core/risk-tiers.md).
3. Treat the runtime-addressable threats with AIRS controls, and the training-time threats with data governance and supply chain controls.
4. Record the mapping in your Statement of Applicability using [ISO 27001 Alignment](iso-27001-alignment.md) and [ISO 42001 Clause Mapping](iso-42001-clause-mapping.md).

!!! info "References"
    - [ISO/IEC 27090:2026, Cybersecurity, Artificial intelligence, Addressing security threats and compromises to AI systems](https://www.iso.org/standard/27090)
    - [ISO/IEC 27001:2022, Information security management systems](https://www.iso.org/standard/27001)
    - [ISO/IEC 42001:2023, AI management system](https://www.iso.org/standard/81230.html)
    - [OWASP AI Exchange](https://owaspai.org/)
    - [ETSI EN 304 223, Baseline Cyber Security Requirements for AI](https://www.etsi.org/deliver/etsi_en/304200_304299/304223/02.01.01_60/en_304223v020101p.pdf)
