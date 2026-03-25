---
description: "How ETSI's Securing Artificial Intelligence (SAI) and Experiential Networked Intelligence (ENI) standards affect the Multi-Agent Security Operations (MASO) framework: standard-by-standard alignment with gap analysis."
---

# ETSI Standards Impact on MASO

**How European AI security and multi-agent standards shape MASO controls, and where MASO already meets or exceeds their requirements.**

> *Part of [Regulatory Alignment](README.md) · Review date: March 2026*

## Why ETSI Matters for MASO

ETSI has two Industry Specification Groups (ISGs) directly relevant to multi-agent AI security. **ETSI SAI** (Securing Artificial Intelligence) defines the threat landscape, mitigation strategies, and testing methods for AI systems. **ETSI ENI** (Experiential Networked Intelligence) studies multi-agent architectures, collaboration patterns, and agent topology design. Together, they form the most comprehensive European standards body for the security of AI agent systems.

For organisations operating multi-agent systems under European regulation, ETSI standards sit alongside the EU AI Act as the technical implementation layer. The EU AI Act says *what* must be achieved. ETSI standards say *how* to demonstrate it. MASO provides the operational controls that satisfy both.

## ETSI SAI: The AI Security Standards

The ETSI SAI group has published a series of Group Reports (GRs) and Group Specifications (GSs) addressing AI security from threat identification through to mitigation and testing. The table below maps each to its MASO relevance.

| Standard | Title | Status | MASO Relevance |
|----------|-------|--------|----------------|
| GR SAI 001 | AI Threat Ontology | Published | High |
| GR SAI 002 | Data Supply Chain Security | Published | High |
| GR SAI 004 | Problem Statement on AI Threats | Published | Medium |
| GR SAI 005 | Mitigation Strategy Report | Published | High |
| GR SAI 006 | Role of Hardware in AI Security | Published | Low |
| GR SAI 008 | AI Model Security | Published | High |
| GR SAI 010 | Automated Testing of AI | Published | High |
| GR SAI 011 | AI Computing Platform Security | Published | Medium |
| TR 104 159 | Securing GenAI and LLMs | Published (2025) | Critical |

### GR SAI 001: AI Threat Ontology

**Scope:** Catalogues threats to AI systems across the lifecycle, including data poisoning, model evasion, model inversion, and supply chain compromise.

**MASO alignment:**

| SAI 001 Threat Category | MASO Control Domain | MASO Coverage |
|--------------------------|---------------------|---------------|
| Data poisoning | Data Protection (Domain 2) | Memory poisoning detection, RAG integrity validation |
| Model evasion / adversarial inputs | Prompt, Goal & Epistemic Integrity (Domain 0) | Input sanitisation, epistemic controls |
| Model inversion / extraction | Execution Control (Domain 3) | Sandboxed execution, tool parameter allow-lists |
| Supply chain compromise | Supply Chain (Domain 5) | AIBOM, model provenance, MCP server vetting |
| Deployment environment attacks | Environment Containment (cross-cutting) | API hardening, opaque error responses |

**Assessment:** MASO's [Emergent Risk Register](../../maso/controls/risk-register.md) extends SAI 001's ontology with nine epistemic risks (EP-01 through EP-09) that have no equivalent in the ETSI taxonomy, including hallucination amplification, groupthink propagation, and uncertainty stripping across agent chains. SAI 001 was written for single-model systems. MASO fills the multi-agent gap.

### GR SAI 002: Data Supply Chain Security

**Scope:** Addresses risks in the data supply chain for AI, including training data integrity, data provenance, and third-party data sources.

**MASO alignment:**

| SAI 002 Requirement | MASO Control | Implementation |
|---------------------|-------------|----------------|
| Data provenance tracking | Supply Chain (Domain 5) | AIBOM generation, model provenance tracking |
| Training data integrity | Data Protection (Domain 2) | RAG integrity validation, cross-agent data fencing |
| Third-party data source vetting | Supply Chain (Domain 5) | A2A trust chain validation, signed manifests |
| Continuous data monitoring | Observability (Domain 4) | Behavioural drift detection, anomaly scoring |

**Assessment:** Strong alignment. SAI 002 focuses on training-time data risks. MASO extends this into runtime, where agents consume, transform, and pass data between themselves. The [Data Protection](../../maso/controls/data-protection.md) controls cover inter-agent data classification and DLP scanning on the message bus, which SAI 002 does not address.

### GR SAI 005: Mitigation Strategy Report

**Scope:** Provides a mitigation framework for AI security threats, organised by attack surface and lifecycle phase.

**MASO alignment:**

| SAI 005 Mitigation Area | MASO Equivalent | Notes |
|--------------------------|-----------------|-------|
| Input validation and sanitisation | Guardrails (Layer 1) | MASO applies this at every agent boundary, not just user-facing |
| Model hardening | Not in scope | MASO is a deployer framework; model training is upstream |
| Output filtering | Judge evaluation (Layer 2) | Model-as-Judge with measurable criteria |
| Human oversight | HITL (Layer 3) | PACE escalation model scales oversight to risk |
| Monitoring and logging | Observability (Domain 4) | Flight Recorder, immutable decision chain logs |
| Incident response | Environment Containment | Kill switches external to agent orchestration |

**Assessment:** SAI 005 is the closest ETSI standard to MASO's three-layer defence model. The key difference: SAI 005 treats mitigations as a flat list. MASO arranges them into layers (guardrails, Judge, human) and tiers (Supervised, Managed, Autonomous) that scale controls to demonstrated trustworthiness.

### GR SAI 008: AI Model Security

**Scope:** Addresses security of AI models themselves, including integrity verification, access controls, and protection against extraction attacks.

**MASO alignment:**

| SAI 008 Requirement | MASO Control Domain | Coverage |
|---------------------|---------------------|----------|
| Model integrity verification | Supply Chain (Domain 5) | Model provenance, runtime integrity checks |
| Model access control | Identity & Access (Domain 1) | Per-agent NHI, scoped credentials, zero-trust |
| Anti-extraction measures | Execution Control (Domain 3) | Sandboxed execution, rate limiting |
| Model lifecycle management | Observability (Domain 4) | Behavioural drift detection against baselines |

**Assessment:** Strong alignment on model access and integrity. SAI 008 does not address the multi-agent dimension where one agent could attempt to extract information from another agent's model through inter-agent messaging. MASO's [Secure Inter-Agent Message Bus](../../maso/README.md) with signed, rate-limited communication addresses this gap.

### GR SAI 010: Automated Testing of AI

**Scope:** Defines methods for automated security testing of AI systems, covering adversarial testing, robustness evaluation, and continuous assessment.

**MASO alignment:**

| SAI 010 Test Method | MASO Equivalent | Tier Applicability |
|---------------------|-----------------|--------------------|
| Adversarial input testing | [Red Team Playbook](../../maso/red-team/red-team-playbook.md) | All tiers |
| Robustness evaluation | [Stress Testing at Scale](../../maso/stress-test/) | Tier 2+ |
| Continuous monitoring | Observability (Domain 4), anomaly scoring | All tiers |
| Regression testing | Judge evaluation baselines | Tier 2+ |

**Assessment:** SAI 010 provides a useful taxonomy for AI testing but does not cover multi-agent specific scenarios like cascading failure propagation, inter-agent prompt injection, or epistemic degradation across chains. MASO's Red Team Playbook and stress testing documents address these gaps directly.

### TR 104 159: Securing Generative AI and LLMs

**Scope:** ETSI's most recent and directly relevant publication. Addresses security risks specific to generative AI and large language models, including prompt injection, hallucination, data leakage, and jailbreaking.

**MASO alignment:**

| TR 104 159 Risk | MASO Control | Domain |
|-----------------|-------------|--------|
| Prompt injection | Input sanitisation, system prompt isolation | Domain 0 |
| Hallucination | Epistemic controls, Judge evaluation | Domain 0 |
| Data leakage | Output DLP, cross-agent data fencing | Domain 2 |
| Jailbreaking | Guardrails (Layer 1), immutable task specs | Domain 0 |
| Insecure plugin/tool use | Tool parameter allow-lists, sandboxed execution | Domain 3 |
| Excessive agency | PACE escalation, blast radius caps | Domain 3 |
| Training data poisoning | RAG integrity validation | Domain 2 |

**Assessment:** This is the ETSI standard with the strongest overlap to MASO's scope. TR 104 159 addresses single-LLM risks that MASO amplifies into the multi-agent context. Where TR 104 159 warns about prompt injection on one model, MASO addresses prompt injection propagation across agent chains. Where TR 104 159 flags hallucination, MASO addresses hallucination amplification when multiple agents build on each other's outputs without independent verification.

## ETSI ENI: Multi-Agent Architecture Standards

ETSI's Experiential Networked Intelligence group has produced the only formal standards work on multi-agent system architecture. While ENI focuses on telecommunications networks, its architectural patterns and security considerations apply broadly to any multi-agent deployment.

### GR ENI 056: Study on Multi-Agent Systems (2025)

**Scope:** Studies multi-agent system architectures, covering agent topologies, conversation patterns, workflow orchestration, and closed-loop optimisation. Reviews existing open-source frameworks (LangGraph, AutoGen, CrewAI) and recommends architectural design principles.

This is the most directly relevant ETSI standard for MASO.

| ENI 056 Topic | MASO Equivalent | Alignment |
|---------------|-----------------|-----------|
| Agent topologies (hierarchical, flat, hybrid) | MASO tier architecture (Supervised, Managed, Autonomous) | **Complementary**: ENI 056 describes topology patterns; MASO prescribes security controls per topology |
| Agent-to-agent communication | Secure Inter-Agent Message Bus | **MASO extends**: ENI 056 describes communication models; MASO requires signed, rate-limited, validated messaging |
| Workflow orchestration | Execution Control (Domain 3), Privileged Agent Governance (Domain 6) | **MASO extends**: MASO adds security governance for orchestrators with elevated authority |
| Closed-loop optimisation | PACE resilience model | **Complementary**: ENI 056 optimises for performance; MASO optimises for safe degradation |
| Agent collaboration mechanisms | Objective Intent (Domain 7), OISpec contracts | **MASO extends**: ENI 056 describes how agents collaborate; MASO ensures they collaborate within declared intent boundaries |

**Assessment:** ENI 056 provides the architectural vocabulary. MASO provides the security controls. Organisations should use ENI 056 to inform their multi-agent architecture design and MASO to secure it. The two standards do not conflict, and ENI 056 explicitly acknowledges that security and trust mechanisms are needed but outside its scope.

### GR ENI 051: AI Agents for Network Slicing (2025)

**Scope:** Studies how AI agents can manage next-generation network slicing, including resource allocation, SLA enforcement, and autonomous network management.

| ENI 051 Concept | MASO Parallel | Notes |
|-----------------|---------------|-------|
| Autonomous resource allocation | Tier 3 (Autonomous) controls | Both address agents with authority to allocate resources without human approval |
| SLA enforcement by agents | OISpec as intent contract | Both define structured specifications that constrain agent behaviour |
| Agent delegation patterns | Privileged Agent Governance (Domain 6) | MASO applies mandatory approval gates and delegation limits |

**Assessment:** Domain-specific to telecoms, but the patterns are transferable. Any organisation deploying autonomous agents that allocate resources (cloud compute, API quotas, budget) faces the same governance challenges ENI 051 identifies for network slicing.

### GR ENI 055: AI-Core Network Architecture (2025)

**Scope:** Proposes use cases for AI-agent-based core network architecture, covering B2C, B2B, and internal operator scenarios.

**MASO relevance:** Lower direct relevance. The use cases are telecoms-specific, but the architectural principle of rebuilding core infrastructure around collaborating agents validates MASO's premise that multi-agent security requires a dedicated control framework, not just extensions to single-model controls.

## Gap Analysis: What ETSI Requires That MASO Addresses

| Gap in ETSI Standards | MASO Coverage |
|-----------------------|---------------|
| Multi-agent prompt injection propagation | Domain 0: cross-agent input sanitisation, system prompt isolation |
| Epistemic risks (groupthink, uncertainty stripping) | Domain 0: nine epistemic risks (EP-01 to EP-09) |
| Transitive privilege escalation | Domain 1: no inherited permissions, Domain 6: delegation limits |
| Inter-agent data leakage | Domain 2: cross-agent data fencing, message bus DLP |
| Orchestrator compromise | Domain 6: mandatory human approval gates, independent monitoring |
| Cascading failure across agent chains | PACE resilience model: Primary, Alternate, Contingency, Emergency |
| Agent identity and authentication | Domain 1: per-agent NHI, zero-trust mutual authentication |
| Runtime behavioural assurance | Domain 7: OISpec contracts, tactical and strategic evaluation |

## Gap Analysis: What ETSI Covers That MASO Does Not

| ETSI Coverage | MASO Position | Recommendation |
|---------------|---------------|----------------|
| Hardware-level AI security (SAI 006) | Out of scope | Correct scoping. MASO is a deployer framework. Hardware security is infrastructure. |
| AI model training security | Out of scope | Correct scoping. MASO secures deployed agents, not the training pipeline. |
| AI for cybersecurity operations | Out of scope | Correct scoping. MASO secures AI, not AI-for-security. |
| Telecoms-specific agent topology (ENI 055) | Not addressed | No action needed. Domain-specific applications do not require framework changes. |
| Formal verification of AI models (SAI 010 advanced) | Partial | [Stress Testing](../../maso/stress-test/) covers runtime verification. Formal methods for model internals are outside MASO scope. |

## Compliance Mapping Summary

For organisations needing to demonstrate ETSI alignment, the following table maps each MASO control domain to the ETSI standards it satisfies.

| MASO Control Domain | ETSI Standards Addressed | Primary Evidence |
|---------------------|--------------------------|------------------|
| 0. Prompt, Goal & Epistemic Integrity | SAI 001, SAI 005, TR 104 159 | Input sanitisation logs, epistemic monitoring alerts, goal integrity reports |
| 1. Identity & Access | SAI 008, ENI 056 | NHI registry, credential rotation logs, authentication audit trail |
| 2. Data Protection | SAI 002, TR 104 159 | DLP scan results, data classification tags, RAG integrity checks |
| 3. Execution Control | SAI 001, SAI 005, SAI 008, TR 104 159 | Sandbox configurations, tool allow-lists, blast radius cap settings |
| 4. Observability | SAI 005, SAI 010 | Flight Recorder exports, drift detection baselines, SIEM integration |
| 5. Supply Chain | SAI 002, SAI 008 | AIBOM records, signed manifests, A2A trust chain validations |
| 6. Privileged Agent Governance | ENI 056, ENI 051 | Approval gate logs, delegation limit configurations, independent monitor reports |
| 7. Objective Intent | ENI 056 | OISpec version history, tactical/strategic evaluation results |
| Environment Containment | SAI 001, SAI 005, TR 104 159 | API hardening configs, kill switch test results, WAF/DLP rules |

## Practical Implications by MASO Tier

### Tier 1 (Supervised)

ETSI alignment is straightforward at this tier. Human-in-the-loop oversight satisfies most SAI 005 mitigation requirements without additional tooling. The main ETSI-driven additions:

- Document agent threat model against SAI 001 ontology
- Log all agent actions per SAI 010 continuous monitoring requirements
- Apply TR 104 159 prompt injection mitigations even for supervised agents

### Tier 2 (Managed)

ETSI requirements start to bite at this tier. Automated controls must compensate for reduced human oversight:

- Implement SAI 010 automated testing as part of the Judge evaluation pipeline
- Apply SAI 002 data provenance controls to all inter-agent data flows
- Use ENI 056 topology patterns to validate your multi-agent architecture design

### Tier 3 (Autonomous)

Full ETSI alignment becomes essential. Autonomous agents operating without human approval need demonstrable compliance:

- Full SAI 001 threat ontology mapping in the risk register
- Continuous automated testing per SAI 010 at runtime, not just pre-deployment
- ENI 056 architecture validation for all agent topologies
- TR 104 159 mitigations enforced at every agent boundary, including inter-agent
- SAI 008 model integrity verification on every model load and update

!!! info "References"
    - [ETSI SAI: Securing Artificial Intelligence](https://www.etsi.org/technologies/securing-artificial-intelligence)
    - [ETSI GR SAI 001: AI Threat Ontology](https://www.etsi.org/deliver/etsi_gr/SAI/001_099/001/01.01.01_60/gr_SAI001v010101p.pdf)
    - [ETSI GR SAI 005: Mitigation Strategy Report](https://www.etsi.org/deliver/etsi_gr/SAI/001_099/005/01.01.01_60/gr_SAI005v010101p.pdf)
    - [ETSI TR 104 159: Securing Generative AI and LLMs](https://www.etsi.org/deliver/etsi_tr/104100_104199/104159/)
    - [ETSI GR ENI 056: Study on Multi-Agent Systems](https://www.etsi.org/deliver/etsi_gr/ENI/001_099/056/04.01.01_60/gr_ENI056v040101p.pdf)
    - [ETSI ENI: Experiential Networked Intelligence](https://www.etsi.org/technologies/experiential-networked-intelligence)
    - [MASO Framework](../../maso/README.md)
