# Module 1: Foundations

**What MASO is, why it exists, and the core mental model.**

## What MASO Stands For

**Multi-Agent Security Operations** — a framework for securing systems where multiple AI agents collaborate, delegate tasks, and act autonomously.

MASO is not a product, a vendor solution, or a prescriptive mandate. It is a framework that defines *what* needs to be true and *why*, leaving implementation approaches flexible.

## The Problem MASO Solves

Single-agent AI systems — one model processing inputs and producing outputs — have a well-understood threat surface. Prompt injection, harmful outputs, data leakage. Serious, but bounded.

Multi-agent systems are different. When multiple agents collaborate, three things change fundamentally:

**1. Risks compound across agents.**
A hallucination from Agent A becomes a "fact" for Agent B. By Agent C, it has been cited, elaborated, and presented with high confidence. One bad output becomes a chain of confident misinformation.

**2. Delegation creates implicit authority.**
If Agent A delegates to Agent B, and Agent B has access to Tool X, then Agent A effectively has access to Tool X — even if nobody intended that. Permission boundaries blur through delegation chains.

**3. Failures look like success.**
When multiple agents agree on the same wrong answer, human reviewers see consensus and have no reason to challenge it. Multi-agent agreement is not the same as multi-agent correctness.

These are not theoretical risks. They are observed failure modes in deployed systems. MASO exists because the security model for single-agent systems does not address them.

## The Core Mental Model

MASO is built on three foundational ideas:

### 1. Three Independent Defence Layers

Every interaction passes through up to three security layers, each operating on a different mechanism so that a single failure cannot cascade through all of them:

| Layer | What It Does | Speed | Mechanism |
|-------|-------------|-------|-----------|
| **Guardrails** | Block known-bad patterns | ~10ms | Deterministic rules |
| **LLM-as-Judge** | Assess unknown-bad behavior | ~500ms–5s | Independent model evaluation |
| **Human Oversight** | Decide on genuinely ambiguous cases | As needed | Cognitive judgment |

Plus a **Circuit Breaker** at the infrastructure level that stops all AI traffic when controls fail.

The independence is the point. A prompt injection that bypasses guardrails will not automatically fool the Judge. A Judge model failure does not impair guardrails or human review.

> **"Guardrails prevent. Judge detects. Humans decide. Circuit breakers contain."**

### 2. PACE — Designed for Failure

Every system will eventually have a control fail. PACE (Primary, Alternate, Contingency, Emergency) defines what happens when it does:

- **Primary** — Everything working. Normal operations.
- **Alternate** — One component degraded. Scope tightened, extra approvals required.
- **Contingency** — Multiple components degraded. Human-in-the-loop for everything.
- **Emergency** — Confirmed compromise. All AI stopped. Non-AI fallback activated.

The critical principle: **every control must have a defined failure mode and fallback path before the system enters production.** PACE is a design requirement, not an afterthought.

### 3. Agents as Non-Human Identities

Each agent is a distinct actor with its own identity, permissions, and credentials. Not an extension of the orchestrator. Not a subroutine of the application. A separate entity that must authenticate, be authorized, and be independently monitored.

This means:
- No shared credentials between agents
- No inherited permissions from the orchestrator
- Short-lived, automatically rotated credentials
- Zero-trust authentication on all inter-agent communication

## What MASO Covers

MASO organizes **128 controls** across **seven domains**, maps to both OWASP threat taxonomies (LLM Top 10 and Agentic Top 10), and aligns with major regulatory frameworks (EU AI Act, NIST AI RMF, ISO 42001, DORA).

It provides three **implementation tiers** representing a progression from supervised to autonomous operations:

| Tier | Autonomy | Human Role | When to Use |
|------|----------|------------|-------------|
| **Tier 1 — Supervised** | Low | Approves all actions | Pilot deployments, initial production |
| **Tier 2 — Managed** | Medium | Approves high-consequence actions | Operational systems with oversight |
| **Tier 3 — Autonomous** | High | Handles exceptions | Mature, trusted systems |

Organizations start at Tier 1, build operational evidence, and graduate to higher tiers after demonstrating control effectiveness.

## What MASO Is Not

- **Not a replacement for application security.** MASO secures the AI agent layer. External DLP, API gateways, database access controls, SIEM, and secure coding practices all still apply.
- **Not a product.** It is a framework. You implement it with your tools, in your environment, using your orchestration platform.
- **Not prescriptive about technology.** It defines what needs to be true, not which vendor or library to use. Integration patterns exist for LangGraph, AutoGen, CrewAI, AWS Bedrock Agents, and others.
- **Not optional for production multi-agent systems.** If agents can act autonomously, delegate to each other, and affect real-world outcomes, the risks MASO addresses are present whether or not you have a framework for them.

## Key Insight

The single most important thing to understand about MASO:

> Multi-agent AI systems introduce failure modes that do not exist in single-agent systems. These include epistemic failures (agents reinforcing each other's mistakes), coordination failures (agents deadlocking or oscillating), and authority failures (delegation chains creating unintended privilege escalation). MASO exists to make these risks visible, measurable, and manageable.

---

**Next:** [Module 2: The Three-Layer Defence](02-three-layer-defence.md)
