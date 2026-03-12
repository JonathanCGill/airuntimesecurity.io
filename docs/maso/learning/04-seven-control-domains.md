# Module 4: The Seven Control Domains

**What each domain protects and why it matters.**

## Overview

MASO organizes 128 controls into seven domains. Each domain addresses a distinct threat surface in multi-agent systems. Together, they provide comprehensive coverage mapped to both OWASP threat taxonomies (LLM Top 10 and Agentic Top 10).

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   0. Prompt, Goal & Epistemic Integrity                    │
│      Protect what agents think and believe                 │
│                                                            │
│   1. Identity & Access                                     │
│      Control who agents are and what they can reach        │
│                                                            │
│   2. Data Protection                                       │
│      Fence what agents can see and share                   │
│                                                            │
│   3. Execution Control                                     │
│      Bound what agents can do and how much damage they     │
│      can cause                                             │
│                                                            │
│   4. Observability                                         │
│      See what agents are doing and detect drift            │
│                                                            │
│   5. Supply Chain                                          │
│      Verify where agents and their components come from    │
│                                                            │
│   6. Privileged Agent Governance                           │
│      Apply elevated controls to agents with elevated power │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Domain 0: Prompt, Goal & Epistemic Integrity

**Protects:** The trustworthiness of agent instructions, objectives, and information chains.

This is the cross-cutting domain. It addresses both adversarial threats (prompt injection, goal hijacking) and epistemic threats (hallucination amplification, groupthink, semantic drift) — the latter having no OWASP equivalent.

**Key controls:**
- Input sanitisation on all channels — not just user-facing, but inter-agent messages, tool outputs, and RAG results
- System prompt isolation prevents cross-agent extraction
- Immutable task specifications with continuous goal integrity monitoring
- Epistemic controls: consensus diversity gates, claim provenance enforcement, uncertainty preservation, self-referential evidence prohibition

**Why it matters for multi-agent systems:** A prompt injection in a single-agent system affects one model's context. In a multi-agent system, a poisoned document processed by one agent becomes instructions to another. And epistemic failures — agents reinforcing each other's mistakes without any attacker present — are unique to multi-agent systems.

**OWASP coverage:** LLM01 (Prompt Injection), LLM07 (System Prompt Leakage), ASI01 (Agent Goal Hijack), plus nine epistemic risks (EP-01 through EP-09).

## Domain 1: Identity & Access

**Protects:** Agent identity boundaries and permission scope.

**Key controls:**
- Every agent gets a unique Non-Human Identity (NHI) — not a shared service account
- No credential sharing between agents
- No inherited permissions from the orchestrator
- Short-lived, scoped credentials with automatic rotation
- Zero-trust mutual authentication on the inter-agent message bus

**Why it matters for multi-agent systems:** In single-agent systems, the model operates with the application's identity. In multi-agent systems, delegation creates transitive authority chains. If the orchestrator delegates to Agent B using its own credentials, Agent B effectively has the orchestrator's permissions. NHI prevents this by ensuring each agent authenticates and is authorized independently.

**The principle:** No delegation chain can accumulate permissions beyond what any individual agent holds. Separate "request," "approve," and "execute" roles.

**OWASP coverage:** ASI03 (Identity & Privilege Abuse), ASI07 (Insecure Inter-Agent Communication), LLM06 (Excessive Agency).

## Domain 2: Data Protection

**Protects:** Data boundaries between agents and data integrity across the system.

**Key controls:**
- Cross-agent data fencing: agents operating at different classification levels cannot freely share data
- DLP scanning on inter-agent communications (not just external outputs)
- RAG integrity validation with freshness checks
- Memory poisoning detection — flag inconsistencies between stored context and expected state
- Session-isolated memory per agent with decay policies

**Why it matters for multi-agent systems:** Delegation creates implicit data flows. When Agent A asks Agent B to perform a task, Agent A's data context may flow to Agent B without anyone designing that data path. Data classification boundaries that work for single-agent systems break when agents share information freely through a message bus.

**OWASP coverage:** LLM02 (Sensitive Information Disclosure), LLM04 (Data and Model Poisoning), ASI06 (Memory & Context Poisoning), LLM08 (Vector and Embedding Weaknesses).

## Domain 3: Execution Control

**Protects:** The scope and impact of what agents can do.

**Key controls:**
- Sandboxed execution for all tool invocations with strict parameter allow-lists
- Blast radius caps: maximum records modifiable, maximum financial value, maximum API calls per agent
- Circuit breakers triggering on error rate thresholds
- Time-boxing: maximum execution duration per agent and per task
- Code execution isolation with filesystem, network, and process scope containment

**Why it matters for multi-agent systems:** A single agent with excessive permissions is a risk. An agent chain where permissions compound through delegation is a systemic risk. Execution control ensures that even if an agent is compromised, the damage it can do is bounded — not just by its permissions, but by infrastructure-enforced limits on its impact.

**The principle:** Every action has a blast radius cap. The cap is enforced by infrastructure, not by the agent's good judgment.

**OWASP coverage:** ASI02 (Tool Misuse), ASI05 (Unexpected Code Execution), ASI08 (Cascading Failures), LLM05 (Improper Output Handling).

## Domain 4: Observability

**Protects:** Visibility into agent behavior for detection, forensics, and compliance.

**Key controls:**
- Immutable decision chain logs capturing the full reasoning and action history of every agent
- Behavioral drift detection comparing current behavior against established baselines
- Per-agent anomaly scoring feeding into PACE escalation logic
- SIEM and SOAR integration for correlation with broader security operations
- Decision traceability for regulated decisions

**Why it matters for multi-agent systems:** When something goes wrong in a multi-agent system, you need to reconstruct the entire chain: which agent produced the bad output, which agents consumed it, what decisions were made based on it, and how it affected the final result. Without immutable per-agent logs with full provenance, this forensic reconstruction is impossible.

**The principle:** If you cannot explain what happened and why, you cannot govern the system. Observability is not optional.

**OWASP coverage:** ASI09 (Human-Agent Trust Exploitation), ASI10 (Rogue Agents), LLM09 (Misinformation), LLM10 (Unbounded Consumption).

## Domain 5: Supply Chain

**Protects:** The provenance and integrity of models, tools, and components in the agent system.

**Key controls:**
- AI Bill of Materials (AIBOM) generation for every model in the system
- MCP server vetting with signed manifests and runtime integrity checks
- A2A trust chain validation for inter-agent protocol endpoints
- Model version pinning with provenance tracking
- Continuous vulnerability scanning of the agent toolchain

**Why it matters for multi-agent systems:** A single-agent system has one model and a set of tools. A multi-agent system may use models from multiple providers, dozens of MCP servers, and a complex graph of tool integrations. Each is an entry point. A poisoned MCP server component, a compromised model update, or a tampered tool descriptor can affect every agent that uses it.

**OWASP coverage:** LLM03 (Supply Chain Vulnerabilities), ASI04 (Agentic Supply Chain).

## Domain 6: Privileged Agent Governance

**Protects:** Against the disproportionate risk posed by orchestrators, planners, and meta-agents.

Not all agents are equal. Orchestrators can create agents, assign tasks, allocate resources, and modify workflows. Planners can define what other agents do. Meta-agents can change the system's configuration. These privileged agents require elevated controls.

**Key controls:**
- Mandatory human approval gates for privileged actions
- Authority delegation limits — how much of its authority a privileged agent can delegate
- Audit trails for every exercise of privilege
- Independent monitoring that the privileged agent cannot influence
- No self-modification: a privileged agent cannot change its own permissions or monitoring

**Why it matters for multi-agent systems:** If the orchestrator is compromised, every downstream agent is at risk. If the planner is manipulated, every subsequent action follows the manipulated plan. Privileged agents are single points of leverage — and therefore require the strongest controls.

**OWASP coverage:** ASI03, ASI07, LLM06 (elevated controls for high-authority agents).

## How the Domains Interact

The domains are not independent silos. They reinforce each other:

- **Identity & Access** determines what each agent can reach. **Execution Control** limits what it can do with that access. **Observability** records what it actually did.
- **Prompt & Epistemic Integrity** protects the quality of information. **Data Protection** protects its boundaries. **Observability** tracks its flow.
- **Supply Chain** verifies the components. **Privileged Agent Governance** controls who can change them. **Execution Control** sandboxes their operation.

When designing your control set, think about these interactions. A gap in one domain may be compensated by controls in another — or it may create a blind spot that compounds across domains.

---

**Next:** [Module 5: Emergent Risks](05-emergent-risks.md)
