---
title: Control Domains
description: "The eleven MASO control domains: identity and access, data protection, execution control, observability, supply chain, epistemic integrity, privileged agents, and more, each scaled by tier."
search:
  boost: 2
---

# Control Domains

Eleven domains cover what agents do to data, to tools, to each other, and to the truth. Each domain scales by tier: the more autonomy an agent has, the more of the domain applies. Everything here inherits from [Objective Intent](objective-intent.md), so read that first.

<div class="grid cards" markdown>

-   **Prompt, Goal & Epistemic Integrity**

    ---

    Keeping instructions, goals, and "facts" trustworthy as they pass between agents.

    [:octicons-arrow-right-24: Open](prompt-goal-and-epistemic-integrity.md)

-   **Identity & Access**

    ---

    Per-agent identity and least-privilege permissions so authority cannot leak through hand-offs.

    [:octicons-arrow-right-24: Open](identity-and-access.md)

-   **Data Protection**

    ---

    What data each agent may read, write, or move, and how it is protected in transit between them.

    [:octicons-arrow-right-24: Open](data-protection.md)

-   **Document Extraction Integrity**

    ---

    Treating extracted document content as data to be checked, never as instructions to be obeyed.

    [:octicons-arrow-right-24: Open](extraction-integrity.md)

-   **Execution Control**

    ---

    Constraining what actions an agent can actually commit, and gating the irreversible ones.

    [:octicons-arrow-right-24: Open](execution-control.md)

-   **Observability**

    ---

    Seeing what the fleet did: the flight recorder for multi-agent behaviour.

    [:octicons-arrow-right-24: Open](observability.md)

-   **Expected vs Real Monitoring (Comoverlay)**

    ---

    Comparing what agents should be doing with what they are doing, reporting what the monitor cannot see, and keeping responses that can cause loss with people. Spans Observability and Execution Control.

    [:octicons-arrow-right-24: Open](comoverlay.md)

-   **Supply Chain**

    ---

    Trust in the models, tools, and packages the agents depend on.

    [:octicons-arrow-right-24: Open](supply-chain.md)

-   **Privileged Agent Governance**

    ---

    Extra scrutiny for the agents that hold the keys.

    [:octicons-arrow-right-24: Open](privileged-agent-governance.md)

-   **Model Cognition Assurance**

    ---

    Assurance that the models still reason the way you validated them to.

    [:octicons-arrow-right-24: Open](model-cognition-assurance.md)

-   **Agentic Task Mandate**

    ---

    The scope of work an agent is mandated to perform, and the boundary it must not cross.

    [:octicons-arrow-right-24: Open](agentic-task-mandate.md)

-   **Emergent Risk Register**

    ---

    The living record of risks that only appear once agents interact at scale.

    [:octicons-arrow-right-24: Open](risk-register.md)

</div>

---

*At single-agent scale these collapse into the [ASO Core Controls](../../core/reference.md): the same protections, one boundary.*
