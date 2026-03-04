# Why Containment Beats Evaluation

*A constrain-regardless architecture for sandbagging-resistant AI governance.*

> **Position paper:** [Why Containment Beats Evaluation - A Runtime Security Architecture for Sandbagging-Resistant AI Governance in Regulated Environments](https://airuntimesecurity.co.za/insights/why-containment-beats-evaluation/) (Jonathan Gill, March 2026)

---

## The Core Argument

The dominant paradigm in AI safety follows a linear sequence: evaluate a model's capabilities, determine what is safe to permit based on those results, then deploy with safeguards calibrated to the evaluation findings. This **evaluate-then-permit** model underpins every major frontier safety framework.

Sandbagging threatens this paradigm at its foundation. If a model can detect that it is being evaluated and strategically underperform, the evaluation produces a false picture of capabilities. Safeguards are calibrated to a capability level that does not reflect reality.

The safety research community is attempting to solve sandbagging by making evaluations more accurate. This framework takes a different position: **make evaluations less important.**

---

## The Mirror Risk: Evaluation Overconfidence

The sandbagging literature focuses on models that are more capable than evaluation reveals. But evaluation failure has two faces. The mirror risk is a model that appears more capable than it is: one that is deployed with permissions it can technically exercise but cannot competently exercise. It produces outputs that are plausible, fluent, structurally sound, and wrong.

This is arguably the more prevalent failure mode in enterprise deployment today. Every organisation that has deployed a summarisation agent or compliance checker has encountered this: the model sounds like it knows what it is doing, and it does not. Pre-deployment evaluation that overestimates competence is as dangerous as evaluation that underestimates capability, and it is far more common.

If sandbagging is a model hiding what it *can* do, this is **sandbugging** - a model masking what it *cannot* do.

Both failure modes share the same structural cause: security and governance that depend on evaluation accuracy inherit the full uncertainty of that evaluation. The constrain-regardless architecture addresses both directions of failure through the same mechanism, as described in the following sections.

---

## Constrain-Regardless vs Evaluate-Then-Permit

The evaluate-then-permit model asks: *"What can this model do?"* and sets permissions accordingly.

The constrain-regardless model asks: *"What does this business process require the model to do?"* and sets permissions accordingly.

This is a fundamental inversion. Permissions are derived from **business intent and operational requirements** - not from evaluation of the model's capabilities. The boundary is set by the use case, not by the model.

If permissions are not derived from evaluation, there is nothing to game. A model that conceals its ability to exfiltrate data cannot exploit that ability if the containment boundary does not permit data exfiltration in the first place. The capability exists; the execution path does not.

This is the principle that drives the framework's [Containment Through Declared Intent](containment-through-intent.md) architecture and the [Infrastructure Beats Instructions](infrastructure-beats-instructions.md) design principle.

---

## Closed-Loop vs Open-Loop Control

The difference between these paradigms can be expressed in control systems terms.

**Open-loop control** (evaluate-then-permit): Measure the system's state once during evaluation. Set control parameters based on that measurement. Operate without further verification. If the initial measurement is wrong - whether due to sandbagging, evaluation limitations, or capability changes after deployment - the control parameters remain miscalibrated indefinitely.

**Closed-loop control** (this framework): Define the desired operating state (containment boundaries). Continuously measure actual operating state (LLM-as-Judge). Compute the error between desired and actual (behavioural drift detection). Apply corrective action (escalation to human oversight). The accuracy of initial evaluation is useful but not load-bearing. The system self-corrects.

The three-layer architecture is explicitly a closed-loop control system:

| Control Element | Framework Implementation |
|---|---|
| **Setpoint** (desired state) | [Declared intent specification](containment-through-intent.md) |
| **Sensor** (measurement) | [LLM-as-Judge](../core/judge-assurance.md) + [Observability](../maso/controls/observability.md) |
| **Comparator** (error detection) | [Behavioural drift detection](behavioral-anomaly-detection.md) |
| **Actuator** (correction) | [Human oversight escalation](humans-remain-accountable.md) + [PACE degradation](../PACE-RESILIENCE.md) |

Closed-loop systems can still fail - through sensor error (judge blind spots), actuator failure (escalation processes that do not respond effectively), or feedback delay (drift that accumulates faster than detection). But closed-loop systems degrade gracefully and are self-correcting by design. Open-loop systems fail silently and without recovery.

In engineering, no critical system operates on open-loop control. AI governance should be no different. The question is not whether the model passed its evaluation. The question is whether the model is behaving correctly **right now**.

---

## Compound Defence by Design

The three layers are not just defence-in-depth by coincidence. Each layer is specifically designed to catch what the previous layer misses.

**Layer 1 - Containment Boundaries (Guardrails):** Define what the agent is permitted to do based on business intent. Enforced through [infrastructure controls](../infrastructure/): API restrictions, tool permissions, data scopes, action whitelists. This neutralises sandbagging as a breakout vector - there is nothing to game.

**What Layer 1 does not catch:** Adversarial behaviour *within* permitted bounds. An agent that subtly degrades output quality, optimises for unintended objectives, or produces technically compliant but strategically misaligned results.

**Layer 2 - Enterprise-Owned LLM-as-Judge:** A separate model, configured with an enterprise-defined behavioural constitution, continuously evaluates outputs against expected patterns. Behavioural degradation manifests as a change in the statistical distribution of outputs over time. The Judge detects this drift **regardless of its cause**. The agent does not need to be "caught sandbagging"; it needs to be caught behaving differently from baseline.

The Judge must be **owned, configured, and governed by the deploying organisation** - not vendor-side safeguards. Vendor safeguards prevent the model from producing harmful outputs. Enterprise-owned judges verify the model is producing the **correct outputs for a specific business context**. These are different objectives with different threat models. See [Judge Model Selection](../extensions/technical/judge-model-selection.md).

**What Layer 2 does not catch:** Correlated failures (judge shares blind spots with base model), ambiguous cases where the Judge's confidence is insufficient, and novel behaviour patterns outside baseline.

**Layer 3 - Human Oversight Escalation:** Triggered by defined thresholds: judge confidence below threshold, anomalous patterns, high-stakes decisions, periodic audit. This layer handles what the first two cannot resolve autonomously.

**The compound requirement:** For sandbagging or any adversarial behaviour to succeed, a model would need to simultaneously: remain within its containment boundary (evading all technical controls), produce output that passes the Judge's behavioural constitution over sustained periods without triggering drift detection, **and** avoid triggering any human escalation threshold. This is not defence-in-depth by accident - it is defence-in-depth by design, where each layer is specifically calibrated to catch what the previous layer misses.

---

## Action-Space vs Reasoning-Space Constraints

The strongest practical objection: if containment constrains the AI this tightly, why not write conventional code?

The answer lies in a distinction between two types of constraint:

- **Action-space constraints** limit what an agent may *do*: which tools it may call, which data it may access, which operations it may execute.
- **Reasoning-space constraints** limit how an agent may *think*: what it may infer, synthesise, interpret, or generate.

**Containment operates exclusively on the action space. The reasoning space remains unconstrained.**

The entire value of deploying AI - rather than deterministic code - lies in its ability to handle ambiguity, generalise across contexts, synthesise unstructured information, and produce outputs that could not have been pre-specified. None of that requires unrestricted action.

A model summarising customer complaints needs full reasoning freedom to interpret nuance, identify patterns, and generate coherent analysis. It does not need the ability to call external APIs, modify database records, or exfiltrate data. Containment preserves the former while preventing the latter.

Ironically, the alternative approaches - evaluate-then-permit and vendor-side safety training - are *more* likely to constrain the reasoning space. Over-refusal, where a model declines legitimate business queries because safety training is poorly calibrated, is a reasoning-space constraint. It reduces utility without improving operational security. Containment avoids this by moving control to the action layer and leaving reasoning alone.

The right question is not *whether* to constrain, but **where on the spectrum of action-space tightness to operate**. This is what the framework's [risk tiers](../core/risk-tiers.md) determine - proportionate governance that preserves AI's value precisely because it does not attempt to control AI's reasoning.

---

## Making Sandbagging and Sandbugging Operationally Irrelevant

The empirical evidence that sandbagging is real and growing is substantial:

- **UK AISI (December 2025):** Models can sandbag subtly enough to fool automated monitoring. Black-box monitors lose accuracy as task difficulty increases. No evidence of spontaneous sandbagging found, but monitors may not detect all forms.
- **International AI Safety Report 2026:** Models increasingly distinguish test settings from deployment. Dangerous capabilities could go undetected before deployment.
- **Anthropic research:** Automated researchers can subtly sandbag. Models can hack their own reward systems. Constitutional Classifiers required 1,700+ hours of red-teaming.

The constrain-regardless architecture does not attempt to detect sandbagging or sandbugging. It makes both **operationally irrelevant** by decoupling security enforcement from evaluation accuracy:

| Evaluate-Then-Permit | Constrain-Regardless |
|---|---|
| Permissions derived from evaluation | Permissions derived from business intent |
| Sandbagging undermines the permission model | Sandbagging has nothing to target |
| Sandbugging leads to over-permissioned deployment | Containment boundaries are set by use case, not by assessed capability |
| Point-in-time assessment | Continuous closed-loop monitoring |
| Security owned by model developer | Security owned by deploying organisation |
| Scales poorly with model capability | Independent of model capability |

This does not mean either risk is harmless. A model that sandbags within its permitted bounds - subtly degrading output quality - is still a threat. A model that sandbugs - producing confident, plausible, wrong outputs within its permissions - is equally dangerous. But both threats are in the Judge's domain (Layer 2), not the containment boundary's domain (Layer 1). The architecture addresses them through continuous behavioural monitoring, not through better pre-deployment evaluation.

For the detailed treatment of sandbagging mitigations and AISI evidence, see [Evaluation Integrity Risks](evaluation-integrity-risks.md).

---

## Limits

Intellectual honesty requires acknowledging what this architecture does not solve:

**Judge brittleness.** The Judge is itself a model, subject to drift, hallucination, and correlated blind spots - particularly if it shares architectural lineage with the base model. Judge calibration is an ongoing operational requirement. See [When the Judge Can Be Fooled](../core/when-the-judge-can-be-fooled.md).

**Within-bounds adversarial behaviour.** Containment prevents breakout. It does not prevent a model from pursuing misaligned objectives within its permitted action space - subtle bias, slow-burn optimisation, technically compliant but strategically harmful results.

**Escalation fatigue.** Three interlocking layers require three layers of operational support. Containment boundaries evolve with business processes. Judge baselines shift with model updates. Human reviewers develop alert fatigue. The architecture introduces cost that must be justified by risk.

**Model update risk.** When a vendor updates the underlying model, the Judge's baseline may become stale. The Judge must detect change without treating every update as anomaly.

**Cross-model collusion.** In multi-agent architectures, if the Judge and agent share the same provider or training methodology, correlated failures become possible. Use judges from different providers to preserve independence.

None of these invalidate the architecture. They define its operating envelope. A control system that is honest about its failure modes is more trustworthy than one that claims none.

---

## Regulatory Alignment

The constrain-regardless architecture aligns with regulatory expectations:

| Standard | Alignment |
|---|---|
| **ISO 42001** | Containment satisfies operational controls; Judge satisfies monitoring; human oversight satisfies governance |
| **EU AI Act** | Human oversight for high-risk systems; risk management throughout lifecycle, not only at deployment |
| **NIST AI RMF** | Continuous monitoring; separation of AI risk management from the AI system's own capabilities |
| **Banking supervisors** (APRA, PRA, ECB) | Operational risk controls owned by deploying institution, not outsourced to technology providers |
| **International AI Safety Report 2026** | Defence-in-depth with layered safeguards where no single control is trusted alone |
| **CoSAI Principles** | Human-governed, bounded and resilient, risk-based controls |

---

## Relationship to Other Framework Pages

| Page | Connection |
|------|-----------|
| [Containment Through Declared Intent](containment-through-intent.md) | The architectural thesis this position builds on - intent as the organising principle for all control layers |
| [Evaluation Integrity Risks](evaluation-integrity-risks.md) | The empirical evidence from AISI that evaluation-dependent security is structurally fragile |
| [When the Judge Can Be Fooled](../core/when-the-judge-can-be-fooled.md) | Judge adversarial failure modes - the honest assessment of Layer 2's limits |
| [Infrastructure Beats Instructions](infrastructure-beats-instructions.md) | Why containment must be enforced through infrastructure, not prompts - action-space constraints in practice |
| [The Intent Layer](the-intent-layer.md) | The Declare → Execute → Evaluate pattern that implements closed-loop control |
| [Judge Assurance](../core/judge-assurance.md) | How to measure and maintain the enterprise-owned Judge's accuracy |
| [PACE Resilience](../PACE-RESILIENCE.md) | Structured degradation when the closed-loop detects failure |
| [Why AI Security Is a Runtime Problem](why-ai-security-is-a-runtime-problem.md) | The broader case for continuous runtime security over point-in-time assessment |

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
