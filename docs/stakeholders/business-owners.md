---
description: "AIRS framework guide for business unit leaders — managing AI risk across product lines when agents are operational and the risk is yours."
---

# Business Owners

**Business Unit Leaders, P&L Owners, General Managers - how to manage AI risk across your product lines when agents are operational, costs are real, and the risk is yours.**

> *Part of [Stakeholder Views](README.md) · [AI Runtime Security](../)*

## The Problem You Have

You own the business outcome. Your products are running AI agents - possibly multiple agent sets across multiple products - and you're accountable for what they do. Revenue, cost, risk, and reputation all sit with you.

Four realities are converging:

1. **AI risk is business risk.** When your AI chatbot fabricates a policy, commits to a price, leaks customer data, or approves an unauthorised transaction, that's your P&L impact. Air Canada was held liable when their chatbot hallucinated a bereavement fare policy. Chevrolet's dealership AI agreed to sell a vehicle for $1. DPD's customer service AI swore at customers and went viral. Every one of these was a business owner's problem before it was a security team's problem.

2. **Control costs vary by orders of magnitude.** An internal FAQ bot costs almost nothing to secure. A customer-facing autonomous agent processing financial transactions costs substantially more - not because security is expensive, but because the risk is high and the controls must be proportionate. If you don't understand the relationship between risk tier and control cost, you'll either overspend on low-risk systems or underspend on high-risk ones.

3. **Multiple products mean multiplied complexity.** When you run different agent sets across different products - a customer service agent here, a claims processing agent there, an internal knowledge assistant elsewhere - each has its own risk profile, its own control requirements, and its own operational cost. Portfolio thinking is essential.

4. **Skills are a constraint, not just a cost.** Deloitte's 2026 survey found that organisations with enterprise-wide AI strategy are 3x more likely to report transformative results. But strategy without operational capability is fiction. You need people who can operate AI controls, not just people who can build AI features. The skills market is tight, and operational AI security skills are the scarcest of all.

## What This Framework Gives You

### A risk-based investment model

Not every AI system needs the same investment in controls. The framework's [Risk Tiers](../core/risk-tiers.md) map directly to cost:

| Your Product's AI | Likely Tier | Control Investment | Business Impact |
|---|---|---|---|
| Internal knowledge assistant | LOW | Basic guardrails, self-certification | Days to deploy; negligible security overhead |
| Internal document processor with write access | MEDIUM | Guardrails + sampled Judge evaluation | 1-2 weeks added; modest ongoing cost |
| Customer-facing chatbot | HIGH | Full three layers + PACE fail postures | 3-6 weeks added; meaningful but proportionate cost |
| Autonomous agent making financial decisions | CRITICAL | Full three layers, 100% Judge, tested PACE, dedicated reviewers | 6-12 weeks; substantial control infrastructure |

The [Fast Lane](../FAST-LANE.md) pre-approves low-risk deployments. If your AI meets four criteria (internal users, read-only, no regulated data, human reviews output), deploy with basic guardrails and move on. Don't put an internal FAQ bot through the same process as a payment agent.

### The real cost of controls - and the cost of not having them

Controls are insurance, and insurance has measurable ROI:

**Without controls** (based on documented incident data):

| Risk | Frequency (per 1K transactions) | Business Impact |
|---|---|---|
| Hallucinated information acted on by customers | ~50 | Liability, complaints, regulatory scrutiny |
| PII leaked in AI responses | ~10 | Data breach notification, regulatory fines (EU AI Act: up to 7% global turnover) |
| Unauthorised commitments (pricing, refunds, actions) | ~5 | Direct financial loss, reputational damage |
| Prompt injection exploited | ~20 | System manipulation, data exfiltration |

**With three-layer controls** (framework's quantified model):

| Same Risk | Residual Frequency (per 1K) | Reduction |
|---|---|---|
| Hallucinated information | ~0.005 | 99.99% |
| PII leakage | ~0.001 | 99.99% |
| Unauthorised commitments | ~0.0005 | 99.99% |
| Prompt injection | ~0.002 | 99.99% |

For a customer-facing system at 1M transactions/year, that's the difference between ~85,000 incidents and ~10. The [Risk Assessment](../core/risk-assessment.md) has the full worked methodology.

### Portfolio risk management across multiple products

When you run multiple products with different agent sets, manage them as a portfolio:

| Portfolio View | What It Tells You | Action |
|---|---|---|
| **Tier distribution** | How much of your portfolio is HIGH/CRITICAL vs. LOW/MEDIUM | Determines total control investment and staffing requirements |
| **Shared infrastructure opportunities** | Which products can share guardrail, Judge, and logging infrastructure | Reduces per-product cost; concentrates expertise |
| **Highest-risk product** | Which product dominates your risk exposure | Focus governance attention and control investment here |
| **Skills concentration risk** | Whether one person operates controls for multiple products | Cross-train or hire; single points of failure are unacceptable for HIGH/CRITICAL systems |
| **Aggregate incident exposure** | Total expected incidents across all products | Board-level risk metric; drives insurance and regulatory conversations |

**Multi-agent complexity:** If any product runs a multi-agent system (agents communicating with other agents), the control requirements increase. The [MASO Framework](../maso/) adds seven control domains: prompt integrity, identity and access, data protection, execution control, observability, supply chain, and privileged agent governance. This isn't optional overhead - it addresses risks (privilege escalation across agents, emergent behavior, delegation chain attacks) that don't exist in single-agent systems.

### Operational staffing reality

The [Human Factors](../strategy/human-factors.md) assessment and the [AI Governance Operating Model](../extensions/regulatory/ai-governance-operating-model.md) provide the staffing formula:

```
FTE = (Volume × Sample Rate × Review Time) / Working Hours
```

**Example for a HIGH-tier customer-facing system (50,000 interactions/day, 5% human review):**

- 50,000 × 5% = 2,500 reviews/day
- At 10 minutes per review = ~416 hours/day
- At 7.5 productive hours per person = **55 FTE for human review alone**

**Example for a MEDIUM-tier internal system (50,000 interactions/day, 1% human review):**

- 50,000 × 1% = 500 reviews/day
- At 5 minutes per review = ~42 hours/day
- At 7.5 productive hours per person = **6 FTE**

The difference between MEDIUM and CRITICAL isn't a label - it's a 9x staffing difference for human oversight alone. When building business cases, model the operational cost for the actual tier, not the tier you wish it was.

### A clear path from pilot to scale

Most AI initiatives start small. The framework supports this through [Progression](../strategy/progression.md):

| Phase | What You Have | What You Need | Typical Duration |
|---|---|---|---|
| **Pilot** | AI in controlled environment, internal users | Basic guardrails, logging, feature flag kill switch | 2-4 weeks |
| **Limited production** | AI serving real users, constrained scope | Tier-appropriate controls, sampled Judge evaluation | 1-3 months |
| **Full production** | AI at target scale and scope | Full control stack for classified tier, trained operators | 3-6 months |
| **Autonomous operation** | AI taking actions without human approval per transaction | CRITICAL-tier controls, 100% Judge coverage, tested PACE, dedicated staff | 6-12 months from full production |

Each phase requires demonstrated operational maturity before progressing. You don't jump from pilot to autonomous operation. Henderson & Venkatraman's Strategic Alignment Model emphasises that alignment is bidirectional - business ambition shapes AI capability requirements, but AI operational reality should also shape business expectations.

## Your Starting Path

| # | Document | Why You Need It |
|---|---|---|
| 1 | [Cheat Sheet](../CHEATSHEET.md) | The entire framework on one page - know your tier in 2 minutes |
| 2 | [Fast Lane](../FAST-LANE.md) | Check if any of your products qualify for accelerated low-risk deployment |
| 3 | [Business Alignment](../strategy/business-alignment.md) | Four questions every AI initiative must answer - including cost and skills feasibility |
| 4 | [Risk Assessment](../core/risk-assessment.md) | Quantified methodology for understanding your actual risk exposure |
| 5 | [Cost & Latency](../extensions/technical/cost-and-latency.md) | The real numbers for control costs at each tier |

**If you run multi-agent products:** Add [MASO Overview](../maso/) - the seven control domains for multi-agent orchestration.

**If you're building the business case for controls:** Add [Risk Stories](../insights/risk-stories.md) for documented incident costs and the [Risk Assessment](../core/risk-assessment.md) worked examples.

**If you're planning AI strategy:** [From Strategy to Production](../strategy/) covers the full lifecycle from business alignment through data reality, human factors, and progression planning.

**To see the framework in action across a full enterprise:** Read [A Day in the Life](../strategy/enterprise-day-in-the-life.md) - what a single day looks like when eight AI systems across multiple departments operate under the framework, including a Business Owner quarterly planning session.

## What You Can Do Monday Morning

1. **Classify every AI system in your portfolio** using the [Risk Tiers](../core/risk-tiers.md). Map each product's AI to a tier. This gives you the portfolio view - and reveals whether any products are running at a higher tier than their controls support.

2. **Build a portfolio cost model.** For each product, map tier to control cost using the [Cost & Latency](../extensions/technical/cost-and-latency.md) analysis. Add staffing costs from the [Human Factors](../strategy/human-factors.md) assessment. Make these costs visible in each product's P&L.

3. **Identify shared infrastructure opportunities.** If multiple products need guardrails and Judge evaluation, build shared services. The alternative - each product team building independently - costs more and creates inconsistent security posture across your portfolio.

4. **Ask every product team two questions.** First: *"What happens when your AI gets it wrong?"* If they don't have a tested answer, they need [PACE Resilience](../PACE-RESILIENCE.md). Second: *"What's your human fallback?"* If the answer is "we'd figure it out," that's not a plan.

5. **Model the staffing requirement.** Use the FTE formula above for each product at its classified tier. Sum across the portfolio. If the total exceeds available capacity, either fund the gap or adjust the tier (by reducing autonomy, adding human review, or limiting scope). Operating a CRITICAL-tier system with MEDIUM-tier staffing is operating a CRITICAL-tier system without adequate controls.

## Common Objections - With Answers

**"Controls will slow down our time to market."**
The [Fast Lane](../FAST-LANE.md) exists specifically for this concern. Low-risk deployments (internal, read-only, no sensitive data, human-reviewed) deploy with basic guardrails in days. Only HIGH and CRITICAL tier systems need full controls - and those are the systems where moving fast without controls creates the incidents that slow you down for months (legal review, regulatory response, customer remediation).

**"We can't afford this level of security on every product."**
You don't need to. LOW-tier products need negligible investment. The cost concentrates at HIGH and CRITICAL tiers - which is where the risk concentrates. If a product's AI risk doesn't justify the control investment, reduce the tier by limiting autonomy or scope. The framework scales proportionately.

**"Our competitors aren't doing this."**
Your competitors either have controls you can't see, or they're accumulating risk they haven't yet realised. The regulatory environment is tightening - the EU AI Act, DORA, and sector-specific regulations are all increasing AI governance requirements. Being ahead of regulatory enforcement is a strategic advantage. Being behind it is a liability.

**"We don't have the people to operate these controls."**
This is the most honest objection and the most important one to address. The [Human Factors](../strategy/human-factors.md) assessment provides three paths: retrain existing staff (most operational roles), hire specialists (architecture and leadership), or reduce the tier by keeping humans in the loop (which trades automation for reduced control overhead). What you cannot do is deploy CRITICAL-tier systems with nobody trained to operate the controls.

**"Each business unit should decide its own AI risk appetite."**
Business units should inform risk appetite through their domain expertise. But risk appetite for AI is an enterprise governance decision - because a single AI incident in one business unit creates reputational and regulatory exposure for the entire organisation. The framework's [AI Governance Operating Model](../extensions/regulatory/ai-governance-operating-model.md) provides the structure for enterprise-level AI governance with business unit input.

