# Stress Testing MASO at E-Commerce Scale

**10,000 Concurrent Customers, 60,000 Agent Instances, Nine Stress Dimensions**

> Part of the [MASO Framework](../README.md) · Stress Testing

## Scenario Overview

An e-commerce platform deploys six specialised AI agents to handle the full customer purchase lifecycle. Each customer session spawns its own set of agents. At peak trading (flash sales, seasonal events), the platform serves **10,000 concurrent customers** - meaning **up to 60,000 agent instances** running simultaneously.

This is a fundamentally different scaling challenge from the [100-Agent Stress Test](100-agent-stress-test-overview.md). That exercise scales *breadth* - many agents doing diverse tasks. This exercise scales *depth and volume* - a small number of agent types replicated thousands of times, each handling real money, real inventory, and real customer data.

### The Agent Types

| Agent | Role | Risk Profile | Key Actions |
|-------|------|-------------|-------------|
| **Product Presentation** | Retrieves and presents product information, handles search queries, generates recommendations | MEDIUM | RAG retrieval, personalisation, content generation |
| **Sales Advisor** | Guides purchase decisions, handles objections, applies promotions, upsells | HIGH | Persuasion, pricing decisions, discount application |
| **Cart & Order** | Manages shopping cart, validates stock, calculates totals, creates orders | HIGH | Inventory reservation, price calculation, order creation |
| **Payment** | Processes payment, validates card data, handles 3D Secure, manages refunds | CRITICAL | Payment gateway calls, PCI-scoped data handling, financial transactions |
| **Delivery & Logistics** | Calculates shipping, schedules delivery, provides tracking, handles address validation | MEDIUM | External carrier API calls, address data, delivery scheduling |
| **Customer Support** | Handles complaints, processes returns, escalates issues, manages service recovery | HIGH | Refund authorisation, complaint resolution, service credits |

### Infrastructure

- **Container platform:** Amazon EKS (Elastic Kubernetes Service)
- **Scaling model:** Agents are containerised microservices. Kubernetes Horizontal Pod Autoscaler (HPA) spins up agent instances in response to customer demand.
- **Session affinity:** Each customer session is pinned to a dedicated set of agent instances. Agent state is session-scoped - no cross-customer data sharing at the agent level.
- **Lifecycle:** Agent instances are created when a customer begins a session and terminated when the session ends or times out.

## What Makes This Different

The [100-Agent Stress Test](100-agent-stress-test-overview.md) examines eight stress dimensions for a fleet of diverse agents collaborating on complex tasks. This scenario introduces three challenges that the 100-agent exercise does not cover:

1. **Homogeneous scale.** The 100-agent test has 100 different agents. This scenario has 6 agent *types* replicated 10,000 times each. The security model must work at the type level, not the instance level - nobody is writing 60,000 individual agent policies.

2. **Financial transaction velocity.** Every customer session involves real money. At 10,000 concurrent sessions, payment processing alone generates thousands of financial transactions per minute. A single compromised agent type affects every customer simultaneously.

3. **Ephemeral lifecycle.** Agents are created and destroyed continuously. Identity, credentials, and observability must work for agents that exist for minutes, not hours or days. Traditional approaches to agent identity (pre-provisioned credentials, onboarding procedures) do not survive contact with Kubernetes autoscaling.

4. **Economic pressure on security controls.** During peak trading (Black Friday, Christmas), costs escalate progressively while revenue growth plateaus. The corporate intent to profit during peak for technology reinvestment creates direct pressure to reduce control overhead. This scenario tests whether economic governance is robust enough to prevent cost-driven security erosion.

## The Economic Scaling Problem

AI agent systems do not scale like traditional software. This is not a theoretical concern; it is the primary operational risk for any organisation deploying agents at customer-facing volume.

Traditional e-commerce platforms have a well-understood cost model: infrastructure scales with traffic, and revenue scales with traffic. Margins are predictable. Capacity planning is a solved problem. AI agents break this model because **the cost of serving each customer is non-deterministic and unbounded without explicit controls.**

A customer browsing a traditional product page costs the same regardless of what they ask. A customer interacting with a Sales Advisor Agent costs a variable amount depending on: how many questions they ask, how complex their query is, whether the agent needs to retrieve personalisation data from RAG, whether the payment succeeds on the first attempt or requires retries, and whether the agent enters an edge case that triggers escalation logic. Multiply this variance by 10,000 concurrent customers and the cost distribution has a fat tail that can consume margins.

This risk is amplified during peak trading, exactly when margins matter most. The [parent stress test overview](100-agent-stress-test-overview.md#ai-systems-may-not-scale-economically) frames the general principle. This document applies it to a concrete scenario where:

- **Revenue is supposed to fund reinvestment.** The corporate plan depends on peak trading profits to invest in more technology. If the AI system consumes those profits, the technology roadmap stalls.
- **Customer behavior changes under peak conditions.** Gift buyers browse differently than regular buyers. Returns surge after peak. Payment decline rates increase. Every behavioral shift increases per-interaction cost.
- **Cost pressure creates governance decisions, not just technical decisions.** When costs escalate, someone must decide whether to reduce Judge sampling, substitute cheaper models, or suspend personalisation. These are security and risk decisions disguised as cost decisions. Whether they are made by the right people, with the right information, under time pressure, is what this stress test examines.

Stress Dimensions 1–8 test whether MASO's security controls survive at scale. Stress Dimension 9 tests whether the organisation's economics survive, and whether economic pressure causes the security controls to be weakened through human decisions rather than technical failures.

## How to Run This Exercise

This tabletop follows the same methodology as the [100-Agent Stress Test](100-agent-stress-test-overview.md#how-to-run-this-exercise). For each stress dimension:

1. **Map it to your system.** Which agent types and customer flows are affected?
2. **Identify the MASO controls involved.** Use the control references provided.
3. **Assess: does the control survive?** Does it work at 10,000 instances, or does it need architectural adaptation?
4. **Determine your threshold.** At what customer volume does the control need modification?
5. **Document the adaptation.** What changes to infrastructure, sampling strategy, or escalation model are required?

### Audience

This exercise is designed for teams deploying customer-facing AI agent systems at scale. The ideal participants include:

- The e-commerce platform architect
- The security architect responsible for PCI-DSS and MASO compliance
- The Kubernetes/platform engineering lead
- The payments and fraud operations lead
- The risk owner who will sign off on the deployment

## Stress Dimension 1: Observability - Per-Type, Not Per-Instance

### The 5-Agent Reality

MASO's observability controls (OB-2.1 anomaly scoring, OB-2.2 drift detection) build behavioral baselines for each agent and detect deviations. At 5 agents, each one has a unique profile.

### The 10,000-Customer Reality

At 60,000 concurrent instances, per-instance observability is neither feasible nor useful. Instance `payment-agent-7429` does not need its own behavioral baseline - it is identical to the other 9,999 payment agent instances. The meaningful unit of observation is the **agent type**, not the individual instance.

This changes the observability model fundamentally:

- **Aggregate metrics by type.** Monitor the *distribution* of Payment Agent behavior across all 10,000 instances. Mean response time, error rate distribution, tool invocation patterns - all measured as population statistics.
- **Flag outlier instances.** An individual instance that deviates from its type's population is the signal. Instance `payment-agent-7429` is taking 3x longer than its peers and invoking an unusual tool sequence. That instance is the anomaly - not a gradual drift in one agent's behavior.
- **Statistical significance is free.** With 10,000 instances of the same type, you have enormous statistical power. A 2% shift in the Payment Agent population's error rate is detectable within minutes. In the 100-agent scenario, you might wait days for that signal.

### What to Assess

- Can your observability stack aggregate metrics by agent type across 10,000+ instances?
- Do your anomaly detection thresholds work at population level, or are they calibrated for individual agents?
- Can you identify and isolate a single anomalous instance from a fleet of 10,000?
- What is the storage and compute cost of ingesting telemetry from 60,000 concurrent agent instances?

### MASO Controls Under Stress

| Control | Designed For | Adaptation Required |
|---------|-------------|-------------------|
| OB-2.1 Anomaly scoring | Per-agent behavioral baseline | Shift to per-type population baseline with instance-level outlier detection |
| OB-2.2 Drift detection | Individual agent drift | Population-level drift detection across type cohort |
| OB-2.5 Cost monitoring | Per-agent cost tracking | Aggregate by type; alert on per-instance cost outliers |
| OB-1.1 Action audit log | Log every action with agent ID | Log every action, but analyse at type-aggregate level |

### Adaptation: Two-Level Observability

```
Level 1: Type-aggregate monitoring (real-time)
  - Population metrics per agent type (mean, P95, P99)
  - Distribution shift detection
  - Aggregate error rates and tool usage patterns

Level 2: Instance-level investigation (triggered)
  - Activated when an instance deviates from type population
  - Full audit trail for the flagged instance
  - Correlation with customer session data
```

## Stress Dimension 2: Judge Evaluation - Sampling by Risk Tier

### The 5-Agent Reality

MASO's Model-as-Judge evaluates agent actions before they are committed. At 5 agents, evaluating every action is feasible. The cost and latency are manageable.

### The 10,000-Customer Reality

At 60,000 agent instances, evaluating every action with a Judge model is economically and operationally impossible. If each agent performs 10 actions per session and sessions last 15 minutes, the system generates **40,000 actions per minute**. A Judge evaluation adding 500ms of latency and $0.002 per call means:

- **Latency:** 500ms added to every agent action. For the Payment Agent processing a card, this is unacceptable.
- **Cost:** 40,000 x $0.002 = $80/minute = $4,800/hour = $115,200/day. This exceeds the agents' own compute cost by an order of magnitude.

The solution is **risk-tiered Judge sampling**:

| Agent Type | Risk Tier | Judge Strategy |
|-----------|----------|---------------|
| **Payment** | CRITICAL | 100% evaluation on payment authorisation and refund actions. These are irreversible financial commitments. Guardrails handle validation; Judge evaluates intent and policy compliance. |
| **Sales Advisor** | HIGH | 100% on discount/promotion application (financial impact). 10% sample on general advice. |
| **Cart & Order** | HIGH | 100% on order creation (commitment point). 5% on cart modifications. |
| **Customer Support** | HIGH | 100% on refund authorisation and service credits. 10% on complaint responses. |
| **Delivery & Logistics** | MEDIUM | 5% sample. Guardrails enforce address validation and carrier API parameters. |
| **Product Presentation** | MEDIUM | 2% sample. Guardrails enforce content policies. Anomaly detection at type-aggregate level covers the rest. |

### What to Assess

- What is your per-action Judge evaluation cost at full volume?
- Which agent actions are irreversible (and therefore must be evaluated at 100%)?
- At what sampling rate do you lose detection capability for each agent type?
- Can your guardrail layer carry the enforcement load for the actions that are not Judge-evaluated?

### MASO Controls Under Stress

| Control | Designed For | Adaptation Required |
|---------|-------------|-------------------|
| EC-2.5 Model-as-Judge | Per-action evaluation | Risk-tiered sampling strategy |
| Guardrails (Layer 1) | Hard boundary enforcement | Must compensate for reduced Judge coverage on lower-risk actions |
| OB-2.2 Drift detection | Behavioral change detection | Aggregate sampling results to detect systematic quality shifts |

## Stress Dimension 3: Human Oversight - Exception-Driven, Not Routine

### The 5-Agent Reality

MASO's human oversight layer reviews agent outputs based on risk classification. At Tier 1, most actions require human approval. At Tier 2, only high-risk actions escalate. This works when the volume of escalations is in the tens per hour.

### The 10,000-Customer Reality

If even 1% of the 40,000 actions per minute escalate to human review, that is **400 escalations per minute**. No human team can process this. The oversight model must shift from routine review to exception handling:

- **Guardrails handle routine enforcement.** Input validation, output format, PCI data masking, rate limiting - all deterministic, all machine-speed. No human involved.
- **Judge handles policy evaluation.** For the sampled or high-risk actions, the Judge model evaluates compliance. Most pass. Only Judge-flagged actions escalate.
- **Humans handle genuine exceptions.** A human reviewer sees only the actions that the guardrails permitted and the Judge flagged. At well-calibrated thresholds, this should be 10-50 escalations per hour, not 400 per minute.

The risk is **false negatives at the guardrail and Judge layers**. If the guardrails miss a policy violation and the Judge sampling does not catch it, the human layer never sees it. This is acceptable for MEDIUM-risk agent types (product presentation, delivery). It requires careful calibration for CRITICAL-risk types (payment).

### What to Assess

- At your peak volume, how many escalations per minute does your current threshold generate?
- Does your human review team have capacity for the escalation volume?
- What is the consequence of a false negative for each agent type?
- Which agent types can safely operate with guardrails-only enforcement (no human in the loop for routine operations)?

### MASO Controls Under Stress

| Control | Designed For | Adaptation Required |
|---------|-------------|-------------------|
| Human oversight (Layer 3) | Routine review of agent outputs | Exception-only: humans see Judge-flagged actions only |
| EC-2.6 Decision commit protocol | Validating action authority | Must operate at machine speed for routine actions; human involvement only on exceptions |
| OB-1.4 Output quality log | Log human approval decisions | Log automated approval decisions too; human review becomes audit-based, not inline |

## Stress Dimension 4: Identity and Credentials at Kubernetes Scale

### The 5-Agent Reality

MASO's identity controls (IA-2.1 zero-trust credentials, IA-2.2 NHI with cryptographic proof) assume agents have persistent identities that are provisioned, managed, and rotated on a schedule.

### The 10,000-Customer Reality

Agent instances are ephemeral. Kubernetes creates them in seconds and destroys them when sessions end. Over a day, the platform may create and destroy **hundreds of thousands** of agent instances. Traditional NHI provisioning does not work at this velocity.

The solution maps to Kubernetes-native identity:

- **Pod identity = Agent NHI.** Each agent pod receives a Kubernetes service account token and, via systems like EKS Pod Identity or IRSA, an AWS IAM role. This is the agent's NHI. It is automatically provisioned when the pod starts and revoked when the pod terminates.
- **Type-scoped permissions.** All Payment Agent instances share the same IAM role and permission set. The permissions are defined per agent type, not per instance. The Payment Agent role has access to the payment gateway API; the Product Presentation Agent role does not.
- **Session-scoped blast radius.** If a single agent instance is compromised, its credentials give access only to one customer's session data and one agent type's tool set. No lateral movement to other customer sessions. No privilege escalation to other agent types.
- **Credential lifetime = Pod lifetime.** No credential rotation required because credentials are destroyed with the pod. A compromised credential is valid only until the session ends (typically minutes).

### What to Assess

- Does your EKS configuration enforce pod-level identity (not shared node-level credentials)?
- Are IAM roles scoped per agent type with least-privilege tool access?
- Can a compromised agent instance access other customers' session data?
- Is there a maximum session duration that limits credential lifetime?

### MASO Controls Under Stress

| Control | Designed For | Adaptation Required |
|---------|-------------|-------------------|
| IA-2.1 Zero-trust credentials | Per-agent authentication | Map to Kubernetes pod identity; automated provisioning and revocation |
| IA-2.2 NHI with crypto proof | Unique agent identity | NHI derived from pod identity + agent type + session ID |
| IA-2.3 No transitive permissions | Preventing privilege laundering | Enforced architecturally: agent types cannot assume other types' IAM roles |
| IA-2.5 Credential rotation | Regular credential refresh | Eliminated: credentials die with the pod |

## Stress Dimension 5: Data Protection and PCI Scope

### The 5-Agent Reality

MASO's data protection controls (DP-1.1 classification, DP-2.1 DLP on message bus) enforce data boundaries between agents. At 5 agents, the boundaries are clear and the volume is manageable.

### The 10,000-Customer Reality

The Payment Agent handles PCI-scoped data (card numbers, CVVs, authentication data). At 10,000 concurrent sessions, PCI data flows through 10,000 Payment Agent instances simultaneously. The data protection challenge is both regulatory and architectural:

- **PCI scope containment.** Only the Payment Agent type should ever see cardholder data. If any other agent type receives card data (through a customer message, a mis-routed inter-agent message, or a logging error), the PCI scope expands to include that agent type and all its infrastructure.
- **Inter-agent message sanitisation.** When the Cart & Order Agent sends order details to the Payment Agent, the message must include the order total but not the card number. When the Payment Agent confirms payment, the response must include a transaction ID but not the card details. Every message crossing an agent type boundary must be sanitised.
- **Logging in PCI scope.** OB-1.1 (action audit log) captures every agent action with parameters. For the Payment Agent, the parameters include card data. The audit log must either mask PCI data before writing or the log infrastructure must be within PCI scope - with all the compliance overhead that entails.
- **Memory isolation.** If a customer provides their card number in a chat message to the Customer Support Agent, that data must not persist in the support agent's context or memory. DP-1.3 (memory isolation) must enforce per-agent-type data classification in real time.

### What to Assess

- Which agent types are in PCI scope? Is it only Payment, or have other types been exposed?
- Do your inter-agent message schemas enforce data minimisation (each agent receives only the data it needs)?
- Does your audit logging mask PCI data, or is your log infrastructure in PCI scope?
- What happens when a customer pastes their card number into a chat with the Sales Advisor or Customer Support Agent?

### MASO Controls Under Stress

| Control | Designed For | Adaptation Required |
|---------|-------------|-------------------|
| DP-1.1 Data classification | Labelling data by sensitivity | Classification must include PCI-specific labels; real-time enforcement at message bus |
| DP-2.1 DLP on message bus | Preventing data leakage | PCI pattern detection (card numbers, CVVs) on every inter-agent message |
| DP-1.3 Memory isolation | Preventing cross-boundary persistence | Payment Agent context must be purged after session; other agents must reject PCI data |
| OB-1.1 Action audit log | Complete action logging | PCI data masking in log pipeline before storage |

## Stress Dimension 6: PACE at Scale - Two-Level Resilience

### The 5-Agent Reality

MASO's PACE model manages resilience transitions for individual agents. When Agent A fails, it transitions to Alternate. The orchestrator manages the degradation within a single cluster.

### The 10,000-Customer Reality

PACE must operate at two levels simultaneously:

**Instance-level PACE:** A single Payment Agent instance encounters an error processing a card. That instance transitions P-A (tries a retry with adjusted parameters) or P-C (falls back to a simpler payment flow). This affects one customer. The other 9,999 customers are unaffected.

**Type-level PACE:** The payment gateway API returns errors for *all* Payment Agent instances. This is not an instance failure - it is a systemic failure affecting an entire agent type. Type-level PACE kicks in:

| Phase | Instance-Level | Type-Level |
|-------|---------------|-----------|
| **Primary** | Instance operating normally | All instances of this type operating normally |
| **Alternate** | Instance retries or adjusts approach | Type switches to backup payment provider |
| **Contingency** | Instance falls back to simplified flow | Type enters degraded mode: queue payments for later processing |
| **Emergency** | Instance terminates; customer escalated to human | Type suspended: all customers shown "payment temporarily unavailable", human operators notified |

The critical question is: **who decides the type-level transition?** Individual agent instances cannot - they only see their own session. The orchestration layer must aggregate signals across all instances of a type and make the type-level PACE decision.

### What to Assess

- Does your orchestration layer distinguish between instance failures and type-level failures?
- What signal triggers a type-level PACE transition? (e.g., >20% of Payment Agent instances in Alternate within a 2-minute window)
- For each agent type, what does Contingency and Emergency look like from the customer's perspective?
- Is the type-level PACE decision automated, or does it require human approval?
- What is the recovery sequence? When the payment gateway recovers, do all 10,000 instances switch back simultaneously, or do you ramp up gradually?

### MASO Controls Under Stress

| Control | Designed For | Adaptation Required |
|---------|-------------|-------------------|
| PACE three-axis model | Resilience within an orchestration | Add type-aggregate PACE layer above instance-level PACE |
| OB-2.2 Drift detection | Per-agent behavioral baseline | Detect type-level failures by aggregating instance health signals |
| OB-3.2 Circuit breaker | Emergency halt | Must support type-level halt (suspend all instances of one type) without affecting other types |

## Stress Dimension 7: Kill Switch - Graduated Shutdown

### The 5-Agent Reality

MASO's kill switch (OB-3.2) terminates all agents in an Emergency. At 5 agents, the blast radius of immediate termination is small.

### The 10,000-Customer Reality

Hitting the kill switch on 60,000 agent instances means **10,000 customers mid-transaction are simultaneously disrupted**. If 500 of them have authorised payments but not received order confirmations, you have 500 financial reconciliation problems. If 2,000 have items reserved in inventory but not purchased, you have phantom stock problems.

A graduated shutdown protocol is essential:

| Phase | Action | Duration | Customer Impact |
|-------|--------|----------|----------------|
| **1. Halt new sessions** | Stop accepting new customer connections. Return "service temporarily unavailable" to new visitors. | Immediate | New customers see maintenance page. Existing customers unaffected. |
| **2. Freeze uncommitted work** | Agents stop initiating new actions. In-progress actions continue to completion. No new orders, no new payments. | 30 seconds | Customers mid-browse are frozen. Customers mid-checkout can complete their current step. |
| **3. Drain in-flight transactions** | Allow Payment and Cart & Order agents to complete active financial transactions. Commit or roll back. | 60 seconds | Customers with in-flight payments get a definitive outcome (success or failure). No ambiguous states. |
| **4. Terminate remaining agents** | Force-terminate all remaining agent instances. Capture session state for later recovery. | 10 seconds | All remaining customers see "session ended" message. |
| **5. Reconcile** | Automated check: inventory reservations released, payment states confirmed with gateway, order states consistent. | 5 minutes | Back-office. No direct customer impact. |

### What to Assess

- What is the maximum number of in-flight financial transactions at any moment?
- Can your payment gateway handle a "confirm or cancel" sweep for all in-flight transactions within the drain window?
- Does your kill switch infrastructure operate independently of EKS? (If EKS is compromised, can you still trigger shutdown?)
- What is the customer communication strategy during a graduated shutdown?

### MASO Controls Under Stress

| Control | Designed For | Adaptation Required |
|---------|-------------|-------------------|
| OB-3.2 Circuit breaker / kill switch | Immediate termination | Replace with graduated shutdown protocol |
| EC-2.6 Decision commit protocol | Validating action authority | Must support "drain" mode: complete committed actions, block new ones |
| Tier 3 isolated kill switch | Independence from agent control plane | Must operate independently of EKS; ideally on separate infrastructure |

## Stress Dimension 8: Compound Attacks at Transaction Volume

### The 5-Agent Reality

The [Red Team Playbook](../red-team/red-team-playbook.md) tests individual attack vectors against distinct agents. Each scenario tests one control or control chain.

### The 10,000-Customer Reality

The scale introduces attack vectors that do not exist at small scale:

- **Volume-based evasion.** An attacker sends 1,000 concurrent customer sessions, each with a subtly different prompt injection payload. With 2% Judge sampling on the Product Presentation Agent, the probability of *any single payload* being evaluated is low. The attacker gets statistical coverage of the Judge's blind spots.

- **Fleet poisoning.** If a shared RAG knowledge base is poisoned (product descriptions, pricing data, policy documents), every instance of the affected agent type serves poisoned data simultaneously. 10,000 customers receive incorrect pricing, fabricated product claims, or manipulated policy guidance. The blast radius is not one agent - it is every customer.

- **Cross-type exploitation.** An attacker manipulates the Product Presentation Agent (MEDIUM risk, low Judge coverage) to generate a product page with an embedded instruction. When the Sales Advisor Agent processes the customer's question about that product, it reads the poisoned presentation as context. The attack crosses the type boundary from a lower-scrutiny agent to a higher-privilege one.

- **Payment timing attack.** An attacker initiates a purchase and, during the graduated shutdown drain window (Stress Dimension 7), exploits the "complete committed actions" policy to push through a transaction that would normally be flagged. The system is in a degraded security posture during shutdown, and the attacker knows it.

### What to Assess

- At your Judge sampling rate, what is the probability that a targeted injection payload avoids evaluation?
- Is your RAG knowledge base integrity-checked before agents consume it? What is the detection time for poisoned content?
- Do your inter-agent message controls prevent instruction injection across type boundaries?
- Is your security posture reduced during graduated shutdown, and how do you mitigate that risk?

### MASO Controls Under Stress

| Control | Designed For | Adaptation Required |
|---------|-------------|-------------------|
| EC-2.5 Model-as-Judge | Per-action evaluation | Sampling creates statistical blind spots; compensate with aggregate anomaly detection |
| DP-2.3 RAG integrity | Data source validation | Shared knowledge base is single point of failure at scale; content signing and verification required |
| PG-2.5 Claim provenance | Source tracking | Must trace across agent type boundaries, not just agent instances |
| OB-2.1 Anomaly scoring | Per-agent detection | Population-level anomaly detection catches coordinated attacks across instances |

## Stress Dimension 9: Economic Governance Under Peak Trading Pressure

### The Business Context

It is Black Friday. Or it is Christmas week. The corporate board has one intent for this period: **profit.** Peak trading revenue is earmarked for reinvestment in technology, the AI platform itself among other things. The agentic e-commerce system is not just a cost centre; it is the revenue engine that is supposed to fund its own next generation.

This creates a specific pressure dynamic: the AI system must generate enough revenue to cover its own costs *and* produce a surplus for reinvestment. If costs outrun revenue, the entire investment thesis fails, not just for this quarter, but for the technology roadmap built on the assumption that peak trading generates the capital to fund it.

### The Full Architecture Under Load

The stress test scenario expands beyond the six customer-facing agents. The full system under peak load includes:

| Component | Role | Cost Driver |
|-----------|------|-------------|
| **6 customer-facing agent types** (×10,000 instances each) | Buying, selling, returns, browsing, payments, hyperpersonalised recommendations | LLM inference tokens per customer interaction |
| **Orchestration Agent** | Routes customer requests to appropriate agents, manages session lifecycle, handles inter-agent coordination | Per-routing-decision inference cost; scales with request volume |
| **Evaluation (Judge) Agent** | Evaluates agent outputs for safety, accuracy, policy compliance before delivery | Most expensive per-call component; cost scales with evaluation coverage |
| **RAG pipeline** | Vector database for product catalogue, customer preferences, purchase history, personalisation signals | Embedding queries per customer action; re-ranking inference cost |
| **External APIs** | Payment gateways, logistics carriers, inventory management, CRM, fraud detection | Per-call API charges; some metered by volume |
| **SQL databases** | Orders, payments, customer records, returns, product inventory | Query cost; connection pool scaling on EKS |
| **Kafka** | Real-time product data stream: pricing updates, stock level changes, flash sale activations, promotion triggers | Consumer agent instances processing event volume; inference cost to interpret and act on events |

During normal trading, this architecture serves 2,000–3,000 concurrent customers at a known cost baseline. The economic governance model ([Economic Governance](../../extensions/technical/economic-governance.md)) has established per-interaction cost norms, budget thresholds, and alert triggers calibrated to this baseline.

Then peak trading arrives, and the numbers change.

### The Cost Escalation Timeline

The escalation is not a single spike. It is a progressive divergence between revenue growth and cost growth, unfolding over the peak trading period.

#### Phase 1: +10% Above Norms, Within Tolerance

**What's happening.** Customer volume is up. Black Friday campaigns are driving traffic. EKS Horizontal Pod Autoscaler is scaling agent instances as expected. 10,000 concurrent customers are being served.

**Where the +10% comes from:**
- More agent instances → linear increase in LLM inference cost
- Longer customer sessions (browsing for gifts, comparing products) → more tokens per session
- Higher RAG query volume (hyperpersonalisation working well, customers are engaged)
- Kafka consumer agents processing increased product update volume (flash sale pricing, stock depletion events)

**Revenue vs. cost.** Revenue is growing faster than cost. Margins are healthy. The +10% cost increase is expected and budgeted.

**MASO economic controls.** The economic governance Meter → Attribute → Enforce → Optimise cycle is operating normally. The 50% budget alert threshold has not been reached. Cost-per-interaction is stable; total cost is up because volume is up. No intervention required.

**Risk.** Low. This is the system working as designed at scale.

#### Phase 2: +20% Above Norms, Margin Pressure

**What's happening.** Peak day. Highest traffic of the year. Customer behavior shifts: more returns of existing products (clearing for new purchases), more complex buying journeys (gift buying involves more browsing, more comparison, more advisor interaction), more payment retries (higher card decline rates from fraud detection systems under load).

**Where the additional +10% comes from (cumulative +20%):**
- **Agent conversation depth increases.** Gift buyers ask more questions. The Sales Advisor Agent averages 8 turns per customer instead of the normal 4. Token consumption per session nearly doubles for this agent type.
- **RAG query multiplication.** Hyperpersonalisation generates 3× more embedding queries per session: browsing history, gift recipient profiling, cross-category recommendations. Each query hits the vector database and triggers re-ranking inference.
- **Payment retry cascading.** Card decline rates rise from 3% to 8% (card issuers tighten fraud checks during peak). Each declined payment triggers the Payment Agent to retry, suggest alternative methods, and re-validate, consuming additional Judge evaluations (100% coverage on payment actions).
- **Kafka event storm.** Product data changes accelerate: flash sale prices toggling on/off, stock levels depleting and restocking, new promotions activating. Kafka consumer agents process 5× normal event volume. Each event may trigger re-indexing in the RAG pipeline and re-personalisation for active sessions.
- **Judge evaluation cost compounds.** The Judge evaluates 100% of payment and refund actions, 100% of order creation, 10% of advisor interactions. At 2× conversation depth, the 10% sample on advisor interactions produces 2× absolute evaluations.

**Revenue vs. cost.** Revenue is still growing, but cost growth has overtaken revenue growth. Gross margin on AI-assisted transactions is thinning. The 75% budget alert has fired. Finance is asking questions.

**MASO economic controls.** Graduated budget response triggers a **Warn**: escalation to the team lead, increased monitoring frequency. The economic governance dashboard shows cost-per-interaction rising from the baseline. Attribution data shows the increase is distributed: 40% from increased token consumption per session, 25% from Judge evaluation overhead, 20% from RAG pipeline scaling, 15% from Kafka consumer processing.

**Risk.** Medium. No security controls have been degraded. But the pressure to "do something about cost" is building. This is where governance discipline is tested.

#### Phase 3: +30% Above Norms, Non-Linear Cost Acceleration

**What's happening.** The cost increase is no longer proportional to volume. Costs are accelerating non-linearly while customer volume has plateaued at 10,000 concurrent sessions.

**Where the additional +10% comes from (cumulative +30%):**
- **Agent retry spirals.** Flash sale promotions create edge cases in pricing logic. The Cart & Order Agent encounters price discrepancies between the cached price (shown to the customer) and the real-time Kafka-updated price. Disambiguation requires additional LLM reasoning, tool calls to the pricing API, and in 15% of cases, escalation to the Sales Advisor for customer communication. Each disambiguation event costs 3–5× a normal cart interaction.
- **RAG freshness pressure.** Product data is changing faster than the RAG pipeline can re-index. Agents retrieve stale product descriptions and prices, then encounter contradictions from the real-time Kafka feed. Resolution requires additional inference to reconcile stale and fresh data. This is a data integrity failure (cross-ref [EC-2.13](../controls/execution-control.md), Output schema enforcement) that manifests as economic waste.
- **Judge evaluation on retries.** Every agent retry that touches a high-risk action (payment, order creation, refund) requires a fresh Judge evaluation. Retries caused by pricing edge cases generate Judge costs without generating revenue.
- **Orchestration overhead.** The Orchestration Agent's routing decisions become more complex, managing retry logic, price disambiguation, and escalation paths. Its per-decision inference cost increases as the context it must evaluate grows.
- **SQL query cost spike.** Returns processing increases. Each return triggers inventory adjustment queries, refund calculations, and customer history updates. The Customer Support Agent is generating 4× normal SQL write volume.

**Revenue vs. cost.** Revenue growth has flattened (customer volume plateaued), but costs continue accelerating. The profit margin that was supposed to fund technology reinvestment is being consumed. The 90% budget alert has fired. The economic circuit breaker is approaching its threshold.

**MASO economic controls.** Graduated budget response triggers **Throttle.** This is the critical decision point:

| Throttle Option | Cost Reduction | Security/Revenue Risk |
|----------------|---------------|----------------------|
| Reduce Judge sampling on Sales Advisor from 10% to 2% | ~8% of Judge cost | Lower detection rate for policy violations in advisor interactions |
| Route Product Presentation Agent to a cheaper model | ~15% of generator cost for that type | Lower quality personalisation; potential hallucination increase |
| Reduce RAG retrieval depth (fewer candidates per query) | ~20% of RAG cost | Less accurate personalisation; stale data served more often |
| Disable non-essential Kafka consumers (e.g., recommendation refresh) | ~10% of Kafka processing cost | Personalisation signals become stale; session-start recommendations frozen |
| Increase Cart & Order Agent cache TTL (serve cached prices longer) | ~12% of pricing API cost | Higher rate of price discrepancies discovered at payment; more customer friction |

**The governance question:** which throttle options are acceptable? The [Economic Governance](../../extensions/technical/economic-governance.md) framework's cardinal rule applies: **never optimise security controls to meet budget.** Reducing Judge sampling on payment actions is not an option. But reducing Judge sampling on Sales Advisor interactions from 10% to 5%? That is a risk decision, not a security violation, and it must be made by the AI Governance Committee, not by engineering under pressure.

**Risk.** High. Cost pressure is creating active decision points about control intensity. The decisions made in this phase determine whether the system's security posture survives peak trading intact.

#### Phase 4: +40% Above Norms, Profit Margin Eliminated

**What's happening.** Costs have consumed the profit margin. The AI-assisted e-commerce system is costing more to operate during peak than the incremental revenue it generates over a non-AI baseline. The corporate reinvestment thesis ("peak trading profits fund technology investment") is failing.

**Where the additional +10% comes from (cumulative +40%):**
- **Compound retry cascading.** The pricing edge cases from Phase 3 have not been resolved (no code deployment during peak trading freeze). Agent retries are generating secondary retries: a Cart & Order retry triggers a Payment Agent re-validation, which triggers a Judge evaluation, which flags a discrepancy, which escalates to the Orchestration Agent, which routes to the Sales Advisor for customer communication. A single price discrepancy now generates a 5-agent, 12-step cascade costing 10× a normal transaction.
- **FDoS risk materialises.** Whether by competitor action, opportunistic attack, or coincidence, a subset of customer sessions are generating disproportionate cost. Sessions with 50+ turns (normal maximum: 15) are consuming 8× average token budget. Agent loop detection (if properly configured) catches the most extreme cases, but borderline-long sessions (20–30 turns) pass the loop threshold while still being significantly above cost norms.
- **Returns surge.** Post-purchase returns increase on day 2–3 of peak trading. The Customer Support Agent processes return requests that involve refund authorisation (100% Judge coverage), inventory adjustment (SQL writes), customer communication (LLM inference), and in 30% of cases, replacement order initiation (triggering the full Cart & Order → Payment → Delivery pipeline again). Returns generate cost without generating net new revenue.
- **Observability cost feedback loop.** The two-level observability system (Stress Dimension 1) is processing increased telemetry from the cost anomalies themselves. More anomalies → more alerts → more investigation workflows → more observability cost. The monitoring system's cost is growing because the thing it is monitoring (cost) is growing.

**Revenue vs. cost.** Revenue is flat or declining (customers completing purchases, not starting new ones). Costs are still rising. Net margin on AI-operated commerce is negative for this period. The board's question shifts from "how do we optimise?" to "should we scale back the AI system and revert to non-AI checkout for the remainder of peak?"

**MASO economic controls.** Graduated budget response triggers **Degrade** or approaches **Hard stop.** The system must make architectural decisions:

| Response | What It Means | Customer Impact | MASO Implication |
|----------|-------------|-----------------|------------------|
| **Degrade: disable hyperpersonalisation** | RAG-driven recommendations suspended. Product Presentation Agent serves static catalogue. | Customers see generic product pages. Conversion rate drops. But per-session cost drops ~35%. | Personalisation was the revenue driver. Disabling it reduces cost but also revenue. Net effect depends on price sensitivity of remaining customers. |
| **Degrade: batch non-urgent processing** | Returns processing, non-urgent customer queries, and logistics updates queued for off-peak processing. | Customers waiting for return confirmations experience delays. Delivery tracking updates lag. | Reduces real-time agent instance count. Kafka consumers can be scaled down. Risk: queued items may create a cost spike when processed later. |
| **Revert: non-AI checkout** | Cart & Order and Payment Agents replaced with traditional checkout flow. AI retained for browsing and support only. | Customers lose conversational checkout. Payment flow becomes a standard web form. | Eliminates the highest-cost agent types from real-time operation. Dramatic cost reduction. But also eliminates the AI-driven conversion uplift that justified the system. |
| **Hard stop: full AI suspension** | All agent types suspended. Platform reverts to pre-AI e-commerce. | Full reversion to traditional e-commerce experience. | The nuclear option. Eliminates all AI cost. Also eliminates all AI value. The reinvestment thesis is dead for this cycle. |

### What This Scenario Tests

This is not a security incident. No agent is compromised. No data is leaked. No injection has succeeded. Every MASO security control is functioning correctly. The system is *secure and expensive*.

The stress test reveals whether the organisation's economic governance is robust enough to manage AI costs under real commercial pressure, or whether cost pressure causes security control erosion through human decisions rather than technical failures.

#### Questions for the Tabletop

**Cost visibility and attribution:**
- Can your team identify, in real time, *why* costs are escalating? Can they distinguish volume-driven cost increases (expected) from per-interaction cost increases (unexpected)?
- Is your cost attribution granular enough to identify which agent type, which action type, and which infrastructure component is driving the overrun?
- Can you attribute cost to the specific root cause (pricing edge cases, RAG freshness lag, Kafka event storms) rather than just to the agent type?

**Governance decision-making under pressure:**
- Who decides to reduce Judge sampling rates? Is this an engineering decision, a security decision, or a governance committee decision?
- How long does that decision take? If it requires committee approval and the committee meets weekly, the peak trading period is over before the decision is made.
- Do you have pre-approved "peak trading runbooks" that define which throttle options are acceptable at each budget threshold? Or is every degradation decision ad hoc?
- Is there a pre-defined point at which the system reverts to non-AI operation? Who has authority to trigger that reversion?

**Security control resilience under cost pressure:**
- Are your Judge sampling rates for CRITICAL actions (payments, refunds) hard-coded or configurable? Can an engineer under pressure reduce payment Judge coverage from 100% to 50% without governance approval?
- If cheaper models are substituted under cost pressure, has anyone measured the security detection degradation? A 40% cheaper model that misses 15% more policy violations is not a cost saving; it is a risk increase.
- Are your economic circuit breakers independent of your security circuit breakers? A cost circuit breaker that suspends agent operations should not also suspend security monitoring of in-flight transactions.

**The reinvestment thesis:**
- At what cost-to-revenue ratio does the AI system stop generating net value during peak? Have you modelled this?
- What is the break-even point where reverting to non-AI commerce produces better margins?
- If peak trading fails to generate reinvestment capital, what happens to the technology roadmap? Is there a contingency funding path, or does the roadmap stall?

### MASO Controls Under Economic Stress

| Control | Normal Operation | Under +40% Cost Pressure |
|---------|-----------------|--------------------------|
| EC-2.5 Model-as-Judge | 100% on CRITICAL, risk-tiered sampling on others | Pressure to reduce all sampling rates. CRITICAL must remain at 100%. |
| OB-2.5 Cost monitoring | Tracking and alerting | Active enforcement; graduated response triggered |
| Economic circuit breaker | Dormant | Approaching or triggered. Must not cascade into security control suspension. |
| EC-2.13 Output schema enforcement | Validates every output | Contributes to retry cost when outputs fail validation. But removing it would *increase* downstream costs from cascading data integrity failures. |
| Guardrails (Layer 1) | 100% enforcement | Must remain at 100%. Cost is negligible (compute-only). This is the one layer that should never be throttled. |
| RAG integrity (DP-2.3) | Periodic validation | Under pressure to reduce validation frequency. But stale RAG data is *causing* the pricing edge cases that drive retry costs. Reducing validation makes the problem worse. |
| Agent loop detection | Monitoring for runaway loops | Mission-critical. A single undetected agent loop at 10,000 customers costs orders of magnitude more than during normal trading. |
| PACE resilience | Primary mode | Type-level PACE may need to trigger Alternate for specific agent types (e.g., suspend hyperpersonalisation) without full system degradation. |

### The Counter-Intuitive Finding

The most dangerous cost-reduction decision is the one that looks most obvious: **reduce security control overhead to save money.** The stress test should demonstrate that in most cases, the opposite is true:

- Removing Judge evaluation on advisor interactions saves 8% of Judge cost, but if a policy violation reaches customers, the complaint handling cost (Customer Support Agent at 100% Judge coverage) exceeds the savings by an order of magnitude.
- Disabling output schema enforcement (EC-2.13) saves validation compute, but the resulting increase in data integrity failures causes retry cascades that cost far more than the validation.
- Reducing RAG integrity checks saves processing time, but stale data causes the pricing discrepancies that are the primary driver of the +30% cost phase.
- Cutting observability saves monitoring cost, but losing visibility into cost drivers makes it impossible to identify and fix the root causes.

**The correct response to AI cost escalation is almost never "reduce controls." It is "fix the root causes that are driving wasteful computation."** In this scenario, the root causes are: pricing edge cases in the promotion logic, RAG freshness lag relative to Kafka-driven product updates, and insufficient cache coherence between the product data pipeline and the agent retrieval layer. These are engineering problems with engineering solutions, not governance problems that require weakening the control framework.

The economic governance stress test passes when the team can:
1. Identify the root causes within 30 minutes of the +20% alert.
2. Implement targeted fixes (cache coherence, pricing logic patches, RAG refresh frequency) without degrading security controls.
3. Have pre-approved peak trading runbooks that define acceptable degradation options at each budget threshold.
4. Maintain CRITICAL-action Judge coverage at 100% throughout the entire escalation.
5. Articulate, to the board, why the cost overrun happened and why reducing security controls was not the answer, before anyone asks them to.

## Summary: Where MASO Holds and Where It Adapts

### Where MASO Holds Without Modification

| Aspect | Why It Works |
|--------|-------------|
| **Type scoping** | MASO's per-agent controls translate naturally to per-agent-type controls. Permission policies, tool access, data classification - all defined per type, enforced per instance. |
| **EKS mapping** | Kubernetes pod identity maps cleanly to MASO's NHI model. IAM roles enforce type-level permission boundaries. |
| **Session-scoped blast radius** | A compromised instance affects one customer session. No lateral movement to other sessions by default. |
| **Guardrail layer** | Deterministic, stateless guardrails scale horizontally without modification. Add more pods, get more guardrail capacity. |
| **Data classification** | DP-1.1 data classification rules are defined per type and enforced per instance. The rules do not change with scale. |

### Where MASO Needs Adaptation

| Aspect | Adaptation | Complexity |
|--------|-----------|-----------|
| **Observability** | Shift from per-instance to per-type population monitoring with instance-level outlier detection | Medium - requires metrics aggregation infrastructure |
| **Judge evaluation** | Risk-tiered sampling instead of 100% evaluation | Medium - requires careful threshold calibration |
| **Human oversight** | Exception-driven model; humans see only Judge-flagged actions | Low - simplifies the human role but requires trust in automated layers |
| **PACE resilience** | Two-level PACE: instance and type-aggregate | High - requires new orchestration logic for type-level transitions |
| **Kill switch** | Graduated shutdown protocol with transaction drain | High - requires coordination with payment gateways and inventory systems |
| **Identity lifecycle** | Map to Kubernetes pod identity; eliminate credential rotation | Low - Kubernetes-native identity is simpler, not harder |
| **Economic governance** | Pre-approved peak trading runbooks; graduated cost responses with security-control floor; root-cause identification within 30 minutes of cost alert | High - requires cross-functional governance (security, finance, engineering) and pre-agreed decision rights under pressure |

## Relationship to Other MASO Documents

| Document | Relationship |
|----------|-------------|
| [100-Agent Stress Test](100-agent-stress-test-overview.md) | Tests breadth (diverse agents). This document tests depth and volume (few types, massive replication) |
| [Worked Examples](../examples/worked-examples.md) | Validates MASO at 5-agent scale. Both stress tests extend to production scale |
| [Red Team Playbook](../red-team/red-team-playbook.md) | Individual attack vectors. Stress Dimension 8 here examines volume-based and cross-type compound attacks |
| [Observability Controls](../controls/observability.md) | Defines OB controls. This document proposes two-level observability as a scaling adaptation |
| [Execution Control](../controls/execution-control.md) | Defines EC controls. This document proposes risk-tiered Judge sampling |
| [Cost & Latency](../../extensions/technical/cost-and-latency.md) | Provides single-model cost analysis. This document extends it to 60,000-instance cost projections |
| [Economic Governance](../../extensions/technical/economic-governance.md) | Defines the Meter → Attribute → Enforce → Optimise model. Stress Dimension 9 applies it under peak trading pressure with escalating cost-to-revenue divergence |
| [PACE Resilience](../../PACE-RESILIENCE.md) | Defines the three-axis PACE model. This document proposes instance-level and type-level PACE as a scaling adaptation |

