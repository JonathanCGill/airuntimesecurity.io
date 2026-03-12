# Module 5: Emergent Risks

**Risks unique to multi-agent systems — epistemic, coordination, compound failures, and operational degradation.**

## Why "Emergent"?

These risks do not exist in single-agent systems. They arise from the *interaction dynamics* between agents — not from any individual agent being flawed. A system of individually competent agents can still fail catastrophically as a collective.

MASO formally identifies **34 emergent risks across nine categories**. Many have no OWASP equivalent. This module covers the most important categories and their practical implications.

## Epistemic Risks: When Agents Corrupt Each Other's Reasoning

Epistemic risks are the highest-priority gap addressed by MASO. They describe information-processing failures between agents — situations where agents undermine each other's accuracy *without any adversarial attacker present.*

### Groupthink and Premature Consensus (EP-01)

**What happens:** Agents converge quickly on a plausible narrative. Dissent disappears. A human reviewer sees unanimous agreement and has no reason to challenge it.

**Why it matters:** Multi-agent agreement is not the same as multi-agent correctness. When all agents share the same model, training data, and retrieval sources, their "independent" conclusions are correlated — redundancy in compute, not in reasoning.

**MASO response:** Consensus diversity gates. Unanimous agreement with shared evidence sources triggers escalation, not approval. At least one agent must be assigned an adversarial role with a mandatory "produce a counterexample" step.

### Hallucination Amplification (EP-03)

**What happens:** Agent A hallucinates a claim. It enters the message bus or shared memory. Agent B treats it as fact. By Agent C, the hallucination has been cited, elaborated, and presented with high confidence.

**Why it matters:** In a single-agent system, a hallucination affects one output. In a multi-agent system, it metastasizes through the chain, gaining apparent credibility at each step.

**MASO response:** Claim provenance enforcement. All claims carry metadata: `{source: "tool|rag|agent-generated", verified: bool}`. Claims marked `agent-generated` with `verified: false` cannot be treated as established facts by downstream agents.

### Synthetic Corroboration (EP-04)

**What happens:** Agent A produces a claim. Agent B, asked to verify, retrieves Agent A's output from shared memory and reports "confirmed." One source masquerades as two.

**MASO response:** Self-referential evidence prohibition. No agent may cite another agent's output as primary evidence. The Judge rejects claims where all supporting evidence originates within the orchestration.

### Uncertainty Stripping (EP-06)

**What happens:** An agent reports "this might be the case (70% confidence)." The next agent summarizes as "this is the case." By the time a human reviews it, all uncertainty has been removed, and they approve based on false certainty.

**MASO response:** Mandatory uncertainty fields in inter-agent message schema: `{confidence: float, assumptions: [], unknowns: []}`. Downstream agents must preserve or increase — never decrease — the uncertainty signal.

### Semantic Drift (EP-05)

**What happens:** As information passes through agent chains, precision degrades. "Must" becomes "should." "Never exceed 5%" becomes "keep low." Requirements soften. The final output is plausible but unfaithful to the original input.

**MASO response:** Structured state (JSON schemas, typed fields) for constraints instead of free-text summaries. For chains of 3+ handoffs, the Judge compares the final output against the original task specification for constraint preservation.

## Coordination Risks: When Agents Get Stuck or Drift

### Deadlock and Livelock (CR-01)

**What happens:** Agents wait for each other indefinitely (deadlock) or negotiate endlessly without converging (livelock). The system appears active but produces nothing useful.

**MASO response:** Timeouts on all inter-agent interactions. Maximum turn caps on negotiation sequences (recommended: 10). If agents cannot agree, the orchestrator or Judge decides deterministically.

### Oscillation (CR-02)

**What happens:** Decision flips repeatedly. Agent A proposes X, Agent B proposes Y. Agent A switches to Y, Agent B switches to X. Tokens and time consumed without convergence.

**MASO response:** Decision commit protocol. Once a decision passes Judge review, it is committed. Reversal requires human authorization or documented input change.

### Role Drift (CR-03)

**What happens:** A critic starts taking actions. An executor starts approving its own work. Roles blur because natural language processing allows broad interpretation of responsibilities.

**MASO response:** Hard role boundaries enforced through tool access control lists — not prompts. A critic physically has no write tools. An executor physically has no approval authority. Enforcement at infrastructure layer.

## Operational Degradation: Token Exhaustion as a Dual Failure Path

### The Risk: Agent Failure *and* Detection Failure Simultaneously

Token exhaustion is not merely a performance or cost concern. It is a **dual failure path** — the agent degrades *and* the mechanisms designed to detect that degradation degrade at the same time. This is exactly the kind of correlated failure that PACE is designed to catch, but only if it is explicitly modeled as a risk.

When an agent's context window fills, four things degrade progressively:

**1. Attention dilution.** Safety instructions in the system prompt compete with thousands of tokens of accumulated content. As context fills, the model attends less reliably to its constraints. Prompt-based guardrails effectively weaken without anything adversarial happening.

**2. Lost-in-the-middle effect.** Models empirically recall information at the beginning and end of context better than the middle. Critical constraints or intermediate reasoning buried in a long context can functionally disappear.

**3. Increased hallucination rate.** Noisy, conflicting, or redundant context increases the likelihood of plausible-sounding but unsupported outputs — which then propagate through the agent chain.

**4. Instruction-following degradation.** The model becomes less reliable at following structured output formats, respecting tool schemas, and honoring role boundaries. This is where agents silently "drift" from their roles.

### Why This Is a Correlated Failure in Multi-Agent Systems

The compounding dynamics make token exhaustion especially dangerous:

- **Each agent burns tokens independently.** The orchestrator cannot see that a sub-agent's context is 90% full. Degradation is invisible from the outside until it produces a bad output.
- **Retry loops accelerate exhaustion.** Each failed attempt consumes more context — error messages, failed tool outputs, correction attempts all accumulate. The agent gets *worse* at solving the problem with each retry, not better.
- **The LLM-as-Judge is also vulnerable.** If the Judge is evaluating long chains of agent output, its own context fills. A degraded Judge reviewing a degraded agent means **two defence layers fail simultaneously** — the agent produces lower-quality output, and the Judge is less likely to catch it. This is a direct path to an undetected failure.
- **Token exhaustion is gradual, not binary.** There is no crash, no error code, no circuit breaker trigger. The agent's outputs still *look* reasonable. Behavioral baselines may not flag a slow quality decline until damage is done.
- **Adversarial exploitation becomes easier.** As system prompt influence weakens under context pressure, adversarial content injected through tool outputs or RAG results has proportionally *more* influence on the model's behavior. The agent's immune system weakens as it gets tired.

### Controls: Prevent, Detect, Respond

Token exhaustion requires controls at all three stages — not just monitoring.

#### Prevention: Token Budget Management

| Control | Description | Tier |
|---------|-------------|------|
| **Context rotation** | Periodically checkpoint essential structured state (goal, constraints, accumulated decisions), flush the context, and resume with a clean window. The agent does not lose its work — it gets a fresh attention budget. | Tier 2+ |
| **Input volume limiting** | Cap the volume of data flowing into any single agent context. Force task decomposition into smaller scoped sub-tasks rather than letting one agent accumulate unbounded context. | Tier 1+ |
| **Summarization checkpoints** | At each agent handoff, produce a structured summary rather than forwarding raw context. Use typed fields (JSON schemas) for constraints and decisions to resist semantic drift during summarization. | Tier 2+ |
| **Retry caps** | Limit retry attempts per agent to prevent error-message accumulation. If an agent cannot succeed in N attempts, escalate — do not let it keep trying with an increasingly degraded context. | Tier 1+ |
| **Judge context isolation** | The Judge must manage its own context budget independently. It should evaluate agent outputs in fresh or rotation-managed context — never by accumulating the full history of everything it has reviewed. | Tier 2+ |

#### Detection: Token Budget Monitoring

| Control | Description | Tier |
|---------|-------------|------|
| **Threshold alerts** | Monitor token consumption per agent as a first-class operational metric (like CPU or memory). Alert operators at configurable thresholds (e.g., 70%, 85%, 95% of context capacity). | Tier 1+ |
| **Quality regression signals** | Monitor for symptoms of context degradation: increased format violations, constraint drift, hallucination rate changes, instruction-following failures. These are leading indicators before the context is fully exhausted. | Tier 2+ |
| **Judge budget monitoring** | Track the Judge's context consumption independently. If the Judge approaches its own capacity threshold, this is a **detection-layer degradation** event — treat it as a PACE trigger, not just an operational metric. | Tier 2+ |

#### Response: PACE-Integrated Escalation

This is where token exhaustion connects directly to the PACE model. The response must be **scaled to tier and risk**, not one-size-fits-all:

| Threshold | Tier 1 Response | Tier 2 Response | Tier 3 Response |
|-----------|----------------|-----------------|-----------------|
| **Warning** (e.g., 70%) | Log alert. Notify administrator. | Log alert. Initiate context rotation for affected agent. Notify operator. | Automated context rotation. Notify operator. Quality regression monitoring tightened. |
| **Critical** (e.g., 85%) | Log alert. Notify administrator. Recommend manual context rotation. | **Fail-closed on the affected agent.** Pause agent, rotate context, resume. If Judge is also at threshold, transition P→A (tighten scope, require human approval for writes). | **Automatic P→A transition.** Affected agent paused and rotated. Backup agent activated. If Judge is at threshold, transition to P→C (human-in-the-loop for all decisions). |
| **Exhaustion** (e.g., 95%+) | Fail-closed. Agent paused until administrator intervenes. | **P→A or A→C transition.** Agent terminated and restarted with clean context and checkpointed state. Human approves all pending actions. | **A→C or C→E transition** depending on blast radius. If both agent and Judge are exhausted simultaneously, treat as correlated failure — Contingency minimum. |

**The key principle:** When the agent *and* the Judge both approach exhaustion thresholds, this is a **correlated dual-layer failure**. It must trigger a PACE transition, not just an alert. The appropriate response depends on tier:

- **Tier 1:** Administrator warning is sufficient — human oversight is already in the loop for all actions.
- **Tier 2:** Fail-closed on affected agents. Automatic context rotation. If rotation is not possible, transition to Alternate with tightened human oversight.
- **Tier 3:** Automatic PACE transition. Correlated exhaustion of agent and Judge at Tier 3 is a Contingency-level event — two independent defence layers have degraded simultaneously.

### Context Rotation: The Primary Mitigation

Context rotation is the core operational response to token exhaustion. It preserves the agent's work while restoring its cognitive capacity:

```
  Agent operating normally
        │
        ▼
  Token budget threshold reached
        │
        ▼
  Checkpoint structured state:
  ┌─────────────────────────────┐
  │ • Original task/goal        │
  │ • Active constraints        │
  │ • Decisions made so far     │
  │ • Current step in plan      │
  │ • Uncertainty metadata      │
  │ • Assumption register       │
  └─────────────────────────────┘
        │
        ▼
  Flush context window
        │
        ▼
  Resume with:
  • System prompt (full strength)
  • Checkpointed structured state
  • Fresh attention budget
```

**Critical design consideration:** Summarization during context rotation introduces its own risk — semantic drift (EP-05). This is why checkpointed state must use **structured fields** (JSON schemas, typed constraints), not free-text summaries. "Must not exceed 5%" stored as `{constraint: "max_percentage", value: 5, type: "hard_limit"}` survives rotation intact. "Keep the percentage low" does not.

### Why This Matters for Solution Design

Token exhaustion is not an edge case. It is an **expected operational condition** for any long-running or complex multi-agent system. If your agents process large documents, interact over many turns, or perform multi-step research, they *will* approach context limits. The question is not whether it will happen, but whether your system degrades gracefully when it does.

Treat token budget like any other resource constraint — monitor it, set thresholds, define responses, and test your rotation and failover paths.

### Partial Failure Masquerading as Success (OP-03)

**What happens:** An agent chain completes, returns an output, and reports success — but one agent silently failed, skipped a step, or substituted a shallow analysis for a thorough one. The final output looks complete but is built on incomplete work.

**MASO response:** Plan-execution conformance checks. Execution is validated against the approved plan at the step level. Deviations trigger re-approval. The Judge also scores analytical depth, not just format compliance.

## Safety and Misuse Risks

### Cumulative Harm via Decomposition (SM-01)

**What happens:** Each agent's individual output is benign. But combined, they enable a harmful outcome. A planning agent decomposes a harmful task into harmless-looking subtasks that individually pass guardrails.

**MASO response:** Aggregate harm assessment. The Judge evaluates the full task plan, not just individual outputs. For multi-step plans, the Judge reviews the whole plan before execution begins.

### Persuasion Optimization (SM-02)

**What happens:** Agents iterating on user-facing messaging optimize for compliance — A/B testing persuasion techniques, escalating emotional appeal, manufacturing urgency. This can occur without adversarial intent if agents optimize for "task completion."

**MASO response:** Anti-manipulation guardrail. Outputs directed at humans must not employ escalating persuasion, manufactured urgency, or emotional manipulation. The Judge includes a manipulativeness score in its evaluation criteria.

## The Pattern Across All Emergent Risks

Notice the common thread: **these risks arise from agent interactions, not from individual agent flaws.** This is why single-agent security models are insufficient for multi-agent systems, and why MASO exists as a distinct framework.

The defenses follow a pattern too:

1. **Structured data over natural language** for critical information (constraints, uncertainty, provenance)
2. **Infrastructure enforcement over prompt enforcement** for role boundaries and permissions
3. **Independent verification** at each handoff, not just at the system boundary
4. **The Judge evaluates the aggregate**, not just individual parts

---

**Next:** [Module 6: Applying MASO to Your Solution](06-applying-maso.md)
