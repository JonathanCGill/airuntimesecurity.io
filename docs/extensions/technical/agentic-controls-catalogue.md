---
description: "Comprehensive technical controls catalogue for agentic AI systems: identity, execution, data, observability, and supply chain controls with framework cross-references."
---

# Technical Controls Catalogue for Agentic AI Systems

A comprehensive catalogue of technical controls for agentic AI systems, mapped to the framework's existing control specifications. Use this as a cross-reference to locate control implementations across the framework's documentation.

## Identity & Access

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **Agent identity tokens / cryptographic agent credentials** | IA-2.1 Non-Human Identity (NHI) with certificate-based identity per agent | [MASO Identity & Access](../../maso/controls/identity-and-access.md), [IAM-01](../../infrastructure/controls/identity-and-access.md#iam-01-authentication-of-all-entities) |
| **Per-agent service accounts (least privilege)** | IA-1.2 no shared credentials, IA-1.4 scoped permissions, IAM-02 least-privilege access | [MASO Identity & Access](../../maso/controls/identity-and-access.md), [IAM-02](../../infrastructure/controls/identity-and-access.md#iam-02-least-privilege-access) |
| **Agent-to-agent authentication (mTLS, signed requests)** | IA-2.3 mutual authentication on the message bus, mTLS in network controls | [MASO Identity & Access](../../maso/controls/identity-and-access.md), [Network & Segmentation](../../infrastructure/controls/network-and-segmentation.md) |
| **Human-in-the-loop step-up authentication for privileged actions** | IAM-05 human approval for high-impact actions, EC-1.1 human approval gate | [IAM-05](../../infrastructure/controls/identity-and-access.md#iam-05-human-approval-for-high-impact-actions), [MASO Execution Control](../../maso/controls/execution-control.md) |
| **Session binding (prevent token reuse across contexts)** | IAM-06 session-scoped credentials, SEC-02 non-transferable tokens bound to session | [IAM-06](../../infrastructure/controls/identity-and-access.md#iam-06-session-scoped-credentials), [Secrets & Credentials](../../infrastructure/controls/secrets-and-credentials.md) |
| **Role-based capability grants per agent instance** | IAM-04 agent tool invocation constraints, TOOL-01 declared tool permissions | [IAM-04](../../infrastructure/controls/identity-and-access.md#iam-04-agent-tool-invocation-constraints), [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md) |
| **Delegation chain attestation (who spawned whom)** | DEL-02 complete audit trail across chains, DEL-05 user identity propagation | [Delegation Chains](../../infrastructure/agentic/delegation-chains.md) |

## Action & Tool Controls

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **Allow lists**: explicit enumeration of permitted tools, APIs, shell commands, file paths | TOOL-01 declare tool permissions explicitly (allowlist, not denylist), EC-1.2 tool allow-lists | [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md), [MASO Execution Control](../../maso/controls/execution-control.md) |
| **Deny lists** (secondary, for known-bad patterns) | TOOL-01 operates as strict allowlist; deny lists are a secondary layer for known-bad tool parameter patterns | [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md), [Agentic Controls](../../core/agentic.md) |
| **Tool call signing / integrity verification** | SC-2.2 signed tool manifests, SC-2.4 runtime integrity checks at load time | [MASO Supply Chain](../../maso/controls/supply-chain.md) |
| **Read-only vs read-write tool separation** | TOOL-04 classifies actions by reversibility: read-only, reversible-write, irreversible-write, privileged | [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md#tool-04---classify-tool-actions-by-reversibility-and-impact) |
| **Rate limiting per tool per agent per session** | TOOL-05 per-session, per-tool, and time-window rate limits with burst detection | [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md#tool-05---rate-limit-tool-invocations-per-agent-and-per-tool) |
| **Time-boxed tool grants (expiring permissions)** | IAM-06 session-scoped credentials with automatic expiry, SEC-02 short-lived tokens, IA-2.2 automatic rotation | [IAM-06](../../infrastructure/controls/identity-and-access.md#iam-06-session-scoped-credentials), [MASO Identity & Access](../../maso/controls/identity-and-access.md) |
| **Dry-run / simulation mode before execution** | EC-2.1 action classification (auto-approve, escalate, block), AG.1.1 plan disclosure before execution, EC-2.7 aggregate harm assessment of full plan before execution | [MASO Execution Control](../../maso/controls/execution-control.md), [Agentic Controls Extended](agentic-controls-extended.md) |
| **Mandatory confirmation gates for irreversible actions** | IAM-05, EC-1.1 human approval gate, TOOL-04 irreversible-write classification, EC-1.6 reversibility assessment | [IAM-05](../../infrastructure/controls/identity-and-access.md#iam-05-human-approval-for-high-impact-actions), [MASO Execution Control](../../maso/controls/execution-control.md) |
| **Tool invocation logging with full parameter capture** | TOOL-06 log every tool invocation with full context (parameters, decision, response, chain context) | [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md#tool-06---log-every-tool-invocation-with-full-context) |

## Data Controls

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **Data boundaries**: namespaced access per agent, per task, per tenant | DP-2.3 infrastructure data fencing, DAT-04 access-controlled RAG retrieval, session isolation in memory controls | [MASO Data Protection](../../maso/controls/data-protection.md), [Data Protection](../../infrastructure/controls/data-protection.md) |
| **Prompt injection filtering (input sanitisation at tool boundaries)** | PG-1.1 input sanitisation per agent on all input sources, LOG-06 injection detection | [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md), [Agentic Controls](../../core/agentic.md) |
| **Output filtering / DLP before data leaves agent context** | DAT-03 PII detection and redaction on I/O, DAT-06 response leakage prevention, DP-2.1 DLP on message bus | [Data Protection](../../infrastructure/controls/data-protection.md), [MASO Data Protection](../../maso/controls/data-protection.md) |
| **PII/sensitive data redaction in tool outputs before returning to model** | DAT-03 PII detection at tool result boundary, SEC-01 tool result sanitisation, LOG-09 redaction in logs | [Data Protection](../../infrastructure/controls/data-protection.md#dat-03-pii-detection-and-redaction), [Secrets & Credentials](../../infrastructure/controls/secrets-and-credentials.md) |
| **Data residency constraints (agent cannot exfiltrate to non-compliant endpoints)** | NET-04 agent egress restricted to declared endpoints, SAND-03 sandbox network restrictions with allowlisted destinations, egress proxy enforcement | [Network & Segmentation](../../infrastructure/controls/network-and-segmentation.md), [Sandbox Patterns](../../infrastructure/agentic/sandbox-patterns.md) |
| **Secrets management integration (Vault, AWS Secrets Manager), no credentials in context** | SEC-01 through SEC-08: centralised vault, out-of-band credential injection, context window isolation, IA-2.6 secrets exclusion from context | [Secrets & Credentials](../../infrastructure/controls/secrets-and-credentials.md), [MASO Identity & Access](../../maso/controls/identity-and-access.md) |
| **Context window scrubbing (strip sensitive fields before handoff to sub-agents)** | Memory & context controls section 2 (context window hygiene), IA-2.6 secrets exclusion, DAT-02 data minimisation | [Memory & Context](../../core/memory-and-context.md), [Data Protection](../../infrastructure/controls/data-protection.md#dat-02-data-minimisation) |
| **Grounding source restrictions (retrieval only from approved corpora)** | SUP-03 RAG data source integrity with source allowlisting, SC-1.4 RAG source inventory, DAT-04 access-controlled retrieval | [Supply Chain](../../infrastructure/agentic/supply-chain.md), [Data Protection](../../infrastructure/controls/data-protection.md#dat-04-access-controlled-rag-retrieval) |

## Supply Chain & Composition

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **AI Bill of Materials (AI BOM)**: model provenance, version, training data lineage, fine-tune history | SUP-07 AI component inventory (AI-BOM), SC-2.1 AIBOM per agent with full component coverage | [Supply Chain](../../infrastructure/agentic/supply-chain.md), [MASO Supply Chain](../../maso/controls/supply-chain.md) |
| **Plugin/tool registry with cryptographic signing** | SUP-05 tool registry with security assessment, SC-2.2 signed tool manifests | [Supply Chain](../../infrastructure/agentic/supply-chain.md#sup-05---audit-tool-and-plugin-supply-chain), [MASO Supply Chain](../../maso/controls/supply-chain.md) |
| **Sub-agent provenance tracking (which model, which version, which orchestrator)** | DEL-02 complete audit trail with hop tracking, AIBOM specification per agent | [Delegation Chains](../../infrastructure/agentic/delegation-chains.md), [MASO Supply Chain](../../maso/controls/supply-chain.md) |
| **Dependency scanning for agent frameworks (LangChain, AutoGen, CrewAI, etc.)** | SC-3.3 continuous dependency scanning, SUP-08 monitor for vulnerabilities | [MASO Supply Chain](../../maso/controls/supply-chain.md), [Supply Chain](../../infrastructure/agentic/supply-chain.md#sup-08---monitor-for-model-and-dependency-vulnerabilities) |
| **Model card validation before deployment** | SUP-02 assess model risk before adoption with pre-adoption assessment and risk classification | [Supply Chain](../../infrastructure/agentic/supply-chain.md#sup-02---assess-model-risk-before-adoption) |
| **Third-party MCP server vetting and pinning** | SC-2.3 MCP server allow-listing, SC-3.4 A2A trust chain validation | [MASO Supply Chain](../../maso/controls/supply-chain.md), [Multi-Agent Controls](../../core/multi-agent-controls.md#mcp-model-context-protocol) |
| **Orchestrator integrity checks (hash validation on startup)** | SUP-01 cryptographic integrity with SHA-256 hash verification, SC-2.4 runtime integrity checks | [Supply Chain](../../infrastructure/agentic/supply-chain.md#sup-01---verify-model-provenance-and-integrity) |

## Runtime Behavior Monitoring

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **Behavioral baselines**: expected tool call patterns, output distributions, token velocity | OB-2.2 continuous anomaly scoring against established baseline, LOG-05 behavioral drift detection | [MASO Observability](../../maso/controls/observability.md), [Logging & Observability](../../infrastructure/controls/logging-and-observability.md) |
| **Anomaly detection on tool call sequences (graph-based or statistical)** | OB-2.2 anomaly scoring model with tool usage pattern signal (0.15 weight), TOOL-05 burst detection | [MASO Observability](../../maso/controls/observability.md#anomaly-scoring-model-tier-2), [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md) |
| **Model-as-Judge for output validation** | EC-2.5 LLM-as-Judge gate, the core three-layer pattern (Layer 2) | [Controls](../../core/controls.md), [MASO Execution Control](../../maso/controls/execution-control.md) |
| **Semantic drift detection (output meaning diverging from task intent)** | OB-2.3 drift detection with rolling baseline, EP-05 semantic drift in epistemic controls | [MASO Observability](../../maso/controls/observability.md), [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md) |
| **Prompt injection attempt detection (pattern + semantic)** | PG-1.1 input sanitisation, PG-3.1 multi-layer injection defence (pattern + semantic + canary), LOG-06 injection detection | [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md), [Logging & Observability](../../infrastructure/controls/logging-and-observability.md) |
| **Repetition / loop detection (agent stuck in recursive calls)** | EC-2.4 circuit breakers, EC-1.5 interaction timeout, CR-01 deadlock/livelock in risk register | [MASO Execution Control](../../maso/controls/execution-control.md), [Agentic Controls](../../core/agentic.md) |
| **Unexpected external communication alerts (callback to unknown endpoints)** | NET-04 agent egress restricted to declared endpoints, SAND-03 network restrictions with default no-network | [Network & Segmentation](../../infrastructure/controls/network-and-segmentation.md), [Sandbox Patterns](../../infrastructure/agentic/sandbox-patterns.md) |
| **Resource consumption limits (tokens, API calls, compute time, cost ceiling)** | OB-2.5 cost and consumption monitoring, EC-2.3 blast radius caps, SAND-04 resource limits, circuit breakers | [MASO Observability](../../maso/controls/observability.md), [MASO Execution Control](../../maso/controls/execution-control.md), [Sandbox Patterns](../../infrastructure/agentic/sandbox-patterns.md) |

## Sandboxing & Isolation

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **Execution sandboxes**: containerised tool execution (gVisor, Firecracker, Wasm) | SAND-01 isolated execution environments with four isolation levels (process, container, VM, remote sandbox) | [Sandbox Patterns](../../infrastructure/agentic/sandbox-patterns.md#sand-01-isolated-execution-environments) |
| **Network egress filtering per agent (allowlisted domains only)** | SAND-03 default no-network with allowlisted destinations, NET-04 egress proxy with declared endpoints | [Sandbox Patterns](../../infrastructure/agentic/sandbox-patterns.md#sand-03-network-restrictions), [Network & Segmentation](../../infrastructure/controls/network-and-segmentation.md) |
| **Filesystem isolation (chroot, ephemeral volumes, no persistence by default)** | SAND-02 file system restricted to declared paths, read-only mounts, no system access | [Sandbox Patterns](../../infrastructure/agentic/sandbox-patterns.md#sand-02-file-system-restrictions) |
| **Process isolation for code execution tools** | SAND-01 process isolation with seccomp, AppArmor; container and VM isolation for higher risk | [Sandbox Patterns](../../infrastructure/agentic/sandbox-patterns.md#sand-01-isolated-execution-environments) |
| **Memory namespace isolation between concurrent agent sessions** | DP-2.4 per-agent persistent memory isolation, memory & context session isolation | [MASO Data Protection](../../maso/controls/data-protection.md), [Memory & Context](../../core/memory-and-context.md) |
| **Ephemeral environments (destroy on task completion)** | SAND-05 no persistent state escaping sessions; containers created from clean image per execution, never reused | [Sandbox Patterns](../../infrastructure/agentic/sandbox-patterns.md#sand-05-no-persistent-state-escaping-sessions) |
| **No shared state between agent sessions unless explicitly bridged** | Memory & context session isolation, DP-2.4 shared state mediated exclusively through the message bus with DLP scanning | [Memory & Context](../../core/memory-and-context.md), [MASO Data Protection](../../maso/controls/data-protection.md) |

## Orchestration & Multi-Agent Controls

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **Trust tiers**: orchestrator vs sub-agent vs tool with differentiated permissions | PA agent role classification (task, orchestrator, evaluator, observer), IA-2.5 orchestrator privilege separation | [Privileged Agent Governance](../../maso/controls/privileged-agent-governance.md), [MASO Identity & Access](../../maso/controls/identity-and-access.md) |
| **Maximum delegation depth (prevent runaway spawning)** | DEL-03 maximum delegation depth per risk tier with gateway enforcement | [Delegation Chains](../../infrastructure/agentic/delegation-chains.md#del-03---limit-delegation-depth) |
| **Agent spawn rate limits** | EC-1.3 per-agent rate limits, EC-2.3 blast radius caps; orchestrator spawn rate enforcement at the gateway | [MASO Execution Control](../../maso/controls/execution-control.md), [Multi-Agent Controls](../../core/multi-agent-controls.md) |
| **Cross-agent communication signing / verification** | IA-2.3 mutual authentication with NHI certificates, IA-3.3 signed delegation contracts | [MASO Identity & Access](../../maso/controls/identity-and-access.md) |
| **Shared context integrity (detect tampering in shared memory/scratchpad)** | PG-2.5 claim provenance enforcement, EC-2.14 inter-agent data contracts, DP-2.2 RAG integrity validation | [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md), [MASO Execution Control](../../maso/controls/execution-control.md) |
| **Task scope pinning (agent cannot redefine its own objective)** | PG-1.3 immutable task specification, PG-2.2 goal integrity monitoring, PG-3.2 goal integrity hash chain | [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md) |
| **Dead-man switches (agent auto-terminates on loss of orchestrator contact)** | OB-3.3 independent observability agent with kill switch, EC-1.5 interaction timeout, EC-3.4 time-boxing | [MASO Observability](../../maso/controls/observability.md), [MASO Execution Control](../../maso/controls/execution-control.md) |
| **Circular delegation detection** | DEL-03 depth limits with circumvention detection, DEL-04 explicit delegation authorisation with manifest-based pairs; gateway detects and denies attempts to start a fresh chain for the same task context | [Delegation Chains](../../infrastructure/agentic/delegation-chains.md), [Multi-Agent Controls](../../core/multi-agent-controls.md) |

## Memory & State

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **Memory access controls**: scoped read/write per agent instance | Memory & context persistent memory controls, DP-2.4 per-agent memory isolation | [Memory & Context](../../core/memory-and-context.md), [MASO Data Protection](../../maso/controls/data-protection.md) |
| **Memory TTL / automatic expiry** | DP-3.2 memory decay with maximum retention window and auto-purge | [MASO Data Protection](../../maso/controls/data-protection.md), [Memory & Context](../../core/memory-and-context.md) |
| **Memory audit log (who wrote what, when)** | Memory & context section 3 persistent memory audit trail, OB-1.1 action audit log | [Memory & Context](../../core/memory-and-context.md), [MASO Observability](../../maso/controls/observability.md) |
| **Semantic deduplication to prevent poisoned memory accumulation** | DP-3.3 cross-session memory analysis for poisoning indicators, memory content filtering before storage | [MASO Data Protection](../../maso/controls/data-protection.md), [Memory & Context](../../core/memory-and-context.md) |
| **Cross-session memory isolation (episodic vs semantic separation)** | Memory & context session isolation (section 1), DP-1.2 logical separation, DP-2.4 memory isolation | [Memory & Context](../../core/memory-and-context.md), [MASO Data Protection](../../maso/controls/data-protection.md) |
| **Retrieval source attestation in RAG pipelines** | PG-2.5 claim provenance enforcement with source metadata, SUP-03 RAG provenance tracking | [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md), [Supply Chain](../../infrastructure/agentic/supply-chain.md) |
| **Prohibition on agents writing to their own instruction/system prompt store** | IAM-03 control plane / data plane separation, PG-1.2 system prompt isolation, TOOL-01 no runtime modification of manifests | [IAM-03](../../infrastructure/controls/identity-and-access.md#iam-03-control-plane--data-plane-separation), [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md) |

## Human Oversight

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **Mandatory human approval thresholds (configurable by action risk tier)** | IAM-05 human approval for high-impact actions, EC-2.1 action classification (auto-approve / escalate / block), TOOL-04 tiered enforcement by action class | [IAM-05](../../infrastructure/controls/identity-and-access.md#iam-05-human-approval-for-high-impact-actions), [MASO Execution Control](../../maso/controls/execution-control.md) |
| **Audit trail with full replay capability (inputs, tool calls, outputs, decisions)** | OB-2.1 immutable decision chain, TOOL-06 full context logging, LOG-01 through LOG-04 | [MASO Observability](../../maso/controls/observability.md), [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md), [Logging & Observability](../../infrastructure/controls/logging-and-observability.md) |
| **Interrupt / kill switch accessible to human operators at any point** | OB-3.3 independent observability agent with kill switch authority, PA-2.6 kill switch dual authorisation | [MASO Observability](../../maso/controls/observability.md), [Privileged Agent Governance](../../maso/controls/privileged-agent-governance.md) |
| **Escalation paths for out-of-distribution inputs** | PG-1.6 task clarity threshold (flag ambiguity rather than interpret), circuit breaker escalation, PACE methodology | [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md), [MASO Execution Control](../../maso/controls/execution-control.md) |
| **Red-line tripwires (automatic halt on defined condition, e.g. cost > $X, PII detected in output)** | EC-2.3 blast radius caps, EC-2.4 circuit breakers, OB-2.5 cost alerting thresholds | [MASO Execution Control](../../maso/controls/execution-control.md), [MASO Observability](../../maso/controls/observability.md) |
| **Oversight SLA enforcement (maximum time before human review required)** | EC-2.9 latency SLOs, OB-2.7 accountable human per workflow; human review escalation with defined timeframes | [MASO Execution Control](../../maso/controls/execution-control.md), [MASO Observability](../../maso/controls/observability.md) |

## Network & Communication

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **Egress allow list (agent can only communicate with pre-approved endpoints)** | NET-04 agent egress restricted to declared tool endpoints, SAND-03 allowlisted destinations only | [Network & Segmentation](../../infrastructure/controls/network-and-segmentation.md), [Sandbox Patterns](../../infrastructure/agentic/sandbox-patterns.md) |
| **mTLS for all agent-to-service communication** | DAT-05 mTLS for service-to-service in Zone 2 (Tier 3+), IA-2.3 mutual authentication | [Data Protection](../../infrastructure/controls/data-protection.md#dat-05-encryption-standards), [MASO Identity & Access](../../maso/controls/identity-and-access.md) |
| **API gateway intermediation (no direct external calls from agent runtime)** | NET-07 API gateway as single entry point, TOOL-02 gateway mediation for all tool calls | [Network & Segmentation](../../infrastructure/controls/network-and-segmentation.md), [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md) |
| **DNS filtering (prevent typosquatting / C2 via DNS)** | DNS sinkhole / RPZ controls, DoH blocking | [Technical Controls](technical-controls.md#12-dns-controls) |
| **Request signing with short-lived credentials** | SEC-02 short-lived scoped tokens, IA-3.3 signed delegation contracts | [Secrets & Credentials](../../infrastructure/controls/secrets-and-credentials.md), [MASO Identity & Access](../../maso/controls/identity-and-access.md) |
| **Payload size limits (prevent large data exfiltration)** | TOOL-03 payload size limits per tool per operation, SAND-04 output size limits | [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md#tool-03---constrain-tool-parameters-to-declared-bounds), [Sandbox Patterns](../../infrastructure/agentic/sandbox-patterns.md) |

## Configuration & Policy

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **Policy-as-code for agent permissions (OPA, Cedar)** | TOOL-01 machine-readable manifests, delegation policies in structured YAML, EC-2.1 action classification rules | [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md), [Multi-Agent Controls](../../core/multi-agent-controls.md), [MASO Execution Control](../../maso/controls/execution-control.md) |
| **Immutable configuration (agent cannot modify its own policy at runtime)** | TOOL-01 no runtime modification, PG-1.3 immutable task specification, IAM-03 control plane separation | [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md), [IAM-03](../../infrastructure/controls/identity-and-access.md#iam-03-control-plane--data-plane-separation) |
| **Environment separation (dev/test/prod) with model version pinning per env** | SUP-01 version pinning (never "latest"), SC-3.1 model version pinning per agent | [Supply Chain](../../infrastructure/agentic/supply-chain.md), [MASO Supply Chain](../../maso/controls/supply-chain.md) |
| **Change management controls on system prompts (versioned, approved, audited)** | PA-2.3 Judge criteria versioning with approval trail, IAM-03 control plane changes require approval | [Privileged Agent Governance](../../maso/controls/privileged-agent-governance.md), [IAM-03](../../infrastructure/controls/identity-and-access.md#iam-03-control-plane--data-plane-separation) |
| **Configuration drift detection** | OB-2.3 drift detection with rolling baseline, PA-2.7 orchestrator behavioral baseline, SUP-06 tamper detection on guardrail configurations | [MASO Observability](../../maso/controls/observability.md), [Privileged Agent Governance](../../maso/controls/privileged-agent-governance.md), [Supply Chain](../../infrastructure/agentic/supply-chain.md) |

## Evaluation & Testing

| Control | Framework Coverage | Reference |
|---------|-------------------|-----------|
| **Red-teaming protocols** specific to agentic attack surfaces (prompt injection, goal hijacking, tool abuse) | PA-2.8 privileged agent red team (quarterly), PG-3.6 prompt leakage red team, SUP-02 adversarial testing | [Privileged Agent Governance](../../maso/controls/privileged-agent-governance.md), [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md), [Red Team Playbook](../../maso/red-team/red-team-playbook.md) |
| **Adversarial task injection testing** | PG-3.1 canary agent for injection susceptibility testing, PA-2.8 inject a goal-subverting decomposition plan | [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md), [Privileged Agent Governance](../../maso/controls/privileged-agent-governance.md) |
| **Sandbagging / capability concealment detection probes** | Comprehensive coverage in evaluation integrity risks: canary interactions, evaluation signature elimination, multi-model cross-validation, behavioral consistency monitoring | [Evaluation Integrity Risks](../../insights/evaluation-integrity-risks.md), [Why Containment Beats Evaluation](../../insights/why-containment-beats-evaluation.md) |
| **Jailbreak resistance benchmarking** | SUP-02 adversarial testing (prompt injection, jailbreak, data extraction) before model approval, PA-2.2 Judge calibration testing with known-good and known-bad cases | [Supply Chain](../../infrastructure/agentic/supply-chain.md#sup-02---assess-model-risk-before-adoption), [Privileged Agent Governance](../../maso/controls/privileged-agent-governance.md) |
| **Multi-turn attack simulation (attacks that unfold over multiple steps)** | PG-3.6 automated probing for system prompt extraction, PG-3.1 multi-layer injection defence, context poisoning detection in memory controls | [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md), [Memory & Context](../../core/memory-and-context.md) |
| **Automated regression testing on behavior guardrails after model updates** | SUP-06 update validation with regression testing against known attack patterns, SC-3.2 automated rollback on quality degradation | [Supply Chain](../../infrastructure/agentic/supply-chain.md#sup-06---verify-guardrail-and-safety-model-integrity), [MASO Supply Chain](../../maso/controls/supply-chain.md) |

## Standards Anchors

| Domain | Standard | Framework Mapping |
|--------|----------|-------------------|
| AI governance | ISO 42001, NIST AI RMF | [ISO 42001 Annex A](../../infrastructure/mappings/iso42001-annex-a.md), [NIST AI RMF](../../infrastructure/mappings/nist-ai-rmf.md), [ISO 42001 Clause Mapping](../../extensions/regulatory/iso-42001-clause-mapping.md) |
| Security controls | NIST CSF 2.0, SOC 2 | [NIST CSF 2.0](../../infrastructure/mappings/csf-2.0.md), [SOC Integration](soc-integration.md) |
| Supply chain | SLSA, SBOM (SPDX/CycloneDX) | SUP-07 AI-BOM (framework-specific SBOM analogue), [Supply Chain Controls](../../infrastructure/agentic/supply-chain.md), [Technical Supply Chain](supply-chain.md) |
| Agentic threats | OWASP Top 10 for LLMs (esp. LLM08/09/10), MITRE ATLAS | [OWASP LLM Top 10](../../infrastructure/mappings/owasp-llm-top10.md), [Threat Intelligence](../../maso/threat-intelligence/emerging-threats.md) |
| Cloud execution | CSA CCM | Referenced in cloud security controls and compliance mappings |

## Emerging / Not Yet Standardised

Controls that are emerging or not yet standardised but worth tracking. The framework addresses these at varying levels of maturity.

| Control | Description | Framework Status | Reference |
|---------|-------------|------------------|-----------|
| **Capability sealing** | Formal declaration of what a model version can and cannot do, enforced at runtime | Partially addressed through TOOL-01 (machine-readable manifests declare permitted capabilities) and SUP-01 (version pinning). The formal "sealing" concept (a cryptographically signed capability declaration that the runtime enforces) extends beyond current manifest-based controls | [Tool Access Controls](../../infrastructure/agentic/tool-access-controls.md), [Supply Chain](../../infrastructure/agentic/supply-chain.md) |
| **Intent verification** | Confirming agent interpretation of a task before execution begins | Addressed by PA-2.1 (orchestrator intent verification by independent model), PG-1.6 (task clarity threshold, agents must flag ambiguity rather than interpret), and AG.1.1 (plan disclosure before execution) | [Privileged Agent Governance](../../maso/controls/privileged-agent-governance.md), [MASO Prompt, Goal & Epistemic Integrity](../../maso/controls/prompt-goal-and-epistemic-integrity.md) |
| **Economic circuit breakers** | Cost-based kill switches as a practical proxy for runaway behavior | Addressed by OB-2.5 (cost and consumption monitoring with alerting thresholds), EC-2.3 (blast radius caps including financial value), and circuit breaker patterns | [MASO Observability](../../maso/controls/observability.md), [MASO Execution Control](../../maso/controls/execution-control.md) |

