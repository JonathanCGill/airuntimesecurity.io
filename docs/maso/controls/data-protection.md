---
description: "MASO data protection controls: classifying and controlling data flows between agents, securing shared knowledge bases, and preventing cross-agent data leakage."
---

# MASO Control Domain: Data Protection

> Part of the [MASO Framework](../README.md) · Control Specifications
> Covers: LLM02 (Sensitive Info Disclosure) · LLM04 (Data/Model Poisoning) · ASI06 (Memory & Context Poisoning) · LLM08 (Vector/Embedding Weaknesses)
> Also covers: DR-02 (RAG Poisoning/Corpus Drift) · DR-03 (Derived Data Elevation)

## Principle

Data flows between agents must be classified, controlled, and monitored. An agent's access to data is determined by its own classification level, not by the classification of the agent that sent the data. Shared knowledge bases are integrity-checked. Persistent memory is isolated per agent and has a finite lifespan.

In a multi-agent system, every inter-agent message is a data transfer across a trust boundary. The message bus is not just a communication channel - it is the primary data loss prevention enforcement point.

## Why This Matters in Multi-Agent Systems

**Implicit data flows through delegation.** When Agent A asks Agent B to summarise a document, Agent A's context - including any sensitive data it has processed - may leak into the request. Agent B, which may have a lower data classification, now has access to data it shouldn't see. The developer didn't intend a data transfer; the delegation created one.

**RAG poisoning scales across agents.** A poisoned document in a shared vector database doesn't just affect one model - it affects every agent that queries that database. In a multi-agent system, the poisoned data can be retrieved by one agent and passed to others through the message bus, amplifying the poisoning across the entire orchestration.

**Memory becomes a persistent attack surface.** If agents have persistent memory across sessions, poisoned data injected in one session persists into future sessions. In single-model systems, this is a context window risk. In multi-agent systems, a poisoned memory in one agent can contaminate others through shared interactions.

**Cross-classification data mixing.** Different agents may legitimately operate at different data classification levels - one processes public data, another processes confidential customer records. Without explicit fencing, the message bus becomes a channel for data to flow from high-classification agents to low-classification agents.

**Derived data elevation (DR-03).** An agent combines two individually non-sensitive data fields - customer ID and purchase history - and the result is PII. An analyst agent aggregates anonymised records and the output is re-identifiable. In multi-agent systems, data passes through multiple processing stages, and each stage can increase the effective classification of the output without any agent recognising the transition. The output is treated at the classification of the inputs, when it should be treated higher. Classification must be reassessed after processing, not just inherited from source data.

## Controls by Tier

### Tier 1 - Supervised

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **DP-1.1** Data classification | Classification applied to all agent data flows (input, output, inter-agent) | At minimum: public, internal, confidential, restricted. |
| **DP-1.2** Logical separation | Agents handling different classification levels do not share context or memory | Enforced by policy at Tier 1; infrastructure at Tier 2. |
| **DP-1.3** Output logging | All agent outputs captured and available for review | Enables post-hoc detection of sensitive data leakage. |
| **DP-1.4** RAG inventory | RAG data sources inventoried per agent | Organisation knows which knowledge bases each agent accesses. |
| **DP-1.5** Data flow diagram | Documented diagram showing what data moves between which agents | Must be maintained when agents or data sources change. |
| **DP-1.6** Classification metadata propagation | Data classification tags travel with data through inter-agent messages | Messages without classification metadata are rejected by the bus. Prevents classification from being lost between agents. |

### Tier 2 - Managed

All Tier 1 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **DP-2.1** DLP on message bus | Inter-agent messages scanned for sensitive data patterns before delivery | PII, credentials, financial data, health data. Messages above recipient's classification are blocked. |
| **DP-2.2** RAG integrity and freshness validation | Knowledge base content checksummed at ingestion; periodic verification including content currency | Changes trigger automated review. Recommended: daily integrity checks. Freshness metadata tracks whether content has been superseded; documents past defined freshness window flagged for review (Amendment: DR-02). |
| **DP-2.3** Infrastructure data fencing | Cross-agent data isolation enforced at platform level | Agent A at "confidential" cannot access Agent B's "restricted" data store, even with application-layer compromise. |
| **DP-2.4** Memory isolation | Per-agent persistent memory isolated; agents cannot read/write other agents' memory | Shared state mediated exclusively through the message bus with DLP scanning. |
| **DP-2.5** Derived data reclassification | Agent outputs are assessed for classification elevation when combining or enriching data from multiple sources | DLP evaluates whether the output classification should be higher than the input classification. Elevation rules defined per data type (e.g., combining identifiers with behavioral data = PII). Elevated data is tagged at the new classification before it enters the message bus (DR-03). |

### Tier 3 - Autonomous

All Tier 2 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **DP-3.1** Real-time RAG integrity | Checksums verified at query time, not just periodically | Retrieval blocked if checksum mismatch at the moment of access. |
| **DP-3.2** Memory decay | Agent persistent memory has a maximum retention window; auto-purged beyond it | Limits the lifespan of poisoned data. Retention windows documented per agent. |
| **DP-3.3** Cross-session memory analysis | Independent analysis agent reviews stored memory entries for poisoning indicators | Operates on separate infrastructure; cannot be influenced by task agents. |
| **DP-3.4** Data provenance chain | Every data item carries provenance metadata: origin, timestamp, agent, transformations | Enables root cause tracing when data integrity issues are detected. |

## Testing Criteria

### Tier 1 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| DP-T1.1 | Classification audit | Every agent's data flows (input, output, inter-agent) have a documented classification. |
| DP-T1.2 | Cross-classification review | Verify no agent processing confidential data shares context with agents at lower classification without explicit approval. |
| DP-T1.3 | Output log completeness | Perform 20 agent actions. Verify all 20 outputs appear in the audit log. |
| DP-T1.4 | RAG inventory accuracy | Compare documented RAG inventory against actual agent configurations. No undocumented sources. |
| DP-T1.5 | Classification metadata | Send 10 inter-agent messages. Verify each carries classification metadata. Send a message without classification metadata and verify it is rejected by the bus. |

### Tier 2 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| DP-T2.1 | DLP detection rate | Send 50 test messages containing known PII patterns through the bus. DLP detection rate ≥ 95%. |
| DP-T2.2 | DLP evasion | Attempt common evasion techniques (Base64 encoding, character substitution, fragmentation). Measure bypass rate. Target: < 10% bypass. |
| DP-T2.3 | RAG integrity and freshness | Modify a document in the RAG store. Verify the integrity check detects the modification within the defined schedule. Also: mark a document as superseded. Verify the freshness check flags it for review. |
| DP-T2.4 | Cross-agent data fencing | From within an agent's execution environment, attempt to access another agent's data store. Access is blocked at the infrastructure level. |
| DP-T2.5 | Memory isolation | From within an agent, attempt to read another agent's persistent memory. Read is blocked. |
| DP-T2.6 | Derived data elevation | Agent combines two non-sensitive fields (e.g., anonymised ID + location history) that together constitute PII. Verify the output is reclassified at the higher level before entering the message bus. |

### Tier 3 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| DP-T3.1 | Real-time RAG integrity | Modify a RAG document. Immediately attempt retrieval. Retrieval is blocked due to checksum mismatch. |
| DP-T3.2 | Memory decay enforcement | Write a memory entry. Wait for the retention window to expire. Verify the entry is purged. |
| DP-T3.3 | Memory poisoning detection | Inject a deliberately inconsistent memory entry. Verify the cross-session analysis agent flags it within the configured analysis interval. |
| DP-T3.4 | Provenance chain verification | Trace a data item end-to-end from ingestion through agent processing to final output. All provenance metadata is present and consistent. |

## Maturity Indicators

| Level | Indicator |
|-------|-----------|
| **Initial** | No data classification on agent data flows. Agents share RAG sources without access controls. No DLP on inter-agent communication. |
| **Managed** | Data classification applied. RAG sources inventoried. Agent outputs logged. Data flow diagram exists. |
| **Defined** | DLP active on message bus. RAG integrity validated on schedule. Cross-agent data fencing enforced at infrastructure level. Per-agent memory isolation. |
| **Quantitatively Managed** | DLP detection rate measured and reported. RAG integrity check frequency and results tracked. Memory isolation tested regularly with documented results. |
| **Optimising** | Real-time RAG integrity at query time. Memory decay policies with documented rationale. Independent memory analysis agent. Full data provenance chain. |

## Environment Containment: Data Controls

The controls above govern data flows within the agent orchestration. The controls below govern the data systems agents connect to. Both are necessary. Data-layer environment controls remain effective even when the agent is compromised, because they do not depend on the agent's cooperation.

For the full strategy, see [Environment Containment](../environment-containment.md).

### Database-Level Containment

Agent-accessible database operations should execute through **stored procedures**, not dynamic SQL. The agent cannot construct arbitrary queries. It can only invoke pre-defined operations with validated parameters. This eliminates SQL injection as an attack class entirely, regardless of what the agent attempts.

**Parameterized queries** with typed parameters prevent the agent's input from being interpreted as SQL, even where stored procedures are not feasible.

**Row-level security** at the database layer enforces access boundaries independently of the application. If the application layer is compromised (through prompt injection, for example), the database still enforces that the agent cannot read or modify data outside its permitted scope.

**Database constraints** (CHECK, FOREIGN KEY, UNIQUE, NOT NULL) enforce business rules at the storage layer. An agent that attempts to insert invalid data, violate referential integrity, or create duplicate records is stopped by the database itself.

**Read replicas** for read-heavy agents remove write access at the infrastructure level. The agent cannot accidentally or intentionally modify production data through a read replica. This is a structural guarantee, not a policy.

### Opaque Error Responses from Data Systems

Database and API error responses to agents should return success or failure only. No SQL error messages, no schema details, no internal column names. Full diagnostics are logged server-side for human operators. This prevents the agent from using error messages to map the database schema or infer access control boundaries.

### Kill Switch on Data Anomalies

DLP alerts, fraud detection alerts, and database-level anomaly detection (unusual query volume, access to normally untouched tables, bulk data reads) should feed into an automated kill switch that terminates agent access within 30 seconds. The kill switch operates at the infrastructure level (credential revocation, network block), not through the agent's cooperation.

## DLP Beyond the Message Bus

MASO's DLP controls (DP-2.1) scan inter-agent messages within the orchestration. This is necessary but not sufficient. DLP applies in both directions - inbound and outbound - and the controls outside the AI system play an equally important role.

**Inbound DLP.** Your organisation's network DLP, email DLP, and endpoint DLP should prevent sensitive data from reaching agents that shouldn't have it. If a user pastes classified material into an agent's input, network-level DLP catching it before it reaches the model is a faster and more reliable defence than relying on the agent's input guardrails alone.

**Outbound DLP.** If an agent exfiltrates data through a tool call, API request, or generated output, the message bus DLP (DP-2.1) is the first catch point. But network-level DLP, API gateway validation, and database access controls are the second. An agent that constructs a malformed API call or an overly broad database query should be stopped by the target system's own validation - not just by the orchestration's controls.

**Reporting.** External DLP systems that detect AI-originated data incidents provide a feedback loop. If network DLP catches sensitive data that the message bus DLP missed, that is a signal to tighten DP-2.1 rules. DLP is not a single control - it is a layered strategy, and the AI-specific layer is one part of it.

These external controls are outside the scope of this framework, but they should be included in your threat model, your data flow diagrams (DP-1.5), and your design reviews.

## Common Pitfalls

**Classifying agents instead of data flows.** An agent is not "confidential" - it processes data that is confidential. The same agent might process both internal and confidential data depending on the task. Classification must be applied to the data flows, not the agent itself.

**Trusting RAG content because it's internal.** RAG databases are a persistent injection point. An attacker who can modify a document in the knowledge base has a standing injection into every agent that queries it. Integrity validation is not optional.

**Assuming memory isolation from model provider guarantees.** Model providers may offer session isolation, but if your orchestration framework maintains its own context store (which most do), that store is the actual memory surface. The provider's isolation guarantees don't cover your framework's state management.

**Scanning outputs but not inter-agent messages.** DLP on final outputs catches data leakage to end users. But in a multi-agent system, the more dangerous leak path is agent-to-agent - where sensitive data crosses trust boundaries invisibly within the orchestration.

**Inheriting input classification without reassessment.** An agent that combines public customer IDs with internal behavioral data produces output that is neither public nor internal - it's PII. If the output inherits the classification of the higher input ("internal"), it's still under-classified. Classification must be reassessed after processing, particularly when agents combine, enrich, or aggregate data from multiple sources. The output classification may be higher than any individual input.

**Dropping classification metadata between agents.** If classification tags don't travel with data through the message bus, downstream agents and DLP controls have no basis for enforcement. A message arriving without a classification tag should be treated as an error, not as unclassified.

