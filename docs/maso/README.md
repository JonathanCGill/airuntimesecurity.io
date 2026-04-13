---
description: "The Multi-Agent Security Operations (MASO) framework: risk-proportionate, PACE-driven controls for securing multi-model agent orchestration. Select the controls you need. Deselect the ones you do not."
---

# Multi-Agent Security Operations (MASO) Framework

![MASO Hero: Single chatbot security vs multi-agent security operations](../images/maso-hero.svg){ .arch-diagram }

**Risk-proportionate controls for securing multi-model agent orchestration.**

Agentic AI systems are powerful and fragile at the same time. They [reason in natural language, act through tools, and collaborate through delegation](../agentic-agent-anatomy.md). Every one of those capabilities is also an attack surface. MASO exists because agents cannot be trusted to police themselves: something outside the agent must [declare what it should do, constrain what it can do, and evaluate whether it did the right thing](../constraining-agents.md) before irreversible actions are committed.

That evaluation must be proportionate to risk. An agent reading internal documents does not need the same scrutiny as one executing financial transactions. MASO provides the controls, tiers, and resilience model to scale security to consequence. AI product owners can quickly identify the controls relevant to their deployment and consciously deselect those that do not apply. Every organisation has its own way of working, and the framework is designed to fit that context rather than override it.

## MASO Is One Layer, Not the Whole Stack

MASO manages risks specific to AI agents: prompt injection propagation, hallucination amplification, transitive privilege escalation, epistemic failures, and the other threats catalogued in the [Emergent Risk Register](controls/risk-register.md). It does not manage risks in the systems agents connect to. Those systems must have their own controls in place and working.

Agents interact with APIs, databases, message queues, email services, file stores, and third-party endpoints. Every one of those systems must enforce its own security independently of the agent. If an API has no input validation, a database accepts dynamic SQL, or an email service allows unrestricted sending, MASO cannot compensate. The weakness is in the connected system, not in the agent, and no amount of guardrails, Judge evaluation, or human oversight on the agent side will fix a broken API or an unprotected database.

This is no different from ordinary software. A well-architected application with strong internal security is still compromised if it talks to a database with default credentials or an API that returns stack traces in error messages. The same principle applies to agent systems, with one critical difference: **agents are non-deterministic callers.** You cannot predict exactly what an agent will send to an API or query from a database. This makes the receiving system's own defences more important, not less.

**Prevention and detection both matter.** Prevention means the connected systems enforce their own boundaries: strict input validation, stored procedures, parameterized queries, row-level security, request-scoped authorization, opaque error responses. Detection means monitoring systems (DLP, fraud detection, SIEM, WAF) watch agent traffic the same way they watch human traffic, and flag anomalies regardless of origin. If the agent misbehaves, a kill switch external to the agent and its orchestration should terminate all agent activity.

MASO secures the agent. You secure everything the agent touches. Both are necessary. Neither is sufficient alone. The [Environment Containment](environment-containment.md) strategy formalises these requirements into specific controls mapped to each MASO tier.

### Built or Bought: MASO Applies Either Way

MASO is designed for **AI agent systems your organisation operates**, whether you build them from scratch or deploy them on a managed platform. If you are building custom multi-agent systems (using LangGraph, AutoGen, CrewAI, or your own orchestration), MASO provides both the security requirements and the architectural patterns. If you are using a cloud platform's agent orchestration (AWS Bedrock Agents, Azure AI Agent Service), MASO provides the mental model for what security controls should be in place; the platform provides the implementation mechanisms.

The eight control domains, three implementation tiers, and PACE resilience model describe **what needs to be true** for multi-agent AI to be safe. The technical implementation varies by platform and approach. The security model does not.

For AI you consume as a service (copilots, productivity tools, SaaS with embedded AI), MASO's control domains are not directly applicable. Those systems are covered by vendor-side controls and your organisation's data governance. See [Maturity Levels](../strategy/maturity-levels.md) for how the framework addresses consumed AI differently from AI you operate.

## Why Agents Need External Evaluation

Agents are fragile. They reason in natural language, which means they can be misdirected by crafted inputs, drift from their objectives over long task horizons, hallucinate facts with high confidence, and compound each other's errors when they collaborate. These are not bugs. They are properties of how language models work. You cannot patch them out. For a full breakdown of the components and connections that produce this fragility, see [Anatomy of an Agentic Agent](../agentic-agent-anatomy.md).

This fragility means agents cannot be trusted to evaluate their own work. A model that has been manipulated by prompt injection will not detect the manipulation in its own reasoning. An agent that has hallucinated a fact will cite it with the same confidence as a grounded one. Something outside the agent's own ecosystem must assess its actions against what it was supposed to do. That is the role of the judge: an independent model, in a separate trust zone, that observes and rules without participating in the agent's reasoning.

### Evaluation Must Be Proportionate to Risk

Not every agent action needs the same scrutiny. An agent reading a public knowledge base does not warrant the same evaluation rigour as one approving a financial transaction or modifying access controls. Evaluation that is disproportionate to risk wastes money, adds latency, and creates alert fatigue that degrades human oversight.

MASO scales evaluation to consequence:

| Action Risk | Evaluation Approach | Example |
|------------|-------------------|---------|
| **Low** | Guardrails only, async judge sampling | Reading documents, logging notes, internal lookups |
| **Medium** | Pre-action judge evaluation | Sending emails, updating records, calling external APIs |
| **High** | Pre-action judge plus human approval | Issuing payments, modifying permissions, bulk operations |
| **Critical** | Pre-action judge, dual human approval, dry-run | Deploying code, regulatory submissions, irreversible decisions |

An agent processing low-risk read operations can run with guardrails and periodic sampling. An agent making irreversible financial decisions needs pre-action judge evaluation, human approval, and blast radius caps. The [implementation tiers](implementation/tier-1-supervised.md) formalise this progression, and the action classification rules in [Execution Control](controls/execution-control.md) define how each action is routed.

### Declared Intent Is the Judge's Statute Book

A judge is only as good as the law it applies. A human judge ruling on a vague statute produces inconsistent, unpredictable verdicts. The same is true for a judge model. If the agent's purpose is described as "handle customer requests" or "be helpful," the judge has nothing precise to evaluate against. It falls back on generic safety criteria that catch obvious failures but miss subtle deviations from purpose.

The clearer the declaration, the more sound the ruling. When intent is specific ("process refund requests for orders under 90 days, maximum $500, scoped to the returns database"), the judge can verify each element. When outcomes are measurable ("refund issued within policy limits, customer notified, audit trail complete"), the judge can assess success or failure, not just safety. When constraints are explicit ("no access to payment instruments, no external API calls, maximum 50 records per query"), the judge can flag violations precisely.

This is why the [Objective Intent](controls/objective-intent.md) control domain exists. Every agent, judge, and workflow in a MASO deployment operates against a declared Objective Intent Specification (OISpec): a versioned, machine-readable contract defining purpose, outcomes, constraints, and evaluation criteria. These are the reference standard that the entire evaluation architecture depends on.

Three things follow:

**Tactical evaluation** checks individual agents. The judge evaluates each action against the agent's OISpec: does this action match the declared intent, will it satisfy the success criteria, are constraints respected?

**Strategic evaluation** checks combined outcomes. Individual agents may each pass their tactical evaluation while the aggregate workflow fails. A research agent retrieves accurate data, a drafting agent produces well-structured output, but the report contradicts the research because context was lost in the handoff. A strategic evaluator assesses the workflow-level OISpec to catch what per-agent evaluation cannot.

**Asynchronous evaluation** covers what cannot wait. When time constraints or low risk make pre-action evaluation impractical, the judge evaluates after the fact and reports deviations to a human. The action proceeds, but deviations trigger alerts and escalations. The human remains accountable even when the judge cannot rule in advance.

The quality of this entire system depends on the quality of the declarations it evaluates against. Invest in clear, specific, measurable OISpecs and the judge can make sound rulings. Deploy vague specifications and the judge becomes an expensive safety net that catches only the most obvious failures. The foundation is not the model. The foundation is the [declared intent](../constraining-agents.md).

## Architecture

![MASO Architecture](../images/maso-architecture.svg)

### Evaluation Architecture: Inline vs. Offline

![MASO Evaluation Architecture](../images/maso-evaluation-architecture.svg)

The evaluation architecture separates two fundamentally different types of judgment. **Inline evaluation** (left) runs at agent speed using SLMs with measurable criteria: security, privacy, compliance, and business intent. These domains have clear thresholds. When they conflict, security and privacy override business intent. A **Flight Recorder** captures every action, verdict, and reasoning chain.

**Offline evaluation** (right) handles ethics, bias, and fairness. These are policy-driven domains where criteria are set by organisational values, not technical measurement, and where the most important evidence (customer complaints, appeal outcomes, demographic distributions) accumulates over time and is invisible to inline judges. An LLM evaluates sampled decisions retrospectively, statistical monitoring detects portfolio-level patterns, and findings route to human governance for review, investigation, and policy updates that feed back into MASO as guardrail tuning and OISpec revisions.

### Three-Layer Defence

MASO operates on a **three-layer defence model** adapted for multi-agent dynamics:

**Layer 1 - Guardrails** enforce hard boundaries: input validation, output sanitisation, tool permission scoping, and rate limiting. Deterministic, non-negotiable, machine-speed.

**Layer 2 - Model-as-Judge Evaluation** uses a dedicated evaluation model (distinct from task agents) to assess quality, safety, and policy compliance of agent actions and outputs before they are committed. In multi-agent systems, this layer also evaluates inter-agent communications for goal integrity and instruction injection.

**Layer 3 - Human Oversight** provides the governance backstop. Scope scales inversely with demonstrated trustworthiness and directly with consequence severity. Write operations, external API calls, and irreversible actions escalate based on risk classification.

The critical addition for multi-agent systems is the **Secure Inter-Agent Message Bus** - a validated, signed, rate-limited communication channel through which all agent-to-agent interaction must pass. No direct agent-to-agent communication is permitted outside this bus.

The **Flight Recorder** captures every agent action, judge verdict, tool invocation, inter-agent message, conflict resolution, and PACE state transition in an immutable, tamper-evident log. This serves two purposes: forensic investigation when things go wrong, and feeding the offline evaluation pipeline with the evidence it needs for portfolio-level analysis of ethics, bias, and fairness.

## Visual Navigation

![MASO Tube Map](../images/maso-tube-map.svg)

Seven coloured lines represent seven control domains. Stations are key controls. Zones are implementation tiers. Interchanges mark where domains share control points (Judge Gate, PACE Bridge, Agent Registry). River PACE flows through the centre, mapping resilience phases to tier progression.

## How the Pieces Fit Together

MASO has many moving parts. Before diving into control domains, OWASP mappings, and implementation tiers, it helps to see how they connect.

The logic runs in a chain. **Agents are fragile** because they reason in natural language, which makes them vulnerable to manipulation, hallucination, and drift ([Anatomy of an Agentic Agent](../agentic-agent-anatomy.md)). That fragility means they need **external evaluation**: something outside the agent that checks its work against declared expectations ([Why Agents Need External Evaluation](#why-agents-need-external-evaluation)). For that evaluation to work, you need **clear declarations** of intent, outcomes, and constraints ([Constraining Agents](../constraining-agents.md), [Objective Intent](controls/objective-intent.md)). Those declarations give the judge a reference standard, and the quality of the declarations directly determines the quality of the judge's rulings.

From there, MASO provides the operational framework:

- **Eight control domains** address specific risk categories: protecting the agent's goals, identity, data, execution, observability, supply chain, privileged agents, and model cognition. Each domain contains controls that enforce the declarations you made and give the judge the signals it needs.
- **Three implementation tiers** scale controls to autonomy level. Tier 1 (supervised) requires human approval for every write. Tier 2 (managed) uses judge evaluation to auto-approve low-risk actions and escalate high-risk ones. Tier 3 (autonomous) operates with minimal human intervention for pre-approved task categories. You choose the tier that matches your risk tolerance.
- **PACE resilience** defines what happens when controls fail. Every layer has a defined failure mode and a predetermined safe state to transition to, from normal operations through to full shutdown.
- **OWASP coverage** maps every control to specific, documented threats from both the LLM Top 10 and the Agentic Top 10, so you can trace from a known risk to the controls that address it.
- **Threat intelligence and red teaming** ground the controls in real incidents and provide structured testing to verify they work.

None of these pieces stand alone. The control domains implement the declarations. The judge evaluates against them. The tiers scale the evaluation. PACE handles failure. The threat intelligence validates the whole stack. If you skip the declarations, the judge has nothing to evaluate against. If you skip the judge, the declarations are unenforceable. If you skip PACE, you have no plan for when controls fail. The framework is a system, not a menu.

## Control Domains

The framework organises controls into nine domains. The first five map to specific OWASP risks. The sixth, Prompt, Goal & Epistemic Integrity, addresses both the three OWASP risks that require cross-cutting controls and the nine epistemic risks identified in the [Emergent Risk Register](controls/risk-register.md) that have no OWASP equivalent. The seventh, Privileged Agent Governance, addresses the unique risks of orchestrators, planners, and other agents with elevated authority. The eighth, Model Cognition Assurance, addresses the gap between a model's expressed reasoning and its internal computational state.

### 0. [Prompt, Goal & Epistemic Integrity](controls/prompt-goal-and-epistemic-integrity.md)

Every agent's instructions, objectives, and information chain must be trustworthy and verifiable. Input sanitisation on all channels - not just user-facing. System prompt isolation prevents cross-agent extraction. Immutable task specifications with continuous goal integrity monitoring. Epistemic controls prevent groupthink, hallucination amplification, uncertainty stripping, and semantic drift across agent chains.

*Covers: LLM01, LLM07, ASI01, plus Epistemic Risks EP-01 through EP-09*

### 1. [Identity & Access](controls/identity-and-access.md)

Every agent must have a unique Non-Human Identity (NHI). No shared credentials. No inherited permissions from the orchestrator. Short-lived, scoped credentials that are rotated automatically. Zero-trust mutual authentication on the inter-agent message bus.

*Covers: ASI03, ASI07, LLM06*

### 2. [Data Protection](controls/data-protection.md)

Cross-agent data fencing prevents uncontrolled data flow between agents operating at different classification levels. Output DLP scanning at the message bus catches sensitive data in inter-agent communications. RAG integrity validation ensures the knowledge base hasn't been tampered with. Memory poisoning detection flags inconsistencies between stored context and expected agent state.

*Covers: LLM02, LLM04, ASI06, LLM08*

### 3. [Execution Control](controls/execution-control.md)

Every tool invocation runs in a sandboxed environment with strict parameter allow-lists. Code execution is isolated per agent with filesystem, network, and process scope containment. Blast radius caps limit the damage any single agent can do before circuit breakers engage. PACE escalation is triggered automatically when error rates exceed defined thresholds.

*Covers: ASI02, ASI05, ASI08, LLM05*

### 4. [Observability](controls/observability.md)

Immutable decision chain logs capture the full reasoning and action history of every agent. Behavioral drift detection compares current agent behavior against established baselines. Per-agent anomaly scoring feeds into the PACE escalation logic. SIEM and SOAR integration enables correlation with broader security operations.

*Covers: ASI09, ASI10, LLM09, LLM10*

### 5. [Supply Chain](controls/supply-chain.md)

Model provenance tracking and AIBOM generation for every model in the agent system. MCP server vetting with signed manifests and runtime integrity checks. A2A trust chain validation for inter-agent protocol endpoints. Continuous scanning of the agent toolchain for known vulnerabilities and poisoned components.

*Covers: LLM03, ASI04*

### 6. [Privileged Agent Governance](controls/privileged-agent-governance.md)

Orchestrators, planners, and meta-agents hold disproportionate authority - they can create agents, assign tasks, allocate resources, and modify workflows. These privileged agents require elevated controls: mandatory human approval gates, authority delegation limits, audit trails for every privilege exercise, and independent monitoring that the privileged agent cannot influence.

*Covers: ASI03, ASI07, LLM06 (elevated controls for high-authority agents)*

### 7. [Model Cognition Assurance](controls/model-cognition-assurance.md)

Controls for assessing whether a model's internal reasoning state aligns with its expressed chain-of-thought and outputs. Activation-layer transparency requirements for model providers. CoT integrity testing as a necessary but not sufficient control. Reward hacking detection through behavioural baselines and anomaly monitoring. Third-party AI risk classification with SR 11-7 gap analysis. Procurement attestation requirements for vendors supplying models to regulated financial services.

*Covers: Deceptive reasoning alignment, reward hacking, CoT faithfulness, activation-layer transparency, vendor interpretability attestation*

### [Environment Containment](environment-containment.md)

Cross-cutting strategy that complements all eight control domains. Instead of relying on the agent to behave correctly, harden every system the agent connects to: strict API input validation, opaque error responses, stored procedures, no-retry enforcement, and infrastructure-level kill switches. Existing enterprise security systems (DLP, fraud detection, WAF, SIEM) apply unchanged to agent traffic. The agent proposes; the infrastructure disposes.

*Cross-cuts: All Control Domains · All Implementation Tiers*

### 8. [Objective Intent](controls/objective-intent.md)

Every agent, judge, and workflow operates against a developer-declared Objective Intent Specification (OISpec), a structured, version-controlled contract defining what the agent should accomplish and within what parameters. Tactical judges evaluate individual agents against their OISpecs. A strategic evaluation agent assesses whether combined agent actions satisfy the workflow's aggregated intent. Judges are themselves monitored against their own OISpecs. This is the bridge from fault detection to behavioral assurance: from catching things that go wrong to verifying that things go right.

*Covers: Intent alignment at all levels: individual agent compliance (tactical), aggregate workflow compliance (strategic), and judge behavioral monitoring (lateral). Most critical at HIGH and CRITICAL risk tiers.*

## OWASP Risk Coverage

![OWASP Dual Mapping](../images/owasp-dual-mapping.svg)

Full mapping against both OWASP threat taxonomies relevant to multi-agent systems.

### OWASP Top 10 for LLM Applications (2025)

These risks apply to each individual agent. In a multi-agent context, each risk compounds across agents.

| Risk | Multi-Agent Amplification | MASO Control Domain |
|------|--------------------------|-------------------|
| **LLM01: Prompt Injection** | Injection in one agent's context propagates through inter-agent messages. A poisoned document processed by an analyst agent becomes instructions to an executor agent. | Input guardrails per agent · Message bus validation · Goal integrity monitor |
| **LLM02: Sensitive Information Disclosure** | Data shared between agents across trust boundaries. Delegation creates implicit data flows. | Cross-agent data fencing · Output DLP at message bus · Per-agent data classification |
| **LLM03: Supply Chain Vulnerabilities** | Multiple model providers, MCP servers, tool integrations multiply the attack surface. | AIBOM per agent · Signed tool manifests · MCP server vetting · Runtime component audit |
| **LLM04: Data and Model Poisoning** | Poisoned RAG data consumed by one agent contaminates reasoning of downstream agents. | RAG integrity validation · Source attribution · Cross-agent output verification |
| **LLM05: Improper Output Handling** | Agent outputs become inputs to other agents. Unsanitised output from Agent A becomes executable input for Agent B. | Output validation at every agent boundary · Model-as-Judge review · Schema enforcement |
| **LLM06: Excessive Agency** | The defining risk. Delegation creates transitive authority chains. If Agent A delegates to Agent B, and B has tool X, then A effectively has access to tool X. | Least privilege per agent · No transitive permissions · Scoped delegation contracts · PACE containment |
| **LLM07: System Prompt Leakage** | An agent's system prompt may be extractable by other agents in the same orchestration. | Prompt isolation per agent · Separate system prompt boundaries · Obfuscation |
| **LLM08: Vector and Embedding Weaknesses** | Shared vector databases across agents create a single point of compromise for RAG poisoning. | Per-agent RAG access controls · Embedding integrity verification · Source validation |
| **LLM09: Misinformation** | Hallucinations compound. One agent's hallucination becomes another's "fact". In self-reinforcing loops, misinformation amplifies. | Cross-agent validation · Dedicated fact-checking agent · Confidence scoring with source attribution |
| **LLM10: Unbounded Consumption** | Runaway agent loops cause exponential resource consumption. | Per-agent rate limits · Orchestration cost caps · Loop detection · Circuit breakers |

### OWASP Top 10 for Agentic Applications (2026)

These risks are specific to autonomous agent behavior - the primary threat surface for MASO.

| Risk | Description | MASO Controls |
|------|-------------|--------------|
| **ASI01: Agent Goal Hijack** | Attacker manipulates an agent's objectives through poisoned inputs. Hijacking one agent redirects an entire workflow. | Goal integrity monitor · Prompt boundary enforcement · Signed task specifications · Model-as-Judge goal validation |
| **ASI02: Tool Misuse** | Agents use legitimate tools in unintended, unsafe, or destructive ways. Chained tool misuse across agents compounds damage. | Signed tool manifests with strict parameter schemas · Argument validation · Sandboxed execution · Per-tool audit logging |
| **ASI03: Identity & Privilege Abuse** | Agents with leaked, over-scoped, or shared credentials. Credential sharing between agents is a common design flaw. | Unique NHI per agent · Short-lived scoped credentials · Zero-trust mutual authentication · No credential inheritance |
| **ASI04: Agentic Supply Chain** | Dynamic composition of MCP servers, A2A protocols, and tool plugins at runtime. | Runtime component signing · MCP server allow-listing · A2A trust chain validation · Dependency scanning |
| **ASI05: Unexpected Code Execution** | Natural language to code pathways bypass traditional code review gates. | Code execution sandbox · Execution allow-lists · Output containment · Time-boxing |
| **ASI06: Memory & Context Poisoning** | Persistent memory carries poisoned data across sessions. Shared memory becomes a persistent backdoor. | Session-isolated memory per agent · Memory integrity checksums · Context window fencing · Memory decay policies |
| **ASI07: Insecure Inter-Agent Communication** | Spoofed, tampered, or replayed messages between agents. | Signed and encrypted message bus · Mutual TLS per agent · Schema validation · Rate limiting · Replay protection |
| **ASI08: Cascading Failures** | Single fault propagates with escalating impact. Hallucination → flawed plan → destructive action. | Blast radius caps · Circuit breaker patterns · PACE escalation triggers · Independent error detection per agent |
| **ASI09: Human-Agent Trust Exploitation** | Agents produce confident, authoritative explanations that manipulate operators into approving harmful actions. Multi-agent consensus amplifies this. | Confidence calibration · Independent human verification · Decision audit trails · No agent can claim consensus authority |
| **ASI10: Rogue Agents** | Behavioral drift, misalignment, concealment, or self-directed action. Rogue behavior in one agent may be concealed by collaborating agents. | Continuous drift detection · Kill switch · Anomaly scoring against baselines · Regular red-team testing |

## PACE Resilience for Multi-Agent Operations

![PACE Multi-Agent Cycle](../images/pace-multi-agent-cycle.svg)

The [PACE methodology](../) (Primary, Alternate, Contingency, Emergency) from the parent framework is extended for multi-agent failure modes.

**Primary - Normal Operations.** All agents active within designated roles. Full three-layer security stack operational. Inter-agent communication through the signed message bus. Behavioral baselines actively monitored.

**Alternate - Agent Failover.** Triggered when a single agent shows anomalous behavior. The anomalous agent is isolated. A backup agent (potentially from a different provider) is activated. Tool permissions tightened to read-only. All write operations require human approval. Transition authority: automated (monitoring agent or orchestrator can initiate P→A without human approval, but must notify).

**Contingency - Degraded Mode.** Triggered when multiple agents are compromised, message bus integrity is questioned, or the alternate agent also exhibits anomalous behavior. Multi-agent orchestration is suspended. Single pre-validated agent operates in fully supervised mode. All agent state captured for forensics. Transition authority: security team or AI security officer.

**Emergency - Full Shutdown.** Triggered by cascading failures, confirmed exfiltration, coordinated manipulation, or rogue behavior. All agents terminated. Tool access revoked. Memory and context snapshots preserved in immutable storage. Full rollback initiated. Transition authority: CISO or incident commander.

**Recovery (E→P):** Requires post-incident review confirming root cause identification, control remediation, and updated baselines before returning to Primary.

## Implementation Tiers

### [Tier 1 - Supervised](implementation/tier-1-supervised.md) (Low Autonomy)

All agent actions require human approval. Inter-agent communication is logged but not encrypted. Behavioral monitoring is periodic (batch review). Suitable for pilot deployments and low-consequence use cases.

**Minimum controls:** Guardrails layer, basic tool scoping, human-in-the-loop for all writes, action audit log.

### [Tier 2 - Managed](implementation/tier-2-managed.md) (Medium Autonomy)

Agents execute read operations and low-consequence writes autonomously. High-consequence actions escalate to human oversight. Inter-agent communication is signed and validated. Behavioral monitoring is continuous with automated anomaly alerting. PACE Alternate and Contingency fully configured.

**Required controls:** All three security layers, per-agent NHI, signed message bus, Model-as-Judge evaluation, continuous anomaly scoring, PACE A and C configured and tested.

### [Tier 3 - Autonomous](implementation/tier-3-autonomous.md) (High Autonomy)

Agents operate with minimal human intervention for pre-approved task categories. Human oversight focuses on exception handling and strategic review. Full PACE cycle operational and tested through regular red-team exercises. All eight control domains fully implemented.

**Required controls:** Everything in Tier 2, plus kill switch tested and auditable, drift detection with baseline comparison, blast radius caps enforced, circuit breakers active, full OWASP coverage validated, regular adversarial testing.

## Threat Intelligence

| Document | Purpose |
|----------|---------|
| [Incident Tracker](threat-intelligence/incident-tracker.md) | Real-world AI security incidents mapped to framework controls, with confidence ratings and prevention mechanisms |
| [Emerging Threats](threat-intelligence/emerging-threats.md) | 8 forward-looking threat patterns: cross-agent worms, agent collusion, transitive authority exploitation, MCP supply chain, epistemic cascading failure, memory poisoning, A2A protocol attacks, AI vs AI defences |

### Threat Intelligence Grounding

Every control in MASO is grounded in observed or demonstrated attack patterns:

**Confirmed Incidents (2025):** EchoLeak (indirect prompt injection → data exfiltration, informs ASI01/LLM01), Amazon Q Exploit (tool misuse via manipulated inputs, informs ASI02), GitHub MCP Exploit (poisoned MCP server components, informs ASI04), AutoGPT RCE (natural language → code execution, informs ASI05), Gemini Memory Attack (persistent memory poisoning, informs ASI06), Replit Meltdown (rogue agent behavior, informs ASI10).

**Emerging Patterns:** Multi-agent consensus manipulation via shared knowledge base poisoning (ASI09), transitive delegation attacks creating implicit privilege escalation, agent-to-agent prompt injection through inter-agent output, credential harvesting via poisoned MCP tool descriptors, behavioral slow drift evading threshold-based detection.

## Red Team Operations

| Document | Purpose |
|----------|---------|
| [Red Team Playbook](red-team/red-team-playbook.md) | 16 structured test scenarios: 13 individual control tests across three tiers, plus 3 compound attack chains (injection-to-exfiltration, privilege escalation via Judge manipulation, slow drift to rogue behavior). Includes test results template and reporting metrics |

## Integration & Examples

| Document | Purpose |
|----------|---------|
| [Integration Guide](integration/integration-guide.md) | MASO control implementation patterns for LangGraph, AutoGen, CrewAI, and AWS Bedrock Agents. Framework comparison matrix, per-control mapping, and architecture-specific guidance |
| [Worked Examples](examples/worked-examples.md) | End-to-end MASO implementation for investment research (financial services), clinical decision support (healthcare), and grid operations (critical infrastructure). Includes PACE failure scenarios |

## Stress Testing at Scale

| Document | Purpose |
|----------|---------|
| [Stress Testing MASO at Scale](stress-test/100-agent-stress-test-overview.md) | Tabletop methodology for identifying framework breakpoints as agent count grows from single digits to 100+. Eight stress dimensions covering epistemic cascade depth, delegation graph complexity, cross-cluster PACE cascades, observability volume, provider concentration, data boundary enforcement, kill switch practicality, and compound attack surfaces |

## Regulatory Alignment

MASO inherits the parent framework's regulatory mappings and extends them to multi-agent-specific requirements:

| Regulation/Standard | Relevant Articles/Clauses | MASO Relevance |
|---------------------|---------------------------|---------------|
| **EU AI Act** | Art. 9, 14, 15 | Human oversight proportional to autonomy level. PACE provides the operational model. |
| **NIST AI RMF** | Govern, Map, Measure, Manage | Control domains map directly: Observability → Measure, Execution Control → Manage. |
| **ISO 42001** | §8.1-8.6, Annex A/B | Per-agent risk assessment and control assignment. |
| **MITRE ATLAS** | Agent-focused techniques (Oct 2025) | Threat intelligence aligned with ATLAS agent-specific attack techniques. |
| **DORA** | Art. 11 | Digital operational resilience for AI agents in financial services. PACE provides the resilience model. |
| **APRA CPS 234** | Information Security | Australian prudential requirements for AI agent deployments in financial services. |

## Known Architectural Trade-offs

MASO is honest about what it cannot guarantee. These are structural tensions in the framework, not bugs to be fixed. Understanding them is essential before deployment.

### The Judge is the high-value target

MASO concentrates trust in the Model-as-Judge layer. At Tier 2, where humans only review escalated actions, a compromised or bypassed Judge is effectively invisible. The [Red Team Playbook](red-team/red-team-playbook.md) scenario RT-06 confirms that Judges can be fooled by adversarial suffixes, context overloading, and distributed harm spread across individually-acceptable outputs.

**Mitigations exist but none eliminate the risk.** Model independence (different provider for the Judge), structured evaluation criteria, rotating evaluation strategies, and multi-model cross-validation at Tier 3 all reduce the attack surface. A [distilled SLM](../extensions/technical/distill-judge-slm.md) sidecar adds a second evaluation perspective at negligible latency. None of these make the Judge infallible. The full analysis is in [When the Judge Can Be Fooled](../core/when-the-judge-can-be-fooled.md) and [Judge Assurance](../core/judge-assurance.md).

**The design rationale:** a Judge that catches 90% of what guardrails miss, combined with human oversight that catches what the Judge misses, is strictly better than either alone. The alternative to an imperfect Judge is no Judge, which is worse.

### Slow drift beats fast attack

MASO's anomaly detection uses behavioural baselines. An adversary who shifts agent behaviour gradually, staying within scoring thresholds at each step, can accumulate significant drift without triggering alerts. The framework's long-window behavioural analysis (Tier 3) and trend-based alerting (OB-2.4) are the counters, but they require careful calibration of what "long window" means for your workload. Organisations that deploy anomaly scoring without tuning it to their operational patterns will have a false sense of security.

### Compound attacks exploit gaps between controls

The individual red team scenarios (RT-01 through RT-13) test controls in isolation. Real attackers chain techniques: injection to gain a foothold, delegation exploitation to escalate privilege, then data exfiltration through the elevated access. The [Red Team Playbook](red-team/red-team-playbook.md) includes compound attack scenarios (RT-14 through RT-16) that test these chains. If your individual control tests pass but compound tests fail, the gap is in control integration, not in individual control strength.

### Tier 3 is unproven at scale

The [100-agent stress test](stress-test/100-agent-stress-test-overview.md) identifies eight breakpoints that emerge above roughly 20 agents: epistemic cascade depth, cross-cluster PACE coordination, observability volume, and compound attack surface. These are acknowledged gaps, not solved problems. Organisations scaling beyond pilot deployments will need to extend the framework. This is by design: MASO provides the foundation and is transparent about where the edges are, rather than pretending completeness.

## Security Overhead at a Glance

Security controls are not free. The full analysis with worked examples is in [Cost & Latency](../extensions/technical/cost-and-latency.md). Here are the headline numbers.

| Approach | Evaluation cost at 1M actions/month | Critical-path latency added |
|----------|--------------------------------------|----------------------------|
| Cloud Judge on every action | $10K-50K per agent | 500ms-5s (if synchronous) |
| SLM sidecar + 1% cloud sampling | $350-700 (mostly fixed infrastructure) | 10-50ms |
| Rule-based guardrails only | Negligible | 5-20ms |

**Multi-agent multiplier:** In a 3-agent workflow, evaluation volume triples. A cloud-Judge-only approach at $30K-150K/month becomes $3K-4K/month with an SLM sidecar. The break-even for SLM distillation is roughly 50,000 evaluations per month.

**Rule of thumb:** Security overhead runs 15-40% of generator cost at Tier 2, and 40-100% at Tier 3 using cloud Judges. SLM distillation brings Tier 3 costs into the Tier 2 range. Budget for the full evaluation stack (tactical + domain + strategic + meta + observer), not just one Judge layer.

## Operational Concerns

These questions come up in every MASO deployment. The answers sit across the framework - collected here so you don't have to hunt.

| Question | Where It's Answered |
|----------|-------------------|
| What does the Judge layer cost? When should it run async? | [Cost & Latency](../extensions/technical/cost-and-latency.md) - sampling rates, latency budgets, tiered evaluation cascade |
| What if the Judge is wrong or manipulated? | [Judge Assurance](../core/judge-assurance.md) · [When the Judge Can Be Fooled](../core/when-the-judge-can-be-fooled.md) · [Privileged Agent Governance](controls/privileged-agent-governance.md) |
| How do we prevent operator fatigue at scale? | [Human Factors](../strategy/human-factors.md) - skill development, alert fatigue, canary testing, challenge rates |
| How do we vet models, tools, and MCP servers? | [Supply Chain Controls](controls/supply-chain.md) - AIBOM, signed manifests, model provenance, dependency scanning |
| What emergent risks have no OWASP equivalent? | [Emergent Risk Register](controls/risk-register.md) - 34 risks across 9 categories including epistemic, coordination, and inference-side attacks |
| How do we evaluate whether agents are doing what they were designed to do? | [Objective Intent](controls/objective-intent.md) - developer-declared OISpecs for every agent, judge, and workflow. Tactical judges evaluate individual compliance, strategic evaluators assess aggregate behavior, judge meta-evaluators close the watchmen loop |
| Won't multiple judges create "judge hell"? How many evaluation agents do I actually need? | [Privileged Agent Governance](controls/privileged-agent-governance.md#recognising-judge-proliferation) - evaluation roles vs. services, judge necessity decision framework, deployment topology. [Judge Assurance](../core/judge-assurance.md#when-you-need-a-judge-and-when-you-do-not) - the judge necessity test and ROI assessment. [Execution Control](controls/execution-control.md#deployment-topology-evaluation-roles-vs-services) - how the conceptual architecture maps to actual services |
| What happens when judges disagree? (e.g. fraud says flag, security says approve) | [Privileged Agent Governance](controls/privileged-agent-governance.md#inter-judge-conflict-resolution) - precedence orders, most-restrictive-wins default, conflict logging, pattern tracking |
| What about ethics, bias, and fairness evaluation? | [Privileged Agent Governance](controls/privileged-agent-governance.md#policy-driven-evaluation-domains-ethics-bias-and-fairness) - offline policy-driven evaluation outside the inline architecture. Statistical portfolio monitoring, external signals (complaints, appeals, demographics), findings feed back as guardrail tuning. See [Evaluation Architecture diagram](#evaluation-architecture-inline-vs-offline) |
| What does the full evaluation stack cost, not just one judge? | [Cost & Latency](../extensions/technical/cost-and-latency.md#total-cost-of-evaluation-multi-agent-workflows) - compound cost model for cloud judge vs. SLM scenarios, with fraud detection worked example |
| How much latency does multi-layer evaluation add to time-sensitive workflows? | [Cost & Latency](../extensions/technical/cost-and-latency.md#critical-path-latency-for-time-sensitive-workflows) - sync vs. async breakdown, critical-path analysis for fraud detection and trading compliance |
| How do I get a single audit view of a multi-agent decision? | [Observability](controls/observability.md#decision-trace-consolidated-audit-view) - Decision Trace format collapsing the full evaluation chain into one auditable document per decision |
| What about DLP, API validation, database controls, and existing IAM? | [Environment Containment](environment-containment.md) - hardened APIs, opaque errors, stored procedures, no-retry enforcement, and kill switches. Also: [Defence in Depth Beyond the AI Layer](../foundations/README.md#defence-in-depth-beyond-the-ai-layer) |
| What if the agent is compromised and all behavioral controls fail? | [Environment Containment](environment-containment.md) - environment controls remain effective because they do not depend on the agent's cooperation. The agent's intent is irrelevant if every connected system enforces its own boundaries |

## Relationship to Parent Framework

MASO is the multi-agent extension of [AI Runtime Security](../). It inherits the three-layer defence model, PACE resilience methodology, risk classification matrix, and regulatory mapping framework. It also inherits the core philosophy: controls are proportionate to risk, organisations select what they need based on their own context, and the goal is reducing harm rather than imposing process.

It extends into multi-agent territory by addressing multi-model orchestration security, inter-agent communication integrity, the OWASP Agentic Top 10 (2026), compound risk dynamics, Non-Human Identity management, and kill switch architecture.

## File Structure

```
README.md                              # This document
environment-containment.md             # Environment containment strategy
controls/
├── prompt-goal-and-epistemic-integrity.md
├── identity-and-access.md
├── data-protection.md
├── execution-control.md
├── observability.md
├── supply-chain.md
├── model-cognition-assurance.md
├── objective-intent.md
└── risk-register.md
threat-intelligence/
├── incident-tracker.md
└── emerging-threats.md
red-team/
└── red-team-playbook.md
integration/
└── integration-guide.md
examples/
└── worked-examples.md
implementation/
├── tier-1-supervised.md
├── tier-2-managed.md
└── tier-3-autonomous.md
stress-test/
└── 100-agent-stress-test-overview.md
```

## MASO 2.0: Anticipated Changes

**[Anticipated Changes to AI and Framework: MASO 2.0](maso-2.0-anticipated-changes.md)**

Six AI capability trajectories that will stress or break the current framework, with architectural responses and a phased roadmap:

| Evolution Vector | Framework Impact | MASO 2.0 Response |
|-----------------|-----------------|-------------------|
| **Judge ceiling** | Primary models exceed Judge evaluation capability | Verifiable action constraints, evidence-based reasoning, domain-specific verification oracles, ensemble Judge |
| **Human oversight scaling** | Transaction review becomes untenable at agent scale | Humans shift to governance over review, outcome-based oversight, automated escalation triage |
| **Session boundary dissolution** | Persistent/ambient agents invalidate session-based analysis | Continuous behavioral streams, intent inheritance, memory integrity as core control |
| **Multi-agent emergent behaviors** | Fleet interactions produce unanticipated states | Interaction graph analysis, fleet-level baselines, composition constraints, emergent behavior simulation |
| **AI-vs-AI adversarial dynamics** | Offensive AI outpaces human-speed defense updates | Continuous adversarial simulation, adaptive guardrails, Judge unpredictability |
| **Regulatory divergence** | Jurisdictions impose conflicting requirements | Jurisdiction-aware control profiles, compliance evidence automation |

Three-phase roadmap: Extend (0–6 months) → Architect (6–18 months) → Paradigm shift (18–36 months).

<div class="learning-callout" markdown>

<span class="learning-callout__label">Learning</span>

<p class="learning-callout__title">Learn the MASO Framework</p>

<p class="learning-callout__desc">AIruntimesecurity.co.za provides structured learning paths for the Multi-Agent Security Operations framework, from core concepts through to implementation.</p>

[Explore AIruntimesecurity.co.za](https://airuntimesecurity.co.za){ .md-button }

</div>

## What's Next

The framework core, implementation tiers, control domain specifications, threat intelligence, red team playbook, integration guide, and worked examples are complete. Planned extensions:

1. **Terraform/CloudFormation modules** for automated MASO infrastructure deployment on AWS and Azure.
2. **Compliance evidence packs** - pre-built documentation sets for ISO 42001, NIST AI RMF, and EU AI Act audits.
3. **Agent orchestration security benchmark** - quantitative scoring methodology for multi-agent system security posture.

