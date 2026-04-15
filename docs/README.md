---
title: AI Runtime Security (AIRS)
hide:
  - navigation
  - toc
---

# AI Runtime Security

**Your AI passed every test. It still hallucinated in production.**

Most organisations have no controls between the model and the damage it can do. AIRS is a vendor-neutral, risk-proportionate framework for running AI safely in production: layered runtime controls you can match to your actual risk, not a compliance checklist.

[:octicons-arrow-right-24: What AI Runtime Security is](what-is-ai-runtime-security.md)

---

## Three Questions. Three Doors.

<div class="grid cards" markdown>

-   **How do I run AI securely?**

    Ship your first LLM feature with the controls that matter most. Seven controls, one checklist, one decision tree for whether you need to go deeper.

    [Start Here](reading-paths.md) · [AIRSLite](minimum-viable-airs.md) · [Quick Start](QUICK_START.md)

-   **How do I secure AI while it is running?**

    The framework itself: four independent control layers for single-agent systems, ten control domains for multi-agent orchestration, PACE resilience for graceful degradation.

    [Core Controls](core/README.md) · [MASO](maso/README.md) · [Architecture](ARCHITECTURE.md)

-   **How do I get the most out of AI safely?**

    Role-specific entry points. Each page tells you what matters for your role, why, where to start reading, and what you can do on Monday morning.

    [For Your Role](stakeholders/README.md)

</div>

---

## Framework at a Glance

| Layer | What It Covers | Entry Point |
|---|---|---|
| **Foundation** | Three-layer behavioural controls for single-agent deployments. 80 infrastructure controls across 11 domains. | [Architecture](ARCHITECTURE.md) |
| **MASO** | Ten control domains for multi-agent orchestration. PACE resilience. OWASP Agentic Top 10 coverage. | [MASO](maso/README.md) |
| **Implementation** | Platform patterns for AWS, Azure, Databricks. Tool access controls. Agentic infrastructure. | [Infrastructure](infrastructure/README.md) |
| **SDK** | Python reference implementation. Guardrails, judge evaluation, circuit breakers in code. | [SDK](sdk/README.md) |

---

## Four Control Layers

Each layer operates independently. No single failure compromises the system.

<div class="grid cards" markdown>

-   **Guardrails**

    Fast, deterministic boundaries: content policies, scope constraints, tool-use permissions. Catches the obvious failures at machine speed.

-   **Model-as-Judge**

    A separate model evaluates outputs against policy, context, and intent before they reach users. Catches the subtle failures guardrails miss.

-   **Human Oversight**

    Escalation paths, audit trails, and intervention capability for high-stakes decisions. Scope scales with consequence.

-   **Circuit Breakers**

    Emergency failsafes that halt AI operations and activate safe fallbacks when controls fail or compromise is confirmed.

</div>

[:octicons-arrow-right-24: How the layers work together](what-is-ai-runtime-security.md)

---

## The Problem AIRS Solves

AI security focuses almost entirely on the model layer: training data, prompt injection, pre-deployment red-teaming. This misses the point. The risk that matters is what the model *does* at runtime, in production, with real data and real users. Guardrails alone are a single point of failure. Process gates slow delivery without reducing harm. In every other security domain we layer controls and assume any single one will fail. AI security has not caught up.

[Why AI security is a runtime problem](insights/why-ai-security-is-a-runtime-problem.md)

---

## Insights

The *why* before the *how*. Each article identifies a specific problem that the controls then solve.

[Why guardrails aren't enough](insights/why-guardrails-arent-enough.md) · [The MCP problem](insights/the-mcp-problem.md) · [The orchestrator problem](insights/the-orchestrator-problem.md) · [What works](insights/what-works.md) · [All insights](insights/README.md)

---

## Related

<div class="grid cards" markdown>

-   **AI Secured by Design**

    Shifts security left, embedding it into AI systems from the start rather than bolting it on after deployment.

    [aisecuredbydesign.io](https://aisecuredbydesign.io/)

-   **MASO Learning Site**

    Structured guides, walkthroughs, and practical examples for the Multi-Agent Security Operations framework.

    [airuntimesecurity.co.za](https://airuntimesecurity.co.za)

</div>

---

<div style="text-align: center; padding: 1rem 0;" markdown>

Created by [Jonathan Gill](https://www.linkedin.com/in/jonathancgill/) · [feedback@airuntimesecurity.io](mailto:feedback@airuntimesecurity.io)

</div>
