---
title: AI Runtime Behaviour Security
description: A practical, open-source framework for securing AI systems at runtime - where prompt injection, model manipulation, and agent drift actually happen.
template: home.html
hide:
  - toc
  - path
  - feedback
comments: false
---

# AI Runtime Behaviour Security

<div class="home-subtitle" markdown>

**The risk is not what the model can do. It is what the model does do, at runtime, in production.**

</div>

## Why This Matters

### The problem

Enterprises are deploying large language models into production at pace. Customer-facing, decision-supporting, data-processing. The security conversation is almost entirely focused on the model layer: training data provenance, prompt injection, red-teaming before deployment.

This misses the point. The risk that actually matters in a regulated enterprise is not what the model can do. It is what the model does do, at runtime, in production, when it is interacting with real data, real users, and real business processes. A model that passed every benchmark can still hallucinate a regulatory disclosure, leak PII through a poorly scoped tool call, or take an action in a multi-agent chain that no human authorised.

Most enterprises have no runtime behavioural controls. They deploy. They monitor logs. They hope.

### Why existing approaches fall short

Prompt engineering is fragile. Input and output filters catch known patterns but miss novel failures. Model evaluations are point-in-time. They tell you how the model behaved in a controlled test environment, not how it behaves in production when exposed to real users, real data, and unpredictable workflows. Guardrails on their own are a single point of failure.

In every other domain of enterprise security (network, identity, data) we layer controls. We assume any single control will fail and we design accordingly. AI security has not caught up. The industry is still treating deployment as the finish line when it is actually where the risk begins.

### The approach

AI Runtime Behaviour Security applies defence-in-depth at the point of execution. Three layers, each independent, each compensating for the others.

**Guardrails** enforce hard boundaries. Content policies, scope constraints, tool-use permissions. They are fast, deterministic, and limited. They catch the obvious failures.

**LLM-as-Judge evaluation** uses a separate model to assess the primary model's outputs against policy, context, and intent before those outputs reach users or downstream systems. It catches the subtle failures. The response that is technically within policy but contextually inappropriate. The tool call that is technically permitted but operationally dangerous.

**Human oversight** provides escalation paths, audit trails, and intervention capability. This is not human-in-the-loop for every transaction. That does not scale. It is structured checkpoints for high-risk decisions and anomaly-triggered review.

Each layer operates independently. If guardrails miss something, the judge catches it. If the judge misjudges, human oversight provides the backstop. No single failure compromises the system. The principle is not new. Defence-in-depth has always been how we secure complex systems. What is new is applying it systematically to AI runtime behaviour.

### Why it matters for regulated industries

Banking supervisors, data protection authorities, and AI regulators are all converging on the same expectation: you must be able to demonstrate that your AI systems behave within defined boundaries, and that you have controls to detect and respond when they do not.

This framework maps directly to EU AI Act requirements for high-risk AI systems, NIST AI RMF functions, ISO 42001 controls, and sector-specific expectations from banking regulators. It is not a compliance checkbox. It is an operational architecture that produces the evidence compliance requires. The controls are the compliance. That is the point.

### Where to go from here

<div class="home-paths" markdown>

<div class="home-path" markdown>

#### Stakeholder Views

What this framework means for CISOs, architects, risk teams, and operators.

[Stakeholder Views](stakeholders/){ .md-button }

</div>

<div class="home-path" markdown>

#### Architecture Overview

The technical control model and how it integrates with existing cloud and platform security.

[Architecture Overview](ARCHITECTURE.md){ .md-button }

</div>

<div class="home-path" markdown>

#### MASO Framework

Securing autonomous agent coordination in multi-agent systems.

[MASO Framework](maso/){ .md-button }

</div>

</div>
