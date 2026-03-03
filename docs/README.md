---
title: AI Runtime Behaviour Security
description: A practical, open-source framework for securing AI systems at runtime - where prompt injection, model manipulation, and agent drift actually happen.
hide:
  - toc
  - path
  - navigation
  - feedback
comments: false
---

# AI Runtime Behaviour Security

## AI systems don't just have vulnerabilities. They have behaviours.

**A practical, open-source framework for securing AI systems at runtime - where prompt injection, model manipulation, and agent drift actually happen.**

Most AI security guidance stops at the model layer. This framework addresses what happens after deployment: how AI systems behave in production, how that behaviour is monitored, and how it's contained when things go wrong. Built from 20+ years of enterprise cybersecurity experience in regulated financial services.

<div style="text-align: center" markdown>

[Quick Start Guide](QUICK_START.md){ .md-button .md-button--primary }
[See the Architecture](ARCHITECTURE.md){ .md-button }
[Downloads](downloads.md){ .md-button }
[About the Author](ABOUT.md){ .md-button }

</div>

---

<div class="landing-cards" markdown>

<div class="landing-card" markdown>

### For Security Leaders

**"I need to govern AI risk across the enterprise"**

Start with the three-layer architecture: guardrails, LLM-as-Judge evaluation, and human oversight. Map it to your existing risk framework and regulatory obligations.

[Framework Overview](ARCHITECTURE.md){ .md-button }

</div>

<div class="landing-card" markdown>

### For Security Architects & Engineers

**"I need to implement runtime controls"**

Go straight to the technical controls: behavioural boundaries, output validation, agent containment patterns, and integration with AWS Bedrock, Azure AI, or self-hosted models.

[Technical Implementation](QUICK_START.md){ .md-button }

</div>

<div class="landing-card" markdown>

### For Compliance & Risk

**"I need to show regulators we have this covered"**

See how the framework maps to ISO 42001, EU AI Act, NIST AI RMF, and banking-specific requirements. Ready-made crosswalks for audit and compliance conversations.

[Regulatory Mapping](stakeholders/compliance-and-legal.md){ .md-button }

</div>

</div>

---

## Three layers. One principle: contain behaviour, don't just classify risk.

| Layer | What it does | Why it matters |
| --- | --- | --- |
| **Guardrails** | Enforces behavioural boundaries at the input and output level | Stops known-bad patterns before they reach users or downstream systems |
| **LLM-as-Judge** | Uses a secondary model to evaluate outputs against policy | Catches nuanced violations that rule-based systems miss |
| **Human Oversight** | Escalation, review, and override for high-stakes decisions | Keeps humans in the loop where regulatory and ethical stakes demand it |

![Four-layer runtime security: Guardrails → Judge → Human → Circuit Breaker](images/runtime-layers.svg)

[See the full architecture diagram](ARCHITECTURE.md){ .md-button }

---

!!! abstract "MASO - Multi-Agent Security Operations"

    As AI moves from single-model deployments to multi-agent orchestration, the attack surface multiplies. MASO addresses agent-to-agent trust, delegation boundaries, and coordinated containment.

    [Explore the MASO Framework](maso/){ .md-button }

!!! abstract "ISO 42001 Clause Mapping"

    Clause-by-clause mapping showing how runtime behaviour controls satisfy ISO 42001 requirements. Built for teams preparing for certification or audit.

    [View the Mapping](extensions/regulatory/iso-42001-clause-mapping.md){ .md-button }

---

## Take the framework with you

Download the executive summary - a single document covering the architecture, key controls, and regulatory alignment. No email required. Share it with your team, your CISO, or your auditors.

[Download PDF (Executive Summary)](downloads.md){ .md-button .md-button--primary }

---

??? question "Common questions - cost, Judge reliability, supply chain, human factors"

    | I'm asking about... | Start here |
    | --- | --- |
    | What these controls cost and how to manage latency | [Cost & Latency](extensions/technical/cost-and-latency.md) - sampling strategies, latency budgets, tiered evaluation cascade |
    | What happens when the Judge is wrong | [Judge Assurance](core/judge-assurance.md) - accuracy metrics, calibration, adversarial testing, fail-safe mechanisms |
    | How the Judge can be attacked | [When the Judge Can Be Fooled](core/when-the-judge-can-be-fooled.md) - output crafting, judge manipulation, mitigations by tier |
    | Securing the AI supply chain | [Supply Chain Controls](maso/controls/supply-chain.md) - AIBOM, signed manifests, MCP vetting, model provenance |
    | Human operator fatigue and automation bias | [Human Factors](strategy/human-factors.md) - skill development, alert fatigue, challenge rate testing |
    | Risks that emerge when agents collaborate | [Emergent Risk Register](maso/controls/risk-register.md) - 33 risks across 9 categories, with coverage assessment |

??? example "More paths - strategy, red teaming, worked examples, full reference"

    | I want to... | Start here |
    | --- | --- |
    | Get the one-page reference | [Cheat Sheet](CHEATSHEET.md) - classify, control, fail posture, test |
    | Quantify AI risk for board reporting | [Risk Assessment](core/risk-assessment.md) |
    | Align AI with business strategy | [From Strategy to Production](strategy/) |
    | See everything on one map | [Tube Map](TUBE-MAP.md) |
    | Understand PACE resilience | [PACE Methodology](PACE-RESILIENCE.md) |
    | Run adversarial tests on agents | [Red Team Playbook](maso/red-team/red-team-playbook.md) |
    | Implement in LangGraph, AutoGen, CrewAI, or Bedrock | [Integration Guide](maso/integration/integration-guide.md) |
    | See one transaction end-to-end with every log event | [Runtime Telemetry Reference](extensions/technical/runtime-telemetry-reference.md) |
    | Enforce controls at infrastructure level | [Infrastructure Controls](infrastructure/) |
    | See real incidents mapped to controls | [Incident Tracker](maso/threat-intelligence/incident-tracker.md) |
    | See MASO applied in finance, healthcare, or energy | [Worked Examples](maso/examples/worked-examples.md) |
    | Navigate by role | [Framework Map](FRAMEWORK-MAP.md) |
    | Understand what's validated and what's not | [Maturity & Validation](MATURITY.md) |
    | See all references and further reading | [References & Sources](REFERENCES.md) |

---

<div class="credibility-strip" markdown>

**Open source on GitHub** - star, fork, or contribute  ·  **Built by a practitioner, not a vendor**  ·  **Based on real-world incidents in regulated financial services**

</div>

---

## How to Use This

??? info "What it provides, what it doesn't, and how to approach it"

    This is a practitioner's reference - not a standard, not a certification, not a product pitch. Take what's useful, adapt it to your environment, ignore what doesn't fit.

    **What it provides:**

    - **A way of thinking about controls, not a prescription for them.** It describes *what* needs to be true and *why* it matters. It does not mandate a specific product, vendor, or architecture. If your existing tools already satisfy a control, you don't need new ones.
    - **Help deciding where to invest.** Not every control matters equally. Risk tiers, PACE resilience levels, and the distinction between foundation and multi-agent controls exist so you can reason about priority.
    - **Defence in depth as a design principle.** The layered approach exists because each layer covers gaps in the others. The question isn't "which layer do we need?" but "what happens when each layer fails?"
    - **Resilience thinking for AI products.** Traditional security asks "how do we prevent bad things?" This reference also asks "what happens when prevention fails?"
    - **Clarity on when tools are *not* needed.** Some controls are already handled by your existing infrastructure. This should help you see where you already have coverage, not convince you to buy something new.
    - **An AI-specific layer, not a replacement for everything else.** This addresses the controls unique to non-deterministic AI behaviour. It does not replace your existing DLP, API validation, database access controls, IAM, SIEM, secure coding practices, or incident response capabilities. Those controls still matter - arguably more than ever, because they are your safety net when AI-specific controls miss something.

    **What it is not:**

    - Not a certification or audit standard. You cannot be "compliant with" this reference.
    - Not a product recommendation. Tool and vendor references are illustrative, not endorsements.
    - Not a substitute for professional security assessment of your specific deployment.
    - Not a finished document. AI security is moving fast. This will evolve as the landscape does.

---

## About the Author

**Jonathan Gill** is a cybersecurity practitioner with over 30 years in information technology and 20+ years in enterprise cybersecurity. His career spans UNIX system administration, building national-scale ISP infrastructure, enterprise security architecture at major financial institutions, and diplomatic IT service.

His current focus is AI security governance: designing control architectures that address the unique challenges of securing non-deterministic systems at enterprise scale, and translating complex technical risk into actionable guidance for engineering teams and executive leadership.

- GitHub: [@JonathanCGill](https://github.com/JonathanCGill)
- LinkedIn: [Jonathan Gill](https://www.linkedin.com/in/jonathancgill/)

[Read more](ABOUT.md){ .md-button }

---

## Disclaimer

This reference is provided as-is under the [MIT License](../LICENSE). As described in [How to Use This](#how-to-use-this), it is a thinking tool - not a standard, certification, or guarantee of security. It reflects one practitioner's synthesis of industry patterns, regulatory requirements, and operational experience.

If you adopt any part of this, you are responsible for validating it against your own threat model, environment, and regulatory obligations.

This framework was written with AI assistance (Claude and ChatGPT) for drafting, structuring, and research synthesis. Architecture, control design, risk analysis, and editorial judgment are the author's.

This is a personal project. It is not affiliated with, endorsed by, or representative of any employer, organisation, or other entity. The views and opinions expressed are the author's own and should not be construed as reflecting the position or policy of any company or institution with which the author is or has been associated.

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
