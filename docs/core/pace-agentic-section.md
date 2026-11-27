---
description: Defines the structured degradation path for autonomous AI systems, explaining why agents require a staged response between full autonomy and a complete shutdown.
---

# Agentic AI: Graceful Degradation and PACE Resilience

*This section defines the structured degradation path for autonomous AI systems. For stateless generative AI (chatbots, content tools), the Emergency response is simple: stop the service, route to fallback, fix, restart. For agentic AI, it's not.*

> *This document uses the simplified three-tier system (Tier 1/2/3). See [Risk Tiers - Simplified Tier Mapping](risk-tiers.md#simplified-tier-mapping) for the mapping to LOW/MEDIUM/HIGH/CRITICAL.*

## Why Agents Need a Degradation Path

Agentic AI systems can't be stopped the way you stop a web server. When you shut down an agent, you may be interrupting:

- **Mid-transaction workflows** - the agent has already committed state changes to external systems (database writes, API calls, file modifications) that need resolution
- **Held resources** - database locks, API sessions, file handles, reserved capacity that need clean release
- **Multi-agent dependencies** - other agents waiting for this agent's output, creating cascade risk
- **Scheduled operations** - timer-triggered or event-triggered actions that continue even when you stop accepting new requests
- **Accumulated state** - context, memory, and in-progress plans that represent hours of work and can't be cleanly discarded

"Turn it off" is not a resilience plan. It's a panic response that creates orphaned transactions, locked resources, and confused downstream systems. The degradation path provides structured alternatives between "fully autonomous" and "completely stopped."

![Agentic AI Graceful Degradation Path](../images/pace-degradation-path.svg){ .arch-diagram }

## The Five Degradation Phases

Each phase reduces the agent's autonomy while maintaining as much business value as possible. The phase boundaries are defined by **trigger criteria** that are configured before deployment and monitored in production.

### Phase 1: Normal

| Aspect | Detail |
|---|---|
| **Autonomy level** | Full, within defined boundaries |
| **What the agent can do** | Execute actions, call tools, make decisions, manage state |
| **Controls active** | Guardrails (P), Judge (P), Human Oversight on exception only |
| **Human role** | Monitor dashboards. Review exceptions. Periodic audit sampling. |
| **Trigger to Phase 2** | Judge flags behavioral anomaly; guardrail bypass rate exceeds threshold; action pattern deviates from baseline; external threat intelligence triggers review |

### Phase 2: Constrained

| Aspect | Detail |
|---|---|
| **Autonomy level** | Reduced scope |
| **What the agent can do** | Read-only tool access. Narrowed action space. Can still analyse, draft, recommend - but cannot execute changes. |
| **Controls active** | Guardrails (A - tightened thresholds), Judge (P - evaluating 100%), Human Oversight reviewing all outputs |
| **Human role** | Review all agent outputs. Approve any scope changes. Assess whether to restore or degrade further. |
| **What changes** | Write permissions revoked. Tool access restricted to read-only. Guardrail thresholds tightened. All outputs queued for review. |
| **Trigger to Phase 3** | Constraint breach detected; control failure in any layer; repeated Judge flags after constraint; human reviewer escalates concern |

### Phase 3: Supervised

| Aspect | Detail |
|---|---|
| **Autonomy level** | Propose only |
| **What the agent can do** | Draft action plans for human approval. No autonomous execution of any kind. Still provides analytical value. |
| **Controls active** | Guardrails (A), Judge (A - priority evaluation), Human Oversight (P - approving every action) |
| **Human role** | Approve or reject every proposed action. The agent is an assistant, not an actor. |
| **What changes** | Agent cannot call any tool without explicit human approval. Every proposed action is logged with the human decision. |
| **Trigger to Phase 4** | Integrity compromise confirmed; adversarial breach evidence; agent proposing actions that violate constraints even in supervised mode |

### Phase 4: Bypassed

| Aspect | Detail |
|---|---|
| **Autonomy level** | Isolated |
| **What the agent can do** | Nothing. Agent sessions quarantined. |
| **Controls active** | Circuit breaker active. Non-AI fallback path serving traffic. |
| **Human role** | Operate manual or rule-based process for business continuity. Security team investigates the agent. |
| **What changes** | All traffic routed to non-AI fallback. Agent isolated from all systems. Audit logs and agent state preserved for forensic analysis. |
| **Trigger to Phase 5** | Non-AI fallback path also compromised; investigation reveals fundamental design flaw requiring full rebuild; regulatory order to cease |

### Phase 5: Full Stop

| Aspect | Detail |
|---|---|
| **Autonomy level** | None |
| **What the agent can do** | Nothing. All sessions terminated. |
| **Controls active** | None. Service halted. |
| **Human role** | Incident response. Regulatory notification. Post-incident review. |
| **What changes** | Service unavailable. All agent sessions terminated with transaction resolution. Audit logs and state snapshots immutable and preserved. Stakeholders notified. |
| **Trigger to recovery** | Root cause identified. Fix implemented and validated. Degradation path tested. Risk function sign-off. Phased restart through Supervised → Constrained → Normal. |

## Transaction Resolution

Before an agent can transition to a lower phase, in-flight transactions must be resolved. For each tool in the agent's permission set, the architect must define the resolution strategy.

### Transaction Resolution Matrix

For every tool or system the agent can access, document:

| Question | If Yes | If No |
|---|---|---|
| **Can the action be rolled back?** | Include rollback in the phase transition procedure. Automate where possible. | Document that the action is irreversible and must be completed or abandoned with defined consequences. |
| **Can the action be completed safely without the agent?** | A human or rule-based system completes it as part of the transition. | The action must be abandoned. Document the consequences and notification requirements. |
| **Is partial completion dangerous?** | The transition procedure must either complete or roll back before the agent is isolated. No partial states allowed. | Partial state can be left for human resolution after transition. |
| **Does the action hold external locks or resources?** | Release procedure must be part of the transition. Define timeout for automated release. | No resource cleanup needed. |

### Example: Agent Processing Customer Loan Applications

| Tool / System | Rollback? | Complete without agent? | Partial dangerous? | Resolution |
|---|---|---|---|---|
| CRM record update | Yes | Yes (human) | No | Roll back uncommitted changes. Human completes any in-progress updates. |
| Credit bureau API query | No (read-only) | N/A | No | Let query complete. Discard results if not yet processed. |
| Decisioning engine submission | Yes (within window) | Yes (human resubmits) | Yes (partial submission corrupts record) | Must either complete submission or roll back entirely. No partial state. |
| Customer notification email | No (once sent) | Yes (human sends) | No | If queued but not sent, hold for human review. If sent, log and accept. |
| Document generation | No | Yes (human regenerates) | No | Discard incomplete documents. Human regenerates if needed. |

## Multi-Agent Cascade Prevention

When one agent in a multi-agent system transitions to a lower phase, the impact on other agents must be contained. Without explicit cascade prevention, one agent's shutdown can propagate unpredictably.

### Design Requirements

**1. Timeout and fallback for all inter-agent communication.**

Every agent that waits for another agent's output must have:
- A defined **timeout** (not indefinite wait)
- A **fallback behavior** when the timeout expires (return cached result, return error, escalate to human)
- No assumption that the other agent will respond

**2. Orchestrator awareness of agent health.**

The orchestrator (or coordination layer) must:
- Detect when an agent transitions to a lower phase
- Redistribute or queue pending work that was assigned to the degraded agent
- Prevent new work from being assigned to the degraded agent
- Notify dependent agents of the state change

**3. No blocking dependencies.**

No agent should be able to indefinitely block another agent's progress. If Agent A needs Agent B's output to proceed:
- Agent A must have a timeout
- Agent A must have a degraded-mode path that works without Agent B's output
- The system must not deadlock if both agents are waiting for each other

**4. Phase transitions are observable.**

All phase transitions must be:
- Logged as auditable events with timestamp, trigger, and authoriser
- Visible to the orchestrator and all dependent agents
- Communicated to the human oversight function

## State Preservation for Post-Incident Analysis

When the degradation path activates (any transition below Normal), the following must be preserved before the agent's state changes:

| Artefact | Why | How |
|---|---|---|
| **Agent memory and context** | Understand what the agent "knew" when the anomaly occurred | Snapshot to immutable storage before phase transition |
| **In-progress plans and pending actions** | Determine what the agent was about to do | Export from orchestrator queue |
| **Tool call history** | Trace what external actions were taken | API call logs with timestamps, parameters, and responses |
| **Judge evaluation state** | Understand what the Judge flagged and when | Export Judge scores, confidence levels, and flag reasons |
| **Guardrail hit log** | Identify what was blocked and what passed | Export guardrail engine logs for the session |
| **Inter-agent messages** | Trace multi-agent coordination for cascade analysis | Export from message bus or orchestrator |

All preservation must be automated. The agent must not be able to modify its own logs during a phase transition. Immutability is enforced at the infrastructure layer.

## Recovery: Stepping Back Up

Recovery is not "restart and hope." It's a phased return through the degradation path:

| Step | Action | Validation |
|---|---|---|
| 1 | Root cause identified and fix implemented | Documented in incident report |
| 2 | Fix validated in non-production environment | Test suite passes; adversarial test suite passes |
| 3 | Restart in **Supervised** phase (agent proposes, human approves) | Run for defined period (minimum 4 hours at Tier 2, 24 hours at Tier 3) with production traffic |
| 4 | Promote to **Constrained** phase (reduced scope, enhanced monitoring) | Judge confidence scores within baseline for defined period |
| 5 | Promote to **Normal** phase | All control layers healthy; monitoring confirms baseline behavior; risk function sign-off (Tier 3) |

At Tier 3, each step-up requires explicit authorisation. The agent does not return to Normal automatically.

## Pre-Deployment Requirements

No agentic AI system should enter production without:

- [ ] All five degradation phases defined with trigger criteria
- [ ] Transaction resolution matrix completed for every tool in the agent's permission set
- [ ] Multi-agent cascade prevention designed and tested (if multi-agent)
- [ ] State preservation automation validated
- [ ] Non-AI fallback path documented, tested, and staffed
- [ ] Recovery (step-back-up) procedure documented with authorisation gates
- [ ] Full degradation walkthrough completed with production-equivalent scenario

