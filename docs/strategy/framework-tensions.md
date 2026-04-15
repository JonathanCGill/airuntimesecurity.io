---
description: "Where the security framework supports strategy, where it constrains choices, and how to navigate the tension between risk management and business value creation."
---

# Framework Tensions

*Where this framework supports strategy, where it's silent, and where it actively constrains strategic choices.*

> Part of [From Strategy to Production](README.md)

## The Nature of the Tension

A security controls framework and a business strategy want different things.

The framework asks: **"What could go wrong, and how do we prevent it?"**
Strategy asks: **"What value can we create, and how do we capture it?"**

These aren't opposed. Good security enables ambitious strategy by managing the risks that would otherwise kill projects or create crises. But they are in tension. Every control adds cost, time, and complexity. Every risk taken without controls adds exposure.

This article maps the tension points - where the framework actively helps strategy, where it's silent on strategic questions, and where it constrains choices that strategists would rather make freely. It also identifies where strategies will legitimately test the framework's limits, and what to do about it.

## Where the Framework Supports Strategy

### 1. Risk Tiers Prevent Over-Engineering

Without a risk framework, every AI deployment triggers the same security conversation. The same controls are debated. The same policies are applied. Everything takes the same amount of time.

The framework's [risk tiers](../core/risk-tiers.md) solve this by creating **proportionate** responses:

| Strategic Benefit | How |
|-------------------|-----|
| **Low-risk projects move fast** | Fast Lane deployments self-certify; no security review needed |
| **Resources focus where they matter** | Security team reviews HIGH/CRITICAL; not buried in LOW/MEDIUM assessments |
| **Business cases are realistic** | Control costs are known per tier; no negotiation or surprise |
| **Innovation isn't blocked** | The framework says "yes, with these controls" not "no" |

**Without the framework:** A team wanting to deploy an internal summarisation tool goes through the same review process as a team deploying autonomous credit decisions. The first team waits 8 weeks and gives up. The second team shortcuts the review because it takes too long. Both outcomes are worse than tiered assessment.

### 2. PACE Enables Confidence to Launch

The [PACE resilience model](../PACE-RESILIENCE.md) is strategically valuable because it answers the question that blocks most launches: **"What happens if it goes wrong?"**

Without PACE, the answer is "we don't know" - which is why risk-averse organisations never launch. With PACE, the answer is specific:

- Primary fails → Alternate activates (degraded but functioning)
- Multiple failures → Contingency (human-supervised only)
- Everything fails → Emergency (AI off, manual fallback)

**Strategic benefit:** Leaders can approve AI deployments because they know the worst case is "we turn it off and go back to manual" - not "we lose control and can't stop it."

### 3. Fast Lane Removes the Starting Friction

The single biggest strategic benefit of the framework is the [Fast Lane](../FAST-LANE.md). By defining criteria under which AI can be deployed *without security review*, the framework removes the most common blocker to AI adoption: the approval queue.

**Strategic impact:**
- First AI deployments can happen in weeks, not months
- Teams learn by doing, not by waiting
- Success stories build momentum for harder projects
- Security is positioned as an enabler, not a gatekeeper

### 4. Standards Alignment De-Risks Regulatory Strategy

The framework's [regulatory crosswalks](../extensions/regulatory/README.md) map controls to NIST AI RMF, ISO 42001, EU AI Act, and other standards. This supports strategy by:

- Reducing regulatory uncertainty ("if we do X, we're aligned with Y standard")
- Making compliance investment count for multiple regulations
- Providing evidence for board and audit committee
- Preparing for regulatory examinations before they happen

## Where the Framework Is Silent

The framework is a **security controls** framework. It deliberately doesn't cover several domains that strategy requires:

### 1. Value Assessment

The framework tells you what controls a Tier 2 deployment needs. It doesn't tell you whether the deployment is worth building. Business case development, ROI analysis, and value measurement are outside its scope.

**Strategic gap:** Organisations using only this framework have no mechanism for deciding *whether* to build - only *how to secure* what they build.

**What to do:** Use the [Business Alignment](business-alignment.md) assessment alongside the framework's risk classification. Classify both the risk and the value before committing.

### 2. Build vs. Buy

The framework is implementation-agnostic. Whether you build custom AI, use a platform (Bedrock, Azure, Vertex), or buy a SaaS product, the same controls apply. But the strategic implications are very different:

| Approach | Framework Implication | Strategic Implication |
|----------|----------------------|----------------------|
| **Build custom** | You implement all controls yourself | Maximum flexibility; maximum skill requirement; maximum cost |
| **Platform** | Platform provides some controls; you implement the rest | Moderate cost; vendor dependency; faster time to value |
| **SaaS product** | Vendor claims to handle controls; you verify and supplement | Least skill requirement; least control; hardest to customise |

The framework doesn't help you choose. It just tells you what controls must exist regardless.

### 3. AI Product Strategy

The framework secures AI systems. It doesn't help design them. Questions the framework doesn't answer:

- Which use cases should we prioritise?
- Should we build a platform or point solutions?
- Should we centralise AI or embed it in business units?
- What's our LLM provider strategy (single vendor, multi-vendor, open source)?
- How does AI fit into our broader digital strategy?

These are strategy questions. The framework provides constraints within which strategy operates, but it doesn't generate strategy.

### 4. Competitive Dynamics

The framework optimises for safety. Strategy must also optimise for speed. In competitive markets, being second to deploy AI customer service or AI-powered pricing means losing market share.

**The framework doesn't account for competitive pressure.** It says Tier 2 deployments need 20-50% Judge evaluation and 4-hour review SLAs. It doesn't say "unless your competitor launches first."

This is correct - security requirements shouldn't be weakened by competitive pressure. But it creates a tension that strategy must manage: how to deploy quickly while meeting control requirements.

**Resolution approaches:**
- Use vendor-managed controls to accelerate (platform guardrails are faster than custom-built)
- Deploy at a lower tier initially, then upgrade as controls mature (Tier 1 decision support → Tier 2 automated)
- Parallelise control implementation with system development (don't build sequentially)
- Accept that some competitive speed comes from accepting lower tiers - which means less capability, not less security

## Where the Framework Constrains Strategy

These are genuine tensions - places where the framework's requirements conflict with what strategy would prefer.

### 1. CRITICAL-Tier Costs Limit Business Cases

The framework's CRITICAL tier requires:
- 100% Judge evaluation
- 1-hour human review SLAs
- 7-year immutable logging
- Senior expert reviewers
- Full PACE resilience plan

At high volume, this is expensive. As calculated in [Business Alignment](business-alignment.md), a CRITICAL-tier system processing 50,000 interactions/day needs ~55 FTE for human review alone. Many business cases don't survive this math.

**The tension:** The framework correctly identifies these requirements as necessary for autonomous high-impact decisions. The strategy correctly identifies the cost as prohibitive for many organisations.

**Resolutions:**

| Approach | How It Works | Trade-off |
|----------|-------------|-----------|
| **Reduce scope to lower tier** | Keep humans in the decision loop → Tier 2 | Less autonomy, but dramatically lower control costs |
| **Reduce volume** | Apply autonomous AI only to a subset of decisions | Less coverage, but viable economics |
| **Improve Judge accuracy** | Better Judge → fewer false positives → fewer human reviews | Requires investment in Judge R&D; takes time |
| **Risk-based human review** | Not all CRITICAL outputs need human review - only Judge-flagged ones | Requires confidence in Judge accuracy; regulatory acceptance uncertain |
| **Challenge the classification** | Is this really CRITICAL? Could human oversight be restructured to make it HIGH? | Requires honest risk assessment, not wishful thinking |

### 2. Tier Downgrade Requirements Are Conservative

The framework requires 6+ months of stable operation and governance approval to downgrade a system's risk tier. This is sensible for safety but slow for strategy.

**Scenario:** An organisation deploys a customer service AI at Tier 2 (HIGH). After 3 months, data shows the AI is performing well: low error rate, high customer satisfaction, no incidents. They want to upgrade the AI's capability (give it write access to ticketing systems) but this would push it to CRITICAL. They'd rather *first* demonstrate that the current AI is safe at HIGH, then upgrade.

But the framework's downgrade path doesn't have an "upgrade with evidence" mechanism. Adding capability is a new risk classification, not a continuation of the existing one.

**The gap:** The framework treats capability expansion as a new assessment, not as a progression. A system that's proven safe at Tier 2 for 6 months should have an easier path to Tier 3 than a brand-new Tier 3 deployment - but the framework doesn't distinguish between them.

### 3. The Framework Assumes a Single Risk Tier Per System

In practice, AI systems often span multiple risk tiers:

| Component | Risk Tier | Reason |
|-----------|-----------|--------|
| FAQ responses | LOW | Public information, no decisions |
| Account balance inquiry | MEDIUM | Customer data, but read-only |
| Transaction dispute filing | HIGH | Write access, customer-facing action |
| Fraud alert suspension | CRITICAL | Autonomous decision with financial impact |

The framework classifies the *system* at the highest applicable tier. This means the FAQ component has CRITICAL-tier controls - 100% Judge evaluation on responses about your opening hours.

**The tension:** Over-controlling low-risk functions adds cost without proportionate risk reduction. But allowing mixed-tier controls within one system creates complexity and potential for misclassification.

**Resolutions:**

| Approach | How It Works | Trade-off |
|----------|-------------|-----------|
| **Separate systems** | Build FAQ separately from fraud management | Architecture complexity; may not be feasible in a single conversation |
| **Function-level classification** | Different controls for different capabilities within one system | Control complexity; harder to audit |
| **Classify by highest, optimise by sampling** | System is CRITICAL; but Judge evaluates only non-FAQ interactions at 100% | Requires reliable capability detection |
| **Accept the overhead** | Apply CRITICAL controls uniformly | Simpler to audit; more expensive to operate |

### 4. No "Experiment" Tier

The framework starts at Fast Lane (internal, read-only, no regulated data, human-reviewed). But some valuable experiments don't fit:

- Testing an AI chatbot with a small group of real customers (external users - fails Fast Lane criterion 1)
- Running an AI in shadow mode alongside a real decision system (may process regulated data - fails criterion 3)
- Deploying an AI prototype to a partner organisation (external - fails criterion 1)

These are experiments, not production systems. The risk is genuinely low because of limited scope and duration. But the framework doesn't have a mechanism for time-limited, scope-limited deployments at reduced control levels.

**The gap:** An "Experiment" tier could allow limited external deployments with time bounds, mandatory monitoring, and automatic shutdown - without requiring full Tier 2 controls that take months to implement.

### 5. Multi-Agent Progression Isn't Addressed

The framework's [MASO section](../maso/README.md) covers multi-agent security in detail. But the progression from single-agent to multi-agent isn't mapped.

An organisation with mature Tier 2 single-agent deployments wants to introduce multi-agent orchestration. The MASO framework starts at Tier 1 (Supervised - all writes require human approval). But the organisation's single-agent capability is already beyond this.

**The gap:** There's no guidance on how single-agent maturity translates to multi-agent readiness. Organisations either start MASO from scratch (losing momentum) or assume single-agent maturity transfers (it doesn't - multi-agent risks are fundamentally different).

## When Strategies Break the Framework

Some strategic decisions will exceed what the framework covers. This isn't failure - it's the framework meeting its limits.

### Scenario 1: Speed-to-Market Requires Parallel Control Development

**Strategy:** Deploy a customer-facing AI in 8 weeks to match a competitor launch.
**Framework:** Tier 2 deployment needs 20-50% Judge evaluation, trained HITL reviewers, PACE plan. These typically take 3-6 months.

**What happens:** The team deploys with basic guardrails only (Fast Lane controls) on a customer-facing system (Tier 2 risk). They plan to add Judge and HITL "in the next sprint."

**Framework view:** Non-compliant. The system is operating above its control level.
**Strategic view:** Necessary. The market opportunity has a window.

**Resolution:** Deploy at Tier 1 capability (decision support, not autonomous) with a documented plan and timeline for Tier 2 controls. Accept that the AI will be less capable initially - recommendations to human agents, not direct customer interaction - in exchange for faster launch. The framework supports this: the system is genuinely Tier 1 at launch, and the controls match.

**The honest version:** If the strategy *requires* Tier 2 capability on day 1, the framework says the controls must also be there on day 1. If they can't be, either the strategy adjusts or the risk is explicitly accepted by governance - documented, time-bound, with a remediation plan. This is an exception, not a norm.

### Scenario 2: Data Constraints Require Risk Acceptance

**Strategy:** Build an AI underwriting assistant for a new insurance market.
**Framework:** CRITICAL tier - automated decisions affecting financial outcomes. Maximum controls.
**Data reality:** Only 2 years of data in this market. Limited representativeness. Known gaps in claims history.

**What happens:** The AI is built. It works well on the available data. But the data limitations mean it will have blind spots. The framework's controls can detect when the AI is wrong, but they can't make the data better.

**Framework view:** The controls are implemented correctly. Residual risk from data quality is documented.
**Strategic view:** We need to enter this market now. We'll improve data over time.

**Resolution:** The framework supports this - through documented risk acceptance. The system operates at CRITICAL tier with full controls. The risk register includes "data quality limitations in [market]" with compensating controls (higher Judge scrutiny for this market segment, lower autonomy thresholds, mandatory human review for edge cases). The strategy proceeds with eyes open.

**Where the framework should be stronger:** It should explicitly integrate data quality into risk assessment. A CRITICAL-tier system with poor data is a higher residual risk than a CRITICAL-tier system with excellent data, even with identical controls. Currently the framework doesn't distinguish.

### Scenario 3: Innovation Requires Operating Beyond the Framework

**Strategy:** Build a novel AI application that doesn't fit existing risk categories - for example, an AI that generates personalised investment portfolio recommendations using real-time market data.
**Framework:** The risk tiers and controls exist. But the combination of real-time data, personalised financial advice, and regulatory implications (MiFID II suitability) creates a profile the framework's examples don't cover.

**What happens:** The risk classification team debates whether this is HIGH or CRITICAL. The guardrail patterns don't cover financial suitability. The Judge evaluation criteria need custom development. The HITL process requires investment advisory qualifications.

**Framework view:** Classify at the highest applicable tier. Implement controls accordingly. Use the [threat model template](../extensions/templates/threat-model-template.md) to identify specific risks.
**Strategic view:** This takes too long. The framework doesn't have ready-made controls for this use case.

**Resolution:** The framework is a **starting point**, not a finished product. For novel use cases:

1. Classify conservatively (CRITICAL if in doubt)
2. Implement the framework's generic controls (guardrails, Judge, HITL)
3. Develop use-case-specific criteria (what does "good" look like for investment recommendations?)
4. Document gaps between the framework's controls and the use case's needs
5. Feed learnings back into the framework (contribute to the framework's evolution)

## Managing the Tensions

### The Governance Conversation

Every tension between framework and strategy should be resolved through governance, not by ignoring the framework or abandoning the strategy.

The right forum is the AI governance committee (or equivalent), with this agenda:

| Input | Question | Decision |
|-------|----------|----------|
| **Strategic priority** | What are we trying to achieve and why does it matter? | Is this a genuine priority? |
| **Framework requirement** | What controls does the framework specify? | Are the requirements understood? |
| **Gap analysis** | Where do the requirements exceed current capability? | What's the specific gap? |
| **Options** | What are the resolution approaches? | Which approach balances risk and value? |
| **Risk acceptance** | If we proceed with reduced controls, what's the residual risk? | Is the residual risk within appetite? |
| **Timeline** | When will full controls be in place? | Is the remediation plan credible? |
| **Monitoring** | How will we know if the risk materialises? | What are the trigger points? |

### When to Change the Framework

If multiple strategic initiatives hit the same framework limitation, the framework may need to change. Signs:

| Signal | Possible Framework Change |
|--------|--------------------------|
| Many projects stuck at Tier 1 because Tier 2 controls take too long to implement | Introduce an intermediate tier or streamlined Tier 2 path |
| Every system is classified at the highest tier because components span tiers | Introduce function-level risk classification |
| Innovation projects bypass the framework entirely | Introduce an experiment tier with time-limited controls |
| Organisations can't staff CRITICAL-tier human review requirements | Revisit whether 100% Judge evaluation can reduce human review volume |
| Multi-agent deployment stalls because MASO Tier 1 is too restrictive | Define a progression path from single-agent maturity to multi-agent |

The framework explicitly invites this. The [Maturity & Validation](../MATURITY.md) section acknowledges gaps and encourages feedback. Strategy that tests the framework's limits is exactly the kind of feedback that improves it.

## Summary

| Aspect | Framework Position | Strategic Reality | Resolution |
|--------|-------------------|-------------------|------------|
| **Speed** | Controls take time | Markets don't wait | Deploy at lower tier; upgrade with evidence |
| **Cost** | Controls cost money | Business cases are tight | Match tier to what's funded; don't pretend CRITICAL-tier costs are MEDIUM-tier costs |
| **Flexibility** | Single tier per system | Systems span multiple risks | Function-level classification or separate systems |
| **Innovation** | Framework covers known patterns | Novel use cases exceed patterns | Start conservative; develop custom criteria; feed back |
| **Progression** | Tiers are static once classified | Capability evolves | Build explicit progression with readiness criteria |
| **Human factors** | Controls assume competent operators | People need time to learn | Include human readiness in deployment criteria |
| **Data quality** | Framework assumes adequate data | Data is often poor | Include data quality in risk assessment |

The framework is a tool for managing risk. Strategy is the process of deciding which risks to take. The best outcomes come from using both - not from letting either dominate the other.

