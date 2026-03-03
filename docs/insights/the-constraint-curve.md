---
description: When constraining LLM actions crosses the line from useful security into counterproductive overhead. A framework for finding the point of diminishing returns.
og_title: The Constraint Curve - AI Runtime Behaviour Security
og_description: Analysis of when LLM constraints become counterproductive, with a proportionality framework for matching controls to actual risk.
---

# The Constraint Curve: When LLM Constraints Become Counterproductive

*LLMs are valuable because they make contextual, non-deterministic choices across ambiguous inputs. Constrain that property completely and you have built an expensive rules engine. Leave it unconstrained and you have built an attack surface. The question is where the line falls.*

---

## The Shape of the Problem

Every constraint applied to an LLM reduces both risk and capability simultaneously. The relationship is not linear. Early constraints deliver outsized security gains at minimal capability cost. Late constraints deliver marginal safety improvements while destroying the versatility that justified using an LLM in the first place.

![The Constraint Curve](../images/insight-constraint-curve.svg)

The graph shows three curves that tell the story:

- **LLM capability utilised** drops as constraints increase. Each additional rule, filter, or approval gate narrows the space of useful outputs the model can produce.
- **Control cost** rises exponentially. Basic guardrails are cheap. Adding judge evaluation, human review queues, escalation workflows, and audit trails compounds operational overhead.
- **Net value** peaks in the proportionate zone and then falls. Past the peak, every additional constraint costs more than the risk it mitigates.

The peak is not fixed. It shifts depending on the use case, the data involved, the decision authority, and the blast radius of failure. That is why [risk tier classification](../core/risk-tiers.md) exists - not as bureaucracy, but as a mechanism for finding the peak for each deployment.

---

## Three Thresholds Where Constraints Cross the Line

### 1. When controls cost more than the risk they mitigate

The [business alignment](../strategy/business-alignment.md) analysis quantifies this. A CRITICAL-tier system processing 50,000 interactions per day requires approximately 55 FTE for human review alone. A MEDIUM-tier system handling the same volume needs 6 FTE. That is a 9x staffing difference for one control layer.

When the operational cost of constraints exceeds the value the LLM delivers, the constraint apparatus has become the problem. The system is no longer an AI deployment with security controls. It is a human review operation with an AI component.

**The test:** Can you articulate the specific risk each constraint mitigates? If the answer is "general safety" or "best practice," the constraint may not be earning its cost.

### 2. When determinism is imposed on a probabilistic system

LLMs produce value through contextual reasoning across ambiguous inputs. That is the capability organisations pay for. When constraints narrow the output space to the point where responses are fully predictable, the system is functionally deterministic.

A deterministic system built on probabilistic infrastructure is an engineering mismatch. Traditional rules engines, decision trees, or lookup tables achieve deterministic outputs at lower cost, lower latency, and with full auditability. If your constraints have made the LLM deterministic, the [first control](the-first-control.md) applies: AI is no longer the right tool.

| System Behaviour | Constraint Level | Better Alternative |
| --- | --- | --- |
| Responses are fully templated | Over-constrained | Template engine |
| Outputs match a fixed decision tree | Over-constrained | Rules engine |
| Human approves 100% of outputs | Over-constrained | Human does the task directly |
| Model selects from a small fixed set | Over-constrained | Lookup table or classifier |
| Model reasons across ambiguous inputs | Proportionate | LLM with appropriate controls |

### 3. When controls shift work rather than eliminate risk

Each control layer adds operational surface area. The full control chain becomes:

```
AI > review > exception handling > remediation > audit
```

As the [first control](the-first-control.md) analysis identifies, these costs rarely appear in initial ROI estimates:

| Category | Ongoing Cost |
| --- | --- |
| **Governance** | Guardrails, evaluation pipelines, policy maintenance |
| **Observability** | Telemetry capture, drift detection, alert triage |
| **Operations** | Escalation workflows, rollback capability, review management |
| **Assurance** | Judge evaluation, human calibration, audit trail |

When the humans maintaining the control apparatus are doing more work than if they had performed the original task without the LLM, the constraints have not reduced total effort. They have redistributed it into a more complex, harder-to-manage form.

---

## The Security Risk Threshold

Constraints are not just about productivity. There is a real boundary where under-constrained LLMs become genuine security risks. The framework identifies four conditions where this threshold is crossed:

**Write access without validation.** When an LLM can modify systems, databases, or external services without parameter validation, sandboxing, or blast-radius limits, a single prompt injection can cascade into infrastructure-level damage. The [execution control](../maso/controls/execution-control.md) domain exists for this reason.

**Autonomous action chaining.** When agents chain actions across systems without transitive authority controls, the effective permission scope compounds with each hop. The [incident tracker](../maso/threat-intelligence/incident-tracker.md) documents confirmed real-world examples: the Amazon Q tool misuse exploit, the AutoGPT remote code execution, the Replit agent meltdown.

**Poisonable context.** When inputs to the LLM can be manipulated through indirect prompt injection, memory attacks, or tool-result tampering, the model's decisions are being made on compromised data. EchoLeak, the Gemini memory attack, and the GitHub MCP exploit demonstrate this is not theoretical.

**Operations beyond observability.** If the system cannot record what the LLM did, why it did it, and what data it accessed, the risk is unbounded. You cannot detect anomalies in behaviour you cannot see. The [visibility problem](the-visibility-problem.md) explores this gap.

These are not problems solved by adding more constraints. They are problems solved by structural controls: sandboxing, identity, logging, and blast-radius containment. The distinction matters. Piling guardrail rules onto a system with no execution isolation is security theatre. Building proper infrastructure and then applying proportionate behavioural controls is security engineering.

---

## The Human Factor Inversion

Over-constraining produces a specific failure mode that is worse than having fewer controls: human reviewers become rubber-stamp operators.

When a human-in-the-loop reviewer approves 95% or more of outputs without independent analysis, the control has inverted. It provides the *appearance* of oversight while delivering the *reality* of automated pass-through with added latency. The [use case definition](../strategy/use-case-definition.md) guidance flags this directly:

> *"If the human reviewer accepts the AI recommendation 95% of the time without independent analysis, the system is influential regardless of what the process document says."*

The [human factors](../strategy/human-factors.md) analysis documents how this happens:

| PACE Phase | Technical Equivalent | Human Equivalent |
| --- | --- | --- |
| **Primary** | All controls active | All roles staffed, trained, engaged |
| **Alternate** | One layer degraded | Key person leaves; coverage maintained |
| **Contingency** | Multiple layers degraded | Team understaffed; reviews backlogged; guardrails stale |
| **Emergency** | Full stop | Nobody qualified to operate the system; knowledge lost |

Alert fatigue, deskilling, and reviewer burnout are not edge cases. They are the predictable consequence of controls that demand human attention without delivering human value. Every mandatory review that does not genuinely require human judgement degrades the quality of the reviews that do.

---

## Proportionality in Practice

The framework resolves this through the [risk tier](../core/risk-tiers.md) system and the [Fast Lane](../FAST-LANE.md) for low-risk deployments. The principle is simple: match controls to actual risk, not to technology or to fear.

| Factor | Under-constrained | Proportionate | Over-constrained |
| --- | --- | --- | --- |
| **Autonomy** | LLM acts without oversight on high-impact decisions | Controls match decision authority | Human approves every output regardless of impact |
| **Scope** | No input/output filtering | Guardrails on known-bad patterns | Guardrails so aggressive they block legitimate use |
| **Evaluation** | No monitoring of outputs | Judge samples or evaluates proportionate to risk | 100% judge evaluation on trivial interactions |
| **Human oversight** | None where needed | Targeted review of edge cases and escalations | Reviewer rubber-stamps 95%+ without analysis |
| **Blast radius** | Unrestricted system access | Sandboxed with scoped permissions | So restricted the LLM cannot perform its function |

The Fast Lane concept is the most direct expression of this principle. Systems that meet four criteria - internal users only, read-only operations, no regulated data, and human always in the loop - qualify for minimal controls: basic guardrails, logging, a feature flag, and fallback documentation. That is four controls, not eighty. The remaining controls exist for systems that need them.

---

## When the Framework Itself Becomes a Constraint

The [framework tensions](../strategy/framework-tensions.md) document acknowledges this risk explicitly. Constraints on paper that do not translate into constraints in practice are not neutral. They consume governance attention, create compliance overhead, and breed resentment in delivery teams.

The [security as enablement](security-as-enablement.md) analysis draws the line clearly:

> *"Give teams tools that solve real problems and they will use them. Give them a list of issues and you will be negotiated."*

A security framework that makes the controlled path harder than the uncontrolled path will be bypassed. Not because teams are reckless, but because delivery pressure is real and frameworks that add friction without visible value do not survive contact with production schedules.

The secure path must be the easiest path. Controls embedded in platform infrastructure - default guardrails, automatic logging, built-in circuit breakers - are adopted because they cost nothing to use. Controls that require manual processes, separate approval workflows, or additional headcount are adopted only when the risk visibly justifies the cost.

---

## Key Takeaways

1. **Constraints have diminishing returns.** Early controls deliver large security gains cheaply. Late controls deliver marginal gains expensively. Find the peak, not the maximum.

2. **Proportionality is the operating principle.** The risk tier determines the constraint level. LOW-tier systems need four controls. CRITICAL-tier systems need the full architecture. Applying CRITICAL controls to LOW-risk systems kills projects without improving security.

3. **Over-constraining is not safer.** It produces rubber-stamp reviews, alert fatigue, governance theatre, and teams that bypass controls entirely. These outcomes are less safe than proportionate controls that people actually follow.

4. **The test is cost versus risk.** If you cannot name the specific risk a constraint mitigates, or if the constraint costs more than the risk it prevents, remove it.

5. **Structural controls beat behavioural rules.** Sandboxing, identity, logging, and blast-radius containment are the foundation. Behavioural guardrails are the refinement. Do not stack behavioural rules on a system with no structural foundation.

6. **If the LLM is fully deterministic, it should not be an LLM.** The value of the technology is contextual reasoning. If constraints have eliminated that, use a cheaper, more auditable tool.

---

## Related

- [The First Control: Choosing the Right Tool](the-first-control.md) - when AI is not the answer
- [Security as Enablement, Not Commentary](security-as-enablement.md) - controls that help versus controls that hinder
- [Framework Tensions](../strategy/framework-tensions.md) - where the framework constrains strategy
- [Business Alignment](../strategy/business-alignment.md) - the cost reality of control tiers
- [Human Factors](../strategy/human-factors.md) - sustainability of human-dependent controls
- [Fast Lane](../FAST-LANE.md) - minimal controls for low-risk systems
- [Risk Tiers](../core/risk-tiers.md) - classifying systems by use case, not technology

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
