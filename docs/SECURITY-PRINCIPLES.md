---
description: Established security and military principles mapped to the AI runtime security framework - defense in depth, assume breach, zero trust, OODA loop, and more.
---

# Security Principles

**Established principles. Applied to AI runtime security.**

*Security practitioners already know these principles - or should. This page maps them to the framework so you can build a mental model of why each architectural decision exists and what established thinking supports it.*

> The framework wasn't designed in a vacuum. Every layer, every control domain, every resilience mechanism traces back to principles that have been tested in military operations, cryptographic systems, and enterprise security for decades. If you understand the principles, you understand the framework.

## How to Read This Page

Principles are grouped into four categories:

1. **Foundational** - These are WHY the framework exists
2. **Architectural** - These explain HOW the framework is designed
3. **Operational** - These guide HOW you operate the framework
4. **Practitioner Maxims** - These shape your MINDSET

Each principle includes its origin, a plain description, and a direct mapping to where it appears in the framework. If you're already familiar with a principle, skip to the mapping.

---

## Foundational Principles

*These six principles are the philosophical bedrock. If you understand only these, you understand the framework's reason for being.*

### Assume Breach

**Origin:** DoD Zero Trust strategy (~2014), evolved from post-Snowden security thinking. Formalized in the [DoD Zero Trust Reference Architecture](https://dodcio.defense.gov/Portals/0/Documents/Library/(U)ZT_RA_v2.0(U)_Sep22.pdf).

**The principle:** Operate under the assumption that your perimeter has already been compromised. Design for detection, containment, and recovery - not just prevention.

**In this framework:** This is the entire thesis. The framework opens with the assertion that *you cannot fully test AI before deployment* - the input space is infinite, behavior is non-deterministic, and emergent failures can't be predicted. Assume the model WILL produce harmful output. Assume guardrails WILL be bypassed. Assume prompt injection WILL succeed. Then build controls that detect, contain, and recover when it happens.

The [Judge layer](ARCHITECTURE.md) exists because guardrails will be bypassed. The [Circuit Breaker](ARCHITECTURE.md) exists because the Judge will fail. [PACE](PACE-RESILIENCE.md) defines what happens when each layer degrades - because they will. The entire shift from design-time assurance to runtime behavioral monitoring is Assume Breach applied to AI.

---

### Defense in Depth

**Origin:** Military strategy - Roman fortifications, medieval castle design (moat, walls, keep, citadel), the Battle of Kursk. Adopted into cybersecurity by the NSA. Formalized in [NIST SP 800-14](https://csrc.nist.gov/pubs/sp/800/14/final).

**The principle:** Layer multiple independent defensive mechanisms so that an attacker must breach ALL of them to succeed. No single point of failure.

**In this framework:** The [three-layer architecture](ARCHITECTURE.md) (Guardrails → LLM-as-Judge → Human Oversight) is a direct application. Each layer catches what the previous layer misses - by design, not by coincidence:

| Layer | What it catches | Why the previous layer can't |
|-------|----------------|------------------------------|
| **Guardrails** | Known-bad patterns (PII, injection signatures, policy violations) | N/A - first line |
| **Model-as-Judge** | Unknown-bad - semantically inappropriate outputs that pass pattern matching | Guardrails can't reason about meaning |
| **Human Oversight** | Genuinely ambiguous cases, novel situations, edge cases | Neither automated layer can handle true ambiguity |
| **Circuit Breaker** | Systemic failure of controls themselves | Previous layers can't detect their own compromise |

The compound detection math makes this quantitative: if each layer independently catches 90% of issues, the three-layer system catches 99.9%. Remove any layer and you have a gap.

In [MASO](maso/), defense in depth extends to seven control domains - each covering a different attack surface, each with its own failure mode.

---

### Trust but Verify

**Origin:** Russian proverb (*"Doveryai, no proveryai"*), popularized by Ronald Reagan during Cold War nuclear arms negotiations with the Soviet Union.

**The principle:** Allow operations to proceed, but independently validate their correctness. Trust is conditional and continuously monitored.

**In this framework:** This perfectly describes the Guardrails + Judge relationship. Guardrails let "good enough" traffic through (trust). The Judge independently evaluates whether the output is appropriate (verify). The asynchronous nature of the Judge is key - you don't block operations waiting for verification; you verify continuously and escalate when verification fails.

The [Human Oversight layer](ARCHITECTURE.md) extends verification to cases where automated verification is insufficient. [Judge Assurance](core/judge-assurance.md) verifies the verifier - measuring whether the Judge itself is performing accurately.

For multi-agent systems, [MASO Domain 1](maso/controls/domain-1-identity-access.md) (Identity & Access) enforces mutual authentication - agents verify each other's identity on every interaction, not just the first.

---

### Fail-Safe Defaults

**Origin:** Saltzer & Schroeder, *"The Protection of Information in Computer Systems"* (1975) - one of the eight foundational design principles for computer security.

**The principle:** When a system fails, it should default to a secure state (deny access) rather than an open state. The default should be denial of access; the system identifies conditions under which access is *permitted*, not conditions under which it is *denied*.

**In this framework:** The [Circuit Breaker](ARCHITECTURE.md) is the ultimate fail-safe - when controls fail, halt all AI traffic and activate a non-AI fallback. [PACE Emergency](PACE-RESILIENCE.md) = full stop.

The framework is explicit: *"The absence of a control result should be treated as a failure, not a pass."* If the Judge is unreachable, the output is queued for human review - not released. If guardrails timeout, traffic is held - not passed.

The [fail posture decision](PACE-RESILIENCE.md) (fail-open vs. fail-closed) is identified as the single most important resilience choice an architect makes, with clear guidance:

- **Tier 1** (internal, no customer impact): Fail-open acceptable
- **Tier 2** (customer-facing): Fail-closed by default
- **Tier 3** (regulated, autonomous): Fail-closed always

---

### Resilience Over Prevention

**Origin:** Modern cybersecurity doctrine - [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) (Recover function), [DORA](https://www.digital-operational-resilience-act.com/) (Digital Operational Resilience Act). Also central to chaos engineering and site reliability engineering.

**The principle:** Since prevention will eventually fail, invest in the ability to detect, contain, recover from, and adapt to incidents - not just in preventing them.

**In this framework:** [PACE](PACE-RESILIENCE.md) is the operational expression of this principle. Every control layer has a defined failure mode and degradation path. The framework doesn't promise prevention - it promises structured degradation:

| State | Posture |
|-------|---------|
| **Primary** | All layers operational. Normal production. |
| **Alternate** | One layer degraded. Backup active. Scope tightened. |
| **Contingency** | Multiple layers degraded. Supervised-only mode. |
| **Emergency** | Confirmed compromise. AI stopped. Non-AI fallback active. |

Even at the lowest risk tier, there's a fallback plan. At the highest, there's a structured path from full autonomy to full stop. This is resilience by design - the system is built to absorb failure and continue functioning, not to assume failure won't happen.

---

### Proportionality

**Origin:** International humanitarian law (jus in bello); widely adopted in risk management, regulatory compliance (EU AI Act risk tiers), and operational security.

**The principle:** Responses should be proportionate to the threat. Excessive controls waste resources and create pressure to bypass them. Insufficient controls leave gaps. Match the control to the risk.

**In this framework:** The [four-tier risk model](core/risk-tiers.md) (LOW → MEDIUM → HIGH → CRITICAL) with proportionate controls is this principle in action:

| Tier | Profile | Controls Required |
|------|---------|-------------------|
| **LOW** | Internal, non-sensitive, human-reviewed | Basic guardrails, optional Judge |
| **MEDIUM** | Internal, moderate impact | Guardrails + sampling Judge |
| **HIGH** | Customer-facing, sensitive data | All three layers, continuous Judge |
| **CRITICAL** | Autonomous decisions, regulated | Full architecture, mandatory human approval |

The [Fast Lane](FAST-LANE.md) exists because this principle demands it - a low-risk internal chatbot should not require the same control overhead as an autonomous financial trading agent. Proportionality prevents security theater and preserves security team capacity for systems that genuinely need it.

In MASO, the [three implementation tiers](maso/) (Supervised → Managed → Autonomous) apply the same logic to multi-agent systems.

---

## Architectural Principles

*These explain specific design decisions in the framework. When you ask "why is it built this way?", the answer traces to these.*

### Zero Trust

**Origin:** John Kindervag at Forrester Research (2010). Formalized in [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) and the DoD Zero Trust Reference Architecture.

**The principle:** No entity - internal or external - is inherently trusted. Every request must be authenticated, authorized, and continuously validated regardless of origin.

**In this framework:** The Judge doesn't trust the primary model's output - it independently verifies. [MASO Domain 1](maso/controls/domain-1-identity-access.md) mandates mutual authentication between agents - no agent is trusted based on origin or prior behavior. The agent that behaved correctly on the last 10,000 requests may be compromised on the next one.

This is particularly critical for the [confused deputy](maso/controls/emergent-risk-register.md) risk: an agent that trusts another agent's delegation without independent verification becomes a weapon.

---

### Least Privilege

**Origin:** Saltzer & Schroeder (1975). Echoes the military "need-to-know" principle.

**The principle:** Every entity should operate with the minimum permissions necessary for its function. No more access than needed, for no longer than needed.

**In this framework:** [MASO Domain 1](maso/controls/domain-1-identity-access.md) - per-agent unique identity, scoped credentials, short-lived tokens. [MASO Domain 6](maso/controls/domain-6-privileged-governance.md) - orchestrators get elevated but bounded authority with explicit delegation limits. [Domain 3](maso/controls/domain-3-execution-control.md) - tool access via parameter allow-lists, not open-ended capability.

An agent summarizing documents should not have write access to databases. Permissions derive from the use case, not from the model's capabilities.

---

### Separation of Duties

**Origin:** Accounting and audit practice. Formalized in the Clark-Wilson integrity model (1987) and NIST SP 800-53 (AC-5).

**The principle:** No single entity should control all aspects of a critical function. Critical operations require agreement from multiple independent parties.

**In this framework:** The AI that generates output MUST NOT be the same AI that evaluates it. The [Judge](ARCHITECTURE.md) is explicitly an independent model - different model, different provider if possible. If the primary model is compromised, the Judge must not be compromised with it.

This extends to governance: humans who configure guardrails should not be the same humans who approve exceptions. In multi-agent systems, the [orchestrator](maso/controls/domain-6-privileged-governance.md) should not also be the executor.

---

### Complete Mediation

**Origin:** Saltzer & Schroeder (1975).

**The principle:** Every access to every resource must be checked for authorization, every time. No caching of authorization. No bypass paths.

**In this framework:** Every AI output passes through guardrails - no "fast path" that skips controls for performance. Every tool invocation by an agent is validated against allow-lists. In MASO, every [inter-agent message](maso/controls/domain-3-execution-control.md) traverses the security bus.

This principle argues against "performance shortcuts" that skip security checks. If you're tempted to bypass guardrails for latency reasons, you're violating complete mediation - and you're creating the gap an attacker will find.

---

### Kerckhoffs's Principle

**Origin:** Auguste Kerckhoffs, *La Cryptographie Militaire* (1883). Restated by Claude Shannon (1949) as: *"The enemy knows the system."*

**The principle:** Security should not depend on secrecy of design. Assume adversaries know your architecture. Only specific keys or credentials should be secret.

**In this framework:** System prompts WILL leak - through prompt extraction attacks, through the AI itself, through operational disclosure. Guardrail rules WILL be reverse-engineered. The framework's controls must remain effective under full disclosure.

This is why the framework is open-source. It's also why relying on "the attacker won't know our prompt" is explicitly identified as a non-defense. [System prompt leakage](maso/controls/domain-0-prompt-goal-epistemic-integrity.md) (OWASP LLM07) is a recognized risk precisely because organizations violate this principle.

---

### Least Common Mechanism

**Origin:** Saltzer & Schroeder (1975).

**The principle:** Minimize shared mechanisms between components. Shared resources are potential information leakage and cross-contamination paths.

**In this framework:** [MASO Domain 2](maso/controls/domain-2-data-protection.md) - cross-agent data fencing. Agents should not share memory spaces, credentials, or communication channels unnecessarily. Shared context windows between agents create cross-contamination risks where one compromised agent poisons another's inputs.

The [memory poisoning](maso/controls/emergent-risk-register.md) and [RAG poisoning](insights/rag-is-your-biggest-attack-surface.md) risks are direct consequences of violating this principle.

---

### Center of Gravity

**Origin:** Carl von Clausewitz, *On War* (1832). The hub of all power and movement upon which everything depends.

**The principle:** Identify the component whose compromise collapses the entire defense. Protect it with priority. Attack your adversary's.

**In this framework:** The center of gravity in an AI system is the model's decision-making process - the prompt, context window, and instruction chain. [MASO Domain 0](maso/controls/domain-0-prompt-goal-epistemic-integrity.md) (Prompt, Goal & Epistemic Integrity) exists specifically to protect this center of gravity.

Prompt injection is a direct attack on the center of gravity. It targets the mechanism by which the model receives instructions, attempting to substitute adversary instructions for legitimate ones. Domain 0's controls - instruction provenance, goal integrity, epistemic risk detection - are all center-of-gravity protection.

---

### Contain and Isolate

**Origin:** Military cordon operations; law enforcement containment doctrine; network security segmentation.

**The principle:** When a threat is identified, contain it to prevent spread before attempting resolution. Isolate compromised components to prevent lateral movement.

**In this framework:** The [Circuit Breaker](ARCHITECTURE.md) is containment - stop all AI traffic when controls fail. [Domain 3](maso/controls/domain-3-execution-control.md) (Execution Control) provides isolation - sandboxed tool execution, blast radius caps, parameter allow-lists. [Domain 2](maso/controls/domain-2-data-protection.md) provides data isolation - cross-agent data fencing prevents lateral data movement.

The AI equivalent of network segmentation: if one agent is compromised, the blast radius is limited to what that agent can access - not the entire system.

---

## Operational Principles

*These guide how you run and maintain the framework day-to-day. They're about operational discipline, not architecture.*

### OODA Loop

**Origin:** Colonel John Boyd, U.S. Air Force (1960s). Originally developed for fighter pilot decision-making during the Korean War. Widely adopted in military strategy, business, and cybersecurity incident response.

**The principle:** Decision superiority comes from cycling through four phases faster than your adversary: **Observe** the environment, **Orient** (contextualize and interpret), **Decide** on a course of action, **Act**. The side that cycles faster wins.

**In this framework:** The three-layer architecture implements a continuous OODA loop:

| OODA Phase | Framework Element |
|------------|-------------------|
| **Observe** | Guardrail telemetry, Judge evaluations, behavioral drift detection, anomaly scoring ([Domain 4](maso/controls/domain-4-observability.md)) |
| **Orient** | Correlate alerts with threat intelligence, compare against behavioral baselines, classify by risk tier |
| **Decide** | PACE triage - escalate, auto-remediate, or dismiss. Human oversight for ambiguous cases |
| **Act** | Block, quarantine, circuit-break, adjust guardrail sensitivity, notify stakeholders |

Faster loops mean faster detection-to-response. The Judge's async evaluation is about accelerating Orient. Risk tiers pre-define Decide criteria so operators don't deliberate from scratch. PACE pre-defines Act responses so execution is immediate.

Adversaries also run OODA loops - probing guardrails (Observe), calibrating attacks (Orient), selecting injection vectors (Decide), executing (Act). Your defenses disrupt their loop: unpredictable monitoring disrupts their Observe; varied Judge criteria disrupts their Orient.

---

### Fog of War

**Origin:** Carl von Clausewitz, *On War* (1832). Also: *friction* - the accumulation of minor difficulties that makes the apparently easy so difficult.

**The principle:** In conflict, uncertainty is pervasive. Information is always incomplete, often inaccurate, and frequently contradictory. Plans that assume perfect information will fail.

**In this framework:** AI is inherently non-deterministic - the same input produces different output. LLM reasoning is opaque. Multi-agent interactions produce emergent behavior that no single log entry captures. Alert data is noisy and ambiguous.

This is WHY the framework exists as runtime monitoring rather than pre-deployment certification. You cannot eliminate fog - you can only build controls that operate effectively despite it. The [epistemic risks](maso/controls/emergent-risk-register.md) in the emergent risk register are specific manifestations of fog:

- **Hallucination amplification** - false information presented with high confidence
- **Uncertainty stripping** - qualified statements losing their qualifications through agent chains
- **Semantic drift** - meaning shifting gradually through multi-step processing
- **Partial failure masquerading as success** - the most dangerous fog of all

Clausewitz's companion concept, **friction**, also applies: API latency causes Judge timeouts, log pipelines lag behind events, alert fatigue degrades human reviewers, guardrail updates break legitimate workflows. Security architectures that assume frictionless execution will fail.

---

### Maneuver and Flexibility

**Origin:** Principles of war (U.S. Army FM 3-0). Also: Boyd's emphasis on agility and adaptation.

**The principle:** Place the adversary at a disadvantage through the flexible application of capability. Maintain multiple options. Adapt to changing conditions.

**In this framework:** [PACE](PACE-RESILIENCE.md) IS pre-planned maneuver. It's not a single rigid security posture - it's a set of pre-defined adaptation options:

- Primary fails → maneuver to Alternate
- Alternate degrades → maneuver to Contingency
- Contingency overwhelmed → maneuver to Emergency

The two-axis PACE model (horizontal across layers, vertical within each layer) gives operators multiple maneuver options at every point. Adaptive guardrail sensitivity - tightening thresholds when threat indicators rise - is tactical maneuver within a layer.

Static, predictable defenses are easier to bypass than adaptive ones. Varying Judge evaluation criteria, rotating monitoring patterns, and adjusting escalation thresholds create uncertainty for adversaries attempting to calibrate their attacks.

---

### Unity of Command

**Origin:** Napoleonic military doctrine. One of the nine U.S. Army principles of war.

**The principle:** Every operation should have a single commander with clear authority and accountability. Divided command creates gaps, confusion, and diffused responsibility.

**In this framework:** [MASO Domain 6](maso/controls/domain-6-privileged-governance.md) (Privileged Agent Governance) - the orchestrator is the "commander" in a multi-agent system. Clear authority hierarchies, explicit delegation limits, single accountability chains.

The [accountability blur](maso/controls/emergent-risk-register.md) emergent risk is what happens when this principle is violated - when multiple teams (ML engineering, security, compliance, product) share responsibility with no single accountable owner, gaps emerge. When multiple agents share authority with no clear orchestrator, actions fall between the cracks.

---

### Economy of Force

**Origin:** Principles of war. Complementary to Mass (Concentration).

**The principle:** Allocate minimum essential resources to secondary efforts so you can concentrate maximum capability at the decisive point. Accept calculated risk in lower-priority areas.

**In this framework:** The [Fast Lane](FAST-LANE.md) for low-risk deployments. Sampling strategies for Judge evaluation of low-risk outputs. Spot-check human review instead of full review for Tier 1 systems.

Human review capacity is finite. Judge compute is finite. Security team attention is finite. Economy of force says: don't apply CRITICAL-tier controls to a LOW-risk internal chatbot. Save your capacity for the systems where failure has real consequences. The [risk tier system](core/risk-tiers.md) is a resource allocation framework as much as it is a risk classification.

---

### Perseverance

**Origin:** Added to U.S. Joint principles of operations (2011).

**The principle:** Ensure the sustained commitment necessary to attain the objective. Security is not a project with an end date - it's a continuous operation.

**In this framework:** AI security is not a one-time deployment. Behavioral baselines drift as models are updated. New attack techniques emerge from the research community. Threat actors adapt to your defenses. Regulatory requirements evolve.

Continuous monitoring, regular [red-teaming](maso/red-team/red-team-playbook.md), ongoing control refinement, and periodic reassessment of risk tiers are required indefinitely. The [threat intelligence](maso/threat-intelligence/) section tracks emerging threats precisely because the threat landscape doesn't stand still. The framework's [maturity model](MATURITY.md) assumes continuous progression, not a finish line.

---

## Practitioner Maxims

*These aren't architectural principles - they're hard-won observations about how security fails in practice. They shape the mindset you need to operate the framework effectively.*

---

> **Beware Silent Failures** - *"The most dangerous AI failures look like normal responses."*
>
> The AI system looks like it is running fine. Outputs flow. Dashboards are green. No alerts fire. But the system is not actually functioning correctly. A grounding source has gone stale and the model is answering from outdated data. A guardrail rule was updated and now silently passes traffic it should block. The Judge is evaluating against the wrong policy version. An agent loop is completing successfully but producing meaningless results because an upstream dependency changed.
>
> These are not crashes or outages. They are the operational equivalent of carbon monoxide - everything appears normal until the damage is done. Silent failures evade traditional monitoring because they produce no error signals. Latency is fine. Throughput is fine. Status codes are fine. The system is confidently wrong.
>
> Detecting silent failures requires behavioral baselines that track output quality over time ([Domain 4](maso/controls/domain-4-observability.md)), semantic evaluation that goes beyond surface-level health checks ([Judge layer](ARCHITECTURE.md)), and structured human review that samples outputs for correctness, not just availability.
>
> If your monitoring only tells you the system is up, it is not telling you enough.

---

> **Schneier's Law** - *"Anyone can invent a security system so clever that they themselves cannot think of how to break it."*
>
> - Bruce Schneier (1998)
>
> Your team's inability to bypass their own guardrails proves nothing about actual security. Internal red-teaming is necessary but insufficient. External adversarial testing and community review are essential. The [Red Team Playbook](maso/red-team/red-team-playbook.md) exists for this reason - and it's a starting point, not a complete list.

---

> **The Infinity Maxim** - *"There are an unlimited number of security vulnerabilities for a given system, most of which will never be discovered by either defenders or attackers."*
>
> - Roger G. Johnston, Argonne National Laboratory
>
> The behavioral space of an LLM is effectively infinite. No amount of pre-deployment testing enumerates all failure modes. This is the fundamental argument for runtime monitoring: you cannot find them all in advance, so you must detect them when they occur.

---

> **The Arrogance Maxim** - *"The ease of defeating a security system is proportional to the confidence of its designer."*
>
> - Roger G. Johnston, Argonne National Laboratory
>
> Claims that an AI system is "aligned," "safe," or "jailbreak-proof" should be treated as red flags. Overconfidence in guardrail effectiveness leads to underinvestment in monitoring and incident response. The framework's layered approach exists precisely because no single control deserves that level of confidence.

---

> **The Low-Tech Maxim** - *"Low-tech attacks work, even against high-tech systems."*
>
> - Roger G. Johnston, Argonne National Laboratory
>
> Sophisticated AI systems are defeated by simple plain-language manipulation - "ignore previous instructions" bypasses complex architectures. Defenses must account for trivially simple attacks, not just advanced adversarial techniques. If your guardrails only catch sophisticated attacks, you've missed the point.

---

> **The Gossip Maxim** - *"People and organizations cannot keep secrets."*
>
> - Roger G. Johnston, Argonne National Laboratory
>
> System prompts will leak. Guardrail configurations will leak. AI systems themselves leak them through prompt extraction attacks. This reinforces [Kerckhoffs's Principle](#kerckhoffss-principle): design controls that remain effective after full disclosure.

---

> **The Double-Edged Sword Maxim** - *"Within months of availability, new technology helps attackers at least as much as it helps defenders."*
>
> - Roger G. Johnston, Argonne National Laboratory
>
> LLMs power both sides: defenders use them for monitoring, anomaly detection, and judge evaluations; attackers use them for generating adversarial prompts, automating reconnaissance, and crafting social engineering attacks. Every AI-powered defense capability has an offensive mirror.

---

> **Liddell Hart's Indirection** - *"The most effective approach is rarely the direct one."*
>
> - B.H. Liddell Hart, *Strategy* (1954)
>
> Attackers won't attack where defenses are strongest. If input guardrails are robust, attacks come through indirect paths: [poisoned RAG sources](insights/rag-is-your-biggest-attack-surface.md), compromised tool APIs, manipulated training data, or social engineering of human reviewers. Defense must cover indirect vectors, not just the front door.

---

> **"Know Your Enemy and Know Yourself"** - *"Know your enemy and know yourself; in a hundred battles, you will never be defeated."*
>
> - Sun Tzu, *The Art of War* (c. 500 BCE)
>
> Understand YOUR AI system's failure modes - hallucination patterns, injection susceptibility, behavioral drift tendencies - AND understand attacker methodologies ([MITRE ATLAS](https://atlas.mitre.org/) techniques, known jailbreak taxonomies, emerging attack research). Threat modeling requires both perspectives. The framework's [threat intelligence](maso/threat-intelligence/) section and [emergent risk register](maso/controls/emergent-risk-register.md) serve both sides of this equation.

---

> **"All Warfare Is Based on Deception"** - *"Hence, when we are able to attack, we must seem unable; when using our forces, we must appear inactive."*
>
> - Sun Tzu, *The Art of War* (c. 500 BCE)
>
> Prompt injection IS deception - data masquerading as instructions, benign content hiding adversarial payloads. But defenders can also employ deception: honeypot tool endpoints that detect unauthorized access attempts, canary tokens in data that trigger alerts if exfiltrated, and decoy agent identities that reveal attacker reconnaissance.

---

> **"Subdue the Enemy Without Fighting"** - *"The supreme art of war is to subdue the enemy without fighting."*
>
> - Sun Tzu, *The Art of War* (c. 500 BCE)
>
> The best AI security control is avoiding the risky situation entirely. [The First Control: Choosing the Right Tool](insights/the-first-control.md) - don't use AI where it's not needed. Constrain the action space. Remove dangerous tool access. Limit delegation authority. The most secure agent is the one that never had the capability to cause harm in the first place.

---

## Quick Reference: Principles to Framework

| Principle | Primary Framework Element |
|-----------|--------------------------|
| Assume Breach | Runtime-first philosophy, three-layer architecture |
| Defense in Depth | Guardrails → Judge → Human Oversight → Circuit Breaker |
| Trust but Verify | Guardrails (trust) + async Judge (verify) |
| Fail-Safe Defaults | Circuit Breaker, PACE Emergency, fail posture decisions |
| Resilience Over Prevention | PACE methodology, structured degradation |
| Proportionality | Four-tier risk model, Fast Lane |
| Zero Trust | Judge independence, mutual agent auth (Domain 1) |
| Least Privilege | Scoped credentials, tool allow-lists (Domains 1, 3, 6) |
| Separation of Duties | Independent Judge model, orchestrator/executor separation |
| Complete Mediation | No-bypass guardrails, per-request authorization |
| Kerckhoffs's Principle | Open design, no reliance on prompt secrecy |
| Least Common Mechanism | Cross-agent data fencing, isolated memory (Domain 2) |
| Center of Gravity | Domain 0 - Prompt, Goal & Epistemic Integrity |
| Contain and Isolate | Circuit Breaker, sandboxing, blast radius caps (Domain 3) |
| OODA Loop | Observe (monitoring) → Orient (classify) → Decide (PACE) → Act (respond) |
| Fog of War | Non-determinism acceptance, epistemic risk register |
| Maneuver | PACE pre-planned adaptation, adaptive thresholds |
| Unity of Command | Orchestrator governance, accountability chains (Domain 6) |
| Economy of Force | Fast Lane, sampling strategies, tiered human review |
| Perseverance | Continuous monitoring, ongoing red-teaming, threat intelligence |
| Beware Silent Failures | Judge layer, behavioral baselines (Domain 4), human oversight |

---

## Sources and Further Reading

**Foundational Computer Security:**

- Saltzer, J.H. & Schroeder, M.D. (1975). [The Protection of Information in Computer Systems](https://www.cs.virginia.edu/~evans/cs551/saltzer/). *Proceedings of the IEEE*, 63(9).
- Kerckhoffs, A. (1883). *La Cryptographie Militaire*. Journal des Sciences Militaires.

**Cybersecurity Standards:**

- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [NIST SP 800-160: Engineering Trustworthy Secure Systems](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final)
- [DoD Zero Trust Reference Architecture v2.0](https://dodcio.defense.gov/Portals/0/Documents/Library/(U)ZT_RA_v2.0(U)_Sep22.pdf)

**Security Maxims:**

- Johnston, R.G. [Vulnerability Assessment Team Security Maxims](https://spaf.cerias.purdue.edu/classes/CS526/securitymaxims.pdf). Argonne National Laboratory.
- Schneier, B. (1998). [Schneier's Law](https://www.schneier.com/blog/archives/2011/04/schneiers_law.html). Schneier on Security.

**Military Strategy:**

- Clausewitz, C. von. (1832). *On War*. Translated by Michael Howard and Peter Paret.
- Sun Tzu. (c. 500 BCE). [*The Art of War*](https://classics.mit.edu/Tzu/artwar.html).
- Boyd, J. (1976). *Destruction and Creation*. U.S. Army Command and General Staff College.
- Liddell Hart, B.H. (1954). *Strategy*. Faber & Faber.
- U.S. Army FM 3-0: *Operations*. Principles of War.

**Threat Intelligence:**

- [MITRE ATLAS (Adversarial Threat Landscape for AI Systems)](https://atlas.mitre.org/)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
