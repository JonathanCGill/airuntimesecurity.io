---
title: AI Runtime Security (AIRS)
hide:
  - navigation
  - toc
---

# AI Runtime Security

**Your AI passed every test. It still hallucinated in production.**

Most organisations have no controls between the model and the damage it can do. AIRS gives you four layers of runtime defence -- guardrails, a judge model, human oversight, and circuit breakers -- so you can match controls to your actual risk, not a compliance checklist.

Vendor-neutral. Risk-proportionate. Built for regulated industries.

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

## The Problem

AI security focuses almost entirely on the model layer: training data, prompt injection, pre-deployment red-teaming. This misses the point. The risk that matters is what the model *does* at runtime, in production, with real data and real users. Guardrails alone are a single point of failure. Process gates slow delivery without reducing harm. In every other security domain we layer controls and assume any single one will fail. AI security has not caught up.

[Why AI security is a runtime problem](insights/why-ai-security-is-a-runtime-problem.md)

---

## Start Here

<div class="grid cards" markdown>

-   **New to AIRS?**

    Seven controls you can implement in an afternoon. Enough runtime safety to go live, enough observability to learn, enough structure to decide where to invest next.

    [Minimum Viable AIRS](minimum-viable-airs.md)

-   **Know Your Role?**

    Entry points for CISOs, architects, risk teams, CIOs, product owners, AI engineers, compliance, and insider threat teams. Each page tells you what matters for your role, why, and where to start.

    [Stakeholder views](stakeholders/index.md)

-   **Want the Full Framework?**

    Reading paths organised by depth and interest. Pick a track and follow it.

    [Start here](reading-paths.md)

</div>

---

## Multi-Agent Security (MASO)

When agents coordinate autonomously, every single-agent risk compounds. An injection in one agent propagates through inter-agent messages. Hallucinations become another agent's facts. Delegation creates transitive authority chains nobody authorised.

MASO adds ten control domains, three implementation tiers, and PACE resilience to handle what single-agent controls cannot: inter-agent communication integrity, non-human identity management, execution containment, and kill switch architecture.

[MASO Framework](maso/index.md) · [Interactive Demo](maso/demo.md)

---

## Framework at a Glance

| Layer | What It Covers | Entry Point |
|---|---|---|
| **Foundation** | Three-layer behavioural controls for single-agent deployments. 80 infrastructure controls across 11 domains. | [Architecture](ARCHITECTURE.md) |
| **MASO** | Ten control domains for multi-agent orchestration. PACE resilience. OWASP Agentic Top 10 coverage. | [MASO](maso/index.md) |
| **Implementation** | Platform patterns for AWS, Azure, Databricks. Tool access controls. Agentic infrastructure. | [Infrastructure](infrastructure/index.md) |
| **SDK** | Python reference implementation. Guardrails, judge evaluation, circuit breakers in code. | [SDK](sdk/index.md) |

---

## Insights

The *why* before the *how*. Each article identifies a specific problem that the controls then solve.

**Foundations:** [Why guardrails aren't enough](insights/why-guardrails-arent-enough.md) · [Infrastructure beats instructions](insights/infrastructure-beats-instructions.md) · [Humans remain accountable](insights/humans-remain-accountable.md)

**Emerging challenges:** [The MCP problem](insights/the-mcp-problem.md) · [The orchestrator problem](insights/the-orchestrator-problem.md) · [When agents talk to agents](insights/when-agents-talk-to-agents.md) · [The long-horizon problem](insights/the-long-horizon-problem.md)

**Analysis:** [What works](insights/what-works.md) · [What scales](insights/what-scales.md) · [State of reality](insights/state-of-reality.md) · [The constraint curve](insights/the-constraint-curve.md)

[All insights](insights/index.md)

---

## Regulatory Alignment

The framework maps to EU AI Act (Articles 9, 14, 15), NIST AI RMF, ISO 42001, OWASP LLM Top 10 (2025), OWASP Agentic Top 10 (2026), DORA, and APRA CPS 234. Effective controls generate compliance evidence as a by-product of normal operation.

[EU AI Act crosswalk](extensions/regulatory/eu-ai-act-crosswalk.md)

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
