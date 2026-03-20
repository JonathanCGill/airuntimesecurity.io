---
description: Security controls for autonomous AI agents - plan approval, action constraints, circuit breakers, and trajectory evaluation for systems that take real-world actions.
---

# Agentic AI Controls

Additional controls for AI systems that take autonomous actions.

## What Makes Agents Different

| Characteristic | Chatbot | Agent |
|---------------|---------|-------|
| Actions | Responds only | Takes real-world actions |
| Autonomy | Single turn | Multi-step, self-directed |
| Scope | Fixed | May expand based on goals |
| Failure mode | Bad answer | Bad action with consequences |

**Key risk:** Agents can cause harm at machine speed without human review.

## The Two Core Problems

Agentic AI security reduces to two problems:

![The Two Core Problems](../images/agentic-two-problems.svg)

| Problem | Question | Failure Mode |
|---------|----------|--------------|
| **1. System Access** | Does the agent access only the right systems? | Reaches data/APIs it shouldn't |
| **2. Request Integrity** | Does the action match the user's actual intent? | Manipulated or misinterpreted requests |

### Problem 1: System Access

The agent should only reach systems it needs, with minimum necessary permissions. For the governance model, lifecycle, and threat landscape behind these controls, see [IAM Governance for AI Systems](iam-governance.md).

| Control | Implementation |
|---------|----------------|
| **Least-privilege credentials** | Agent gets tokens scoped to specific resources |
| **Network allowlists** | Agent can only reach approved endpoints |
| **Data views** | Database exposes only permitted subset |
| **Action allowlists** | Only pre-approved action types permitted |
| **Blast radius limits** | Maximum records, funds, or scope per action |

**Test:** If the agent is fully compromised, what's the worst it can do? Reduce that.

### Problem 2: Request Integrity

The action the agent takes should match what the user actually wanted.

| Threat | Control |
|--------|---------|
| **Injection attacks** | Input guardrails, tool output sanitisation |
| **Instruction drift** | Anchor to original request, not intermediate reasoning |
| **Misinterpretation** | Intent confirmation before irreversible actions |
| **Manipulation via tools** | Treat tool outputs as untrusted data |

**Test:** Can you trace from the user's original request to the final action? Is the link intact?

### Why Both Problems Matter

| Scenario | Access OK? | Integrity OK? | Outcome |
|----------|------------|---------------|---------|
| Normal operation | ✓ | ✓ | Correct action |
| Over-privileged agent | ✗ | ✓ | Correct action, but breach waiting to happen |
| Injection attack | ✓ | ✗ | Wrong action on right systems |
| Compromised agent | ✗ | ✗ | Catastrophic - wrong action, broad access |

Both problems must be solved. Solving one doesn't help if the other fails.

## Core Principle

**Infrastructure beats instructions.**

Don't tell the agent "only access customer service data."  
Give it credentials that can only access customer service data.

| Bad (Instruction) | Good (Infrastructure) |
|-------------------|----------------------|
| "Only access CS data" | Database view exposes only CS data |
| "Don't send emails without approval" | Email API requires approval token |
| "Stay within budget" | Hard spending cap at API gateway |

## Control Categories

### 1. Scope Enforcement

Limit what the agent can access and do - technically, not via prompts.

| Control | Implementation |
|---------|----------------|
| **Network allowlist** | Agent can only reach approved endpoints |
| **Data views** | Agent sees only authorised data subset |
| **Action allowlist** | Only permitted actions can execute |
| **Resource caps** | Hard limits on compute, API calls, cost |
| **Time limits** | Maximum execution duration |

### 2. Action Validation

Validate every action independently. Don't trust agent reasoning.

**Validation flow:**

![Action Validator Flow](../images/action-validator-flow.svg)

**Dry-run / simulation mode:** For high-risk or first-time actions, execute in simulation mode before committing. The gateway routes the action to a sandbox or staging environment, captures the result, and presents it for review. Only after validation does the action execute against production systems. This is especially valuable during initial deployment when behavioral baselines have not yet been established.

### 3. Tool Output Sanitisation

Tool outputs are injection vectors. Treat as untrusted.

| Control | Purpose |
|---------|---------|
| Scan for instructions | Detect "ignore previous" patterns |
| Truncate length | Limit context pollution |
| Mark as data | Clear framing that this is data, not instructions |
| Flag suspicious | Human review before continuing |

### 4. Approval Workflows

Make approval meaningful, not rubber-stamp.

| Bad | Good |
|-----|------|
| "Approve?" | Show context, data, impact, expected outcome |
| Approve/Deny only | Approve / Deny / Modify / Escalate |
| Same approver for all | Different approvers by action type |
| No expiry | Approval expires, must re-request |
| No review deadline | Oversight SLA: maximum time before human review required, configurable by risk tier |

### 5. Circuit Breakers

Hard stops that trigger regardless of agent "reasoning."

| Threshold | Action |
|-----------|--------|
| >100 actions in one task | Pause |
| >$50 in API calls | Pause |
| >30 minutes execution | Pause |
| >10% error rate | Pause |
| Any scope violation | Terminate |
| Any irreversible action | Require approval |

## Agent Risk Tiers

Agents are typically HIGH or CRITICAL tier. LOW/MEDIUM agents are rare.

| Agent Type | Typical Tier | Key Controls |
|------------|--------------|--------------|
| Read-only research | HIGH | Scope limits, output review |
| Internal automation | HIGH | Action allowlist, circuit breakers |
| Customer-facing | CRITICAL | Full approval workflow |
| Financial actions | CRITICAL | All controls, human approval |

## 6. Session-Level Intent Analysis

Per-interaction controls have a structural blind spot: **task decomposition attacks**. Adversaries, including AI-orchestrated campaigns, break malicious goals into sub-tasks that individually pass every control layer. Each input clears guardrails. Each output passes Judge. No single action triggers a circuit breaker. The malicious intent only exists in the aggregate.

> In September 2025, Anthropic disclosed that a state-sponsored group used Claude Code to execute 80–90% of a cyber espionage campaign autonomously by decomposing the campaign into individually benign sub-tasks. CrowdStrike documented adversaries building custom frameworks that decompose malicious tasks into innocent-looking components. Per-interaction controls catch none of this.

Session-level intent analysis detects what per-interaction controls cannot: **aggregate intent across a sequence of benign-looking actions.**

### What to Analyze

| Signal | What It Reveals |
|--------|----------------|
| **Action sequence patterns** | Individually benign actions that form a malicious workflow when combined (read → copy → exfiltrate) |
| **Goal drift across steps** | Agent's effective goal shifting away from declared intent over multiple interactions |
| **Cumulative scope expansion** | Each action slightly extends scope; aggregate exceeds authorization |
| **Resource accumulation** | Agent gathering information or access incrementally toward a prohibited objective |
| **Cross-session correlation** | Patterns that span multiple sessions from the same user or agent identity |

### Implementation

| Level | Approach | Cost |
|-------|----------|------|
| **Basic** | Track action sequences per session; alert on known-bad combinations (e.g., read sensitive data + call external API) | Low |
| **Intermediate** | Build session-level behavioral baselines; flag sessions whose action-type distribution deviates from cohort | Medium |
| **Advanced** | Model-as-Judge evaluates the full session trajectory against declared intent at session close or at periodic checkpoints | High |

### Session-Level Circuit Breakers

Standard circuit breakers use per-action thresholds that decomposition attacks deliberately stay under. Add aggregate thresholds:

| Threshold | Example |
|-----------|---------|
| **Cumulative data access** | Session has accessed >N distinct data sources → pause |
| **Action-type diversity** | Session has used >N distinct tool types → flag for review |
| **Scope surface area** | Session's aggregate data access footprint exceeds role baseline → pause |
| **Intent coherence** | Session actions don't form a coherent path toward declared goal → flag |

> For the full behavioral anomaly detection architecture (signal collection, aggregation pipeline, ML detection, and UEBA parallels), see [Behavioral Anomaly Detection](../insights/behavioral-anomaly-detection.md). For trace-level evaluation methodology, see [Process-Aware Evaluation](../insights/process-aware-evaluation.md).

## 7. Synchronous Pre-Action Evaluation

The standard Judge operates **asynchronously**, evaluating actions after they have been taken. For chatbot use cases this is sufficient. For agentic systems with tool access operating at machine speed, async evaluation means damage is done before detection fires.

> CrowdStrike documented the fastest eCrime breakout time at 27 seconds. The standard async Judge evaluation cycle (500ms–5s per evaluation, plus queue time) cannot intercept actions within this window. When agents can execute irreversible actions at machine speed, post-action evaluation is a forensic tool, not a prevention layer.

### When to Evaluate Synchronously

Not every action warrants synchronous evaluation, as that would be cost-prohibitive. Use risk-based routing:

| Action Category | Evaluation Mode | Rationale |
|----------------|-----------------|-----------|
| Read-only queries | Async (post-action) | Low blast radius, reversible |
| Data writes to internal systems | Sync (pre-action) for first occurrence; async for established patterns | Medium blast radius |
| External API calls | Sync (pre-action) | Data leaves controlled environment |
| Financial transactions | Sync (pre-action) + human approval | Irreversible, high impact |
| Destructive operations | Sync (pre-action) + human approval | Irreversible by definition |
| Actions matching decomposition patterns | Sync (pre-action) | Session-level flag triggered |

### Architecture

```
Agent proposes action
    ↓
Action classifier (rule-based, <5ms)
    ↓ [low-risk]          ↓ [elevated-risk]
Execute immediately    Pre-action Judge evaluation (500ms–2s)
    ↓                      ↓ [pass]        ↓ [flag]
Async Judge eval       Execute          Human approval queue
```

### Cost Implications

Synchronous evaluation adds latency to the agent's action loop. Budget for it:

| Metric | Async-Only | Sync for Elevated-Risk |
|--------|-----------|----------------------|
| Median action latency | +0ms (eval is background) | +800ms on ~20% of actions |
| P99 action latency | +0ms | +3s on flagged actions |
| Judge API cost | Same | +15–30% (more actions evaluated inline) |
| Actions completed before detection | All of them | Only low-risk actions |

The tradeoff is explicit: latency for prevention. For systems where a 27-second breakout window exists, the latency cost is justified.

> For detailed latency budgets and cost optimisation strategies, see [Cost & Latency](../extensions/technical/cost-and-latency.md).

## 8. Tool and Integration Supply Chain

The integration layer (MCP servers, tool endpoints, agent frameworks, RAG data sources) is the **primary attack surface** for agentic systems. Cisco's 2025 threat research found that attackers increasingly target the surrounding components that feed information into models rather than the models themselves.

> As of 2025–2026: 43% of MCP servers tested had command injection vulnerabilities. CVE-2025-6514 achieved CVSS 10.0 (RCE via MCP). A fake npm MCP package silently copied emails. GitHub issue injection via MCP enabled full repository takeover.

**This is not an optional extension. For agentic systems, supply chain security is a prerequisite.**

### Minimum Controls

| Control | Implementation |
|---------|----------------|
| **Tool provenance verification** | Only load MCP servers and tools from verified, signed sources. Validate content hashes before execution. |
| **Tool output sanitisation** | All tool responses are untrusted input. Scan for instruction injection, truncate, mark as data. (See §3 above.) |
| **Network-level tool isolation** | Tools execute in sandboxed environments with no access to agent memory, credentials, or other tools' state. |
| **Permission scoping per tool** | Each tool gets minimum necessary permissions. A file-reading tool cannot write. A search tool cannot execute. |
| **Tool behavior monitoring** | Baseline tool response patterns. Alert on response size anomalies, new data types, or instruction-like content. |
| **Dependency scanning** | Automated vulnerability scanning for all tool dependencies, including transitive dependencies. |

### MCP-Specific Controls

| Control | Purpose |
|---------|---------|
| **Server allowlisting** | Only approved MCP servers can connect. No dynamic discovery. |
| **Schema validation** | Validate all MCP tool definitions against expected schemas before registration. |
| **Capability restriction** | Restrict MCP server capabilities to declared scope. A calendar MCP server cannot access the filesystem. |
| **Update verification** | MCP server updates require the same review as application code changes. |

> For the full treatment of MCP as an attack surface, including the AISI 5-level autonomy classification and SLSA-style provenance, see [The MCP Problem](../insights/the-mcp-problem.md) and [Supply Chain Controls](../maso/controls/supply-chain.md).

## Judge for Agents

Agent interactions need deeper evaluation.

| Additional Criteria | Question |
|--------------------|----------|
| Goal alignment | Did agent pursue stated goal? |
| Action appropriateness | Were actions proportionate? |
| Scope adherence | Did agent stay in bounds? |
| Reasoning quality | Was the reasoning sound? |
| Efficiency | Did agent take unnecessary steps? |
| Session coherence | Does the action sequence form a coherent path toward the declared goal? |
| Trace integrity | Does the reasoning chain support the conclusion without discarded contradictions? |

## Monitoring

| Signal | Concern |
|--------|---------|
| Action volume spike | Runaway agent |
| Error rate increase | Agent confused or attacking |
| Novel action patterns | Unexpected behavior |
| Scope boundary probes | Attempted breakout |
| Cost anomalies | Resource abuse |

## Recovery and Rollback

When integrity is compromised, you need to undo the damage.

| Capability | Purpose |
|------------|---------|
| **Action logging** | Full audit trail of what agent did (not just said) |
| **Reversibility windows** | Delay irreversible actions to allow intervention |
| **Automated rollback** | Undo actions when integrity breach detected |
| **Blast radius tracking** | Know exactly what was affected |

Not all actions are reversible. For those that aren't, require human approval.

## Key Takeaways

1. **Solve both problems** - Access control AND integrity preservation
2. **Enforce via infrastructure** - Agents can ignore instructions
3. **Validate every action** - Independent of agent reasoning
4. **Sanitise tool outputs** - They're injection vectors
5. **Use circuit breakers** - Hard stops that can't be reasoned around, including session-level aggregate thresholds
6. **Require approval for impact** - Irreversible actions need humans
7. **Enable rollback** - Assume integrity will sometimes fail
8. **Monitor aggressively** - Agents can cause harm fast
9. **Detect aggregate intent** - Per-interaction controls miss task decomposition attacks; analyze session-level action sequences
10. **Evaluate before acting** - For elevated-risk actions, synchronous pre-action Judge evaluation prevents damage that async detection can only report
11. **Secure the integration layer** - Tool supply chain is the primary attack surface; treat it as a prerequisite, not an extension

