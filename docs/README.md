---
title: AI Runtime Security (AIRS)
description: "AI Runtime Security (AIRS) is a risk-proportionate framework for reducing harm caused by organisations' use of AI. It provides risk-oriented paths and control patterns that AI product owners can quickly adopt, adapt, or consciously deselect based on their own risk appetite and organisational context."
template: home.html
hide:
  - toc
  - path
  - feedback
comments: false
---

# AI Runtime Security (AIRS)

<div class="home-subtitle" markdown>

**Your AI passed every test. It still hallucinated in production.**

Runtime is where AI risk lives. AIRS gives you the controls to catch it.

</div>

<div class="home-tldr" markdown>

**You deployed a model. It works. Now what?**

Most organisations have no controls between the model and the damage it can do. AIRS fixes that with three layers of runtime defence, guardrails that enforce hard limits, a judge model that catches what guardrails miss, and human oversight for high-stakes calls, plus a circuit-breaker fallback that shuts things down when every layer fails.

Pick the layers you need. Skip the ones you do not. Match controls to your actual risk, not a compliance checklist.

</div>

## The AIRS Philosophy

![AIRS Runtime Control Plane](images/airs-runtime-control-plane.svg){ .arch-diagram }

<div class="pull-quote" markdown>

> **"AI moves faster than any human. Runtime controls keep you in charge."**

</div>

## The Framework

[AI Runtime Security](what-is-ai-runtime-security.md) helps organisations protect themselves from the risks AI systems create during live operation. It applies defence-in-depth at the point of execution, treating deployment as the beginning of the risk lifecycle rather than the end.

!!! abstract "Vendor-neutral by design"
    This framework does not advocate any specific vendor, product, or platform. It helps you structure a response to AI runtime risks. Tooling decisions are yours.

**Controls should be proportionate to risk.** A summarisation tool for internal meeting notes does not need the same controls as a customer-facing agent handling regulated financial data. The framework gives you risk-oriented paths so you can apply the right level of control to each situation.

Rather than imposing a single way of working, the framework provides a menu of controls that AI product owners can quickly navigate, apply, or consciously deselect. The goal is to make it easy to do the right thing for your context.

**[What is AI Runtime Security? →](what-is-ai-runtime-security.md)**

### The concept in action

A customer uses a chatbot to update personal information. Low-risk changes route directly to an execution agent. High-risk changes are evaluated by a judge model and escalated to a human analyst for approval. Only approved actions reach the customer database.

![Chatbot personal data update with runtime controls](images/chatbot-workflow-runtime-controls.svg){ .arch-diagram }

## Why This Matters

### The problem

Enterprises are deploying large language models into production at pace. The security conversation focuses almost entirely on the model layer: training data, prompt injection, pre-deployment red-teaming.

This misses the point. The risk that matters in a regulated enterprise is what the model *does* do, at runtime, in production, when interacting with real data, real users, and real business processes. A model that passed every benchmark can still hallucinate a regulatory disclosure, leak PII through a poorly scoped tool call, or take an action no human authorised.

Most enterprises have no runtime behavioural controls. They deploy. They monitor logs. They hope.

### Why existing approaches fall short

Adding process (review boards, sign-off stages, documentation requirements) creates gates that slow delivery without meaningfully reducing harm. Teams treat compliance as paperwork and controls become performative rather than protective.

On the technical side, prompt engineering is fragile, input and output filters miss novel failures, and model evaluations are point-in-time snapshots of controlled environments. Guardrails on their own are a single point of failure.

In every other security domain we layer controls and assume any single control will fail. AI security has not caught up.

### The AIRS approach

Four core control patterns, each independent, each compensating for the others:

**Guardrails** enforce hard boundaries: content policies, scope constraints, tool-use permissions. Fast, deterministic, and limited to catching obvious failures.

**Model-as-Judge evaluation** uses a separate model to assess outputs against policy, context, and intent before they reach users or downstream systems. It catches the subtle failures that guardrails miss.

**Human oversight** provides escalation paths, audit trails, and intervention capability for high-risk decisions and anomaly-triggered review.

**Circuit breakers** halt AI operations and activate safe fallbacks when controls fail or confirmed compromise is detected.

Each layer operates independently. No single failure compromises the system. Defence-in-depth is not new. Applying it systematically to AI runtime behaviour is.

### Why it matters for regulated industries

Banking supervisors, data protection authorities, and AI regulators are converging on the same expectation: demonstrate that your AI systems behave within defined boundaries, and that you can detect and respond when they do not.

The AIRS Framework maps to EU AI Act requirements, NIST AI RMF, ISO 42001, and sector-specific banking regulations. Effective controls generate compliance evidence as a by-product of normal operation.

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

<div class="learning-callout" markdown>

<span class="learning-callout__label">Related</span>

<p class="learning-callout__title">Interested in Secure by Design for AI?</p>

<p class="learning-callout__desc">Secure by Design shifts security left, embedding it into AI systems from the start rather than bolting it on after deployment. Learn how design-time decisions and runtime controls work together to reduce risk across the full AI lifecycle.</p>

[Explore AI Secured by Design](https://aisecuredbydesign.io/){ .md-button }

</div>

---

<p style="text-align: center; font-size: 0.85rem; color: var(--md-default-fg-color--light);">
Created by <a href="https://www.linkedin.com/in/jonathancgill/">Jonathan Gill</a>
</p>
