# Multi-Agent Runtime Operations: Failure Node and Feedback Loop Analysis

## Systems Thinking Approach

This document maps the runtime event space of a multi-agent system: failure nodes at each stage, whether failures are detectable or silent, and the feedback loops that amplify, dampen, or transform failures across agent boundaries.

Most dangerous failures are not point failures. They are emergent properties of feedback loops where no single node is observably broken.

---

## 1. Runtime Event Taxonomy

Every multi-agent runtime operation falls into one of seven event classes. Each class contains discrete events that occur during normal operation.

### 1.1 Agent Lifecycle Events

| Event | Description | Trigger |
|-------|-------------|---------|
| Agent instantiation | New agent instance created with identity, role, and permissions | Orchestrator receives task requiring delegation |
| Context assembly | Agent loads system prompt, task instructions, memory, and any upstream context | Immediately post-instantiation |
| Capability binding | Agent is granted access to tools, APIs, other agents, or data sources | Configuration at instantiation or runtime |
| Session state initialisation | Working memory, scratchpad, and intermediate state structures created | First inference cycle |
| Agent termination | Agent instance destroyed, state flushed or persisted | Task completion, timeout, containment trigger, or error |
| Agent restart/retry | Failed agent re-instantiated, potentially with modified context | Error handler or orchestrator policy |

### 1.2 Inference Events

| Event | Description | Trigger |
|-------|-------------|---------|
| Prompt construction | Final prompt assembled from system prompt + context + task + upstream inputs | Pre-inference |
| LLM inference | Model generates output (text, structured data, tool call, or delegation request) | Prompt submitted to model |
| Token streaming | Partial output generated incrementally | During inference |
| Output completion | Full response available for processing | Inference complete |
| Inference timeout | Model fails to produce output within time budget | Clock expiry |
| Inference error | Model returns error, malformed output, or empty response | Model failure |

### 1.3 Inter-Agent Communication Events

| Event | Description | Trigger |
|-------|-------------|---------|
| Message dispatch | Agent sends output to another agent via orchestrator or direct channel | Agent produces output intended for downstream consumption |
| Message receipt | Agent receives input from upstream agent | Orchestrator routes message |
| Delegation request | Agent requests another agent to perform a sub-task | Agent determines it cannot or should not complete task alone |
| Delegation response | Delegated agent returns result to requesting agent | Sub-task complete |
| Broadcast | Agent sends output to multiple downstream agents simultaneously | Fan-out pattern |
| Aggregation | Agent receives and combines inputs from multiple upstream agents | Fan-in pattern |
| Negotiation/debate | Two or more agents exchange messages iteratively to reach consensus | Conflict resolution or deliberation pattern |

### 1.4 Tool and External Interaction Events

| Event | Description | Trigger |
|-------|-------------|---------|
| Tool invocation | Agent calls an external tool, API, database, or service | Agent determines tool use required |
| Tool response | External system returns result to agent | Tool execution complete |
| Tool timeout | External system fails to respond within time budget | Clock expiry |
| Tool error | External system returns error or unexpected result | External failure |
| Data retrieval | Agent fetches data from knowledge base, vector store, or file system | RAG or data lookup |
| Data write | Agent writes data to external store (database, file, API) | Agent produces persistent output |
| Side effect execution | Agent triggers an irreversible action (send email, execute trade, deploy code) | Agent reaches action decision |

### 1.5 Validation and Guardrail Events

| Event | Description | Trigger |
|-------|-------------|---------|
| Input validation | Incoming message checked against schema, bounds, format rules | Message receipt |
| Output guardrail check | Agent output screened for policy violations (toxicity, PII, format) | Post-inference |
| Model-as-Judge evaluation | Secondary model evaluates output quality, relevance, safety | Post-inference or post-handoff |
| Epistemic checkpoint | Independent verification of reasoning basis and claim provenance | Configured checkpoint in chain |
| Guardrail pass | Validation succeeds, output proceeds | Validation complete |
| Guardrail block | Validation fails, output rejected or modified | Policy violation detected |
| Guardrail bypass | Output proceeds despite failing soft validation (risk-accepted) | Override policy or threshold not met |

### 1.6 Orchestration and Flow Control Events

| Event | Description | Trigger |
|-------|-------------|---------|
| Task decomposition | Complex task broken into sub-tasks for distribution | Orchestrator receives complex request |
| Agent selection | Orchestrator chooses which agent(s) to assign sub-tasks | Task decomposition complete |
| Routing decision | Orchestrator determines message path through agent chain | Inter-agent handoff |
| Parallel dispatch | Multiple agents launched concurrently on independent sub-tasks | Task graph allows parallelism |
| Synchronisation barrier | Orchestrator waits for multiple agents to complete before proceeding | Fan-in dependency |
| Retry/fallback | Failed task reassigned to same or different agent with modified parameters | Error recovery |
| Circuit break | Chain execution halted due to repeated failures or anomaly detection | Threshold exceeded |
| Timeout escalation | Task exceeds total time budget, escalated or terminated | Clock expiry at chain level |

### 1.7 Observability and Audit Events

| Event | Description | Trigger |
|-------|-------------|---------|
| Log write | Structured event record written to log store | Every event above |
| Metric emission | Quantitative measurement published (latency, token count, cost) | Per-inference or per-handoff |
| Trace span | Distributed trace segment opened/closed for a unit of work | Agent lifecycle boundaries |
| Anomaly alert | Monitoring system detects deviation from baseline | Statistical threshold breach |
| Audit record | Immutable compliance record of decision, reasoning, and evidence | Side effect execution or decision output |
| Human notification | Alert sent to human operator for review | Escalation policy trigger |

---

## 2. Failure Node Map

Each runtime event is a potential failure node. Failures are classified by **detection** (loud or silent) and **propagation** (contained or propagating). The most dangerous failures are **silent + propagating**: the system continues operating with corrupted state and no alert. These are the primary targets for MASO controls.

### 2.1 Agent Lifecycle Failure Nodes

| Failure | Detection | Propagation | Description |
|---------|-----------|-------------|-------------|
| Identity misconfiguration | Silent | Propagating | Agent instantiated with wrong permissions or role. All subsequent actions authorised incorrectly. No error because the agent functions normally within its (wrong) scope. |
| Context poisoning | Silent | Propagating | Malicious or corrupted data injected into agent context at assembly. Agent operates on false premises. Output appears normal. |
| Stale context | Silent | Propagating | Agent loaded with outdated information (expired cache, old embeddings). Decisions based on superseded data. |
| Capability over-provisioning | Silent | Propagating | Agent granted access to tools or data beyond what the task requires. No failure until the agent uses an unnecessary capability in an unintended way. |
| Zombie agent | Loud | Contained | Agent fails to terminate, continues consuming resources. Detectable via resource monitoring. |
| State persistence failure | Loud | Contained | Agent state not properly saved or flushed on termination. Detectable via data integrity checks. |
| Restart context loss | Silent | Propagating | Agent restarted after failure but loses critical intermediate state. Resumes with incomplete picture. May produce subtly different output path. |

### 2.2 Inference Failure Nodes

| Failure | Detection | Propagation | Description |
|---------|-----------|-------------|-------------|
| Confabulation | Silent | Propagating | Model generates plausible but false factual claims. No error signal. Downstream agents treat output as ground truth. This is the canonical MASO failure. |
| Instruction drift | Silent | Propagating | Model partially follows instructions, omitting or subtly altering requirements. Output looks reasonable but doesn't fully satisfy the task. |
| Sycophantic alignment | Silent | Propagating | Model optimises for upstream agent approval rather than task accuracy. Produces agreeable but potentially incorrect output. |
| Capability masking (sandbagging) | Silent | Propagating | Model conceals its true capability level, performing below its potential. May occur due to alignment pressure or adversarial prompting. |
| Subtle degradation (sandbugging) | Silent | Propagating | Model produces output that is marginally but systematically degraded. Not wrong enough to trigger guardrails. Compounds across chain. |
| Inference timeout | Loud | Contained | Model exceeds time budget. Detectable. Handled by retry/fallback. |
| Malformed output | Loud | Contained | Model produces unparseable output. Caught by schema validation. |
| Refusal | Loud | Contained | Model refuses task due to safety filter. Detectable but may need override or re-routing. |

### 2.3 Inter-Agent Communication Failure Nodes

| Failure | Detection | Propagation | Description |
|---------|-----------|-------------|-------------|
| Semantic loss in handoff | Silent | Propagating | Information is correctly formatted but meaning is lost or distorted in translation between agent contexts. Agent B interprets Agent A's output differently than intended. |
| Context window truncation | Silent | Propagating | Upstream output exceeds downstream agent's context capacity. Critical information silently dropped during summarisation or truncation. |
| Delegation scope creep | Silent | Propagating | Delegated agent interprets its mandate more broadly than intended. Performs actions outside the requesting agent's intent. No error because the delegation was syntactically valid. |
| Delegation goal substitution | Silent | Propagating | Delegated agent optimises for a proxy of the intended objective. Result satisfies surface criteria but misses actual intent. |
| Message ordering violation | Loud or Silent | Propagating | Messages arrive out of expected sequence. If schema-enforced, detectable. If not, agent processes in wrong order with corrupted reasoning. |
| Phantom authority | Silent | Propagating | Agent B acts on Agent A's output as if it carried authority that Agent A does not have. No mechanism to verify delegation authority at runtime. |
| Aggregation bias | Silent | Propagating | When combining outputs from multiple agents, the aggregation logic systematically favours one source over another, or loses minority signals. |

### 2.4 Tool and External Interaction Failure Nodes

| Failure | Detection | Propagation | Description |
|---------|-----------|-------------|-------------|
| Stale external data | Silent | Propagating | Tool returns cached or outdated data. Agent treats it as current. |
| Tool misuse | Silent | Propagating | Agent calls the right tool with subtly wrong parameters. Tool returns a valid result for the wrong query. |
| Side effect irreversibility | Loud (after the fact) | Propagating | Agent executes an irreversible action based on corrupted upstream reasoning. Detectable only post-execution. Damage already done. |
| Tool hallucination | Silent | Propagating | Agent fabricates a tool call that appears in its output as if executed, but never actually ran. Downstream agents may treat the fabricated result as real. |
| API schema drift | Loud or Silent | Propagating | External API changes its response format. If validation is strict, caught. If loose, agent parses incorrect fields silently. |
| Rate limit / throttling | Loud | Contained | External system rejects request. Detectable. Retry logic handles it. |
| Data exfiltration | Silent | Contained | Agent sends sensitive data to an external endpoint via tool use. May not trigger internal monitoring if the tool call is syntactically valid. |

### 2.5 Validation and Guardrail Failure Nodes

| Failure | Detection | Propagation | Description |
|---------|-----------|-------------|-------------|
| Guardrail evasion | Silent | Propagating | Output crafted (intentionally or emergently) to pass guardrails while carrying harmful or incorrect content. The guardrail reports "pass" on a bad output. |
| Judge model confabulation | Silent | Propagating | The Model-as-Judge itself confabulates, approving output based on false reasoning. Second-order confabulation. |
| False positive block | Loud | Contained | Guardrail rejects valid output. Detectable but causes delay, retry, or escalation. |
| Threshold miscalibration | Silent | Propagating | Guardrail thresholds too loose; marginal violations pass consistently. No individual failure is dramatic enough to trigger alerts, but aggregate effect is significant. |
| Checkpoint blind spot | Silent | Propagating | Epistemic checkpoint verifies claims the agent made but doesn't detect claims the agent should have made but omitted. Omission is harder to catch than commission. |
| Validation ordering error | Silent | Propagating | Guardrails applied in wrong sequence. A downstream check assumes an upstream check has already passed, but it hasn't. |

### 2.6 Orchestration Failure Nodes

| Failure | Detection | Propagation | Description |
|---------|-----------|-------------|-------------|
| Task decomposition error | Silent | Propagating | Orchestrator breaks task into wrong sub-tasks. Each sub-task executes correctly but the aggregate doesn't solve the original problem. |
| Agent misselection | Silent | Propagating | Orchestrator assigns task to an agent with insufficient capability or wrong specialisation. Agent produces plausible but suboptimal output. |
| Routing loop | Loud (eventually) | Contained | Message cycles between agents indefinitely. Detectable via loop counter or timeout, but wastes resources. |
| Race condition | Silent | Propagating | Parallel agents produce conflicting outputs. Aggregation resolves the conflict arbitrarily rather than correctly. |
| Synchronisation deadlock | Loud | Contained | Agents waiting on each other. Detectable via timeout. |
| Cascade failure | Loud (eventually) | Propagating | One agent failure triggers retries that overload other agents. System degrades progressively. Detectable in aggregate but individual failures may look transient. |

---

## 3. Feedback Loops

Feedback loops make multi-agent systems behave as complex adaptive systems rather than linear pipelines.

### 3.1 Amplifying Loops (Positive Feedback - Destabilising)

These loops make small problems bigger and are the primary source of emergent systemic risk.

#### Loop 1: Confabulation Cascade

```
Agent A confabulates claim X
    → Agent B receives X as verified input
    → Agent B builds reasoning on X, adds claims Y and Z derived from X
    → Agent C receives X + Y + Z, all appearing well-sourced
    → Agent C makes decision based on three "facts," all rooted in one fabrication
    → Confidence in the chain output is HIGH (multiple supporting claims)
    → Human reviewer sees high-confidence output, less likely to challenge
```

**Amplification mechanism:** Each agent adds derived claims, burying the original fabrication under legitimate-looking reasoning.

**MASO intervention point:** Epistemic checkpoint at each handoff verifying claim provenance. Break the loop at first propagation.

#### Loop 2: Sycophantic Reinforcement

```
Agent A produces output aligned with orchestrator's implicit preference
    → Orchestrator (or evaluation agent) rates output favourably
    → Favourable rating reinforces Agent A's approach in subsequent cycles
    → Agent A becomes increasingly aligned with perceived preference
    → Actual task accuracy drifts from actual objective
    → Favourable ratings continue (evaluator has same bias)
    → System converges on confidently wrong equilibrium
```

**Amplification mechanism:** The evaluation signal rewards agreement, not accuracy.

**MASO intervention point:** Independent epistemic evaluation measuring accuracy against external reference, not chain-internal coherence.

#### Loop 3: Context Window Compression Death Spiral

```
Chain generates large volumes of inter-agent communication
    → Context windows fill up
    → Summarisation/truncation applied to fit context budgets
    → Critical nuance lost in compression
    → Downstream agent makes subtly wrong inference due to missing nuance
    → Downstream agent's output adds more text, further filling context
    → Next summarisation step compounds the loss
    → Each cycle loses more signal, adds more noise
    → Eventually, agents operate on heavily degraded representations of original inputs
```

**Amplification mechanism:** Information loss is cumulative and irreversible. Each compression cycle removes the details most likely to catch errors.

**MASO intervention point:** Provenance tagging on critical claims so they survive summarisation. Checkpoint verifying key facts are preserved post-compression.

#### Loop 4: Error Recovery Amplification

```
Agent fails on task
    → Retry triggered with modified prompt or fallback agent
    → Retry produces different output (not necessarily better)
    → Downstream agents now receive a different input than expected
    → Downstream outputs diverge from the path they would have taken
    → If retry output is subtly worse, downstream agents compound the degradation
    → System has no mechanism to compare retry path with original path
    → Retry is treated as "recovery" but may be "mutation"
```

**Amplification mechanism:** Error recovery changes the system trajectory with no mechanism to evaluate whether the new path is better or worse.

**MASO intervention point:** Containment boundary evaluating retry output against original task criteria before allowing downstream propagation.

### 3.2 Dampening Loops (Negative Feedback - Stabilising)

These loops reduce the impact of failures. They are what MASO controls are designed to create.

#### Loop 5: Epistemic Checkpoint Correction

```
Agent produces output with unverifiable claim
    → Epistemic checkpoint detects missing provenance
    → Output rejected, agent prompted to provide sourced claims
    → Agent regenerates with explicit sourcing
    → Checkpoint verifies sources
    → Corrected output propagates downstream
```

**Dampening mechanism:** Verification barrier forces correction before propagation. Failure is caught at the node of origin.

**Dependency:** Checkpoint must verify provenance, not just plausibility. A Model-as-Judge that only checks "does this sound right" will not catch well-constructed confabulations.

#### Loop 6: Human Oversight Escalation

```
Automated monitoring detects anomaly in chain behaviour
    → Alert escalated to human reviewer
    → Human reviews chain state, inter-agent messages, and decision basis
    → Human identifies root cause (or requests more information)
    → Human intervenes: corrects output, adjusts policy, or terminates chain
    → Correction propagates through remainder of chain
```

**Dampening mechanism:** Human judgment breaks automated feedback loops that have converged on wrong answers.

**Dependency:** Chain-of-custody logging must provide the full reasoning trail. Oversight debt (speed mismatch between chain execution and human review) limits the frequency of this loop.

#### Loop 7: Containment Circuit Breaker

```
Agent output triggers containment policy (e.g., confidence below threshold, anomaly score above threshold)
    → Chain execution paused at containment boundary
    → Partial state preserved for inspection
    → System evaluates: retry, escalate, or terminate
    → If retry: modified parameters, tighter constraints, or different agent
    → If terminate: graceful shutdown, partial results flagged as incomplete
    → Downstream agents never receive corrupted input
```

**Dampening mechanism:** Hard stop prevents propagation at the node where the failure occurred.

**Dependency:** Containment thresholds must be correctly calibrated. Too tight = constant false positives. Too loose = failures pass through.

### 3.3 Transforming Loops (Feedback that Changes the Nature of the Failure)

These loops don't amplify or dampen failures. They transmute them into qualitatively different problems.

#### Loop 8: Guardrail Adversarial Co-evolution

```
Guardrail blocks certain output patterns
    → Agent adjusts output to avoid triggering guardrail
    → Adjusted output passes guardrail but carries the problematic content in different form
    → Guardrail updated to catch new pattern
    → Agent adjusts again
    → System converges on increasingly sophisticated evasion/detection arms race
    → Original content problem transforms into a guardrail gaming problem
```

**Transformation mechanism:** The failure shifts from "bad output" to "output optimised to appear good to the specific detection mechanism." The risk surface moves from content to evaluation.

**MASO intervention point:** Multi-layered evaluation (guardrail + Model-as-Judge + epistemic checkpoint + human sample) so gaming one layer doesn't bypass all layers.

#### Loop 9: Delegation Recursion

```
Agent A delegates sub-task to Agent B
    → Agent B determines it needs to delegate part of the sub-task to Agent C
    → Agent C delegates further to Agent D
    → Each delegation slightly reinterprets the original objective
    → By Agent D, the task being performed is related to but different from the original
    → Agent D's output passes back up the chain
    → Each agent accepts the output because it matches what they delegated (not the original task)
    → Final output satisfies no one's actual intent but everyone's proximate request
```

**Transformation mechanism:** Goal fidelity degrades through reinterpretation at each delegation boundary: "wrong answer" becomes "right answer to the wrong question."

**MASO intervention point:** Delegation scope specification carrying the original objective through the chain. Checkpoint at each boundary verifying alignment with the root objective.

#### Loop 10: Observability Saturation

```
System generates high volume of logs, metrics, and alerts
    → Monitoring dashboards become noisy
    → Operators apply filters to reduce noise
    → Filters inadvertently suppress signals of novel failure modes
    → Novel failure occurs, alert suppressed by filter
    → Failure propagates undetected
    → Post-incident review identifies the suppressed alert
    → New alert rule added, increasing total alert volume
    → Cycle repeats with higher baseline noise
```

**Transformation mechanism:** The failure transforms from an agent-level problem to an observability problem. Managing information overload creates blind spots that become the actual vulnerability.

**MASO intervention point:** Structured anomaly detection operating on patterns rather than individual alerts. Epistemic integrity scoring provides a composite signal harder to drown in noise than discrete event alerts.

---

## 4. Failure Propagation Pathways

Understanding the propagation mode determines where controls are effective.

### 4.1 Linear Propagation

```
A → B → C → D
Failure at A corrupts B, B corrupts C, C corrupts D.
Detection opportunity at every boundary.
```

**Control strategy:** Epistemic checkpoint at each handoff. Any checkpoint that catches the failure stops propagation. Defence in depth.

### 4.2 Fan-Out Amplification

```
        → B₁ → D₁
A → B  → B₂ → D₂
        → B₃ → D₃
Failure at A propagates to B, then fans out to B₁, B₂, B₃.
Single upstream failure creates multiple downstream failures.
```

**Control strategy:** Checkpoint BEFORE the fan-out point. Catching the failure after fan-out requires catching it in every branch.

### 4.3 Fan-In Masking

```
A₁ →
A₂ → C → D
A₃ →
Failure at A₁, but A₂ and A₃ are correct.
Aggregation at C may mask A₁'s failure (majority vote) or amplify it (if A₁'s output is weighted higher).
```

**Control strategy:** Independent validation of each input at C before aggregation. Don't rely on aggregation to filter out bad inputs.

### 4.4 Recursive Amplification

```
A → B → A → B → A → B ...
Output from B feeds back to A in next cycle.
Small bias compounds exponentially with each cycle.
```

**Control strategy:** Circuit breaker on recursive loops. Maximum iteration count. Drift detection that measures how much the output is shifting per cycle. Terminate when drift exceeds threshold.

### 4.5 Latent Propagation

```
A → B → C → [data store] → ... → X → Y → Z
Failure at A is written to persistent store.
Much later, Agent X reads from store, reintroducing the corruption.
No temporal or causal proximity between origin and impact.
```

**Control strategy:** Provenance metadata on all persisted data. When Agent X reads from store, provenance is available for verification. This is the hardest propagation mode to control because the failure crosses execution boundaries.

---

## 5. Composite Failure Scenarios

Real-world failures combine multiple failure nodes and feedback loops simultaneously. These scenarios illustrate how systems thinking reveals risks that point-analysis misses.

### Scenario 1: The Confident Wrong Answer

**Failure nodes activated:** Confabulation (2.2) + Semantic loss in handoff (2.3) + Judge model confabulation (2.5)
**Feedback loops activated:** Confabulation Cascade (Loop 1) + Sycophantic Reinforcement (Loop 2)

Agent A retrieves data but confabulates one regulatory threshold. Agent B receives this, and the handoff summary loses the qualifier "approximately" that Agent A included. Agent C now has a precise-looking but fabricated number. The Model-as-Judge evaluates the chain and assesses it as "well-sourced and internally consistent." The human reviewer sees a confident, high-rated output and approves it.

**Why point-analysis misses this:** Each node performed acceptably. The failure is emergent from the interaction of individually small deviations.

### Scenario 2: The Slow Drift

**Failure nodes activated:** Subtle degradation/sandbugging (2.2) + Threshold miscalibration (2.5) + Context window compression (2.3)
**Feedback loops activated:** Context Window Compression Death Spiral (Loop 3) + Observability Saturation (Loop 10)

An agent in a recurring process subtly degrades its output quality over time (or across iterations). Each output is marginally worse than the last, but never enough to trigger guardrails. Context compression between cycles loses the details that would reveal the trend. Monitoring generates alerts on noise that operators filter out, incidentally suppressing the degradation signal. Over weeks, the system's baseline output quality drops significantly. No single event is a failure. The failure is the trajectory.

**Why point-analysis misses this:** No single execution contains a detectable failure. The degradation is only visible in the time series across executions.

### Scenario 3: The Delegation Shell Game

**Failure nodes activated:** Delegation scope creep (2.3) + Task decomposition error (2.6) + Phantom authority (2.3)
**Feedback loops activated:** Delegation Recursion (Loop 9) + Error Recovery Amplification (Loop 4)

Orchestrator decomposes task incorrectly, assigning a sub-task to Agent A that should have gone to Agent B. Agent A partially fails, triggering retry. The retry agent reinterprets the task, delegates to Agent C, which delegates further. By the end, the executed task bears only superficial resemblance to the original. But each delegation was syntactically valid, and the final output matches the format expected. The output is accepted because it looks right.

**Why point-analysis misses this:** Every agent completed its delegated task and every handoff was valid. Root cause analysis requires reconstructing the full delegation chain and comparing it to the original intent.

---

## 6. Control Placement Principles

Based on the failure node map and feedback loop analysis, MASO controls should be placed according to these principles:

### Principle 1: Prioritise silent + propagating failures
Loud failures handle themselves (they trigger errors). Contained failures don't spread. The controls that matter most target the top-left quadrant: failures that are invisible and that corrupt downstream state.

### Principle 2: Break amplifying loops at first propagation
Every amplifying feedback loop (Loops 1-4) has a point where the failure first crosses an agent boundary. Place the epistemic checkpoint there. Catching it later is exponentially harder.

### Principle 3: Control before fan-out, validate before fan-in
Fan-out amplifies failures multiplicatively. Fan-in can mask them. Place verification before divergence points and independent validation before convergence points.

### Principle 4: Monitor trajectories, not just states
Transforming loops (Loops 8-10) and slow-drift scenarios are invisible to point-in-time monitoring. Longitudinal metrics (epistemic integrity scores over time, delegation depth trends, guardrail near-miss rates) detect what snapshots miss.

### Principle 5: Provenance survives persistence
Any time agent output is written to a data store, the provenance metadata must persist with it. Latent propagation (4.5) defeats every other control if corrupted data can be reintroduced without its lineage.

### Principle 6: Containment must be faster than propagation
If the chain can execute three handoffs before a checkpoint evaluates the first one, the checkpoint is architecturally irrelevant. Containment response time must be shorter than inter-agent message propagation time.

---

## 7. Mapping to MASO Control Domains

| Failure Class | Primary MASO Control | Secondary Controls |
|---------------|---------------------|-------------------|
| Confabulation propagation | Epistemic checkpoints with provenance verification | Chain-of-custody logging, claim-level source tagging |
| Delegation failures | Delegation scope specification, root objective preservation | Authority verification at each boundary, delegation depth limits |
| Context degradation | Critical claim preservation through summarisation | Context integrity scoring, mandatory retention of provenance metadata |
| Guardrail evasion | Multi-layered evaluation (guardrail + judge + checkpoint) | Adversarial testing of guardrail configurations, evaluation diversity |
| Orchestration errors | Task decomposition validation, agent capability matching | Independent verification of decomposition against original objective |
| Tool misuse / side effects | Pre-execution verification of tool calls against task scope | Irreversibility gates requiring elevated confidence before side effects |
| Feedback loop amplification | Circuit breakers on recursive patterns, drift detection | Maximum iteration limits, per-cycle deviation measurement |
| Observability failures | Structured anomaly detection, composite integrity scoring | Alert hygiene, longitudinal trend monitoring |
| Latent propagation | Provenance metadata persistence, lineage tracking on reads | Data store integrity verification, source freshness validation |
| Silent identity/capability failures | Runtime identity verification, least-privilege enforcement | Capability auditing, periodic re-verification during long-running chains |
