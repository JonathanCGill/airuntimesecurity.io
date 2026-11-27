---
as_at: "2026-07-04"
description: "Delegation chain controls for agentic AI: enforcing least privilege, maintaining audit trails, and preventing privilege escalation across agent-to-agent delegation."
---

# Delegation Chain Controls

> Part of the [AI Security Infrastructure Controls](../README.md) framework - Agentic AI Controls.
> Companion to [AI Runtime Security](https://github.com/JonathanCGill/airuntimesecurity.io).

## Overview

When an AI agent delegates a task to another agent, the delegation creates a chain of trust that must be explicitly managed. Without controls, delegation chains become a privilege escalation vector: Agent A has permission to call Agent B, which has permission to call Tool C - but the original user may never have been authorised to use Tool C. The delegation chain must not grant more authority than the originating user possesses.

These five controls enforce the principle that delegation reduces permissions (never increases them), maintains a linked audit trail, limits chain depth, requires explicit authorisation, and propagates the original user identity through the entire chain.

## DEL-01: Enforce Least Delegation (No Privilege Escalation)

**Risk Tiers:** Tier 2+ (agentic)

### Objective

The effective permissions at any point in a delegation chain must be the intersection of all participants' permissions and the originating user's permissions. Delegation can only narrow scope, never expand it.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Permission intersection** | When Agent A delegates to Agent B, the effective permissions of Agent B for that task are: Permissions(User) ∩ Permissions(Agent A) ∩ Permissions(Agent B). No participant in the chain can operate with more authority than the most restricted participant. |
| **Gateway enforcement** | Permission intersection is computed and enforced at the authorisation gateway, not by the agents themselves. The gateway receives the full chain context and evaluates against all applicable permission sets. |
| **No transitive escalation** | An agent cannot gain access to tools or data by delegating to another agent that has broader permissions. The delegation context carries the restriction forward. |
| **Explicit permission propagation** | The delegation message must include the effective permission set (or a reference to it) so that the gateway can enforce intersection at each hop. |
| **Denial logging** | When a delegated agent attempts an action that its own permissions would allow but the chain intersection denies, this is logged as a delegation-scope denial - distinct from a standard permission denial. |

### Relationship to Three Layers

| Layer | How DEL-01 Supports It |
|-------|----------------------|
| **Guardrails** | Permission intersection is the guardrail that prevents privilege escalation through delegation. It is enforced deterministically at the gateway, not by the agent's self-restraint. |
| **Judge** | Judge can evaluate whether delegation patterns are consistent with intended task scope, detecting attempts to route through higher-privilege agents. |
| **Human Oversight** | The permission intersection model is auditable - reviewers can trace exactly what permissions were effective at each point in the chain and verify no escalation occurred. |

## DEL-02: Maintain Complete Audit Trail Across Chains

**Risk Tiers:** Tier 2+ (agentic)

### Objective

Every delegation chain must produce a linked, chronological audit trail that allows complete reconstruction of: who initiated the chain, what was delegated, which agents participated, what actions were taken, and what results were returned.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Chain identifier** | Every delegation chain is assigned a unique chain ID at initiation. All events within the chain reference this ID, enabling end-to-end reconstruction. |
| **Hop tracking** | Each delegation hop is logged with: parent chain ID, hop number, delegating agent identity, receiving agent identity, delegated task description, effective permission set, timestamp, and result. |
| **Cross-agent linking** | Log entries from different agents within the same chain are linked via the chain ID and hop number. This linking survives agent boundaries - even if agents run in different environments or on different platforms. |
| **Tool invocation linking** | Tool invocations made by delegated agents include the chain ID and hop number, linking tool-level logs (TOOL-06) to the delegation chain context. |
| **Return path logging** | Results returned up the delegation chain are logged at each hop, capturing how information flows back through the chain. |
| **Integrity** | Delegation chain logs are subject to the same integrity protections as all operational logs (LOG-07). No participant in the chain can modify or delete chain logs. |

### Relationship to Three Layers

| Layer | How DEL-02 Supports It |
|-------|----------------------|
| **Guardrails** | The audit trail provides evidence that delegation guardrails (permission intersection, depth limits) are functioning correctly. |
| **Judge** | The complete chain audit trail is a primary input for Judge evaluation of multi-agent workflows. The Judge can assess whether the chain's collective behavior was appropriate. |
| **Human Oversight** | End-to-end chain reconstruction is essential for human reviewers. Without it, multi-agent systems are opaque and unaccountable. |

## DEL-03: Limit Delegation Depth

**Risk Tiers:** Tier 2+ (agentic)

### Objective

Constrain the maximum depth of delegation chains to prevent unbounded recursive delegation, reduce complexity for auditability, and limit the blast radius of a compromised agent within a chain.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Maximum depth** | Define a maximum delegation depth per risk tier. Recommended defaults: Tier 1 - delegation not permitted. Tier 2 - maximum depth of 2 (original agent + one delegate). Tier 3 - maximum depth of 3, with human approval required for chains exceeding depth 2. |
| **Gateway enforcement** | The authorisation gateway tracks delegation depth via the chain context. When a delegation request would exceed the maximum depth, the gateway denies it. |
| **No circumvention** | Agents cannot circumvent depth limits by initiating a new chain - the gateway detects and denies attempts to start a fresh chain for the same task context. |
| **Circular delegation detection** | The gateway tracks the full chain path and denies any delegation that would create a cycle (e.g., A→B→C→A). The chain context carries the set of agents already participating; re-delegation to any agent in the active set is blocked. |
| **Depth visibility** | The current depth and maximum depth are available in the chain context for logging and monitoring, but are not exposed to the agent's context window (to prevent manipulation). |
| **Override process** | If a legitimate use case requires deeper delegation, the depth limit can be increased through the standard change management process, not at runtime. |

### Relationship to Three Layers

| Layer | How DEL-03 Supports It |
|-------|----------------------|
| **Guardrails** | Depth limits are a structural guardrail that bounds system complexity and prevents recursive delegation patterns that could evade detection. |
| **Judge** | Shorter chains are easier for the Judge to evaluate comprehensively. Depth limits ensure that chain complexity remains within the Judge's effective evaluation capacity. |
| **Human Oversight** | Depth limits ensure that delegation chains remain tractable for human review. A chain of depth 15 is effectively unauditable. |

## DEL-04: Require Explicit Delegation Authorisation

**Risk Tiers:** Tier 2+ (agentic)

### Objective

Delegation between agents must be explicitly authorised. An agent's ability to invoke another agent is governed by the same manifest-based, gateway-enforced access control as tool invocations. Delegation is not a default capability.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Delegation manifest** | Each agent's manifest declares which other agents it may delegate to. Delegation to agents not in the manifest is denied. |
| **Bidirectional consent** | Delegation requires both: the delegating agent is authorised to delegate to the target, and the target agent is authorised to accept delegation from the source. Both declarations are in the respective manifests. |
| **Task-scoped delegation** | Delegation authorisation can be scoped to specific task types or contexts. An agent authorised to delegate data retrieval tasks may not be authorised to delegate write operations. |
| **Gateway enforcement** | The authorisation gateway validates delegation requests against both manifests before routing the delegation. The gateway, not the agents, determines whether delegation is permitted. |
| **No implicit discovery** | Agents cannot discover what other agents exist or what their capabilities are through runtime enumeration. Available delegation targets are declared in the manifest at deployment time. |

### Relationship to Three Layers

| Layer | How DEL-04 Supports It |
|-------|----------------------|
| **Guardrails** | Explicit delegation authorisation prevents agents from recruiting other agents beyond their declared scope, a critical guardrail against autonomous capability expansion. |
| **Judge** | Judge can verify that all delegations in a chain match the declared authorisation, detecting any delegation that bypassed the manifest. |
| **Human Oversight** | Delegation manifests give human reviewers a complete map of agent-to-agent trust relationships, enabling review of the system's actual delegation topology. |

## DEL-05: Propagate User Identity Through Chains

**Risk Tiers:** Tier 2+ (agentic)

### Objective

The identity of the originating user must be propagated through the entire delegation chain so that every action - regardless of which agent executes it and how many hops removed it is - can be attributed to the user who initiated it and evaluated against the user's permissions.

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Identity propagation** | The originating user's identity is included in the chain context and passed to every agent and gateway in the chain. Identity cannot be dropped, replaced, or impersonated at any hop. |
| **Immutable identity token** | User identity is carried as a signed, tamper-evident token (e.g., a JWT or equivalent) that agents cannot modify. The gateway verifies the token at each hop. |
| **Permission evaluation** | At every gateway enforcement point, the user's identity is used in the permission intersection calculation (DEL-01). The user's permissions are always the outermost constraint. |
| **Audit attribution** | All log entries, tool invocations, and delegation events in the chain include the originating user identity, enabling end-to-end attribution from any point in the chain. |
| **Session binding** | The user identity token is bound to the originating session. If the session expires or is terminated (SESS-05), the identity token becomes invalid and all active delegations in the chain are terminated. |

### Relationship to Three Layers

| Layer | How DEL-05 Supports It |
|-------|----------------------|
| **Guardrails** | User identity propagation ensures that guardrail enforcement always considers the user's authorisation level, even in deeply nested delegation chains. |
| **Judge** | User identity in chain logs enables the Judge to evaluate whether actions taken on behalf of a user are consistent with that user's role, permissions, and historical behavior patterns. |
| **Human Oversight** | User identity propagation enables accountability. Every action by every agent in a chain is traceable to the human who initiated it. |

