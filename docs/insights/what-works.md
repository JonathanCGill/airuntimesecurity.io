---
description: "Where AI security controls are measurably reducing harm: evidence from breach data, industry surveys, and operational deployments that defence-in-depth works."
---

# What's Working: Where Controls Are Reducing Harm

<!-- golden-thread-nav -->
!!! tip "Part of the Golden Thread (14 of 14)"
    Previous: [Architecture Overview](../ARCHITECTURE.md) · [See the full sequence](../reading-paths.md#the-golden-thread-guardrails-judges-and-why-they-work-together)
<!-- golden-thread-nav -->

> *"People often call me an optimist, because I show them the enormous progress they didn't know about. That makes me angry. I'm not an optimist. That makes me sound naive. I'm a very serious 'possibilist'."*
> - Hans Rosling

A framework focused exclusively on failure modes trains readers to expect failure. This document provides calibration: where runtime behavioral monitoring and proportionate controls are measurably reducing AI risk.

## Defensive AI Is Delivering Measurable Results

The IBM 2025 Cost of a Data Breach Report provides the clearest evidence that AI security controls work when deployed:

- Organizations using **extensive AI and automation in security** detect breaches **108 days faster** than those without - reducing the average breach lifecycle to roughly 133 days versus 241.
- This speed translates to **$1.9 million lower breach costs per incident** ($2.54M vs $4.44M average).
- **74% of organizations** deploying security AI report positive first-year ROI. Among early adopters, this rises to **88%**.
- Per-record breach costs drop from **$234 to $128** - a 45% reduction - when AI-powered detection is in place.

These numbers are not specific to AI *system* security. They measure AI used for *defensive* security across all breach types. But the principle transfers directly: runtime monitoring catches what design-time testing misses.

## The Pattern in Practice

The three-layer pattern this framework describes (guardrails → judge → human oversight) is not theoretical. It is deployed in production across the industry:

### Guardrails Catching Known-Bad

- **Microsoft blocks 1.6 million bot signup attempts per hour** using AI-powered fraud detection at the input layer.
- **Lakera Guard** processes millions of adversarial attempts across production deployments, detecting prompt injection patterns in real-time across enterprise applications.
- AWS Bedrock Guardrails, Azure AI Content Safety, and NVIDIA NeMo Guardrails provide managed, configurable input/output filtering that enterprises can deploy without building from scratch.

These are guardrails doing what guardrails do: blocking known patterns at speed. They are not perfect, but they are reducing the blast radius of the most common attacks.

### Model-as-Judge Detecting Unknown-Bad

- **Galileo's eval-to-guardrail lifecycle** demonstrates the feedback loop: evaluation metrics from production identify new failure modes, which are then converted into guardrail rules.
- **Confident AI / DeepEval** provides async Model-as-Judge evaluation that catches hallucination, toxicity, and coherence failures that static rules miss.
- Red teaming tools (Promptfoo, Adversa AI's platform) are enabling continuous adversarial testing - not just pre-deployment, but as ongoing runtime verification.

### Human Oversight Preventing Harm

- The **Norwegian Supreme Court incident** (April 2025) - where fabricated AI-generated case citations were filed - was caught by human reviewers before it affected a ruling. The system failed; the human oversight layer worked.
- Multiple South African court filings with AI-generated non-existent case law were detected and flagged. The pattern is consistent: where human review exists in the pipeline for high-stakes outputs, hallucination-driven harm is caught.
- Organizations with formal incident response plans for AI-specific events contain breaches faster and at lower cost.

## What Proportionate Controls Look Like

Not every AI system needs every control. The evidence supports tiered implementation:

**Low-risk systems** (internal summarization, search, content drafting) - basic input validation and output filtering are sufficient to prevent the majority of observed failure modes. These systems need guardrails, not judges.

**Medium-risk systems** (customer-facing chatbots, document analysis, code generation) - guardrails plus async evaluation plus logging. The Anysphere/Cursor incident (April 2025), where an AI support bot invented a login policy that triggered subscription cancellations, would have been caught by a judge layer monitoring for policy hallucination.

**High-risk systems** (financial decisions, healthcare recommendations, legal analysis, autonomous agents) - full three-layer pattern with mandatory human oversight for consequential outputs. The evidence is clear that hallucination rates, while declining, are not yet low enough for unsupervised high-stakes operation.

## The Adoption Maturity Curve

These tools and patterns exist. Adoption is a different story.

Most enterprises are still at the earliest stages of AI security maturity. The IBM data shows that only 37% have policies to manage or detect shadow AI. Only 34% of those *with* governance policies audit for unsanctioned AI regularly.

This is not cause for despair. It is a **normal technology adoption pattern**. The tools are available. The evidence base is growing. The gap between what is possible and what is deployed is closing, albeit slowly.

The organizations avoiding major incidents are not the ones with the largest budgets. They are the ones with **visibility into what AI systems they actually have** and **basic controls on the ones that matter most**.

## The Honest Assessment

Controls reduce risk. They do not eliminate it.

- Guardrails with 95% effectiveness still fail 1 in 20 times. At enterprise scale (millions of interactions), this means thousands of failures.
- Model-as-Judge evaluation is itself a probabilistic system - it will have false negatives.
- Human oversight only works if the humans are trained, resourced, and empowered to override the system.

The framework's value is not in promising zero risk. It is in making the residual risk **visible, measurable, and manageable**. That is worth doing, and the data shows it works.

