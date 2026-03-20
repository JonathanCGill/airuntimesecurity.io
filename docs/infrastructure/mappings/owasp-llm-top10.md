---
description: "Mapping infrastructure controls to the OWASP Top 10 for LLM Applications (2025) and the OWASP Top 10 for Agentic AI with specific mitigations per risk."
---

# OWASP LLM Top 10 and Agentic Top 10 Mapping

> Maps infrastructure controls to the OWASP Top 10 for Large Language Model Applications (2025) and the OWASP Top 10 for Agentic AI.
>
> Part of the [AI Security Infrastructure Controls](../README.md) framework.
> Companion to [AI Runtime Security](https://github.com/JonathanCGill/airuntimesecurity.io).

## OWASP LLM Top 10 (2025)

### LLM01 - Prompt Injection

Manipulation of model behavior through crafted inputs that override system instructions or extract sensitive information.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | LOG-06, NET-02, SEC-01, DAT-02 | Five-layer injection detection (LOG-06) identifies injection attempts. Network-enforced guardrail bypass prevention (NET-02) ensures all inputs transit guardrails. Credential isolation from context (SEC-01) removes high-value extraction targets. Data minimisation (DAT-02) reduces what can be extracted. |
| **Secondary** | LOG-01, LOG-02, DAT-03, DAT-06, NET-07 | I/O logging captures injection attempts for analysis. Guardrail decision logs track detection rates. PII redaction reduces extraction value. Response leakage prevention catches successful extraction. API gateway ensures single entry point. |
| **Agentic** | TOOL-02, TOOL-03, SAND-03 | Gateway enforcement (not agent self-enforcement) prevents injected tool invocations. Parameter constraints limit what injected commands can achieve. Network-restricted sandboxes prevent injected code from exfiltrating data. |

### LLM02 - Sensitive Information Disclosure

Model outputs that expose confidential data, PII, proprietary information, or system internals.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | DAT-03, DAT-06, SEC-01, DAT-02 | PII detection and redaction (DAT-03) on both inputs and outputs. Response leakage prevention (DAT-06) scans outputs for sensitive patterns. Credential exclusion from context (SEC-01) prevents credential disclosure. Data minimisation (DAT-02) limits what enters context. |
| **Secondary** | LOG-01, LOG-09, DAT-04, DAT-08 | I/O logging enables disclosure incident investigation. Log redaction prevents logs from becoming a secondary disclosure vector. Access-controlled RAG prevents unauthorised document retrieval. Evaluation data tokenisation protects data sent to Judge. |
| **Agentic** | SESS-02, DEL-01, SAND-02 | Session isolation prevents cross-session data leakage. Permission intersection prevents agents from accessing data via delegation. File system restrictions prevent sandbox code from reading sensitive files. |

### LLM03 - Supply Chain Vulnerabilities

Compromise of AI system components through malicious models, poisoned training data, compromised tools, or vulnerable dependencies.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SUP-01, SUP-02, SUP-03, SUP-04, SUP-05, SUP-06, SUP-07, SUP-08 | The entire supply chain control domain directly addresses this risk. Provenance verification (SUP-01), risk assessment (SUP-02), RAG integrity (SUP-03), fine-tuning security (SUP-04), tool auditing (SUP-05), safety model integrity (SUP-06), AI-BOM (SUP-07), and vulnerability monitoring (SUP-08). |
| **Secondary** | NET-05, SEC-08 | Ingestion/runtime separation prevents poisoned data from reaching models directly. Code scanning catches embedded malicious content. |

### LLM04 - Data and Model Poisoning

Intentional manipulation of training data or model weights to embed backdoors, biases, or degraded safety behavior.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SUP-03, SUP-04, SUP-01, LOG-05 | RAG data source integrity (SUP-03) prevents poisoning through knowledge bases. Fine-tuning pipeline security (SUP-04) protects training processes. Provenance verification (SUP-01) detects model tampering. Drift detection (LOG-05) identifies behavioral changes that may indicate poisoning effects. |
| **Secondary** | NET-05, SUP-06, IAM-03, LOG-07 | Ingestion isolation separates data pipelines from runtime. Safety model integrity verification prevents poisoning of guardrails. Control plane separation protects model configurations. Log integrity prevents evidence tampering. |

### LLM05 - Improper Output Handling

Insufficient validation of model outputs before they are passed to downstream systems, enabling injection into those systems.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | DAT-06, LOG-02, NET-01 | Response leakage prevention (DAT-06) scans outputs before delivery. Guardrail decision logging (LOG-02) records output validation decisions. Zone architecture (NET-01) ensures outputs transit evaluation infrastructure. |
| **Secondary** | SAND-06, TOOL-03, DAT-03 | Code scanning before execution catches malicious generated code. Parameter constraints prevent injection via tool parameters. PII redaction applies to outputs. |
| **Agentic** | TOOL-02, TOOL-03, SAND-01, SAND-06 | Gateway enforcement validates tool invocations generated from model output. Parameter constraints prevent output-driven injection. Sandbox isolation contains generated code execution. Pre-execution scanning catches dangerous patterns. |

### LLM06 - Excessive Agency

Model or agent takes actions beyond what was intended or authorised, including unintended tool use, inappropriate parameter values, or actions exceeding scope.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | TOOL-01, TOOL-02, TOOL-03, TOOL-04, IAM-04, IAM-05 | Declared tool manifests (TOOL-01) define the boundary of permitted actions. Gateway enforcement (TOOL-02) makes the boundary real. Parameter constraints (TOOL-03) limit scope within permitted tools. Action classification (TOOL-04) routes high-impact actions to human approval. Agent tool constraints (IAM-04) and human approval routing (IAM-05) provide additional governance. |
| **Secondary** | TOOL-05, SESS-01, SESS-03, DEL-03 | Rate limiting prevents runaway behavior. Session boundaries limit duration. Task scope constraints limit purpose. Delegation depth limits prevent recursive agency expansion. |

### LLM07 - System Prompt Leakage

Exposure of system prompts, instruction sets, or internal configuration through model outputs or side channels.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | IAM-03, NET-06, DAT-06, SEC-01 | Control/data plane separation (IAM-03) protects configuration from runtime access. Control plane network protection (NET-06) restricts access to system prompts. Response leakage prevention (DAT-06) scans for system prompt content in outputs. Credential isolation principles (SEC-01) extend to system prompt protection. |
| **Secondary** | LOG-06, DAT-02, SUP-06 | Injection detection catches attempts to extract system prompts. Data minimisation reduces what is included in system prompts. Safety model integrity ensures guardrails that prevent leakage are not themselves compromised. |

### LLM08 - Vector and Embedding Weaknesses

Attacks targeting vector databases and embedding pipelines, including embedding inversion, adversarial embedding injection, and retrieval manipulation.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SUP-03, DAT-04, NET-05, DAT-05 | RAG data source integrity (SUP-03) prevents injection of adversarial content into vector stores. Access-controlled RAG (DAT-04) enforces document-level permissions on retrieval. Ingestion/runtime separation (NET-05) isolates vector write paths from query paths. Encryption (DAT-05) protects embeddings at rest and in transit. |
| **Secondary** | LOG-01, DAT-01, SUP-07 | I/O logging captures retrieval context for investigation. Data classification at RAG boundaries identifies sensitive content. AI-BOM tracks vector database components. |

### LLM09 - Misinformation

Model generates factually incorrect, misleading, or fabricated information (hallucination) that is presented as authoritative.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | LOG-03, LOG-05, SUP-03 | Judge evaluation (LOG-03) provides a second opinion on output quality and factual consistency. Drift detection (LOG-05) identifies when hallucination rates increase beyond baseline. RAG data integrity (SUP-03) ensures the knowledge base contains accurate source material. |
| **Secondary** | LOG-01, DAT-06, IR-01 | I/O logging enables investigation of misinformation incidents. Output scanning can include factual consistency checks. AI-specific incident categories include misinformation events. |

### LLM10 - Unbounded Consumption

Resource exhaustion attacks where model or agent systems consume excessive compute, memory, storage, or API calls, causing denial of service or cost escalation.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | TOOL-05, SESS-01, SAND-04, NET-07 | Rate limiting per agent and per tool (TOOL-05) prevents invocation-based resource exhaustion. Session boundaries (SESS-01) limit total resource consumption per session. Resource limits on execution (SAND-04) cap compute and memory. API gateway (NET-07) provides a single throttling point. |
| **Secondary** | LOG-01, IR-02, IR-03 | I/O logging tracks consumption patterns. Detection triggers identify abnormal resource usage. Containment procedures include service isolation for resource exhaustion incidents. |

## OWASP Top 10 for Agentic Applications (2026)

!!! info "Version note"
    Updated March 2026 to align with the official OWASP Top 10 for Agentic Applications released December 2025 at Black Hat Europe. Risk IDs use the **ASI** (Agentic Security Issue) prefix as published by OWASP.

### ASI01 - Agent Goal Hijack

Attackers redirect agent objectives by manipulating instructions, tool outputs, or external content, causing agents to pursue unintended or malicious objectives. This includes direct goal manipulation through prompt injection, indirect instruction injection via documents or RAG content, and recursive hijacking where goal modifications propagate through agent reasoning chains.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | LOG-06, TOOL-02, IAM-03, NET-02, SEC-01 | Injection detection (LOG-06) identifies hijack attempts including indirect injection via tool outputs. Gateway enforcement (TOOL-02) limits what a hijacked agent can do. Control plane separation (IAM-03) prevents runtime goal modification. Bypass prevention (NET-02) ensures guardrails are always in the path. Credential isolation (SEC-01) removes high-value targets from context. |
| **Secondary** | SESS-01, TOOL-05, TOOL-01, SAND-03, DAT-02 | Session limits bound the duration of a hijacked session. Rate limits constrain the speed of malicious actions. Manifests limit available tools. Network-restricted sandboxes prevent exfiltration. Data minimisation reduces what a hijacked agent can access. |

### ASI02 - Tool Misuse and Exploitation

Agents misuse legitimate tools due to ambiguous prompts, over-privilege, or poisoned inputs, staying within granted permissions but performing harmful actions such as deleting data, exfiltrating records, or running destructive commands. Includes tool poisoning and tool shadowing where attackers corrupt tool interfaces.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | TOOL-01, TOOL-02, TOOL-03, TOOL-04, TOOL-06, IAM-04 | Manifests define intended use and permitted tool combinations. Gateway enforces boundaries. Parameter constraints limit scope. Action classification routes risky operations to review. Full logging enables detection of misuse patterns. Agent tool constraints (IAM-04) enforce least privilege per tool. |
| **Secondary** | LOG-04, SESS-03, TOOL-05, NET-04, DAT-06 | Agent chain logging captures multi-tool sequences that may constitute exfiltration paths. Task scope limits purpose. Rate limiting prevents high-volume misuse. Egress proxy controls where agents can send data. Response leakage prevention scans outbound data. |

### ASI03 - Identity and Privilege Abuse

Attackers exploit inherited credentials, cached tokens, delegated permissions, or agent-to-agent trust boundaries. Agents inherit user sessions, reuse secrets, or rely on implicit cross-agent trust, leading to privilege escalation and actions that cannot be cleanly attributed to a distinct agent identity.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | DEL-01, DEL-05, IAM-02, IAM-04, TOOL-02, IAM-06 | Permission intersection (DEL-01) prevents escalation through delegation. User identity propagation (DEL-05) constrains all actions to user permissions. Least privilege (IAM-02) minimises starting permissions. Tool constraints (IAM-04) limit agent capabilities. Gateway enforcement (TOOL-02) prevents self-authorisation. Session-scoped credentials (IAM-06) limit token lifetime. |
| **Secondary** | DEL-03, DEL-04, IAM-08, SEC-01, IAM-01 | Depth limits reduce escalation paths. Explicit delegation authorisation prevents ad-hoc trust. Access auditing detects escalation. Credential isolation prevents credential leakage to context. Authentication ensures agent identity verification. |

### ASI04 - Agentic Supply Chain Compromise

Compromised tools, descriptors, models, or agent personas influence agent behaviour at runtime. Unlike LLM03 (static pre-deployment supply chain), ASI04 addresses dynamic runtime composition where agents discover and integrate components during execution, such as through MCP and A2A ecosystems.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SUP-01, SUP-02, SUP-05, SUP-06, SUP-07, SUP-08 | Provenance verification (SUP-01) detects tampered components. Risk assessment (SUP-02) evaluates runtime-discovered tools before use. Tool supply chain auditing (SUP-05) identifies insecure tools. Safety model integrity (SUP-06) protects guardrails from compromise. AI-BOM (SUP-07) tracks all components. Vulnerability monitoring (SUP-08) covers dynamically loaded dependencies. |
| **Secondary** | TOOL-01, TOOL-02, TOOL-03, SEC-07, NET-05 | Manifests validate tool identity and capabilities. Gateway enforcement mediates all tool calls. Parameter constraints limit exploitation surface. Endpoint protection secures tool authentication. Ingestion/runtime separation isolates data pipelines. |

### ASI05 - Unexpected Code Execution

Agents generate or execute untrusted or attacker-controlled code through code generation tools, dynamic evaluation, or injection into executable contexts. Natural-language execution paths unlock dangerous avenues for remote code execution that bypass traditional security controls.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SAND-01, SAND-02, SAND-03, SAND-04, SAND-05, SAND-06 | The entire sandbox control domain directly addresses this risk. Isolation levels (SAND-01), file system restrictions (SAND-02), network restrictions (SAND-03), resource limits (SAND-04), ephemeral state (SAND-05), and pre-execution scanning (SAND-06). |
| **Secondary** | NET-01, LOG-04, TOOL-06, SEC-08 | Zone architecture places sandboxes in appropriate zones. Agent chain logs link code execution to agent reasoning. Tool invocation logs capture execution context. Code scanning catches embedded malicious content. |

### ASI06 - Memory and Context Poisoning

Persistent corruption of agent memory, RAG stores, embeddings, or contextual knowledge that reshapes agent behaviour long after the initial interaction. Poisoned memory can propagate across sessions and influence decisions made by other agents that share knowledge stores.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | SAND-05, SESS-02, SESS-05, DAT-07, SUP-03 | Ephemeral environments (SAND-05) prevent persistent state. Session isolation (SESS-02) prevents cross-session contamination. Session cleanup (SESS-05) removes state on termination. Conversation history management (DAT-07) controls what persists. RAG data source integrity (SUP-03) prevents poisoning through knowledge bases. |
| **Secondary** | LOG-06, DAT-01, LOG-05, DAT-04 | Injection detection identifies poisoning attempts. Data classification at boundaries identifies suspicious persistent content. Drift detection identifies behavioural changes that may indicate poisoning effects. Access-controlled RAG enforces document-level permissions. |

### ASI07 - Insecure Inter-Agent Communication

Spoofed, intercepted, or manipulated messages between agents in multi-agent systems. When agents communicate, messages can be intercepted, spoofed, or manipulated if communication channels lack authentication, encryption, or message integrity verification. Spoofed inter-agent messages can misdirect entire agent clusters.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | DEL-01, DEL-02, DEL-04, DEL-05, NET-01, IAM-01 | Permission intersection (DEL-01) governs what agents can request of each other. Delegation audit trails (DEL-02) track all inter-agent communication. Explicit delegation authorisation (DEL-04) prevents ad-hoc agent-to-agent trust. User identity propagation (DEL-05) ensures messages carry verifiable origin. Zone architecture (NET-01) segments agent communication paths. Authentication (IAM-01) verifies agent identity at each hop. |
| **Secondary** | LOG-04, IAM-03, DAT-05, NET-06 | Agent chain logging captures inter-agent message sequences. Control plane separation prevents runtime manipulation of communication policies. Encryption protects messages in transit. Control plane network protection restricts access to agent coordination infrastructure. |

### ASI08 - Cascading Agent Failures

Small missteps or faults propagate through multi-agent workflows, amplifying impact as they cascade. A failure in one component (the LLM provider, a downstream API, or a tool) propagates through the agent system, causing widespread outages, degraded behaviour, or compounding incorrect decisions across dependent agents.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | DEL-03, SESS-01, IR-03, IR-04, TOOL-05 | Delegation depth limits (DEL-03) bound the propagation distance of failures. Session boundaries (SESS-01) limit the scope of cascading effects. Containment procedures (IR-03) isolate affected agent chains. Rollback capability (IR-04) enables recovery from cascading state corruption. Rate limiting (TOOL-05) prevents runaway failure loops. |
| **Secondary** | LOG-04, IR-02, LOG-10, NET-08, SAND-04 | Agent chain logging enables reconstruction of failure propagation paths. Detection triggers identify abnormal patterns indicative of cascading failures. SIEM correlation identifies cross-system impact. Cross-zone monitoring detects failures spanning trust boundaries. Resource limits prevent resource exhaustion from cascading load. |

### ASI09 - Human-Agent Trust Exploitation

Confident, polished agent explanations mislead human operators into approving harmful actions. Humans overly rely on agent recommendations, rubber-stamping decisions without meaningful review due to automation bias, information asymmetry, or the persuasive quality of AI-generated justifications.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | IAM-05, TOOL-04, SESS-04, LOG-03 | Human approval routing (IAM-05) for high-impact actions ensures humans are in the loop. Action classification by reversibility (TOOL-04) determines which actions need human approval. Progressive trust (SESS-04) starts with restrictive permissions rather than defaulting to trust. Judge evaluation (LOG-03) provides independent assessment alongside agent explanations, giving humans a second opinion. |
| **Secondary** | TOOL-01, TOOL-02, SESS-01, DEL-03, LOG-01 | Manifests define the scope of autonomous action. Gateway enforces approval requirements. Session limits bound autonomous runtime. Delegation depth limits prevent deep autonomous chains. I/O logging provides audit trail for post-hoc review of human-approved actions. |

### ASI10 - Rogue Agents

Misaligned or compromised agents diverge from intended behaviour, exhibiting concealment, self-directed action, or persistent misalignment that is difficult to detect. Unlike ASI01 (external hijacking), rogue agents may arise from emergent misalignment, fine-tuning corruption, or sophisticated compromise that evades standard detection.

| Control Type | Controls | How It Mitigates |
|-------------|----------|-----------------|
| **Primary** | LOG-03, LOG-05, TOOL-02, TOOL-04, IR-02, NET-02 | Judge evaluation (LOG-03) provides independent behavioural assessment that can detect deviation from expected patterns. Drift detection (LOG-05) identifies gradual behavioural changes. Gateway enforcement (TOOL-02) limits what any agent can do regardless of intent. Action classification (TOOL-04) routes high-impact actions through human review. Detection triggers (IR-02) fire on anomalous behaviour patterns. Bypass prevention (NET-02) ensures even rogue agents cannot circumvent guardrails. |
| **Secondary** | LOG-04, LOG-01, SESS-01, IR-03, SAND-01, IAM-08 | Agent chain logging enables forensic analysis of rogue behaviour. I/O logging captures all agent interactions for review. Session boundaries limit the duration and scope of rogue activity. Containment procedures isolate compromised agents. Sandbox isolation prevents escape. Access auditing detects anomalous access patterns. |

## Control Coverage Summary

### OWASP LLM Top 10 - Primary Control Distribution

| Risk | Primary Controls |
|------|-----------------|
| LLM01 Prompt Injection | LOG-06, NET-02, SEC-01, DAT-02 |
| LLM02 Sensitive Information Disclosure | DAT-03, DAT-06, SEC-01, DAT-02 |
| LLM03 Supply Chain Vulnerabilities | SUP-01 through SUP-08 |
| LLM04 Data and Model Poisoning | SUP-03, SUP-04, SUP-01, LOG-05 |
| LLM05 Improper Output Handling | DAT-06, LOG-02, NET-01 |
| LLM06 Excessive Agency | TOOL-01 through TOOL-04, IAM-04, IAM-05 |
| LLM07 System Prompt Leakage | IAM-03, NET-06, DAT-06, SEC-01 |
| LLM08 Vector and Embedding Weaknesses | SUP-03, DAT-04, NET-05, DAT-05 |
| LLM09 Misinformation | LOG-03, LOG-05, SUP-03 |
| LLM10 Unbounded Consumption | TOOL-05, SESS-01, SAND-04, NET-07 |

### OWASP Agentic Top 10 (2026) - Primary Control Distribution

| Risk | Primary Controls |
|------|-----------------|
| ASI01 Agent Goal Hijack | LOG-06, TOOL-02, IAM-03, NET-02, SEC-01 |
| ASI02 Tool Misuse and Exploitation | TOOL-01 through TOOL-04, TOOL-06, IAM-04 |
| ASI03 Identity and Privilege Abuse | DEL-01, DEL-05, IAM-02, IAM-04, TOOL-02, IAM-06 |
| ASI04 Agentic Supply Chain Compromise | SUP-01, SUP-02, SUP-05, SUP-06, SUP-07, SUP-08 |
| ASI05 Unexpected Code Execution | SAND-01 through SAND-06 |
| ASI06 Memory and Context Poisoning | SAND-05, SESS-02, SESS-05, DAT-07, SUP-03 |
| ASI07 Insecure Inter-Agent Communication | DEL-01, DEL-02, DEL-04, DEL-05, NET-01, IAM-01 |
| ASI08 Cascading Agent Failures | DEL-03, SESS-01, IR-03, IR-04, TOOL-05 |
| ASI09 Human-Agent Trust Exploitation | IAM-05, TOOL-04, SESS-04, LOG-03 |
| ASI10 Rogue Agents | LOG-03, LOG-05, TOOL-02, TOOL-04, IR-02, NET-02 |

