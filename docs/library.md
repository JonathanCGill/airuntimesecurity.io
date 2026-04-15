---
title: Library
description: "Index to the AI Runtime Security reference library: insights, implementation guidance, SDK, regulatory mappings, technical reference, templates, examples, and project history."
---

# Library

**Everything behind the framework.** Research articles, implementation guidance, platform patterns, reference code, regulatory mappings, templates, and examples. Use the cards below to find the right shelf.

## Reading and research

<div class="grid cards" markdown>

-   **[Insights](insights/README.md)**

    The *why* before the *how*. Forty-six research articles grouped into six themes: foundations, architecture, threats, agentic AI, models and technology, and evidence and analysis. Start with the Core Six if you are new to the thesis.

-   **[News](news.md)**

    Curated AI runtime security news linked to the framework's controls and domains. Useful for tracking where the threat landscape is moving and which controls new incidents validate.

</div>

## Implementation guidance

<div class="grid cards" markdown>

-   **[Infrastructure](infrastructure/README.md)**

    Eighty infrastructure controls across seven domains (identity, logging, network, data, secrets, supply chain, incident response) plus agentic extensions (sandboxing, delegation, tool access). Includes standards mappings to ISO 42001, NIST, OWASP, and platform patterns for AWS, Azure, and Databricks.

-   **[Strategy](strategy/README.md)**

    The guided path from "we have a business problem" to "we have a governed AI system in production". Twelve articles covering business alignment, use-case filtering, data reality, human factors, progression, framework tensions, maturity levels, and the return loop that keeps systems honest after launch.

-   **[SDK](sdk/README.md)**

    Python reference implementation. Guardrails, Judge evaluation, circuit breakers, PACE resilience, pipeline, agent security, telemetry, FastAPI integration, examples, and what the tests prove. The framework, in runnable code.

</div>

## Reference

<div class="grid cards" markdown>

-   **[Regulatory](extensions/regulatory/README.md)**

    Standards alignment: EU AI Act crosswalk and risk tiering, ISO 42001 alignment and clause mapping, ISO 27001 alignment, NIST IR 8596, ETSI SAI, AI governance operating model, and high-risk financial services guidance.

-   **[Technical Reference](extensions/technical/README.md)**

    Deep dives grouped by purpose: judge internals (model selection, distillation, precedents), detection and SOC (integration, content packs, anomaly detection, graph monitoring), control catalogues (agentic, endpoint hardening, RAG security), and economics and identity (cost and latency, economic governance, NHI lifecycle).

-   **[Templates](extensions/templates/README.md)**

    Ready-to-use artefacts: AI incident playbook, threat model template, judge prompt examples, data retention guidance, testing guidance, vendor assessment questionnaire, model card template.

-   **[Examples](extensions/examples/README.md)**

    Worked examples of the framework applied end-to-end: customer service AI, internal doc assistant, credit decision support, high-volume customer communications, fraud analytics, and a multi-agent risk demo.

-   **[Downloads](downloads.md)**

    Downloadable resources including position papers and practitioner training materials.

</div>

## Project

<div class="grid cards" markdown>

-   **[Changes & Evidence](CHANGELOG.md)**

    Changelog, maturity and validation, incidents the framework has been validated against, implementation guide, and the full references list.

-   **[About](what-is-ai-runtime-security.md)**

    About the discipline (what AI Runtime Security covers, and what it does not) and about the author.

</div>

!!! tip "Looking for the framework itself?"
    The framework lives under [Framework](ARCHITECTURE.md) in the top nav, split into [Core Controls](core/README.md) for single-agent deployments and [MASO](maso/README.md) for multi-agent orchestration. This library sits alongside it as supporting material.

!!! info "References"
    - [Home](README.md)
    - [Start](start.md)
    - [For Your Role](stakeholders/README.md)
    - [Framework: Architecture Overview](ARCHITECTURE.md)
