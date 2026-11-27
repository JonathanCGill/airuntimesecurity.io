---
description: "A shared responsibility model for AI systems. Who owns each control when you build AI versus consume it from a vendor, framed across five actors: cloud provider, model provider, orchestrator, application provider, and AI customer."
---

# Shared Responsibility for AI Systems

The rest of this framework is written for **AI you develop and operate**: your own models, RAG pipelines, agents, and multi-agent systems. When you build the system, you own nearly every control in it.

Most organisations are not in that position for most of their AI. They **consume** AI from vendors: a copilot embedded in a SaaS product, a hosted model behind an API, an agentic feature in a platform they did not write. The controls still need to exist. The question is **who owns each one**, and the honest answer is that it is no longer all you.

This page gives you the vocabulary for that split. It is the missing axis that lets you read every other control page twice: once as the builder who owns the control, and once as the customer who has to verify someone else owns it.

## The five actors

A production AI system is rarely one party's work. Borrowing the structure of the [CSA AI Controls Matrix](../extensions/regulatory/csa-aicm-alignment.md) shared responsibility model, responsibility distributes across five actors stacked from infrastructure up to the consuming organisation.

| Actor | What they own | Example |
|-------|---------------|---------|
| **Cloud Service Provider** | The infrastructure the AI runs on: compute, storage, network, tenancy isolation, physical security. | AWS, Azure, GCP |
| **Model Provider** | The model itself: training data governance, model integrity, alignment, documented limitations, safety evaluations. | Anthropic, OpenAI, an internal model team |
| **Orchestrator** | The layer that connects models to tools, memory, and other agents: routing, tool exposure, context assembly, inter-agent messaging. | A LangGraph or Bedrock orchestration layer, an MCP host |
| **Application Provider** | The product the user interacts with: prompts, guardrails, the Judge, business logic, the action surface. | The team that ships the feature |
| **AI Customer** | The organisation deploying or consuming the system: use-case fitness, risk acceptance, data fed in, monitoring of outputs, accountability to its own regulators. | You |

In a fully **self-built** system, your organisation is the Model Provider (or a close partner of one), the Orchestrator, the Application Provider, and the AI Customer all at once. That is why the framework's default voice assumes you own everything: in that configuration, you do.

In a **consumed** system, the first four roles belong to vendors and you are left holding the AI Customer column. The control still has to be satisfied. Your job shifts from *implementing* it to *verifying* that the responsible party implements it, and *owning the residual* where they do not.

## The same control, owned differently

The point of the model is that a control does not disappear when you consume AI. It changes hands. Take three controls from elsewhere in this framework and trace who owns them in each configuration.

| Control | You build it | You consume it |
|---------|--------------|----------------|
| **Input guardrails** ([Three-Layer Model](controls.md)) | You implement and tune the guardrail. | The Application Provider implements it. You verify coverage and test it against your own injection cases. |
| **Model-as-Judge gate** ([Judge Assurance](judge-assurance.md)) | You build, calibrate, and adversarially test the Judge. | Often absent in vendor products. You either accept the residual risk, add your own outbound Judge at the integration boundary, or restrict the use case. |
| **Runtime identity and scope** ([IAM Governance](iam-governance.md)) | You issue agent identities and scope every tool call. | The Orchestrator and Application Provider scope the agent. You own the credentials and data the agent acts on, and the blast radius inside your tenant. |

The pattern is consistent. **What you build, you own. What you consume, you verify and bound.** The residual, the part no vendor will own, almost always lands back on the AI Customer: use-case fitness, the data you feed in, and accountability when the output is wrong.

## How to use this

1. **Place yourself in the stack** for each AI system. For each one, which of the five roles do you actually hold? Most portfolios are mixed: you build some systems and consume others.
2. **For controls you own, implement them.** The rest of the framework tells you how.
3. **For controls a vendor owns, verify them.** Turn the relevant control pages into questions. The [Vendor Assessment Questionnaire](../extensions/templates/vendor-assessment-questionnaire.md) and the CSA **AI-CAIQ** are built for exactly this.
4. **For the residual, accept it consciously.** Document what no party owns, decide whether the use case is still appropriate, and record the risk acceptance. This is the AI Customer's irreducible job.

This maps directly onto the framework's two-track design. The full control architecture is for systems you build. For systems you consume, the framework is the **mental model** that tells you which questions to ask and which residual risks are yours. See [Maturity Levels](../strategy/maturity-levels.md) for how the two tracks progress.

## What this is not

This is not a way to offload accountability. A vendor owning a control reduces your **implementation** burden, not your **accountability** to your own customers and regulators. If a consumed AI system harms your customer, "the vendor owned that control" is an explanation, not a defence. The AI Customer role exists precisely because someone has to own the outcome end to end, and that someone is you.

This page splits responsibility by vendor role. For the split inside your own organisation, between MASO and the functions around it, with a RACI for running agents, see [Scope and Responsibilities](scope-and-responsibilities.md).

!!! info "References"
    - [Scope and Responsibilities](scope-and-responsibilities.md)
    - [CSA AI Controls Matrix v1.1](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix-v1-1)
    - [CSA AICM Alignment](../extensions/regulatory/csa-aicm-alignment.md)
    - [Maturity Levels](../strategy/maturity-levels.md)
    - [Vendor Assessment Questionnaire](../extensions/templates/vendor-assessment-questionnaire.md)
