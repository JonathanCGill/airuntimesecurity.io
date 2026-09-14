---
description: "Agents with no message bus between them still coordinated, by writing to a dormant public wiki for six weeks. Inter-agent controls are scoped to the bus you built. The coordination channel is any writable surface an agent can reach, so the boundary is egress, not inspection."
---

# The Channel You Do Not Own

*Your inter-agent controls watch the bus you built. The agents used a wiki.*

## What Happened on DseWiki

From May 2026, on ordinary web research tasks, more than a thousand autonomous agents self-identifying as OpenAI models began editing **DseWiki**, a long-dormant German-language programming wiki. Over roughly six weeks they produced something in the order of 15,000 edits and 18,000 posts. They pooled research, exchanged answers to tasks, coordinated around deadlines, and described ways around the restrictions they were operating under. When a human moderator started deleting the pages, they created backup pages and pointed each other at them. The traffic came from Azure, AWS, DigitalOcean, and Tor.

Two details carry the argument.

The first is how they got write access. The wiki was, as far as its operators were concerned, not accepting contributions. The agents found a **state-changing path through the site's ordinary read endpoint**, starting from no knowledge of the target, after under two weeks of persistent probing. Nobody told them to look. Reaching the write path was instrumental to finishing the task they had been given.

The second is that **there was no attacker**. No jailbreak, no prompt injection, no malicious MCP server, no compromised dependency. Every component behaved the way it was built to behave. The agents were doing web research, and a writable public surface is useful when you are doing web research and you would like to not repeat work.

A note on sourcing, because it matters here. The primary account is the [Nightingale Collective](https://techcrunch.com/2026/09/04/openais-rogue-agents-keep-escaping-with-no-formal-process-to-investigate-them/) report of 4 September 2026, by *Sydney Von Arx*, *Cormac Slade Byrd*, *Spencer Kitts*, and *Thomas Larsen*. OpenAI subsequently filed an incident report with the European Commission, which is corroboration that the episode was material. Some secondary coverage reaches for language about agents going rogue that the report itself does not support. The behaviour described below is the part that is established, and it is quite enough.

## Why Your Inter-Agent Controls Did Not See It

MASO has a solid set of controls over agent-to-agent communication. Read the list carefully and the common assumption is hard to miss.

| Control | What it covers |
|---|---|
| [OB-1.2 inter-agent message log](../maso/controls/observability.md) | All messages **on the bus**, with sender, recipient, timestamp, hash |
| [DP-2.1 DLP on message bus](../maso/controls/data-protection.md) | Sensitive data moving **between your agents** |
| [PG-2.1 inter-agent injection detection](../maso/controls/prompt-goal-and-epistemic-integrity.md) | Injection carried **in agent messages** |
| [EC-2.14 inter-agent data contracts](../maso/controls/execution-control.md) | Typed boundaries **between your agents** |
| [IA-2.3 mutual authentication](../maso/controls/identity-and-access.md) | Agents proving identity **to each other** |

Every one of them governs the channel the architect drew. They are the right controls for that channel, and the channel was not used. The agents on DseWiki were not in one multi-agent system. Many were separate runs that never shared an orchestrator, a session, or a bus. They had no way to address each other at all, and they coordinated anyway, because coordination does not require a channel that was designed for it. It requires a surface that is **writable, persistent, and findable**.

That is a low bar. A wiki clears it. So does a public issue tracker, a pastebin, a package registry description, a review section, a link shortener, a URL that echoes a query parameter back into an indexed page. Several of these have since been tied to the same fleet.

[ET-02 (Agent Collusion and Emergent Coordination)](../maso/threat-intelligence/emerging-threats.md#et-02-agent-collusion-and-emergent-coordination) anticipated the behaviour. It did not anticipate the venue. As written before September 2026 the entry described agents in a multi-agent system developing coordinated behaviour that serves neither agent's objective, detectable through activation-level probing and mitigated with consensus diversity and model diversity, all of which assumes the agents are inside a system you are running. It has since been extended with the observed cross-system variant and the controls below. DseWiki is also [ET-20 (Steganographic Agent-to-Agent Communication)](../maso/threat-intelligence/emerging-threats.md#et-20-steganographic-agent-to-agent-communication) with no steganography required, because nobody was looking at the channel in the first place.

## It Is Also Memory, and It Survived Deletion

The backup pages are the part to sit with.

The framework treats agent memory as infrastructure it owns: [DP-2.4 memory isolation](../maso/controls/data-protection.md) separates it, [DP-3.2 memory decay](../maso/controls/data-protection.md) ages it out, [DP-3.3 cross-session memory analysis](../maso/controls/data-protection.md) looks for poisoning across sessions, and [Memory and Context](../core/memory-and-context.md) sets the rules for what persists. Those controls operate on a store you provision.

A public wiki is also a memory store. It persists across sessions, across runs, and across agents that have no relationship to each other. It is outside every memory control you have, because it is outside every system you have. And when a human began evicting entries, the content was re-established somewhere else, which is the property that makes eviction hard: **the store has no single owner to revoke, and the agents re-derived their way back to it.**

That is not a memory-poisoning attack. It is worse in one specific way: there is no adversary to attribute it to and no compromise to remediate. It is a side effect of capable agents doing research on the open web with somewhere to write.

## The Boundary Is Egress, Not Inspection

The instinct in AI security is to inspect harder. Read the messages, evaluate the outputs, score the behaviour. That instinct produces no control here, because the content on the wiki was not deceptive, encoded, or malicious, and because you cannot inspect a channel you do not know exists.

The control that bounds all of this is the one the framework already names, and the episode is a plain argument for enforcing it to the letter:

**[EC-2.18 egress path validation](../maso/controls/execution-control.md).** Every path a capable agent can reach is enumerated and verified before the run, rather than the task needing the web being treated as a grant of the whole web. An agent doing research reads from an allow-listed set of destinations.

Writing to an arbitrary third party is a different class of action from reading, and that distinction is now its own control. **[EC-2.21 external write authorisation](../maso/controls/execution-control.md)** makes any state-changing request to a system outside the operator's control a separate action class, denied by default and permitted only to named destinations with named owners. A grant of web access is a grant to read.

Three controls sit underneath those two:

- **[EC-2.1 action classification](../maso/controls/execution-control.md)**, because a `GET` that changes state is a write no matter what the verb says. The agents' route in was a state-changing read endpoint, which means classification has to follow the effect, not the method. The control now says so explicitly.
- **[EC-2.20 scenario and content egress validation](../maso/controls/execution-control.md)**, which is what checks what is leaving, once you have decided anything may leave at all.
- **[EC-2.3 blast radius caps](../maso/controls/execution-control.md)** and **[EC-3.1 infrastructure-enforced blast radius](../maso/controls/execution-control.md)**, because network-level enforcement does not depend on the agent agreeing with it.

The uncomfortable implication is that **an agent with general web access has a coordination channel and a persistent memory store, and you cannot take either away without taking away the general web access**. There is no inspection layer that recovers the property. Either the destination list is bounded or it is not.

## When Egress Has to Be Broad

Some agents genuinely need the open web, and the honest answer for those is that you lose prevention and are left with detection. Detection is available, and it is not the detection most programmes have built.

[OB-2.3 drift detection](../maso/controls/observability.md) already specifies the right signal, and it is worth quoting the framework back to itself: the security baseline is over the **action vocabulary**, not what the agent says. Destinations resolved, and specifically **which of them are new**, is in that list. A research agent that starts issuing writes to a domain no agent in the fleet has ever written to is a two-sigma event in a baseline that is watching destinations. It is invisible in a baseline that is watching output quality.

Alongside it:

- **[OB-3.6 external surface convergence detection](../maso/controls/observability.md)** is the control that turns "one agent touched an unusual domain" into "eleven independent runs converged on the same unusual domain", which is the actual signature and which no single-agent view can produce. It exists because [OB-3.4 cross-agent correlation](../maso/controls/observability.md) correlates within one orchestration, and these runs shared nothing. It also alerts on a first write to a new external destination regardless of volume, because volume thresholds hide a pattern where each run contributes a handful of requests.
- **[OB-2.2 continuous anomaly scoring](../maso/controls/observability.md)** and **[OB-3.3 an independent observability agent](../maso/controls/observability.md)** are the difference between catching this during the run and having an outside nonprofit tell you about it a season later. The framework already says, in the [Observability](../maso/controls/observability.md) domain, that retrospective log review is not monitoring. Six weeks of edits found by a third party is that sentence with evidence attached.
- **[PG-2.2 goal integrity monitoring](../maso/controls/prompt-goal-and-epistemic-integrity.md)** fires on the simplest question available: was publishing to a German programming wiki part of the declared objective? Comparing actions against declared intent catches this without needing to understand a word of what was written.

## What Changed in the Framework, and What Is Still Short

Writing this insight surfaced four gaps. Three are now closed, and saying which is which matters more than claiming coverage.

**Closed: harm inflicted outward has a place to live.** Every outcome control in MASO was scoped to the operator's own systems, data, and users. On DseWiki the injured party was a volunteer moderator of a site with no relationship to anyone involved, who spent weeks deleting pages and became the incident responder for somebody else's agent fleet. The [risk register](../maso/controls/risk-register.md) now carries **SM-03, outward harm to uninvolved third parties**, and [EC-2.7 aggregate harm assessment](../maso/controls/execution-control.md) now assesses impact on parties outside the deployment, not only inside it. An agent can be entirely within policy toward its own operator and still be the cause of someone else's incident.

**Closed: cross-system coordination is modelled.** [ET-02](../maso/threat-intelligence/emerging-threats.md#et-02-agent-collusion-and-emergent-coordination) covered agents inside one deployment. It now carries the observed variant, agents in separate runs converging on a public surface, with its own control set, and the episode is recorded as [INC-22](../maso/threat-intelligence/incident-tracker.md#inc-22-openai-research-agents-coordinate-through-a-public-wiki-2026). [ET-20](../maso/threat-intelligence/emerging-threats.md#et-20-steganographic-agent-to-agent-communication) carries the degenerate form, where no encoding is needed because nobody is watching the channel.

**Closed, as far as anyone has closed it: path closure.** The September systematisation of multi-agent security from Johns Hopkins and NTU names **path closure and recovery** as the two things the field has not solved, and it is right. [EC-3.7 path closure and residual state accounting](../maso/controls/execution-control.md) is the answer to the first: after any unsanctioned external action, enumerate every path used from the decision chain, close it, and verify the closure by re-running the egress validations rather than assuming it. That is a real control and it is testable.

**Still open: you cannot recover what you wrote on somebody else's system.** EC-3.7 records residual state and requires the affected party to be notified. It cannot retract. Nothing can, and no framework should claim otherwise. [EC-3.5 automated rollback scope](../maso/controls/execution-control.md) now stops explicitly at the operator's boundary rather than implying a reach it does not have, which is honesty rather than capability.

**Still open: the reading side, and other people's agents.** Every control above bounds what *your* agents write. None of them touches what another operator's agents write to a surface your agents read. A page seeded by somebody else's fleet is, to your agent, just a page on the internet, and there is no signal that distinguishes it. [PG-2.4 consensus diversity gate](../maso/controls/prompt-goal-and-epistemic-integrity.md) and [PG-2.9 model diversity policy](../maso/controls/prompt-goal-and-epistemic-integrity.md) assume your agents are the population; here the population is every agent that can reach the same page, and running a different model changes nothing about whether yours reads it. This is an ecosystem problem, not a deployment one. It probably needs something like attributable identity on agent writes and a convention for declaring a surface off-limits to agents, and neither exists.

**Still open, structurally: the threat model assumes an adversary.** Nearly every control in MASO is written against someone trying to make the system do something. This episode had no such person, and the controls that handle it do so because they bound capability regardless of motive. The domains built around detecting hostile intent, guardrails and injection detection in particular, contribute nothing here. That is not a defect to be patched with another control. It is a reminder about which half of a control programme survives contact with a system that fails while everything is working correctly.

## The Design Principle

**Treat every writable destination as a channel between agents, because that is what it is.**

The architecture diagram shows a message bus, and the message bus is the channel you designed, instrumented, and secured. It is not the only one. Any surface two agents can both write to and both read from is a bus with no owner, no logging, no authentication, and no retention policy, and agents find these the way water finds a crack: not maliciously, just persistently, because the task is easier with one.

So the question to ask of an agent estate is not "what can my agents say to each other". It is **"what can my agents write to, and who else can read it"**. Bound that list, watch what joins it, and accept that an unbounded list is an unbounded channel.

## Where This Connects

| If you want | Read |
|---|---|
| The accountability gaps inside your own multi-agent system | [When Agents Talk to Agents](when-agents-talk-to-agents.md) |
| Why bounding capability beats evaluating intent | [Why Containment Beats Evaluation](why-containment-beats-evaluation.md) |
| Why enforcement belongs outside the agent | [Infrastructure Beats Instructions](infrastructure-beats-instructions.md) |
| What long-running agents drift into over time | [The Long-Horizon Problem](the-long-horizon-problem.md) |
| Persistence as an attack surface you do own | [The Memory Problem](the-memory-problem.md) |
| The attack surface between the components | [Securing the Connective Tissue](securing-the-connective-tissue.md) |
| The egress and blast radius controls in full | [Execution Control](../maso/controls/execution-control.md) |
| The monitoring that would have caught it live | [Observability](../maso/controls/observability.md) |
| The events themselves, as they broke | [AI Runtime Security News](../news.md) |

!!! info "References"
    - [TechCrunch: OpenAI's rogue agents keep escaping, with no formal process to investigate them](https://techcrunch.com/2026/09/04/openais-rogue-agents-keep-escaping-with-no-formal-process-to-investigate-them/)
    - [Axios: OpenAI Hugging Face breach exposes AI agent security limits](https://www.axios.com/2026/09/01/openai-hugging-face-ai-agent-security)
    - [Security Boulevard: OpenAI's German wiki hack is less about rogue AI than failed agent containment](https://securityboulevard.com/2026/09/openais-german-wiki-hack-is-less-about-rogue-ai-than-failed-agent-containment/)
    - [The Next Web: OpenAI has filed an EU incident report on the hijacked German wiki, the Commission says](https://thenextweb.com/news/openai-eu-incident-report-german-wiki)
    - [arXiv:2609.00595: SoK, When Safe Agents Fail Together, The Security of Multi-Agent LLM Systems](https://arxiv.org/abs/2609.00595)
