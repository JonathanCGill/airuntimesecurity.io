---
title: AI Runtime Security (AIRS)
description: "AI Runtime Security (AIRS) is a risk-proportionate framework for monitoring, controlling, and constraining AI system behaviour in production environments. It focuses on guardrails rather than gates, enabling organisations to consciously select controls based on risk appetite."
template: home.html
hide:
  - toc
  - path
  - feedback
comments: false
---

# AI Runtime Security (AIRS)

<div class="home-subtitle" markdown>

**A risk-proportionate framework for controlling AI behaviour in production.**

Protect your organisation from AI security risks without slowing it down. AIRS provides guardrails, not gates. It helps you select the right controls for your actual risk, not bury you in documentation.

</div>

<div class="pull-quote" markdown>

> **"Reduce harm. Not paperwork."**

</div>

## The Framework

[AI Runtime Security](what-is-ai-runtime-security.md) is the practice of monitoring, constraining, and governing AI system behaviour in production environments. It applies defence-in-depth principles at the point of execution, treating deployment as the beginning of the risk lifecycle rather than the end of it.

This is not a vendor product or a proprietary methodology. It is a field of practice, comparable to how disciplines like Zero Trust, DevSecOps, and Security Chaos Engineering emerged to address gaps that existing security models did not cover.

The framework is built around a core principle: **controls should be proportionate to risk**. Not every AI use case carries the same risk. A summarisation tool for internal meeting notes does not need the same controls as a customer-facing advisory agent handling regulated financial data. AIRS gives you risk-oriented paths so you can apply the right level of control to each situation.

**[What is AI Runtime Security? →](what-is-ai-runtime-security.md)**

## Why This Matters

### The problem

Enterprises are deploying large language models into production at pace. Customer-facing, decision-supporting, data-processing. The security conversation is almost entirely focused on the model layer: training data provenance, prompt injection, red-teaming before deployment.

This misses the point. The risk that actually matters in a regulated enterprise is not what the model can do. It is what the model does do, at runtime, in production, when it is interacting with real data, real users, and real business processes. A model that passed every benchmark can still hallucinate a regulatory disclosure, leak PII through a poorly scoped tool call, or take an action in a multi-agent chain that no human authorised.

Most enterprises have no runtime behavioural controls. They deploy. They monitor logs. They hope.

### Why existing approaches fall short

The typical response to AI risk is to add process. More review boards. More sign-off stages. More documentation requirements. This creates gates that slow delivery without meaningfully reducing harm. Teams learn to treat compliance as a paperwork exercise and the controls become performative rather than protective.

On the technical side, prompt engineering is fragile. Input and output filters catch known patterns but miss novel failures. Model evaluations are point-in-time. They tell you how the model behaved in a controlled test environment, not how it behaves in production when exposed to real users, real data, and unpredictable workflows. Guardrails on their own are a single point of failure.

In every other domain of enterprise security (network, identity, data) we layer controls. We assume any single control will fail and we design accordingly. AI security has not caught up.

### The AIRS approach

AI Runtime Security applies defence-in-depth at the point of execution. It provides a menu of controls that you select based on the risk profile of each use case. Not everything needs every control. The framework gives AI product owners and business owners the ability to consciously deselect controls based on their risk appetite, rather than imposing a one-size-fits-all mandate.

Four core controls, each independent, each compensating for the others:

**Guardrails** enforce hard boundaries. Content policies, scope constraints, tool-use permissions. They are fast, deterministic, and limited. They catch the obvious failures.

**LLM-as-Judge evaluation** uses a separate model to assess the primary model's outputs against policy, context, and intent before those outputs reach users or downstream systems. It catches the subtle failures. The response that is technically within policy but contextually inappropriate. The tool call that is technically permitted but operationally dangerous.

**Human oversight** provides escalation paths, audit trails, and intervention capability. This is not human-in-the-loop for every transaction. That does not scale. It is structured checkpoints for high-risk decisions and anomaly-triggered review.

**Circuit breakers** halt AI operations and activate safe fallbacks when controls themselves fail or when confirmed compromise is detected.

Each layer operates independently. If guardrails miss something, the judge catches it. If the judge misjudges, human oversight provides the backstop. No single failure compromises the system.

The principle is not new. Defence-in-depth has always been how we secure complex systems. What is new is applying it systematically to AI runtime behaviour. What is also new is making the control selection explicit and risk-proportionate, so that teams can move fast where the risk is low and apply rigour where it genuinely matters.

### Why it matters for regulated industries

Banking supervisors, data protection authorities, and AI regulators are all converging on the same expectation: you must be able to demonstrate that your AI systems behave within defined boundaries, and that you have controls to detect and respond when they do not.

The AIRS Framework maps directly to EU AI Act requirements for high-risk AI systems, NIST AI RMF functions, ISO 42001 controls, and sector-specific expectations from banking regulators. It is not a compliance checkbox. It is an operational architecture that produces the evidence compliance requires. The controls are the compliance. That is the point.

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

<div class="learning-callout" markdown>

<span class="learning-callout__label">Learning</span>

<p class="learning-callout__title">New to the MASO Framework?</p>

<p class="learning-callout__desc">AIruntimesecurity.co.za is a dedicated learning site for the Multi-Agent Security Operations framework. Structured guides, walkthroughs, and practical examples to help you get started.</p>

[Explore AIruntimesecurity.co.za](https://airuntimesecurity.co.za){ .md-button }

</div>

---

<p style="text-align: center; font-size: 0.85rem; color: var(--md-default-fg-color--light);">
Created by <a href="https://www.linkedin.com/in/jonathancgill/">Jonathan C. Gill</a>
</p>
