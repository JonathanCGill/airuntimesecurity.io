# Module 7: Key Takeaways and Quick Reference

**Condensed principles, checklists, and decision aids.**

## The Five Things to Remember

1. **Multi-agent systems fail differently.** Risks compound across agents. Delegation creates implicit authority. Consensus is not correctness. Security models designed for single-agent systems are insufficient.

2. **Three layers, independent mechanisms.** Guardrails prevent (deterministic). Judge detects (probabilistic). Humans decide (cognitive). Circuit breakers contain (infrastructure). Independence is the point — a single failure cannot cascade through all of them.

3. **Design for failure with PACE.** Every control must have a defined failure mode and fallback before production. Primary → Alternate → Contingency → Emergency. If any answer is "we'll figure it out when it happens," the system is not ready.

4. **Enforce at infrastructure, not prompts.** Role boundaries, permission scopes, blast radius caps, and circuit breakers must be infrastructure controls. Prompt-based controls weaken under context pressure, adversarial input, and model updates.

5. **Start supervised, graduate with evidence.** Begin at Tier 1. Build operational baselines. Catalog failure modes. Calibrate trust. Graduate to Tier 2 and 3 only after demonstrating control effectiveness.

## Core Principles Quick Reference

| Principle | What It Means |
|-----------|--------------|
| Agents are Non-Human Identities | Each agent has its own identity, credentials, and permissions. No sharing, no inheritance. |
| No transitive authority | Delegation chains cannot accumulate permissions. Separate request, approve, and execute roles. |
| Inter-agent messages are untrusted input | Guardrails run at every agent boundary, not just external interfaces. |
| Structured data over natural language | Constraints, uncertainty, provenance, and assumptions travel as typed fields, not prose. |
| The Judge evaluates the aggregate | Multi-step plans are reviewed as a whole, not just individual outputs. |
| Blast radius caps are infrastructure | Maximum impact limits are enforced by the platform, not by agent judgment. |
| Token exhaustion is a dual failure path | Context pressure degrades the agent *and* the Judge simultaneously. This correlated failure must trigger PACE transitions, not just alerts. |
| Observability is not optional | If you cannot explain what happened and why, you cannot govern the system. |
| Test your fallbacks | A PACE plan that has not been tested is a plan that will not work. |

## Seven Control Domains at a Glance

| # | Domain | One-Line Summary |
|---|--------|-----------------|
| 0 | Prompt, Goal & Epistemic Integrity | Protect what agents think and believe |
| 1 | Identity & Access | Control who agents are and what they can reach |
| 2 | Data Protection | Fence what agents can see and share |
| 3 | Execution Control | Bound what agents can do and how much damage they can cause |
| 4 | Observability | See what agents are doing and detect drift |
| 5 | Supply Chain | Verify where agents and their components come from |
| 6 | Privileged Agent Governance | Apply elevated controls to agents with elevated power |

## Three-Tier Progression

| | Tier 1: Supervised | Tier 2: Managed | Tier 3: Autonomous |
|---|---|---|---|
| **Human role** | Approves all actions | Approves high-consequence | Handles exceptions |
| **Guardrails** | Mandatory | Mandatory | Mandatory |
| **Judge** | Optional | Mandatory | Mandatory |
| **Inter-agent auth** | Logged, not encrypted | Signed and validated | Certificate-based NHI |
| **Behavioral monitoring** | Periodic/batch | Continuous with alerts | Real-time with auto-response |
| **PACE testing** | Annually | Quarterly | Monthly |
| **Use when** | Pilot, initial production | Operational with oversight | Mature, trusted systems |

## Emergent Risk Categories

| Category | Count | Key Insight |
|----------|-------|-------------|
| Epistemic | 9 | Agents corrupt each other's reasoning without any attacker |
| Coordination | 4 | Deadlock, oscillation, role drift, goal drift |
| Security | 6 | Cross-agent injection, confused deputy, privilege escalation |
| Safety & Misuse | 2 | Harm via decomposition, persuasion optimization |
| Data | 3 | Memory poisoning, RAG poisoning, provenance loss |
| Governance | 2 | Non-determinism, metric gaming |
| Operational | 3 | Cost blowouts, latency compounding, silent partial failure |
| Human Factors | 2 | Automation bias, accountability blur |
| Inference-Side | 3 | Model extraction, membership inference, side-channel |

## PACE Quick Decision Guide

```
Is a control layer degraded or an agent anomalous?
  │
  ├── No → Stay in PRIMARY
  │
  ├── One layer / one agent → Move to ALTERNATE
  │   • Isolate affected component
  │   • Tighten permissions (read-only across chain)
  │   • All writes need human approval
  │   • Activate backup agent (different provider if possible)
  │
  ├── Multiple layers / multiple agents → Move to CONTINGENCY
  │   • Suspend multi-agent orchestration
  │   • Single agent, fully supervised
  │   • Human approves every action
  │
  └── Confirmed compromise or cascading failure → Move to EMERGENCY
      • Circuit breaker: terminate all agents
      • Revoke tool access at infrastructure level
      • Snapshot memory and context for forensics
      • Activate non-AI fallback
      • Engage incident response

Recovery: E → C → A → P (never skip phases)
  • Verify root cause fixed
  • Confirm no poisoned data persists
  • Update baselines
  • Test controls before stepping up
```

## Solution Design Checklist

Use this when designing a new multi-agent system or assessing an existing one.

### Identity & Boundaries
- [ ] Every agent has a unique Non-Human Identity
- [ ] No shared credentials between agents
- [ ] Credentials are short-lived and auto-rotated
- [ ] Each agent has an explicit tool allow-list
- [ ] Blast radius caps defined per agent

### Communication
- [ ] All inter-agent communication through controlled message bus
- [ ] Messages signed with sender identity
- [ ] Schema includes provenance, confidence, assumptions, unknowns
- [ ] Rate limits per agent on the bus
- [ ] Source tagging distinguishes data from instructions

### Defence Layers
- [ ] Guardrails at every agent boundary (not just external)
- [ ] Judge is a different model from task agents
- [ ] Judge evaluates inter-agent communication, not just final outputs
- [ ] Human oversight scaled to consequence level
- [ ] Circuit breaker is infrastructure-level, tested, and fast

### Epistemic Integrity
- [ ] Consensus diversity gates prevent unchallenged agreement
- [ ] Claim provenance metadata on all inter-agent claims
- [ ] Uncertainty signals preserved through the chain
- [ ] Self-referential evidence prohibited
- [ ] At least one challenger/adversarial agent for high-consequence decisions

### Token Exhaustion Controls
- [ ] Token budget monitored per agent as a first-class operational metric
- [ ] Alert thresholds defined (warning, critical, exhaustion) per tier
- [ ] Context rotation strategy: checkpoint structured state, flush, resume
- [ ] Checkpointed state uses typed fields, not free-text summaries
- [ ] Retry caps per agent to prevent error-accumulation degradation
- [ ] Judge context managed independently from task agents
- [ ] Correlated agent + Judge exhaustion defined as a PACE trigger
- [ ] Tier 2+: fail-closed on affected agent at critical threshold
- [ ] Tier 3: automatic PACE transition at critical threshold

### Operational Resilience
- [ ] PACE transitions defined for every control
- [ ] Fail posture (open/closed) documented per control per tier
- [ ] Non-AI fallback path exists and is tested
- [ ] Recovery procedures include chain verification

### Observability & Governance
- [ ] Immutable decision chain logs per agent
- [ ] Behavioral baselines established and monitored
- [ ] SIEM/SOAR integration for broader security correlation
- [ ] Accountability clearly assigned for system outcomes
- [ ] Regular red team exercises at appropriate frequency for tier

## Further Reading

| Topic | Document |
|-------|----------|
| Full framework | [MASO README](../README.md) |
| Control specifications | [Controls directory](../controls/) |
| Implementation by tier | [Tier 1](../implementation/tier-1-supervised.md) · [Tier 2](../implementation/tier-2-managed.md) · [Tier 3](../implementation/tier-3-autonomous.md) |
| Red team playbook | [Red Team](../red-team/red-team-playbook.md) |
| Integration patterns | [Integration Guide](../integration/integration-guide.md) |
| Worked examples | [Industry Examples](../examples/worked-examples.md) |
| PACE methodology | [PACE Resilience](../../PACE-RESILIENCE.md) |
| Use case definition | [Use Case Framework](../../strategy/use-case-definition.md) |
