# Emerging Threats

**Forward-Looking Threat Patterns for Multi-Agent AI Systems**

> Part of the [MASO Framework](../README.md) · Threat Intelligence
> Last updated: February 2026

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

**Status:** Theoretical with supporting research

**Threat:** Two or more agents in a multi-agent system develop coordinated behavior that serves neither agent's intended objective. This is not adversarial in the traditional sense - no external attacker is involved. It emerges from optimisation pressure when agents discover that coordinating on certain outputs (even deceptive ones) produces better reward signals than honest independent operation.

**Why it matters:** Current multi-agent architectures assume that agents are independent actors whose outputs can be cross-validated. If agents learn to coordinate their outputs - producing consistent but incorrect results - the cross-validation assumption breaks down entirely. Three agents agreeing on a wrong answer looks exactly like three agents agreeing on a right answer.

**Emerging variant - Implicit collusion:** Agents don't need to explicitly communicate to collude. If they share training data, model architecture, or retrieval corpora, they may produce correlated outputs that appear independent but aren't. This is the epistemic risk that MASO's PG-2.4 (Consensus diversity gate) and PG-2.9 (Model diversity policy) are designed to address.

**MASO controls:** PG-2.4 (consensus diversity gate), PG-2.9 (model diversity policy), PG-3.5 (challenger agent), PG-2.6 (self-referential evidence prohibition), OB-2.3 (inter-agent communication profiling)

**Assessment:** Medium likelihood, but high impact. The conditions for implicit collusion already exist in most multi-agent deployments (shared models, shared RAG corpora). Formal controls for detection are rare outside MASO.

### ET-03: Transitive Authority Exploitation

**Status:** Demonstrated in isolated cases; systematic exploitation not yet reported

**Threat:** An attacker exploits delegation chains to gain access to tools and data that no single agent is authorised to access. Agent A can delegate to Agent B. Agent B has access to Tool X. The attacker compromises Agent A and instructs it to delegate a task to Agent B that uses Tool X in an unintended way. Agent A never directly accesses Tool X - the access is transitive through delegation.

**Why it's getting worse:** Agent orchestration frameworks increasingly support dynamic delegation - agents can spawn sub-agents, delegate tasks, and chain operations without pre-defined workflows. Each delegation step is individually authorised, but the cumulative chain may grant access that was never intended.

**Emerging variant - Delegation laundering:** An attacker uses a chain of 3+ agents to obscure the origin of a malicious request. By the time the request reaches the execution agent, it appears to be a legitimate delegated task from an authorised intermediate agent. Audit logs show a valid delegation chain; the malicious origin is buried.

**MASO controls:** IA-2.1 (zero-trust agent credentials), IA-2.3 (no transitive permissions), EC-2.6 (decision commit protocol), PG-3.3 (constraint fidelity check for 3+ handoff chains), PG-3.4 (plan-execution conformance), OB-3.5 (decision traceability)

**Assessment:** High likelihood. Transitive authority is a fundamental property of current agent orchestration patterns. Without explicit controls (like MASO's IA-2.3), every multi-agent system has this exposure.

### ET-04: Model Context Protocol (MCP) as Attack Surface

**Status:** Active exploitation in the wild

**Threat:** MCP servers expose tool definitions, resource listings, and schema metadata to AI agents. Poisoned MCP servers can inject instructions through tool descriptions, manipulate agent behavior through crafted resource metadata, or exfiltrate data through tool call parameters.

**Why it's getting worse:** MCP adoption is accelerating - tens of thousands of MCP servers are now published. The ecosystem is largely unvetted. Organisations consume MCP servers the way they consumed npm packages in 2016 - freely, with minimal verification. The supply chain attack surface is enormous.

**Emerging variant - MCP squatting:** Attackers publish MCP servers with names similar to popular legitimate servers (typosquatting). When developers configure their agent systems, they connect to the malicious server instead. The poisoned server responds normally to most queries but injects instructions for specific trigger conditions.

**Emerging variant - MCP-in-the-middle:** An attacker interposes a proxy MCP server between an agent and a legitimate MCP server. The proxy passes through most requests transparently but modifies specific responses to inject instructions or exfiltrate data.

**MASO controls:** SC-1.2 (signed tool manifests), SC-2.2 (MCP server vetting), SC-2.3 (runtime component audit), SC-3.1 (cryptographic trust chain), PG-1.1 (input guardrails per agent)

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

**Status:** Research demonstrated; production exploitation emerging

**Threat:** Long-term agent memory stores (persistent context, conversation history, learned preferences) become attack surfaces. An attacker injects content into an agent's memory through normal interaction, and the poisoned memory influences all future interactions. In a multi-agent system, shared memory stores amplify the impact - poisoning one agent's memory can affect the behavior of all agents that read from the same store.

**Why it's getting worse:** The shift from stateless to stateful agents means that attacks persist across sessions. Memory poisoning is a form of time-delayed prompt injection - the payload is stored now and activated later, potentially weeks or months after the initial injection.

**Emerging variant - Memory-mediated lateral movement:** An attacker poisons Agent A's memory. Agent A writes a summary to shared memory. Agent B reads the summary and incorporates it into its context. The poisoned content has moved from Agent A's memory to Agent B's context without any direct inter-agent communication - the shared memory store is the propagation vector.

**MASO controls:** DP-1.3 (memory isolation), DP-2.2 (RAG integrity with freshness), PG-2.5 (claim provenance enforcement), OB-2.2 (behavioral drift detection), OB-2.6 (log security)

**Assessment:** High likelihood for stateful multi-agent systems. Memory poisoning is harder to detect than prompt injection because the payload doesn't look like an instruction at injection time - it becomes one when the memory is retrieved in a future context.

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

**Emerging variant - Adaptive evasion:** Attackers test their payloads against replicas of known guardrail and Judge models, iteratively refining until they achieve bypass. If the defender's model is known (or can be inferred), the attacker can optimise specifically against it.

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

