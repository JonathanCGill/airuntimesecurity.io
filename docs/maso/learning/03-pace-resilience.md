# Module 3: PACE Resilience

**Designing for failure with Primary, Alternate, Contingency, Emergency.**

## The PACE Principle

PACE comes from military communications planning. It ensures mission-critical functions continue when the preferred method fails by pre-defining four layers of redundancy — each on a different failure domain so a single event cannot cascade through all of them.

In MASO, PACE is a **core design principle**, not an optional overlay. Every control must have a defined failure mode and fallback path before the system enters production.

> Defence in depth tells you to have multiple layers. PACE tells you what happens when each layer fails, how to transition between operational states, how to step back up after an incident, and how to test whether your fallback actually works.

## The Four Phases

```
 ┌──────────────────────────────────────────────────────────┐
 │  PRIMARY          All controls operational.              │
 │                   Normal autonomy within tier.           │
 │                                                          │
 │       ──── Agent anomaly or single layer degraded ────   │
 │                           ▼                              │
 │  ALTERNATE         One component degraded.               │
 │                   Scope tightened. Extra approvals.       │
 │                   Backup agent activated if needed.       │
 │                                                          │
 │       ──── Multiple layers degraded ────                 │
 │                           ▼                              │
 │  CONTINGENCY       Multi-agent orchestration suspended.  │
 │                   Single agent, fully supervised.         │
 │                   Human approves every action.            │
 │                                                          │
 │       ──── Confirmed compromise or cascade ────          │
 │                           ▼                              │
 │  EMERGENCY         All agents terminated.                │
 │                   Tool access revoked. Non-AI fallback.  │
 │                   Incident response engaged.             │
 │                                                          │
 │       ──── Root cause fixed, controls verified ────      │
 │                           ▼                              │
 │                   Return to PRIMARY                      │
 └──────────────────────────────────────────────────────────┘
```

### Primary — Normal Operations

All agents active within designated roles. Full three-layer security stack operational. Inter-agent communication through the signed message bus. Behavioral baselines actively monitored.

### Alternate — Agent Failover

**Trigger:** Single agent shows anomalous behavior, or one security layer degrades.

**Response:**
- Isolate the anomalous agent
- Activate a backup agent (ideally from a different model provider to avoid correlated failures)
- Tighten tool permissions to read-only across the affected chain
- All write operations require human approval
- Notify the security team

**Transition authority:** Automated at Tier 2+. Multi-agent cascading failures move faster than human response times. Humans are notified, not gated.

### Contingency — Degraded Mode

**Trigger:** Multiple agents compromised, message bus integrity questioned, or the alternate agent also exhibits anomalous behavior.

**Response:**
- Suspend multi-agent orchestration entirely
- Single pre-validated agent operates in fully supervised mode
- Human approves every action
- All agent state captured for forensics

**Transition authority:** Security team or AI security officer.

### Emergency — Full Shutdown

**Trigger:** Cascading failures, confirmed data exfiltration, coordinated manipulation, or rogue agent behavior.

**Response:**
- All agents terminated via circuit breaker
- Tool access revoked at infrastructure level
- Memory and context snapshots preserved in immutable storage
- Non-AI fallback activated
- Full incident response engaged

**Transition authority:** CISO or incident commander.

### Recovery (Emergency to Primary)

Recovery is not "restart." It requires:
1. Post-incident review confirming root cause identification
2. Control remediation applied and verified
3. Updated baselines reflecting the new threat understanding
4. Verification that no poisoned data persists in any agent's memory, context, or RAG corpus
5. Phased return: E → C → A → P, not E → P directly

## The Two-Axis Model

PACE applies on two axes simultaneously:

**Horizontal PACE** — across the three defence layers:
- If Guardrails fail → LLM-as-Judge becomes primary defence
- If Judge fails → Human Oversight absorbs more
- If Human Oversight is overwhelmed → Circuit Breaker activates

**Vertical PACE** — within each defence layer:
- If the guardrail engine is slow → fall back to a stricter, simpler rule set
- If it is down entirely → adopt configured fail posture (open or closed)
- If it is compromised → isolate and escalate

Both axes must be defined before deployment.

## The Architect's Most Important Decision: Fail Posture

When a control degrades, it does one of two things:

- **Fail-open:** Allow traffic to pass, rely on remaining layers. Accepts risk for continuity.
- **Fail-closed:** Block all AI traffic through the degraded layer. Accepts disruption for safety.

**The rule of thumb:**

| Tier | Default Fail Posture | Rationale |
|------|---------------------|-----------|
| Tier 1 | Fail-open acceptable | Internal, low consequence. Log everything. Fix next business day. |
| Tier 2 | Fail-closed by default | Customer-facing, human-reviewed. Automated switchover to fallback. |
| Tier 3 | Fail-closed always | Regulated, autonomous. No AI traffic passes a degraded control. |

## Multi-Agent PACE vs Single-Agent PACE

Multi-agent systems fail differently. Three key distinctions:

**1. Blast radius is wider.** A compromised agent can inject instructions into the message bus that affect every downstream agent. Containment must isolate the agent *and* quarantine its recent outputs across the chain.

**2. Transitions must be faster.** At Tier 2+, the monitoring agent or orchestrator can initiate P→A transitions without waiting for human approval — because cascading failures propagate faster than humans can respond.

**3. Recovery requires chain verification.** Stepping back from C→A or A→P requires verifying that no poisoned data from the compromised agent persists in other agents' memory, context, or RAG corpus. You cannot just restart the failed component.

## Testing Your PACE Plan

A PACE plan that has not been tested is a plan that will not work.

| Test Type | Tier 1 | Tier 2 | Tier 3 |
|-----------|--------|--------|--------|
| Guardrail failure simulation | Annually | Quarterly | Monthly |
| Judge failure simulation | Annually | Quarterly | Monthly |
| Human escalation exercise | Annually | Quarterly | Quarterly |
| Circuit breaker activation | Annually | Quarterly | Monthly |
| Full degradation walkthrough | — | Semi-annually | Quarterly |
| Non-AI fallback operation | Annually | Quarterly | Monthly |
| Recovery (step-back-up) validation | Annually | Quarterly | Monthly |

For Tier 3 systems, testing should involve the same personnel who would handle a real incident, using the same tools and communication channels.

## Applying PACE to Your Solution

**Before deployment, answer these questions for every control:**

1. What is the Primary mechanism?
2. What triggers a transition to Alternate?
3. What is the Alternate mechanism, and is it on a different failure domain?
4. What triggers a transition to Contingency?
5. What does Contingency look like — and can the business operate in that mode?
6. What triggers Emergency?
7. What is the non-AI fallback, and has it been tested?
8. What are the conditions for recovery back to Primary?

If any answer is "we'll figure it out when it happens," the system is not ready for production.

---

**Next:** [Module 4: The Seven Control Domains](04-seven-control-domains.md)
