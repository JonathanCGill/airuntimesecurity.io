---
description: Runtime security controls for single-model AI deployments. Risk-proportionate, layered controls that you select or consciously deselect based on your risk appetite and organisational context.
---

# AI Runtime Security - Single-Agent Controls

> Most AI governance guidance assumes you can test your way to safety.
> You cannot.

AI systems are non-deterministic. Same prompt, same model, same parameters - different response. Every time. Your test suite proves the system *can* behave correctly. It cannot prove it *will* on the next request.

- **AI systems are non-deterministic** - same input, different output, by design
- **Guardrails fail silently** - the most dangerous outputs look perfectly normal
- **Multi-agent systems amplify errors** - hallucinations compound, permissions propagate, failures correlate

**Guardrails** → **Judge** → **Human Oversight** → **Circuit Breaker**

*Block known-bad → Detect unknown-bad → Decide edge cases → Fail safely*

**Start here:**

- [Read the Quick Start guide](../QUICK_START.md) - get working controls in 30 minutes
- [Explore the technical architecture](#architecture) - three layers, what fails when
- [Get working controls in 30 minutes](../QUICK_START.md) - from zero to deployed

## Architecture

![Single-Agent Security Architecture](../images/single-agent-architecture.svg)

Three layers, one principle: **you can't fully test a non-deterministic system before deployment, so you continuously verify behavior in production.** This is a [closed-loop control system](../insights/why-containment-beats-evaluation.md) - not evaluate-once-and-deploy, but constrain-and-continuously-verify.

**Layer 1 - Guardrails** (containment boundaries) block known-bad inputs and outputs at machine speed (~10ms). Deterministic pattern matching: content filters, PII detection, topic restrictions, rate limits. Permissions derive from business intent - what the use case requires - not from evaluation of the model's capabilities. These are **action-space constraints** that leave the model's reasoning unconstrained. Every request passes through. No exceptions.

**Layer 2 - Model-as-Judge** catches unknown-bad through independent model evaluation. The Judge can be a large LLM running asynchronously (500ms to 5s) or a [distilled SLM](../extensions/technical/distill-judge-slm.md) running inline as a sidecar (10ms to 50ms). Either way, **enterprise-owned and configured**, evaluating task agent outputs against policy, factual grounding, tone, and safety criteria. Catches what guardrails cannot pattern-match, including within-bounds adversarial behavior that containment alone cannot address.

**Layer 3 - Human Oversight** provides the accountability backstop. Scope scales with risk: low-risk systems get spot checks, high-risk systems get human approval before commit. Humans decide edge cases. Humans own outcomes. Handles what neither containment nor the Judge can resolve autonomously.

**Circuit Breaker** stops all AI traffic and activates a non-AI fallback when any layer fails. Not a degradation - a full stop with a predetermined safe state.

Each layer is specifically designed to catch what the previous layer misses. This is compound defence by design - not defence-in-depth by coincidence. For the full argument, see [Why Containment Beats Evaluation](../insights/why-containment-beats-evaluation.md).

This pattern already exists in production at major platforms: NVIDIA NeMo, AWS Bedrock, Azure AI, LangChain, Guardrails AI, and others. This reference provides the vendor-neutral implementation: risk classification, controls, fail postures, and tested fallback paths.

## Get Started

| If you want to... | Go here |
| --- | --- |
| Get started quickly | [Quick Start](../QUICK_START.md) |
| Deploy low-risk AI fast | [Fast Lane](../FAST-LANE.md) |
| Understand the concepts in 30 minutes | [Quick Start](../QUICK_START.md) |
| Implement controls with working code | [Implementation Guide](../IMPLEMENTATION_GUIDE.md) |
| Classify a system by risk | [Risk Tiers](../core/risk-tiers.md) |
| Deploy an agentic AI system | [Agentic Controls](../core/agentic.md) |
| Understand what happens when controls fail | [PACE Resilience](../PACE-RESILIENCE.md) |
| Enforce controls at the infrastructure layer | [Infrastructure Controls](../infrastructure/) |
| Track your implementation | [Checklist](../core/checklist.md) |
| **Secure a multi-agent system** | **[MASO Framework](../maso/)** |

## Before You Build Controls

> **[The First Control: Choosing the Right Tool](../insights/the-first-control.md)**
>
> The most effective way to reduce AI risk is to not use AI where it doesn't belong. Before guardrails, judges, or human oversight - ask whether AI is the right tool for this problem.

If your deployment is internal, read-only, handles no regulated data, and has a human reviewing output - start with the [Fast Lane](../FAST-LANE.md). You may not need the rest.

## Risk-Scaled Controls

Controls scale to risk so that low-risk AI moves fast and high-risk AI stays safe. The framework provides a menu of control patterns. Select the ones you need. Consciously deselect the ones you do not. Every organisation has its own way of doing things, and the controls are designed to fit your context rather than impose a single way of working.

| Risk Tier | Controls Required | PACE Posture | Use Case Examples |
| --- | --- | --- | --- |
| **Low** | Fast Lane: minimal guardrails, self-certification | P only (fail-open with logging) | Internal chatbots, document summarisation, code assistance |
| **Medium** | Guardrails + Judge, periodic human review | P + A configured | Customer-facing content, recommendation engines, search |
| **High** | All three layers, human-in-the-loop for writes | P + A + C configured and tested | Financial advice, medical support, regulatory decisions |
| **Critical** | Full architecture, mandatory human approval | Full PACE cycle with tested E→P recovery | Autonomous actions on regulated data, safety-critical systems |

Classify your system: **[Risk Tiers](../core/risk-tiers.md)**

## PACE Resilience

Every control has a defined failure mode. The [PACE methodology](../PACE-RESILIENCE.md) ensures that when a control layer degrades - and it will - the system fails safely rather than silently.

**Primary:** All layers operational. Normal production.

**Alternate:** One layer degraded. Backup activated. Scope tightened. Example: Judge layer is down → guardrails remain active, all outputs queued for human review.

**Contingency:** Multiple layers degraded. AI operates in supervised-only mode. Human approves every action. Reduced capacity, high assurance.

**Emergency:** Confirmed compromise or cascading failure. Circuit breaker fires. AI traffic stopped. Non-AI fallback activated. Incident response engaged.

Even at the lowest risk tier, there's a fallback plan. At the highest, there's a structured degradation path from full autonomy to full stop.

## Core Documents

| Document | Purpose |
| --- | --- |
| [Quick Start](../QUICK_START.md) | From zero to deployed in 30 minutes |
| [Fast Lane](../FAST-LANE.md) | Pre-approved minimal controls for low-risk AI |
| [Risk Tiers](../core/risk-tiers.md) | Classify your system, determine control and resilience requirements |
| [Risk Assessment](../core/risk-assessment.md) | Quantitative control effectiveness, residual risk per tier, NIST AI RMF aligned |
| [Controls](../core/controls.md) | Guardrails, Judge, and Human Oversight implementation with per-layer fail postures |
| [Agentic](../core/agentic.md) | Controls for single autonomous AI agents including graceful degradation path |
| [PACE Resilience](../PACE-RESILIENCE.md) | What happens when controls fail |
| [Checklist](../core/checklist.md) | Track implementation and PACE verification progress |
| [Emerging Controls](../core/emerging-controls.md) | Multimodal, reasoning, and streaming considerations *(theoretical)* |

## Infrastructure Controls

This section defines *what* to enforce. The [infrastructure](../infrastructure/) section defines *how* - 80 technical controls across 11 domains, with standards mappings and platform-specific patterns.

**Domains:** Identity & Access Management (8), Logging & Observability (10), Network & Segmentation (8), Data Protection (8), Secrets & Credentials (8), Supply Chain (8), Incident Response (8), Tool Access (6), Session & Scope (5), Delegation Chains (5), Sandbox Patterns (6).

**Standards mappings:** Every control maps to the three-layer model, ISO 42001 Annex A, NIST AI RMF, and OWASP LLM/Agentic Top 10.

**Platform patterns:** AWS Bedrock, Azure AI, and Databricks reference architectures.

## Defence in Depth Beyond the AI Layer

![Defence in Depth Beyond the AI Layer](../images/defence-in-depth-beyond-ai.svg)

The three-layer model above - guardrails, judge, human oversight - addresses controls specific to non-deterministic AI behavior. It does not replace the security controls your organisation already has. It sits inside them.

Your existing DLP systems apply to data flowing into and out of AI systems - both preventing sensitive data from reaching models and catching leakage that AI-specific controls miss. API gateways validate requests and enforce schemas regardless of whether the caller is human or AI. Database access controls and parameterised queries prevent injection even if an agent constructs a malicious query. IAM governs who can invoke AI systems in the first place. SIEM correlates AI events with network, endpoint, and application events. Secure coding practices in the systems agents interact with still matter - arguably more, because the caller is now non-deterministic.

These controls are outside the scope of this reference, but they are part of your defence. When you assess your AI security posture, include them. When you threat-model, include them. When one of these controls misses something, they are your safety net.

For multi-agent systems, the **[MASO Environment Containment](../maso/environment-containment.md)** strategy formalises this principle: harden every system the agent connects to (strict API validation, stored procedures, opaque errors, no-retry enforcement, kill switches) so that agent misbehavior is structurally harmless regardless of the agent's intent.

## When You Need Multi-Agent

When AI agents collaborate, delegate tasks, and take autonomous actions across trust boundaries, the single-agent controls on this page are necessary but not sufficient. The **[MASO Framework](../maso/)** extends this architecture into multi-agent orchestration.

| What MASO adds | Why single-agent controls aren't enough |
| --- | --- |
| **Inter-agent message bus security** | Agents communicating directly create uncontrolled trust boundaries |
| **Non-Human Identity per agent** | Shared credentials between agents create lateral movement risk |
| **Epistemic integrity controls** | Hallucinations compound across agent chains; confidence inflates without evidence |
| **Transitive authority prevention** | Delegation creates implicit privilege escalation |
| **Kill switch architecture** | Multi-agent cascading failures require system-wide emergency stop |
| **Dual OWASP coverage** | Agentic Top 10 (2026) risks only exist when agents act autonomously |

| Document | Purpose |
| --- | --- |
| [MASO Overview](../maso/) | Architecture, PACE integration, OWASP dual mapping, 7 control domains |
| [Tier 1 - Supervised](../maso/implementation/tier-1-supervised.md) | Low autonomy: human approves all writes |
| [Tier 2 - Managed](../maso/implementation/tier-2-managed.md) | Medium autonomy: NHI, signed bus, Model-as-Judge, continuous monitoring |
| [Tier 3 - Autonomous](../maso/implementation/tier-3-autonomous.md) | High autonomy: self-healing PACE, adversarial testing, isolated kill switch |
| [Red Team Playbook](../maso/red-team/red-team-playbook.md) | 13 adversarial test scenarios for multi-agent systems |
| [Integration Guide](../maso/integration/integration-guide.md) | LangGraph, AutoGen, CrewAI, AWS Bedrock implementation patterns |
| [Worked Examples](../maso/examples/worked-examples.md) | Financial services, healthcare, critical infrastructure |

## Extensions

| Folder | Contents |
| --- | --- |
| [Regulatory](../extensions/regulatory/) | ISO 42001 and EU AI Act mapping |
| [Technical](../extensions/technical/) | Bypass prevention, metrics |
| [Industry Solutions](../extensions/technical/current-solutions.md) | Guardrails, evaluators, and safety model reference |
| [Templates](../extensions/templates/) | Risk assessment templates, implementation plans |
| [Worked Examples](../extensions/examples/) | Per-tier implementation walkthroughs |

## Insights

**Foundational Arguments**

| Article | Key Argument |
| --- | --- |
| [The First Control: Choosing the Right Tool](../insights/the-first-control.md) | Design thinking before technology selection |
| [Why Your AI Guardrails Aren't Enough](../insights/why-guardrails-arent-enough.md) | Guardrails block known-bad; you need detection for unknown-bad |
| [The Judge Detects. It Doesn't Decide.](../insights/judge-detects-not-decides.md) | Async evaluation beats real-time blocking for nuanced decisions |
| [Infrastructure Beats Instructions](../insights/infrastructure-beats-instructions.md) | You can't secure AI systems with prompts alone |
| [Risk Tier Is Use Case, Not Technology](../insights/risk-tier-is-use-case.md) | Classification reflects deployment context, not model capability |
| [Humans Remain Accountable](../insights/humans-remain-accountable.md) | AI assists decisions; humans own outcomes |

**Emerging Challenges**

| Article | Key Argument |
| --- | --- |
| [The Verification Gap](../insights/the-verification-gap.md) | Current safety approaches can't confirm ground truth |
| [Behavioral Anomaly Detection](../extensions/technical/behavioral-anomaly-detection.md) | Aggregating signals to detect drift from expected behavior |
| [Multimodal AI Breaks Your Text-Based Guardrails](../insights/multimodal-breaks-guardrails.md) | Images, audio, and video create new attack surfaces |
| [When AI Thinks Before It Answers](../insights/when-ai-thinks.md) | Reasoning models need reasoning-aware controls |
| [When Agents Talk to Agents](../insights/when-agents-talk-to-agents.md) | Multi-agent accountability gaps → see [MASO](../maso/) |
| [The Memory Problem](../insights/the-memory-problem.md) | Long context and persistent memory introduce novel risks |
| [You Can't Validate What Hasn't Finished](../insights/you-cant-validate-unfinished.md) | Real-time streaming challenges existing validation |
| [Open-Weight Models Shift the Burden](../insights/open-weight-models-shift-the-burden.md) | Self-hosted models inherit the provider's control responsibilities |
| [When the Judge Can Be Fooled](../core/when-the-judge-can-be-fooled.md) | The Judge layer needs its own threat model |

## Platforms Implementing This Pattern

This isn't a theoretical proposal. These platforms already implement variants of this pattern:

| Platform | Approach |
| --- | --- |
| [NVIDIA NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | Five rail types: input, dialog, retrieval, execution, output |
| [LangChain](https://docs.langchain.com/) | Middleware chains with human-in-the-loop |
| [Guardrails AI](https://www.guardrailsai.com/) | Open-source validator framework |
| [Galileo](https://www.rungalileo.io/) | Eval-to-guardrail lifecycle |
| [DeepEval](https://github.com/confident-ai/deepeval) | Model-as-Judge evaluation framework |
| AWS Bedrock Guardrails | Managed input/output filtering |
| Azure AI Content Safety | Content filtering and moderation |

## Standards Alignment

| Standard | Relevance | Mapping |
| --- | --- | --- |
| [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | Security vulnerabilities in LLM applications | [OWASP mapping](../infrastructure/mappings/owasp-llm-top10.md) |
| [OWASP Agentic Top 10](https://genai.owasp.org/) | Risks specific to autonomous AI agents | [MASO mapping](../maso/) |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | AI risk management framework | [NIST mapping](../infrastructure/mappings/nist-ai-rmf.md) |
| [ISO 42001](https://www.iso.org/standard/81230.html) | AI management system standard | [ISO 42001 mapping](../infrastructure/mappings/iso42001-annex-a.md) |
| [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final) | Secure development for generative AI | [SP 800-218A mapping](../infrastructure/mappings/nist-sp800-218a.md) |
| [MITRE ATLAS](https://atlas.mitre.org/) | Adversarial threat landscape for AI | [MASO threat intelligence](../maso/threat-intelligence/incident-tracker.md) |
| [DORA](https://www.digital-operational-resilience-act.com/) | Digital operational resilience | [MASO regulatory alignment](../maso/) |

## Scope

**In scope:** Custom LLM applications, AI decision support, document processing, single-agent systems - from deployment through incident response.

**Out of scope:** Vendor AI products (use vendor controls), model training (see MLOps security guidance), and pre-deployment testing. This framework is about reducing harm during live operation.

**Pre-deployment complement:** For secure development practices covering data sourcing, training, fine-tuning, and model release, see [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final). This framework begins where SP 800-218A ends.

**For multi-agent systems:** See [MASO](../maso/).

## Contributing

Feedback, corrections, and extensions welcome. See [CONTRIBUTING.md](../CONTRIBUTING.md).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

