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

## Operational Degradation: Token Exhaustion and Silent Failures

### Token Exhaustion as a Security Risk

As agents process more information, their context windows fill. This causes progressive degradation that creates security vulnerabilities:

**Attention dilution.** Safety instructions in the system prompt compete with thousands of tokens of accumulated content. As context fills, the model attends less reliably to its constraints. Prompt-based guardrails effectively weaken without anything adversarial happening.

**Lost-in-the-middle effect.** Models empirically recall information at the beginning and end of context better than the middle. Critical constraints or intermediate reasoning buried in a long context can functionally disappear.

**Increased hallucination rate.** Noisy, conflicting, or redundant context increases the likelihood of plausible-sounding but unsupported outputs — which then propagate through the agent chain.

**Instruction-following degradation.** The model becomes less reliable at following structured output formats, respecting tool schemas, and honoring role boundaries. This is where agents "drift" from their roles.

**Why this compounds in multi-agent systems:**

- Each agent burns tokens independently — degradation is invisible from the orchestrator's perspective
- Retry loops accelerate exhaustion: each failed attempt consumes more context, making the agent *worse* at each retry
- The LLM-as-Judge is also vulnerable — a degraded Judge reviewing a degraded agent is a compounding failure
- Token exhaustion is gradual, not binary — behavioral baselines may not catch it because outputs still look superficially reasonable

**Security implication:** As system prompt influence weakens, adversarial content injected through tool outputs or RAG results has proportionally *more* influence. The agent's defenses weaken as its context fills.

**MASO response:** This maps to execution control (time-boxing, blast radius caps), observability (behavioral drift detection), and the circuit breaker. Token budget management should be treated as an operational control, not just a cost concern. Context rotation strategies, summarization checkpoints, and session time-boxing all help prevent exhaustion-driven degradation.

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
