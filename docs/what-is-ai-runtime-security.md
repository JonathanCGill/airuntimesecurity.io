---
title: What is AI Runtime Security?
description: "AI Runtime Security (AIRS) is the discipline of reducing harm caused by AI systems during live operation. It provides risk-proportionate controls that organisations can select, adapt, or consciously deselect based on their own risk appetite and context."
---

# What is AI Runtime Security?

**AI Runtime Security (AIRS)** is the discipline of reducing harm caused by AI systems during live operation, rather than relying solely on design-time testing or model evaluation.

It addresses a gap that existing security disciplines do not cover: the period between deployment and decommission, when AI systems interact with real users, real data, and real business processes, and when their behaviour can diverge from what was tested, expected, or authorised. The framework provides risk-oriented control patterns that organisations select based on their own risk appetite, applying the right controls at the right time for the right purposes.

## Definition

> AI Runtime Security is the practice of identifying, assessing, and treating threats to the confidentiality, integrity, and availability of AI systems in production. It applies defence-in-depth principles at the point of execution, treating deployment as the beginning of the risk lifecycle rather than the end of it.

## Scope

AI Runtime Security covers the operational phase of AI systems. It is concerned with what AI systems actually do, not what they were designed to do.

| In scope | Out of scope |
|----------|-------------|
| Runtime behavioural controls | Model training and fine-tuning |
| Production monitoring and observability | Pre-deployment red-teaming (as standalone) |
| Automated evaluation of live outputs | Dataset curation and provenance |
| Human oversight and escalation | Model architecture selection |
| Incident response for AI-specific failures | Prompt engineering best practices |
| Multi-agent coordination security | AI ethics and fairness (as standalone) |
| Regulatory evidence from live operation | Theoretical alignment research |

This does not mean pre-deployment activities are unimportant. They are necessary but insufficient. A model that passed every evaluation can still hallucinate a regulatory disclosure, leak PII through a tool call, or take an action in an agent chain that no human authorised.

### AI You Build vs. AI You Consume

The full framework (three-layer controls, PACE resilience, risk tiers, MASO) is designed for **AI systems your organisation develops and operates**: custom models, RAG pipelines, autonomous agents, and multi-agent systems. These are the systems where you own the runtime and bear full responsibility for behaviour in production.

Most organisations also consume AI through vendor platforms (copilots, SaaS features, cloud AI services). For consumed AI, the security questions are different: data classification, access governance, platform control configuration, and understanding what the vendor does and does not secure on your behalf. The framework's [maturity levels](strategy/maturity-levels.md) address how these tracks differ and what good practice looks like for each.

## Core Controls

AI Runtime Security is built on layered, independent controls that compensate for each other's weaknesses:

**Guardrails** are fast, deterministic boundaries that enforce content policies, scope constraints, and tool-use permissions at the point of execution.

**Model-as-Judge** is an independent model that evaluates the primary model's outputs against policy, context, and intent before those outputs reach users or downstream systems. The Judge can be a large LLM for async assurance or a [distilled SLM](extensions/technical/distill-judge-slm.md) for inline, real-time evaluation.

**Human Oversight** provides structured escalation paths, audit trails, and intervention capability for high-risk decisions and anomaly-triggered review.

**Circuit Breakers** are emergency failsafes that halt AI operations and activate safe fallbacks when controls themselves fail or when confirmed compromise is detected.

Each layer operates independently. No single failure compromises the system.

## Relationship to Existing Security Domains

AI Runtime Security does not replace existing security disciplines. It extends them into a domain they were not designed to cover.

| Existing discipline | What it secures | Where AIRS extends it |
|--------------------|----------------|----------------------|
| Application Security | Code, APIs, web applications | AI-specific input/output validation, prompt injection defence |
| Network Security | Traffic, segmentation, perimeters | Agent-to-agent communication, tool-call routing |
| Identity & Access | Users, roles, permissions | Per-agent identity, delegation chains, transitive authority |
| Data Protection | Storage, transit, classification | Context window leakage, cross-agent data flow, RAG poisoning |
| Incident Response | Detection, containment, recovery | AI-specific failure modes, PACE resilience, circuit breaker activation |
| Security Operations | Monitoring, alerting, investigation | AI behavioural telemetry, judge evaluation pipelines, drift detection |

The principle is not new. Defence-in-depth has always been how we secure complex systems. What is new is applying it systematically to AI runtime behaviour, where the system's outputs are non-deterministic, context-dependent, and capable of autonomous action.

## Why a Discipline, Not Just a Framework

Frameworks get copied. Categories get cited.

AI Runtime Security is not a single product, vendor capability, or proprietary methodology. It is a field of practice that any organisation deploying AI systems in production needs to address. Every organisation has its own structures, risk tolerances, and ways of getting things done. The discipline respects this by providing risk-oriented paths and control patterns that can be adopted, adapted, or consciously deselected based on organisational context.

The [AIRS Framework](ARCHITECTURE.md) is a reference architecture for this discipline: one implementation model that provides controls, patterns, and operational guidance. It is designed so that AI product owners can quickly identify the controls they need and apply them, without being forced into a one-size-fits-all mandate. But the discipline itself is broader than any single framework. It encompasses:

- The [Foundation Framework](foundations/README.md) for single-agent deployments: the three-layer behavioural pattern (Guardrails, Judge, Human Oversight), backed by 80 [infrastructure controls](infrastructure/README.md) across 11 domains.
- [Multi-Agent Security Operations (MASO)](maso/README.md) for autonomous agent coordination, with controls organised into 10 domains
- [Regulatory alignment](extensions/regulatory/eu-ai-act-crosswalk.md) with EU AI Act, ISO 42001, and NIST AI RMF
- [Platform-specific patterns](infrastructure/reference/platform-patterns/aws-bedrock.md) for AWS, Azure, and Databricks


As AI systems grow more autonomous, the need for structured runtime security will only increase. The question is not whether organisations need AI Runtime Security. It is whether they implement it before or after the first production incident forces them to.

## Standards Alignment

AI Runtime Security maps to established regulatory and standards frameworks:

- **EU AI Act**: Article 9 (risk management), Article 14 (human oversight), Article 15 (accuracy and robustness)
- **NIST AI RMF**: GOVERN, MAP, MEASURE, MANAGE functions
- **ISO 42001**: Annex A controls for AI management systems
- **OWASP LLM Top 10 (2025)**: full coverage across runtime control layers
- **OWASP Agentic Top 10 (2026)**: multi-agent specific controls via MASO

---

*[Jonathan Gill](https://www.linkedin.com/in/jonathancgill/) contributes to the AI Runtime Security discipline through the AIRS Framework at [airuntimesecurity.io](https://airuntimesecurity.io).*
