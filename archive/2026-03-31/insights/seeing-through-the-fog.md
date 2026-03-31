# Seeing Through the Fog: Agent Visibility in Complex Environments

*In multi-product, multi-agent environments, the hardest problem isn't controlling agents; it's knowing where they are and what they're doing.*

The [visibility problem](the-visibility-problem.md) establishes a foundational truth: you can't govern what you can't see. That article addresses discovery: finding out what AI exists in your organisation. This article addresses a harder problem: **maintaining continuous, real-time visibility across agents that are distributed across multiple products, platforms, teams, and environments.**

Discovery tells you what you have. Visibility tells you what it's doing right now.

In a single-product environment with three agents, this is straightforward. You instrument them, you watch them, you move on. But production environments aren't staying simple. They're becoming multi-product, multi-vendor, multi-cloud, multi-team estates where agents run across boundaries that your monitoring wasn't designed to cross.

## The Fog of Agents

Enterprise agent deployments are fragmenting across:

| Dimension | Example | Visibility Challenge |
|-----------|---------|---------------------|
| **Products** | Customer service agents, internal IT agents, sales pipeline agents, compliance agents | Each product team builds and instruments independently. No shared schema, no common agent identity. |
| **Platforms** | LangGraph in AWS, AutoGen on Azure, CrewAI on GCP, custom frameworks on-premise | Each platform has its own logging format, its own metrics, its own concept of an "agent." |
| **Teams** | Engineering, operations, marketing, finance, legal | Each team deploys agents with different governance standards, different monitoring maturity, different urgency. |
| **Vendors** | Third-party agents embedded in SaaS products, partner-managed agent services, marketplace agents | You may not control the agent at all. Your visibility depends on what the vendor exposes. |
| **Lifecycle stages** | Development, staging, production, shadow/experimental | Agents in staging may access production data. Experimental agents may escape the sandbox. |

The result is a fog. Not complete darkness; you have partial views from each product, platform, and team. But no single view of the whole. And the gaps between partial views are exactly where problems hide.

This isn't a theoretical concern. It's the operational reality of any organisation running agents across more than one product or team.

## Why Partial Visibility Is Dangerous

Partial visibility creates specific failure modes that full blindness or full visibility don't:

**You detect the symptom in one product but miss the cause in another.** Agent A in the customer service product starts producing degraded outputs. Your monitoring catches it. But the root cause is Agent X in the data pipeline product, which corrupted a shared knowledge base three hours ago. Without cross-product visibility, you troubleshoot Agent A while Agent X continues poisoning data for every other consumer.

**You see individual agents but miss the system.** Each product team monitors its own agents. Each reports green. But the emergent behavior across products, where the output of one product's agents feeds into another product's agents, is unmonitored. The inter-product agent interaction is a blind spot by design, because nobody owns it.

**You optimise locally and degrade globally.** The sales team tunes its agents for speed. The compliance team tunes its agents for thoroughness. When both interact with the same customer data, the speed-optimised agent races ahead while the compliance agent falls behind. Customer-facing decisions are made before compliance review completes. Each team's dashboard shows healthy performance. The organisation is exposed.

**You lose the thread across boundaries.** A request enters through Product A, triggers an agent in Product B, which delegates to an agent in Product C. The trace ID doesn't propagate across product boundaries. When the final output is wrong, you have three partial logs and no way to stitch them together without manual investigation.

## What You Need to See

Effective visibility across complex environments requires answering five questions continuously, not periodically:

### 1. Where Are They Running?

The most basic question, and the one most organisations can't answer comprehensively.

**What this means in practice:**
- A live inventory of every agent instance, not just agent types, across every environment
- Which infrastructure each agent runs on (cloud account, region, cluster, container)
- Whether agents have moved (redeployed, scaled, migrated) since the last check
- Which agents are ephemeral (spawned for a task, then terminated) and which are persistent

**Why this is hard across products:** Each product manages its own deployment. The customer service platform knows its agents. The data pipeline knows its agents. Nobody maintains the unified view. An agent spawned dynamically by an orchestrator in one product may invoke APIs that trigger agents in another product, and neither product's inventory captures the cross-boundary interaction.

**The minimum viable answer:** A centralised agent registry that every deployment pipeline writes to. Not a periodic scan, but a real-time feed. Every agent that starts, registers. Every agent that stops, deregisters. Every agent that's discovered outside the registry is flagged.

### 2. What State Are They In?

Running agents exist in states that matter for governance:

| State | Governance Implication |
|-------|----------------------|
| **Active (processing)** | Normal. Monitor for anomalies. |
| **Active (waiting)** | May be holding resources, connections, or locks. Monitor for timeouts. |
| **Active (escalated)** | In a PACE transition. Requires attention. |
| **Degraded** | Operating with reduced capability. May be in Alternate or Contingency mode. |
| **Suspended** | Intentionally paused. Verify it stays paused. |
| **Failed** | Terminated abnormally. Verify no side effects persist. |
| **Unknown** | The worst state. The agent exists, but you can't determine its condition. |

In a single-product environment, state is typically visible in the orchestrator's dashboard. In a multi-product environment, states are tracked in different systems with different definitions. "Degraded" in one product might mean "serving cached results." In another, it might mean "making decisions without guardrails." The same word, different risk.

**The minimum viable answer:** A common state taxonomy that all products map to. Not a replacement for product-specific states, but an overlay that normalises them for cross-product visibility.

### 3. What Are They Doing?

State tells you the agent is active. Behaviour tells you what it's doing with that activity.

**Cross-product behavioral visibility requires:**

- **Action streams:** What tools each agent is invoking, what data it's accessing, what outputs it's generating, in a format that can be correlated across products
- **Decision traces:** The reasoning chain behind agent actions, at sufficient granularity for investigation but not so verbose that it's unusable
- **Interaction maps:** Which agents are communicating with which other agents, across product boundaries, and what data flows between them
- **Deviation signals:** Where current behaviour diverges from baseline, scored and prioritised, not raw alerts

This is where the [MASO observability controls](../maso/controls/observability.md) provide the specification. The challenge in complex environments is implementing those controls consistently across products that were built independently, by different teams, at different times, with different architectures.

**The honest reality:** You will not achieve uniform behavioral visibility across all products simultaneously. Prioritise by risk. The product with the highest-risk agents gets instrumented first, to the full OB specification. Lower-risk products get minimum viable logging with a path to full instrumentation.

### 4. How Are They Connected?

In multi-product environments, the most dangerous visibility gap is the connections between agents across product boundaries.

**What you need to map:**
- **Direct connections:** Agent A in Product X calls Agent B in Product Y via API
- **Indirect connections:** Agent A writes to a shared data store; Agent B reads from the same store. They're connected, but neither knows the other exists
- **Transitive connections:** Agent A triggers Agent B triggers Agent C. Agent A has no visibility into Agent C's existence or behaviour, but is causally responsible for its activation
- **Vendor connections:** Your agent sends data to a vendor API. The vendor's agent processes it. You have no visibility into what happens on the vendor side, but you're accountable for the data you sent

The [graph-based monitoring](../extensions/technical/graph-based-agent-monitoring.md) approach becomes essential here. Flat log analysis cannot surface connection patterns across product boundaries. Graph structures, where agents are nodes and interactions are edges, make hidden relationships visible.

**The minimum viable answer:** A cross-product interaction graph, updated in real time, that shows every agent-to-agent connection (direct, indirect, and transitive). When a new edge appears that hasn't been seen before, it's flagged for review. When an edge's data volume spikes, it's flagged for investigation.

### 5. What Is Their Blast Radius?

If this agent fails or is compromised right now, what's affected? That question is easy to answer for a single agent in a single product. It's much harder when agents span products.

**Blast radius in complex environments includes:**
- **Direct impact:** The product the agent serves
- **Data impact:** Every data store the agent can read from or write to, across products
- **Downstream impact:** Every agent and system that consumes this agent's outputs, including agents in other products that the team may not even know about
- **Cascading impact:** If this agent's failure triggers PACE transitions in connected agents, what's the aggregate availability impact?

Without cross-product visibility, blast radius calculations are incomplete by definition. You know what breaks in your product. You don't know what breaks in products downstream.

## The Unified Visibility Architecture

Achieving cross-product, cross-platform agent visibility requires an architecture that doesn't depend on every product using the same tools.

### The Three Layers

![Unified Visibility Architecture](../images/seeing-through-fog-visibility-layers.svg)

**Product Layer:** Each product continues using its own agent framework, logging system, and monitoring tools. You don't rip and replace. You instrument.

**Normalisation Layer:** Translates product-specific telemetry into a common schema. This is where the hard integration work happens:

| Function | What It Does | Why It's Hard |
|----------|-------------|---------------|
| **Schema mapping** | Maps product-specific log formats to a common event model | Every product has different field names, different granularity, different semantics for the same concepts |
| **Identity resolution** | Connects agent identities across products (Agent "customer-helper-01" in Product A is the same entity as "svc-agent-7" in Product B's logs) | Products assign their own agent IDs. No shared namespace exists without explicit coordination |
| **Trace stitching** | Connects distributed traces across product boundaries | Requires trace context propagation standards (W3C Trace Context, OpenTelemetry) adopted consistently |
| **State mapping** | Translates product-specific states to the common taxonomy | Requires agreement on what "degraded" or "failed" means across teams |
| **Time synchronisation** | Aligns timestamps across products running in different infrastructure | Clock skew across cloud accounts and regions can make causal ordering ambiguous |

**Unified Visibility Layer:** Consumes normalised telemetry and provides the cross-product view. This is where the five questions get answered. This layer doesn't replace product-level monitoring; it provides the view that product-level monitoring structurally cannot.

### The Agent Identity Problem

Cross-product visibility depends on knowing that an agent in one product is the same agent referenced in another product's logs. This sounds trivial. It isn't.

Consider: Product A's orchestrator delegates a sub-task to an API. That API is Product B, which invokes its own agents to fulfill the request. Product A's logs show an outbound API call. Product B's logs show an inbound request triggering agent activity. Without a shared correlation ID, these are two unrelated events in two separate systems.

**Solutions, in order of increasing maturity:**

1. **Correlation by timing and endpoint.** Match Product A's outbound call timestamp and destination with Product B's inbound request. Brittle, doesn't scale, breaks under load.

2. **Shared trace context.** Product A propagates a trace ID (W3C Trace Context or equivalent) in its API call. Product B records that trace ID alongside its agent activity. The normalisation layer stitches the traces. Requires every inter-product integration to propagate context headers.

3. **Centralised agent registry with global IDs.** Every agent instance, across all products, registers with a central registry and receives a globally unique identity. Inter-product interactions reference global IDs, not product-local names. Requires organisational coordination and pipeline integration, but is the only approach that scales reliably.

## What to Instrument First

You won't instrument everything at once. Prioritise based on where the gaps are most dangerous.

### Priority 1: Cross-Product Boundaries

The gaps between products are where visibility fails most and where incidents are hardest to investigate. Instrument every inter-product agent interaction first:
- What data crosses the boundary
- Which agent sent it and which agent received it
- Whether the receiving agent validated the input or trusted it implicitly

### Priority 2: Shared Data Stores

Agents in different products that read from or write to the same data stores are indirectly connected. Map these connections. Monitor for:
- Concurrent access by agents from different products
- Write patterns that could corrupt data consumed by other products' agents
- Data stores that have become implicit coordination channels between agents that were never designed to interact

### Priority 3: Ephemeral Agents

Agents that are spawned dynamically (by orchestrators, by workflow engines, by event-driven architectures) are the hardest to track and the easiest to miss. They exist for the duration of a task and disappear. Without real-time registry updates, they're invisible.

Priority here means: ensure every agent spawning mechanism (orchestrator, serverless trigger, container scheduler) writes to the registry at creation time, not after task completion.

### Priority 4: Vendor-Managed Agents

Agents running inside vendor products give you the least visibility and the least control. You're dependent on vendor telemetry, which varies from comprehensive (full API logs, event webhooks) to minimal (monthly usage reports) to nonexistent.

**What you can do:**
- Require vendor telemetry as a procurement condition (see [the supply chain problem](the-supply-chain-problem.md))
- Monitor what you send to vendor agents and what you receive back, even if you can't see what happens in between
- Treat vendor agent responses as untrusted input, because you can't verify the processing

## The Organisational Dimension

Technical architecture alone doesn't create visibility. Someone has to own the cross-product view.

**The ownership anti-pattern:** Each product team monitors its own agents. The security team monitors the perimeter. Nobody monitors the spaces between products.

**What's needed:** A cross-product agent visibility function, whether it sits in security operations, platform engineering, or a dedicated AI operations team. This function:

- **Owns the unified visibility layer.** Not the products, not the individual agent monitoring, but the cross-product view.
- **Defines the common schema** that the normalisation layer implements. Works with product teams, doesn't dictate to them, but holds the standard.
- **Operates the agent registry.** Ensures every product pipeline registers agents. Flags unregistered agents discovered through network monitoring, API gateway logs, or cross-reference anomalies.
- **Maintains the interaction graph.** Understands which agents connect to which across products. Identifies new connections, unusual patterns, and unmonitored boundaries.
- **Runs cross-product incident investigation.** When an incident spans products, this function has the context to trace across boundaries, because it has the unified view that product teams individually lack.

Without this ownership, cross-product visibility is nobody's job. And nobody's job doesn't get done.

## Metrics That Matter

Visibility needs its own governance metrics, distinct from individual product observability metrics:

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| **Registry coverage** | Percentage of running agent instances registered in the central registry | >95% |
| **Trace completeness** | Percentage of cross-product interactions with end-to-end trace stitching | >90% |
| **Boundary instrumentation** | Percentage of inter-product agent connections with active monitoring | 100% for high-risk, >80% overall |
| **Mean time to correlate** | Time from "anomaly detected in Product A" to "root cause identified in Product B" | <1 hour |
| **Unknown agent detection rate** | Unregistered agents discovered per period | Trending downward |
| **State visibility** | Percentage of agents for which current state is known in the unified layer | >95% |
| **Interaction graph currency** | Lag between a new agent connection forming and it appearing in the graph | <15 minutes |
| **Vendor telemetry coverage** | Percentage of vendor-managed agents with usable telemetry | Tracked, improving |

## The Honest Gaps

Some visibility challenges don't have clean solutions today:

**Cross-vendor agent interactions.** When your agent calls a vendor's agent, which calls another vendor's agent, you lose visibility at the first boundary. Trace context doesn't propagate through third-party systems that don't support it. The best you can do is monitor your boundary and treat everything beyond it as opaque.

**Agent-to-agent communication via unstructured channels.** Agents that communicate through shared documents, databases, or message queues rather than direct API calls create implicit connections that are hard to discover and harder to monitor. These connections only become visible when something breaks.

**Dynamic topologies.** In sophisticated multi-agent systems, the topology itself is dynamic: agents are spawned, connections form, delegation chains extend and contract, all within a single task execution. Static interaction maps can't capture this. You need runtime topology capture that updates as the system operates.

**Cost of comprehensive visibility.** Full instrumentation across every product, every boundary, every agent instance generates significant telemetry volume. Storing, processing, and analysing this data has real infrastructure and operational cost. There's a practical ceiling on how much you can instrument before the monitoring system itself becomes a scaling bottleneck.

**The gap between seeing and understanding.** Even with full visibility, interpreting what you see across a complex multi-agent environment requires expertise that most organisations haven't developed yet. A dashboard full of agent states and interaction graphs is only useful if someone (or something) can distinguish signal from noise.

## The Principle

In simple environments, monitoring is a feature. In complex multi-product, multi-agent environments, **visibility is infrastructure**. It needs to be designed, built, owned, and operated with the same rigour as the agent systems it monitors.

You can't control what you can't see. And in complex environments, what you can't see is most of the system.

## Key Takeaways

1. **Multi-product agent environments create structural blind spots.** Each product has its own monitoring, but nobody monitors the spaces between products. This is where incidents hide and propagate.

2. **Five questions define adequate visibility:** Where are they running? What state are they in? What are they doing? How are they connected? What's their blast radius? If you can't answer all five across product boundaries, your visibility is incomplete.

3. **The normalisation layer is the hard part.** Getting different products to emit telemetry is relatively easy. Normalising that telemetry into a coherent cross-product view (identity resolution, trace stitching, state mapping) is where the integration effort concentrates.

4. **Prioritise boundaries over interiors.** Instrument cross-product interactions and shared data stores before perfecting within-product monitoring. The most dangerous blind spots are at the edges, not the centres.

5. **Someone must own the cross-product view.** Without explicit organisational ownership of unified agent visibility, it becomes nobody's responsibility. Assign it. Staff it. Fund it.

6. **Start with the registry.** A centralised, real-time agent registry is the foundation. Everything else (interaction graphs, blast radius maps, cross-product correlation) depends on knowing what agents exist and where they're running.

## Related

- [The Visibility Problem](the-visibility-problem.md): Discovery, knowing what AI exists in your organisation
- [MASO Observability Controls](../maso/controls/observability.md): Control specifications for agent logging, anomaly scoring, and drift detection
- [Graph-Based Agent Monitoring](../extensions/technical/graph-based-agent-monitoring.md): Using graph structures to detect agent interaction patterns
- [The Orchestrator Problem](the-orchestrator-problem.md): Governance of privileged agents that control other agents
- [When Agents Talk to Agents](when-agents-talk-to-agents.md): Accountability gaps in multi-agent communication
- [Behavioral Anomaly Detection](../extensions/technical/behavioral-anomaly-detection.md): UEBA-style monitoring adapted for AI agents
- [Infrastructure Beats Instructions](infrastructure-beats-instructions.md): Why controls must be enforced at infrastructure level
- [The Supply Chain Problem](the-supply-chain-problem.md): Visibility into AI components you don't control
