---
description: "Alignment review of the AIRS Framework against the NIST Cybersecurity Framework Profile for Artificial Intelligence (IR 8596), covering all six CSF 2.0 Functions with gap analysis."
---

# NIST IR 8596 Alignment Review

**How the AIRS Framework aligns with the NIST Cybersecurity Framework Profile for Artificial Intelligence (Cyber AI Profile), including gap analysis and enhancement recommendations.**

> *Part of [Regulatory Alignment](README.md) · Review date: March 2026*

## About NIST IR 8596

**Full title:** Cybersecurity Framework Profile for Artificial Intelligence (Cyber AI Profile): NIST Community Profile

**Published:** December 16, 2025 (Initial Preliminary Draft)

**Status:** Public comment period closed. Initial public draft expected 2026.

**Purpose:** Provides guidelines for managing cybersecurity risk related to AI systems and identifies opportunities for using AI to enhance cybersecurity capabilities. Bridges the NIST Cybersecurity Framework (CSF) 2.0 with AI-specific considerations.

**Development:** Over 6,500 contributors from government, academia, and industry. Developed by NIST's National Cybersecurity Center of Excellence (NCCoE).

- [NIST IR 8596 Publication Page](https://csrc.nist.gov/pubs/ir/8596/iprd)
- [NIST IR 8596 PDF](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8596.iprd.pdf)
- [NCCoE Cyber AI Profile Project](https://www.nccoe.nist.gov/projects/cyber-ai-profile)

## Three Focus Areas

NIST IR 8596 organises AI cybersecurity around three overlapping focus areas:

| Focus Area | Shorthand | Description | AIRS Coverage |
|---|---|---|---|
| **Securing AI Systems** | Secure | Identifying cybersecurity challenges when integrating AI into organisational ecosystems and infrastructure | **Primary scope**: this is what AIRS does |
| **Conducting AI-Enabled Cyber Defence** | Defend | Identifying opportunities to use AI to enhance cybersecurity and understanding challenges when leveraging AI for defensive operations | **Out of scope**: AIRS secures AI systems, not AI-for-security |
| **Thwarting AI-Enabled Cyberattacks** | Thwart | Building resilience to protect against new AI-enabled threats (deepfakes, AI-generated phishing, automated vulnerability exploitation) | **Partial**: addressed where AI-enabled attacks target AI systems (e.g., adversarial inputs, prompt injection) |

**Assessment:** This is a correct and intentional scoping decision. AIRS is a deployer-focused framework for securing AI systems in production. The "Defend" and "Thwart" focus areas are cybersecurity operations concerns that belong in SOC playbooks and enterprise security architectures, not in an AI deployment controls framework. The existing [CSF 2.0 mapping](../../infrastructure/mappings/csf-2.0.md) already notes this explicitly.

## Structure and Priority System

IR 8596 is organised as six tables, one per CSF 2.0 Function, with AI-specific considerations for each subcategory. Each subcategory receives a priority rating:

| Priority | Level | Meaning |
|---|---|---|
| 1 | High | Essential for AI cybersecurity; implement first |
| 2 | Moderate | Important but can follow foundational controls |
| 3 | Foundational | Standard cybersecurity practice; AI twist is minimal |

Where no unique AI consideration exists, the profile states "standard cybersecurity practices apply."

## Alignment Assessment by CSF Function

### GOVERN (GV): Strong Alignment

IR 8596 emphasises AI governance, risk strategy, roles/responsibilities, policy, oversight, and supply chain risk management. AI-specific considerations include communicating intended use and known limitations of AI, identifying business outcomes reliant on AI, and continuous monitoring of supplier-provided AI models and datasets.

| IR 8596 Emphasis | AIRS Coverage | Assessment |
|---|---|---|
| Organisational context for AI risk management | [Risk Tiers](../../core/risk-tiers.md), four-level classification (LOW/MEDIUM/HIGH/CRITICAL) based on six dimensions | **Strong** |
| AI risk appetite and tolerance statements | Risk tier boundaries define tolerance per deployment category | **Strong** |
| Roles and responsibilities for AI cybersecurity | [Human Oversight](../../foundations/README.md) layer, escalation paths, [AI Governance Operating Model](ai-governance-operating-model.md) (three lines) | **Strong** |
| AI-specific policy establishment and enforcement | Controls registry enforces policy at infrastructure layer | **Strong** |
| Oversight and continuous improvement | [PACE Resilience](../../PACE-RESILIENCE.md), post-incident review (IR-07, IR-08) | **Strong** |
| AI supply chain risk management | [Supply Chain controls](../../maso/controls/supply-chain.md) (SC-1.1 through SC-3.4), AIBOM, signed manifests, model provenance | **Strong** |
| Communicating intended use and limitations of AI | Not explicitly addressed as a control | **Gap**: see [Recommendation G1](#g1-intended-use-and-limitation-documentation) |
| AI definition flexibility | Framework uses operational definitions (single-model, multi-agent) rather than categorical AI definitions | **Aligned** |

### IDENTIFY (ID): Strong Alignment

IR 8596 urges organisations to maintain inventories covering models, agents, APIs/keys, datasets/metadata, and embedded AI integrations/permissions, plus maps of end-to-end AI data flows.

| IR 8596 Emphasis | AIRS Coverage | Assessment |
|---|---|---|
| AI asset inventory (models, agents, APIs, datasets) | SC-05 (Asset inventory), model registry, risk tier classification per deployment | **Strong** |
| End-to-end AI data flow mapping | [Network & Segmentation](../../infrastructure/README.md) controls, three-layer pipeline data flow documentation | **Strong** |
| AI-specific vulnerability identification | Guardrail patterns (prompt injection, jailbreak vectors), [Red Team Playbook](../../maso/red-team/red-team-playbook.md) (RT-01 through RT-13) | **Strong** |
| AI-specific threat identification | [Threat Intelligence Review](../../maso/threat-intelligence/threat-intelligence-review.md), [Incident Tracker](../../maso/threat-intelligence/incident-tracker.md), [Emerging Threats](../../maso/threat-intelligence/emerging-threats.md) | **Strong** |
| Risk assessment incorporating AI-specific factors | Six-dimension risk scoring, tier-based control selection | **Strong** |
| Embedded AI integrations/permissions inventory | MASO [Identity & Access](../../maso/controls/identity-and-access.md) controls cover agent identity and tool permissions | **Strong** |
| AI data flow boundary enforcement and anomaly detection | [Observability controls](../../maso/controls/observability.md) (OB-1.1 through OB-3.5), behavioral drift detection | **Strong** |

### PROTECT (PR): Strong Alignment

IR 8596 focuses on data provenance and integrity for training and input data, extending supply chain risk management to model and data supply chains, and AI-specific access controls.

| IR 8596 Emphasis | AIRS Coverage | Assessment |
|---|---|---|
| Training/input data provenance and integrity | SC-01 (Provenance verification), SC-02 (Integrity checking) | **Strong** |
| AI-specific identity and access management | [Identity & Access Management](../../infrastructure/README.md) controls, [MASO Identity & Access](../../maso/controls/identity-and-access.md) | **Strong** |
| Data-in-use protection (context windows, inference) | PR.DS-10 mapped to Session & Scope controls, guardrail layer | **Strong**: identified as "Key AI subcategory" in CSF 2.0 mapping |
| Least privilege for AI agents and tools | [Tool Access](../../infrastructure/README.md) controls, TA-based least-privilege, MASO IA-2.3 (no transitive permissions) | **Strong** |
| AI-specific logging and monitoring | [Logging & Observability](../../infrastructure/README.md), prompts, responses, guardrail decisions, Judge evaluations, tool invocations | **Strong** |
| Model and data supply chain extension | Supply Chain controls, AIBOM, dependency scanning | **Strong** |
| AI-specific contractual terms with suppliers | SC controls specify provider requirements | **Moderate**: present but could be more prescriptive |
| Infrastructure resilience for AI systems | Circuit breakers, fallback models, PACE degradation | **Strong** |
| Zero Trust principles applied to AI | Infrastructure-beats-instructions principle, continuous verification at every trust boundary | **Strong** |
| Adversarial robustness and input validation | Guardrail layer, injection detection, input/output validation | **Strong** |

### DETECT (DE): Strong Alignment

IR 8596 addresses monitoring AI systems for adversarial behaviours and anomalies, with guidance on adversarial input pattern detection.

| IR 8596 Emphasis | AIRS Coverage | Assessment |
|---|---|---|
| Runtime monitoring for adversarial inputs | Guardrail layer (Layer 1), real-time pattern matching, ~10ms | **Strong** |
| AI output evaluation against policy | Model-as-Judge layer (Layer 2), independent model evaluation, ~500ms-5s | **Strong** |
| Behavioural anomaly detection | [Observability controls](../../maso/controls/observability.md), behavioral drift detection | **Strong** |
| Correlation across multiple AI telemetry sources | LO controls correlate guardrail + Judge + human override + model telemetry | **Strong** |
| Adversarial input pattern detection | RegexGuardrail (30+ default patterns), extensible guardrail chain | **Strong** |
| AI-specific incident declaration criteria | IR controls define AI-specific criteria: sustained guardrail bypass, Judge degradation, confirmed data leakage | **Strong** |

### RESPOND (RS): Strong Alignment

IR 8596 emphasises extending incident response to AI-specific scenarios, including supplier coordination.

| IR 8596 Emphasis | AIRS Coverage | Assessment |
|---|---|---|
| AI-specific incident response playbooks | [Incident Response](../../infrastructure/README.md) controls, AI-specific playbooks for model compromise, prompt injection campaigns, agent misbehaviour | **Strong** |
| AI-specific containment (circuit breakers, tool revocation) | Circuit breakers disable model endpoints, TA controls revoke tool access, NS controls isolate segments | **Strong** |
| AI-specific eradication (model rollback, cache purge) | Model rollback, guardrail/Judge criteria reset, credential rotation, cache purge procedures | **Strong** |
| Supplier coordination during AI incidents | IR controls specify notification to model providers | **Moderate** |
| Forensic analysis of AI incidents | Prompt/response logs, guardrail decision logs, Judge evaluation records, tool invocation history | **Strong** |
| Tamper-evident logging | LO controls ensure tamper-evident logging | **Strong** |

### RECOVER (RC): Strong Alignment

IR 8596 covers recovery plan execution for AI systems and stakeholder communication during recovery.

| IR 8596 Emphasis | AIRS Coverage | Assessment |
|---|---|---|
| AI system recovery (model re-deployment from verified source) | IR controls, Supply Chain integrity verification before restoration | **Strong** |
| Post-recovery behavioural validation | Heightened logging, reduced autonomy, tighter guardrail thresholds until confidence restored | **Strong** |
| Recovery prioritisation by risk tier | Risk tier determines recovery priority and sequence | **Strong** |
| Integrity verification of restored AI assets | Model weights and configuration integrity verification, guardrail/Judge re-validation | **Strong** |
| Stakeholder communication during recovery | IR controls specify notification procedures | **Moderate** |

## Overall Alignment Summary

| CSF Function | IR 8596 Subcategories | AIRS Mapped | Coverage | Rating |
|---|---|---|---|---|
| **GOVERN** | ~25 | 23 | 92% | Strong |
| **IDENTIFY** | ~19 | 19 | 100% | Strong |
| **PROTECT** | ~21 | 21 | 100% | Strong |
| **DETECT** | ~11 | 11 | 100% | Strong |
| **RESPOND** | ~13 | 13 | 100% | Strong |
| **RECOVER** | ~8 | 8 | 100% | Strong |

**Overall: Strong alignment.** The AIRS Framework covers the "Secure" focus area of IR 8596 comprehensively. The existing [CSF 2.0 mapping](../../infrastructure/mappings/csf-2.0.md) already provides subcategory-level traceability.

## Identified Gaps and Recommendations

Despite strong overall alignment, the review identified areas where the framework could strengthen its IR 8596 alignment.

### G1: Intended Use and Limitation Documentation

**IR 8596 reference:** GV, Communicating the intended use and known limitations of AI systems.

**Current state:** The framework assumes deployers define use cases through risk tier classification, but does not explicitly require documentation of intended use boundaries or known model limitations as a control.

**Recommendation:** Add guidance in the [Risk Tiers](../../core/risk-tiers.md) documentation recommending that each AI deployment's risk tier assessment include: (a) documented intended use statement, (b) known model limitations relevant to the use case, and (c) out-of-scope use identification. This aligns with EU AI Act Article 13 (transparency) requirements already mapped elsewhere.

**Priority:** Low. The risk tier classification implicitly achieves much of this. Explicit documentation would strengthen audit evidence.

### G2: AI-Specific Contractual Guidance

**IR 8596 reference:** GV.SC-05, Requirements to address cybersecurity risks in supply chains are established and integrated into contracts.

**Current state:** Supply chain controls specify what to require from model providers (integrity verification, provenance data, vulnerability disclosure) but don't provide template contract language or a checklist of AI-specific contractual terms.

**Recommendation:** Consider adding a contractual requirements checklist in the [Supply Chain controls](../../maso/controls/supply-chain.md) covering: model update notification requirements, security incident disclosure timelines, data retention and deletion obligations, performance degradation notification, and right-to-audit provisions for AI-specific concerns.

**Priority:** Low. This is operational guidance rather than a control gap.

### G3: Defend and Thwart Focus Area Acknowledgement

**IR 8596 reference:** Focus areas 2 (Defend) and 3 (Thwart).

**Current state:** The CSF 2.0 mapping correctly notes these are out of scope. However, the framework doesn't discuss how organisations should address these complementary focus areas alongside AIRS controls.

**Recommendation:** Add a brief section in the CSF 2.0 mapping or this document noting that organisations implementing AIRS should also address the "Defend" and "Thwart" focus areas through their SOC operations, threat intelligence programmes, and enterprise security architecture. Cross-reference to relevant resources (MITRE ATLAS for Thwart, existing SOC AI integration guidance for Defend).

**Priority:** Low. This is guidance, not a control gap.

### G4: AI-Specific Training and Awareness

**IR 8596 reference:** PR.AT-01, PR.AT-02, Training and awareness for AI cybersecurity.

**Current state:** The CSF 2.0 mapping marks these as "Organisational practice, not infrastructure control" and out of scope. This is reasonable for a controls framework, but IR 8596 assigns these moderate priority with AI-specific considerations (e.g., training staff to recognise AI-generated content, understanding AI-specific attack vectors).

**Recommendation:** Consider adding a brief note in the [Human Oversight](../../foundations/README.md) documentation that effective human oversight depends on trained reviewers who understand AI-specific risks (hallucination patterns, prompt injection indicators, confidence calibration). This doesn't require new controls but acknowledges the dependency.

**Priority:** Low. Valid scoping decision. Brief acknowledgement would strengthen completeness.

### G5: Priority Rating Cross-Reference

**IR 8596 reference:** Priority 1/2/3 ratings across all subcategories.

**Current state:** The CSF 2.0 mapping provides control-level traceability but does not cross-reference IR 8596's priority ratings.

**Recommendation:** Consider adding IR 8596 priority ratings to the CSF 2.0 mapping table. This would help organisations that are using IR 8596 as their primary planning tool understand which AIRS controls address their highest-priority subcategories.

**Priority:** Medium. Practical value for organisations implementing both frameworks simultaneously.

## Strengths Relative to IR 8596

The AIRS Framework exceeds IR 8596's guidance in several areas:

### 1. Runtime Behavioural Controls

IR 8596, as a CSF profile, is outcome-oriented: it describes *what* to achieve. AIRS provides the *how* with a concrete three-layer architecture (guardrails → Judge → human oversight) and the PACE resilience model. This is the gap IR 8596 explicitly acknowledges exists between framework guidance and operational implementation.

### 2. Multi-Agent Security

IR 8596 does not specifically address multi-agent system risks. AIRS's [MASO framework](../../maso/README.md) provides controls across 10 domains specifically for multi-agent orchestration, covering epistemic integrity, cross-agent data fencing, delegation tracking, privileged agent governance, model cognition assurance, agentic task contracts, and objective intent. As agentic AI adoption accelerates, this is a significant area where AIRS provides guidance that IR 8596 does not yet cover.

### 3. Operational Resilience Patterns

IR 8596 references resilience in general terms. AIRS provides the [PACE resilience model](../../PACE-RESILIENCE.md) with concrete state machine definitions, transition criteria, and per-state control requirements, a production-ready implementation pattern rather than aspirational guidance.

### 4. Defence-in-Depth Architecture

IR 8596 recommends layered controls but does not prescribe a specific architecture. AIRS's complementary principle ("Guardrails prevent. Judge detects. Humans decide. Circuit breakers contain.") provides an actionable architecture where each layer compensates for the others' blind spots.

### 5. Threat Intelligence Integration

AIRS maintains a living [Incident Tracker](../../maso/threat-intelligence/incident-tracker.md), [Emerging Threats](../../maso/threat-intelligence/emerging-threats.md) register, and [Red Team Playbook](../../maso/red-team/red-team-playbook.md) that ground controls in demonstrated (not theoretical) risk. IR 8596 references threat intelligence as an input but does not provide AI-specific threat catalogues.

### 6. Agent-Specific Controls

IR 8596 addresses AI systems broadly. AIRS provides specific controls for agent-specific risks including: tool-use escalation, delegation chain tracking, non-human identity management, execution sandboxing, blast radius containment, and memory poisoning detection, all areas where the threat landscape has evolved significantly since IR 8596's drafting.

## Complementary Frameworks

IR 8596 references several frameworks that AIRS also aligns with, reinforcing the convergence of the broader AI security landscape:

| Referenced by IR 8596 | AIRS Alignment Document |
|---|---|
| NIST AI RMF 1.0 | [NIST AI RMF Mapping](../../infrastructure/mappings/nist-ai-rmf.md) |
| NIST SP 800-218A | [SP 800-218A Mapping](../../infrastructure/mappings/nist-sp800-218a.md) |
| OWASP AI Security Guides | [OWASP LLM Top 10 Mapping](../../infrastructure/mappings/owasp-llm-top10.md) |
| MITRE ATLAS | Referenced in [MASO Threat Intelligence Review](../../maso/threat-intelligence/threat-intelligence-review.md) |
| ISO/IEC 42001 | [ISO 42001 Alignment](iso-42001-alignment.md) |

In addition, IR 8596 notes NIST is developing **SP 800-53 Control Overlays for Securing AI Systems (COSAiS)**, implementation-level controls that complement the Cyber AI Profile's outcome-oriented guidance. When COSAiS is published, a separate alignment review should be conducted, as it will likely map more directly to AIRS's infrastructure control level.

## Conclusion

The AIRS Framework demonstrates **strong alignment** with NIST IR 8596's "Secure" focus area across all six CSF 2.0 Functions. The existing [CSF 2.0 mapping](../../infrastructure/mappings/csf-2.0.md) provides comprehensive subcategory-level traceability, and the five identified gaps are minor, primarily documentation enhancements rather than control deficiencies.

More significantly, AIRS **extends beyond** what IR 8596 currently covers in several critical areas: multi-agent security, operational resilience patterns, runtime behavioural architecture, and agent-specific threat models. As NIST develops the initial public draft (expected 2026), these areas may receive expanded coverage, positioning AIRS as an early implementer of controls that the regulatory landscape is moving toward.

**Recommended actions:**

1. Add IR 8596 priority ratings to the existing CSF 2.0 mapping (G5), **medium priority**
2. Add intended use documentation guidance to risk tier process (G1), **low priority**
3. Monitor NIST's development of the initial public draft and COSAiS for alignment updates
4. Add NIST IR 8596 to [REFERENCES.md](../../REFERENCES.md) as a primary reference

!!! info "References"
    - [NIST IR 8596: Cybersecurity Framework Profile for Artificial Intelligence](https://csrc.nist.gov/pubs/ir/8596/iprd)
    - [NIST IR 8596 PDF](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8596.iprd.pdf)
    - [NCCoE Cyber AI Profile Project](https://www.nccoe.nist.gov/projects/cyber-ai-profile)
    - [CSF 2.0 Mapping](../../infrastructure/mappings/csf-2.0.md)
    - [ISO 42001 Alignment](iso-42001-alignment.md)

