---
description: "AIRS framework guide for CROs and risk managers, covering how to quantify AI risk, set appetite, and demonstrate control effectiveness to the board."
---

# Risk & Governance

**CROs, Risk Managers, GRC Teams - how to quantify AI risk, set appetite, and demonstrate control effectiveness to the board.**

> *Part of [Stakeholder Views](README.md) · [AI Runtime Security](../)*

## Executive Summary

Your organisation is deploying AI systems that behave differently every time they run. Traditional risk frameworks assume deterministic systems - test it, prove it works, assign a rating, move on. AI breaks that assumption. The same system can pass every test today and hallucinate a medical dosage, leak customer data, or approve an unauthorised transaction tomorrow.

**Three things the board needs to know:**

1. **You can quantify AI risk** the same way you quantify any operational risk - inherent risk, control effectiveness per layer, residual risk, annualised frequency. This framework provides the methodology.
2. **Controls exist and are measurable.** The industry has converged on a layered pattern: automated guardrails (real-time), independent AI evaluation (async), human oversight (as needed), and circuit breakers (immediate). Each layer's effectiveness can be measured through red team testing, evaluation datasets, and agreement studies.
3. **Failure modes are defined in advance.** Every control layer has a predetermined degradation path - from full operation to supervised-only to full stop. The system doesn't fail silently. It transitions to a safe state you've already approved.

**The ask:** Classify your AI systems by risk tier, set quantified appetite per tier, and require measured control evidence - not assertions. This page shows you how.

**Time to read:** 5 minutes. **Time to act:** Start Monday.

## Five Runtime Control Principles

The framework is built on five principles. Every control, every metric, every degradation path follows from these:

1. **Prevent known-bad in real time.** Guardrails block prompt injection, data leakage, and policy violations before the AI responds. This is your first line - fast, pattern-based, always on.
2. **Detect unknown-bad independently.** A separate AI evaluates outputs the guardrails passed. It catches semantic violations, hallucinated facts, and subtle policy breaches that pattern matching misses.
3. **Keep humans in the loop where it matters.** Not on every transaction - on the ones that matter. High-risk decisions, edge cases, and flagged outputs route to qualified reviewers with defined SLAs.
4. **Fail to a safe state, not to silence.** When controls degrade, the system doesn't continue unchecked. It transitions through predetermined states - each with defined risk implications - down to full stop if needed.
5. **Measure everything. Assert nothing.** Control effectiveness is quantified through red team testing, evaluation datasets, and human agreement studies. "We have guardrails" is not a risk treatment.

## How the Layers Work Together

![Three-Layer Control Stack](../images/three-layer-stack.svg)

Three independent control layers, each catching what the previous one missed:

| Layer | Function | Speed | What It Catches |
|---|---|---|---|
| **Guardrails** | Block known-bad patterns | Real-time (<100ms) | Prompt injection, PII leakage, policy violations |
| **AI Evaluation** | Assess output quality and safety | Near-real-time | Hallucination, semantic policy breaches, tone violations |
| **Human Oversight** | Review flagged and sampled outputs | Hours to days | Edge cases, novel risks, calibration drift |

Circuit breakers sit across all three: if any layer detects a critical failure or becomes unavailable, the system transitions to a predetermined safe state.

## What This Adds That Existing Standards Don't

You already have NIST AI RMF, ISO 42001, and the EU AI Act. This framework isn't competing with them - it fills three gaps they don't address:

| Gap | What's Missing in Standards | What This Framework Provides |
|---|---|---|
| **Runtime behavior** | Standards focus on design-time risk assessment and pre-deployment testing. They don't specify how to monitor and control AI *after* it's deployed, in production, under real conditions. | A layered runtime control architecture with quantified per-layer effectiveness |
| **Defined failure modes** | Standards require "robustness" and "resilience" but don't define what happens when specific control layers fail. | PACE degradation: four predetermined states (Primary → Alternate → Contingency → Emergency) with pre-approved risk implications |
| **Multi-agent security** | Standards address single AI systems. They don't cover agent-to-agent communication, delegated authority, tool access chains, or emergent behavior in multi-agent workflows. | MASO: seven control domains for multi-agent orchestration with risk-tiered implementation |

This framework is the **implementation layer** that sits between what standards require and what engineering teams build. It turns "implement risk management measures" (EU AI Act Art. 9) into "here are the three control layers, here's how to measure each one, and here's what happens when they fail."

## Why AI Risk Is Different

AI introduces a risk category your frameworks weren't designed for: **non-deterministic system behavior.**

Your existing risk models assume systems behave predictably. AI doesn't. The same input produces different outputs at different times. An AI system that passed every test last quarter might produce harmful outputs tomorrow - not because something broke, but because that's how the technology works.

Three questions your board is already asking:

| Board Question | What They Need | Where It Is |
|---|---|---|
| **How much AI risk do we have?** | Inventory and classification | [Risk Tiers](../core/risk-tiers.md) - six dimensions, four tiers |
| **Are our controls actually working?** | Measurement, not assertion | [Risk Assessment](../core/risk-assessment.md) - quantified per layer |
| **What happens when controls fail?** | Defined resilience posture | [PACE Resilience](../PACE-RESILIENCE.md) - predetermined degradation |

## The Cost of Doing Nothing

AI risk isn't theoretical. These are public, documented incidents:

- **Air Canada (2024)** - Chatbot fabricated a bereavement fare policy. Customer relied on it. Airline held liable by tribunal. *No runtime monitoring detected the hallucination before the customer acted on it.*
- **Chevrolet dealership (2023)** - AI chatbot agreed to sell a vehicle for $1. *No guardrail prevented the commitment. No human oversight caught it.*
- **DPD (2024)** - Customer service AI swore at customers and criticised the company. Went viral. *No behavioral monitoring flagged the output before delivery.*
- **Mata v. Avianca (2023)** - Lawyer submitted AI-generated legal brief citing fabricated case law. Sanctioned by the court. *No independent evaluation verified the AI's output.*
- **Microsoft Copilot EchoLeak (2025)** - Indirect prompt injection in email content caused Copilot to exfiltrate sensitive data. *No untrusted content isolation or exfiltration detection.*

Every one of these was preventable with controls this framework describes. Every one caused measurable financial, legal, or reputational damage.

**Regulatory exposure is increasing:**

| Regulation | AI Relevance | Penalty |
|---|---|---|
| **EU AI Act** | Risk management, human oversight, robustness requirements | Up to 7% annual global turnover |
| **DORA** | Digital operational resilience for AI in financial services | Regulatory sanctions, licence conditions |
| **NIST AI RMF** | US federal AI risk management expectations | Procurement disqualification, reputational |
| **ISO 42001** | AI management system certification | Market access, contractual requirements |

The question isn't whether to manage AI risk. It's whether you have a defensible methodology when the regulator asks how.

## What This Framework Gives You

### Quantified residual risk - in language the board already uses

Your risk committee can read this without translation. The [Risk Assessment](../core/risk-assessment.md) methodology produces these outputs directly:

**Example: HIGH-tier system** (customer-facing chatbot, 1M transactions/year):

| Threat Scenario | Inherent Risk (per 1K) | Residual Risk (per 1K) | Annual Incidents |
|---|---|---|---|
| Prompt injection | 20 | 0.002 | ~2 |
| Hallucinated information | 50 | 0.005 | ~5 |
| PII leakage | 10 | 0.001 | ~1 |
| Unauthorised action | 5 | 0.0005 | ~0.5 |

This is inherent risk, control effectiveness, residual risk, annualised frequency. The same language you use for every other operational risk. Not "we have guardrails."

The methodology is aligned to **NIST AI RMF** (Govern, Map, Measure, Manage):

| NIST AI RMF Function | What the Framework Provides |
|---|---|
| **GOVERN** | Risk tolerance expressed as quantitative residual risk thresholds |
| **MAP** | Threat identification per scenario, per system, per tier |
| **MEASURE** | Per-layer effectiveness measurement with compounding calculations |
| **MANAGE** | Control selection proportionate to risk; defined fail postures per tier |

### A classification scheme that maps to risk appetite

Four tiers. Six scoring dimensions. Each produces a measurable assessment, not a subjective rating:

| Dimension | What It Measures |
|---|---|
| Decision authority | Can the AI take action, or only advise? |
| Reversibility | Can outcomes be undone? At what cost? |
| Data sensitivity | PII, financial, health, legal, classified? |
| Audience | Internal employees or external customers? |
| Scale | Hundreds or millions of transactions? |
| Regulatory | Which regulatory obligations apply? |

The tier drives everything downstream: which controls apply, how much evaluation coverage, how often humans review, what resilience posture is required. **Risk appetite is expressed through tier boundaries**, not abstract statements.

### Defined resilience for operational risk

Every control layer has a predetermined degradation path:

![PACE Degradation Path](../images/pace-degradation.svg)

| State | What It Means | Risk Implication |
|---|---|---|
| **Primary** | All control layers operational | Within approved risk appetite |
| **Alternate** | Backup controls active, primary being restored | Elevated monitoring, risk still within tolerance |
| **Contingency** | Supervised-only mode, human approval required | Reduced throughput, risk contained |
| **Emergency** | AI traffic stopped, non-AI fallback active | No AI risk exposure, operational impact |

This maps directly to DORA, BCM, and operational risk appetite statements. The AI system doesn't fail silently. It transitions through states you've already approved, each with defined risk implications.

### Regulatory mapping you can hand to auditors

Pre-built crosswalks to the standards your GRC team already tracks:

| Standard | Mapping |
|---|---|
| NIST AI RMF 1.0 | [51 subcategories mapped](../infrastructure/mappings/nist-ai-rmf.md) |
| ISO 42001 | [Annex A alignment](../infrastructure/mappings/iso42001-annex-a.md) |
| EU AI Act | [Art. 9, 14, 15 crosswalk](../extensions/regulatory/eu-ai-act-crosswalk.md) |
| OWASP LLM Top 10 | [Full control mapping](../infrastructure/mappings/owasp-llm-top10.md) |
| NIST CSF 2.0 | [Function mapping](../infrastructure/mappings/csf-2.0.md) |

## Your Starting Path

| # | Document | Why You Need It | Time |
|---|---|---|---|
| 1 | [Risk Tiers](../core/risk-tiers.md) | The classification scheme - six dimensions, four tiers, governance approval gates | 15 min |
| 2 | [Risk Assessment](../core/risk-assessment.md) | Quantitative methodology - worked examples at every tier, NIST AI RMF aligned | 20 min |
| 3 | [Controls](../core/controls.md) | What each control layer does, so you can evaluate whether they're implemented correctly | 15 min |
| 4 | [PACE Resilience](../PACE-RESILIENCE.md) | Operational resilience - defined fail postures and degradation paths | 15 min |
| 5 | [AI Governance Operating Model](../extensions/regulatory/ai-governance-operating-model.md) | Organisational structure for AI risk governance | 20 min |

**For regulated industries:** Add [High-Risk Financial Services](../extensions/regulatory/high-risk-financial-services.md) and [EU AI Act Crosswalk](../extensions/regulatory/eu-ai-act-crosswalk.md).

## What You Can Do Monday Morning

1. **Inventory and classify** every AI system using the [Risk Tiers](../core/risk-tiers.md) six-dimension scoring. Most organisations don't know how many AI systems they're running or at what tier.

2. **Define risk appetite per tier.** Use the [Risk Assessment](../core/risk-assessment.md) template: "For HIGH-tier systems, we accept residual risk below X per 1,000 transactions." This converts abstract appetite into measurable thresholds.

3. **Require quantified control evidence.** Stop accepting "we have guardrails" as a risk treatment. Require the worked example format: inherent risk → per-layer effectiveness → residual risk → compensated residual.

4. **Add resilience posture to your risk register.** For each AI system, record which state it's in (Primary / Alternate / Contingency / Emergency) and what triggers transitions between states. This is your operational resilience evidence.

5. **Schedule quarterly recalibration.** Control effectiveness rates change. Require red team results, evaluation accuracy measurements, and human reviewer agreement studies to update residual risk calculations. The recalibration schedule is in the [Risk Assessment](../core/risk-assessment.md) document.

## Anticipating Pushback

**"We already have an AI risk framework."**
Does it quantify residual risk per control layer? Does it define what happens when controls fail? Does it map to NIST AI RMF at the subcategory level? This framework isn't competing with your existing GRC tooling - it provides the AI-specific risk methodology that plugs into it.

**"The AI team says the risk is low."**
Risk classification is a governance function, not an engineering function. The six-dimension scoring is designed to be completed jointly by the AI team and the risk function. Engineers assess technical dimensions (reversibility, scale); risk assesses business dimensions (regulatory, data sensitivity, audience).

**"We can't measure AI control effectiveness."**
You can. Guardrail effectiveness is measured through red team exercises. Evaluation layer accuracy is measured through labelled datasets. Human reviewer effectiveness is measured through agreement studies. The [Risk Assessment](../core/risk-assessment.md) methodology explains exactly how - and what to do with illustrative rates before you have measured ones.

**"This is too complex for our current maturity."**
Start with the [Risk Tiers](../core/risk-tiers.md) and apply tier classification only. Even classifying your AI systems into four tiers, without implementing any new controls, gives you a risk inventory you didn't have before. That alone is a board-reportable improvement.

