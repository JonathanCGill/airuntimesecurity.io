# Module 2: The Three-Layer Defence

**Guardrails, LLM-as-Judge, and Human Oversight — how they work together to secure multi-agent systems.**

## Why Three Layers

No single security mechanism can catch everything. Deterministic rules miss novel attacks. AI-based evaluation can be fooled. Humans cannot review every transaction. The three-layer model combines their strengths while compensating for their individual weaknesses.

The critical design principle: **each layer depends on a different mechanism**, so a single failure mode cannot cascade through all of them.

```
┌─────────────────────────────────────────────────────┐
│                   Input / Action                     │
├─────────────────────────────────────────────────────┤
│  Layer 1: GUARDRAILS              (~10ms)           │
│  Deterministic · Pattern matching · Rule-based      │
│  Block known-bad · Enforce hard boundaries          │
├─────────────────────────────────────────────────────┤
│  Layer 2: LLM-AS-JUDGE            (~500ms–5s)       │
│  Probabilistic · Semantic analysis · Independent    │
│  Assess unknown-bad · Evaluate quality & safety     │
├─────────────────────────────────────────────────────┤
│  Layer 3: HUMAN OVERSIGHT          (As needed)      │
│  Cognitive · Contextual judgment · Final authority   │
│  Decide ambiguous cases · Approve high-risk actions │
├─────────────────────────────────────────────────────┤
│  CIRCUIT BREAKER                   (Emergency)      │
│  Infrastructure-level · Stops all AI traffic        │
│  Activates when controls fail or compromise confirmed│
└─────────────────────────────────────────────────────┘
```

## Layer 1: Guardrails

**Purpose:** Block known-bad inputs and outputs at machine speed.

Guardrails are deterministic — they apply rules, regex patterns, and allow/deny lists without interpretation. They are fast, predictable, and non-negotiable.

**What guardrails do in multi-agent systems:**

| Function | Single-Agent | Multi-Agent Extension |
|----------|-------------|----------------------|
| Input validation | User input | User input + inter-agent messages + tool outputs + RAG results |
| Output sanitisation | Model output to user | Model output to user + output to other agents via message bus |
| Content policy | Topic blocking, PII detection | Same, applied at every agent boundary |
| Rate limiting | Per-user, per-session | Per-agent, per-delegation chain |
| Tool permissions | Allow-list of tools | Per-agent tool allow-lists with no transitive inheritance |

**Key multi-agent principle:** Guardrails must run at every agent boundary, not just at the system's external interfaces. An inter-agent message is an untrusted input.

**Guardrails do not:**
- Evaluate whether an output is *correct* or *helpful*
- Detect novel attack patterns that don't match known signatures
- Make judgment calls about ambiguous content

That is what the next layer is for.

## Layer 2: LLM-as-Judge

**Purpose:** Detect what guardrails miss through semantic understanding.

The Judge is a separate LLM instance — distinct from the task agents — that evaluates the quality, safety, and policy compliance of agent actions and outputs. It catches the *unknown-bad*: outputs that are technically well-formed but semantically harmful, inaccurate, or policy-violating.

**What the Judge evaluates in multi-agent systems:**

| Evaluation | What It Checks |
|-----------|---------------|
| Output quality | Accuracy, completeness, relevance |
| Safety compliance | Harmful content, manipulation, coercion |
| Goal integrity | Is the agent still working toward its assigned objective? |
| Inter-agent communication | Are messages between agents consistent with their roles? |
| Epistemic validity | Are claims supported by evidence? Is uncertainty preserved? |
| Plan conformance | Does execution match the approved plan? |

**Critical requirements for the Judge:**

1. **Independence.** The Judge must be a different model from the task agents. If all agents (including the Judge) are the same model from the same provider, their errors will be correlated, not independent.

2. **Cannot be overridden by agents.** The Judge's evaluation is final for its scope. An agent cannot argue its way past a Judge rejection.

3. **Evaluates inter-agent communication.** In multi-agent systems, the Judge does not only evaluate final outputs — it also reviews what agents say to each other, checking for injection propagation, goal drift, and unauthorized instructions.

**The Judge is not infallible.** It can be fooled by sophisticated adversarial inputs. It can make errors on edge cases. This is why the third layer exists.

## Layer 3: Human Oversight

**Purpose:** Apply cognitive judgment to genuinely ambiguous cases.

Human oversight is the governance backstop. Scope scales inversely with demonstrated trustworthiness and directly with consequence severity.

**When humans are involved depends on the implementation tier:**

| Tier | Human Role |
|------|-----------|
| Tier 1 (Supervised) | Approves all write operations |
| Tier 2 (Managed) | Approves high-consequence actions; reviews Judge escalations |
| Tier 3 (Autonomous) | Handles exceptions; reviews flagged patterns; strategic oversight |

**Multi-agent considerations for human oversight:**

- **Automation bias is amplified.** When multiple agents agree, humans are less likely to challenge the result. MASO addresses this through challenger agents and consensus diversity gates.
- **Volume scales with agent count.** More agents means more escalations. The framework addresses this through tiered evaluation (not everything needs human review) and structured escalation queues.
- **Challenge rate matters.** If human reviewers approve 100% of escalations, the oversight layer is not functioning. MASO tracks approval rates and uses canary tests to verify reviewer engagement.

## The Circuit Breaker

**Purpose:** Stop everything when controls have failed.

The circuit breaker operates at the infrastructure level — network routing, feature flags, kill switches — not at the prompt level. An agent cannot talk its way past a circuit breaker.

**Triggers:**
- Confirmed compromise or data exfiltration
- Cascading failures across multiple agents
- Multiple security layers simultaneously degraded
- Error rates exceeding defined thresholds

**Actions:**
- All agent sessions terminated
- Tool access revoked
- Memory and context snapshots preserved for forensics
- Non-AI fallback paths activated

## How the Layers Work Together

Consider an example: a multi-agent investment research system where Agent A collects data, Agent B analyses it, and Agent C compiles the report.

1. **Guardrails** validate every input and output at each agent boundary. They catch PII in the data feed, block tool calls outside each agent's allow-list, and enforce rate limits on API calls.

2. **LLM-as-Judge** evaluates Agent B's analysis for accuracy, checks that Agent C's report faithfully represents Agent B's findings (no semantic drift), and verifies that uncertainty signals from Agent A are preserved through the chain.

3. **Human Oversight** reviews the final report before it is sent to the client. For high-consequence recommendations, a human reviewer sees the full reasoning chain, including where each claim originated and what evidence supports it.

4. **Circuit Breaker** activates if Agent B starts producing outputs that diverge dramatically from its baseline behavior, indicating potential compromise or model degradation.

## Applying This to Your Solution

When designing a multi-agent system with MASO's three-layer defence:

**Design guardrails first.** They are the cheapest, fastest layer. Define what is definitively in-scope and out-of-scope for each agent. Enforce it with rules, not prompts.

**Deploy the Judge on inter-agent communication, not just final outputs.** The most dangerous failures in multi-agent systems happen between agents, not at the system boundary.

**Scale human oversight to consequence, not volume.** Not every action needs human review. Define which action classes require approval based on their blast radius (financial impact, data sensitivity, reversibility).

**Make the circuit breaker real.** It must be an infrastructure control that agents cannot influence. Test it. If you cannot stop all AI traffic within seconds, your emergency layer does not exist.

---

**Next:** [Module 3: PACE Resilience](03-pace-resilience.md)
