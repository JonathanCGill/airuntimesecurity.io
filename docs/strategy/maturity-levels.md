---
description: "How organisational maturity affects AI security posture. What Level 1 and Level 5 organisations actually look like, the real gap between available controls and operational discipline, and why the answer is different for AI you build versus AI you consume."
---

# Maturity Levels

*What maturity actually means for AI security, why most organisations are further along than they think, and where the real gaps are.*

> Part of [From Strategy to Production](README.md)

## Scope: AI You Build vs. AI You Consume

This framework is primarily designed for **AI systems your organisation develops and operates**: custom models, fine-tuned LLMs, RAG pipelines, autonomous agents, and multi-agent systems. These are the systems where you own the runtime, control the data flows, and bear full responsibility for behaviour in production.

Most organisations also consume AI through other channels. The maturity questions are different for each:

| Track | Examples | Who owns the runtime | What maturity looks like |
|-------|----------|---------------------|------------------------|
| **AI you build and operate** | Custom agents, RAG pipelines, fine-tuned models, multi-agent systems | You do | Full framework applies. Three-layer controls, PACE resilience, progressive autonomy. |
| **AI platforms you build on** | AWS Bedrock, Azure OpenAI Service, GCP Vertex AI | Shared. Platform provides infrastructure; you configure and govern. | Configure the controls your platform provides. Monitor the logs. Act on what you find. |
| **Copilots and productivity AI** | Microsoft 365 Copilot, GitHub Copilot, Salesforce Einstein | Vendor operates the AI; you govern access and data. | Data classification, access governance, RAG exposure management, output review processes. |
| **AI coding tools** | GitHub Copilot, Cursor, Claude Code | Vendor operates the AI; you own what ships to production. | Code review discipline. Understanding AI-generated output before it reaches production. |

The rest of this article addresses maturity across all four tracks. The full [control architecture](../ARCHITECTURE.md), [risk tiers](../core/risk-tiers.md), and [MASO framework](../maso/README.md) apply in depth to the first track. For the other three, the framework provides the mental model; the implementation details differ.

## Why Maturity Models Matter

Maturity models exist to answer a simple question: **where are we, and what should we build next?**

Without one, organisations either underinvest (operating at risk levels they don't recognise) or overinvest (applying Tier 3 controls to Tier 1 problems). The complication: most organisations are at different levels on different tracks simultaneously. An enterprise might be Level 4 on copilot adoption and Level 1 on custom AI. The model needs to help leaders locate themselves on each track.

## Established Maturity Models

Several authoritative models inform this framework's approach. None were designed specifically for AI runtime security, but each contributes a useful lens.

### CMMI (Capability Maturity Model Integration)

The most widely recognised maturity model. Five levels from ad hoc to optimising, maintained by ISACA (originally SEI at Carnegie Mellon). The existing [MASO implementation tiers](../maso/README.md) reference CMMI levels explicitly: Tier 1 maps to CMMI Level 1-2, Tier 2 maps to Level 2-3, Tier 3 maps to Level 3+.

**Median transition time from Level 1 to Level 2: 5 months. Level 2 to Level 3: an additional 21 months.**

### NIST Cybersecurity Framework 2.0

Four implementation tiers (Partial, Risk Informed, Repeatable, Adaptive). NIST is explicit that these are not maturity levels, but they are widely used as a practical maturity proxy. The NIST AI RMF mirrors this structure with four functions: Govern, Map, Measure, Manage.

NIST is also developing **COSAiS (Control Overlays for Securing AI Systems)**, which will provide separate security overlays for different AI use cases: adapting and using generative AI, fine-tuning predictive AI, and using agentic AI. This is the clearest signal from a standards body that consumed AI and built AI require different security treatments.

### C2M2 (Cybersecurity Capability Maturity Model)

From the U.S. Department of Energy. Four levels (MIL 0-3), 356 practices across 10 domains. The critical design principle: **achieving the highest level in all domains is not necessarily optimal.** Organisations should set target maturity per domain based on business objectives. This principle applies directly to AI security maturity: not every organisation needs Tier 3 autonomous AI, and not every domain needs Level 5 data governance.

### AI-Specific Models

| Model | Source | Released | Key contribution |
|-------|--------|----------|-----------------|
| **AI Maturity Model for Cybersecurity** | Cloud Security Alliance + Darktrace | January 2026 | Five levels (L0-L4) based on operational data from ~10,000 deployments. Grounded in what organisations actually do, not what they should do. |
| **AI Maturity Assessment (AIMA)** | OWASP | August 2025 | Eight assessment domains including data management, governance, and operations. Adapted from OWASP SAMM. |
| **ISO/IEC 42001:2023** | ISO | 2023 | First certifiable AI management system standard. Not a maturity model, but a management system that builds on ISO 27001. Organisations already ISO 27001 certified can reach 42001 compliance up to 40% faster. |
| **AI Controls Matrix** | Cloud Security Alliance | 2025 | 243 control objectives with an explicit shared responsibility model distinguishing AI Consumer, Model Provider, and Application Provider roles. |

A **DoD AI Security Framework** (CMMC-style for AI) is mandated by Section 1513 of defence policy law, with a status report to Congress due June 2026.

## What Organisations Actually Look Like

### Level 1: Ad Hoc

**How you recognise it:** Security depends on individual effort, not organisational capability. Controls exist in pockets but are not coordinated. AI adoption is happening, but governance has not caught up.

**AI you build and operate:**
No formal AI security programme. Development teams deploy AI experiments without security review. No data lineage tracking, so poisoning detection is impossible. No behavioural monitoring of AI systems in production. Incidents are discovered by accident. If an AI system hallucinates a regulatory disclosure or leaks PII through a tool call, nobody knows until a customer complains or an auditor asks.

**Cloud AI platforms:**
The organisation uses AWS, Azure, or GCP for AI workloads but has not configured the security controls the platform provides. On AWS Bedrock, guardrails are entirely opt-in and have not been created. On GCP Vertex AI, the main harm filters are off by default and nobody has turned them on. Azure OpenAI Service ships with default content filters active, which provides a baseline, but logging and alerting have not been configured. The controls exist. Nobody has configured them.

**Copilots and productivity AI:**
Shadow AI is widespread. Developers use GitHub Copilot, teams use ChatGPT through personal accounts, departments adopt AI tools without IT involvement. No tracking of AI-generated content versus human-created content. Data classification is poor, so copilots that access organisational data (M365 Copilot, Salesforce Einstein) surface sensitive information to users who should not see it. Only 30% of organisations classify and protect data effectively.

**AI coding tools:**
Developers use AI code generation without any review process distinguishing AI-generated code from human-written code. AI-generated code goes through the same review process as human code, if it goes through review at all. No organisational awareness of which production code was AI-generated.

**Data management:**
No ownership, no accountability. Training data (where custom AI exists) is sourced informally. No data quality gates. Gartner found that 63% of organisations lack appropriate data management practices for AI, and predicts that most AI projects unsupported by AI-ready data will be abandoned.

**Monitoring and incident response:**
For AI systems: none. For cloud platforms generally: basic logging that is configured but rarely reviewed. SOC teams review only 49% of alerts they should on a typical day (IBM). One-third of security teams admit to ignoring alerts due to false positives. Average time to identify a breach: 194 days.

**AI vs. non-AI security balance:** ~95:5. Security is almost entirely manual and traditional. AI plays no formal role in the security stack.

### Level 2: Managed

**How you recognise it:** Processes exist but vary across teams. Basic project-level discipline. Some documentation, some repeatability, but not consistent across the organisation.

**AI you build and operate:**
A small number of AI systems have been through a risk assessment. Basic guardrails are deployed on the most visible systems. No Judge evaluation capability. Human oversight is informal. Logging exists but is not structured for AI-specific failure modes. The team that built each system is also the team that monitors it.

**Cloud AI platforms:**
Platform-level controls are configured for production systems. Bedrock guardrails have been created for key deployments. Azure content filters are tuned per deployment. Logging is enabled and flows to the SIEM. But configuration is per-project, not standardised. Different teams make different choices. No organisational standard for AI platform security configuration.

**Copilots and productivity AI:**
An AI usage policy exists. Some discovery tooling is in place. The most visible shadow AI has been brought under governance. M365 Copilot deployment includes basic data governance (sensitivity labels applied to the most critical content). GitHub Copilot is licensed centrally. But embedded AI features in SaaS tools are still appearing without review.

**AI coding tools:**
Teams are aware that AI generates code. Some teams have guidelines for reviewing AI-generated code. No enforcement mechanism. No tracking of AI-generated code in production.

**Data management:**
Some processes documented and repeatable within business units. Basic data quality checks exist but are inconsistent. Access controls on datasets are formalised but may not cover AI-specific data flows.

**Monitoring and incident response:**
Rule-based automation appears (SOAR playbooks, XDR rules). AI-specific monitoring is limited to availability checks. No behavioural drift detection. Incident response for AI failures follows the generic IR playbook with no AI-specific runbooks.

**AI vs. non-AI security balance:** ~80:20. Automation is rule-based. AI may be piloted for specific security functions (anomaly detection) but is not integrated into workflows.

### Level 3: Defined

**How you recognise it:** Organisation-wide standards exist and are followed. Processes are documented, measured, and consistent across business units. This is where most useful work happens and where most organisations stall.

**AI you build and operate:**
Risk classification is systematic. All AI systems are assessed against the [risk tiers](../core/risk-tiers.md). Guardrails are standardised per tier. Judge evaluation is operational for HIGH and CRITICAL systems (5-10% sampling, scaling up). Human oversight processes are defined with SLAs. Logging is structured and AI-specific. PACE resilience is documented for critical systems. An AI governance function exists (or at least a defined role within governance).

**Cloud AI platforms:**
Platform security configuration is standardised through infrastructure-as-code. Every AI deployment inherits organisational defaults for content filtering, logging, and access control. Drift from the standard is detected. Platform-specific controls (Bedrock guardrails, Azure content safety, Vertex AI Model Armor) are configured to organisational policy and enforced consistently.

**Copilots and productivity AI:**
AI inventory is maintained and updated. Data classification covers the content that copilots can access. Sensitivity labels are enforced. DLP policies are extended to AI interactions. Usage analytics are reviewed. RAG exposure (what organisational data copilots can retrieve) is understood and governed. Procurement includes AI capability review for new SaaS tools.

**AI coding tools:**
Organisational policy defines expectations for AI-generated code review. Static analysis and security scanning apply equally to AI-generated and human-written code. Development teams understand the risks of AI code generation (licence contamination, insecure patterns, hallucinated dependencies).

**Data management:**
Organisation-wide standards for data processes. Data quality and security policies documented and enforced. Formal data lineage tracking is possible. Training data validation pipelines are standardised. RAG knowledge bases have defined quality and access policies. This is the minimum threshold where systematic AI data governance becomes feasible, a finding that converges across DAMA-DMBOK, DCAM, CMMI DMM, and ISO 8000.

**Monitoring and incident response:**
AI-assisted security is standard for specific functions (triage, alert correlation, vulnerability prioritisation). AI-specific monitoring includes behavioural baselines and drift detection. Incident response includes AI-specific runbooks. Post-incident reviews feed back into control improvement.

**AI vs. non-AI security balance:** ~60:40. AI tools assist with volume and pattern detection. Human analysts supervise, decide, and govern.

### Level 4: Quantitatively Managed

**How you recognise it:** Processes are measured with metrics and KPIs. Performance is predictable. Decisions are data-driven. Continuous improvement is based on quantitative analysis, not intuition.

**AI you build and operate:**
Judge accuracy is measured and tracked over time (detection rate, false positive rate, calibration data). Human oversight effectiveness is quantified (challenge rates, override accuracy, SLA compliance). Control effectiveness is scored per system. Risk assessments incorporate operational data, not just design-time assumptions. PACE transitions are tested through regular exercises with measured recovery times.

**Cloud AI platforms:**
Platform control effectiveness is measured. Guardrail activation rates, false positive rates, and content filter accuracy are tracked per deployment. Configuration drift is measured and remediated within defined SLAs. Cost of AI security controls is tracked and optimised.

**Copilots and productivity AI:**
AI usage analytics drive governance decisions. Data exposure incidents are tracked and trending. User compliance with AI policies is measured. Business impact of AI productivity tools is quantified (not just adoption rates).

**Data management:**
Statistical quality controls gate training data. Automated drift detection is integrated into ML pipelines. Quantitative thresholds trigger retraining or data review. Data poisoning detection through statistical anomaly analysis.

**Monitoring and incident response:**
AI is deeply embedded in detection and response. Decisions are data-driven. Mean time to detect and mean time to respond for AI-specific incidents are tracked. Predictive analytics identify emerging risks. The distinction between "AI in the SOC" (bolt-on tools) and an "AI SOC" (AI-native operations) begins to resolve.

**AI vs. non-AI security balance:** ~40:60. AI handles volume, speed, and pattern detection. Human analysts focus on exceptions and strategic oversight.

### Level 5: Optimising

**How you recognise it:** Continuous improvement through innovation. Processes are stable, measured, and actively refined. The organisation learns from operations and adapts.

**AI you build and operate:**
AI systems operate autonomously within defined boundaries. Continuous learning loops refine controls. Behavioural assurance through [Objective Intent Specifications](../maso/controls/objective-intent.md). PACE resilience ensures graceful degradation. Circuit breakers are tested and auditable. Full OWASP coverage validated through regular adversarial testing. The full three-layer architecture operates at scale with quantified effectiveness.

**Cloud AI platforms:**
Platform security is policy-driven and automated. Configuration is continuously validated against organisational standards. New platform capabilities (model updates, new safety features) are evaluated and adopted through a defined process. Multi-cloud AI governance is consistent across providers.

**Copilots and productivity AI:**
Governance is automated and embedded in daily workflows. Policy enforcement is automatic. Data classification is comprehensive and continuously validated. AI usage is a managed capability with clear value metrics, risk metrics, and governance metrics that drive decisions.

**Data management:**
Fully automated governance. Every dataset version is traceable with full lineage. Automated anomaly detection flags suspicious data before it reaches models. RAG data sources are continuously validated with embedding drift monitoring and confidence scoring. Fewer than 5% of organisations are at this level today.

**Monitoring and incident response:**
Predictive and self-optimising. AI-assisted monitoring of AI systems. Behavioural drift detection, anomaly scoring, semantic drift analysis across multi-agent systems. Incidents are largely prevented through predictive controls. When they occur, response is near-instant with automated remediation and full root cause analysis.

**AI vs. non-AI security balance:** ~20:80 for operational tasks. AI handles volume, speed, and pattern detection at machine speed. Humans focus entirely on governance, policy, strategic oversight, and novel situations.

## The Real Maturity Gap

**The gap is not capability. It is operational discipline.** 95%+ of enterprises are on cloud platforms. 50% use GenAI services through them. The platforms provide security controls. The question is whether organisations configure them, monitor them, and act on what they find.

The data is well-sourced:

- **99% of cloud security failures** are the customer's fault, primarily misconfigurations (Gartner, corroborated by CSA, Thales, breach reports)
- **Only 26%** of organisations use cloud security posture management tools
- **SOC teams review only 49%** of alerts they should on a typical day (IBM)
- **One-third of security teams** admit to ignoring alerts due to false positives (CSA)
- **43% of SOC teams** occasionally or frequently turn off alerts entirely
- **194 days** average time to identify a breach

For AI specifically, Azure is the only major platform that ships content safety filters on by default. AWS Bedrock requires full manual configuration. GCP Vertex AI has narrow always-on filters (CSAM, PII) but the main harm categories are off by default.

The maturity question for most organisations is not "do we have the tools?" It is:

1. **Do you know what AI is running in your environment?** ([The Visibility Problem](../insights/the-visibility-problem.md))
2. **Have you configured the controls your platform provides?**
3. **Are you reading the logs?**
4. **Do you act on what you find?**

For AI you build and operate: have you implemented the [three-layer defence](../ARCHITECTURE.md), scaled controls to [risk tiers](../core/risk-tiers.md), and tested [PACE resilience](../PACE-RESILIENCE.md)?

## The Balance Between AI and Non-AI Solutions

A mature organisation layers AI capabilities on top of strong traditional foundations. Access controls, encryption, network segmentation, DLP, SIEM, secure coding practices remain essential at every level. The shift is augmentation, not replacement:

| Level | Traditional security | AI-assisted security | Human role |
|-------|---------------------|---------------------|------------|
| 1 | Foundation (often incomplete) | None | Everything |
| 2 | Solid basics, rule-based automation | Piloted, isolated | Plans, executes, reviews |
| 3 | Standardised, enforced | Embedded for specific functions | Supervises, decides, governs |
| 4 | Measured, optimised | Deeply integrated, data-driven | Focuses on exceptions, strategy |
| 5 | Policy-driven, automated | Autonomous within bounds | Governs, audits, handles novel cases |

## How the Transition Works

### Typical timelines

| Transition | Timeframe | What must happen |
|---|---|---|
| Level 1 to 2 | 3-6 months | Document processes, assign ownership, configure platform controls, establish basic monitoring |
| Level 2 to 3 | 12-21 months | Enterprise-wide standardisation, policy formalisation, AI governance function, Judge operations. **This is where most organisations stall.** |
| Level 3 to 4 | 12-24 months | Quantitative measurement infrastructure, AI integration into core workflows, data-driven decision making |
| Level 4 to 5 | 18-36 months | Cultural shift toward AI trust, robust governance, continuous improvement loops, predictive controls |

These align with the [progression timelines](progression.md) already in the framework: 2-3 years from first deployment to autonomous AI. The reason is the same: operational maturity cannot be compressed below the time it takes to actually operate systems and encounter real problems.

### What blocks transitions

- **70% of organisations** lack optimised AI governance; 40% have none at all
- **Fragmented ownership:** CIOs control AI security in 29% of organisations; CISOs only 14.5%
- **Siloed teams:** Data scientists and security teams operate in separate worlds
- **Skills shortage:** Cybersecurity workforce gap of 3.5 million; AI security specialists extremely scarce
- **Alert fatigue:** Average enterprise runs 45 tools. SOC teams are overwhelmed before AI monitoring adds to the load

### What accelerates transitions

- **Governance maturity** is the strongest single indicator of AI security readiness (Cloud Security Alliance)
- **Existing ISO 27001 certification** accelerates ISO 42001 compliance by up to 40%
- **Standardised platforms** (the principle behind [Platform and Patterns](platform-and-patterns.md)): every system on the same infrastructure inherits the same controls
- **Dedicated AI leadership:** 91% of high-maturity organisations have appointed dedicated AI leaders
- **Starting with the Fast Lane:** Low-risk deployments build capability without high-stakes pressure

## Data Management as a Gate

All data management maturity models (DAMA-DMBOK, DCAM, CMMI DMM, ISO 8000, Gartner) converge: **organisations below Level 3 in data management lack the foundation for meaningful AI security controls.**

**AI you build and operate:** Without data lineage, poisoning detection is impossible. Without classification, access controls are arbitrary. Level 3 data management is the minimum for systematic AI data governance.

**Copilots and productivity AI:** Copilots retrieve from your organisational data. If classification is poor, they surface sensitive information to the wrong users. Only 30% of organisations classify data effectively. AI amplifies this gap by making data retrieval effortless.

**AI coding tools:** The concern is output, not input. AI-generated code may introduce insecure patterns, hallucinated dependencies, or licence-contaminated snippets. The question is whether your review processes catch these.

Key data dimensions that mature across levels:

| Dimension | Level 1 | Level 3 | Level 5 |
|-----------|---------|---------|---------|
| **Training data quality** | Unvetted sourcing | Formal quality gates, validated pipelines | Automated validation, statistical controls |
| **Data lineage** | Non-existent | Source-to-model tracking | Full provenance chains, rapid poisoning isolation |
| **RAG integrity** | Unclassified, unmonitored | Defined quality and access policies | Continuous embedding drift monitoring, confidence scoring |
| **Data incident handling** | Accidental discovery | Defined response procedures, post-mortems | Predictive prevention, automated remediation |

## MASO and Maturity

The [MASO framework](../maso/README.md) secures multi-agent AI systems, whether built from scratch or deployed on a platform (LangGraph, AutoGen, CrewAI, AWS Bedrock Agents).

**Level 1-2:** MASO is a reference architecture. The ten [control domains](../maso/README.md) provide the vocabulary for multi-agent security before you implement formal controls.

**Level 3:** MASO becomes operational. [Tier 1 (Supervised)](../maso/implementation/tier-1-supervised.md) applies: all agent actions require human approval, communication is logged, monitoring is periodic.

**Level 4-5:** [Tier 2 (Managed)](../maso/implementation/tier-2-managed.md) and [Tier 3 (Autonomous)](../maso/implementation/tier-3-autonomous.md) apply. Agents operate autonomously within bounds, PACE resilience is fully operational, kill switches tested quarterly.

For cloud platform orchestration (Bedrock Agents, Azure AI Agent Service), the [integration guide](../maso/integration/integration-guide.md) maps MASO controls to platform capabilities. For custom systems, MASO provides both requirements and architectural patterns.

## Where Most Organisations Are

The data suggests most enterprises sit around Level 2, with significant variation by track:

| Track | Typical maturity | Why |
|-------|-----------------|-----|
| **Copilot/productivity AI** | Level 2-3 | Fast adoption (70% of Fortune 500 on M365 Copilot), governance catching up. Data classification is the bottleneck. |
| **Cloud AI platforms** | Level 2 | Controls available but inconsistently configured. 50% using GenAI services, fewer than half have standardised security configuration. |
| **Custom/internal AI** | Level 1-2 | Fewer than 5% of enterprises have custom AI in production. Most are piloting. |
| **Multi-agent/agentic AI** | Level 1 | 2% deployed at scale, 61% still exploring. Only 21% report a mature governance model for agents. |

76% of enterprise AI use cases are now purchased rather than built (Menlo Ventures 2025, up from 53% in 2024). The most impactful maturity improvements for most organisations are in tracks 2 and 3 (platform configuration and copilot governance), not track 1 (building custom AI).

For organisations building custom AI or deploying agents, the maturity path follows the [progression model](progression.md): Fast Lane, then Tier 1, then Tier 2, then Tier 3 only if genuinely needed.

## A Note on Statistics

The AI security market generates a lot of alarming numbers. Some are well-sourced. Some are vendor propaganda designed to sell consulting or products. Here is how the commonly cited statistics hold up:

| Statistic | Source | Verdict |
|-----------|--------|---------|
| "90% not prepared for AI threats" | Accenture (2,286 executives surveyed) | Real data, but the 90% is Accenture's own segmentation. The underlying findings (22% have GenAI policies, 25% use encryption effectively) are more useful than the headline. |
| "97% of AI incidents lacked controls" | Often attributed to Palo Alto Networks | Likely a misquote. The actual Palo Alto report says 97% want to consolidate tooling, and 99% experienced at least one attack on AI systems. Use the real figures. |
| "60% of AI projects abandoned for data quality" | Gartner | A prediction, not measurement. Based on 248 respondents. But their earlier, more conservative prediction (30% abandoned) proved to understate reality. Directionally sound. |
| "76% buy, 24% build" | Menlo Ventures (495 U.S. AI decision-makers) | Solid methodology, transparent sample. U.S.-only, active AI users only. The year-over-year shift (from 53/47) is the significant finding. |
| Cloud misconfiguration data | CSA, Gartner, Thales, Fortinet | Well-corroborated across multiple independent sources. The most reliable data in this space. |

When building a business case for AI security maturity, use the specific, well-sourced data points. Avoid the headline numbers that were designed to alarm.

## Relationship to Progression

This maturity model complements the [progression path](progression.md) (No AI, Assisted, Supported, Supervised, Autonomous). Progression describes **what your AI systems can do**. Maturity describes **what your organisation can safely govern**.

An organisation at Level 2 attempting Tier 3 (Autonomous) AI is taking on risk it cannot manage. The maturity model provides the organisational context for why skipping steps is the most common strategic failure.

!!! info "References"
    - [CMMI Institute (ISACA)](https://cmmiinstitute.com/)
    - [NIST Cybersecurity Framework 2.0](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf)
    - [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
    - [NIST COSAiS: Control Overlays for Securing AI Systems](https://csrc.nist.gov/projects/cosais)
    - [DOE C2M2 v2.1](https://www.energy.gov/ceser/cybersecurity-capability-maturity-model-c2m2)
    - [CSA/Darktrace AI Maturity Model for Cybersecurity](https://www.darktrace.com/ai-maturity-model)
    - [OWASP AI Maturity Assessment v1.0](https://owasp.org/www-project-ai-maturity-assessment/)
    - [ISO/IEC 42001:2023](https://www.iso.org/standard/42001)
    - [CSA AI Controls Matrix](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix)
    - [DCAM v3.1 (EDM Council)](https://edmcouncil.org/frameworks/dcam/)
    - [Menlo Ventures: 2025 State of Generative AI in the Enterprise](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/)
    - [Flexera 2025 State of the Cloud](https://www.flexera.com/blog/finops/the-latest-cloud-computing-trends-flexera-2025-state-of-the-cloud-report/)
    - [Gartner AI Maturity Survey (June 2025)](https://www.gartner.com/en/newsroom/press-releases/2025-06-30-gartner-survey-finds-forty-five-percent-of-organizations-with-high-artificial-intelligence-maturity-keep-artificial-intelligence-projects-operational-for-at-least-three-years)
    - [IBM Cost of a Data Breach 2025](https://newsroom.ibm.com/)
    - [MITRE ATLAS](https://atlas.mitre.org/)
    - [AI Incident Database](https://incidentdatabase.ai/)
