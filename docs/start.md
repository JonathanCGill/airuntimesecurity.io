---
title: Where to Begin
description: "Triage page for new readers. Pick the entry point that matches your situation: shipping today, shipping this week, or learning the framework in full."
---

# Where to Begin

**Where you begin depends on what you are doing now.** Five entry points, one triage.

## Pick your situation

<div class="grid cards" markdown>

-   **I am shipping an LLM feature in days, not weeks**

    Seven controls, one checklist, one decision tree. Deliberately short, deliberately opinionated. Once these are in place, you have a Minimum Viable AIRS deployment: enough runtime safety to go live, enough observability to learn, enough structure to decide where to invest next.

    [AIRSLite](minimum-viable-airs.md)

-   **I am deploying low-risk AI and want to move fast**

    Pre-approved controls for low-risk deployments. If your system qualifies (internal, read-only, no regulated data, human in the loop), you deploy without a formal security assessment. If it does not, the Fast Lane tells you exactly which path to take instead.

    [Fast Lane](FAST-LANE.md)

-   **I need working code in thirty minutes**

    End-to-end: classify risk, deploy guardrails, configure a Judge model, set up human oversight. Opinionated setup, runnable examples, zero multi-quarter runway required.

    [Quick Start](QUICK_START.md)

-   **I want to understand the framework before I build**

    Curated reading paths through the full framework, organised by goal. The Golden Thread takes you from *why runtime security?* through each control layer to *how the system self-corrects* in about two hours. Other paths cover threat landscape, multi-agent security, and practical artefacts.

    [Start Here (Reading Paths)](reading-paths.md)

-   **I have a specific question about scope, cost, or standards**

    Honest answers to the questions practitioners actually ask: does this apply to vendor AI, what does a Judge cost, how does it map to ISO 42001, what is the minimum team size to operate this.

    [FAQ](FAQ.md)

</div>

## If you are still not sure

Walk through these in order. Each one answers a question the previous one raises, and you can stop at any point once you have what you need.

1. **[AIRSLite](minimum-viable-airs.md)** gives you the short list. If the seven controls are enough for your situation, you are done.
2. **[Quick Start](QUICK_START.md)** turns the short list into working code.
3. **[Reading Paths](reading-paths.md)** gives you the reasoning behind every control, so you can adapt them to your context rather than copying them blindly.
4. **[For Your Role](stakeholders/README.md)** tells you what any of this means for your specific responsibilities: security leader, product owner, AI engineer, risk manager, and six others.

!!! tip "Prefer a role-based path?"
    If you would rather triage by who you are than by what you are doing, jump straight to [For Your Role](stakeholders/README.md). Each page tells you what matters for your role, why, and where to start reading.

!!! info "References"
    - [What AI Runtime Security is](what-is-ai-runtime-security.md)
    - [Architecture Overview](ARCHITECTURE.md)
    - [Core Controls](core/README.md)
    - [MASO (Multi-Agent)](maso/README.md)
