---
description: "AIRS Framework architecture — layered runtime controls for single-agent and multi-agent AI systems."
---

# Architecture Overview

![Three-layer runtime security: Guardrails, LLM-as-Judge, Human Oversight](images/three-layer-simple.svg){ .arch-diagram }

The industry is converging on the same answer independently. NVIDIA NeMo, AWS Bedrock, Azure AI, LangChain, Guardrails AI - all implement variants of the same pattern:

| Layer | What It Does | Speed |
| --- | --- | --- |
| **Guardrails** | Block known-bad inputs and outputs - PII, injection patterns, policy violations | Real-time (~10ms) |
| **LLM-as-Judge** | Detect unknown-bad - an independent model evaluating whether responses are appropriate | Async (~500ms–5s) |
| **Human Oversight** | Decide genuinely ambiguous cases that automated layers can't resolve | As needed |
| **Circuit Breaker** | Stop all AI traffic and activate a safe fallback when controls themselves fail | Immediate |

**Guardrails prevent. Judge detects. Humans decide. Circuit breakers contain.**

Each layer catches what the others miss. Remove any layer and you have a gap. Together they form a **closed-loop control system**: containment boundaries define the desired state, the Judge continuously measures actual behavior, drift detection computes the error, and human oversight applies corrective action. Unlike open-loop approaches that evaluate once and deploy, this architecture self-corrects continuously. See [Why Containment Beats Evaluation](insights/why-containment-beats-evaluation.md).

## Single-Agent Architecture

![Single-Agent Security Architecture](images/single-agent-architecture.svg)

For a single AI model - a chatbot, a document processor, an assistant - the three layers wrap the model's input and output. Each layer is specifically designed to catch what the previous layer misses (compound defence by design, not by coincidence):

- **Guardrails** (containment boundaries) run synchronously on every request. Deterministic pattern matching: content filters, PII detection, topic restrictions, rate limits. Permissions derive from **business intent** - what the use case requires - not from evaluation of the model's capabilities. This is a [constrain-regardless](insights/why-containment-beats-evaluation.md) architecture: action-space constraints that leave the model's reasoning unconstrained. Fast and necessary, but insufficient alone - you cannot write a regex for every possible failure of a system that generates natural language.
- **LLM-as-Judge** runs asynchronously, evaluating whether the response is appropriate, safe, within scope, and consistent with purpose. Different model, different provider if possible - **enterprise-owned and configured**, not vendor-side safeguards. If the primary model is compromised, the Judge must not be compromised with it. Catches within-bounds adversarial behavior that containment cannot address.
- **Human Oversight** scales with risk. Low-risk systems get spot checks. High-risk systems get human approval before execution. Only genuinely ambiguous cases reach human reviewers. Handles what neither containment nor the Judge can resolve autonomously.

Controls scale to risk tier - from minimal self-certification ([Fast Lane](FAST-LANE.md)) to full architecture with mandatory human approval.

**→ [Foundation Framework](foundations/)** - 80 controls, risk tiers, implementation checklists

## Multi-Agent Architecture

When multiple LLMs collaborate, delegate, and take autonomous actions, single-agent controls are necessary but not sufficient. New failure modes emerge:

- **Prompt injection propagates** across agent chains - one poisoned document becomes instructions for every downstream agent
- **Hallucinations compound** - Agent A hallucinates a claim, Agent B cites it as fact, Agent C elaborates with high confidence
- **Delegation creates transitive authority** - permissions transfer implicitly through delegation chains nobody designed
- **Failures look like success** - the most dangerous outputs are well-formatted, confident, unanimously agreed, and wrong

Multi-agent security requires per-agent identity, per-agent permissions, per-agent evaluation - plus controls for the interactions between them: message bus security, epistemic integrity, kill switch architecture.

**→ [MASO Framework](maso/)** - 128 controls across 7 domains, 3 implementation tiers, full OWASP dual coverage

## PACE Resilience

Every control has a defined failure mode. The [PACE methodology](PACE-RESILIENCE.md) ensures that when a layer degrades - and it will - the system transitions to a predetermined safe state rather than failing silently.

| State | What's happening |
| --- | --- |
| **Primary** | All layers operational. Normal production. |
| **Alternate** | One layer degraded. Backup active. Scope tightened. |
| **Contingency** | Multiple layers degraded. Supervised-only mode. Human approves every action. |
| **Emergency** | Confirmed compromise. Circuit breaker fired. AI stopped. Non-AI fallback active. |

Even at the lowest risk tier, there's a fallback plan. At the highest, there's a structured degradation path from full autonomy to full stop.

