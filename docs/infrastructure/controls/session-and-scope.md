---
as_at: "2026-07-04"
description: Explains controls for isolating agent sessions, limiting blast radius, and preventing scope creep in autonomous AI operations.
---

# Session & Scope for Agentic AI

> **Control Domain:** Agentic - Containment Controls  
> **Purpose:** Isolate agent sessions, limit blast radius, and prevent scope creep in autonomous AI operations.  
> **Extends:** IAM-06 (session-scoped credentials) and NET-01 (network zones) with agentic-specific depth.

## The Problem

An agent operating within a session accumulates context, credentials, data access, and decision history. Over time, a long-running agent session becomes a high-value target: it holds data from multiple tool calls, has active credentials, and has built a context window containing potentially sensitive information from across the session.

The longer a session runs, the greater the blast radius if compromised. Session isolation limits what an attacker can reach through any single compromised session.

## Control Objectives

| ID | Objective | Risk Tiers |
|----|-----------|------------|
| SESS-01 | Define and enforce session boundaries with automatic expiry | Tier 2+ (agentic) |
| SESS-02 | Isolate sessions from each other (no cross-session data leakage) | Tier 2+ (agentic) |
| SESS-03 | Limit the scope of each session to a declared task | Tier 2+ (agentic) |
| SESS-04 | Implement progressive trust within sessions | Tier 3+ (agentic) |
| SESS-05 | Clean up session state on termination | Tier 2+ (agentic) |
| SESS-06 | Limit each session to two of untrusted input, sensitive access, and outbound action | All (agentic) |

## SESS-01: Session Boundaries

Every agent session must have defined boundaries:

| Boundary | Enforcement |
|----------|-------------|
| **Time limit** | Maximum session duration (e.g., 30 minutes for Tier 3, 4 hours for Tier 2). Hard cutoff, not advisory. |
| **Token limit** | Maximum total tokens consumed across all model calls in the session. Prevents denial-of-wallet and runaway context accumulation. |
| **Action limit** | Maximum number of tool invocations per session. Prevents infinite loops and excessive automation. |
| **Scope boundary** | Session is scoped to a declared task. The agent cannot "pivot" to unrelated tasks within the same session. |
| **Credential expiry** | All session credentials expire with the session (IAM-06). No credential carry-over. |

When any boundary is reached, the session terminates gracefully: pending actions are cancelled (not auto-approved), the user is notified, and all session state is cleaned up (SESS-05).

## SESS-02: Session Isolation

Sessions must be isolated from each other. No data, credentials, context, or state from one session should be accessible to another.

### Isolation Requirements

- **Context isolation:** Agent A's session context (conversation history, tool results, intermediate reasoning) is not accessible to Agent B's session, even if they serve the same user.
- **Credential isolation:** Credentials issued for Session A cannot be used in Session B.
- **Memory isolation:** If the agent has persistent memory, session-specific data must be clearly separated from cross-session memory, and cross-session memory must not contain sensitive data from individual sessions.
- **Resource isolation:** For Tier 3+ systems, sessions run in separate compute contexts (containers, sandboxes) to prevent side-channel information leakage.

### What This Prevents

- A compromised session cannot pivot to access data from other sessions.
- An attacker who extracts context from one session cannot use it to authenticate in another.
- Cross-session data correlation attacks (where an attacker uses multiple sessions to reconstruct information that no single session should reveal).

## SESS-03: Scope Constraints

Each session should have a declared scope - the task it is permitted to accomplish.

### Scope Definition

| Element | Description |
|---------|-------------|
| **Task type** | What the session is doing (e.g., "answer customer query", "process expense report") |
| **Data domain** | What data the session can access (e.g., "customer record for user X only") |
| **Tool set** | Which tools are available in this session (subset of the agent's full manifest) |
| **Output type** | What the session can produce (e.g., "text response only", "response + database update") |
| **User context** | Who initiated the session and what permissions they carry |

### Scope Enforcement

The authorization gateway (IAM-04) enforces scope by:

- Restricting tool invocations to those relevant to the declared task.
- Filtering data queries to the declared data domain.
- Monitoring agent reasoning for scope drift (e.g., the agent starts discussing topics unrelated to the declared task).
- Terminating sessions that persistently attempt out-of-scope actions.

## SESS-04: Progressive Trust

For Tier 3+ systems, sessions should not start with full permissions. Instead, permissions increase as the session demonstrates expected behavior.

### Trust Levels

| Level | Permissions | Triggers to Advance |
|-------|------------|---------------------|
| **Initial** | Read-only tool access, text response only | N successful interactions without guardrail flags |
| **Standard** | Full read access, reversible writes | No Judge flags, confirmed user identity |
| **Elevated** | Irreversible writes (with approval), external communications | Human reviewer approves elevation, explicit user request |

### Why Progressive Trust

- Limits the damage from injection attacks early in a session (before the agent has accumulated data or context).
- Forces attackers to maintain consistent benign behavior before gaining access to destructive capabilities.
- Provides natural checkpoints where human oversight can intervene.

## SESS-05: Session Cleanup

When a session terminates (normally or abnormally), all session state must be cleaned up:

- **Credentials:** All session-scoped tokens revoked immediately.
- **Context:** Session context purged from memory (not just dereferenced - actively cleared).
- **Temporary data:** Any temporary files, cache entries, or intermediate results created during the session are deleted.
- **Tool connections:** Any open connections to backend tools are closed.
- **Audit record:** A session termination event is logged with: session duration, token consumption, tool invocation count, guardrail/Judge flags, and termination reason.

For abnormal termination (crash, timeout, forced kill), cleanup must still occur - design for crash-safe cleanup.

## SESS-06: Rule of Two per Session

An agent session must not hold all three of the following at once:

- **(A) Untrusted input:** it reads content an attacker can influence, such as web pages, inbound email, uploaded files, retrieved documents, tool output, or messages from other agents.
- **(B) Sensitive access:** it can reach private data, internal systems, or credentials.
- **(C) Outbound action:** it can change state or communicate externally, including sending messages, writing records, calling external APIs, or rendering links and images that cause outbound requests.

This is Meta's **Agents Rule of Two**, applied as an infrastructure control. With all three present, an injected instruction has everything it needs to exfiltrate data or cause harm, and no guardrail is reliable enough to be the only barrier.

- **Declared per session type:** Each session type declares which of A, B, and C it holds. The declaration is reviewed at design time and recorded with the tool manifest (TOOL-01).
- **Enforced in infrastructure:** The tool gateway, credential issuer, and egress proxy enforce the declaration. A session that has read untrusted content loses access to the tools, credentials, or destinations that would complete the third leg. Instructions in the system prompt do not count as enforcement.
- **All three requires approval:** Where a task genuinely needs all three, each action that completes the set requires human approval (IAM-05) or an isolation pattern that removes a leg, such as dual LLM or plan-then-execute.
- **Untrusted by default:** Tool output, retrieved documents, memory, and messages from other agents are treated as untrusted input unless their provenance is verified.

The design patterns that satisfy this control are set out in [Injection-Resistant Design](https://aisecuredbydesign.io/core/injection-resistant-design/#the-agents-rule-of-two).

## Platform-Neutral Implementation Checklist

- [ ] Session boundaries defined (time, token, action, scope, credential expiry)
- [ ] Hard session termination on boundary breach (not advisory)
- [ ] Sessions isolated from each other (context, credentials, memory, resources)
- [ ] Session scope declared and enforced via authorization gateway
- [ ] Progressive trust implemented for Tier 3+ systems
- [ ] Session cleanup verified for normal and abnormal termination
- [ ] Each session type declares which Rule of Two properties it holds, enforced by gateway, credentials, and egress
- [ ] Session metadata logged for forensics and drift detection
- [ ] Cross-session data correlation attacks considered in threat model

## Customer-to-Agent Session Binding

The controls above address agent sessions - how an autonomous AI system manages its own context, credentials, and scope. But in customer-facing deployments (chatbots, self-service portals, AI-assisted commerce), there is an additional trust boundary: **the authenticated customer whose intent the agent is executing**.

This is not the same as agent identity. Agent identity answers "which AI component is acting?" Customer session binding answers "on whose behalf, and how do we know?"

### The Problem

When a customer authenticates to your application and interacts with an AI agent, the agent acts *as a proxy* for that customer - reading their data, modifying their cart, processing their payment. If the binding between customer identity and agent session is weak, an attacker can:

- **Session hijack:** Take over another customer's agent session and issue commands on their behalf
- **Session fixation:** Pre-set a session that a customer later authenticates into, giving the attacker a parallel path
- **Cross-customer contamination:** In concurrent sessions, context from Customer A bleeds into Customer B's agent responses
- **Scope escape:** The agent holds credentials scoped to "customer cart access" but the scope isn't bound to *which* customer's cart

### What You Must Design

The framework gives you the agent-side controls (SESS-01 through SESS-06). For customer-facing systems, you must additionally answer:

| Question | Why It Matters |
|----------|---------------|
| How is the customer's identity propagated into the agent session? | The agent needs to know *whose* data it can access - not just *what kind* of data |
| Is customer identity verified per-session or per-request? | Per-session is simpler but vulnerable to mid-session takeover. Per-request is safer for CRITICAL-tier |
| Are the agent's write permissions scoped to this specific customer? | "Can write to shopping carts" is insufficient. "Can write to customer-12345's cart" is the control |
| What happens if the customer's account is compromised mid-session? | You need a revocation path from your identity provider to active agent sessions |
| How do you prevent cross-customer context contamination in concurrent sessions? | SESS-02 covers agent isolation. You also need to verify that shared resources (connection pools, caches) don't leak between customers |

### Design Pattern: Customer Context Injection

```
Customer authenticates → Your application verifies identity
  → Application creates agent session with:
    - Customer ID (verified, not user-supplied to the agent)
    - Scoped permissions (this customer's resources only)
    - Session binding token (ties agent session to customer session)
  → Agent receives customer context via system prompt or secure context injection
  → Agent CANNOT modify its own customer binding
  → All agent actions logged with both agent ID and customer ID
```

The critical principle: **customer identity is injected by your infrastructure, not extracted from the conversation.** If the agent determines which customer it's serving by reading the chat, an attacker can inject a different identity through the conversation.

### Offramps - Go Here Next

This framework gives you the AI-specific session controls. For customer authentication, session management, and identity propagation, these are the domain-specific resources:

| Topic | Resource | Why |
|-------|----------|-----|
| **Session management fundamentals** | [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | Token generation, session lifecycle, fixation prevention - the upstream controls your AI session inherits |
| **Authentication architecture** | Your identity platform documentation (Entra ID, Cognito, Auth0, Okta, Keycloak) | How customer identity tokens are issued, validated, and revoked. Your agent session must consume these, not reinvent them |
| **Payment authentication** | PCI-DSS Requirement 8 (your QSA or [PCI SSC Document Library](https://www.pcisecuritystandards.org/document_library/)) | If your agent handles payment data, PCI-DSS defines authentication requirements that apply *through* the agent, not just around it |
| **Customer data scoping** | Your data platform's row-level security or tenant isolation documentation | How your backend ensures the agent can only read/write this customer's data - the enforcement point beneath the agent |
| **Session revocation** | Your identity provider's real-time revocation documentation (token introspection, webhook-based revocation) | How to kill an active agent session when a customer reports account compromise |

**The framework's role:** Define the agent session controls (SESS-01–05), require customer identity binding, and mandate that write permissions are scoped to the authenticated customer - not just to a resource type.

**Your platform's role:** Implement the authentication, issue the scoped tokens, enforce row-level data access, and provide the revocation path.

