---
title: Glossary and Unified Taxonomy
description: "The single canonical definition source for terms shared across airuntimesecurity.io and aisecuredbydesign.io: PACE, MASO, ASO, risk tiers, the control layers, the circuit breaker, and the 85-control ID scheme."
---

# Glossary and Unified Taxonomy

Core concepts like **PACE**, **MASO**, and **risk tiers** appear on both [airuntimesecurity.io](https://airuntimesecurity.io/) (runtime) and [aisecuredbydesign.io](https://aisecuredbydesign.io/) (pre-runtime). This page is the **single canonical definition source** for those shared terms. Where the pre-runtime site mentions a shared concept, it links back to the anchor here rather than redefining it, so the two sites cannot drift.

!!! info "How to cite a term"
    Every term below has a stable anchor. Link to it directly, for example `https://airuntimesecurity.io/glossary/#pace` or `https://airuntimesecurity.io/glossary/#risk-tiers`. Keep the heading text stable so the anchors do not change.

## The lifecycle

### Secure by Design

AI security *before* deployment: model selection, platform selection, DevOps, MLOps, data security, and governance. This is the domain of [aisecuredbydesign.io](https://aisecuredbydesign.io/). It decides *what* to enforce and builds the infrastructure that makes enforcement possible.

### AI Runtime Security (AIRS)

AI security *during* runtime: guardrails, reviewing controls, human oversight, and containment applied to a live system. This is the domain of [airuntimesecurity.io](https://airuntimesecurity.io/). It enforces, detects, decides, and contains while the system is serving traffic.

Together, Secure by Design and AIRS form the complete AI security lifecycle. The handoff between them is documented in the [Control Handoff Matrix](infrastructure/handoff-matrix.md).

## The control layers

AIRS is built from three independent control layers plus a containment failsafe. Each does one job, and each keeps working even if the others fail. See [The Architecture](architecture.md) for the full picture.

### Guardrails

**Layer 01.** Deterministic prevention. Guardrails block or constrain known-bad patterns before or during model execution: injection detection, PII handling, content policy, rate limiting, and the tool-call gateway for agents. They are fast, cheap, and inspectable, but they can only catch what a rule can name. See [How guardrails are built](core/controls.md).

### Model-as-Judge

**Layer 02.** Probabilistic detection. A model weighs a response against policy, context, and declared intent to surface the unknown-bad that a fixed rule cannot name. Because the Judge is itself a model, it is probabilistic and can be fooled: it informs the decision rather than making the final call, and never replaces the deterministic guardrails beneath it. See [When the judge can be fooled](core/when-the-judge-can-be-fooled.md).

### Semantic firewall

The intent-level check that sits between Guardrails and Model-as-Judge, catching prohibited *intent* expressed in novel wording that a pattern-matching guardrail would miss. See [Semantic Firewall](core/controls/semantic-firewall.md).

### Human Oversight

**Layer 03.** Human judgment on high-consequence decisions: review, approval, investigation, and adjustment. Human oversight is where accountability lives. Its infrastructure counterpart is the approval workflow (IAM-05). See also [Humans in the Business Process (HITBP)](extensions/technical/humans-in-the-business-process.md), which places the human at the point in the workflow where the decision actually matters.

### Circuit breaker

The containment failsafe behind the three layers. When guardrails, the Judge, and human oversight are all overwhelmed or bypassed, the circuit breaker trips and routes to a non-AI path, freezes actions, or kills the session. It operates at the infrastructure layer, independent of the AI stack, and maps to **PACE Emergency**. It contains rather than evaluates, so it is not itself a behavioural layer.

## Agent design principles

### Lethal trifecta

The combination of **access to private data**, **exposure to untrusted content**, and **a way to communicate externally** in one AI system or session. With all three present, a prompt injection can turn into data exfiltration. Term coined by Simon Willison. Removing any one leg closes the path. Design patterns that do this are on [aisecuredbydesign.io](https://aisecuredbydesign.io/core/injection-resistant-design/).

### Rule of Two

Meta's **Agents Rule of Two**: within one session, an agent should hold no more than two of (A) processing untrusted input, (B) access to sensitive systems or private data, and (C) the ability to change state or communicate externally. A session that needs all three must not run autonomously and requires human approval or equivalent validation. It is a design-time rule, enforced at runtime by the tool gateway, credentials, and network controls. See [Injection-Resistant Design](https://aisecuredbydesign.io/core/injection-resistant-design/#the-agents-rule-of-two).

## Resilience and operating models

### PACE

**Primary, Alternate, Contingency, Emergency.** A resilience-planning methodology borrowed from military communications: every mission-critical function has four pre-defined fallback layers, each on a different failure domain, so a single event cannot cascade through all of them. In AIRS, PACE runs on two axes: **horizontal** across the control layers (Guardrails → Judge → Human → Circuit Breaker) and **vertical** within each layer. See [PACE Resilience](pace-resilience.md).

### ASO

**Agent Security Operations.** AIRS applied to a single system: one model, one boundary, three layers, and a circuit breaker. The foundation that MASO extends to a fleet. See [ASO](aso/index.md).

### MASO

**Multi-Agent Security Operations.** Risk-proportionate runtime controls for systems where many AI agents collaborate: the same three control layers plus the circuit breaker, now governing what agents do to each other, to data, to tools, and to the truth. Organised into eleven control domains. See [MASO](maso/README.md).

### Objective Intent

The anchor concept in MASO: an agent's declared, machine-checkable objective, against which its actions are evaluated. Everything in the MASO control set inherits from it. See [Objective Intent](maso/controls/objective-intent.md).

### Fail posture

The pre-declared behaviour of a control when it fails: **fail-closed** (block on failure, default for higher tiers) or **fail-open** (allow on failure). Every control must have a defined fail posture before production, per PACE.

## Risk classification

### Risk tiers

The four named tiers that scale controls to the harm a system could cause: **LOW**, **MEDIUM**, **HIGH**, **CRITICAL**. The purpose is proportionality: identify the controls you need and consciously deselect the ones you do not. See [Risk Tiers](core/risk-tiers.md).

### Simplified tiers (Tier 1/2/3)

A three-tier operational shorthand used by PACE and specialised controls, mapping to the named tiers:

| Simplified | Named | Meaning |
|------------|-------|---------|
| **Tier 1** | LOW, MEDIUM | Internal, no regulated decisions, recoverable errors |
| **Tier 2** | HIGH | Customer-facing, sensitive data, human review before delivery |
| **Tier 3** | CRITICAL | Regulated decisions, autonomous write access, financial/medical/legal |

The `min_tier` field in the [machine-readable catalog](infrastructure/catalog/README.md) uses this 1/2/3 system. MASO reuses Tier 1/2/3 for multi-agent **autonomy** (Supervised → Managed → Autonomous), which is a separate axis from risk.

### Fast Lane

A self-certification path for genuinely low-risk systems (internal, read-only, no regulated data) that lets them skip the full review. See [Fast Lane](fast-lane.md).

## Infrastructure controls

### Infrastructure controls (the 85)

The 85 technical controls that make behavioural security enforceable, across identity, logging, network, data, secrets, supply chain, incident response, and four agentic domains. airuntimesecurity.io is authoritative for their definitions; aisecuredbydesign.io mirrors them into the pre-runtime lifecycle. See the [Infrastructure Controls Reference](infrastructure/reference.md) and the [machine-readable catalog](infrastructure/catalog/README.md).

### Control ID scheme

Every infrastructure control has a stable ID of the form `PREFIX-NN`. The prefix names the domain:

| Prefix | Domain | Prefix | Domain |
|--------|--------|--------|--------|
| `IAM` | Identity & Access | `IR` | Incident Response |
| `LOG` | Logging & Observability | `TOOL` | Agentic - Tool Access |
| `NET` | Network & Segmentation | `SESS` | Agentic - Session & Scope |
| `DAT` | Data Protection | `DEL` | Agentic - Delegation Chains |
| `SEC` | Secrets & Credentials | `SAND` | Agentic - Sandbox Patterns |
| `SUP` | Supply Chain | | |

### AI-BOM

**AI Bill of Materials.** A maintained inventory of the models, datasets, tools, and dependencies a system uses, so coverage and provenance can be verified systematically (SUP-07). The AI analogue of a software SBOM.

!!! info "References"
    - [The Architecture](architecture.md)
    - [PACE Resilience](pace-resilience.md)
    - [MASO Framework](maso/README.md)
    - [Risk Tiers](core/risk-tiers.md)
    - [Infrastructure Controls Reference](infrastructure/reference.md)
    - [Secure by Design (aisecuredbydesign.io)](https://aisecuredbydesign.io/)
