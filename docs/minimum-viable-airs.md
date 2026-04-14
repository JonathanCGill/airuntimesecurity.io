---
title: Minimum Viable AIRS
description: "The seven controls every team should put in place before shipping an LLM-powered feature to production. If you do nothing else, do these."
---

# Minimum Viable AIRS

*If you do nothing else, do these seven things before your first LLM feature goes live.*

## Who This Is For

You are shipping an LLM-powered feature into production for the first time. Maybe it is a chatbot, a summariser, a code assistant, a retrieval app, or something stitched together with a handful of tool calls. You do not have a dedicated AI security team. You do not have a multi-quarter runway to read a 200-page framework before you ship.

You need a short, practical list of things to put in place so that when the feature goes live, the obvious failure modes are already covered and you can see the less obvious ones coming.

This page is that list. It is deliberately opinionated and deliberately short. Seven controls, one checklist, one decision tree. Once you have these in place, you have a Minimum Viable AIRS deployment: enough runtime safety to go live, enough observability to learn, and enough structure to decide where to invest next.

!!! abstract "What this page is not"
    This is not the full framework. It is not a substitute for a proper risk assessment on high-stakes systems. If your feature handles regulated data, takes autonomous actions, or is customer-facing in a sensitive domain, treat this as the floor, not the ceiling. The [decision tree](#do-you-need-to-go-deeper) at the end tells you when to go further.

## The Seven Controls

Each control answers a specific failure mode. None of them requires exotic tooling. Most can be implemented in an afternoon.

### 1. Input guardrails

**What:** A filter on user input before it reaches the model. At minimum: basic prompt injection patterns, obvious attempts to override system instructions, and content that is clearly out of scope for your feature.

**Why:** Most production incidents start with an input the model was never meant to handle. Catching the obvious ones at the edge is cheap and eliminates a long tail of noise from your logs.

**Minimum viable:** Your LLM provider's built-in content filter, plus a short regex list for the patterns that matter to your use case. Do not try to build a perfect detector. Assume things will get through and let the next layers catch them.

### 2. Output guardrails

**What:** A filter on model output before it reaches the user or a downstream system. At minimum: PII detection if your users might paste sensitive data, secrets detection if your context includes any credentials, and length and format checks so the model cannot return something your application cannot handle.

**Why:** The model will occasionally echo input it should not, fabricate content it should not, or produce something that breaks the downstream contract. The output filter is the last line of defence before damage is visible.

**Minimum viable:** A small set of regex or library-based checks on the response, applied synchronously, with a safe default message when a check fails.

### 3. Structured logging

**What:** Every request and response recorded with: user identity, timestamp, model and version, input, output, latency, and the outcome of any guardrail check. Stored somewhere you can query.

**Why:** When something goes wrong, and it will, you need to reconstruct what happened. Without structured logs you are guessing. With them you can answer questions from regulators, users, and your own engineering team.

**Minimum viable:** JSON lines to your existing log platform, with a correlation ID per request. Retention set by whatever your organisation already does for application logs.

### 4. Rate limiting and cost caps

**What:** Per-user request limits, global request limits, and a hard daily or monthly spend cap on the model API. Alerts when any of them are approached.

**Why:** Runaway loops, scraping, and abuse all look the same on the first day: a cost spike. A cap turns a potential finance incident into a feature outage, which is easier to explain and easier to fix.

**Minimum viable:** A token bucket per user in your application layer, a daily spend limit configured in your provider console, and a single alert wired to somewhere a human will see it.

### 5. Kill switch

**What:** A feature flag, environment variable, or config entry that one person can flip to disable the AI feature within minutes, without a code deployment.

**Why:** When you discover a serious problem in production, the first question is "how do we stop the bleeding?" The kill switch is the answer. Without it, the answer is "wait for a deploy," which is rarely acceptable.

**Minimum viable:** A boolean flag checked on every request. When off, the feature returns the documented fallback response. Test that it works before you need it.

### 6. Human-reviewable path for high-stakes output

**What:** An explicit definition of which outputs are high-stakes for your feature, and a path for a human to review or approve those outputs before they have irreversible effects.

**Why:** The model will be wrong sometimes. For low-stakes outputs (a draft email, a summary) that is fine. For high-stakes outputs (an action taken against a customer account, an external communication, a code change merged into main) you want a human in the loop until you have enough evidence that the model is reliable in that specific context.

**Minimum viable:** For your first deployment, route anything you are unsure about to a human queue or leave the AI in an advisory role only. Autonomy is something you earn with evidence, not something you assume on day one.

### 7. Documented fallback

**What:** A one-paragraph description of what users, operators, and downstream systems do when the feature is disabled or failing. Written down somewhere your team can find it.

**Why:** Features get turned off. Providers have outages. Models get deprecated. If nobody can remember how the work got done before the AI arrived, the kill switch becomes a work-stoppage event, not a safety mechanism.

**Minimum viable:** One paragraph in your runbook. "When `ai_feature_enabled = false`, users see *[message]*. Operators follow *[manual process]*. Contact *[owner]* to restore."

## One-Page Checklist

Copy this into your team's tracker before you ship.

- [ ] **Input guardrails** in place: provider content filter plus use-case-specific patterns.
- [ ] **Output guardrails** in place: PII, secrets, and format checks, with a safe default on failure.
- [ ] **Structured logging** for every request and response, queryable, with correlation IDs.
- [ ] **Rate limits** per user and **spend cap** per day, with an alert on approach.
- [ ] **Kill switch** implemented, tested, and documented. One person can flip it in minutes.
- [ ] **High-stakes outputs** defined, with a human-review path or advisory-only mode.
- [ ] **Fallback documented** in one paragraph, visible to everyone who supports the feature.

If you cannot tick all seven, you are not ready to ship. The gaps are the work.

## Do You Need to Go Deeper?

The seven controls above are a floor. They are sufficient for an internal-facing, low-stakes, non-regulated feature with a human close to the output. They are not sufficient for everything.

Use this decision tree to decide where to invest next. Any *yes* answer means you should treat the Minimum Viable list as step one, not the finish line.

| Question | If yes |
|----------|--------|
| Does the feature face external customers or the general public? | Read [Why Guardrails Aren't Enough](insights/why-guardrails-arent-enough.md), then add a [Model-as-Judge](core/judge-assurance.md) layer for output evaluation. |
| Does the feature process regulated data (PII, financial, health, legal)? | Walk through the [Risk Tiers](core/risk-tiers.md) to classify the deployment, then map controls with the [Implementation Checklist](core/checklist.md). |
| Does the feature take actions against external systems without a human in the loop? | Read [Infrastructure Beats Instructions](insights/infrastructure-beats-instructions.md) and apply [Tool Access Controls](infrastructure/agentic/tool-access-controls.md). |
| Is there more than one agent, or does the feature delegate to other agents? | Start with the [MASO Framework](maso/) for multi-agent controls. |
| Do outputs influence decisions that are hard or impossible to reverse? | Build a [Human Oversight](stakeholders/security-leaders.md) path before you go live, not after. |
| Are you operating under the EU AI Act, ISO 42001, or sector-specific AI regulation? | Start with the relevant [regulatory crosswalk](extensions/regulatory/eu-ai-act-crosswalk.md) and align your controls to the obligations. |

If every answer is *no*, the seven controls are a reasonable ceiling for now. Revisit the questions every quarter, or whenever the feature's scope changes.

## Where to Next

Once the seven controls are in place and the feature is stable in production, the natural progressions are:

- **Add a judge layer** to catch the semantic failures your guardrails miss. See [The Judge Detects, Not Decides](insights/judge-detects-not-decides.md).
- **Tighten the feedback loop** between runtime signals and control updates. See [The Feedback Loops That Make It Work](insights/feedback-loops.md).
- **Formalise your resilience posture** beyond the kill switch. See [PACE Resilience](PACE-RESILIENCE.md).
- **Turn the controls into code** using the reference implementation. See the [AIRS Python SDK](sdk/README.md).

None of these are required to ship. All of them become relevant as your AI footprint grows.

!!! info "References"
    - [What is AI Runtime Security?](what-is-ai-runtime-security.md)
    - [Secure AI Fast Lane](FAST-LANE.md)
    - [Quick Start](QUICK_START.md)
    - [Implementation Checklist](core/checklist.md)
    - [Risk Tiers](core/risk-tiers.md)
