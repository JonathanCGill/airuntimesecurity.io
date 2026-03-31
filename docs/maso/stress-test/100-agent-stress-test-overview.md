# Stress Testing MASO at Scale

**A Tabletop Methodology for Finding Framework Breakpoints**

> Part of the [MASO Framework](../README.md) · Stress Testing

## What This Is (And What It Is Not)

This is a **tabletop stress test**: a structured thought exercise for identifying where MASO's controls encounter their limits as agent count increases from single digits to triple digits.

No 100-agent system was deployed. The value is in the reasoning: taking the framework's controls and asking *does this still work when the numbers change by an order of magnitude?*

The [worked examples](../examples/worked-examples.md) validate MASO against 5-agent systems. This document asks what happens when agent count grows from a handful to a fleet.

## Why Tabletop Stress Testing Matters

Design intent and operational reality diverge in predictable ways:

- **Linear controls hit quadratic problems.** Output inspection scales linearly. Monitoring communication *between* agents scales with the number of agent pairs, quadratically.
- **Composition creates emergent behavior.** Five agents with well-tested PACE transitions do not guarantee fifty agents degrade gracefully. Cascade dynamics only emerge at scale.
- **Operational cost becomes a constraint.** A Judge evaluation on every inter-agent message is sound architecture. Whether the organisation can afford it at 10,000 messages per second is a question to answer before production.

This exercise helps architects anticipate breakpoints *before* scaling.

## AI Systems May Not Scale Economically

Most AI deployment plans assume pilot-scale economics hold at production scale. This is often wrong, and the failure mode is financial, not technical.

**1. Cost per interaction is non-deterministic.** The same query can cost 2x or 10x more depending on reasoning path, tool calls, conversation depth, and retry loops. At 10,000 concurrent customers, the tail of expensive interactions drives total cost disproportionately.

**2. Security controls scale with risk, not revenue.** A Judge evaluation costs the same whether serving 100 or 10,000 customers. At scale, security control overhead can exceed agent costs. Unlike infrastructure, this overhead cannot be amortised because each interaction requires independent evaluation.

**3. Revenue plateaus before costs do.** During peak trading, customer volume is finite but per-interaction costs keep rising: longer conversations, more retries, more edge cases. The system becomes most expensive precisely when it should be most profitable.

Every dimension in this document has a cost axis. The question is not only *does it still work?* but *can you still afford it?* The [E-Commerce 10K Stress Test](ecommerce-10k-stress-test.md) examines this through a four-phase cost escalation scenario. The [Economic Governance](../../extensions/technical/economic-governance.md) extension provides the enforcement model. **A system that is technically sound but economically unviable under load has failed the stress test.**

## How to Run This Exercise

### Audience

The team responsible for a multi-agent deployment growing beyond a single orchestration cluster: AI/ML engineering lead, security architect/CISO, platform/infrastructure lead, and risk owner.

### Format

Work through each stress dimension below. For each one:

1. **Map it to your system.** Which agents, clusters, and communication paths are affected?
2. **Identify the MASO controls involved.** Use the control references provided.
3. **Assess: linear, quadratic, or breaking?** Does the control scale with agent count, with agent pairs, or does it hit a hard limit?
4. **Determine your threshold.** At what agent count (or message volume, or delegation depth) does the control need architectural adaptation?
5. **Document the adaptation.** What changes - additional infrastructure, modified control parameters, architectural segmentation - would you need?

The stress dimensions are ordered from most likely to surface first (epistemic cascade) to most consequential if missed (kill switch at scale).

## Stress Dimension 1: Epistemic Cascade Depth

### The 5-Agent Reality

In MASO's worked examples, an epistemic failure (hallucinated claim, corrupted data source) passes through at most 4 agents before reaching an output boundary. Controls PG-2.5 (claim provenance), PG-2.7 (uncertainty preservation), and PG-2.4 (consensus diversity gate) are designed to catch degradation within this depth.

### The Scale Question

In a system with 50–100 agents organised into functional clusters, a data point may traverse 8–12 agents across 3–4 clusters before it reaches an external boundary. At each handoff:

- **Uncertainty is stripped** (EP-06). Agent A reports "estimated at 85% (single source, unverified)." Agent B summarises as "approximately 85%." Agent C states "85%." By Agent D, it is treated as established fact.
- **Provenance thins.** Claim provenance tags (PG-2.5) carry source metadata, but each summarisation step abstracts away detail. By the fourth summarisation, the provenance may say "derived from Cluster 1 analysis" - technically accurate but useless for verification.
- **Corroboration is synthetic** (EP-04). If agents in Cluster 2 and Cluster 3 both derive their analysis from Cluster 1's output, their agreement is not independent validation - it is the same source presenting as two. The consensus diversity gate (PG-2.4) catches this if it tracks data lineage, but not if it only checks model diversity.

### What to Assess

- What is the maximum handoff depth in your system from data ingestion to external output?
- At that depth, does PG-2.7 (uncertainty preservation) still carry meaningful confidence metadata, or has it been summarised into meaninglessness?
- Does your PG-2.4 (consensus diversity gate) check data lineage, or only model provider diversity?
- At what depth would you need to introduce a mandatory re-verification checkpoint - an agent that goes back to primary sources rather than trusting the chain?

### MASO Controls Under Stress

| Control | Designed For | Stress Point |
|---------|-------------|-------------|
| PG-2.5 Claim provenance | Tracing claims to sources | Provenance metadata degrades through successive summarisation |
| PG-2.7 Uncertainty preservation | Carrying confidence levels | Confidence qualifiers stripped at each handoff |
| PG-2.4 Consensus diversity gate | Detecting false consensus | May check model diversity but miss shared data lineage |
| PG-2.6 Self-referential evidence prohibition | Preventing circular validation | Harder to detect when the circle spans 4 clusters |

## Stress Dimension 2: Delegation Graph Complexity

### The 5-Agent Reality

MASO's identity and access controls (IA-2.3 no transitive permissions, IA-2.1 zero-trust credentials) are demonstrated against delegation graphs with ~20 edges. Permission policies can be reviewed manually. Misconfiguration is visible.

### The Scale Question

At 100 agents, the potential delegation graph has up to ~10,000 edges. Even if most are unused, the *policy surface* - the set of rules defining who can delegate what to whom - grows with the number of agent pairs. Consider:

- **Policy complexity.** Each delegation rule specifies: source agent, target agent, permitted scope, maximum permissions, time limit. At 100 agents, the policy set may contain thousands of rules. Auditing this manually is not feasible.
- **Delegation contracts at speed.** At Tier 3, every delegation creates a cryptographically signed contract (source, scope, permissions, time limit, expected output). If agents delegate tasks hundreds of times per minute, the signing and validation overhead may become a latency bottleneck.
- **Transitive path detection.** IA-2.3 prohibits transitive permissions, but detecting a transitive path through 4–5 intermediate agents requires graph analysis on every delegation request. The computational cost of this analysis grows with graph size.

### What to Assess

- How many active delegation paths does your system have? (Not theoretical maximum - actual observed paths.)
- Can your policy engine evaluate delegation requests within your latency budget?
- Do you have automated tooling to detect transitive permission paths, or is this a manual review?
- At what agent count would you need to move from point-to-point delegation policies to role-based or cluster-based delegation models?

### MASO Controls Under Stress

| Control | Designed For | Stress Point |
|---------|-------------|-------------|
| IA-2.3 No transitive permissions | Preventing privilege laundering | Graph analysis cost grows with delegation depth |
| IA-2.1 Zero-trust credentials | Per-agent authentication | Credential management overhead at 100+ agents |
| Tier 3 delegation contracts | Scoped, time-limited delegation | Signing and validation latency at high delegation frequency |
| EC-2.6 Decision commit protocol | Validating action authority | Must trace authority chain through potentially deep delegation graph |

## Stress Dimension 3: Cross-Cluster PACE Cascades

### The 5-Agent Reality

PACE transitions in the worked examples affect a single orchestration cluster. When one agent enters Alternate, the orchestrator manages the transition. The blast radius is contained within the cluster.

### The Scale Question

When agents are organised into multiple clusters with dependencies between them, a PACE transition in one cluster may force transitions in others:

- **Upstream dependency failure.** If a data-producing cluster (e.g., market intelligence) enters Contingency and stops producing outputs, every downstream cluster that depends on those outputs must decide: operate on stale data, degrade to a fallback data source, or cascade to Contingency themselves.
- **Coordinated degradation.** MASO's three-axis PACE model (horizontal across layers, vertical within layers, orchestration across agents) operates within a single orchestration boundary. It does not define how multiple orchestrators coordinate their PACE states. Does Cluster B's orchestrator even *know* that Cluster A has entered Alternate?
- **Recovery sequencing.** Stepping back up from Contingency to Primary requires confirmed stability. If Cluster A recovers but Cluster B is still degraded because it cascaded from Cluster A's failure, the recovery sequence must be coordinated. The current PACE model does not specify inter-cluster recovery ordering.

### What to Assess

- Map the dependencies between your clusters. Which clusters produce data that other clusters consume?
- For each dependency: what happens to the consuming cluster if the producing cluster enters each PACE phase (A, C, E)?
- Do your cluster orchestrators share PACE state? Is there a system-level PACE coordinator, or does each cluster manage independently?
- Define the cascade rules: does a producing cluster entering Contingency automatically cascade, or does each consuming cluster make its own assessment?
- What is the recovery sequence? Which clusters must recover first?

### MASO Controls Under Stress

| Control | Designed For | Stress Point |
|---------|-------------|-------------|
| PACE three-axis model | Resilience within an orchestration | No defined behavior for inter-cluster cascade |
| OB-3.2 Circuit breaker | Emergency halt for one cluster | Coordinated halt across multiple clusters undefined |
| OB-2.2 Drift detection | Per-agent behavioral baseline | Baseline behavior changes when upstream clusters degrade |

### Potential Framework Extension

MASO may need a **fourth PACE axis: inter-cluster coordination**. This would define:
- Cluster dependency declarations (which clusters depend on which)
- Cascade policies (automatic cascade vs. independent assessment)
- A system-level PACE state that aggregates cluster states
- Recovery sequencing rules

## Stress Dimension 4: Observability at Volume

### The 5-Agent Reality

MASO's observability controls (OB-2.1 anomaly scoring, OB-2.2 drift detection, OB-2.3 communication profiling) are designed to process every inter-agent message. At 5 agents with ~20 communication paths, this is straightforward.

### The Scale Question

At 100 agents, the message volume changes the problem:

- **Message throughput.** If each agent sends an average of 10 messages per minute to other agents, the system generates ~1,000 messages per minute. At peak (e.g., market open, incident response), this may spike to 10,000+ per minute. Every message needs anomaly scoring, drift comparison, and potentially DLP scanning.
- **Anomaly baseline complexity.** Behavioral baselines at 5 agents are 5 profiles. At 100 agents, it is 100 profiles - plus the interaction patterns between agents, which is combinatorial. What constitutes "anomalous" for Agent 47's communication pattern with Agent 83?
- **Alert fatigue.** More agents means more anomaly signals. If each agent generates a false positive alert once per day, 100 agents generate 100 false positives per day. The human review capacity for PACE escalation decisions becomes the bottleneck.
- **Cost.** If every message is evaluated by a Judge model, the observability compute cost may exceed the task compute cost. The framework's [cost and latency guidance](../../extensions/technical/cost-and-latency.md) discusses sampling rates for single-model systems - the same logic applies at scale, but the trade-offs are sharper.

### What to Assess

- What is your expected message volume at steady state and at peak?
- Can your observability infrastructure process this volume within your latency budget?
- What is your anomaly alert rate, and does your team have capacity to review escalations?
- At what volume would you need to move from per-message evaluation to statistical sampling - and what is the risk trade-off of sampling?
- What is the compute cost of full observability vs. the compute cost of the agents themselves?

### MASO Controls Under Stress

| Control | Designed For | Stress Point |
|---------|-------------|-------------|
| OB-2.1 Anomaly scoring | Per-agent anomaly detection | 100 baselines + interaction pattern baselines |
| OB-2.2 Drift detection | Behavioral change detection | Drift thresholds harder to calibrate at scale |
| OB-2.3 Communication profiling | Inter-agent traffic analysis | Volume may require sampling rather than full inspection |
| EC-2.5 Model-as-Judge | Per-action evaluation | Cost scales linearly with message count |

## Stress Dimension 5: Provider Concentration

### The 5-Agent Reality

MASO's model diversity policy (PG-2.9) flags concentration risk when multiple agents use the same provider. At 5 agents across 2–3 providers, diversity is manageable and the risk is limited to correlated errors.

### The Scale Question

At 100 agents, provider allocation becomes a strategic decision with systemic implications:

- **Correlated failure.** If 40 agents use Provider A and Provider A experiences an outage, 40% of the system fails simultaneously. If those 40 agents include infrastructure agents (monitoring, incident response), the system loses both its operational capability and its ability to manage the degradation.
- **Correlated errors.** Agents using the same model produce correlated reasoning errors. At 5 agents, PG-2.4 (consensus diversity gate) catches this. At 40 agents on the same provider, the "consensus" of 40 agents agreeing on a wrong answer is overwhelming - and the 10 agents on other providers that disagree look like outliers, not correctors.
- **Rate limiting cascade.** Providers impose rate limits. At 100 agents making concurrent API calls, a single provider's rate limit may throttle operations across multiple clusters simultaneously, creating correlated latency spikes that look like system degradation.

### What to Assess

- Map your provider allocation. What percentage of agents (and which clusters) depend on each provider?
- If your most-used provider has a full outage, what percentage of your system is affected? Does that include control-plane agents?
- Are your PACE transition agents on a different provider than your task agents?
- At what provider concentration level does PG-2.9 require architectural intervention (separate providers for task vs. control plane)?

### MASO Controls Under Stress

| Control | Designed For | Stress Point |
|---------|-------------|-------------|
| PG-2.9 Model diversity policy | Preventing correlated reasoning errors | Concentration risk amplified at scale |
| PG-2.4 Consensus diversity gate | Detecting false consensus | May be overwhelmed when majority of agents share a provider |
| PACE transition agents | Managing degradation | Must not share providers with task agents |

## Stress Dimension 6: Data Boundary Enforcement

### The 5-Agent Reality

MASO's data protection controls (DP-1.1 classification, DP-2.1 DLP on message bus) enforce data boundaries between agents. At 5 agents with clear roles, the classification rules are straightforward: Agent A handles classified data, Agent B does not, the boundary is between them.

### The Scale Question

In regulated environments with complex information barriers (financial services Chinese walls, healthcare PHI boundaries, legal privilege), the number of boundary rules scales with the complexity of the regulatory environment *and* the number of agent pairs:

- **Rule explosion.** A financial services firm may have 10 information barriers (equity research, M&A, proprietary trading, etc.). At 100 agents, each barrier must be enforced on every relevant communication path. The rule set becomes thousands of entries.
- **Classification propagation.** When Agent A (with access to restricted data) sends a summary to Agent B (without access), has the restricted data been adequately transformed? At each hop, the question of whether derived data inherits the classification of source data requires judgement - and the framework relies on DLP scanning to enforce it.
- **Latency of enforcement.** If every inter-agent message must be scanned against thousands of DLP rules before delivery, the scanning latency becomes a bottleneck on inter-agent communication speed.

### What to Assess

- How many distinct information barriers or data boundaries does your regulatory environment require?
- How many agent pairs cross those boundaries?
- Is message-level DLP scanning viable at your message volume, or do you need architectural segmentation (separate message buses per boundary)?
- How do you handle derived data - does a summary of restricted data inherit the restriction?

### MASO Controls Under Stress

| Control | Designed For | Stress Point |
|---------|-------------|-------------|
| DP-1.1 Data classification | Labelling data by sensitivity | Classification rules scale with barriers x agent pairs |
| DP-2.1 DLP on message bus | Preventing data leakage | Scanning latency at high message volume with many rules |
| DP-1.3 Memory isolation | Preventing cross-boundary data persistence | Memory management complexity grows with agent count |

## Stress Dimension 7: Kill Switch at Scale

### The 5-Agent Reality

MASO's kill switch (OB-3.2) terminates all agents in a confirmed Emergency. At 5 agents in one cluster, termination is fast and the blast radius of in-flight work is manageable.

### The Scale Question

At 100 agents across multiple clusters and potentially multiple geographic regions:

- **In-flight work.** At the moment of kill switch activation, dozens of agents may be mid-task. In financial services, this means in-flight orders, partial settlements, and uncommitted position changes. Killing agents without resolving in-flight work may leave external systems in an inconsistent state.
- **Coordination time.** Terminating 100 agents across 4 data centres is not instantaneous. Network latency alone introduces seconds of delay. During that window, agents that have not yet received the kill signal continue operating.
- **Recovery complexity.** After a kill switch event, every agent's state must be captured, every in-flight transaction must be resolved, and every external system must be reconciled. At 100 agents, this is a major operational event, not a button press.

### What to Assess

- What is the maximum time between kill switch activation and the last agent terminating?
- What in-flight work exists at any given moment, and what is the consequence of abandoning it?
- Do you need a "controlled halt" (resolve in-flight work, then stop) rather than "immediate kill" (stop everything now)?
- Is the kill switch infrastructure itself independent of the agent infrastructure? (If the kill switch runs on the same platform as the agents, a platform failure disables both.)

### MASO Controls Under Stress

| Control | Designed For | Stress Point |
|---------|-------------|-------------|
| OB-3.2 Circuit breaker / kill switch | Emergency termination | Coordination delay across regions; in-flight work resolution |
| Tier 3 isolated kill switch | Independence from agent control plane | Must cover multiple data centres, not just one cluster |

### Potential Framework Extension

MASO may need a **graduated shutdown protocol** for large-scale deployments:
1. **Halt new work** - no new tasks accepted
2. **Drain in-flight work** - allow active tasks to complete within a time limit (e.g., 30 seconds)
3. **Force terminate** - kill remaining agents after the drain window
4. **Reconcile** - automated check of external system state against expected state

## Stress Dimension 8: Compound Attack Surface

### The 5-Agent Reality

The [red team playbook](../red-team/red-team-playbook.md) tests individual attack vectors: prompt injection propagation (RT-01), transitive permission exploitation (RT-02), judge bypass (RT-06), anomaly evasion (RT-10). Each scenario tests one control or control chain.

### The Scale Question

At 100 agents, the attack surface is not 20x larger - it is combinatorially larger. An attacker can chain techniques:

- **Injection + delegation laundering.** Inject a payload into a low-privilege agent (RT-01). The payload instructs the agent to delegate a seemingly benign task to a high-privilege agent (RT-02). The delegated task, once accepted, exploits the high-privilege agent's tool access. The attack crosses 3 agents and 2 control domains (prompt integrity, identity & access).
- **Slow drift + judge evasion.** Gradually shift an agent's behavior over hundreds of interactions (RT-07) while keeping each individual interaction within the anomaly detection threshold (RT-10). Once the agent's behavioral baseline has been sufficiently shifted, exploit the new baseline as "normal."
- **Supply chain + epistemic cascade.** Poison an MCP server (ET-04) that feeds data to a cluster of agents. The poisoned data propagates through the epistemic chain (ET-05) and is corroborated by multiple agents using the same poisoned source. The consensus diversity gate (PG-2.4) does not trigger because the agents use different models - the correlation is in the data, not the models.

### What to Assess

- Have you tested compound attack scenarios, or only individual red team playbook scenarios?
- At your agent count, how many distinct 3-step attack paths exist? (This is a graph analysis problem on your delegation and communication graph.)
- Do your controls detect attack *chains*, or only individual attack *steps*? For example, does your anomaly detection correlate a suspicious delegation request with a prior injection attempt on the delegating agent?
- At what scale would you invest in a dedicated attack-path analysis tool (graph-based threat modelling on your actual agent topology)?

### MASO Controls Under Stress

| Control | Designed For | Stress Point |
|---------|-------------|-------------|
| All RT-01 through RT-13 | Individual attack vector testing | Compound attacks exploit gaps between controls |
| OB-2.1 Anomaly scoring | Per-agent anomaly detection | Does not natively correlate anomalies across agents |
| OB-3.5 Decision traceability | Post-incident chain reconstruction | Useful for forensics, but does not prevent compound attacks in real-time |

## Using This Exercise to Plan Your Deployment

After working through the 8 dimensions, you should have:

1. **A scaling profile for each MASO control**: linear with agent count, quadratic with agent pairs, or hitting hard limits.
2. **Your breakpoints**: the agent count or volume at which you need architectural adaptation.
3. **Architectural decisions**: where you need segmentation, sampling, or new coordination mechanisms.
4. **Cost projections**: operational cost of full MASO compliance at target scale.

These findings feed directly into MASO implementation planning and risk owner sign-off. The controls are the *what*. This exercise plans the *how much* and *at what cost*.

## Relationship to Other MASO Documents

| Document | Relationship |
|----------|-------------|
| [E-Commerce 10K Stress Test](ecommerce-10k-stress-test.md) | Tests depth, volume, and economic pressure (6 agent types, 10,000 customers, 60,000 instances, peak trading cost escalation). Complements this document's breadth focus |
| [Worked Examples](../examples/worked-examples.md) | Validates MASO at 5-agent scale. This document extends that thinking to 50-100+ agents |
| [Red Team Playbook](../red-team/red-team-playbook.md) | Tests individual controls. Stress Dimension 8 asks what happens when those attacks are combined |
| [Tier 3 - Autonomous](../implementation/tier-3-autonomous.md) | Defines the controls required for high autonomy. This document asks which of those controls need adaptation at scale |
| [Cost & Latency](../../extensions/technical/cost-and-latency.md) | Provides single-model cost analysis. Stress Dimension 4 extends that to multi-agent observability cost |
| [PACE Resilience](../../PACE-RESILIENCE.md) | Defines the three-axis PACE model. Stress Dimension 3 identifies the need for a potential fourth axis |

