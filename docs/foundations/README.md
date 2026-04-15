---
description: Runtime security controls for single-agent AI deployments. The architecture in one page, with pointers into the Core Controls library for depth.
---

# Single-Agent Overview

**Most AI governance guidance assumes you can test your way to safety. You cannot.**

AI systems are non-deterministic. Same prompt, same model, same parameters, different response. Every time. Your test suite proves the system *can* behave correctly. It cannot prove it *will* on the next request.

This page is a one-screen overview of the single-agent pattern. When you want the control reference, the checklist, the risk tiers, or the specialised controls, go to [Core Controls](../core/README.md).

## Architecture

![Single-Agent Security Architecture](../images/single-agent-architecture.svg){ .arch-diagram }

Three layers, one principle: you cannot fully test a non-deterministic system before deployment, so you continuously verify behaviour in production. This is a [closed-loop control system](../insights/why-containment-beats-evaluation.md), not evaluate-once-and-deploy.

**Guardrails** block known-bad inputs and outputs at machine speed (~10ms). Deterministic pattern matching: content filters, PII detection, topic restrictions, rate limits. These are **action-space constraints** that leave the model's reasoning unconstrained.

**Model-as-Judge** catches unknown-bad through independent model evaluation. A large LLM running asynchronously (500ms to 5s), or a [distilled SLM](../extensions/technical/distill-judge-slm.md) running inline (10ms to 50ms). Enterprise-owned and configured, evaluating outputs against policy, factual grounding, tone, and safety criteria.

**Human Oversight** provides the accountability backstop. Scope scales with risk: low-risk systems get spot checks, high-risk systems get human approval before commit. Humans decide edge cases, humans own outcomes.

**Circuit Breaker** stops all AI traffic and activates a non-AI fallback when any layer fails. Not a degradation, a full stop with a predetermined safe state.

Each layer is specifically designed to catch what the previous layer misses. This is compound defence by design, not defence-in-depth by coincidence. For the full argument, see [Why Containment Beats Evaluation](../insights/why-containment-beats-evaluation.md).

## Risk-Scaled Controls

Controls scale to risk so that low-risk AI moves fast and high-risk AI stays safe.

| Risk Tier | Controls Required | PACE Posture |
| --- | --- | --- |
| **Low** | Fast Lane: minimal guardrails, self-certification | P only (fail-open with logging) |
| **Medium** | Guardrails + Judge, periodic human review | P + A configured |
| **High** | All three layers, human-in-the-loop for writes | P + A + C configured and tested |
| **Critical** | Full architecture, mandatory human approval | Full PACE cycle with tested E→P recovery |

Classify your system: [Risk Tiers](../core/risk-tiers.md). Understand the failure modes: [PACE Resilience](../PACE-RESILIENCE.md).

## Defence in Depth Beyond the AI Layer

![Defence in Depth Beyond the AI Layer](../images/defence-in-depth-beyond-ai.svg){ .arch-diagram }

The three-layer model addresses controls specific to non-deterministic AI behaviour. It does not replace the security controls your organisation already has. It sits inside them.

Your existing DLP applies to data flowing into and out of AI systems. API gateways validate requests regardless of whether the caller is human or AI. Database access controls and parameterised queries prevent injection even if an agent constructs a malicious query. IAM governs who can invoke AI in the first place. SIEM correlates AI events with network, endpoint, and application events. Secure coding practices in the systems agents interact with matter arguably more, because the caller is now non-deterministic.

These controls are outside the scope of this reference, but they are part of your defence. When you threat-model, include them. When one of these catches something, it is your safety net.

For multi-agent systems, the [MASO Environment Containment](../maso/environment-containment.md) strategy formalises this principle: harden every system the agent connects to so that agent misbehaviour is structurally harmless regardless of the agent's intent.

## Where to Next

| If you want to... | Go here |
| --- | --- |
| Ship your first LLM feature | [AIRSLite](../minimum-viable-airs.md) |
| Deploy low-risk AI fast | [Fast Lane](../FAST-LANE.md) |
| Get working code in 30 minutes | [Quick Start](../QUICK_START.md) |
| See every single-agent control | [Core Controls](../core/README.md) |
| Classify a system by risk | [Risk Tiers](../core/risk-tiers.md) |
| Enforce controls at the infrastructure layer | [Infrastructure](../infrastructure/README.md) |
| Secure a multi-agent system | [MASO Framework](../maso/README.md) |

!!! info "References"
    - [Core Controls](../core/README.md)
    - [Architecture Overview](../ARCHITECTURE.md)
    - [Why Containment Beats Evaluation](../insights/why-containment-beats-evaluation.md)
    - [PACE Resilience](../PACE-RESILIENCE.md)
    - [MASO Framework](../maso/README.md)
