---
description: "AIRS framework guide for CISOs and security directors, focused on translating AI runtime risks into actionable security programme requirements."
---

# Security Leaders

**CISOs, Security Directors, Security Architects - what this framework means for your security programme.**

> *Part of [Stakeholder Views](README.md) · [AI Runtime Security](../README.md)*

## The Problem You Have

You've secured applications, networks, identities, and data for years. AI breaks your mental model in three ways:

1. **You can't test it before deployment and call it done.** The same input produces different outputs. Edge cases emerge in production that no test suite anticipated. Your traditional assurance model - test, prove, ship - doesn't work.

2. **The threat model is unfamiliar.** Prompt injection isn't SQL injection. Hallucination isn't a bug - it's a property of the technology. An AI system can be exploited through its *training data*, its *retrieval corpus*, or just a cleverly worded question. Your WAF won't see it.

3. **You're accountable, but the technology team is building.** AI systems are being deployed faster than security organisations can evaluate them. You need a way to set requirements without becoming a bottleneck.

## What This Framework Gives You

### A control architecture you can mandate

Three layers, applied proportionately by risk:

![Three-Layer Control Stack](../images/three-layer-stack.svg)

This isn't a product recommendation. It's a **pattern** your teams implement with whatever tooling fits your environment. The framework describes *what needs to be true* at each layer and *how to verify it*.

### Risk tiers that scale controls to actual risk

Not every AI system needs the same controls. The four-tier model (LOW / MEDIUM / HIGH / CRITICAL) lets you mandate proportionate security:

| Tier | What It Means | Security Posture |
|---|---|---|
| **LOW** | Internal, read-only, no sensitive data | Guardrails only, self-certification |
| **MEDIUM** | Internal with write access, or human-reviewed external | Guardrails + sampled Judge |
| **HIGH** | Customer-facing, sensitive data, financial actions | Full three layers + PACE resilience |
| **CRITICAL** | Regulated decisions, autonomous actions, safety impact | Full three layers, 100% Judge coverage, tested fail postures |

### Quantified residual risk for board reporting

The [Risk Assessment](../core/risk-assessment.md) document provides a methodology for calculating residual risk per control layer. Instead of telling the board "we have guardrails," you say: *"Residual risk after all three control layers is 0.01% per transaction - approximately 10 incidents per year at our transaction volume, with critical-severity incidents at fewer than 2 per year."*

### PACE resilience - what happens when controls fail

Every control layer has a defined fail posture. When the Judge goes down, the system doesn't continue unchecked - it transitions to a predetermined safe state. Primary → Alternate → Contingency → Emergency. This is the same thinking you apply to your SOC, your DR plan, your incident response. Now it applies to AI.

### A clear answer to "are we covered against OWASP?"

Full mapping against [OWASP LLM Top 10 (2025)](../infrastructure/mappings/owasp-llm-top10.md) and OWASP Agentic Top 10 (2026). When audit asks, you have a control-by-control crosswalk.

## Your Starting Path

Read these in order. Total time: ~90 minutes.

| # | Document | Why You Need It |
|---|---|---|
| 1 | [Quick Start](../QUICK_START.md) | The framework essentials: classify, control, fail posture, test |
| 2 | [Risk Tiers](../core/risk-tiers.md) | The classification scheme you'll mandate across the organisation |
| 3 | [Controls](../core/controls.md) | What each layer does, how to verify it works, when each is required |
| 4 | [Risk Assessment](../core/risk-assessment.md) | Quantitative methodology for board-level risk reporting |
| 5 | [PACE Resilience](../PACE-RESILIENCE.md) | Fail postures - what happens when each control layer degrades |

**If you have multi-agent systems:** Add [MASO Overview](../maso/README.md) and the [Red Team Playbook](../maso/red-team/red-team-playbook.md).

**If you run a SOC:** Add [SOC Integration](../extensions/technical/soc-integration.md) and [Behavioral Anomaly Detection](../extensions/technical/behavioral-anomaly-detection.md).

## What You Can Do Monday Morning

1. **Classify your existing AI deployments** using the [Risk Tiers](../core/risk-tiers.md). Most organisations don't have a complete inventory of what's running, at what risk level.

2. **Require the three-layer pattern** for any HIGH or CRITICAL tier system. Don't specify products - specify the pattern. "Every customer-facing AI system requires guardrails, an independent evaluation layer, and defined human oversight."

3. **Ask every AI team one question:** *"What happens when your guardrails fail?"* If they don't have an answer, they need [PACE Resilience](../PACE-RESILIENCE.md).

4. **Add AI-specific scenarios to your next red team exercise.** The [Red Team Playbook](../maso/red-team/red-team-playbook.md) has 13 structured scenarios you can adapt.

5. **Use the [Risk Assessment](../core/risk-assessment.md) template** for the next board security update. Replace "we have AI guardrails" with quantified residual risk.

## Common Objections - With Answers

**"We already have guardrails."**
Guardrails alone catch ~90% of known-pattern issues. They miss semantic violations, novel attacks, and subtle policy breaches. The Judge layer catches 95% of what guardrails miss. [Why Guardrails Aren't Enough](../insights/why-guardrails-arent-enough.md) has the full argument.

**"This will slow down our AI delivery."**
The [Fast Lane](../FAST-LANE.md) pre-approves low-risk deployments with minimal controls. Only HIGH and CRITICAL tier systems need the full three layers. The framework doesn't slow delivery - it prevents teams from deploying CRITICAL-tier systems with LOW-tier controls.

**"We use [vendor X] - they handle security."**
Your vendor provides guardrails. They don't provide the Judge layer, human oversight processes, PACE fail postures, or risk-tier classification. The framework sits above vendor tooling. See [Infrastructure Beats Instructions](../insights/infrastructure-beats-instructions.md).

**"The AI team says their model is safe."**
Design-time safety testing is necessary but insufficient. The question isn't whether the model is safe in the lab - it's whether it behaves correctly in production, under adversarial conditions, with real customer data. That's a runtime security problem. That's what this framework solves.

