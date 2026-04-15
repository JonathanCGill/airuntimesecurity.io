# Containment Through Declared Intent

<!-- golden-thread-nav -->
!!! tip "Part of the Golden Thread (2 of 14)"
    Previous: [Why AI Security Is a Runtime Problem](why-ai-security-is-a-runtime-problem.md) · Next: [Process-Aware Evaluation](process-aware-evaluation.md) · [See the full sequence](../reading-paths.md#the-golden-thread-guardrails-judges-and-why-they-work-together)
<!-- golden-thread-nav -->

*If you know what an agent is supposed to do, every layer of defence has a reference point.*

## The Theory

An AI agent with no declared purpose is uncontrollable. You cannot write guardrails for it because you do not know what to constrain. You cannot judge its outputs because you do not know what "correct" looks like. You cannot monitor it for anomalies because you have no baseline for normal.

An AI agent with a clearly declared intent is a fundamentally different problem. You know what it should do. You know what it should not do. You know what data it needs, what tools it should use, what outputs it should produce, and what boundaries it must respect.

That knowledge - declared, codified, and enforced - is the foundation of every control in this framework.

**The thesis:** If intent is properly articulated upfront, and downstream systems enforce hard limits aligned with that intent, agent behavior is confined to predictable parameters. Not perfectly. Not absolutely. But within limits that are monitorable, auditable, and defensible.

This is a **constrain-regardless** architecture. Permissions derive from declared business intent - what the use case requires - not from evaluation of what the model can do. If the model's hidden capabilities cannot manifest because the containment boundary prevents them, those capabilities are operationally irrelevant as a breakout vector. This is why [containment beats evaluation](why-containment-beats-evaluation.md) as the primary security control.

Critically, containment operates on the **action space** (what the model may *do*) while leaving the **reasoning space** unconstrained (how the model may *think*). This is the key distinction. The entire value of deploying AI lies in its ability to handle ambiguity, generalise, and synthesise. None of that requires unrestricted action. A model summarising customer complaints needs full reasoning freedom. It does not need the ability to call external APIs or modify databases. Containment preserves the value of AI precisely because it does not attempt to control AI's reasoning - only its actions.

Think of it as parental. A good parent does not script what a child says or thinks. They set boundaries - don't cross the road, don't touch the stove, come home before dark. Within those boundaries, the child has full autonomy. The boundaries are non-negotiable. The behavior within them is free. And the parent watches - not to control every action, but to notice when something looks wrong. Containment is the boundary. The Judge is the parent watching. Human oversight is the parent stepping in when passive observation is insufficient.

## How Intent Flows Through the Defence Stack

Each layer of the framework's control architecture serves a different function. Intent is what gives each layer its reference point.

### Layer 1: Guardrails - The Hard Limits

Guardrails are deterministic, machine-speed constraints. They do not interpret. They do not negotiate. They enforce.

But enforce *what*? Without intent, guardrails are generic: block profanity, mask PII, rate-limit API calls. These are useful but blunt. With declared intent, guardrails become purpose-specific:

- A **payment agent** whose intent is "process card transactions for customer orders" gets guardrails that enforce: PCI data handling, transaction amount ceilings, approved payment gateway endpoints only, no access to product catalogue data.
- A **product recommendation agent** whose intent is "suggest relevant products based on browsing history" gets guardrails that enforce: read-only data access, no pricing modifications, no access to payment data, content policy compliance on generated descriptions.

The same guardrail infrastructure, configured differently because the intent is different. The intent specification is the input to the guardrail configuration.

**What guardrails catch:** Actions that violate the declared boundaries - the things the agent was never supposed to do, regardless of circumstances. This is [infrastructure beating instructions](infrastructure-beats-instructions.md). You do not tell the payment agent "please don't access the product catalogue." You give it credentials that cannot access the product catalogue. The intent tells you which credentials to provision.

### Layer 2: The Judge - Semantic Alignment

Guardrails catch mechanical violations. The Judge catches semantic ones - actions that are technically permitted but do not align with the declared purpose.

A sales advisor agent with intent "guide customers toward suitable products based on their stated needs" operates within its guardrails. But the Judge evaluates: is the agent actually guiding based on customer needs, or is it pushing the highest-margin product regardless of fit? Is it applying discounts appropriately, or giving away margin to close every sale? Is its persuasion proportionate, or is it manipulating?

These are semantic questions. They require understanding what the agent was *supposed* to accomplish. Without the intent specification, the Judge can assess coherence and policy compliance in the abstract. With intent, it can assess *alignment* - is this agent doing what it was deployed to do, in the way it was meant to do it?

The [intent layer](the-intent-layer.md) describes this pattern in detail: Declare, Execute, Evaluate. The intent specification gives the Judge its evaluation criteria.

### Layer 3: Human Oversight - Accountability and Calibration

Humans cannot review every agent action at scale. That is the premise of this framework - [exception-driven oversight](humans-remain-accountable.md), not routine approval.

Intent determines what gets escalated. A payment agent processing a transaction within normal parameters does not need human review. The same agent processing a refund that exceeds the declared intent's maximum refund threshold does. The escalation rule is derived from the intent: "this action falls outside what this agent was supposed to do."

Humans also calibrate the other layers. When a Judge flags an action that turns out to be legitimate, the intent specification may need refinement - it was too narrow. When a guardrail blocks a valid tool call, the intent specification may need to expand the agent's permitted scope. The declared intent is a living document that improves through operational feedback.

### Layer 4: Monitoring and Observability - Detecting Violations

MASO's observability controls (anomaly scoring, drift detection, communication profiling) watch for agents that deviate from expected behavior. Expected behavior is defined by - intent.

If a delivery logistics agent with intent "calculate shipping options and schedule deliveries" starts making unusually frequent calls to the customer support API, that is an anomaly. Not because API calls are forbidden (they might be within its technical permissions), but because they are inconsistent with the declared purpose. The monitoring layer knows this because it knows the intent.

At scale, this becomes population-level monitoring. Ten thousand instances of the same agent type, all with the same declared intent, should exhibit similar behavior. An instance that deviates from the population is the signal. The intent defines the population's expected behavior profile.

### Layer 5: PACE - Resilience When Intent Cannot Be Fulfilled

PACE (Primary, Alternate, Contingency, Emergency) manages what happens when an agent cannot fulfil its declared intent. The payment gateway is down. The recommendation engine's data source is stale. The delivery carrier's API is returning errors.

Without intent, PACE is generic: try again, fall back, degrade, halt. With intent, each phase is purpose-specific:

| Agent Intent | Primary | Alternate | Contingency | Emergency |
|---|---|---|---|---|
| Process card payments | Charge via primary gateway | Charge via backup gateway | Queue for later processing | Display "payments temporarily unavailable" |
| Recommend products | Personalised recommendations | Category-level popular items | Static bestseller list | "Browse our catalogue" fallback |
| Calculate shipping | Real-time carrier quotes | Cached rate tables | Flat-rate shipping only | "Shipping calculated at checkout" |

Each degradation path is coherent because it degrades *toward* a simpler version of the same intent, not toward arbitrary fallback behavior.

## Downstream Intent Awareness

This is where the theory becomes architecturally distinctive. It is not enough for each agent to know its own intent. **Downstream agents must understand the intent of the agents they interact with.**

When Agent A (intent: "retrieve current market data for portfolio analysis") passes data to Agent B (intent: "produce risk assessment from market data"), Agent B should know:

1. **What Agent A was trying to do.** If Agent A's output looks like product recommendations instead of market data, Agent B can flag the mismatch before processing it.
2. **What constraints Agent A was operating under.** If Agent A was restricted to 30-day data windows, Agent B should not treat the data as if it covers 12 months.
3. **What confidence level Agent A attached.** If Agent A flagged uncertainty on a data point, Agent B should propagate that uncertainty rather than treating it as established fact.

This is the epistemic integrity problem that MASO's PG controls address: [claim provenance](../maso/controls/prompt-goal-and-epistemic-integrity.md) (PG-2.5), [uncertainty preservation](../maso/controls/prompt-goal-and-epistemic-integrity.md) (PG-2.7), and [goal integrity monitoring](../maso/controls/prompt-goal-and-epistemic-integrity.md) (PG-2.2).

The intent specification is the contract between agents. Agent A declares what it intended to produce. Agent B validates that what it received matches that declaration. If there is a mismatch - the data does not look like what Agent A's intent said it would produce - Agent B escalates rather than processing potentially compromised input.

This is how you stop epistemic cascades. Not by hoping each agent checks its own work, but by having each agent verify that what it received is consistent with the upstream agent's declared purpose.

## The Confinement Model

Put together, the defence stack creates a confinement model:

**Walls (Guardrails):** Hard infrastructure limits derived from intent. The agent physically cannot access systems, data, or tools outside its declared purpose. Not "shouldn't" - *cannot*.

**Surveillance (Judge + Observability):** Continuous evaluation of whether the agent's behavior aligns with its declared purpose. The Judge evaluates semantic alignment. Observability monitors behavioral patterns. Both use intent as the reference point.

**Guards (Human Oversight):** Humans handle exceptions - actions the agent attempts that fall outside intent, anomalies the monitoring layer detects, edge cases the Judge flags. Humans also update the intent specification based on operational learning.

**Lockdown Protocol (PACE):** When the confinement model detects a serious violation - or when external conditions prevent the agent from fulfilling its intent safely - structured degradation kicks in. Each phase is defined relative to the intent: what is the minimum viable version of this agent's purpose?

**Architectural Plans (Intent Specification):** The declared intent itself. The document that defines what this agent is supposed to do, what data it needs, what tools it uses, what outputs it produces, and what boundaries it must respect. Every other layer references this.

## Why This Works (Most of the Time)

The confinement model works because it operates as a **closed-loop control system with a shared reference point**. The declared intent is the setpoint. The Judge and observability are the sensors. Drift detection is the comparator. Human oversight and PACE are the actuators. The system continuously measures actual behavior against the desired state and applies corrective action - unlike open-loop evaluate-then-permit approaches that assess once and hope.

Each layer is independent - guardrails do not depend on the Judge, the Judge does not depend on human reviewers, monitoring operates regardless of whether PACE is active. But all layers share the same reference: the declared intent. And each layer is specifically designed to catch what the previous layer misses - compound defence by design, not by coincidence.

This means:

- **A guardrail bypass does not defeat the system.** The agent gets past the wall, but the Judge sees the semantic misalignment. The monitoring layer detects the anomalous behavior. The human reviewer investigates.
- **A Judge error does not defeat the system.** The Judge misses a violation, but the guardrails already prevented the most dangerous actions. Monitoring flags the anomaly. The next human review sample catches the pattern.
- **A compromised agent does not defeat the system.** The agent's credentials limit blast radius. The monitoring layer detects the deviation from intent-aligned behavior. PACE triggers degradation. The kill switch is available as a last resort.

No single layer is sufficient. No single layer needs to be. The combination, organised around a shared understanding of what the agent is supposed to do, creates a defence that is stronger than any individual control.

## Why This Does Not Work All of the Time

Intellectual honesty matters more than confidence.

**Intent is hard to specify completely.** For simple, well-defined tasks (process a payment, calculate shipping), intent can be precisely articulated. For complex, open-ended tasks (advise on investment strategy, resolve a customer complaint), the intent specification will always be incomplete. The agent will encounter situations the specification did not anticipate, and its behavior in those situations is not governed by intent - it is governed by the model's training, the prompt, and luck.

**Agents can operate within intent and still cause harm.** A sales advisor operating entirely within its declared intent - "guide customers toward suitable products" - can still be more persuasive than the deployer intended. The intent said *what* to do, not *how aggressively* to do it. Specifying behavioral style as well as functional purpose adds complexity that many organisations will not invest in upfront.

**The gap between declared intent and infrastructure enforcement is non-trivial.** Translating "this agent should only access customer service data" into the correct IAM policies, network rules, API scopes, and guardrail configurations requires engineering effort. Misconfigurations create gaps between what the intent says and what the infrastructure enforces. The intent is correct; the implementation is not.

**Adaptive adversaries target the intent itself.** If an attacker can modify the intent specification - through prompt injection into the orchestration layer, through manipulation of the configuration store, through social engineering of the human who defines the intent - the entire confinement model defends the wrong thing. [Goal integrity controls](../maso/controls/prompt-goal-and-epistemic-integrity.md) (PG-1.3, PG-2.2, PG-3.2) exist precisely to protect the intent specification from tampering.

**Emergent behavior is intent-unaware.** When multiple agents interact, emergent behaviors can arise that no individual agent's intent specification anticipated. Each agent is operating within its intent. The system-level outcome is not what anyone intended. This is the [epistemic cascade problem](../maso/threat-intelligence/emerging-threats.md) and it is not fully solved by intent-based containment alone.

## The Defence Equation

The framework's thesis, stated plainly:

**Declared intent + hard guardrails + semantic evaluation + behavioral monitoring + human oversight + structured degradation = confined, monitorable, defensible AI behavior.**

Each term is necessary. None is sufficient alone.

- Without **intent**, the other layers have no reference point.
- Without **guardrails**, intent is just a suggestion.
- Without the **Judge**, semantic violations go undetected.
- Without **monitoring**, slow drift escapes notice.
- Without **humans**, the system has no accountability backstop and no mechanism for learning.
- Without **PACE**, failures cascade without containment.

This is not a guarantee of safety. It is a guarantee of *defensibility* - the ability to explain what controls were in place, what they were designed to catch, what reference point they were working from, and what happened when they were tested.

That is what regulators ask for. That is what auditors examine. That is what incident post-mortems need. And it starts with declaring, clearly and specifically, what the agent was supposed to do.

## Relationship to Other Framework Pages

| Page | Connection |
|------|-----------|
| [The Intent Layer](the-intent-layer.md) | Detailed architecture for post-execution semantic evaluation against declared intent (Declare, Execute, Evaluate pattern) |
| [Infrastructure Beats Instructions](infrastructure-beats-instructions.md) | Why intent must be enforced through infrastructure, not prompts |
| [Humans Remain Accountable](humans-remain-accountable.md) | Why the human accountability layer is irreducible, even with intent-based containment |
| [Why Guardrails Aren't Enough](why-guardrails-arent-enough.md) | Why guardrails alone (even intent-derived ones) miss semantic violations |
| [PACE Resilience](../PACE-RESILIENCE.md) | How structured degradation maintains intent alignment during failure |
| [PG Controls](../maso/controls/prompt-goal-and-epistemic-integrity.md) | The specific MASO controls that protect intent specifications (PG-1.3, PG-2.2, PG-3.2) |
| [Execution Control](../maso/controls/execution-control.md) | Infrastructure enforcement of intent-derived boundaries |
| [Observability](../maso/controls/observability.md) | Monitoring agent behavior against intent-derived baselines |
| [Why Containment Beats Evaluation](why-containment-beats-evaluation.md) | The position paper: why constrain-regardless architectures are structurally superior to evaluate-then-permit for regulated environments |

