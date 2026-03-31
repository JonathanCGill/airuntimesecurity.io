---
description: "Agentic drift is the gradual erosion of security context, intent, and constraints as tasks flow through agent delegation chains. It is distinct from model drift and harder to detect."
---

# Agentic Drift

*When agents delegate to agents, the security context doesn't just travel. It degrades.*

## The Problem

Consider a user request that passes through four agents. The user's intent is specific: "Summarise Q1 revenue for my team's accounts only." The first agent understands the constraint. By the time the request reaches the fourth agent, the constraint has softened to "get Q1 revenue data," and the agent queries accounts the user was never authorised to see.

Nobody attacked the system. No agent was compromised. The security context simply eroded as it passed through the chain.

This is **agentic drift**: the unintentional, gradual loss of security constraints, intent boundaries, and contextual meaning as tasks are delegated from agent to agent. It is distinct from model drift (where the model's behavior changes over time) and from deliberate privilege escalation (where an attacker exploits a delegation chain). Agentic drift happens in systems that are working as designed, because the design did not account for how context degrades across agent boundaries.

## Why Context Degrades

### 1. Lossy summarisation

Agents do not forward raw instructions verbatim. They interpret, summarise, and rephrase. Each summarisation step is lossy. A constraint expressed as natural language ("only accounts in the EMEA region") may be paraphrased, abbreviated, or dropped entirely when an agent formulates a sub-task for a downstream agent.

The information loss is not random. Constraints and qualifiers are the first casualties. "Summarise recent customer complaints about billing, excluding accounts in legal dispute" becomes "summarise billing complaints." The core task survives. The boundaries do not.

### 2. Context window pressure

Every agent has a finite context window. As chains deepen, upstream context competes with the current agent's own instructions, tool outputs, and reasoning traces. Agents under context pressure shed what looks least relevant to the immediate task. Security constraints often look like metadata rather than core instructions.

This is especially dangerous in long-running agentic workflows where the context window fills over time. The constraint that was prominent in turn one is buried by turn fifty.

### 3. Implicit vs. explicit constraints

Some security context is explicit: "the user has read-only access to dataset X." Some is implicit: the user asked a question about *their* accounts, implying a scope limit. Explicit constraints can be propagated structurally (see [DEL-01](../infrastructure/agentic/delegation-chains.md)). Implicit constraints require interpretation, and each agent may interpret them differently, or not at all.

### 4. Semantic reframing

When Agent A tells Agent B to "look up the customer's order history," the word "customer" refers to a specific individual in Agent A's context. Agent B may interpret "customer" more broadly, returning data for multiple customers. The task description was accurate. The referent shifted.

This is not a bug in any single agent. It is an emergent property of chained natural-language communication.

## How It Differs from Model Drift

Model drift is about the model changing. Agentic drift is about the context changing. They can compound, but they require different controls.

| Dimension | Model Drift | Agentic Drift |
|-----------|-------------|---------------|
| **What changes** | The model's behavior | The security context flowing through the chain |
| **Root cause** | Provider updates, data shift, silent degradation | Lossy summarisation, context pressure, semantic reframing |
| **Detection** | Behavioral baselines, anomaly scoring | Context comparison across chain hops |
| **Time scale** | Days to weeks | Within a single request chain |
| **Affected systems** | Any system using the model | Multi-agent systems with delegation |

When both occur simultaneously, the effect is multiplicative. A model that has drifted toward weaker instruction-following will lose constraints faster as it summarises tasks for downstream agents. The multi-agent drift amplification problem becomes significantly worse.

## Where It Appears

### Orchestrator-to-specialist delegation

The most common pattern. An orchestrator agent decomposes a user request into sub-tasks and assigns them to specialist agents. The orchestrator understands the user's full intent. Each specialist receives only a fragment, stripped of the broader context that gave it meaning.

The specialist optimises for its narrow task. Without the full context, it may take actions that are locally correct but globally inappropriate.

### Chain-of-thought handoffs

Some architectures pass reasoning traces between agents. These traces are verbose, and downstream agents may truncate or ignore them. The reasoning that justified a particular constraint ("we scoped this to EMEA because the user is a regional manager") is lost, and the constraint becomes unmotivated, making it more likely to be dropped in subsequent summarisation.

### Tool-mediated delegation

Agent A calls a tool that triggers Agent B. The tool interface may only pass structured parameters, not the full context. If the security constraints were expressed in natural language in Agent A's context, they do not survive the structured interface. The tool acts as a context bottleneck.

### Cross-system delegation

When agents delegate across system boundaries (via [A2A](../core/multi-agent-controls.md#a2a-agent-to-agent-protocol) or similar protocols), context loss is almost guaranteed. Different systems have different context formats, different permission models, and different assumptions about what "default" access looks like.

## Why Existing Controls Are Necessary but Not Sufficient

The framework already provides structural controls that mitigate parts of this problem:

- **[DEL-01](../infrastructure/agentic/delegation-chains.md)** enforces permission intersection at each hop, preventing privilege escalation through the authorisation gateway.
- **[DEL-05](../infrastructure/agentic/delegation-chains.md)** propagates user identity through the chain via signed tokens.
- **[DEL-03](../infrastructure/agentic/delegation-chains.md)** limits delegation depth, reducing the number of hops where context can degrade.

These controls handle the *structural* dimension of the problem: permissions, identity, chain depth. They do not handle the *semantic* dimension: the loss of intent, the softening of constraints, the reframing of scope.

A system can pass every DEL check and still exhibit agentic drift. The user's identity propagated correctly. The permissions intersected correctly. But the *meaning* of the request changed as it moved through the chain, and the final agent operated within its permissions on data the user never intended it to access.

## Detecting Agentic Drift

### Intent comparison across hops

The most direct detection method. Capture the task description at each delegation hop and compare them semantically. If the task at hop 3 has lost constraints that were present at hop 1, flag it.

This requires the [Objective Intent Specification](../maso/controls/objective-intent.md) (OISpec) to travel with the chain, not just the user identity. The OISpec is the "what should happen" against which each hop's task description can be compared.

| Hop | Task Description | Drift Signal |
|-----|-----------------|--------------|
| 0 (user) | "Summarise Q1 revenue for my EMEA accounts" | Baseline |
| 1 (orchestrator) | "Retrieve Q1 revenue, EMEA region, user's accounts only" | None |
| 2 (data agent) | "Query Q1 revenue for EMEA" | **Scope constraint dropped**: "user's accounts" missing |
| 3 (summariser) | "Summarise the revenue data" | **Region constraint dropped**: "EMEA" missing |

### Constraint propagation tracking

Attach a structured constraint set to the delegation context alongside the natural-language task description. At each hop, the gateway verifies that the downstream task's constraints are a subset of (or equal to) the upstream constraints. Any constraint that disappears triggers an alert.

```yaml
# Constraint set propagated with delegation
constraints:
  - type: data_scope
    field: region
    value: EMEA
    source: user_request
  - type: data_scope
    field: account_owner
    value: user:jgill@example.com
    source: user_request
  - type: access_level
    value: read_only
    source: iam_policy
```

If a downstream agent's task description does not reference or enforce all constraints in this set, the gateway can block the delegation or escalate for review.

### Output scope validation

Compare the scope of the final output against the scope of the original request. If the user asked about "my accounts" and the output contains data from accounts belonging to other users, agentic drift has occurred, regardless of whether each individual hop looked correct.

This is a post-hoc check. It catches drift that slipped past hop-level detection but only after the damage is done. It is a necessary backstop, not a primary control.

## Mitigating Agentic Drift

### 1. Carry structured constraints, not just natural language

Natural-language task descriptions will always be lossy. Supplement them with a machine-readable constraint set that travels with the delegation context. The constraint set is authoritative. If the natural-language description and the constraint set disagree, the constraint set wins.

This extends [DEL-01](../infrastructure/agentic/delegation-chains.md)'s permission intersection to include *semantic* constraints, not just *structural* permissions.

### 2. Bind the OISpec to the delegation chain

The [Objective Intent Specification](../maso/controls/objective-intent.md) should be attached to every delegation chain at initiation and verified at every hop. The OISpec declares what the user intended. Each agent's task should be evaluated against it, not just against the previous agent's instructions.

This prevents the "telephone game" problem where each agent only sees what the previous agent passed along. Every agent in the chain has access to the original intent.

### 3. Limit natural-language delegation

Where possible, use structured delegation interfaces rather than free-text task descriptions. A structured interface forces the delegating agent to populate specific fields (scope, constraints, permitted actions), making it harder to accidentally drop context.

```json
{
  "task": "retrieve_revenue_data",
  "parameters": {
    "period": "Q1-2026",
    "region": "EMEA",
    "account_filter": "owner:jgill@example.com"
  },
  "constraints": ["read_only", "no_aggregation_across_owners"],
  "oispec_ref": "oi-2026-03-4821"
}
```

### 4. Shorten chains

Every hop is a lossy compression step. Fewer hops means less context loss. The [DEL-03](../infrastructure/agentic/delegation-chains.md) depth limits exist for auditability and blast radius, but they also serve as a drift control. Keep chains as shallow as the task allows.

### 5. Implement hop-level Judge evaluation

Deploy the [Judge](../core/judge-assurance.md) at agent boundaries, not just at the system edge. The Judge at each hop compares the downstream task against the OISpec and the upstream constraint set. This catches drift in real time rather than post-hoc.

This is the "distributed guardrails" pattern described in [When Agents Talk to Agents](when-agents-talk-to-agents.md), applied specifically to context preservation rather than content safety.

### 6. Monitor for drift patterns in telemetry

Use the [observability controls](../maso/controls/observability.md) to track constraint survival rates across delegation chains. If a particular agent consistently drops constraints, that is a systemic issue to fix, not a one-off anomaly.

Useful metrics:

- **Constraint survival rate**: percentage of original constraints present at each hop
- **Scope expansion incidents**: cases where the output scope exceeded the input scope
- **OISpec deviation score**: semantic distance between the OISpec and the final task description

## The Relationship to Human Oversight

Agentic drift makes [human oversight](humans-remain-accountable.md) harder because the drift is subtle. A human reviewer looking at the final output may not notice that the scope expanded slightly. The output looks reasonable. The data looks relevant. The fact that it includes accounts the user should not have seen is not obvious without comparing against the original request.

This is why the structured constraint set matters for human reviewers too. A reviewer who can see "original constraint: user's accounts only; final query: all EMEA accounts" has a clear signal. A reviewer who only sees the final summary has nothing to compare against.

## The Bottom Line

Agentic drift is not an attack. It is a property of systems that delegate tasks through natural-language interfaces. It happens because context is lossy, constraints are fragile, and each agent optimises for its local task without full visibility into the original intent.

The structural controls in the framework (permission intersection, identity propagation, depth limits) handle the access control dimension. Agentic drift requires an additional layer: semantic controls that ensure the *meaning* of the request survives the chain, not just the permissions.

The fix is not more guardrails. It is carrying the intent alongside the task, in a form that machines can verify and humans can audit.

!!! info "References"
    - [Temporal Decay](temporal-decay.md) - How correlated model decay compounds with agentic drift in multi-agent systems
    - [Delegation Chain Controls](../infrastructure/agentic/delegation-chains.md) - DEL-01 through DEL-05: structural controls for delegation chains
    - [Multi-Agent Controls](../core/multi-agent-controls.md) - Trust topologies, identity propagation, and circuit breakers
    - [When Agents Talk to Agents](when-agents-talk-to-agents.md) - Accountability gaps and coordination failures in multi-agent systems
    - [Objective Intent Specification](../maso/controls/objective-intent.md) - Machine-readable intent declarations that can travel with delegation chains
    - [MASO Observability Controls](../maso/controls/observability.md) - Per-agent monitoring and drift detection telemetry
