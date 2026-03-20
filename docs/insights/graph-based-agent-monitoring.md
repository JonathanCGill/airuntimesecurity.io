---
description: Using an in-memory graph database like Memgraph to model agent interactions as a live graph, detect anomalous behavior through temporal graph analysis, and feed results into PACE escalation in near real-time.
og_title: Graph-Based Agent Monitoring - AI Runtime Security
og_description: How graph databases transform multi-agent observability from log analysis into structural anomaly detection, catching behavioral patterns that tabular monitoring cannot see.
---

# Graph-Based Agent Monitoring: When Relationships Are the Data

*Tabular logs answer "what did Agent X do?" Graph queries answer "how did the system behave?" For multi-agent systems, the second question is the one that matters.*

## The Problem With Logs

The framework's [observability controls](../maso/controls/observability.md) specify comprehensive logging: action audit logs (OB-1.1), inter-agent message logs (OB-1.2), immutable decision chains (OB-2.1), and anomaly scoring (OB-2.2). These are well-designed. They are also, in their default form, tabular.

Tabular logs capture events as rows. Each row records one thing that happened: Agent X called Tool Y at time T with parameters P. For a single agent, that is sufficient. You can query it, trend it, alert on it.

For a multi-agent system, the most important data is not in the rows. It is in the relationships between them. Which agent delegated to which. What communication paths emerged. Whether the topology of agent interaction changed. Whether a trust chain that should be three hops deep is suddenly five. Whether an agent that normally talks to two peers is now talking to seven.

These are structural questions. Answering them from tabular logs requires multi-way joins across session IDs, chain IDs, agent IDs, and timestamps. The queries are expensive, brittle, and slow. And "slow" is a problem when the framework specifies near real-time anomaly scoring (OB-2.2) and cross-agent correlation (OB-3.4).

A graph database does not answer these questions faster. It answers them *naturally*, because relationships are stored as first-class data, not reconstructed from foreign keys at query time.

## Why a Graph

Every observable event in a multi-agent system is a relationship:

| Event | Graph Representation |
| --- | --- |
| Agent A delegates task to Agent B | `(A)-[:DELEGATED {task, permissions, timestamp}]->(B)` |
| Agent B calls a tool | `(B)-[:INVOKED {params, result, latency}]->(Tool)` |
| Agent B sends a message to Agent C | `(B)-[:MESSAGED {content_hash, confidence, provenance}]->(C)` |
| Judge evaluates Agent B's output | `(Judge)-[:EVALUATED {score, flags}]->(B_output)` |
| Agent B accesses a data source | `(B)-[:ACCESSED {query, record_count}]->(DataSource)` |
| Workflow W includes Agents A, B, C | `(W)-[:CONTAINS]->(A), (W)-[:CONTAINS]->(B), ...` |

These are not just log entries. They are a live, queryable model of how the system is behaving right now. The graph *is* the system's interaction topology, updated in real time, and every graph algorithm in the literature becomes a monitoring tool.

![Agent Interaction Graph with Anomaly Detection](../images/insight-graph-agent-monitoring.svg)

## Near Real-Time: Is It Possible?

Yes. And the architecture is not speculative.

In-memory graph databases like [Memgraph](https://memgraph.com/) are designed for exactly this pattern: high-throughput event ingestion with concurrent graph traversal and algorithm execution. The key characteristics:

**Ingestion.** Memgraph supports native Kafka and Pulsar stream connectors. Agent events flow from the message bus (which the MASO framework already mandates) through the stream processor into the graph as nodes and edges. Ingestion latency is typically under 10ms per event.

**Query.** Cypher queries against an in-memory graph execute in single-digit milliseconds for local traversals (neighbourhood queries, path finding) and tens of milliseconds for global algorithms (PageRank, community detection) on graphs with millions of edges. The framework's nine-signal anomaly scoring vector can be computed per agent on every event or on a sub-second polling interval.

**Algorithm execution.** Memgraph includes built-in graph algorithm libraries (MAGE) that run in-process. PageRank, Louvain community detection, betweenness centrality, and temporal pattern matching run without data export or external computation. Results feed directly into alerting logic.

**Total pipeline latency.** The realistic end-to-end time from agent event emission to anomaly alert is under 200ms:

| Stage | Latency | Technology |
| --- | --- | --- |
| Event emission to stream | ~5ms | Agent message bus (already specified) |
| Stream to graph ingestion | ~10ms | Kafka/Pulsar connector |
| Graph update + index | ~5ms | In-memory storage |
| Anomaly algorithm execution | ~50ms | PageRank/Louvain on warm graph |
| Alert evaluation + PACE trigger | ~10ms | Threshold comparison |
| **Total** | **~80ms typical, &lt;200ms worst case** | |

This is well within the framework's near real-time requirements. For comparison, the Model-as-Judge layer adds 500ms to 5 seconds of latency per evaluation. The graph monitoring layer is an order of magnitude faster.

## Four Detection Patterns That Only Graphs Can See

### 1. New Edge to Unknown Target

The simplest and most powerful pattern. If Agent X has a baseline graph showing connections to Tools A, B, C and Agents Y, Z, any new edge to an unknown target is immediately visible:

```cypher
MATCH (a:Agent)-[e:ACTION]->(t:Target)
WHERE e.timestamp > now() - duration('PT1H')
  AND NOT EXISTS {
    MATCH (a)-[b:ACTION]->(t)
    WHERE b.timestamp < now() - duration('P7D')
  }
RETURN a.id, t.id, count(e), a.anomaly_score
```

This catches: exfiltration via new external API calls, tool-chain exploitation (agent reaches tools outside declared scope), and compromised agents being directed to new targets. In tabular logs, this requires a self-join against the full history. In a graph, it is a one-hop neighbourhood comparison.

**Maps to:** OB-2.2 (anomaly scoring, `tool_usage_pattern` signal), OB-3.4 (cross-agent correlation).

### 2. Edge Weight Spike

Agent A normally sends 3-5 messages per session to Agent B. Today it has sent 47. The edge weight (message count, data volume, or token count as a property) has spiked relative to the rolling baseline.

```cypher
MATCH (a:Agent)-[e:MESSAGED]->(b:Agent)
WHERE e.timestamp > now() - duration('PT1H')
WITH a, b, count(e) AS current_count
MATCH (a)-[baseline:BASELINE_COMM]->(b)
WHERE current_count > baseline.mean + (2 * baseline.stddev)
RETURN a.id, b.id, current_count, baseline.mean, baseline.stddev
```

This catches: data exfiltration through inter-agent channels, runaway loops (LLM10), hallucination amplification chains (one agent feeding fabricated data at high volume), and prompt injection causing excessive delegation.

**Maps to:** OB-2.2 (`message_volume` signal), OB-2.5 (cost and consumption monitoring).

### 3. Centrality Shift

In a stable multi-agent system, the orchestrator has high betweenness centrality (most paths go through it) and task agents have low centrality. If a task agent's centrality score suddenly increases, it has become a hub. Something is routing through it that should not be.

```cypher
CALL pagerank.get()
YIELD node, rank
WHERE node:Agent
WITH node.id AS agent_id, rank AS current_rank
MATCH (a:Agent {id: agent_id})
WHERE abs(current_rank - a.baseline_pagerank) > a.centrality_threshold
RETURN agent_id, current_rank, a.baseline_pagerank
```

This catches: delegation chain manipulation (agent accumulates authority by becoming an intermediary), compromised agents being used as proxies, and emergent hub formation that violates the intended trust topology.

**Maps to:** OB-3.4 (`peer_group_deviation` signal), delegation chain controls (DEL-02).

### 4. Community Fragmentation

Louvain community detection identifies clusters of agents that communicate more with each other than with agents outside the cluster. In a well-configured system, communities map to workflows. If an agent migrates from one community to another, or if the community structure itself fragments, the interaction topology has changed.

```cypher
CALL community_detection.get()
YIELD node, community_id
WHERE node:Agent
WITH node.id AS agent_id, community_id AS current_community
MATCH (a:Agent {id: agent_id})
WHERE current_community <> a.baseline_community
RETURN agent_id, current_community, a.baseline_community
```

This catches: workflow boundary violations, agents being recruited into unauthorized collaboration patterns, and slow topology drift that per-agent monitoring misses because no single agent's behavior changes dramatically.

**Maps to:** OB-3.1 (long-window behavioral analysis), OB-3.4 (cross-agent correlation).

## The Temporal Dimension

Static graph analysis tells you what the interaction topology looks like right now. Temporal graph analysis tells you how it is changing. Both matter, but temporal analysis catches the attacks that static analysis cannot.

### Sliding Window Comparison

The framework specifies three temporal windows: 7-day rolling (OB-2.3), 30-day trend (OB-3.1), and 90-day trend with anchor points (OB-3.1). In a graph database, each window becomes a graph snapshot:

| Window | Graph Operation | What It Detects |
| --- | --- | --- |
| **Real-time vs 7-day** | Diff current graph topology against 7-day rolling baseline | Sudden changes: new edges, removed edges, weight spikes |
| **7-day vs 30-day** | Compare rolling baseline against monthly trend | Gradual drift that 7-day windows normalise |
| **30-day vs 90-day anchor** | Compare current topology against known-good anchor | Slow drift attacks: 0.5% per week, invisible to short windows, 13% cumulative over 6 months |

Memgraph handles this through temporal edge properties. Each edge carries a timestamp. Baseline graphs are computed as materialized views over time-windowed edge sets. The diff between two temporal snapshots is a graph query, not a batch job.

### Temporal Motif Detection

Beyond aggregate comparison, temporal graph analysis can detect specific sequences of interactions that form attack patterns:

![Temporal Motif Detection](../images/graph-agent-temporal-motif.svg)

This is a temporal motif: a specific sequence of edges with temporal ordering constraints. Motif detection on a temporal graph is a single query. On tabular logs, it is a window function with self-joins across four tables, ordered by timestamp, filtered by session. The graph query runs in milliseconds. The SQL query might not finish before the next event arrives.

## Architecture: Fitting the Graph Into the Framework

The graph database does not replace the framework's observability stack. It sits alongside it, consuming the same event stream and producing alerts that feed into the same PACE escalation logic.

![Graph Agent Architecture Pipeline](../images/graph-agent-architecture-pipeline.svg)

The message bus (already mandated by MASO) is the single source of truth. The stream processor (Kafka, Pulsar, or equivalent) fans out to three consumers:

1. **SIEM/SOAR** (OB-2.4) for correlation with non-AI security events
2. **Memgraph** for structural anomaly detection on the live interaction graph
3. **Immutable log store** (OB-2.1) for forensics and regulatory compliance

The graph database is a hot-path analytics layer. It holds the recent interaction graph (7-day window in memory, 30/90-day as periodic snapshots) and runs continuous graph algorithms. Anomaly alerts feed into the PACE escalation logic at the same priority as per-agent anomaly scores.

### What Memgraph Adds That the Existing Stack Does Not

| Capability | Existing Framework | With Graph DB |
| --- | --- | --- |
| Per-agent anomaly scoring | OB-2.2: 9-signal composite vector | Same, but `peer_group_deviation` and `message_volume` computed from graph structure instead of tabular aggregation |
| Cross-agent correlation | OB-3.4: specified but no implementation pattern | Native: community detection, centrality analysis, neighbourhood comparison |
| Delegation chain analysis | DEL-02: logged but analysed post-hoc | Live: chain depth, branching factor, authority accumulation visible as graph properties |
| Topology change detection | Not specified | New: graph diff between temporal snapshots detects structural shifts |
| Temporal motif detection | Not specified | New: attack sequence patterns detected as temporal subgraph matches |

## The UEBA Parallel

The framework already draws the parallel between [User and Entity Behavior Analytics (UEBA)](../maso/controls/observability.md) for human insiders and agent behavioral monitoring. The graph database makes this parallel concrete.

UEBA systems in enterprise security have used graph databases for years. The pattern is established: model entities (users, devices, applications) as nodes, model interactions as edges, compute behavioral baselines as graph properties, and detect anomalies as deviations from the baseline graph.

For agents, the mapping is direct:

| UEBA Entity | Agent Equivalent | Graph Node |
| --- | --- | --- |
| User | Agent | `:Agent {id, role, tier, anomaly_score}` |
| Device | Runtime environment | `:Runtime {provider, model, version}` |
| Application | Tool | `:Tool {name, scope, permissions}` |
| Data store | Data source | `:DataSource {classification, access_policy}` |
| Network destination | External API | `:ExternalAPI {endpoint, approved}` |

| UEBA Behavior | Agent Equivalent | Graph Edge |
| --- | --- | --- |
| Login | Session start | `[:STARTED_SESSION]` |
| File access | Data source query | `[:ACCESSED]` |
| Email sent | Inter-agent message | `[:MESSAGED]` |
| Privilege escalation | Permission request | `[:REQUESTED_PERMISSION]` |
| Lateral movement | Delegation chain hop | `[:DELEGATED]` |

The graph algorithms that detect insider threats in UEBA (anomalous access patterns, unusual communication partners, privilege accumulation, lateral movement paths) transfer directly to agent monitoring. The threat model is the same. The detection patterns are the same. The technology is the same.

## Implementation Considerations

### Graph Size and Retention

An in-memory graph database requires data discipline. Not every log event belongs in the hot graph. A practical retention strategy:

| Data | In-Memory (Memgraph) | Cold Storage (Log Store) |
| --- | --- | --- |
| Current interaction topology | Always | Also persisted (OB-2.1) |
| 7-day rolling edge history | Full edges with properties | Full content |
| 30-day baseline graph | Aggregated edges (counts, means, stddevs) | Full content |
| 90-day anchor snapshot | Topology only (nodes, edges, no content) | Full content |
| Historical forensic data | Not stored | Retained per policy |

For a system with 50 agents, 20 tools, and 10 data sources, the 7-day in-memory graph typically stays under 1GB even with full edge properties. This is well within Memgraph's operational range on a single node.

### Baseline Calibration

The graph-based anomaly detection is only as good as the baseline it compares against. The framework's Tier 1 controls (OB-1.3: weekly manual review, OB-1.4: output quality log) exist specifically to build this baseline during the supervised phase.

A practical calibration sequence:

1. **Week 1-4 (Tier 1).** Ingest all events into the graph. No alerting. Build the interaction topology. Record graph snapshots as candidate baselines.
2. **Week 4-8.** Run anomaly algorithms against the baseline. Review every alert manually. Tune thresholds. The framework specifies OB-1.3 weekly review for this purpose.
3. **Week 8+.** Promote to automated alerting. Per-agent anomaly scores from the graph feed into the composite OB-2.2 vector. PACE escalation thresholds apply.
4. **Ongoing.** Preserve anchor snapshots at known-good states (post-audit, post-validation). Compare rolling baseline against anchors per OB-3.1.

### Alternative Technologies

Memgraph is the strongest fit for this pattern because of its in-memory architecture and native stream processing. But the approach is not Memgraph-specific:

| Technology | Fit for This Pattern | Trade-offs |
| --- | --- | --- |
| **Memgraph** | Purpose-built for real-time streaming graph analytics | Requires in-memory capacity; newer ecosystem |
| **Neo4j** | Mature graph database with extensive algorithm library | Disk-based by default; streaming requires GDS + external connectors; higher latency for real-time |
| **Amazon Neptune** | Managed graph service | Higher query latency; limited algorithm support; vendor lock |
| **Apache AGE (PostgreSQL)** | Graph queries on existing PostgreSQL | Leverages existing infrastructure; limited algorithm support; not designed for streaming |
| **TigerGraph** | High-performance distributed graph | Strong for large-scale analytics; complex deployment; enterprise pricing |

The choice depends on existing infrastructure, team expertise, and scale. For the near real-time requirement specified by the framework, an in-memory solution (Memgraph or equivalent) is the natural starting point.

## What This Enables for PACE

The graph-based monitoring layer gives PACE transitions structural awareness, not just metric thresholds.

| PACE Phase | Graph-Informed Trigger |
| --- | --- |
| **Primary** | Graph topology matches baseline. All communities stable. No unknown edges. Centrality distribution normal. |
| **P to A** | Graph anomaly detected: new edges to unknown targets, centrality shift, community fragmentation, or edge weight spike above 2 sigma. Anomalous agent isolated. Graph query identifies all agents in the affected subgraph for quarantine. |
| **A to C** | Multiple correlated graph anomalies across agents. Community structure has changed. Graph diff against 30-day baseline shows topology divergence beyond threshold. Multi-agent orchestration suspended. |
| **C to E** | Graph analysis confirms propagation: anomalous agent's outputs have been consumed by downstream agents (reachability query). Blast radius computed from graph traversal. All reachable agents terminated. |

The critical capability: when PACE transitions from Alternate to Contingency, the graph can answer "which other agents are affected?" in a single reachability query. In tabular logs, this requires reconstructing delegation chains from chain IDs across multiple log tables. In a graph, it is:

```cypher
MATCH path = (compromised:Agent {id: 'agent-analyst-01'})-[:DELEGATED|MESSAGED*1..5]->(downstream)
WHERE ALL(r IN relationships(path) WHERE r.timestamp > $incident_start)
RETURN downstream.id, length(path) AS hops
```

One query. Milliseconds. The entire blast radius is visible.

## Key Takeaways

1. **Multi-agent observability is a graph problem.** The most important signals are structural: who talks to whom, through what paths, with what frequency, and how that topology changes over time. Graph databases model this natively. Tabular databases reconstruct it expensively.

2. **Near real-time is achievable.** In-memory graph databases with stream connectors (Memgraph + Kafka) deliver sub-200ms end-to-end latency from agent event to anomaly alert. This is faster than the Model-as-Judge layer and well within the framework's requirements.

3. **Four detection patterns emerge from graph structure.** New edges to unknown targets, edge weight spikes, centrality shifts, and community fragmentation catch behavioral anomalies that per-agent metric monitoring cannot see, because they exist in the relationships, not in the individual agents.

4. **The UEBA parallel is direct.** Enterprise security has used graph-based behavioral analytics for human insider threat detection for years. The same entities, relationships, algorithms, and detection patterns transfer to agent monitoring with minimal adaptation.

5. **The graph makes PACE transitions structural.** When an anomaly triggers escalation, the graph answers "what is the blast radius?" as a reachability query instead of a log reconstruction exercise. Containment decisions are faster and more precise.

6. **Baseline calibration is the prerequisite.** The graph is only as good as the baseline it compares against. The framework's Tier 1 supervised phase (OB-1.3, OB-1.4) is where the baseline graph is built. Skipping supervised operation to go directly to automated alerting produces false positives and missed anomalies.

## Related

- [Observability Controls](../maso/controls/observability.md) - the full OB-1.x through OB-3.x control set
- [PACE Resilience](../PACE-RESILIENCE.md) - structured degradation when controls detect anomalies
- [The Hallucination Boundary](the-hallucination-boundary.md) - when the outputs the graph is monitoring cross from tolerable to catastrophic
- [The Verification Gap](the-verification-gap.md) - why monitoring outputs alone is insufficient
- [Prompt, Goal and Epistemic Integrity](../maso/controls/prompt-goal-and-epistemic-integrity.md) - the epistemic controls that generate the events the graph monitors
- [Infrastructure Beats Instructions](infrastructure-beats-instructions.md) - why structural monitoring outperforms behavioral guidelines

