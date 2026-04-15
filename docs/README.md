---
title: AI Runtime Security (AIRS)
hide:
  - navigation
  - toc
---

# AI Runtime Security

**Your AI passed every test. It still hallucinated in production.**

Most organisations have no controls between the model and the damage it can do. AIRS is a vendor-neutral, risk-proportionate framework for running AI safely in production: layered runtime controls you can match to your actual risk, not a compliance checklist.

New here? Start with [what AI Runtime Security is](what-is-ai-runtime-security.md).

---

## Three Questions. Three Doors.

<div class="grid cards" markdown>

-   **How do I run AI securely?**

    Ship your first LLM feature with the controls that matter most. Seven controls, one checklist, one decision tree for whether you need to go deeper.

    [Start](start.md) · [AIRSLite](minimum-viable-airs.md) · [Quick Start](QUICK_START.md)

-   **How do I secure AI while it is running?**

    The framework itself: four independent control layers for single-agent systems, ten control domains for multi-agent orchestration, PACE resilience for graceful degradation.

    [Core Controls](core/README.md) · [MASO](maso/README.md) · [Architecture](ARCHITECTURE.md)

-   **How do I get the most out of AI safely?**

    Role-specific entry points. Each page tells you what matters for your role, why, where to start reading, and what you can do on Monday morning.

    [For Your Role](stakeholders/README.md)

</div>

---

## Find Your Role

Nine role-specific entry points. Each one frames AI runtime security through the lens of a single job, with a starting path, Monday-morning actions, and answers to the pushback you will get.

<div class="grid cards" markdown>

-   **[Security Leaders](stakeholders/security-leaders.md)**

    *How do I secure AI when the threat model is unlike anything I've secured before?*

-   **[Risk & Governance](stakeholders/risk-and-governance.md)**

    *How do I quantify AI risk and prove to the board that controls are working?*

-   **[Compliance & Legal](stakeholders/compliance-and-legal.md)**

    *How do I demonstrate that AI deployments meet regulatory obligations, with evidence?*

-   **[Insider Threat Teams](stakeholders/insider-threat-teams.md)**

    *Your programme already solves the problem AI agents create. How do you extend it?*

-   **[Chief Information Officers](stakeholders/chief-information-officers.md)**

    *How do I govern AI across my technology portfolio when every product runs different agents?*

-   **[Enterprise Architects](stakeholders/enterprise-architects.md)**

    *Where do controls go in my pipeline, what do they cost, and how do they fail?*

-   **[AI Engineers](stakeholders/ai-engineers.md)**

    *What do I actually build? Give me implementation patterns, not governance theory.*

-   **[Business Owners](stakeholders/business-owners.md)**

    *How do I manage AI risk across my product lines when agents are operational?*

-   **[Product Owners](stakeholders/product-owners.md)**

    *What controls are required to ship AI, and what do they cost in time and money?*

</div>

[All nine roles, grouped and explained](stakeholders/README.md)

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

A runtime control plane for AI behaviour. Each layer operates independently, and each can run in **detect-only** mode before you graduate it to **enforcing**. No single failure compromises the system.

<div class="control-layers" markdown>
<div class="grid cards" markdown>

-   **Guardrails**

    Fast, deterministic boundaries: content policies, scope constraints, tool-use permissions. Catches the obvious failures at machine speed. *~10ms per check.*

-   **Model-as-Judge**

    A separate model evaluates outputs against policy, context, and intent before they reach users. Catches the subtle failures guardrails miss. *~500ms to 5s, sync or async by risk tier.*

-   **Human Oversight**

    Escalation paths, audit trails, and intervention capability for high-stakes decisions. Scope scales with consequence.

-   **Circuit Breakers**

    Emergency failsafes that halt AI operations and activate safe fallbacks when controls fail or compromise is confirmed.

</div>
</div>

[How the layers work together](what-is-ai-runtime-security.md) · [End-to-end walkthrough: the Chevrolet $1 chatbot](walkthrough-chevrolet-1-dollar.md) · [Cost & latency by tier](extensions/technical/cost-and-latency.md)

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
