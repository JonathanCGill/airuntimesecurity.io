# Evolution

**How this framework changed - and why.**

> Part of [AI Runtime Behaviour Security](./)
> Last updated: February 2026

---

## Why This Page Exists

Frameworks that don't change aren't frameworks - they're snapshots. This page tracks the significant decisions, course corrections, and additions that shaped this framework, with the reasoning behind each.

A static framework published once and never revised signals that either the domain is solved (it isn't) or the authors stopped paying attention. This page is evidence that neither is true.

For the mechanical changelog (version numbers, file-level changes), see [Changelog](CHANGELOG.md).

---

## Timeline

### December 2025 - Initial Release (v0.1.0)

**The starting point: three layers and a risk model.**

The framework launched with the core thesis: AI systems are non-deterministic, you can't fully test them before deployment, so you need runtime behavioural monitoring. The three-layer model - Guardrails prevent, Judge detects, Humans decide - was the foundation.

This wasn't a novel invention. NVIDIA NeMo, AWS Bedrock, Azure AI, and LangChain were already implementing variants of this pattern independently. The framework's contribution was codifying it: risk tiers, control selection criteria, implementation guidance, and standards mappings - in one place, vendor-neutral.

**What drove this:** Years of watching enterprise AI deployments launch with either no security controls or ad-hoc guardrails that addressed only the most obvious risks. The gap between "we have guardrails" and "we have a security architecture" was the motivation.

---

### January 2026 - Agentic Controls & Standards Alignment (v0.2.0)

**The first expansion: agents change the threat model.**

Agentic AI systems - where the LLM can take actions, call tools, and operate with some autonomy - were becoming standard. The original three-layer model assumed a request/response pattern. Agents break that assumption: they maintain state, make decisions, and execute multi-step plans.

Added agentic controls (AG.1-AG.4), including MCP/function calling security (AG.2.5). Added ISO 42001 alignment and EU AI Act crosswalk.

**What drove this:** The rapid adoption of tool-calling patterns in production LLM applications. Organisations were deploying agents with tool access and no security architecture for the tool boundary.

---

### Early February 2026 - Rapid Expansion (v0.3.0 – v0.4.1)

**The depth phase: controls for real operational risks.**

Three releases in quick succession added:

- 10 new controls addressing novel AI risks, support system dependencies, and banking-specific requirements
- AI Incident Response Playbook (10 AI-specific playbooks)
- Vendor Assessment Questionnaire
- Bypass Prevention document covering 5 bypass categories
- Technical Controls document (network, WAF, AI gateway, DLP)
- 14 new architecture diagrams

**What drove this:** Conversations with practitioners who said "the three-layer model makes sense, but how do I actually implement it in my environment?" The framework needed operational depth, not just architectural direction. The banking cyber risks addition came from direct engagement with financial services practitioners who needed AI risk mapped to their existing control frameworks.

---

### February 7, 2026 - The Structure Reset (v0.5.0)

**The framework had grown to 48 files. Nobody could find anything.**

Major restructure into Core + Extensions. Created a clear 5-document starting path (core/) while preserving all depth in extensions/. This was a usability decision, not a content decision - nothing was removed, everything was reorganised.

**What drove this:** Feedback that the framework was comprehensive but overwhelming. New readers couldn't distinguish essential from supplementary. The Core + Extensions model gave a clear "start here" path while preserving depth for those who needed it.

---

### February 8, 2026 - The Honesty Moment (v0.6.0)

**Renamed from "AI Security Blueprint" to "Enterprise AI Security Framework."**

"Blueprint" implied buildable artifacts - specific, ready-to-deploy implementations. The framework was strategic guidance, not a blueprint. The rename was an honesty correction. Later renamed to **AI Runtime Behaviour Security** to reflect the core thesis: AI is non-deterministic, so you secure it by observing runtime behaviour.

Simultaneously added the Implementation Guide: ~1,500 lines of copy-paste-ready Python covering input guardrails, output guardrails, LLM-as-Judge, human-in-the-loop queue, and telemetry. If the framework was going to be called a framework and not a blueprint, it needed an actual implementation path alongside the strategic guidance.

**What drove this:** A self-assessment that asked: "Would a practitioner be able to build anything from this?" The answer was "they'd know *what* to build but not *how*." The Implementation Guide closed that gap.

---

### February 2026 - MASO: The Multi-Agent Problem

**The biggest addition: 128 controls for multi-agent orchestration.**

The Multi-Agent Security Operations (MASO) framework was the response to a fundamental architectural shift. Single-agent controls assume one AI, one context window, one trust boundary. Multi-agent systems break all three assumptions.

MASO added:

- 7 control domains (Prompt/Goal/Epistemic Integrity, Identity & Access, Data Protection, Execution Control, Observability, Supply Chain, Privileged Agent Governance)
- 3 implementation tiers with graduation criteria
- Incident Tracker mapping known real-world incidents to controls, plus risk stories from production failures
- Red Team Playbook with 13 adversarial test scenarios
- Integration patterns for LangGraph, AutoGen, CrewAI, AWS Bedrock
- Worked examples in financial services, healthcare, and critical infrastructure
- Emerging Threats analysis with 8 forward-looking threat patterns
- Dual OWASP coverage: LLM Top 10 (2025) + Agentic Top 10 (2026)
- 34 emergent risks beyond OWASP taxonomies

**What drove this:** Three things converging: (1) the Morris II worm proof-of-concept showing self-replicating prompt injection across agents, (2) the MCP supply chain attacks demonstrating that agent tool ecosystems have the same problems as npm circa 2016, and (3) the recognition that epistemic failures - groupthink, hallucination amplification, confidence inflation - are not adversarial attacks but emergent properties of multi-agent interaction that produce failures indistinguishable from success.

**The novel contribution:** Epistemic security as a formal control domain. Most AI security frameworks focus on adversarial attacks. MASO also addresses the non-adversarial failures that emerge when agents work together: correlated errors, synthetic corroboration, semantic drift, uncertainty stripping. We haven't found another framework that treats these as formal controls with test criteria - though others may be working on similar ideas.

---

### February 2026 - Infrastructure Controls (80 controls, 11 domains)

**The "how" behind the "what."**

The core framework defines what to enforce. The infrastructure layer defines how - at the network, platform, and tooling level. 80 controls across 11 domains, with standards mappings (OWASP, NIST, ISO) and platform-specific reference architectures (AWS Bedrock, Azure AI, Databricks).

**What drove this:** The gap between "implement DLP on the message bus" (a MASO control) and "here's how to implement DLP on the message bus in AWS Bedrock" (an infrastructure pattern). Security architects needed both levels.

---

### February 2026 - Maturity & Validation

**The credibility reckoning.**

Added the [Maturity & Validation](MATURITY.md) page and [Validated Against Real Incidents](VALIDATED-AGAINST.md) page. These exist because too many frameworks present themselves as established when they're theoretical.

The framework has not been deployed end-to-end in production. No organisation has reported back. The adopters list is empty. Rather than ignoring this, we documented it explicitly - along with what *is* validated (incident mapping, standards alignment, pattern consistency) and what isn't (production metrics, Judge accuracy baselines, PACE failover performance).

**What drove this:** The recognition that credibility doesn't come from claiming validation you don't have. It comes from being honest about what you know and what you don't - and showing your evidence.

---

## What's Next

The [Changelog](CHANGELOG.md) tracks planned work. The major open items:

| Area | Status | What's Needed |
|------|--------|--------------|
| Production deployment data | No data | An organisation pilots the framework and shares results |
| Cost model with production data | Theoretical estimates only | Measured latency, cost, and false positive rates from real deployment |
| Judge accuracy benchmarks | Failure mode analysis exists | Measured accuracy across models and use cases |
| Epistemic risk detection algorithms | Risk categories defined | Algorithmic detection methods with threshold calibration |
| Platform-specific guides (detailed) | Reference architectures exist | Step-by-step deployment guides with Terraform/CDK |

This framework evolves when practitioners use it, break it, and tell us what happened. If you've implemented any part of it - or tried to and failed - that feedback is more valuable than any theoretical improvement.

---

*AI Runtime Behaviour Security, 2026 (Jonathan Gill).*
