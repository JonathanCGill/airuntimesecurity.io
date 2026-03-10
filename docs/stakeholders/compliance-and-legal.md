---
description: "AI-RS framework guide for compliance officers and legal counsel — regulatory mapping, evidence generation, and audit-ready documentation for AI systems."
---

# Compliance & Legal

**Compliance Officers, Legal Counsel, DPOs, Audit Teams - how this framework maps to your regulatory obligations and produces the evidence you need.**

> *Part of [Stakeholder Views](README.md) · [AI Runtime Security](../)*

## The Problem You Have

AI regulation is arriving faster than most compliance programmes can adapt. You're facing:

1. **New obligations with unclear scope.** The EU AI Act, evolving NIST guidance, sector-specific regulators adding AI provisions to existing rules. Requirements are principles-based - you need to demonstrate "appropriate risk management" without a prescriptive checklist.

2. **Evidence gaps.** Traditional compliance evidence (policy documents, annual assessments, audit logs) doesn't cover what regulators are asking about AI: *How do you know the AI's output is correct? How do you detect bias in real-time decisions? What happens when your AI fails? Can you explain why the AI made a specific decision?*

3. **Scope uncertainty.** Which of your AI systems are "high risk" under the EU AI Act? Which are "critical" under DORA? Your AI team says "it's just a chatbot" - your regulator might disagree.

## What This Framework Gives You

### Pre-built regulatory crosswalks

The framework maps its controls to the standards you're already tracking:

| Regulation / Standard | Mapping Document | Coverage |
|---|---|---|
| **EU AI Act** | [EU AI Act Crosswalk](../extensions/regulatory/eu-ai-act-crosswalk.md) | Art. 9 (risk management), Art. 14 (human oversight), Art. 15 (robustness) |
| **NIST AI RMF 1.0** | [NIST AI RMF Mapping](../infrastructure/mappings/nist-ai-rmf.md) | All 51 subcategories across Govern, Map, Measure, Manage |
| **ISO 42001** | [ISO 42001 Alignment](../extensions/regulatory/iso-42001-alignment.md) + [Annex A](../infrastructure/mappings/iso42001-annex-a.md) | AI management system requirements + Annex A controls |
| **ISO 27001** | [ISO 27001 Alignment](../extensions/regulatory/iso-27001-alignment.md) | Extension of ISMS to AI-specific risks |
| **NIST SP 800-218A** | [SP 800-218A Mapping](../infrastructure/mappings/nist-sp800-218a.md) | Secure AI development lifecycle |
| **NIST CSF 2.0** | [CSF 2.0 Mapping](../infrastructure/mappings/csf-2.0.md) | Cybersecurity framework function alignment |
| **NIST IR 8596** | [IR 8596 Alignment](../extensions/regulatory/nist-ir-8596-alignment.md) | Cyber AI Profile — all six CSF Functions for "Secure" focus area |
| **OWASP LLM Top 10** | [OWASP Mapping](../infrastructure/mappings/owasp-llm-top10.md) | Full control mapping to all 10 risks |
| **DORA** | Referenced in [MASO](../maso/) | Digital operational resilience for financial services |

These are **control-level crosswalks**, not executive summaries. They map specific framework controls to specific regulatory requirements, giving you the traceability auditors expect.

### Evidence the framework produces

Each control layer generates specific compliance evidence:

| Regulatory Question | Framework Control | Evidence Produced |
|---|---|---|
| "How do you manage AI risk?" | Risk tier classification + risk assessment | Documented six-dimension scoring, quantified residual risk |
| "How do you detect harmful AI output?" | Three-layer controls | Guardrail logs, Judge evaluations, human review records |
| "Do you have human oversight?" | Human oversight layer + PACE | Documented escalation criteria, review rates, override records |
| "What happens when AI fails?" | PACE resilience | Tested fail postures, degradation path documentation, circuit breaker evidence |
| "Can you explain AI decisions?" | Observability + Judge | Decision chain audit trail, Judge evaluation reasoning, input/output pairs |
| "How do you detect bias?" | Judge + risk assessment | Judge fairness evaluation criteria, statistical monitoring, portfolio-level analysis |
| "How do you manage AI supply chain?" | Supply chain controls | AIBOM, model provenance, vendor assessment, tool manifest |

### Risk classification that aligns with regulatory categories

The framework's four-tier system maps to regulatory risk categories:

| Framework Tier | EU AI Act Category | NIST AI RMF Profile | Compliance Implication |
|---|---|---|---|
| **LOW** | Minimal risk | Light-touch | Standard reporting |
| **MEDIUM** | Limited risk | Moderate | Transparency obligations |
| **HIGH** | High risk | Substantial | Full risk management system, conformity assessment |
| **CRITICAL** | High risk (upper end) | Maximum | All HIGH requirements + enhanced human oversight |

The classification dimensions (decision authority, reversibility, data sensitivity, audience, scale, regulatory) **directly support** the risk assessment your regulator expects. Completing the [Risk Tiers](../core/risk-tiers.md) classification for each AI system produces artefacts that satisfy regulatory risk assessment requirements.

## Your Starting Path

| # | Document | Why You Need It |
|---|---|---|
| 1 | [Risk Tiers](../core/risk-tiers.md) | Classification scheme - produces the risk assessment your regulator requires |
| 2 | [EU AI Act Crosswalk](../extensions/regulatory/eu-ai-act-crosswalk.md) | If EU AI Act applies - control-by-control mapping |
| 3 | [Risk Assessment](../core/risk-assessment.md) | Quantitative methodology - satisfies NIST AI RMF Measure function |
| 4 | [ISO 42001 Alignment](../extensions/regulatory/iso-42001-alignment.md) | If pursuing ISO 42001 certification |
| 5 | [AI Governance Operating Model](../extensions/regulatory/ai-governance-operating-model.md) | Organisational structure for AI governance |

**For financial services:** Add [High-Risk Financial Services](../extensions/regulatory/high-risk-financial-services.md).

**For detailed NIST mapping:** [NIST AI RMF Mapping](../infrastructure/mappings/nist-ai-rmf.md) - all 51 subcategories.

## What You Can Do Monday Morning

1. **Inventory your AI systems** using the [Risk Tiers](../core/risk-tiers.md) classification. Regulators will ask "what AI systems do you operate and how are they classified?" You need this answer before they ask.

2. **Map your highest-risk system** against the [EU AI Act Crosswalk](../extensions/regulatory/eu-ai-act-crosswalk.md) or relevant standard. Identify gaps between current controls and regulatory requirements. This becomes your compliance roadmap.

3. **Require the [Risk Assessment](../core/risk-assessment.md) template** for every HIGH and CRITICAL tier system. This produces the quantified risk documentation that regulators and auditors expect - inherent risk, control effectiveness, residual risk.

4. **Verify human oversight evidence.** For each system with human oversight requirements, confirm you can produce: escalation criteria, review rates, override counts, reviewer qualifications. If you can't produce this evidence today, you have a gap.

5. **Check your AI audit trail.** Can you reconstruct why a specific AI system produced a specific output for a specific user at a specific time? If not, you can't satisfy explainability or transparency obligations. The [Observability](../maso/controls/observability.md) domain defines what to log.

## Common Objections - With Answers

**"The EU AI Act doesn't apply to us."**
If you serve EU customers or deploy AI that affects EU data subjects, it likely does. Even if it doesn't today, the regulatory direction is clear - NIST, sector regulators, and international standards are converging on similar requirements. Building to this framework positions you for any AI regulation, not just the EU AI Act.

**"We already have an AI ethics policy."**
A policy is a statement of intent. A regulator wants evidence of implementation. "We have a responsible AI policy" doesn't answer "show me your risk assessment, your control effectiveness measurements, your human oversight records, and your fail posture testing evidence." This framework produces those artefacts.

**"Our AI vendor handles compliance."**
Your vendor handles their compliance - model safety, platform security, API availability. They don't handle your compliance - how you use the model, what data you feed it, what decisions it makes, how you monitor output quality, what happens when it fails. The shared responsibility model applies to AI just like cloud. See [Infrastructure Beats Instructions](../insights/infrastructure-beats-instructions.md).

**"We're waiting for regulatory clarity before investing."**
The core requirements are already clear across all major frameworks: risk assessment, layered controls, human oversight, resilience planning, audit trails. The details may change; these principles won't. Implementing the framework now gives you a structured approach that adapts as regulations finalise - rather than a scramble when enforcement begins.

**"Compliance requirements will slow down AI adoption."**
Compliance requirements scale with risk. LOW-tier systems (internal, read-only, no regulated data) go through the [Fast Lane](../FAST-LANE.md) - self-certification, minimal controls, days not months. Compliance only adds significant overhead for HIGH and CRITICAL tier systems - where the regulatory obligations actually apply.

