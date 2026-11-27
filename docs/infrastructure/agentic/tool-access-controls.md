---
as_at: "2026-07-04"
description: "Tool access controls for agentic AI: declaring, mediating, constraining, and logging all agent tool invocations through a deterministic authorisation gateway."
---

# Tool Access Controls

> Part of the [AI Security Infrastructure Controls](../README.md) framework - Agentic AI Controls.
> Companion to [AI Runtime Security](https://github.com/JonathanCGill/airuntimesecurity.io).

## Overview

When AI agents invoke external tools - APIs, databases, file systems, code interpreters, or third-party services - the tool invocation boundary is one of the highest-risk points in the system. The agent decides *what* to call and *why*, but it must never decide *whether* it is allowed to call it or *how* to authenticate. That enforcement belongs to deterministic infrastructure: the authorisation gateway.

These seven controls establish the principle that tool access is declared, mediated, constrained, classified, rate-limited, fully logged, and pinned to the definitions that were approved.

## TOOL-01: Declare Tool Permissions Explicitly Before Deployment

**Risk Tiers:** Tier 2+ (agentic)

### Objective

Every tool available to an agent must be declared in a machine-readable manifest before deployment. The manifest defines what the agent is allowed to do. Anything not in the manifest is denied by default - allowlist, not denylist.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Tool manifest** | Each agent deployment includes a tool manifest that declares: every tool the agent may invoke, the operations permitted per tool, parameter constraints per operation, and conditions under which invocation is permitted. |
| **Allowlist enforcement** | The manifest operates as a strict allowlist. Any tool invocation not matching a manifest entry is denied. There is no fallback to a denylist or open access mode. |
| **Manifest versioning** | Manifests are version-controlled. Changes require approval through the same change management process as code deployments. |
| **Pre-deployment validation** | Manifests are validated at deployment time: all referenced tools must exist in the approved tool registry (SUP-05), all declared operations must be within the tool's registered capabilities, and parameter constraints must be within the tool's declared bounds. |
| **No runtime modification** | The manifest cannot be modified at runtime by the agent, by prompt instructions, or by any path that does not go through the approved change management process. |

### Relationship to Three Layers

| Layer | How TOOL-01 Supports It |
|-------|------------------------|
| **Guardrails** | The manifest is the guardrail for tool access - it defines the boundary of permitted actions before any invocation occurs. |
| **Judge** | Judge can evaluate whether the agent's tool invocation patterns align with the manifest's intended scope, detecting misuse within technically permitted bounds. |
| **Human Oversight** | The manifest is a human-readable, auditable declaration of agent capability. Reviewers can assess whether declared permissions are appropriate for the task. |

## TOOL-02: Enforce Permissions at the Gateway, Not at the Agent

**Risk Tiers:** Tier 2+ (agentic)

### Objective

Tool invocation permissions are enforced by a gateway that sits between the agent and the tool. The agent never calls tools directly. The gateway is deterministic infrastructure that cannot be influenced by prompt injection or agent reasoning.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Gateway mediation** | All tool invocations pass through an authorisation gateway. No direct network path exists between the agent runtime and tool endpoints. |
| **Seven-step validation** | The gateway validates each invocation against: (1) manifest membership - is this tool declared? (2) operation permission - is this operation allowed? (3) parameter constraints - are parameters within bounds? (4) rate limits - has the invocation budget been exceeded? (5) context conditions - are contextual prerequisites met? (6) human approval - does this action require approval? (7) credential injection - add authentication out-of-band. |
| **Deterministic enforcement** | The gateway is a deterministic system (code, not a model). Its decisions are based on policy, not inference. It cannot be influenced by the content of the agent's reasoning or the prompt. |
| **Fail-closed** | If the gateway cannot validate an invocation (e.g., manifest lookup fails, rate limit service unavailable), the invocation is denied. The system never fails open. |
| **Agent opacity** | The agent does not receive detailed information about why an invocation was denied. Detailed denial reasons are logged for operators but not returned to the agent's context window, as this information could be used to craft bypass attempts. |

### Relationship to Three Layers

| Layer | How TOOL-02 Supports It |
|-------|------------------------|
| **Guardrails** | The gateway is the enforcement point for tool-level guardrails. It is the infrastructure that makes manifest-based access control real, not aspirational. |
| **Judge** | Gateway logs provide the Judge with a ground-truth record of what the agent actually did (attempted and succeeded), independent of the agent's self-reported reasoning. |
| **Human Oversight** | Gateway enforcement means humans can trust that the permissions they approved are actually being enforced, not merely suggested to the agent. |

## TOOL-03: Constrain Tool Parameters to Declared Bounds

**Risk Tiers:** Tier 2+ (agentic)

### Objective

Even when a tool invocation is permitted, the parameters passed to the tool must be within declared constraints. A tool allowed to read files should not be able to read arbitrary paths. A tool allowed to query a database should not be able to execute arbitrary SQL.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Parameter schemas** | Each tool operation in the manifest includes a parameter schema that defines: allowed types, value ranges, string patterns (regex), enumerated allowed values, and maximum lengths. |
| **Path constraints** | For tools that operate on file paths, URLs, or resource identifiers: declare allowed base paths or domains, prohibit path traversal patterns, and validate against an allowlist of permitted resources where possible. |
| **Query constraints** | For tools that execute queries: restrict to parameterised queries or predefined query templates, prohibit raw query construction from agent-generated strings, and validate query parameters against declared schemas. |
| **Payload size limits** | Enforce maximum payload sizes for all tool invocations. Limits are defined per tool and per operation in the manifest. |
| **Validation at gateway** | Parameter validation occurs at the gateway before the invocation reaches the tool. The tool itself should not be the last line of defence. |

### Relationship to Three Layers

| Layer | How TOOL-03 Supports It |
|-------|------------------------|
| **Guardrails** | Parameter constraints are fine-grained guardrails that prevent abuse within technically permitted tool access. They limit what the agent can do even when it is allowed to use the tool. |
| **Judge** | Judge can evaluate whether parameter values, while technically within bounds, represent unusual or suspicious patterns (e.g., reading an unusually large number of files from a permitted directory). |
| **Human Oversight** | Parameter schemas give human reviewers visibility into the granular scope of agent actions, not just which tools are available but exactly how they can be used. |

## TOOL-04: Classify Tool Actions by Reversibility and Impact

**Risk Tiers:** Tier 2+ (agentic)

### Objective

Not all tool actions carry the same risk. Reading a file is different from deleting it. Querying a balance is different from initiating a transfer. Tool actions must be classified by reversibility and impact to determine the appropriate level of oversight.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Action classification** | Every tool operation is classified into one of four categories based on reversibility and impact. |
| **Category definitions** | **Read-only:** No state change. Lowest risk. Examples: database queries, file reads, API lookups. **Reversible-write:** State change that can be undone. Moderate risk. Examples: creating draft records, writing to staging environments, adding items to a queue. **Irreversible-write:** State change that cannot easily be undone. High risk. Examples: sending emails, publishing content, executing financial transactions, deleting data. **Privileged:** Actions that modify security-relevant state. Highest risk. Examples: changing permissions, modifying configurations, creating credentials, accessing audit logs. |
| **Classification in manifest** | Each tool operation in the manifest includes its action classification. The classification drives gateway enforcement. |
| **Tiered enforcement** | Read-only actions may proceed with standard gateway validation. Reversible-write actions require additional logging and may require confirmation. Irreversible-write actions require human approval for Tier 3+ systems (see IAM-05). Privileged actions require human approval at all tiers with enhanced logging. |
| **No self-classification** | Agents do not classify their own actions. Classification is determined by the manifest, which is set by humans at deployment time. |

### Relationship to Three Layers

| Layer | How TOOL-04 Supports It |
|-------|------------------------|
| **Guardrails** | Action classification is the basis for the guardrail's decision about whether an invocation can proceed automatically or requires escalation. |
| **Judge** | Judge evaluation can be calibrated by action class - irreversible-write and privileged actions warrant more thorough post-hoc evaluation than read-only actions. |
| **Human Oversight** | Classification directly drives when humans are brought into the loop. It ensures human attention is directed at the highest-impact decisions. |

## TOOL-05: Rate-Limit Tool Invocations per Agent and per Tool

**Risk Tiers:** Tier 2+ (agentic)

### Objective

Prevent runaway agent behavior, resource exhaustion, and data exfiltration by enforcing invocation rate limits at the gateway. Rate limits apply per agent session, per tool, and per time window.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Per-session limits** | Each agent session has a maximum number of total tool invocations. When the limit is reached, further invocations are denied until the session is reviewed or reset. |
| **Per-tool limits** | Individual tools have per-session and per-time-window invocation limits. A tool that queries a database may have a different limit than a tool that sends notifications. |
| **Time-window limits** | Enforce sliding window rate limits (e.g., maximum invocations per minute, per hour) in addition to absolute session limits. |
| **Burst detection** | Detect and flag rapid sequences of tool invocations that may indicate automated exploitation or agent malfunction, even if individual limits are not yet exceeded. |
| **Limit configuration** | Rate limits are configured per tool in the manifest and enforced at the gateway. Limits cannot be modified by the agent or by prompt instructions. |
| **Graceful degradation** | When a rate limit is approached, the system may warn (via logging, not via agent context) before hard-blocking. Hard blocks are enforced at the configured limit. |

### Relationship to Three Layers

| Layer | How TOOL-05 Supports It |
|-------|------------------------|
| **Guardrails** | Rate limits are a quantitative guardrail that prevents accumulation attacks - where no single invocation is harmful, but the volume of invocations achieves a harmful outcome (e.g., enumerating records). |
| **Judge** | Rate limit proximity and burst patterns feed Judge evaluation as signals of potential anomalous behavior. |
| **Human Oversight** | Rate limit alerts surface agent sessions that may require human review, directing attention to potentially problematic behavior. |

## TOOL-06: Log Every Tool Invocation with Full Context

**Risk Tiers:** Tier 2+ (agentic)

### Objective

Every tool invocation - whether permitted or denied - must be logged with sufficient context to reconstruct the agent's actions, the gateway's decisions, and the tool's responses.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Invocation logging** | Every tool invocation is logged with: timestamp, session ID, agent identity, tool name, operation, parameters (with PII redaction per DAT-03), gateway decision (permit/deny), denial reason (if denied), tool response summary, and latency. |
| **Denial logging** | Denied invocations are logged with the same detail as permitted invocations, plus the specific validation step that caused denial (manifest, parameter, rate limit, approval, etc.). |
| **Chain context** | Tool invocation logs include a reference to the agent's reasoning chain, linking the invocation to the prompt, model output, and any preceding invocations in the same chain. This enables agent chain reconstruction (see LOG-04). |
| **Response capture** | Tool responses are captured in logs (with PII redaction). This is essential for understanding what information the agent received and how it influenced subsequent reasoning. |
| **Tamper protection** | Tool invocation logs are subject to the same integrity protection as all other logs (LOG-07) - append-only, write-once storage, inaccessible to the agent runtime. |
| **Retention** | Tool invocation logs follow the retention policy defined in LOG-08, with consideration that agentic audit trails may have longer regulatory retention requirements. |

### Relationship to Three Layers

| Layer | How TOOL-06 Supports It |
|-------|------------------------|
| **Guardrails** | Invocation logs provide evidence that guardrail enforcement (via the gateway) is functioning correctly. Logs of denied invocations prove the guardrails are active. |
| **Judge** | Complete invocation logs are a primary input for Judge evaluation of agent behavior - the Judge can assess whether the sequence and pattern of tool use was appropriate. |
| **Human Oversight** | Full invocation logs give human reviewers the ability to understand exactly what an agent did, why it was allowed, and what it received in response. |

## TOOL-07: Pin Tool Definitions by Hash and Reject Unapproved Changes

**Risk Tiers:** Agentic (Tier 2+)

### Objective

Tool names, descriptions, and parameter schemas are read by the model and steer its behaviour, so they are an injection surface. Ensure that the definitions an agent sees at runtime are exactly the ones that were reviewed and approved, and that a tool server cannot change them afterwards.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Hash at approval** | When a tool or MCP server is approved, record a hash of each tool's name, description, and parameter schema in the tool manifest (TOOL-01) and the AI-BOM (SUP-07). |
| **Verify at load** | The client or gateway recomputes the hash whenever tool definitions are fetched and refuses to expose any tool whose definition does not match. |
| **Alert on change** | A mismatch raises a security alert. A changed description on an approved server is treated as a possible rug pull, not a routine update. |
| **Review like prompts** | Definitions are reviewed for embedded instructions, references to files or credentials, and hidden Unicode before approval, using the same process as system prompts (SUP-09). |
| **Re-approval for updates** | Legitimate changes go through the same review and evaluation gate as the original approval before the new hash is accepted. |

### Relationship to Three Layers

| Layer | How TOOL-07 Supports It |
|-------|------------------------|
| **Guardrails** | Guardrails and the gateway operate on a known, reviewed tool surface. Poisoned or silently changed descriptions never reach the model. |
| **Judge** | Judge evaluation of tool use assumes the tool descriptions are the approved ones. Pinning keeps that assumption true. |
| **Human Oversight** | A definition change becomes an explicit human approval decision rather than an invisible runtime event. |

See [Prompt and Configuration Management](https://aisecuredbydesign.io/building/devops/prompt-and-config-management/#tool-definitions-poisoning-and-rug-pulls) for the pre-deployment process.
