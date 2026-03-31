---
description: One-page AI security reference. Classify systems, select controls, define failure postures, and make rapid deployment decisions.
---

# AI Security Cheat Sheet

*Classify. Control. Define fail posture. Test. One page.*

> *This document uses the simplified three-tier system (Tier 1/2/3). See [Risk Tiers - Simplified Tier Mapping](core/risk-tiers.md#simplified-tier-mapping) for the mapping to LOW/MEDIUM/HIGH/CRITICAL.*

## 1. Classify

| All four true? | → **Fast Lane** - self-certify, deploy in days |
|---|---|
| Internal users only | Read-only (no write to external systems) |
| No regulated data (PII, financial, health, legal) | Human reviews before acting on output |

**If any criterion fails**, classify by the highest applicable:

| Tier | When | Example |
|---|---|---|
| **1 - Low** | Internal users. May have write access or unreviewed output. No regulated decisions. | Internal chatbot, code assistant, meeting summariser |
| **2 - Medium** | Customer-facing. Human reviews before delivery. | Customer support draft, document processing, decision support |
| **3 - High** | Regulated decisions, autonomous agents with write access, financial/medical/legal. | Loan decisioning, autonomous trading, clinical support |

## 2. Controls Required

| Control | Fast Lane | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|---|
| **Guardrails** | Basic filter | Standard | Full suite + injection detection | Hardened, multi-layer |
| **Model-as-Judge** | - | 10–20% sample | 100% async | 100% dual-model, pre+post action |
| **Human Oversight** | - | - | Dedicated reviewers, SLA-bound | Domain experts, dual approval |
| **Circuit Breaker** | Feature flag | Feature flag | Automated health-check | Automated + staffed fallback |
| **Usage Logging** | Yes | Yes | Yes | Yes |

**Agentic add-ons** (if agent has write access): tool permission matrix, transaction resolution plan, multi-agent cascade prevention, 5-phase degradation path (Tier 2+), token budget monitoring with context rotation (all tiers).

## 3. Fail Posture

For **each** control, define: when it fails, does the system fail-open or fail-closed?

| Tier | Default | What It Means |
|---|---|---|
| **Fast Lane / Tier 1** | Fail-open | Pass traffic. Log. Fix next business day. |
| **Tier 2** | Fail-closed | Block AI traffic. Auto-switch to fallback. |
| **Tier 3** | Fail-closed always | No AI traffic passes a degraded control. No exceptions. |

**Fallback path:**

| Tier | Fallback | Speed | Maintenance |
|---|---|---|---|
| Fast Lane | Manual process (already exists) | Hours | Near zero |
| Tier 1 | Manual process (documented) | Hours | Near zero |
| Tier 2 | Rule-based / templated | Minutes (auto) | Quarterly |
| Tier 3 | Staffed parallel process | Seconds (auto) | Monthly |

## 4. Agentic Degradation Path

If deploying an agent, define these five phases before go-live:

| Phase | Autonomy | What Changes |
|---|---|---|
| **Normal** | Full | All controls active |
| **Constrained** | Reduced | Read-only tools, tightened thresholds, all outputs reviewed |
| **Supervised** | Propose only | Human approves every action |
| **Bypassed** | Isolated | Non-AI fallback active, agent quarantined |
| **Full Stop** | None | All sessions terminated, incident response |

For each tool the agent uses, answer: Can the action be rolled back? Completed without the agent? Is partial completion dangerous?

## 4b. Multi-Agent Systems

If deploying **multiple agents** that communicate, delegate, or act across trust boundaries, single-agent controls are necessary but not sufficient. The **[MASO Framework](maso/)** adds seven control domains on top of the foundation.

| MASO Control | What It Addresses |
|---|---|
| **Prompt, Goal & Epistemic Integrity** | Injection propagation across agents, goal drift, hallucination amplification, groupthink |
| **Identity & Access** | Non-Human Identity per agent, no shared credentials, no transitive authority |
| **Data Protection** | Cross-agent data fencing, DLP on the message bus, memory isolation |
| **Execution Control** | Sandboxed execution, blast radius caps, Model-as-Judge gate, interaction timeouts |
| **Observability** | Decision chain audit, anomaly scoring, drift detection, independent kill switch |
| **Supply Chain** | AIBOM per agent, signed tool manifests, MCP server vetting |
| **Privileged Agent Governance** | Elevated controls for orchestrators, planners, and meta-agents with disproportionate authority |

**Implementation tiers:** [Tier 1 - Supervised](maso/implementation/tier-1-supervised.md) (human approves all writes) → [Tier 2 - Managed](maso/implementation/tier-2-managed.md) (auto-approve low-risk, escalate high-risk) → [Tier 3 - Autonomous](maso/implementation/tier-3-autonomous.md) (self-healing PACE, adversarial testing, kill switch).

**Key difference from single-agent:** PACE extends to agent orchestration. When one agent fails, the system isolates that agent and tightens permissions across the chain - not just within a single model's control layers.

**→ [Full MASO Framework](maso/)**

## 5. Test

| Test | Fast Lane | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|---|
| Feature flag / kill switch works | Annual | Annual | Quarterly | Monthly |
| Control layer failure simulation | - | Annual | Quarterly | Monthly |
| Human escalation exercise | - | Annual | Quarterly | Quarterly |
| Full degradation walkthrough | - | - | Semi-annual | Quarterly |
| Non-AI fallback operation | Annual | Annual | Quarterly | Monthly |
| Recovery (step back up) | - | Annual | Quarterly | Monthly |

## The Six Questions

Every AI deployment must answer these before production:

1. **What tier is this?**
2. **What controls does it need?**
3. **Fail-open or fail-closed?**
4. **What's the fallback path?**
5. **Has it been tested?**
6. **Is this multi-agent?** If yes → apply [MASO controls](maso/) on top of the foundation.
7. **What happens when context fills up?** Token exhaustion degrades guardrails, increases hallucinations, and weakens instruction-following, and it degrades the Judge monitoring it at the same time. Define context rotation strategy, alerting thresholds (70/85/95%), and fail-closed behavior. See [MASO OP-04](maso/controls/risk-register.md).

If you can answer all seven, you're ready. If you can't, you're not.

