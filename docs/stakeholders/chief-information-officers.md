---
description: "AIRS framework guide for CIOs and CTOs, covering how to govern AI across a technology portfolio with consistent classification, cost visibility, and risk management."
---

# Chief Information Officers

**CIOs, CTOs, VP Technology - how to govern AI across your technology portfolio when every product runs different agents with different risk profiles.**

> *Part of [Stakeholder Views](README.md) · [AI Runtime Security](../README.md)*

## The Problem You Have

You own the technology portfolio. AI is no longer a single initiative - it's spreading across products, teams, and business units. Each team is choosing different models, different frameworks, different agent architectures. You're accountable for all of it.

Three problems are compounding simultaneously:

1. **You can't govern what you can't see.** Product teams are deploying AI agents across multiple products - some using single-model RAG pipelines, others running multi-agent orchestrations with tool access. Without a common classification and control framework, you have no consistent view of risk exposure across the portfolio.

2. **Cost is escalating without visibility.** Every AI deployment carries compute cost (model inference), control cost (guardrails, Judge evaluation, human review), and operational cost (monitoring, incident response, skills). When multiple products run different agent sets, these costs multiply - and they're often buried in different budget lines. McKinsey's 2025 survey found that only 6% of organisations qualify as "AI high performers," with cost management and scaling cited as primary barriers.

3. **Skills don't scale with deployments.** Each new AI product needs people who can build, operate, and oversee it. The technical skills market is competitive, and operational AI security skills barely exist yet. Gartner's AI Maturity Model identifies talent as one of seven critical pillars - and most organisations score lowest on it.

## What This Framework Gives You

### A portfolio-level classification system

The framework's [Risk Tiers](../core/risk-tiers.md) provide a consistent language across every product and team. Six scoring dimensions (decision authority, reversibility, data sensitivity, audience, scale, regulatory) produce four tiers (LOW / MEDIUM / HIGH / CRITICAL). This gives you:

| What You Get | Why It Matters |
|---|---|
| **Consistent inventory** | Every AI deployment classified the same way, regardless of which team built it |
| **Proportionate controls** | LOW-tier systems don't carry CRITICAL-tier overhead - controls scale to actual risk |
| **Resource allocation basis** | You know which products need dedicated AI security engineers and which need basic guardrails |
| **Board reporting language** | "We have 12 AI systems: 4 LOW, 5 MEDIUM, 2 HIGH, 1 CRITICAL" is actionable information |

### Cost governance across the AI portfolio

The control overhead is real and varies dramatically by tier. The [Cost & Latency](../extensions/technical/cost-and-latency.md) analysis provides the numbers:

| Risk Tier | Security Overhead (% of Generator Cost) | Per 1M Requests/Month | What's Included |
|---|---|---|---|
| **LOW** | ~5-10% | Negligible | Rule-based guardrails |
| **MEDIUM** | ~15-40% | $1K-7K | Guardrails + sampled Judge (10-50%) |
| **HIGH** | ~40-80% | $5K-20K | Guardrails + full async Judge + human review |
| **CRITICAL** | ~80-100%+ | $10K-50K+ | Full sync Judge + 100% coverage + dedicated human reviewers |

**When multiple products run different agent sets**, total AI security cost is the sum across the portfolio - not an average. A portfolio of 5 LOW-tier and 1 CRITICAL-tier system is dominated by the CRITICAL-tier cost. Budget accordingly.

For multi-agent systems, add MASO controls: inter-agent message bus, per-agent identity management, cross-agent DLP, and delegation chain auditing. The [MASO Integration Guide](../maso/integration/integration-guide.md) details the implementation overhead per agent framework (LangGraph, AutoGen, CrewAI, AWS Bedrock).

### Technology skills planning

The [Human Factors](../strategy/human-factors.md) assessment maps the skills gap directly:

| Skill Domain | Who Needs It | Availability | Time to Competence |
|---|---|---|---|
| **AI technical** (build, deploy, maintain) | Engineering teams | Competitive market; experienced AI engineers are expensive | 1-6 months depending on role |
| **AI operational** (guardrails, Judge, HITL queues) | Security/ops teams | Almost nobody has this skill set yet | 2-6 months |
| **AI-aware domain expertise** (critical use of AI outputs) | Business users | Most domain experts have never worked with non-deterministic tools | 1-3 months |
| **Multi-agent security** | Security architects | Very rare | 6-12 months |

**The portfolio multiplier:** One product at HIGH tier needs a dedicated AI security engineer. Five products at HIGH tier need a team. Plan for the portfolio, not the project.

Luftman's Strategic Alignment Maturity Model (SAMM) scores alignment across six dimensions including skills and governance. Research consistently finds these are the weakest dimensions in most organisations. The framework provides the AI-specific governance structure; your job is ensuring the skills and organisational readiness exist to operate it.

### A technology standards approach for multi-product environments

When different products run different agent sets, you need shared infrastructure - not shared implementations:

| Shared Layer | What It Provides | Why It Saves Cost |
|---|---|---|
| **Common guardrail service** | Centralised input/output filtering, configurable per product | One team maintains guardrail patterns instead of N teams duplicating effort |
| **Shared Judge infrastructure** | Evaluation service with product-specific prompts | Model costs shared; expertise concentrated in one team |
| **Centralised logging and SIEM integration** | Consistent telemetry across all AI products | Single observability pipeline; correlated threat detection across products |
| **Agent identity platform** | Non-Human Identity (NHI) management for all agents across products | Consistent credential lifecycle; no per-product IAM silos |
| **Common PACE fail postures** | Standardised degradation paths | Incident response works the same way regardless of which product fails |

This is the platform approach applied to AI security. Individual product teams own their risk classification and business logic. The platform team owns the shared control infrastructure. See [Infrastructure Controls](../infrastructure/README.md) for the 80-control mapping.

### Risk visibility for the board

The [Risk Assessment](../core/risk-assessment.md) methodology produces portfolio-level reporting:

| Metric | What It Shows | Source |
|---|---|---|
| **Systems by tier** | Portfolio risk distribution | Risk Tiers classification |
| **Residual risk per system** | Quantified exposure after controls | Per-layer effectiveness measurement |
| **PACE state per system** | Which systems are in degraded operation | Runtime monitoring |
| **Control coverage gaps** | Which systems lack required controls for their tier | Checklist audit |
| **Cost per system by tier** | Total AI security spend mapped to risk | Cost & Latency budgets |

This replaces "we have AI guardrails" with data the board can act on.

## Your Starting Path

Read these in order. Total time: ~90 minutes.

| # | Document | Why You Need It |
|---|---|---|
| 1 | [Quick Start](../QUICK_START.md) | The framework essentials: classification, controls, fail postures |
| 2 | [Risk Tiers](../core/risk-tiers.md) | The classification scheme you'll mandate as the portfolio standard |
| 3 | [Business Alignment](../strategy/business-alignment.md) | Four strategic questions every AI initiative must answer before investment |
| 4 | [Cost & Latency](../extensions/technical/cost-and-latency.md) | Budget the control layers - the numbers behind the portfolio cost model |
| 5 | [Human Factors](../strategy/human-factors.md) | The skills gap that will determine whether your AI portfolio can actually be operated |

**If you have multi-agent products:** Add [MASO Overview](../maso/README.md) and [Multi-Agent Controls](../core/multi-agent-controls.md).

**If you're building a platform team:** Add [Infrastructure Controls](../infrastructure/README.md) and [AI Governance Operating Model](../extensions/regulatory/ai-governance-operating-model.md).

**If you're presenting to the board:** Add [Risk Assessment](../core/risk-assessment.md) for the quantified methodology.

**To see the framework in action across a full enterprise:** Read [A Day in the Life](../strategy/enterprise-day-in-the-life.md) - what a single day looks like when eight AI systems across multiple departments operate under the framework.

## What You Can Do Monday Morning

1. **Inventory every AI deployment** across the portfolio. Use the [Risk Tiers](../core/risk-tiers.md) six-dimension scoring to classify each one. Most CIOs don't have a complete, consistently classified view of their AI estate.

2. **Establish a portfolio cost model.** Map each system's tier to its control cost using [Cost & Latency](../extensions/technical/cost-and-latency.md). Add these costs to existing product P&Ls. AI security cost should be visible, not hidden in infrastructure budgets.

3. **Assess the skills gap.** For each tier in your portfolio, check whether you have the people to operate the required controls. Use the [Human Factors](../strategy/human-factors.md) framework. A CRITICAL-tier system with no trained Judge operator is an uncontrolled CRITICAL-tier system.

4. **Mandate shared infrastructure for common controls.** If multiple products need guardrails and Judge evaluation, build once and share. The alternative - every product team building their own - multiplies cost, fragments expertise, and creates inconsistent security posture.

5. **Add AI risk to your technology governance cadence.** The [AI Governance Operating Model](../extensions/regulatory/ai-governance-operating-model.md) provides the structure. At minimum: quarterly portfolio risk review, tier reclassification triggers, and PACE state monitoring.

## Common Objections - With Answers

**"Each product team should own their own AI security."**
Product teams should own their risk classification and business-specific controls. But shared infrastructure (guardrails, Judge, logging, identity) is more cost-effective, more consistent, and easier to govern than N independent implementations. This is the same argument as shared authentication services or centralised logging - the pattern is proven.

**"We don't have the budget for a platform team."**
The alternative is every product team funding their own AI security capability - which costs more in aggregate. A shared guardrail service, a shared Judge infrastructure, and a shared SIEM integration cost less than five teams building five separate versions. The [Cost & Latency](../extensions/technical/cost-and-latency.md) analysis provides the numbers for the business case.

**"Our AI maturity is too low for this level of governance."**
Start with classification. Even just categorising your AI systems into four tiers - without implementing any new controls - gives you a portfolio view you didn't have before. The [Quick Start](../QUICK_START.md) is designed for exactly this situation. Gartner's AI Maturity Model and MITRE's AI Maturity Model both emphasise that governance maturity must grow alongside technical maturity, not lag behind it.

**"The skills market is too competitive - we can't hire AI security people."**
You don't need to hire all of them. The [Human Factors](../strategy/human-factors.md) assessment shows that most operational roles can be filled by retraining existing security and operations staff. Guardrail maintenance is an extension of existing security operations. Judge calibration is an extension of QA. Dedicated hiring is needed for architecture and leadership roles, not every operational position.

**"Different products need different approaches."**
They do - and the framework supports that. Different products get different risk tiers, which drive different control requirements. What's shared is the classification methodology, the control infrastructure, and the governance process. Product-specific decisions (sampling rates, Judge prompts, PACE thresholds) remain with the product team.

