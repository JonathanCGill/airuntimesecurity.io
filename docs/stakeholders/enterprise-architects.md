---
description: "AIRS framework guide for solution and platform architects, covering where controls go in the AI pipeline, latency impact, and failure mode design."
---

# Enterprise Architects

**Solution Architects, Platform Architects, Technical Leads - where controls go in your pipeline, what they cost, and how they fail.**

> *Part of [Stakeholder Views](README.md) · [AI Runtime Security](../)*

## The Problem You Have

You're designing AI systems or integrating AI into existing architectures. Your security and risk teams are asking for "guardrails" and "oversight," but nobody's told you:

- **Where in the pipeline** do controls go?
- **What's the latency and cost impact** of adding an evaluation layer?
- **How do controls degrade** when upstream services fail?
- **What's different** about securing a RAG pipeline vs. a fine-tuned model vs. a multi-agent system?
- **What can your existing infrastructure** (API gateway, IAM, DLP) already handle?

You don't need governance theory. You need an architecture reference.

## What This Framework Gives You

### Control placement in the request/response flow

Every AI request passes through a pipeline. Controls intercept at specific points:

![Pipeline Control Flow](../images/pipeline-control-flow.svg)

**Key architectural decisions:**
- Judge runs **asynchronously** for most tiers (doesn't block response). Runs **synchronously** for CRITICAL tier (blocks until evaluated)
- Guardrails add **~10ms** per layer. Judge adds **~500ms–5s** depending on model and prompt complexity
- Judge should use a **different model** from the task agent - same-model evaluation has correlated failure modes

### What your existing infrastructure already covers

Before adding AI-specific controls, map what you already have:

| Existing Infrastructure | AI Control Coverage | Gap |
|---|---|---|
| API gateway (rate limiting, auth) | Request throttling, identity verification | No content-aware filtering |
| WAF | Some injection patterns | Doesn't detect semantic injection or indirect prompt injection |
| DLP | PII in structured data | Misses PII in natural language, generated content |
| IAM | User identity, RBAC | No agent identity, no credential scoping per AI session |
| Logging / SIEM | Request/response metadata | No semantic evaluation, no decision chain audit |
| Content delivery | Response caching, edge logic | No output quality evaluation |

The framework fills the gaps, not replaces the stack. See [Infrastructure Controls](../infrastructure/) for the 80-control mapping.

### Architecture patterns by deployment type

| If You're Building... | Read | Key Architecture Decision |
|---|---|---|
| RAG pipeline | [RAG Security](../extensions/technical/rag-security.md) | Retrieval layer is your biggest attack surface - poisoned documents become instructions |
| Single agent with tools | [Agentic Controls](../core/agentic.md) | Tool access scoping, action classification (read/write/irreversible), confirmation gates |
| Multi-agent orchestration | [MASO Integration Guide](../maso/integration/integration-guide.md) | Message bus signing, per-agent NHI, cross-agent DLP, delegation depth limits |
| Streaming responses | [Streaming Controls](../core/streaming-controls.md) | You can't evaluate output that hasn't finished - buffer or accept partial validation |
| Multimodal (image/audio/video) | [Multimodal Controls](../core/multimodal-controls.md) | Text guardrails don't work on images - you need modality-specific evaluation |

### Cost and latency budgets

The Judge layer isn't free. Budget for it:

| Configuration | Added Latency | Added Cost (per 1K txn) | When to Use |
|---|---|---|---|
| Guardrails only | ~10-20ms | ~$0.01-0.05 | LOW tier |
| Guardrails + Judge (sampled 10%) | ~10-20ms p50, ~2s p90 (sampled) | ~$0.50-2.00 | MEDIUM tier |
| Guardrails + Judge (full, async) | ~10-20ms (non-blocking) | ~$5-20 | HIGH tier |
| Guardrails + Judge (full, sync) | ~1-5s added | ~$5-20 | CRITICAL tier |

Full analysis: [Cost & Latency](../extensions/technical/cost-and-latency.md)

### PACE fail postures - what you wire into your architecture

Each control layer needs a defined failure mode. These aren't operational procedures - they're **architecture decisions** you make at design time:

| Layer Failure | Architectural Response |
|---|---|
| Guardrail service down | Route through bypass with full logging → trigger Judge on 100% of traffic |
| Judge service down | Continue with guardrails only → flag all responses for human review queue |
| Judge + Guardrails down | Circuit breaker activates → serve static fallback / disable AI path |
| Human review queue overflows | Auto-hold new requests → expand queue capacity → degrade to narrower scope |

Wire these as **health checks and circuit breakers** in your service mesh or orchestration layer. Not as runbooks. See [PACE Resilience](../PACE-RESILIENCE.md).

## Your Starting Path

| # | Document | Why You Need It |
|---|---|---|
| 1 | [Controls](../core/controls.md) | Three-layer pattern with implementation detail - the core architectural reference |
| 2 | [Risk Tiers](../core/risk-tiers.md) | Determines your control requirements - different tiers, different architectures |
| 3 | [Infrastructure Controls](../infrastructure/) | 80 controls across 11 domains - what to enforce at infrastructure level |
| 4 | [Cost & Latency](../extensions/technical/cost-and-latency.md) | Budget the evaluation layer - latency vs. coverage trade-offs |
| 5 | [PACE Resilience](../PACE-RESILIENCE.md) | Fail postures as architecture decisions |

**If you're building with a specific platform:** [AWS Bedrock](../infrastructure/reference/platform-patterns/aws-bedrock.md) · [Microsoft Foundry](../infrastructure/reference/platform-patterns/microsoft-foundry.md) · [Databricks](../infrastructure/reference/platform-patterns/databricks.md)

**If you're building multi-agent:** [MASO Integration Guide](../maso/integration/integration-guide.md) - LangGraph, AutoGen, CrewAI, AWS Bedrock patterns.

**If you want to see one transaction end-to-end:** [Runtime Telemetry Reference](../extensions/technical/runtime-telemetry-reference.md) - every JSON event, every threshold, every evidence artefact for a single request through the full control stack.

## What You Can Do Monday Morning

1. **Map your existing infrastructure** against the [Infrastructure Controls](../infrastructure/) to identify what you already cover and where the AI-specific gaps are.

2. **Add the Judge layer to your architecture.** Pick one HIGH or CRITICAL tier system. Add an independent LLM evaluation step - even async, even sampled. The [Model-as-Judge Implementation](../extensions/technical/model-as-judge-implementation.md) guide has the implementation patterns.

3. **Wire PACE health checks.** Add circuit breakers for your guardrail and Judge services. Define what the system does when each is unavailable. Test the failover path.

4. **Scope your agent's permissions.** If you have an agentic system, classify every tool by action type (read / write / irreversible) and add confirmation gates for write and irreversible actions. See [Agentic Controls](../core/agentic.md).

5. **Budget the evaluation layer.** Use the [Cost & Latency](../extensions/technical/cost-and-latency.md) analysis to present the cost of the Judge layer vs. the cost of the incidents it prevents. The [Risk Assessment](../core/risk-assessment.md) gives you the incident frequency numbers.

## Common Objections - With Answers

**"Adding a Judge layer doubles our latency."**
Only if you run it synchronously. For HIGH tier, run it async - the guardrails provide real-time protection while the Judge evaluates in the background. Only CRITICAL tier needs synchronous Judge evaluation. Budget ~10ms for guardrails, not seconds.

**"We're using [vendor]'s built-in guardrails. That's enough."**
Vendor guardrails are your first layer. The framework's three-layer pattern adds an independent evaluation layer (different model, different detection approach) and human oversight. Single-layer controls have a ~10% miss rate. Three layers compound to ~0.01%. [Why Guardrails Aren't Enough](../insights/why-guardrails-arent-enough.md).

**"Our RAG pipeline grounds the model - it won't hallucinate."**
RAG reduces but doesn't eliminate hallucination. More importantly, RAG creates a new attack surface: poisoned documents in your retrieval corpus become instructions to the model. [RAG Is Your Biggest Attack Surface](../insights/rag-is-your-biggest-attack-surface.md).

**"The infrastructure team handles security, not us."**
Infrastructure handles network, identity, and data-at-rest. Nobody handles the AI-specific controls (semantic evaluation, injection detection, decision chain audit, agent credential scoping) unless you design them into the pipeline. That's your job.

