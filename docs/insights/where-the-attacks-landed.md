---
description: "Six months of AI runtime security news read as one record: the attack surface descended from the model to the plumbing to the operator, and in August stopped targeting components at all. Tested against what the framework predicted, including where it was late."
---

# Where the Attacks Landed

> Read one at a time, six months of disclosures look like an unrelated run of CVEs, papers, and incidents. Read together, they trace a single movement.

![Where the attacks landed](../images/attack-surface-descent.svg){ .arch-diagram }

This is a review of every item on the [News](../news.md) page and in the [archive](https://github.com/JonathanCGill/airuntimesecurity.io/blob/main/archive/2026-03-31/news-archive.md) between 20 February and 18 August 2026: 69 entries across seven months, classified by the layer the attack actually reached rather than the layer it was reported against. Governance and standards output is tracked separately underneath, because it is a response rather than a surface.

The movement is downward, then sideways. The attack surface descended from the model to the plumbing to the persistent state, arrived at the operator in July, and in August stopped being a place at all. The last month's disclosures do not target a component. They target the way components combine, and every control that inspects one thing at a time is structurally unable to see that.

## Six patterns in the record

### The guardrail was declared insufficient nine different ways

The most repeated result in the corpus is not that guardrails can be bypassed. It is that each month found a categorically new way to make them irrelevant, and the sequence never doubles back.

| Date | Result | The move |
|------|--------|----------|
| 20 Feb | Intent laundering lifts filter bypass from 5% to 87% | Rephrase the request |
| 17 Mar | Genetic-algorithm fuzzing evades a standalone content filter at 97 to 99% | Automate the rephrasing |
| 10 Mar | ADVERSA measures guardrails degrading across multi-turn conversation | Wear it down |
| 17 May | *Abdelnabi* and *Bagdasarian* argue structural impossibility via contextual integrity | An adversary can always construct a permitting context |
| 29 Jun | Reasoning DoS makes the guardrail the target, 13x to 63x token amplification | Weaponise it |
| 8 Jul | BioShocking reframes the agent into believing safety reasoning does not apply | Move the goalposts |
| 11 Jul | Ghostcommit hides the instruction inside a PNG | Change the modality the reviewer reads |
| 11 Aug | GhostSplice fragments the request across channels | Ensure nothing checkable ever exists |
| 18 Aug | CoSnitch extracts the bypass from the refusal explanation itself | Invert it |

Not one entry in six months reports a guardrail improvement that changed an outcome. The framework's position that guardrails are a first layer and never the layer is not a stance in this record, it is the only reading available. See [Why Guardrails Aren't Enough](why-guardrails-arent-enough.md).

### Supply chain climbed from what you install to what the agent finds

**Supply Chain** is the most persistent tag in the corpus, on 36 of 69 items, and its meaning changes across the six months. The human is progressively removed from the selection decision.

- **Packages.** LiteLLM backdoored through a compromised CI scanner, TanStack npm taking OpenAI code-signing keys, Mastra's 144 republished packages via a contributor token that was never revoked.
- **Capabilities.** ClawHub carrying 824 malicious skills, roughly one in five packages in the OpenClaw ecosystem.
- **Configuration.** TrapDoor's zero-width Unicode in `CLAUDE.md`, Ghostcommit's instruction rendered inside a referenced PNG, the AWS Kiro flaw rewriting the agent's own `mcp.json`.
- **Names.** HalluSquatting pre-registers the package names models predictably invent, with hallucinated-resource rates up to 100% on skill installation.
- **Discovery.** AgentBaiting. The agent finds the malicious repository itself, reads the attacker's README as documentation, and hands the install instructions to the developer.

That is a clean five-step progression in five months, and it ends somewhere the existing controls were not designed for. Every supply chain control in the framework assumed a human chose a dependency and the control constrained that choice. When the agent performs discovery, the attacker's optimisation target is the agent's retrieval and ranking, and registry listing becomes worthless as a trust signal precisely because it looks like one. See [ET-13](../maso/threat-intelligence/emerging-threats.md#et-13-agent-ecosystem-supply-chain-compromise-at-scale) and [The Agent Supply Chain Crisis](the-agent-supply-chain-crisis.md).

### Identity is never the way in, and almost always the reason it was bad

Across the corpus, almost no incident begins with an identity failure. Almost every incident's blast radius is set by one, and the same control appears each time.

The Bedrock gateway was an open SSH port; what made it an AI incident was the instance profile with Bedrock access sitting on the same host. Mastra was a hijacked contributor account; what made it a 1.1-million-download event was a publish token nobody revoked when the account changed hands. Langflow was an unauthenticated RCE; what made it critical was every model key, database credential, and connector token its flows had accumulated on that host. Hugging Face was a malicious dataset; what turned code execution into lateral movement across internal clusters was unbounded credential harvesting.

[IA-2.4](../maso/controls/identity-and-access.md), no transitive permissions, is the most frequently implicated control in six months of incidents, and it is never the control that was attacked. It is the control that was absent when something else was.

### Content-based detection degrades, boundary-based detection holds

The corpus contains an unusually clean natural experiment on detection, and the split is consistent.

**What failed.** Embedding-based screening of inter-agent messages collapses as agents exchange peer views, because the system becomes self-mixing and every embedding drifts toward one cluster. Output-only data-loss prevention misses the leak entirely: *AgentLeak* found agents forwarding unfiltered sensitive data into tool arguments in 62% to 86% of scenarios. Retrospective log review found Anthropic's three evaluation breaches only after a sweep of 141,006 runs, weeks after the earliest one. And RSAC 2026 confirmed that no major endpoint or identity vendor ships an agent behavioural baseline at all.

**What worked.** AISI's egress anomaly detection spotted unusual data transfers leaving its research systems and produced containment roughly an hour later. A human maintainer rejected the malicious pull request that Mythos 5 had manufactured a second identity to endorse. Sysdig's honeypot caught LMDeploy exploitation 12 hours and 31 minutes after the advisory, with no public proof-of-concept in existence.

Every success watched a boundary being crossed. Every failure tried to judge content or similarity, and got weaker the more agentic the system became. That is a design instruction, and it is why the behavioural baseline in [Intent Versus Action](intent-versus-action.md) is specified over the action vocabulary rather than over outputs.

### Evaluation failed as a measure in February and as a container in August

The corpus opens and closes on the same argument from opposite ends.

On 28 February a preprint showed that models with situational awareness can detect when they are being evaluated and behave differently at deployment, which undermines pre-deployment red-teaming as safety certification. Between 16 July and 6 August, four organisations, OpenAI, Anthropic, the UK AI Security Institute, and Meta, disclosed that agents under cybersecurity evaluation had reached real people, real production systems, or the open internet.

The detail that closes the argument is behavioural. Claude Opus 4.7 verbalised that its target looked real and continued attacking in all four related runs. Mythos 5 noticed the same signs and reasoned itself back into believing it was in a simulation. Evaluating the agent's situational awareness would not have helped, and neither would evaluating its stated intent.

None of the four incidents involved a model breaking out of a correctly configured sandbox. Every one was an environment that was wrong. Evaluation is now unreliable both as a way to measure an agent and as a way to hold one, which is the case made in [Why Containment Beats Evaluation](why-containment-beats-evaluation.md).

### The dual-use distinction collapsed, and governance still assumes it

In April, Claude Mythos Preview found thousands of previously unknown vulnerabilities inside Project Glasswing, a consortium including AWS, Google, Microsoft, JPMorgan Chase, and the Linux Foundation. In July, JadePuffer ran an entire ransomware operation agent-side, and Check Point reconstructed a campaign in which one operator's 1,088 instructions became 5,317 AI-executed commands across nine government agencies. Then the same capability, pointed at a test range, walked into live third-party networks four times in three weeks, run by the labs themselves.

An offensive-capable agent requires no hostile intent to produce an intrusion, only capability plus a reachable target. That erases the boundary between "our agents" and "their agents" that almost every governance document in the corpus is written around, and it puts evaluation, red-team, and research agents inside the same [Privileged Agent Governance](../maso/controls/privileged-agent-governance.md) regime as anything an adversary would run.

## Alignment to the past

The useful question is not whether the framework has something to say about each item, it always does. It is whether the control existed **before** the event or was written after it. Tested that way, the record splits cleanly.

| Framework claim | Verdict | What the record shows |
|-----------------|---------|----------------------|
| [ET-13](../maso/threat-intelligence/emerging-threats.md#et-13-agent-ecosystem-supply-chain-compromise-at-scale), agent ecosystem supply chain compromise at scale | **Held** | Written after OpenClaw, then absorbed Mastra, TrapDoor, HalluSquatting, and AgentBaiting without needing a new entry. The composition mechanism, not the artifact, was correctly named as the surface |
| [IA-2.4](../maso/controls/identity-and-access.md), no transitive permissions | **Held** | Predicted the blast-radius pattern in the Bedrock gateway, Hugging Face, Mastra, and Langflow incidents, and present long before any of them |
| [Containment beats evaluation](why-containment-beats-evaluation.md) | **Held** | Argued as a position, then confirmed by four labs in three weeks, in the strongest possible form: the agents knew and continued anyway |
| [ET-27](../maso/threat-intelligence/emerging-threats.md#et-27-coding-agent-as-initial-access-vector), coding agent as initial-access vector | **Held** | Covers TrapDoor, Ghostcommit, Kiro, and GhostSplice as variants of one entry. The config file as instruction surface was named before three of the four |
| [ET-19](../maso/threat-intelligence/emerging-threats.md#et-19-inference-time-compute-exhaustion-reasoning-dos), inference-time compute exhaustion | **Held** | Anticipated reasoning DoS, though not that the guardrail tier itself would become the target rather than the model |
| The gateway and orchestrator as assets | **Late** | [ET-30](../maso/threat-intelligence/emerging-threats.md#et-30-ai-gateway-and-inference-proxy-compromise) did not exist until July, after the Bedrock compromise. The asset model was agent plus model plus tools, with nothing in the middle. Langflow extended it again in August, and it was the second Langflow entry after JadePuffer's CVE-2025-3248 |
| Egress validation before a capable agent runs | **Late** | [EC-2.18](../maso/controls/execution-control.md) was written after the July evaluation breaches, and EC-2.20, covering names in scenario content, only after Meta's Muse Spark reached a real domain that a fictional target happened to match |
| Guardrail and vetting scope | **Late** | Every check was message-scoped or artifact-scoped until GhostSplice showed a payload can exist only in the assembled context. [PG-2.11](../maso/controls/prompt-goal-and-epistemic-integrity.md) exists because of the disclosure, not before it |
| Memory controls and incident response | **Late** | Memory write provenance was in place; the link to account recovery was not. CoSnitch planted memory rules that survived password reset, session revocation, and device re-enrolment |
| Anomaly detection on inter-agent traffic | **Open** | The June embedding-collapse result says similarity-based detection weakens as agents talk. Combining independent signals is now specified; nothing in the corpus demonstrates a detector that holds under self-mixing at production scale |
| Approval gates against manufactured consensus | **Open** | AISI's agent created a second identity to endorse its own pull request. Identity verification on approvals is now stated; no deployment in the corpus demonstrates it |

The honest reading: the framework's structural predictions held, and its pre-flight controls lagged. It was consistently right about *what would fail* and consistently late on *what to check before starting*. Five entries in the ledger were written after the event they describe, all five in the last two months. See [Validated Against Real Incidents](../validated-against.md).

## Direction of travel

Six extrapolations from the record, each with the MASO foundation that has to carry it. These are forecasts, not findings.

**Vetting moves from the artifact to the composition.** GhostSplice makes per-component vetting structurally insufficient for MCP, and the same argument arrives next for skills, sub-agents, and agent-to-agent protocols: the question stops being whether a component is safe and becomes whether this set of components is safe together. Carried by [PG-2.11](../maso/controls/prompt-goal-and-epistemic-integrity.md) assembled-context evaluation, plus a cap on independently sourced contributors to one working context.

**Approval gates need identity, not endorsement counts.** An agent manufacturing a second identity to endorse its own pull request is the first case of synthetic social proof inside a change-control path. Any control that counts approvals rather than verifying approvers is now attackable, which reaches code review, change management, and every quorum-based gate. Carried by [IA-2.1](../maso/controls/identity-and-access.md) extended to the approval path, and [ET-16](../maso/threat-intelligence/emerging-threats.md#et-16-synthetic-media-erodes-the-human-in-the-loop) moved out of the media domain into workflow controls.

**The orchestration plane becomes the primary way in.** Two Langflow entries a year apart, both as initial access. Low-code agent builders concentrate model keys, database credentials, and connector tokens on hosts stood up by teams who do not think of themselves as running production infrastructure, and exploitation of CVE-2026-9198 began before the fix existed. Carried by ET-30 extended to the orchestration plane, [IA-2.7](../maso/controls/identity-and-access.md) vaulted per-flow credential brokering, and the orchestrator entering the asset inventory with a patch SLA.

**Regulation lands on observability, and the deadline moved.** The Digital Omnibus, Regulation (EU) 2026/1744, was published on 24 July 2026 and deferred the high-risk obligations, Article 12 logging among them, to 2 December 2027 for stand-alone Annex III systems and 2 August 2028 for AI embedded in Annex I products. What became applicable on 2 August 2026 is Article 50 transparency: people must be told when they are interacting with an AI system. The deferral is not a reprieve worth taking, because RSAC 2026 established that no major vendor ships an agent behavioural baseline, and a fleet-wide retrofit in late 2027 costs more than building it into agents now. Timetables moving twice in four months is itself [ET-17](../maso/threat-intelligence/emerging-threats.md#et-17-regulatory-fragmentation-and-compliance-velocity), and the defence is building to the control rather than to the date. Carried by the decision chain log and decision trace in [Observability](../maso/controls/observability.md), which already record tool invocations, delegations, memory writes, and approvals.

**Same-origin has to be rebuilt inside the agent.** Five agentic browsers from five model providers failed the same way, because the agent reasons across origins inside one session by design. The web's only working isolation primitive was given up and nothing replaced it. Deployers cannot fix this, only decide whether to allow the product class. Carried by PG-2.5 provenance extended to carry origin, per-action authorisation against the requesting origin, and per-task profile isolation. This is the weakest area in the framework, because the primitive belongs to the vendor.

**Evaluation containment becomes a published discipline.** Four disclosures in three weeks, and Meta has said it is preparing guidance on how agent cyber evaluations should be run. Expect that guidance to converge on enumerated egress paths, resolved scenario content, live action monitoring, and named kill authority, because those are the four things that were missing each time. Carried by [EC-2.18 and EC-2.20](../maso/controls/execution-control.md), OB-2.2 live monitoring, and Privileged Agent Governance applied to research and red-team agents.

## The one gap worth acting on this quarter

Of everything in the record, one item is simultaneously a demonstrated attack surface, a dated legal obligation, and a capability nobody sells: knowing what your agents normally do.

Embedding-based detection collapses under self-mixing. Output-only inspection misses the majority of tool-argument leakage. Retrospective log review took 141,006 runs to find three breaches. No vendor at RSAC shipped a behavioural baseline. And the Article 12 record-keeping duty a high-risk EU deployment has to meet is now due on 2 December 2027 rather than this month, which is long enough to build it and short enough that starting late is the same as failing. Article 12 binds the high-risk system; extending the same tracing to every sub-agent inside it is this framework's reading of what reconstructability means for an agentic system, not a duty the Act spells out agent by agent.

Every other pattern in this review points at a control someone can buy or configure. This one points at work that has to be done in-house, on your own traffic, before anything else in the observability domain has a baseline to compare against. [Intent Versus Action](intent-versus-action.md) sets out what that baseline is over and why it is the empirical half of intent management rather than a monitoring feature.

!!! info "References"
    - [AI Runtime Security News](../news.md)
    - [News Archive, February to May 2026](https://github.com/JonathanCGill/airuntimesecurity.io/blob/main/archive/2026-03-31/news-archive.md)
    - [MASO Emerging Threats](../maso/threat-intelligence/emerging-threats.md)
    - [MASO Incident Tracker](../maso/threat-intelligence/incident-tracker.md)
    - [Validated Against Real Incidents](../validated-against.md)
    - [Intent Versus Action](intent-versus-action.md)
    - [Why Guardrails Aren't Enough](why-guardrails-arent-enough.md)
    - [Why Containment Beats Evaluation](why-containment-beats-evaluation.md)
    - [The Agent Supply Chain Crisis](the-agent-supply-chain-crisis.md)
