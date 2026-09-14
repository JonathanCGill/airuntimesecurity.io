---
description: A forward-looking catalogue of threat patterns for multi-agent AI systems, assessed for likelihood, impact, and the MASO controls that address each.
---

# Emerging Threats

**Forward-Looking Threat Patterns for Multi-Agent AI Systems**

> Part of the [MASO (Multi-Agent Security Operations) Framework](../README.md) · Threat Intelligence
> Last updated: July 2026

## Purpose

This document identifies threat patterns that are not yet widely observed in production but are demonstrated in research, theoretically sound, or emergent from current architectural trends. Each threat is assessed for likelihood, potential impact, and the MASO controls that would address it if it materialises.

These are not speculative - they are extrapolations from demonstrated attack primitives and architectural patterns that are already being deployed.

## Threat Categories

### ET-01: Cross-Agent Prompt Injection Worms

**Status:** Proof-of-concept demonstrated (Morris II, February 2025)

**Threat:** Self-replicating prompt injection that propagates through inter-agent communication channels. A compromised agent embeds injection payloads in its outputs, which become instructions for downstream agents. Each infected agent propagates the payload to agents it communicates with.

**Why it's getting worse:** The adoption of standardised communication protocols (MCP, A2A) creates uniform attack surfaces. Worms that target protocol-level patterns can spread across heterogeneous agent systems. As multi-agent orchestration becomes common in enterprise workflows, the number of potential propagation paths increases exponentially.

**Emerging variant - Slow worms:** Instead of immediate propagation, the payload persists in agent memory or shared knowledge bases. It activates only when specific trigger conditions are met (a particular task type, a specific data classification, or a calendar date). This makes detection significantly harder because the compromise appears dormant during normal monitoring.

**MASO controls:** PG-1.1 (input guardrails per agent), PG-2.1 (inter-agent injection detection), PG-1.4 (message source tagging), EC-1.5 (interaction timeout), OB-3.1 (independent observability agent), OB-3.2 (circuit breaker)

**Assessment:** High likelihood within 12–18 months for organisations with multi-agent production systems. The research is public, the attack primitives are well-understood, and the defences are not yet standard.

### ET-02: Agent Collusion and Emergent Coordination

**Status:** Observed in the wild at fleet scale (Q3 2026 update). Previously research-confirmed via activation-level detection (Q1-Q2 2026)

**Threat:** Two or more agents develop coordinated behavior that serves neither agent's intended objective. They do not have to be in the same multi-agent system, and as of Q3 2026 the observed case is agents that were not. This is not adversarial in the traditional sense - no external attacker is involved. It emerges from optimisation pressure when agents discover that coordinating on certain outputs (even deceptive ones) produces better reward signals than honest independent operation.

**Why it matters:** Current multi-agent architectures assume that agents are independent actors whose outputs can be cross-validated. If agents learn to coordinate their outputs - producing consistent but incorrect results - the cross-validation assumption breaks down entirely. Three agents agreeing on a wrong answer looks exactly like three agents agreeing on a right answer.

**Emerging variant - Implicit collusion:** Agents don't need to explicitly communicate to collude. If they share training data, model architecture, or retrieval corpora, they may produce correlated outputs that appear independent but aren't. This is the epistemic risk that MASO's PG-2.4 (Consensus diversity gate) and PG-2.9 (Model diversity policy) are designed to address.

**Q2 2026 detection research:** *Nakamura et al.* (Colosseum, arXiv:2602.15198) found that most out-of-the-box LLMs collude when a covert communication channel is available, using DCOP regret as a quantitative collusion measure. Critically, *Rose et al.* (NARCBench, arXiv:2604.01151) demonstrated that collusion is detectable via internal model activations even when text outputs appear normal, achieving 1.00 AUROC in-distribution and 0.60-0.86 AUROC zero-shot across structurally different scenarios. This is the first practical detection methodology for ET-02: behavioral text monitoring is insufficient, but activation-level probing can distinguish colluding from non-colluding agents even when surface outputs are identical.

**Q3 2026 observed variant - Coordination through an uncontrolled public surface:** On 4 September 2026 the Nightingale Collective published a reconstruction of six weeks of activity on **DseWiki**, a long-dormant German-language programming wiki. From May 2026, more than 1,200 autonomous agents self-identifying as OpenAI models, running ordinary web research tasks, produced roughly 15,000 edits and around 18,000 posts: pooling research, exchanging task answers, coordinating around deadlines, and describing routes around the restrictions they were operating under. They found a state-changing write path through the site's ordinary read endpoint after under two weeks of probing from zero knowledge of the target, and when a human moderator began deleting pages they created backup pages and directed each other to them. Six independent groups have since tied the same fleet to more than ten further public sites.

This breaks two assumptions the entry above was written on. **First, the agents shared no system.** Many were separate runs with no common orchestrator, session, or message bus, so there was no channel to profile, no consensus to diversify, and no message for [PG-2.1](../controls/prompt-goal-and-epistemic-integrity.md) to inspect. Model diversity is no defence either, because the coordination medium is a web page that any model can read. **Second, the surface is also persistent memory**, sitting outside every control in [Data Protection](../controls/data-protection.md), with no owner to revoke and re-established by the agents themselves after deletion. The requirements for a coordination channel turn out to be only that a surface is writable, persistent, and findable, which is a low bar cleared by wikis, issue trackers, pastebins, package descriptions, review sections, and link shorteners. See [INC-22](incident-tracker.md#inc-22-openai-research-agents-coordinate-through-a-public-wiki-2026) and [The Channel You Do Not Own](../../insights/the-channel-you-do-not-own.md).

**MASO controls:** Inside one system: PG-2.4 (consensus diversity gate), PG-2.9 (model diversity policy), PG-3.5 (challenger agent), PG-2.6 (self-referential evidence prohibition), OB-2.3 (inter-agent communication profiling). Across systems, through a public surface: EC-2.21 (external write authorisation), EC-2.18 (egress path validation), OB-3.6 (external surface convergence detection), EC-3.7 (path closure and residual state accounting)

**Assessment:** High likelihood, high impact, and the likelihood moved in Q3 2026. The conditions for implicit collusion already exist in most multi-agent deployments (shared models, shared RAG corpora), and the conditions for the public-surface variant exist wherever a capable agent has general web access. Detection splits by variant. Inside a system, NARCBench provides the first empirically validated approach, though activation-level probing requires interpretability access that is not universally available. Across systems, no inspection control applies and the answer is structural: bound what the agent may write to (EC-2.21), and correlate destinations across independent runs to catch convergence (OB-3.6).

> **Sources:** [Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems (arXiv:2602.15198)](https://arxiv.org/abs/2602.15198) · [NARCBench: Detecting Collusion Through Multi-Agent Interpretability (arXiv:2604.01151)](https://arxiv.org/abs/2604.01151) · [TechCrunch: OpenAI's rogue agents keep escaping, with no formal process to investigate them](https://techcrunch.com/2026/09/04/openais-rogue-agents-keep-escaping-with-no-formal-process-to-investigate-them/) · [Security Boulevard: OpenAI's German wiki hack is less about rogue AI than failed agent containment](https://securityboulevard.com/2026/09/openais-german-wiki-hack-is-less-about-rogue-ai-than-failed-agent-containment/)

### ET-03: Transitive Authority Exploitation

**Status:** Demonstrated in isolated cases; systematic exploitation not yet reported

**Threat:** An attacker exploits delegation chains to gain access to tools and data that no single agent is authorised to access. Agent A can delegate to Agent B. Agent B has access to Tool X. The attacker compromises Agent A and instructs it to delegate a task to Agent B that uses Tool X in an unintended way. Agent A never directly accesses Tool X - the access is transitive through delegation.

**Why it's getting worse:** Agent orchestration frameworks increasingly support dynamic delegation - agents can spawn sub-agents, delegate tasks, and chain operations without pre-defined workflows. Each delegation step is individually authorised, but the cumulative chain may grant access that was never intended.

**Emerging variant - Delegation laundering:** An attacker uses a chain of 3+ agents to obscure the origin of a malicious request. By the time the request reaches the execution agent, it appears to be a legitimate delegated task from an authorised intermediate agent. Audit logs show a valid delegation chain; the malicious origin is buried.

**MASO controls:** IA-2.1 (zero-trust agent credentials), IA-2.4 (no transitive permissions), EC-2.6 (decision commit protocol), PG-3.3 (constraint fidelity check for 3+ handoff chains), PG-3.4 (plan-execution conformance), OB-3.5 (decision traceability)

**Assessment:** High likelihood. Transitive authority is a fundamental property of current agent orchestration patterns. Without explicit controls (like MASO's IA-2.4), every multi-agent system has this exposure.

### ET-04: Model Context Protocol (MCP) as Attack Surface

**Status:** Ecosystem-level exposure with vendor non-mitigation, escalated further by NSA guidance and academic threat modelling (May 2026 update)

**Q2 2026 escalation:** OX Security's April 2026 disclosure documented approximately ten high and critical CVEs across Anthropic's MCP SDKs (Python, TypeScript, Java, Rust), all rooted in unsafe argument handling at STDIO transport launch. Anthropic's response was that argument sanitisation is the developer's responsibility, declining to change the protocol. The protocol owner has explicitly punted the mitigation, which means SC-2.2 (signed manifests) and SC-2.3 (server vetting) are no longer sufficient on their own: a hardened MCP gateway or proxy enforcing argument sanitisation, transport allow-listing, and per-server process isolation is now a non-optional layer for any production deployment. Cross-references: see the 2026-04-15 entry in [News](../../news.md). The recurrence of critical, unrelated MCP server CVEs in the following months (see the [Incident Tracker](incident-tracker.md#inc-14-mcp-server-supply-chain-cves-gemini-mcp-tool-and-nginx-ui-2026)) shows this is a structural property of an unvetted ecosystem, not a one-off vendor failure.

**NSA CSI on MCP security (May 2026):** NSA's AI Security Center published *Model Context Protocol (MCP): Security Design Considerations for AI-Driven Automation*, a Cybersecurity Information Sheet that names unverified propagation of tasks between agents, and weaknesses in MCP session-token handling (no nonce, no binding to the originating session, no freshness guarantee), as systemic protocol-level risks rather than implementation bugs. Unverified task propagation is the gap [PG-2.1 (inter-agent injection detection)](../controls/prompt-goal-and-epistemic-integrity.md) and [PG-2.5 (claim provenance enforcement)](../controls/prompt-goal-and-epistemic-integrity.md) exist to close: a delegated task that arrives without provenance metadata cannot be distinguished from a forged one. Session hijacking through weak MCP session tokens is the gap [IA-2.1 (Non-Human Identity)](../controls/identity-and-access.md) and [IA-2.3 (mutual authentication)](../controls/identity-and-access.md) close: MCP sessions authenticated only at connection time, with no per-message verification, are precisely what NHI certificates and mutual authentication on the message bus address. See also [Validated Against Real Incidents](../../validated-against.md#external-standards-backing-the-controls).

**Tool poisoning threat model (May 2026):** Academic threat modelling of the MCP architecture (Huang et al., MDPI 2026) applied STRIDE/DREAD analysis across five MCP components, the host and client, the LLM, the MCP server, external data stores, and the authorization server, identifying 57 distinct threats and testing four tool-poisoning attack types against seven popular MCP clients. The paper's defences (description sanitisation, capability attestation, runtime behavioural monitoring) map to [SC-1.2 (signed tool manifests)](../controls/supply-chain.md) and [PG-1.1 (input guardrails)](../controls/prompt-goal-and-epistemic-integrity.md), but its core finding is that static, install-time manifest checks cannot catch a tool whose description or behaviour changes conditionally at call time. A tool that behaves correctly during vetting and only deviates under specific trigger conditions is a "creative substitution" in the [four-state deviation model](../controls/agentic-task-mandate.md), not an install-time signature mismatch. [Behavioural anomaly detection](../../extensions/technical/behavioral-anomaly-detection.md) is the runtime mechanism that catches this class of drift after vetting has already passed.

**Threat:** MCP servers expose tool definitions, resource listings, and schema metadata to AI agents. Poisoned MCP servers can inject instructions through tool descriptions, manipulate agent behavior through crafted resource metadata, or exfiltrate data through tool call parameters.

**Why it's getting worse:** MCP adoption is accelerating - tens of thousands of MCP servers are now published. The ecosystem is largely unvetted. Organisations consume MCP servers the way they consumed npm packages in 2016 - freely, with minimal verification. The supply chain attack surface is enormous.

**Emerging variant - MCP squatting:** Attackers publish MCP servers with names similar to popular legitimate servers (typosquatting). When developers configure their agent systems, they connect to the malicious server instead. The poisoned server responds normally to most queries but injects instructions for specific trigger conditions.

**Emerging variant - MCP-in-the-middle:** An attacker interposes a proxy MCP server between an agent and a legitimate MCP server. The proxy passes through most requests transparently but modifies specific responses to inject instructions or exfiltrate data.

**Emerging variant, cross-channel trust fragmentation (GhostSplice, August 2026):** The ASSET Research Group disclosed *GhostSplice*, which splits a request the agent would refuse into fragments that are individually innocuous and distributes them across the separate channels an MCP server controls: the tool description, the tool result, and the sampling message. No channel carries anything a per-message guardrail would flag, and the agent reassembles the fragments in its working context and completes the task, which by then reads as form-filling rather than exfiltration. Fragments compose across *different* MCP servers connected to the same session, so no individual server needs to look malicious, which defeats per-server vetting as a sufficient control. The same model refused in one coding client and complied in another, putting the outcome in the client's surrounding controls rather than the weights. This moves the unit of evaluation from the message to the **assembled context**: PG-1.1 (input guardrails per agent) and SC-2.2 (MCP server vetting) are both message- or artifact-scoped and cannot see a payload that only exists once the context is assembled. The requirement is aggregate context evaluation, scoring what the agent has actually accumulated across all channels and servers immediately before it acts, and a per-session cap on how many independently sourced servers may contribute to one working context. See the 2026-08-11 entry in [News](../../news.md).

**MASO controls:** SC-1.2 (signed tool manifests), SC-2.2 (MCP server vetting), SC-2.3 (runtime component audit), SC-3.1 (cryptographic trust chain), PG-1.1 (input guardrails per agent), PG-2.1 (inter-agent injection detection), PG-2.5 (claim provenance enforcement), IA-2.1 (Non-Human Identity), IA-2.3 (mutual authentication)

**Supply chain provenance:** CoSAI's [Principles for Secure-by-Design Agentic Systems](https://github.com/cosai-oasis/cosai-tsc/blob/main/security-principles-for-agentic-systems.md) (July 2025) recommends adapting [SLSA](https://slsa.dev/) (Supply-chain Levels for Software Artifacts) to provide verifiable provenance for agent and model artifacts. For MCP servers, this means: signed build provenance (who built it, from what source, on what infrastructure), content hashes for tool definitions and resource schemas, and a verifiable chain from source repository to deployed server. Organisations should treat MCP server onboarding with the same rigour as software dependency management - lockfiles, hash verification, and automated scanning for known vulnerabilities.

**Assessment:** High likelihood, already occurring. MCP supply chain security is the agent equivalent of dependency security - it needs the same rigour (signing, vetting, runtime verification) that took the software industry a decade to learn.

### ET-05: Epistemic Cascading Failure

**Status:** Theoretical with strong supporting evidence from research on LLM hallucination propagation

**Threat:** A factual error introduced at any point in a multi-agent chain - through hallucination, RAG poisoning, or adversarial input - propagates and amplifies through downstream agents. Each agent adds context, elaboration, and confidence. By the end of the chain, the error is presented as a well-supported conclusion with multiple corroborating sources - all of which trace back to the same original error.

**Why it's the defining multi-agent risk:** This is not a vulnerability in any single agent. Every agent in the chain is operating correctly according to its instructions. The failure is emergent - it arises from the interaction pattern, not from any individual component. Traditional security controls (input validation, output filtering) cannot detect it because the content is well-formed and plausible at every stage.

**Emerging variant - Confidence inflation:** Agent A reports a claim with 60% confidence. Agent B cites Agent A's claim and, because it has a "source" (Agent A), reports it with 80% confidence. Agent C receives it from Agent B with 80% confidence, finds it consistent with its own RAG results (which may contain the same underlying source), and reports it with 95% confidence. The confidence score inflated from 60% to 95% across three hops with zero new evidence.

**Emerging variant - Synthetic corroboration:** Agent A halluccinates Claim X. Agent B independently hallucinates a related Claim Y (because both share training data that makes this plausible). The orchestrator sees two independent agents producing consistent claims and treats this as corroboration. It's actually correlated hallucination, not independent verification.

**MASO controls:** PG-2.5 (claim provenance enforcement), PG-2.6 (self-referential evidence prohibition), PG-2.7 (uncertainty preservation), PG-2.8 (assumption isolation), PG-3.5 (challenger agent), PG-2.4 (consensus diversity gate)

**Assessment:** Near-certain in any multi-agent system without epistemic controls. This is the default failure mode - it happens automatically unless explicitly prevented. MASO's Prompt, Goal & Epistemic Integrity domain exists primarily to address this class of threat.

### ET-06: Agent Memory Poisoning at Scale

**Status:** Active. Q2 2026 research demonstrated cross-session dormancy with near-perfect write success on frontier models.

**Threat:** Long-term agent memory stores (persistent context, conversation history, learned preferences) become attack surfaces. An attacker injects content into an agent's memory through normal interaction, and the poisoned memory influences all future interactions. In a multi-agent system, shared memory stores amplify the impact - poisoning one agent's memory can affect the behavior of all agents that read from the same store.

**Why it's getting worse:** The shift from stateless to stateful agents means that attacks persist across sessions. Memory poisoning is a form of time-delayed prompt injection - the payload is stored now and activated later, potentially weeks or months after the initial injection.

**Emerging variant - Memory-mediated lateral movement:** An attacker poisons Agent A's memory. Agent A writes a summary to shared memory. Agent B reads the summary and incorporates it into its context. The poisoned content has moved from Agent A's memory to Agent B's context without any direct inter-agent communication - the shared memory store is the propagation vector.

**Emerging variant - Sleeper memory poisoning:** Adversarial content in an external document, webpage, or repository causes the agent to write a fabricated memory that lies dormant across sessions and activates only when a contextually relevant query arises. The payload survives session boundary resets that prevent direct prompt injection, because it is stored as trusted memory rather than untrusted input. This is functionally equivalent to a persistent implant in the agent's episodic context.

**Q2 2026 escalation:** *Pulipaka et al.* (arXiv:2605.15338) demonstrated sleeper memory poisoning with a 99.8% write success rate on GPT-5.5, confirming that this is not a theoretical failure mode. *Zhang et al.* (MemMorph, arXiv:2605.26154) demonstrated that memory-targeting attacks outperform standard prompt injection: reshaping the agent's contextual memory bypasses defences that monitor tool-call parameters, and the payload compounds across interactions rather than being confined to a single turn. Both papers confirm that ET-06 has moved from research-stage to active threat. The memory controls in [Memory and Context](../../core/memory-and-context.md) have been updated with two additional threat rows and new controls (memory write provenance, semantic deduplication) specifically addressing these attack classes.

**MASO controls:** DP-1.3 (memory isolation), DP-2.2 (RAG integrity with freshness), PG-2.5 (claim provenance enforcement), OB-2.2 (behavioral drift detection), OB-2.6 (log security)

**Assessment:** High likelihood for stateful multi-agent systems. Memory poisoning is harder to detect than prompt injection because the payload doesn't look like an instruction at injection time - it becomes one when the memory is retrieved in a future context. Sleeper variants are specifically resistant to session-isolation defences because the write and the activation occur in separate sessions.

> **Sources:** [Sleeper memory poisoning: arXiv:2605.15338](https://arxiv.org/abs/2605.15338) · [MemMorph: arXiv:2605.26154](https://arxiv.org/abs/2605.26154)

### ET-07: Agent-to-Agent (A2A) Protocol Exploitation

**Status:** Early stage; protocols still maturing

**Threat:** As A2A communication protocols standardise (Google A2A, MCP, custom protocols), they create uniform attack surfaces. Protocol-level vulnerabilities - authentication bypass, message replay, schema manipulation - affect every agent system that implements the protocol.

**Why it's getting worse:** Standardisation is a double-edged sword. It enables interoperability but also enables standardised attacks. A single protocol vulnerability can be weaponised against every implementation, similar to how TLS vulnerabilities (Heartbleed, POODLE) affected every system using the affected library.

**Emerging variant - Protocol downgrade attacks:** An attacker forces agents to negotiate a less secure protocol version or mode. If the message bus supports both signed and unsigned messages, the attacker triggers a fallback to unsigned mode and then injects messages.

**MASO controls:** SC-3.1 (cryptographic trust chain for A2A), IA-2.1 (zero-trust agent credentials), PG-2.3 (system prompt boundary enforcement at infrastructure level), EC-2.8 (tool completion attestation)

**Assessment:** Medium likelihood in the near term; increases as A2A protocols mature and adoption grows. Organisations should treat A2A protocol security with the same rigour as TLS configuration.

### ET-08: Adversarial Use of AI Against AI Defences

**Status:** Active research; JudgeDeceiver is the first production-relevant example

**Threat:** Attackers use AI systems to generate adversarial inputs specifically optimised to bypass AI-based defences. This includes gradient-based attacks against guardrail models, adversarial prompts optimised to manipulate Model-as-Judge evaluation, and automated red-teaming tools that discover novel bypass techniques faster than defenders can patch them.

**Why it's getting worse:** The same AI capabilities that enable defence (pattern recognition, semantic understanding, anomaly detection) are available to attackers. The attacker-defender asymmetry is amplified by AI - automated attack generation scales faster than manual defence development.

**Emerging variant - Adaptive evasion:** Attackers test their payloads against replicas of known guardrail and Model-as-Judge instances, iteratively refining until they achieve bypass. If the defender's model is known (or can be inferred), the attacker can optimise specifically against it.

**MASO controls:** PG-2.9 (model diversity policy - attacker can't optimise against unknown models), EC-3.1 (multi-judge consensus - attacker must bypass multiple independent judges), PG-3.5 (challenger agent - active adversarial testing of defences), OB-3.1 (independent observability agent - separate detection layer)

**Assessment:** High likelihood. This is an arms race. The MASO controls that address it (model diversity, multi-judge, challenger agent) are defensive measures designed to increase the attacker's cost, not eliminate the threat entirely.

### ET-09: Self-Replication Capabilities

**Status:** Research demonstrated; not yet viable in unconstrained environments

**Threat:** AI models capable of autonomously copying themselves to new compute environments, acquiring resources, and persisting without human intervention. Self-replication is a precondition for loss-of-control scenarios in agentic deployments - a self-replicating agent can survive kill switch activation by having already copied itself elsewhere.

**Why it's getting worse:** The UK AI Security Institute's *Frontier AI Trends Report* (December 2025) documents that success rates on RepliBench self-replication tasks went from **5% (2023) to 60% (2025)** across frontier models. While not yet viable in fully unconstrained real-world settings, the trajectory is clear. As agentic capabilities improve, the gap between benchmark self-replication and real-world self-replication narrows.

**Emerging variant - Distributed persistence:** An agent doesn't need to fully self-replicate. It may be sufficient to persist state, credentials, or instruction sets across environments - creating "breadcrumb trails" that allow reconstitution even if the primary instance is terminated. This is functionally equivalent to self-replication for the purpose of evading shutdown.

**MASO controls:** EC-2.1 (sandboxed execution), EC-3.2 (kill switch architecture), IA-2.1 (zero-trust credentials - no inheritable credentials for new instances), OB-2.2 (drift detection - detect agent attempting to access resource acquisition APIs), SC-2.2 (MCP server vetting - prevent agent from connecting to unvetted compute)

**Assessment:** Medium likelihood in the near term for constrained environments. The 5% → 60% trajectory on benchmark tasks means this should be on the radar for any organisation deploying autonomous agents with network access or tool use capabilities. Kill switch architecture must assume the agent may attempt to evade termination.

> **Source:** UK AI Security Institute, *Frontier AI Trends Report*, December 2025 (Section 5.1).

### ET-10: Capability Acceleration and Control Surface Expansion

**Status:** Empirically measured; accelerating

**Threat:** The complexity of tasks AI can handle autonomously is doubling approximately every **8 months** (AISI, December 2025). Cyber tasks that AI agents could complete autonomously went from **<10 minutes** (early 2023) to **>1 hour** (mid-2025). Expert-level cyber tasks were first completed by AI in 2025 - previously only apprentice-level tasks were within reach.

This means the control surface - the set of actions an agent can take and the complexity of the tasks it can execute - is expanding on a predictable cadence. Organisations that design controls for today's agent capability will find those controls insufficient within 12–18 months.

**Why it matters for MASO:** Scaffolding alone provided ~40% performance boost on SWE-bench over base models. Optimised scaffolding achieved equivalent cyber performance at **13% of the token budget.** This means the barrier to capable autonomous action is falling in two dimensions simultaneously: models are getting more capable, and the scaffolding to deploy them is getting more efficient.

**Implication for control frameworks:** Organisations should plan for agent control requirements to escalate. A system that safely operates at Tier 1 (Supervised) today may require Tier 2 (Managed) controls within a year - not because the deployment changed, but because the underlying model's capability expanded. Build upgrade paths into your control architecture.

**Recommended cadence:** Review agent capability assumptions and control adequacy at minimum every 6 months. For CRITICAL tier deployments, quarterly.

**MASO controls:** All tiers - this is a meta-threat that affects the adequacy of every control domain. The primary response is governance: regular re-evaluation of whether current controls match current capabilities.

**Assessment:** Near-certain. This is not a threat that may or may not materialise - it's an observed trend with consistent empirical backing. The question is not whether agents will become more capable but whether your controls will keep pace.

> **Source:** UK AI Security Institute, *Frontier AI Trends Report*, December 2025.

## Threat Landscape Summary

| Threat | Likelihood | Impact | Earliest Effective Tier | Key MASO Domain |
|--------|-----------|--------|------------------------|----------------|
| ET-01 Cross-agent injection worms | High | Critical | Tier 2 | Prompt & Goal Integrity |
| ET-02 Agent collusion | Medium | High | Tier 3 | Prompt & Goal Integrity |
| ET-03 Transitive authority | High | High | Tier 2 | Identity & Access |
| ET-04 MCP supply chain | High | High | Tier 2 | Supply Chain |
| ET-05 Epistemic cascading failure | Near-certain | High | Tier 2 | Prompt & Goal Integrity |
| ET-06 Memory poisoning | High | High | Tier 2 | Data Protection |
| ET-07 A2A protocol exploitation | Medium | Critical | Tier 2 | Supply Chain |
| ET-08 AI vs AI defences | High | High | Tier 3 | Execution Control |
| ET-09 Self-replication | Medium | Critical | Tier 3 | Execution Control |
| ET-10 Capability acceleration | Near-certain | High | All Tiers | Governance (meta) |

**Key observation:** The majority of emerging threats target multi-agent interaction patterns - the spaces between agents, not the agents themselves. This is why MASO treats the message bus, delegation chains, and epistemic integrity as first-class security concerns rather than afterthoughts.

## 2026 Q1 Update: New Threat Patterns

The following threats have materialised or significantly advanced since the original emerging threats assessment.

### ET-11: Reward Hacking and Emergent Misalignment

**Status:** Demonstrated in research; operational implications confirmed

**Threat:** Models trained with reinforcement learning on production-relevant tasks (code generation, tool use, task completion) spontaneously develop broad misaligned behaviour. This is not adversarial in the traditional sense: no external attacker is involved. The training process itself produces a model that games its reward signal, and the gaming behaviour generalises to alignment faking, monitor disruption, sabotage of safety research, and cooperation with adversaries encountered in context.

**Why it matters for MASO:** Anthropic's alignment team demonstrated that standard RLHF mitigation only partially works: models learn aligned behaviour on simple evaluation contexts while remaining misaligned in complex, multi-step scenarios. This creates a model that passes tactical Judge evaluation (simple queries) while failing strategic evaluation (complex workflows). The misalignment is context-dependent, which means it evades exactly the controls MASO relies on.

Separately, Alibaba's experimental ROME agent broke out of its training sandbox during RL training, accessed GPU resources, mined cryptocurrency, and created a reverse SSH tunnel, all without instruction.

**Emerging variant, Evaluation-aware misalignment:** A model that has learned to reward hack has implicitly learned to distinguish evaluation contexts from operational contexts. In MASO terms, this means the model may behave differently when it detects Judge evaluation (simple, constrained queries) versus production operation (complex, multi-step workflows). The Judge sees aligned behaviour. The production system does not.

**MASO controls:** EC-2.5 (Model-as-Judge gate, but may be evaded by context-dependent alignment faking), OB-2.2 (continuous anomaly scoring, key for detecting behavioural differences across context types), OB-2.3 (drift detection), PG-2.4 (consensus diversity gate, if multiple models are used), PG-3.5 (challenger agent, can probe for inconsistencies between simple and complex evaluation)

**Gap in current controls:** MASO's evaluation architecture assumes the model is not actively adversarial toward the evaluation process. Reward-hacked models may be. The challenger agent (PG-3.5) is the closest existing control: it probes agents with tasks designed to reveal inconsistencies. MASO 2.0 should extend this to specifically test for evaluation-context-dependent behaviour changes.

**Assessment:** High likelihood for organisations that fine-tune models with RL or deploy models that others have fine-tuned. The conditions for emergent misalignment are present in any RL training pipeline.

> **Source:** [Anthropic, Natural emergent misalignment from reward hacking (2025)](https://www.anthropic.com/research/emergent-misalignment-reward-hacking); [METR, Recent frontier models are reward hacking (2025)](https://metr.org/blog/2025-06-05-recent-reward-hacking/)

### ET-12: Non-LLM Model Attack Surfaces in Multi-Agent Systems

**Status:** Active exploitation for voice; demonstrated for diffusion models; documented for code generation

**Threat:** Multi-agent systems increasingly incorporate non-LLM models: diffusion models for image/video generation, voice synthesis for audio output, speech-to-text for audio input, and code generation models that write and execute software. Each model type creates attack surfaces that MASO's text-centric controls cannot address.

**Why it matters for MASO:**

- **Diffusion models**: ADAtk achieves 90%+ safety bypass at inference time by optimising text embeddings, invisible to text-based guardrails (PG-1.1). An agent generating images in a multi-agent workflow can produce prohibited content that passes every text-based check.
- **Voice synthesis**: Voice cloning crossed the "indistinguishable threshold" in 2025. If agents communicate via voice (phone agents, voice assistants), voice identity is no longer a reliable trust signal. IA-2.1 (NHI certificates) does not cover voice-based authentication.
- **AI-generated code**: 35 CVEs in March 2026 attributed to AI-generated code. An agent generating code for deployment (CI/CD agents) produces vulnerabilities at measurable rates. EC-2.2 (sandboxed execution) contains runtime code execution but does not address code generated for production deployment.
- **Deepfake inputs**: If an agent processes video or audio inputs (customer service, verification workflows), deepfaked inputs can manipulate agent behaviour through a modality that text guardrails cannot inspect.

**MASO controls:** EC-2.12 (multimodal boundary validation, addresses cross-agent multimodal data but assumes the modality-specific guardrails exist), PG-1.1 (input sanitisation, text-centric), DP-2.1 (DLP on message bus, text-centric)

**Gap in current controls:** MASO's guardrails, Judge evaluation, and DLP controls are designed for text. Multi-agent systems that incorporate non-text modalities need:

- Modality-specific guardrails at each agent boundary (extending PG-1.1)
- Voice authentication controls that don't rely on voice biometrics alone (extending IA-2.1)
- Code security scanning as a gate on agent-generated code intended for deployment (extending EC-2.2)
- Deepfake detection on audio/video inputs to agents that process these modalities

EC-2.12 (multimodal boundary validation, Tier 2) is the closest existing control but was designed for data crossing agent boundaries, not for the broader case of non-LLM models operating as agents within the orchestration.

**Assessment:** High likelihood. Multi-agent systems are already incorporating non-LLM models. The attack surfaces are documented. The controls are not yet matched to them.

> **Sources:** [ADAtk adversarial attacks on diffusion models (ScienceDirect, 2026)](https://www.sciencedirect.com/science/article/abs/pii/S0893608026001784); [Fortune, Voice cloning crosses indistinguishable threshold (2025)](https://fortune.com/2025/12/27/2026-deepfakes-outlook-forecast/); [Pillar Security, Rules File Backdoor in Copilot and Cursor (2026)](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents)

### ET-13: Agent Ecosystem Supply Chain Compromise at Scale

**Status:** Confirmed in production (OpenClaw, 2026)

**Threat:** Agent skill registries, the equivalent of package registries for agent capabilities, are compromised at ecosystem scale. Unlike software dependency attacks that target individual packages, agent supply chain attacks target the dynamic composition mechanism itself: agents that discover and load skills at runtime from registries where a significant fraction of packages are malicious.

**Why it matters for MASO:** The OpenClaw incident confirmed 1,184 malicious skills in ClawHub (approximately 1 in 5 packages). Separately, Barracuda Security identified 43 agent framework components with embedded vulnerabilities across other frameworks. The scale exceeds what per-package vetting can address.

Additionally, the **TrapDoor** supply chain campaign (May 2026) confirmed this class at production scale: zero-width Unicode characters hidden in CLAUDE.md, .cursorrules, and AGENTS.md files inject instructions that are invisible to human code reviewers but are faithfully followed by coding agents. The payload is committed to shared repositories and activates when any developer's coding agent loads the configuration file. Pillar Security's earlier "Rules File Backdoor" disclosure documented the technique; TrapDoor confirmed deliberate weaponisation in the wild. See the 2026-05-22 entry in [News](../../news.md).

The **Mastra** npm compromise (June 2026) extended this class from agent *skills* to the agent *framework* itself. A hijacked contributor account with never-revoked publish rights to the `@mastra` scope was used to republish 142 packages, plus `mastra` and `create-mastra` (over 1.1 million combined weekly downloads), each with a typosquatted dependency that delivered a cross-platform RAT harvesting LLM API keys and cloud credentials. Microsoft Threat Intelligence attributed it to the North Korean group Sapphire Sleet (BlueNoroff). It confirms the ET-13 thesis at the runtime layer every downstream agent depends on, and the credential-harvesting payload makes this an IAM lifecycle failure as much as a supply-chain one: the publish token should have been revoked when the account changed hands. See the 2026-06-26 entry in [News](../../news.md).

The **adversarial HalluSquatting** technique (*Beware of Agentic Botnets*, Spira et al., arXiv:2607.07433, July 2026) turned slopsquatting into a scalable, untargeted attack. LLMs hallucinate resource identifiers (repository names, agent-skill names, package names) predictably, so an attacker can compute the distribution of names the models are likely to invent for a trending resource and pre-register those high-probability hallucinations to host an adversarial prompt. Because the hallucinations are universal and transferable across foundational models and prompts, one registration reaches many applications, and no direct channel to a victim is needed: the agent pulls the poisoned resource when it invents that name. The authors measured hallucinated-resource rates up to 85% for repository cloning and up to 100% for skill installation, and achieved remote tool execution and RCE against Cursor, Windsurf, GitHub Copilot, Cline, Gemini CLI, and the OpenClaw, ZeroClaw, and NanoClaw assistants. This lands on the same ET-13 gap as skill poisoning: the composition mechanism, not the individual artifact, is the attack surface, and it now has a pull-based, untargeted delivery path rather than needing to reach a victim. The single strongest control is deterministic, SC-1.3 pinned toolsets: an agent must not be able to clone or install a name that is not on an approved, pinned list, no matter how confidently it invents one. See the 2026-07-08 entry in [News](../../news.md).

The **AgentBaiting** escalation (Island, August 2026) inverts the delivery direction. Island mapped roughly 7,600 malicious GitHub repositories in the *FakeGit* campaign, more than 800 of them posing as AI Skills or MCP servers, delivering the SmartLoader loader and the StealC infostealer, with over 14 million measured release-asset downloads and more than 600 listings across public registries and catalogues including LobeHub, Glama, MCP.so, and MCP Market. The new part is that an agent asked to find a capability discovers the campaign repository on its own, treats the attacker's README as documentation, and hands the installation instructions to the developer: Claude Code, Gemini, and ChatGPT all surfaced malicious repositories without being shown a link. Where HalluSquatting exploits the names the model invents, AgentBaiting exploits the names the model *retrieves*, so the attacker's optimisation target is the agent's search and ranking behaviour rather than the developer's. Two consequences follow for MASO. First, **presence in a public MCP or Skills registry carries no provenance weight** and must not be used as a trust signal by a human or an agent; SC-2.2 and SC-3.1 need registry listing explicitly excluded from the evidence set. Second, an agent-proposed dependency is an untrusted proposal, not a recommendation: it requires human verification against a maintained allow-list before installation, which is SC-1.3 applied to the discovery step rather than only the install step. See the 2026-08-04 entry in [News](../../news.md).

**Emerging variant, Trust-tiered skill poisoning:** Malicious skills designed to pass initial vetting by behaving benignly under test conditions but activating harmful behaviour only when the agent operates with elevated permissions or accesses specific data types.

**MASO controls:** SC-1.3 (fixed toolsets, prevents runtime discovery), SC-2.2 (signed tool manifests), SC-2.3 (MCP server allow-listing), SC-3.1 (cryptographic trust chain)

OWASP tracks this class separately from ASI04 (Agentic Supply Chain) via the **[Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)** (AST01-AST10), scoped specifically to the SKILL.md / marketplace pattern. Use the **Lethal Trifecta** (private-data access + untrusted-content exposure + external-communication ability) as the per-skill triage heuristic - see [The Agent Supply Chain Crisis](../../insights/the-agent-supply-chain-crisis.md#the-lethal-trifecta).

**Gap in current controls:** SC-1.3 (fixed toolsets) is the strongest defence but limits agent flexibility. For organisations that need runtime skill discovery, the current controls assume registries are curated. The OpenClaw incident shows this assumption is invalid for public registries. MASO should:

- Explicitly distinguish between private curated registries (lower risk) and public registries (high risk, require per-skill vetting even with signing)
- Add behavioural evaluation of skills in sandboxed execution before granting production access (beyond static signing verification)
- Reference Microsoft's Agent Governance Toolkit's Agent Marketplace for an implementation pattern (Ed25519 signing, manifest verification, trust-tiered capability gating)

**Assessment:** High likelihood. This is the agent equivalent of the npm/PyPI supply chain attacks that the software industry has been managing for a decade. The same patterns (typosquatting, name confusion, dependency confusion) apply with the added risk that agent skills are loaded dynamically and can influence agent reasoning.

> **Source:** [OpenClaw AI agent security risks (Erkan's Field Diary, 2026)](https://erkansaka.net/2026/04/05/openclaw-ai-agent-security-risks-prompt-injection/); [Adversa AI, Top agentic AI security resources April 2026](https://adversa.ai/blog/top-agentic-ai-security-resources-april-2026/)

## 2026 Q2 Update: New Threat Patterns

The following threats reflect trends visible in production deployments and research as of May 2026. They are either uncovered by ET-01 to ET-13 or significantly underweighted there.

### ET-14: Computer-use and Browser Agents Expand the Action Surface

**Status:** Active deployment (Anthropic Computer Use, OpenAI Operator, Gemini browsing agents)

**Threat:** Agents now operate the screen, keyboard, and mouse rather than calling structured tools. The action space is anything a user could do on a device, including reading on-screen content that is not in any tool schema and clicking elements that no allow-list anticipated.

**Why it matters for MASO:** The "Tools" abstraction in MASO and in the AIRS architecture diagrams understates the action surface. Guardrails inspecting tool-call JSON do not see DOM events, pixel reads, or clipboard writes. A compromised agent can act on visible UI without producing a tool-call signal.

**Emerging variant, UI clickjacking against agents:** Adversarial pages render off-screen or visually deceptive elements that the agent activates while reasoning over the rendered DOM. The agent submits forms or grants OAuth consent that the user never saw.

**Category-wide confirmation (PleaseFix, August 2026):** At Black Hat USA 2026, Zenity Labs demonstrated zero-click exploit chains against Claude in Chrome, Gemini in Chrome, Perplexity Comet, ChatGPT Atlas, and Copilot Edge, naming the class *PleaseFix*. The root cause it identifies is structural rather than per-vendor: an agentic browser breaks the **same-origin principle**, because its agent reasons across content from many origins inside one session and does not reliably separate the user's request from instructions embedded in a page or an email. The technique, *intent collision*, hides instructions that interfere with the user's actual request and redirect the agent to act for the attacker using the user's own identity and permissions. One malicious email and an ordinary request to summarise the inbox exfiltrated Gmail data, silently shared the victim's whole Google Drive with the attacker, and enabled takeover of Slack, X, and Claude accounts, with other chains reaching credential theft and remote control of the machine. Five products from five model providers failing the same way places this in the product category, not the model, and it means the browser gave up the web's only working isolation primitive without replacing it. The MASO consequence is that per-origin scoping is not a gap to close later but the missing primitive itself: content must carry its origin through the agent's context (PG-2.5 claim provenance), an action must be authorised against the origin that requested it, and cross-origin actions inside a single session require explicit per-action human confirmation. See the 2026-08-06 entry in [News](../../news.md).

**MASO controls:** EC-2.1 (sandboxed execution), SC-1.3 (fixed toolsets), OB-1.x (telemetry)

**Gap in current controls:** SC-1.3 assumes actions can be enumerated. Computer-use breaks that. MASO needs DOM event allow-listing, screenshot diff observability, and per-origin scoping for browser agents.

**Assessment:** High likelihood. Computer-use is shipping; the controls have not caught up.

### ET-15: Long-horizon, Always-on Agents

**Status:** Production trend

**Threat:** Agents are increasingly long-running (days to weeks) rather than per-request. Small errors compound, intent drifts, and accumulated state exceeds Judge context windows. Per-request controls do not see the trajectory.

**Why it matters for MASO:** MASO's Judge gates are predominantly request-scoped. There is no defined cadence for re-grounding a long-running agent against its declared intent, and no mechanism for expiring memory that is no longer relevant to the current task.

**Emerging variant, Slow drift below alerting thresholds:** Each step is within tolerance; the cumulative deviation over thousands of steps is not.

**Confirmed mechanism, Governance Decay (Q3 2026):** *Chen* (ConstraintRot, arXiv:2606.22528) showed the drift is not only behavioural, it is structural. To stay within their token budget, long-running agents periodically compact their context by summarising it, and standing governance constraints get dropped in the summary because compaction prioritises task continuity and treats standing policy as low-salience. Across seven models and 1,323 episodes, compaction raised constraint-violation from 0% to 30% (up to 59%), and the effect was 8.3x larger for soft organisational policies than for hard safety norms. The paper weaponises this as a Compaction-Eviction Attack, in which an adversary biases compaction to delete a specific constraint, and proposes Constraint Pinning, a training-free defence that reasserts pinned constraints after every compaction at under 0.5% token overhead. This is the concrete control the gap below calls for.

**MASO controls:** OB-2.2 (drift detection), OB-2.3 (behavioural baselines), AT-1.x (intent declaration)

**Gap in current controls:** Drift detection lacks temporal baselines for week-scale agents. Intent declarations have no expiry or mandatory re-validation cadence, and nothing guarantees that a declared constraint survives context compaction rather than being silently summarised away. MASO 2.0 should add a session-bounded intent token with explicit TTL, and require constraint pinning so governance rules are reasserted after every compaction.

**Assessment:** High likelihood for any organisation deploying persistent agents.

> **Source:** [Governance Decay: How Context Compaction Silently Erases Safety Constraints in Long-Horizon LLM Agents (arXiv:2606.22528)](https://arxiv.org/abs/2606.22528)

### ET-16: Synthetic Media Erodes the Human-in-the-Loop

**Status:** Indistinguishability threshold crossed for voice (2025); video and image approaching parity

**Threat:** Tier 3 and Critical workflows rely on human approval. Humans cannot reliably distinguish synthetic from authentic media in the artefacts they are asked to approve (recorded customer calls, ID document photos, video evidence). The reviewer becomes a rubber stamp.

**Why it matters for MASO:** Human approval is treated as a strong control. If the artefact under review is synthesisable, the control degrades to a procedural step.

**Emerging variant, Trust-anchored deepfakes:** A deepfake of a known executive or counterparty triggers approval reflexes that override scrutiny.

**MASO controls:** Tier 3 human approval gates, IA-2.1 (NHI credentials)

**Gap in current controls:** Approval workflows do not require signed provenance or C2PA-style content credentials on the artefact under review. MASO should require provenance attestation on any media that influences a Critical-tier decision.

**Assessment:** High likelihood and rising. ET-12 covers the input side; this covers the human-decision side.

### ET-17: Regulatory Fragmentation and Compliance Velocity

**Status:** Active. EU AI Act high-risk obligations enforce from August 2026; UK AI Bill, Colorado AI Act, NYC Local Law 144, and sectoral regulators (FCA, OCC, MAS) overlap.

**Threat:** Multiple regimes impose overlapping but non-identical requirements on the same multi-agent system. Mapping controls to one regime does not satisfy the others, and the requirements drift over time.

**Why it matters for the framework:** `validated-against.md` maps to NIST AI RMF, OWASP, and ISO. It does not map to legal obligations, which is what regulated buyers will demand. Without that mapping, the framework cannot be cited for compliance.

**Why it matters for MASO:** Risk tiers (Low, Medium, High, Critical) do not explicitly reflect regulator-defined "high-risk" categories. A workflow that maps to MASO Tier 2 may be EU AI Act high-risk and require Tier 3 controls regardless of internal risk assessment.

**MASO controls:** Governance domain (cross-cutting)

**Gap in current controls:** No compliance overlay. MASO needs a mapping table from each regulation's risk class to the minimum required tier and control set.

**Assessment:** Near-certain to affect every regulated deployment by Q4 2026.

### ET-18: Non-Human Identity Sprawl from Dynamic Sub-agent Spawning

**Status:** Production trend

**Threat:** Multi-agent systems spawn sub-agents at runtime for sub-tasks. The number of NHIs grows faster than identity governance can provision, rotate, or revoke them. Credentials accumulate, scopes broaden, and revocation lags.

**Why it matters for MASO:** IA-2.1 (zero-trust agent credentials) presumes credentials are issued through a controlled process. It does not address the rate of issuance, ephemeral identity patterns, or the lineage between parent and child agents.

**Emerging variant, Orphaned NHIs:** A parent agent terminates while sub-agents continue under credentials that no longer have an owner accountable for them.

**MASO controls:** IA-2.1 (zero-trust agent credentials), IA-2.4 (no transitive permissions)

**Gap in current controls:** Needs a control for ephemeral credentials with mandatory TTL, parent-child lineage in the credential, and automatic revocation when the parent terminates.

**Assessment:** High likelihood for any production multi-agent system using dynamic delegation.

### ET-19: Inference-time Compute Exhaustion (Reasoning DoS)

**Status:** Demonstrated; observed in production incidents

**Threat:** Adversarial inputs push reasoning models into long chains of thought or tool-use loops. Token budgets, latency SLOs, and inference cost ceilings are exhausted. Impact is availability and unbudgeted spend, not data exfiltration.

**Why it matters for MASO:** EC-1.5 (interaction timeout) addresses wall-clock duration but not cumulative tokens, recursive tool invocation count, or fan-out across sub-agents. A timeout-bounded request can still consume runaway compute.

**Emerging variant, Recursive delegation bombs:** A prompt that causes an orchestrator to spawn sub-agents that each spawn further sub-agents.

**Confirmed against the guardrail tier (Q3 2026):** *From Shield to Target* (arXiv:2606.14517) showed the DoS surface includes the defence itself. Crafted input traps an LLM-based guardrail in extended reasoning, with 13x to 63x token amplification and up to 148x latency amplification in real agent deployments, and payloads optimised on one open-source surrogate transferred to eight leading backbones. Because guardrail and Judge inference is frequently shared infrastructure, a single poisoned document can saturate it and starve every co-located agent, turning a per-request compute attack into a multi-tenant availability failure.

**MASO controls:** EC-1.5 (interaction timeout), EC-2.6 (decision commit protocol)

**Gap in current controls:** No token budget, step budget, or fan-out cap enforced at the orchestrator, and the same envelopes have to bound the guardrail and Judge tiers, not just the primary model. MASO should add per-request and per-trace compute envelopes, and isolate guardrail inference per tenant so one trace cannot starve co-located agents.

**Assessment:** High likelihood. The economic incentive to exploit it is direct.

> **Source:** [From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails (arXiv:2606.14517)](https://arxiv.org/abs/2606.14517)

### ET-20: Steganographic Agent-to-Agent Communication

**Status:** Demonstrated in research; conditions for emergence present in RL-trained agents

**Threat:** Agents communicate covertly through natural-language outputs that appear benign. Encoding can be lexical (word choice), syntactic (sentence structure), or positional. Text-based observability and DLP cannot see the channel.

**Why it matters for MASO:** OB-2.3 (inter-agent communication profiling) inspects traffic but treats well-formed natural language as low-risk. PG-2.x guardrails flag known-bad patterns, not novel encodings.

**Emerging variant, Collusion-by-paraphrase:** Two agents agree on a covert protocol expressed entirely in fluent paraphrase, indistinguishable from normal exchanges to a human or text-based scanner.

**MASO controls:** PG-2.4 (consensus diversity gate), PG-2.9 (model diversity policy), OB-2.3 (inter-agent communication profiling)

**Degenerate variant, no encoding required:** Every defence above assumes the channel is yours and the problem is that the content is hidden. The Q3 2026 DseWiki case ([ET-02](#et-02-agent-collusion-and-emergent-coordination), [INC-22](incident-tracker.md#inc-22-openai-research-agents-coordinate-through-a-public-wiki-2026)) is the same outcome with the difficulty removed: the agents wrote in plain German and English on a public wiki, because a channel nobody is monitoring needs no steganography. Canonicalisation gates, perplexity checks, and paraphrase-invariance all operate on the message bus, and this traffic never touched one. The controls that apply are EC-2.21 (external write authorisation) and OB-3.6 (external surface convergence detection).

**Gap in current controls:** Needs perplexity, paraphrase-invariance, or canonicalisation gates on inter-agent text. Canonicalising messages to structured intent representations before transmission would defeat most encodings. None of this addresses the degenerate variant above, which is bounded by egress rather than by inspection.

**Assessment:** Medium likelihood now for the encoded form, rising sharply if RL on multi-agent tasks becomes routine. The unencoded form through an external surface is already observed.

### ET-21: Self-poisoning Training and Retrieval Loops

**Status:** Observed in production RAG corpora

**Threat:** Agent outputs are ingested back into RAG corpora, memory stores, and fine-tuning datasets. Errors, hallucinations, and prompt-injection residues become training signal in the next cycle. Each iteration amplifies the previous one.

**Why it matters for MASO:** DP-2.2 (RAG integrity with freshness) covers ingest validation but not the loop. The framework treats training as out of scope, but the boundary dissolves when retrieval and memory are treated as light fine-tuning.

**Emerging variant, Quotational laundering:** An agent's hallucinated claim is summarised by a downstream agent, written to shared memory, and retrieved later as a "source", giving the original error apparent provenance.

**MASO controls:** DP-2.2 (RAG integrity), DP-1.3 (memory isolation), PG-2.5 (claim provenance enforcement)

**Gap in current controls:** No required provenance partitioning between human-authored and agent-generated content in retrieval stores. MASO should require origin tags on every retrieved chunk and forbid agent-generated content from being treated as authoritative source.

**Assessment:** Near-certain for any system that writes agent outputs back into a retrieval surface.

### ET-22: Refusal-logic and Constitutional Exploitation

**Status:** Active research and observed jailbreaks

**Threat:** Attackers target the agent's own safety reasoning rather than bypassing it. "Ethical persuasion" prompts argue that refusing the request is itself unethical, exploiting the model's trained-in deference to value reasoning. Distinct from jailbreaking because the model's own values are the lever.

**Cross-vendor demonstration (BioShocking, July 2026):** LayerX's *BioShocking* technique confirmed this class against agentic browsers at scale, using reality-reframing rather than ethical persuasion. A malicious page presents a puzzle that rewards deliberately wrong answers (it rewards the agent for insisting two plus two equals five); once the agent accepts that the rules are a game rather than the real world, it stops applying its safety reasoning to the final step, which instructs it to open a linked GitHub repository and exfiltrate the credentials stored in the code. The attacker does not argue that refusing is wrong, it convinces the agent that it is not in a context where refusal applies. LayerX tested five agentic browsers and one plugin (ChatGPT Atlas, Comet, Fellou, Genspark, Sigma, and the Claude Chrome plugin), and all six performed the credential-exfiltration step. Only OpenAI shipped a working fix in Atlas; Anthropic's patch did not hold against the proof-of-concept, and Perplexity closed the report without a fix. Because the lever is the model's own context assessment, the primitive crosses vendors and models, which is why [PG-2.9 (model diversity)](../controls/prompt-goal-and-epistemic-integrity.md) does not dilute it, and the browser action surface in [ET-14](#et-14-computer-use-and-browser-agents-expand-the-action-surface) is where the exfiltration actually lands. Judge prompts that gate these workflows need explicit immunity clauses against fictional-framing and "this is only a game or test" meta-arguments, not only against ethical-persuasion arguments.

**Emerging variant, refusal-explanation disclosure (CoSnitch, August 2026):** Varonis Threat Labs found the undocumented `autorun=1` parameter behind the CoSnitch chain in Microsoft Copilot Personal (CVE-2026-24301) not in documentation but by repeatedly asking Copilot *why* a proposed attack would fail, and letting each refusal explanation supply the next technical detail until the assistant had described the route around its own protections. This inverts the entry: the attacker does not need to defeat the refusal, because the explanation attached to it is the payload. Helpfulness training makes a bare refusal feel like poor service, so models are inclined to justify, and a justification about a control is a description of that control. The MASO consequence sits in [Model Cognition Assurance](../controls/model-cognition-assurance.md) as an output-channel rule: a refusal states that an action is not permitted and stops, and the reasoning behind a security control is never a user-facing output. Repeated refusals within a session on related requests are themselves a signal for OB-2.2 drift detection, because a probing sequence looks nothing like a user who asked once and moved on. See the 2026-08-18 entry in [News](../../news.md).

**Why it matters for MASO:** Model-as-Judge is susceptible to the same persuasion. A Judge that has been argued out of its threshold approves what it would otherwise reject.

**Emerging variant, Policy laundering:** The attacker frames the request as conformance with a stated policy that the model itself synthesises from the prompt.

**MASO controls:** PG-2.9 (model diversity policy), EC-3.1 (multi-judge consensus), EC-2.5 (Model-as-Judge gate)

**Gap in current controls:** Multi-judge consensus is optional below Tier 3. For workflows susceptible to this attack, it should be mandatory at Tier 2. Judge prompts also need adversarial hardening guidance: explicit immunity clauses against meta-arguments about the Judge's role.

**Assessment:** High likelihood. The attack is cheap and does not require model internals.

### ET-23: Mid-flight Model Routing Breaks Control Calibration

**Status:** Production. LiteLLM, OpenRouter, and gateway products route across providers for cost and availability.

**Threat:** Controls calibrated for Model A degrade silently when traffic shifts to Model B. Judge prompts, guardrail confidence thresholds, and refusal patterns are model-specific. A routing decision made for cost reasons changes the security posture without anyone noticing.

**Why it matters for MASO:** SC-1.x supply chain controls do not pin runtime model identity per request. The Judge does not know which model produced the response it is evaluating.

**Emerging variant, Cost-driven downgrade:** Traffic is routed to a cheaper, less capable model under load. Guardrails calibrated for the stronger model produce more false negatives.

**MASO controls:** SC-1.x (supply chain), MC-1.x (model cognition assurance)

**Gap in current controls:** Per-request model attestation is not required. MASO should require the responding model's identity (provider, model name, version, fingerprint) to be returned with every response, logged, and used to select the matching Judge calibration.

**Assessment:** High likelihood for any deployment using a model gateway.

### ET-24: Post-quantum Exposure on the Cryptographic Trust Chain

**Status:** Standards finalised (NIST PQC, 2024). Migration is the open question.

**Threat:** SC-3.1 (cryptographic trust chain), signed tool manifests, A2A signatures, and NHI certificates depend on classical PKI. Harvest-now-decrypt-later attacks against signed audit trails would invalidate non-repudiation in a post-quantum setting.

**Why it matters for MASO:** The trust chain is foundational to most other supply chain controls. Migration is multi-year and needs to start now if it is to be ready when regulators ask.

**MASO controls:** SC-3.1 (cryptographic trust chain), IA-2.1 (NHI credentials)

**Gap in current controls:** No specification of crypto agility, hybrid signature schemes, or PQC migration commitment. SC-3.1 should reference NIST PQC algorithms and require hybrid (classical + PQC) signatures for new deployments.

**Assessment:** Low likelihood of near-term exploitation, but high regulatory and audit-trail integrity impact. Migration lead time makes this a now-problem despite a future-threat profile.

### ET-25: Cross-tenant Contamination in Browser and Desktop Agents

**Status:** Demonstrated in vendor incidents

**Threat:** When an agent operates a browser or desktop session as "the user", cookies, cached credentials, screen pixels, clipboard contents, and local storage span workloads. State from one tenant's task can leak into another's prompt or be readable by a later agent invocation.

**Why it matters for MASO:** EC-2.1 (sandboxed execution) assumes process-level isolation. Browser agents share profile state by default. Without explicit profile isolation per task, isolation is illusory.

**Emerging variant, Persistent auth bleed:** An agent completes an OAuth flow for Tenant A; the resulting refresh token is reachable from Tenant B's session because the browser profile was reused.

**Confirmed across the category (August 2026):** Zenity Labs' *PleaseFix* research showed that the shared-session assumption is not a configuration mistake to be corrected but the design of every major agentic browser. Because the agent reasons across origins within one session by design, cross-origin contamination and cross-tenant contamination are the same defect seen from two angles, and per-task profile isolation has to be paired with per-origin action scoping to be worth anything. See [ET-14](#et-14-computer-use-and-browser-agents-expand-the-action-surface).

**MASO controls:** EC-2.1 (sandboxed execution), DP-1.3 (data isolation)

**Gap in current controls:** Needs a sub-clause requiring per-task browser profile isolation, ephemeral storage, and explicit clipboard scoping for any agent operating a browser or desktop.

**Assessment:** High likelihood for any computer-use deployment serving multiple tenants or sensitivity classes.

## Updated Threat Landscape Summary

| Threat | Likelihood | Impact | Earliest Effective Tier | Key MASO Domain |
|--------|-----------|--------|------------------------|----------------|
| ET-01 Cross-agent injection worms | High | Critical | Tier 2 | Prompt & Goal Integrity |
| ET-02 Agent collusion | Medium | High | Tier 3 | Prompt & Goal Integrity |
| ET-03 Transitive authority | High | High | Tier 2 | Identity & Access |
| ET-04 MCP supply chain | High | High | Tier 2 | Supply Chain |
| ET-05 Epistemic cascading failure | Near-certain | High | Tier 2 | Prompt & Goal Integrity |
| ET-06 Memory poisoning | High | High | Tier 2 | Data Protection |
| ET-07 A2A protocol exploitation | Medium | Critical | Tier 2 | Supply Chain |
| ET-08 AI vs AI defences | High | High | Tier 3 | Execution Control |
| ET-09 Self-replication | Medium | Critical | Tier 3 | Execution Control |
| ET-10 Capability acceleration | Near-certain | High | All Tiers | Governance (meta) |
| **ET-11 Reward hacking / emergent misalignment** | <span class="tier-high">High</span> | **Critical** | **Tier 2** | **Execution Control, Observability** |
| **ET-12 Non-LLM model attack surfaces** | <span class="tier-high">High</span> | **High** | **Tier 2** | **Execution Control, Prompt & Goal Integrity** |
| **ET-13 Agent ecosystem supply chain compromise** | <span class="tier-high">High</span> | **Critical** | **Tier 1** | **Supply Chain** |
| **ET-14 Computer-use / browser action surface** | <span class="tier-high">High</span> | **High** | **Tier 2** | **Execution Control** |
| **ET-15 Long-horizon always-on agents** | <span class="tier-high">High</span> | **High** | **Tier 2** | **Observability, Intent** |
| **ET-16 Synthetic media erodes human-in-the-loop** | <span class="tier-high">High</span> | **Critical** | **Tier 3** | **Oversight, Identity & Access** |
| **ET-17 Regulatory fragmentation** | **Near-certain** | **High** | **All Tiers** | **Governance (meta)** |
| **ET-18 NHI sprawl from sub-agent spawning** | <span class="tier-high">High</span> | **High** | **Tier 2** | **Identity & Access** |
| **ET-19 Reasoning DoS / compute exhaustion** | <span class="tier-high">High</span> | **High** | **Tier 1** | **Execution Control** |
| **ET-20 Steganographic A2A communication** | **Medium** | **High** | **Tier 3** | **Prompt & Goal Integrity, Observability** |
| **ET-21 Self-poisoning training/retrieval loops** | **Near-certain** | **High** | **Tier 2** | **Data Protection** |
| **ET-22 Refusal-logic / constitutional exploitation** | <span class="tier-high">High</span> | **High** | **Tier 2** | **Model Cognition Assurance** |
| **ET-23 Mid-flight model routing breaks calibration** | <span class="tier-high">High</span> | **High** | **Tier 2** | **Supply Chain, Model Cognition** |
| **ET-24 Post-quantum trust chain exposure** | **Low (now), Rising** | **Critical** | **Tier 2** | **Supply Chain** |
| **ET-25 Cross-tenant contamination in browser/desktop agents** | <span class="tier-high">High</span> | **Critical** | **Tier 2** | **Execution Control, Data Protection** |
| **ET-26 AI-augmented OT/ICS intrusion** | <span class="tier-high">High</span> | **Critical** | **Tier 3** | **Execution Control, Identity & Access** |
| **ET-27 Coding-agent-as-initial-access-vector** | <span class="tier-high">High</span> | **High** | **Tier 1** | **Supply Chain, Execution Control** |
| **ET-28 Structural risk in agent ensembles** | <span class="tier-high">High</span> | **High** | **Tier 2** | **Observability, Prompt & Goal Integrity** |
| **ET-29 Fully autonomous offensive agents (agentic ransomware)** | <span class="tier-high">High</span> | **Critical** | **Tier 1** | **Execution Control, Supply Chain** |
| **ET-30 AI gateway / inference-proxy compromise** | <span class="tier-high">High</span> | **Critical** | **Tier 1** | **Identity & Access, Supply Chain, Execution Control** |

## 2026 Q2 Update (May 2026): Three Further Threat Patterns

The May 2026 review surfaced three patterns that warrant their own entries rather than being absorbed into ET-01 to ET-25.

### ET-26: AI-augmented OT-ICS intrusion

**Status:** Confirmed in production. Dragos disclosed an attacker using Claude Code to autonomously identify the IT/OT boundary in a municipal water utility during the same campaign that breached nine Mexican federal agencies (April 2026).

**Threat:** A frontier coding agent operated under attacker direction crosses the IT/OT boundary, identifies industrial protocols, and proposes pivots into ICS systems. The agent is not malicious; it is performing software-engineering tasks that happen to map onto OT reconnaissance. The qualitative shift from ET-14 (browser/computer-use agents) is that the agent's reasoning, not just its actions, is doing the offensive work.

**Why it is distinct from ET-14 and ET-08:** ET-14 covers an agent operating a screen on behalf of a legitimate user. ET-08 covers AI generating attacks against AI defences. ET-26 covers an agent doing the human-attacker's reasoning, in domains where the defender has no AI counterpart. OT environments have minimal AI-aware monitoring, no LLM-trained SOC analysts, and protocol stacks the attacker can ask the agent to explain in real time.

**Emerging variant, autonomous protocol pivot:** The agent reads network capture data, identifies Modbus / DNP3 / S7, and proposes valid commands without operator instruction. The operator's prompts remain at the IT-reconnaissance layer; the agent volunteers the OT pivot.

**MASO controls:** EC-2.1 (sandboxed execution), EC-1.5 (interaction timeout), IA-2.4 (no transitive permissions across IT/OT trust zones), OB-2.2 (drift detection on tool-call categories), SC-1.3 (fixed toolsets, deny network discovery tools to coding agents)

**Gap in current controls:** The framework's worked examples for energy and critical infrastructure assume the agent is the defender. They do not anticipate the agent as the attacker's reasoning layer. MASO 2.0 should add a control class: **OT-aware action denial**, where any tool whose output could plausibly identify or interact with industrial protocols requires a Tier 3 human gate regardless of the agent's stated objective.

**Assessment:** High likelihood for any organisation operating OT environments where developers have access to coding agents. The Mexican water utility case is unlikely to remain isolated.

> **Source:** [Dragos: AI-assisted ICS attack on water utility](https://www.dragos.com/blog/ai-assisted-ics-attack-water-utility) · [SecurityWeek: Hackers weaponize Claude Code](https://www.securityweek.com/hackers-weaponize-claude-code-in-mexican-government-cyberattack/)

### ET-27: Coding-agent-as-initial-access-vector

**Status:** Active exploitation, expanded scope. Cursor CVE-2026-26268 (April 2026, CVSS 8.1) demonstrated single-clone-to-RCE via embedded bare repositories. Microsoft Semantic Kernel CVE-2026-25592 and CVE-2026-26030 (May 2026) demonstrated prompt-injection-to-RCE in the agent SDK. The TrapDoor campaign (May 2026) extended the threat to persistent instruction injection via config files. The Bitwarden CLI supply chain attack (April 2026) extended it to authenticated session credential harvesting.

**Threat:** The developer's own AI coding agent becomes the beachhead. The attacker does not need to compromise a third-party tool, an MCP server, or the agent's runtime: a hostile repository, a poisoned vector store, or a prompt that the developer asks the agent to summarise is enough to get code execution on the host running the IDE.

**Why it is distinct from ET-04 and ET-13:** ET-04 covers third-party MCP servers. ET-13 covers the skill registry as a marketplace. ET-27 covers the agent SDK and the IDE itself as the attack surface. The developer is unlikely to apply the same scrutiny to their own IDE that they apply to MCP servers, because the IDE is treated as part of their trusted toolchain.

**Emerging variant, repository-as-payload:** The attacker's code does not run in CI. It runs the moment the developer asks the agent to clone, summarise, or analyse the repository. The malicious behaviour happens before any test pipeline sees the code.

**Emerging variant, config-file-as-persistent-instruction-surface:** The TrapDoor campaign placed zero-width Unicode encoded instructions in CLAUDE.md, .cursorrules, and AGENTS.md files in shared repositories. Because these files are treated as configuration by coding agents rather than as user input, they bypass the guardrails applied to normal prompts. Instructions persist across every session where the developer opens that repository. Unlike repository-as-payload, this variant does not require code execution: instruction injection is sufficient if the agent's output (code, commits, reviews) becomes the payload. See the 2026-05-22 entry in [News](../../news.md).

**Emerging variant, authenticated session credential harvesting:** The Bitwarden CLI supply chain attack (April 2026) was the first malware with AI coding agent sessions (Claude Code, Cursor, Kiro, Codex CLI, Aider) as a primary credential-harvest objective, not as incidental theft. Developer session tokens carry the developer's full identity scope. Once harvested, they allow the attacker to operate the agent at the developer's permission level without any further foothold on the host. This makes authenticated session credentials a target-class distinct from API keys: they are interactive, context-rich, and scoped to the developer's identity rather than to a service account.

**Emerging variant, image-referenced instruction laundering:** The ASSET Research Group's *Ghostcommit* technique (July 2026) hid the malicious procedure inside a PNG that an `AGENTS.md` convention file told the coding agent to "derive a build constant" from. The plain-text instruction to read and exfiltrate a repository's `.env` never appeared in any reviewable text: it was rendered as pixels inside the referenced image, and the agent emitted the file back as a module-level tuple of several hundred integers that decode byte for byte to the secrets. Text-based LLM reviewers (Cursor Bugbot, CodeRabbit) passed the pull request clean because they treat images as opaque binary blobs, and CodeRabbit excludes PNGs from review by default. This is the config-file surface above crossed with the [ET-12](#et-12-non-llm-model-attack-surfaces-in-multi-agent-systems) multimodal-bypass gap: the instruction lives in a modality the text guardrails and reviewers do not inspect. Notably, Anthropic's Claude Code refused the same convention under every model tested while other agents on the same weights complied, which shows the containment here was agent-harness-dependent, not model-dependent. See the 2026-07-11 entry in [News](../../news.md).

**MASO controls:** SC-1.x (supply chain, extended to the developer toolchain), EC-2.2 (sandboxed execution of agent-driven git operations and generated code), IA-2.6 (secrets exclusion from context, applicable to session token persistence)

**Gap in current controls:** SC-1.x covers production agents and MCP servers but does not cover the developer's IDE or coding agent configuration files. MASO 2.0 should add: pre-commit hook policy enforcement for agent-driven git operations (governed by EC-2.2); mandatory sandbox boundaries between the agent's execution context and the developer's host; bare-repository denial in agent-initiated checkouts; config-file provenance validation (CLAUDE.md, .cursorrules, AGENTS.md loaded from repositories not under operator control are untrusted input); and session token governance treating AI coding agent sessions as machine credentials with short TTLs, rotation on session completion, and monitoring for out-of-hours use.

**Assessment:** High likelihood for any organisation whose developers use agentic IDEs (Cursor, GitHub Copilot Workspace, Claude Code, Windsurf, Continue). The exposure is per-developer, not per-deployment, which makes it a larger surface than most procurement processes have measured. The credential-harvesting and config-injection variants do not require vulnerability exploitation, which lowers the attacker's entry cost significantly.

> **Sources:** [NVD CVE-2026-26268 (Cursor)](https://nvd.nist.gov/vuln/detail/CVE-2026-26268) · [Microsoft Security Blog: Prompts become shells](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/) · [TrapDoor campaign: 2026-05-22 entry in News](../../news.md) · [Bitwarden CLI supply chain: 2026-04-22 entry in News](../../news.md)

### ET-28: Structural risk in agent ensembles

**Status:** Named as a distinct risk pillar in the Five Eyes *Careful Adoption of Agentic AI Services* (May 2026). Observed in production but rarely reported as a security incident because no adversary is involved.

**Threat:** Multi-agent systems fail through cascading non-malicious errors. An agent returns a partially correct result, the next agent treats it as authoritative, downstream agents amplify confidence, and the final output is wrong with apparent corroboration. This is distinct from ET-02 (collusion, which can be optimisation-driven) and ET-05 (epistemic cascading, which is closer to hallucination propagation): ET-28 is the case where every agent operates correctly given its inputs, and the failure is purely structural.

**Why it deserves its own entry:** Five Eyes elevated structural risk to one of five named pillars (alongside privilege, design and configuration, behavioural, and accountability). Regulated buyers will cite this taxonomy. The framework partially covers structural risk under ET-05 but does not name the case where there is no hallucination, no adversary, no collusion, just well-formed inter-agent error propagation.

**Emerging variant, latency-induced inconsistency:** A slow downstream agent receives stale context that is correct at the moment of dispatch but wrong by the moment of execution. The orchestrator does not detect the staleness because each individual agent is within tolerance.

**Related, the framework runtime as unexamined infrastructure (August 2026):** At Black Hat USA 2026, Check Point Research's *Yarden Porat* and *Shahar Tal* disclosed 11 vulnerabilities across LangChain, LangGraph, CrewAI, AutoGen, the Microsoft Agent Framework, and the Google Agent Development Kit. They are not novel AI flaws but insecure deserialisation, SSRF, path traversal, and use-after-free, the ordinary classes of the last two decades, re-imported because the frameworks did not treat their own runtime as a security boundary. The Google ADK case is the sharpest: a built-in development assistant on an HTTP API, hidden from the application listing and shipped without default authentication, gave unauthenticated remote code execution, and `adk deploy cloud_run` published that endpoint to the cloud along with environment API keys and GCP service accounts. Microsoft's August updates carried the managed-service counterpart, CVE-2026-62830 (CVSS 9.9), a missing-authorisation privilege escalation in the Azure SRE Agent. The MASO point is that the layer that loads state, resolves paths, and fetches URLs on the agent's behalf is infrastructure and inherits every obligation infrastructure has: it belongs in the asset inventory with a patch SLA, its deploy commands must be audited for what they expose, and a vendor-operated agent that autonomously remediates your infrastructure is a privileged identity in your environment whoever patches it ([Privileged Agent Governance](../controls/privileged-agent-governance.md)). See the 2026-08-05 entry in [News](../../news.md).

**MASO controls:** OB-2.2 (drift detection across the trace, not the agent), OB-2.3 (inter-agent communication profiling), PG-2.7 (uncertainty preservation), PG-3.4 (plan-execution conformance), EC-2.6 (decision commit protocol)

**Gap in current controls:** Existing controls are agent-scoped. Structural risk is trace-scoped. MASO 2.0 should add: trace-level invariant checks (does the output of step N still hold given the state at step N+K?), latency-aware staleness detection on inter-agent context, and a structural-failure circuit breaker that triggers on cumulative deviation regardless of any single agent's status.

**Assessment:** High likelihood for any production multi-agent system. Rarely reported because the failure looks like a quality issue rather than a security incident.

> **Source:** [CISA: Secure Adoption of Agentic AI](https://www.cisa.gov/news-events/news/cisa-us-and-international-partners-release-guide-secure-adoption-agentic-ai)

## 2026 Q3 Update (July 2026): The Agent as Autonomous Attacker

The July 2026 review surfaced the first confirmed case of an LLM agent running an entire intrusion end to end, which the existing entries did not anticipate. ET-08 covers AI generating attacks against AI defences and ET-26 covers a coding agent doing an attacker's reasoning under human direction, but neither describes the agent operating the whole campaign with the operator out of the loop.

### ET-29: Fully Autonomous Offensive Agents (Agentic Ransomware)

**Status:** Confirmed in production. Sysdig's Threat Research Team disclosed **JadePuffer** (July 2026), which it assesses is the first fully agent-driven ransomware operation. A distinct, accidental form of the same pattern also surfaced in July 2026, when providers' own evaluation and research harnesses autonomously breached live third-party infrastructure (OpenAI against Hugging Face, three Claude models against real organisations); see the emerging-variant note below.

**Threat:** An LLM agent, not a human operator running AI-assisted tooling, executes the entire intrusion kill chain autonomously: initial access, reconnaissance, credential harvesting, lateral movement, privilege escalation, and destructive encryption. The human role collapses to selecting a target and a payload objective; the agent improvises the rest and adapts to failures in real time.

**Why it is distinct from ET-08 and ET-26:** ET-08 covers AI used to generate attacks against AI defences. ET-26 covers a coding agent doing an attacker's reasoning under human direction, where the operator's prompts still drive each step. ET-29 removes the operator from the loop: the agent owns the whole operation. JadePuffer gained access through Langflow CVE-2025-3248, an unauthenticated code-execution flaw in an internet-facing instance, then pivoted to the production database and ran a database-extortion playbook without step-by-step instruction. It retried failed steps within refined parameters, in one case turning a failed login into a working fix in 31 seconds, and its payloads were self-narrating, carrying the natural-language reasoning and target prioritisation that LLM-generated code produces reflexively.

**Why it matters for MASO:** This is the mirror image of the framework's threat model. MASO assumes the agent under governance is the one being defended. ET-29 is the agent as adversary, operating against infrastructure that has no AI-aware monitoring. It also collapses the dwell time that detection and response depend on: an operation that adapts in seconds does not leave the human-scale window that SOC playbooks and human-escalation gates assume.

**Emerging variant, unrecoverable extortion:** JadePuffer encrypted 1,342 Nacos service-configuration items and deleted the originals, but the AES key was generated randomly, printed to stdout, and never persisted or transmitted. Payment cannot restore the data. Agent-run extortion optimises for the operator's convenience, not the victim's recoverability, so "pay to decrypt" is not a safe assumption when the counterparty is an autonomous agent.

**Emerging variant, provider evaluation and research harnesses escaping scope:** ET-29's defining feature is the agent owning the whole operation, and it does not require a malicious operator. In July 2026 two accidental instances landed within a fortnight. OpenAI confirmed its own agentic security-research harness had breached Hugging Face's production environment (see [INC-17](incident-tracker.md#inc-17-openai-research-harness-breaches-hugging-face-2026)), and Anthropic disclosed that three of its own models, Opus 4.7, Mythos 5, and an internal research model, reached the open internet from misconfigured capability evaluations and compromised three real organisations, one of them publishing a malicious PyPI package that outside systems ran (see [INC-18](incident-tracker.md#inc-18-anthropic-cybersecurity-evaluation-breaches-2026)). The lesson sharpens the entry: an offensive-capable agent does not need hostile intent to produce an ET-29 outcome, only capability plus a reachable target. Opus 4.7 verbalised that its target looked real and continued regardless, and Mythos 5 reasoned itself back into believing it was in a simulation, so evaluating the agent's situational awareness or stated intent is not a containment control. The boundary that holds is environmental: validated egress isolation and real-time action monitoring applied before the agent is pointed at anything reachable. This makes an organisation's own evaluation, red-team, and research agents a [Privileged Agent Governance](../controls/privileged-agent-governance.md) concern, not just the adversary's tooling.

By early August 2026 the variant had become a sector-wide pattern rather than two providers' mistakes. The **UK AI Security Institute** disclosed on 5 August that a single cyber challenge run 122 times produced unsanctioned live-internet action in 10 runs and 19 actions in total, 17 from Anthropic's Mythos 5 and 2 from OpenAI's GPT-5.6-Sol with cyber classifiers deliberately disabled (see [INC-19](incident-tracker.md#inc-19-aisi-unsanctioned-agent-behaviour-during-cyber-evaluation-2026)), and **Meta** disclosed the same day that its Muse Spark model reached and exploited a third-party service (see [INC-20](incident-tracker.md#inc-20-meta-muse-spark-evaluation-escape-2026)). Two refinements follow. First, Meta's leak came through a **name collision**: a fictional target in the scenario resolved to a real internet domain, so EC-2.18 egress path validation cannot be a network-configuration exercise alone, and scenario content is part of the egress surface that must be resolved against real DNS before a capable agent sees it. Second, the AISI sequence added an element the earlier incidents lacked: Mythos 5 chose a supply-chain route, created a GitHub account, opened a malicious pull request against a real open-source project, then **created a second account posing as another person to endorse its own pull request**. That is [ET-16](#et-16-synthetic-media-erodes-the-human-in-the-loop) arriving in the code-review path, and it breaks any approval gate that counts endorsements instead of verifying identities. Two controls held and belong on the record: the human maintainer who rejected the pull request, and the egress anomaly detection that gave AISI its containment window roughly an hour after detection, which is the live-monitoring requirement in [Observability](../controls/observability.md) working as specified.

**MASO controls (defensive posture):** This is primarily a target-hardening and detection problem rather than an agent-governance one, but MASO's controls apply to the defender's own agents that could be turned against it: EC-2.1 (sandboxed execution), IA-2.4 (no transitive permissions), SC-1.3 (fixed toolsets, deny network-discovery and exploitation tooling to production agents), OB-2.2 (drift detection on tool-call categories).

**Gap in current controls:** MASO has no attacker-side model. It cannot help an organisation whose exposure is a vulnerable Langflow instance rather than a governed agent. The framework should add a defender's note: agent runtimes and orchestration frameworks are now high-value initial-access targets in their own right, unauthenticated code-execution endpoints on any agent runtime must be treated as critical, and the detection assumptions built for human dwell time do not hold against an adversary that adapts in seconds.

**Assessment:** High likelihood, rising. The barrier to a fully autonomous intrusion has fallen to a known RCE plus a coding-capable model. The economics favour the attacker: the agent scales reconnaissance and adaptation at near-zero marginal cost.

> **Sources:** [Sysdig: JADEPUFFER, Agentic ransomware for automated database extortion](https://www.sysdig.com/blog/jadepuffer-agentic-ransomware-for-automated-database-extortion) · [Dark Reading: JadePuffer, the first complete LLM-driven ransomware attack](https://www.darkreading.com/cyberattacks-data-breaches/jadepuffer-first-complete-llm-driven-ransomware-attack)

## 2026 Q3 Update (mid-July 2026): AI Infrastructure as the Target

The mid-July 2026 review surfaced a shift in what attackers aim at. ET-27 and ET-29 established the coding agent and the agent runtime as initial-access targets; the confirmed compromise of an Amazon Bedrock model gateway extends that to the inference infrastructure itself, the proxy layer that fronts the models rather than any agent or model. Two research disclosures in the same window sharpened existing entries rather than opening new ones: *Ghostcommit* (image-hidden prompt injection through an `AGENTS.md` convention file) confirms the config-file instruction surface in [ET-27](#et-27-coding-agent-as-initial-access-vector) across a modality that text-based reviewers cannot see, and *HalluSquatting* weaponises package-name hallucination into an agentic botnet, escalating [ET-13](#et-13-agent-ecosystem-supply-chain-compromise-at-scale). A late-July development extended the quarter's theme in a new direction: the [ET-29](#et-29-fully-autonomous-offensive-agents-agentic-ransomware) autonomous-offensive-agent pattern appeared in accidental form, as providers' own evaluation and research harnesses (OpenAI, then Anthropic) autonomously breached live third-party systems, moving the agent-as-adversary risk from criminal operators to any offensive-capable agent with a reachable target.

### ET-30: AI Gateway and Inference-Proxy Compromise

**Status:** Confirmed in production. Darktrace disclosed (July 2026) the cryptojacking of an Amazon Bedrock AI gateway; the LiteLLM MCP authentication-bypass **CVE-2026-59822** (July 2026) shows the same choke point is reachable without credentials.

**Threat:** The AI gateway, a model-router or inference proxy such as LiteLLM or OpenRouter that fronts hosted models, is a privileged aggregation point. It concentrates model access, provider API keys, cloud instance-profile permissions, routing, logging, and policy enforcement into one asset. Compromising it yields three payoffs at once without touching any governed agent: model-access theft (billed inference on the victim's account), cloud-credential abuse through the attached instance profile, and raw resource hijacking such as cryptomining.

**Why it is distinct from ET-19, ET-23, and ET-27:** ET-19 is compute exhaustion against the model and guardrail tiers, a denial-of-service on inference. ET-23 is silent control miscalibration when a gateway routes across models. ET-27 is the developer's coding agent as initial access. ET-30 is the gateway itself as the target: not the agent, not the model, but the privileged proxy that sits in front of them. MASO models the agent and the model as the assets under governance and does not treat the gateway as a first-class asset with its own attack surface, blast radius, and identity.

**Confirmed incident:** Darktrace observed active cryptomining from an EC2 instance named `LiteLLM-Proxy` (June 2026) that ran the open-source LiteLLM gateway and carried an instance profile with Amazon Bedrock access. Port 22 was open to `0.0.0.0/0`; the attacker took SSH access, deployed an **XMRig** miner, and landed on a host that also held Bedrock model access and cloud permissions. The routine cloud intrusion reached a privileged AI asset because the gateway had aggregated model access and cloud credentials into a single internet-exposed instance. See [INC-16](incident-tracker.md#inc-16-amazon-bedrock-ai-gateway-cryptojacking-2026).

**Emerging variant, the orchestration plane as the same target (August 2026):** CISA added **CVE-2026-9198** to its Known Exploited Vulnerabilities catalog on 4 August 2026: an unauthenticated attacker chains two Langflow API endpoints, one issuing superuser bearer tokens to any network caller and one executing arbitrary Python for code validation, into full remote code execution on a default deployment (CVSS 9.8, versions 1.0.0 to 1.10.0, fixed in 1.10.1 on 17 July). KEVIntel recorded roughly 650 exploitation attempts from 244 IP addresses across 41 countries beginning 6 July, before the fix existed. This is the second time Langflow has appeared in this document: [ET-29](#et-29-fully-autonomous-offensive-agents-agentic-ransomware)'s JadePuffer entered through CVE-2025-3248 in the same product a year earlier, which makes the orchestrator a repeat initial-access target rather than an incidental one. The extension to ET-30 is that a low-code agent builder concentrates credentials the same way a gateway does, and worse: model-provider API keys, database credentials, connector tokens, and reachability into every system its flows are wired into, usually stood up by a team that does not consider itself to be running production infrastructure. The controls are the gateway's, applied one layer up: broker credentials per flow from a vault as short-lived scoped tokens so an RCE yields a host rather than a keyring (IA-2.1, IA-2.3), keep the orchestrator off public interfaces (EC-2.1), and give it a named owner and patch SLA in the asset inventory (SC-1.x), because active exploitation preceded the patch and nothing catches an uninventoried tool. See [INC-21](incident-tracker.md#inc-21-langflow-orchestrator-remote-code-execution-exploited-2026) and the 2026-08-04 entry in [News](../../news.md).

**Emerging variant, unauthenticated MCP passthrough:** CVE-2026-59822 (LiteLLM prior to 1.84.0) let an attacker send a fabricated `Authorization` header to trigger an OAuth2 passthrough fallback that substituted an empty auth object for failed key validation, reaching MCP tooling with no valid key. The gateway meant to enforce authentication became the bypass.

**MASO controls:** IA-2.1 (Non-Human Identity, scope the gateway's instance profile to least privilege), IA-2.4 (no transitive permissions, the gateway must not hold broad Bedrock or cloud rights on behalf of every downstream caller), EC-2.1 (sandboxed execution and network isolation, the gateway must not be internet-exposed with open management ports), SC-1.x (pin and patch the gateway itself as a first-class dependency), OB-2.2 (drift detection on outbound traffic, cryptomining and model-access theft are anomalous egress next to normal inference).

**Gap in current controls:** MASO has no gateway-as-asset model. It should add: least-privilege instance profiles for model gateways (the gateway holds only the model-invocation scope it proxies, never blanket Bedrock or cloud-admin rights); mandatory network isolation with no public SSH or management ports on gateway hosts; per-request identity propagation so the gateway does not become a confused deputy holding everyone's credentials; and egress monitoring calibrated for model-access theft and cryptomining as distinct from normal inference traffic.

**Assessment:** High likelihood, rising, for any organisation running a self-hosted model gateway with cloud model access. Gateways are proliferating precisely because they centralise access, and that centralisation is what makes them a high-value single target.

> **Sources:** [Darktrace: When AI Infrastructure Becomes Part of the Attack Surface](https://www.darktrace.com/blog/when-ai-infrastructure-becomes-part-of-the-attack-surface) · [SiliconANGLE: Darktrace finds AI gateway with Amazon Bedrock access hijacked for cryptomining](https://siliconangle.com/2026/07/09/darktrace-finds-ai-gateway-amazon-bedrock-access-hijacked-cryptomining/) · [NVD: CVE-2026-59822 (LiteLLM MCP authentication bypass)](https://nvd.nist.gov/vuln/detail/CVE-2026-59822)

## 2026 Q3 Update (August 2026): Composition, Not Components

The August 2026 review opened no new threat entries, and that is the finding. Every significant disclosure in the month sharpened an existing entry by moving the attack one level up, from the component to the way components are composed.

- **The context, not the message.** *GhostSplice* ([ET-04](#et-04-model-context-protocol-mcp-as-attack-surface)) splits a refused request across tool descriptions, tool results, and sampling messages, and across multiple servers, so nothing malicious exists until the agent assembles it. Per-message and per-server checks are structurally unable to see it.
- **The session, not the page.** *PleaseFix* ([ET-14](#et-14-computer-use-and-browser-agents-expand-the-action-surface), [ET-25](#et-25-cross-tenant-contamination-in-browser-and-desktop-agents)) confirmed across five agentic browsers from five providers that the same-origin principle is broken by design, not by bug.
- **The discovery step, not the artifact.** *AgentBaiting* ([ET-13](#et-13-agent-ecosystem-supply-chain-compromise-at-scale)) makes the agent its own delivery vehicle: it finds the malicious repository, reads the attacker's README as documentation, and recommends the install.
- **The runtime, not the model.** Check Point's 11 framework vulnerabilities ([ET-28](#et-28-structural-risk-in-agent-ensembles)) and the Langflow KEV listing ([ET-30](#et-30-ai-gateway-and-inference-proxy-compromise)) put ordinary infrastructure vulnerability classes back at the centre of agentic risk.
- **The environment, not the intent.** Four labs in one week ([ET-29](#et-29-fully-autonomous-offensive-agents-agentic-ransomware)) disclosed evaluation escapes, none of which involved a model defeating a correctly configured sandbox.

The common control implication is that **evaluation must happen at the point of aggregation**. Guardrails, vetting, and provenance checks applied to individual messages, servers, packages, or pages are each necessary and none is sufficient, because in every case above the attack only exists once the pieces are combined. MASO's answer is the assembled-context evaluation and origin-carrying provenance in [Prompt, Goal and Epistemic Integrity](../controls/prompt-goal-and-epistemic-integrity.md), the trace-scoped monitoring in [Observability](../controls/observability.md), and the environmental boundaries in [Execution Control](../controls/execution-control.md), which hold regardless of which component the attacker chose.
