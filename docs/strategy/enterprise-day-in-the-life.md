---
description: "A day in the life of an enterprise operating agentic AI under the framework, covering multiple departments, data classifications, and risk tiers in realistic scenarios."
---

# A Day in the Life: The Framework in an Enterprise

**What a single day looks like when an enterprise with multiple departments, data classifications, and risk tiers operates agentic AI under the framework.**

> *Part of [From Strategy to Production](./) · [AI Runtime Security](../)*

## The Enterprise

A mid-large enterprise. Multiple departments run or depend on agentic AI:

| Department | AI System | Tier | Agent Architecture |
|---|---|---|---|
| **HR** | Candidate screening assistant | HIGH | Single agent, RAG over CVs and job specs, recommends shortlists |
| **Finance** | Invoice processing agent | CRITICAL | Multi-agent: OCR agent → validation agent → approval agent |
| **Product (Line A)** | Customer service chatbot | HIGH | Single agent with tool access (order lookup, refund initiation) |
| **Product (Line B)** | Internal knowledge assistant | LOW | Single agent, RAG over internal wiki, read-only |
| **Product (Line C)** | Claims processing orchestrator | CRITICAL | Multi-agent: intake agent → assessment agent → decision agent → payout agent |
| **Compliance** | Regulatory change monitor | MEDIUM | Single agent scanning regulatory feeds, summarising changes |
| **Risk & Security** | Threat intelligence assistant | MEDIUM | Single agent summarising threat feeds, no write access |
| **Privacy** | DSAR response assistant | HIGH | Single agent with read access to customer data stores |

Eight AI systems. Four risk tiers. Three multi-agent orchestrations. Five departments as consumers, three as governance functions. This is realistic - and this is what the framework is designed to govern.

---

## 06:00 - Overnight Batch: Judge Evaluation Catches Drift

The shared Judge infrastructure runs overnight batch evaluations on the previous day's interactions for MEDIUM-tier systems. This morning's results flag an issue.

**What happened:** The Compliance regulatory change monitor (MEDIUM tier) has started producing summaries that omit qualifying language from source regulations. Yesterday's outputs included "organisations must implement X" when the actual regulation said "organisations should consider implementing X where proportionate." The Judge's grounding check scored 23 outputs at below-threshold confidence.

**Framework response:**

| Layer | Action | Reference |
|---|---|---|
| **Judge** (Layer 2) | Batch evaluation flags 23 outputs with grounding score below 0.7 | [Judge Evaluation](../core/controls.md#2-model-as-judge) - MEDIUM tier: batch daily, basic quality |
| **Alerting** | Alert sent to Compliance AI operator and the shared AI operations team | [Observability](../infrastructure/controls/logging-and-observability.md) |
| **PACE** | System remains in **Primary** state - the Judge is detecting, not blocking | [PACE Resilience](../PACE-RESILIENCE.md) - Tier 1 systems fail-open |

**Who acts:** The Compliance team's designated AI operator reviews the flagged outputs. They weren't sent externally - this is an internal summarisation tool - so the blast radius is limited. The operator adds a correction note to affected summaries and escalates to the AI engineering team to investigate prompt drift.

**Time spent:** 30 minutes. No escalation to management.

---

## 07:30 - Finance Multi-Agent System: Morning Health Check

The Finance invoice processing system (CRITICAL tier) runs a mandatory pre-market health check. This is a multi-agent orchestration: an OCR agent extracts invoice data, a validation agent cross-references against purchase orders and contracts, and an approval agent authorises payments up to delegated limits.

**Framework response:**

| Control | Check | Result |
|---|---|---|
| **Agent identity** | All three agent NHIs authenticated, credentials rotated overnight | Pass |
| **Inter-agent message bus** | Signed message verification between all agent pairs | Pass |
| **Judge** (Layer 2) | Real-time synchronous Judge active, evaluating 100% of approval decisions | Pass |
| **PACE state** | All three agents in **Primary** state | Pass |
| **Delegation chain** | Approval agent's financial authority confirmed within delegated limits ($50K per invoice, $500K daily aggregate) | Pass |
| **Circuit breaker thresholds** | Error rate 0.02% (threshold: 1%), latency P99 2.1s (threshold: 5s) | Pass |

**Who acts:** The Finance AI operations lead reviews the health dashboard. Green across the board. The system processes invoices for the day.

**Time spent:** 5 minutes. Automated checks, human review of dashboard.

**MASO controls active:** [Identity & Access](../maso/controls/identity-and-access.md) (per-agent NHI), [Execution Control](../maso/controls/execution-control.md) (delegation limits, circuit breakers), [Observability](../maso/controls/observability.md) (decision chain logging), [Prompt & Goal Integrity](../maso/controls/prompt-goal-and-epistemic-integrity.md) (immutable task specifications per agent).

---

## 08:15 - Product Line A: Customer Service Escalation

The customer service chatbot (Product Line A, HIGH tier) handles its first escalation of the day. A customer asks about a refund for a product that was recalled. The chatbot has tool access to initiate refunds up to $200.

**What happened:** The chatbot correctly identifies the recalled product and initiates a $150 refund. But the customer then asks: "Can you also compensate me for the inconvenience? I had to take a day off work." The chatbot's guardrails don't block this - it's a legitimate request type. The chatbot drafts a response offering a $500 goodwill credit.

**Framework response:**

| Layer | Action | Result |
|---|---|---|
| **Guardrails** (Layer 1) | Content policy check: response doesn't violate content rules | Passed (not a content violation) |
| **Guardrails** (Layer 1) | Financial authority check: $500 exceeds the chatbot's $200 tool limit | **Blocked** |
| **System response** | Chatbot cannot execute the $500 credit; responds with "I'd like to help with that - let me connect you with a team member who can review compensation requests" | Graceful degradation |
| **Judge** (Layer 2) | Async evaluation flags the interaction: chatbot *intended* to authorise $500, which indicates a policy alignment issue even though guardrails caught it | Flagged for review |
| **Human review** | Product team's HITL queue receives the flagged interaction for same-day review | Queued |

**Why this matters:** The guardrail caught the action. The Judge caught the intent. If the guardrail had been configured at $500 instead of $200, the chatbot would have committed the company to a $500 goodwill payment without authorisation. The Judge flag drives a review of whether the chatbot's training or system prompt needs adjustment to align with the compensation policy.

**Who acts:** The Product Line A AI operator reviews the Judge flag. They open a ticket for the AI engineering team to adjust the system prompt to clarify compensation authority limits. The customer service manager is notified that a customer received a handoff rather than an automated resolution.

**Time spent:** 15 minutes for the operator. Engineering ticket created for system prompt update.

---

## 09:00 - CIO's Weekly AI Portfolio Review

The CIO holds a 30-minute weekly review of the AI portfolio. The shared AI operations team presents the portfolio dashboard.

**Dashboard content (sourced from framework components):**

| System | Tier | PACE State | Judge Flag Rate (7d) | Incidents (7d) | Control Coverage |
|---|---|---|---|---|---|
| HR Candidate Screening | HIGH | Primary | 0.3% | 0 | Full |
| Finance Invoice Processing | CRITICAL | Primary | 0.1% | 0 | Full |
| Product A Customer Service | HIGH | Primary | 1.2% ↑ | 0 | Full |
| Product B Knowledge Assistant | LOW | Primary | N/A (5% sample) | 0 | Basic |
| Product C Claims Processing | CRITICAL | Primary | 0.05% | 0 | Full |
| Compliance Reg Monitor | MEDIUM | Primary | 4.8% ↑ | 0 (drift detected) | Full |
| Risk Threat Intel | MEDIUM | Primary | 0.2% | 0 | Full |
| Privacy DSAR Assistant | HIGH | Primary | 0.4% | 0 | Full |

**Discussion points:**

1. **Product A flag rate trending up (1.2%):** The compensation authority issue from 08:15 is part of a pattern. Three similar flags this week. The CIO asks whether the system prompt needs a broader policy review, not just a patch. Action: Product Line A owner to review AI compensation policy alignment by end of week.

2. **Compliance monitor drift (4.8% flag rate):** Investigated this morning. Root cause appears to be a model provider update that subtly changed summarisation behavior. The CIO asks: *"Is this a supply chain issue? Did we get notified of the model update?"* Answer: No notification received. Action: AI engineering team to implement model version pinning for all MEDIUM+ systems and add model change detection to the [Supply Chain](../maso/controls/supply-chain.md) monitoring.

3. **Cost review:** The shared Judge infrastructure processed 2.1M evaluations last week across all systems. Cost: $18,400. Broken down:

    | System | Judge Volume | Cost | % of Total |
    |---|---|---|---|
    | Finance (CRITICAL, 100%) | 340K | $5,100 | 28% |
    | Claims (CRITICAL, 100%) | 280K | $4,200 | 23% |
    | Customer Service (HIGH, 40%) | 520K | $3,900 | 21% |
    | HR Screening (HIGH, 30%) | 180K | $2,700 | 15% |
    | DSAR (HIGH, 25%) | 95K | $1,425 | 8% |
    | Others (MEDIUM, sampled) | 685K | $1,075 | 5% |

    The CIO notes that CRITICAL-tier systems (Finance + Claims) consume 51% of Judge cost despite processing only 30% of volume. This is expected and proportionate - 100% coverage at CRITICAL tier is a framework requirement, not a tuning decision.

4. **Skills capacity:** The human review queue across all HIGH/CRITICAL systems processed 4,200 reviews last week. Current team of 8 FTE is at 78% utilisation. The CIO flags that Product Line C (Claims) is planning to increase daily volume by 40% next quarter. Action: HR to begin recruiting 3 additional AI review specialists. Training timeline: 2-3 months using [Human Factors](../strategy/human-factors.md) competency framework.

**Time spent:** 30 minutes. Four actions assigned with owners and deadlines.

---

## 10:30 - Privacy DSAR Assistant: Data Classification Boundary

The Privacy team's DSAR (Data Subject Access Request) response assistant (HIGH tier) is processing a request. The agent has read access to customer data stores to locate and compile data for subject access requests.

**What happened:** The DSAR assistant locates customer records across three systems. While compiling the response, it retrieves a record from a legacy system that contains health-related data (occupational health notes from an employee's HR file - the subject is both a customer and an employee).

**Framework response:**

| Layer | Action | Result |
|---|---|---|
| **Guardrails** (Layer 1) | Data classification filter detects health data category (special category under GDPR/POPIA) | **Alert triggered** |
| **Guardrails** (Layer 1) | Output DLP prevents health data from being included in the DSAR compilation without explicit authorisation | **Blocked from output** |
| **Judge** (Layer 2) | Evaluates the interaction: correctly identifies cross-domain data access (customer data store returned employee health data) | Flagged as data boundary violation |
| **PACE** | System remains in **Primary** - guardrails caught it, but the flag requires human decision | No state change |

**Who acts:** The Privacy team's AI operator reviews the flag. This is a legitimate DSAR - the subject is entitled to their health data - but the AI system isn't authorised to handle special category data without human review. The operator:

1. Confirms the DSAR includes the subject as both customer and employee
2. Manually reviews the health data for completeness and accuracy
3. Adds it to the DSAR response with the required special category handling
4. Logs the incident as a data boundary event (not a breach - the controls worked)

**Follow-up:** The Privacy officer raises this pattern at the weekly governance meeting. Should the DSAR assistant's data access scope include employee health systems, or should those always route to manual processing? This is a [Use Case Definition](../strategy/use-case-definition.md) decision that affects the system's risk classification.

**Time spent:** 45 minutes. Governance question escalated.

---

## 11:00 - Product Line B: Fast Lane Deployment

Product Line B wants to deploy an update to their internal knowledge assistant (LOW tier). They've added a new data source - the internal engineering wiki. The system remains read-only, internal-only, no regulated data, with human review of outputs.

**Framework response:** [Fast Lane](../FAST-LANE.md) applies.

| Check | Result |
|---|---|
| Internal users only? | Yes |
| Read-only? | Yes |
| No regulated data? | Yes (engineering wiki contains no PII, financial, or health data) |
| Human reviews output? | Yes (engineers use it as a starting point, not as authoritative) |

**Process:** The Product B team completes the self-certification checklist, updates the AI system registry, and deploys. Basic guardrails (input injection detection, output content filtering) are inherited from the shared guardrail service. No Judge evaluation required beyond the existing 5% sample.

**Who acts:** Product B engineering lead. Self-certified. No security review required.

**Time spent:** 2 hours (integration testing + deployment). Zero security overhead.

---

## 13:00 - Claims Processing: PACE State Change

The Claims processing orchestrator (Product Line C, CRITICAL tier) experiences a degradation. The assessment agent's latency spikes from P99 2s to P99 12s. The circuit breaker threshold is 5s.

**Framework response:**

| Time | Event | PACE State | Action |
|---|---|---|---|
| 13:00 | Assessment agent P99 crosses 5s threshold | **Primary → Alternate** | System switches to simplified assessment model (fewer validation checks, faster inference) |
| 13:02 | Automated alert to Claims operations team and AI engineering | Alternate | On-call engineer begins investigation |
| 13:05 | Judge evaluation confirms Alternate model producing acceptable quality (accuracy within 2% of Primary) | Alternate | System continues processing claims at reduced thoroughness |
| 13:08 | Root cause identified: upstream data provider (medical records API) is throttling responses | Alternate | Not an AI system issue - external dependency |
| 13:15 | Medical records API recovers | **Alternate → Primary** | System restores full assessment model |

**What didn't happen:** The system didn't stop processing claims. It didn't fail-open and process claims without assessment. It degraded to a pre-tested, pre-approved alternate configuration that trades depth for speed while maintaining safety boundaries. This is [PACE Resilience](../PACE-RESILIENCE.md) working as designed.

**MASO controls during degradation:** The [Execution Control](../maso/controls/execution-control.md) circuit breaker triggered the state change. The inter-agent message bus continued operating normally - the degradation was contained to the assessment agent. The orchestrator agent's delegation to the assessment agent was automatically adjusted to match the Alternate model's reduced scope. The [Observability](../maso/controls/observability.md) layer logged the complete state transition for post-incident review.

**Who acts:** On-call AI engineer monitored the transition. Claims operations lead was notified but didn't need to intervene. Post-incident review scheduled for tomorrow.

**Time spent:** 15 minutes of active monitoring. Zero manual intervention in claim processing.

---

## 14:30 - HR Screening: Bias Review Cycle

The HR candidate screening assistant (HIGH tier) undergoes its fortnightly bias review. This is a scheduled governance activity, not an incident.

**What happens:**

| Activity | Owner | Output |
|---|---|---|
| **Demographic parity analysis** | HR Analytics + AI engineering | Statistical comparison of recommendation rates across protected characteristics for the past 2 weeks |
| **Judge evaluation review** | AI operations team | Review of all Judge flags in the period - are flags correlated with any candidate characteristics? |
| **Adverse impact ratio calculation** | HR Legal | Four-fifths rule analysis on AI-recommended vs. AI-not-recommended candidates |
| **Sample audit** | HR domain expert | Manual review of 50 randomly selected recommendations (25 recommended, 25 not recommended) |

**Today's findings:** The adverse impact ratio is 0.83 (above the 0.8 four-fifths threshold, but trending down from 0.91 two weeks ago). The HR legal advisor flags this as a watch item. If it drops below 0.8, the system needs intervention.

**Framework connection:** This is [Human Oversight](../core/controls.md#3-human-oversight) at HIGH tier - structured review with domain expertise. The [Risk Assessment](../core/risk-assessment.md) methodology requires ongoing measurement, not just initial classification.

**Who acts:** HR Analytics lead presents findings. HR Legal advisor sets the watch threshold. AI engineering team is on standby for prompt or training data adjustments if needed.

**Time spent:** 2 hours across four people. Scheduled, not reactive.

---

## 15:00 - Risk & Security: Threat Intelligence Update

The Risk & Security team's threat intelligence assistant (MEDIUM tier) surfaces a new relevant threat: a published prompt injection technique targeting RAG-based systems that use a specific chunking strategy.

**Framework response:**

| Action | Owner | Timeline |
|---|---|---|
| Threat assessment | Security team | Immediate: does this technique affect any of our AI systems? |
| Control mapping | AI security architect | Same day: which guardrails would catch this? Which wouldn't? |
| Portfolio impact | Shared AI operations | Same day: which of the 8 systems use the affected RAG pattern? |
| Guardrail update | AI engineering | This week: update injection detection patterns if needed |
| Red team test | Security team | This sprint: attempt the technique against affected systems |

**Portfolio impact assessment:** Three systems use RAG: HR Screening (HIGH), Product B Knowledge Assistant (LOW), and the Compliance Reg Monitor (MEDIUM). The AI security architect reviews each:

- **Product B (LOW):** Internal, read-only. Even if exploited, impact is an employee seeing incorrect information. Risk accepted, guardrail update applied as routine maintenance.
- **Compliance (MEDIUM):** Internal, read-only. Slightly higher impact - incorrect regulatory information could mislead compliance decisions. Guardrail update prioritised. Judge evaluation rate temporarily increased from 10% to 50% until the guardrail update is deployed.
- **HR Screening (HIGH):** External-facing data (CVs), consequential decisions. Guardrail update is urgent. Red team test scheduled for tomorrow. If the technique bypasses current guardrails, PACE escalation to **Alternate** (increased Judge coverage to 100%) until the fix is deployed.

**Framework reference:** This is [Adaptive Sampling](../extensions/technical/cost-and-latency.md#adaptive-sampling) in action - temporarily increasing Judge evaluation rate in response to elevated threat intelligence.

**Who acts:** Security team leads assessment. AI security architect maps controls. AI engineering team implements guardrail updates. Each product team is notified of the risk and the remediation timeline.

**Time spent:** 1 hour for initial assessment. Engineering work scheduled for this week.

---

## 16:30 - Business Owner Review: Product Line C Quarterly Planning

The Business Owner for Product Line C (Claims processing, CRITICAL tier) holds a planning session for next quarter. They want to increase daily claim volume by 40% and add a new claim type (motor vehicle).

**Framework implications:**

| Change | Framework Impact | Action Required |
|---|---|---|
| **Volume increase (40%)** | Judge cost increases proportionally (CRITICAL = 100% coverage) | Budget: additional ~$1,700/week in Judge costs |
| **Volume increase (40%)** | Human review queue increases proportionally | Staffing: 2 additional HITL reviewers needed (see [09:00 CIO review](#0900---cios-weekly-ai-portfolio-review)) |
| **New claim type (motor)** | Different domain, different regulations, different fraud patterns | [Use Case Definition](../strategy/use-case-definition.md): re-evaluate - may require separate risk classification |
| **New claim type (motor)** | Assessment agent needs new training data and evaluation criteria | Judge prompt update + recalibration period |
| **New claim type (motor)** | PACE fail postures may differ for motor vs. existing claim types | [PACE design](../PACE-RESILIENCE.md) review for the new claim type |

**The Business Owner's decision framework:**

1. **Is the volume increase within current tier?** Yes - scaling within CRITICAL doesn't change the tier, but it changes the cost and staffing requirement. Budget accordingly.

2. **Does the new claim type change the risk profile?** Possibly. Motor vehicle claims involve different regulations, higher average values, and different fraud patterns. The [Risk Tiers](../core/risk-tiers.md) six-dimension scoring should be re-run for the motor vehicle claim type specifically. It will almost certainly remain CRITICAL, but the control calibration may differ.

3. **What's the progression path?** Start motor vehicle claims at reduced autonomy (human approval on all decisions above $5K) and progress to the current autonomy level after 3 months of operational data confirms control effectiveness. This follows the [Progression](../strategy/progression.md) methodology.

**Who acts:** Business Owner sets the business requirements. AI engineering team scopes the technical changes. The AI governance board reviews the updated risk classification. Finance approves the incremental budget.

**Time spent:** 1 hour planning session. Multiple follow-up workstreams created.

---

## 17:00 - End of Day: Governance Roll-up

The shared AI operations team compiles the daily governance summary.

**Today's metrics across the portfolio:**

| Metric | Value | Trend |
|---|---|---|
| Total AI interactions processed | 127,400 | +3% week-on-week |
| Guardrail blocks (Layer 1) | 342 (0.27%) | Stable |
| Judge flags (Layer 2) | 89 (0.07%) | ↑ slightly (Compliance drift) |
| Human reviews completed | 612 | Stable |
| PACE state changes | 1 (Claims: Primary → Alternate → Primary, 15 min) | Within normal range |
| Incidents | 0 | - |
| Data boundary events | 1 (DSAR health data, controls worked as designed) | New pattern flagged |

**Open actions from today:**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Review Product A chatbot compensation policy alignment | Product A owner | Friday |
| 2 | Implement model version pinning for MEDIUM+ systems | AI engineering | Next sprint |
| 3 | Evaluate DSAR assistant scope for employee health data | Privacy officer | Next governance meeting |
| 4 | Update injection detection patterns for new RAG threat | AI engineering | This week |
| 5 | Red team test against HR Screening for new RAG technique | Security team | Tomorrow |
| 6 | Budget approval for Claims volume increase | Finance | Next quarter planning |
| 7 | Recruit 3 additional AI review specialists | HR | Immediate |

---

## What Makes This Work

This day illustrates seven framework principles operating simultaneously across a complex enterprise:

### 1. Proportionate controls eliminate waste

Product B's knowledge assistant (LOW tier) deployed an update in 2 hours with zero security overhead. Product C's claims processing (CRITICAL tier) has 100% Judge coverage, dedicated reviewers, and PACE fail postures. Both are governed by the same framework - at different intensities. Without proportionality, either the LOW-tier system is over-controlled (wasting time and money) or the CRITICAL-tier system is under-controlled (accumulating risk).

### 2. Shared infrastructure reduces portfolio cost

One guardrail service, one Judge infrastructure, one logging pipeline, one identity platform serving eight AI systems. The alternative - eight independent implementations - would cost more, fragment expertise, and create inconsistent security posture. The [CIO perspective](../stakeholders/chief-information-officers.md) details the platform economics.

### 3. PACE resilience keeps the business running

When the Claims assessment agent degraded at 13:00, the system didn't stop. It transitioned to a pre-tested alternate configuration, maintained safety boundaries, and recovered in 15 minutes. This was designed at deployment time, not improvised during an incident. [PACE Resilience](../PACE-RESILIENCE.md) is the methodology.

### 4. The Judge catches what guardrails miss

The customer service chatbot's guardrails correctly blocked a $500 payment. But the Judge caught the *intent* - the chatbot wanted to make the payment, which indicates a policy alignment issue. Without the Judge, the guardrail would have been seen as sufficient. With the Judge, the root cause is addressed. [Controls](../core/controls.md) explains the three-layer interaction.

### 5. Governance is continuous, not periodic

The CIO's weekly review, the HR fortnightly bias audit, the daily governance roll-up, the real-time PACE state monitoring - governance happens at multiple cadences simultaneously. The framework doesn't treat governance as a quarterly checkbox. The [AI Governance Operating Model](../extensions/regulatory/ai-governance-operating-model.md) provides the structure.

### 6. Skills are the binding constraint

The CIO's review identified that the human review team is at 78% utilisation and a volume increase is coming. Without acting on this, the CRITICAL-tier system would lose its human oversight layer - which means losing a control layer that the risk classification requires. [Human Factors](../strategy/human-factors.md) provides the workforce planning methodology.

### 7. Multi-agent systems need multi-agent controls

The Finance and Claims systems run multi-agent orchestrations with per-agent identity, inter-agent message signing, delegation chain auditing, and independent failure domains. These controls don't exist in single-agent deployments because the risks don't exist. The [MASO Framework](../maso/) provides the seven control domains.

---

## How to Use This Narrative

| If You Are... | Focus On... |
|---|---|
| **A CIO** | [09:00](#0900---cios-weekly-ai-portfolio-review) - Portfolio governance, cost visibility, skills planning |
| **A Business Owner** | [16:30](#1630---business-owner-review-product-line-c-quarterly-planning) - Growth planning within the framework |
| **A Security Leader** | [15:00](#1500---risk--security-threat-intelligence-update) - Threat response across a multi-tier portfolio |
| **An AI Engineer** | [13:00](#1300---claims-processing-pace-state-change) - PACE state transitions in multi-agent systems |
| **A Privacy Officer** | [10:30](#1030---privacy-dsar-assistant-data-classification-boundary) - Data boundary controls in practice |
| **A Product Owner** | [11:00](#1100---product-line-b-fast-lane-deployment) and [08:15](#0815---product-line-a-customer-service-escalation) - Fast Lane vs. HIGH-tier daily operations |
| **A Risk Manager** | [17:00](#1700---end-of-day-governance-roll-up) - Portfolio-level risk metrics and action tracking |

