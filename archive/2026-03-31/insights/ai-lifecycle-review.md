---
description: "A systematic review of the AIRS framework against standard AI lifecycle phases, identifying where runtime security connects, where it leads, and where deliberate boundaries create gaps that adopters must fill."
---

# Review: The Framework Against the AI Lifecycle

*The AIRS framework secures AI systems at runtime. But AI systems have a lifecycle that extends far beyond runtime. This review maps the framework against the complete AI lifecycle to identify where it covers, where it consciously scopes out, and where the gaps create risk for adopters who assume full coverage.*

## Why This Review Matters

The framework makes a clear scope claim: it secures AI systems at runtime. It does not claim to be a complete AI governance framework, a model development methodology, or a regulatory compliance programme. That honesty is a strength.

But adopters don't deploy the framework in isolation. They deploy it within organisations that must govern the entire AI lifecycle, from initial concept through retirement. Standards like NIST AI RMF, ISO 42001, the EU AI Act, and NIST IR 8596 all define lifecycle obligations that extend well beyond runtime. When an organisation adopts the AIRS framework as its primary AI security reference, the gaps between "what the framework covers" and "what the lifecycle requires" become operational risks.

This review maps those gaps systematically so that adopters know exactly what they're getting and what they still need to build.

## The Standard AI Lifecycle

Drawing from NIST AI RMF, ISO 42001 (Clause 8), and the EU AI Act, the AI lifecycle has seven broadly recognised phases:

| Phase | Description | Key Activities |
|-------|-------------|----------------|
| **1. Concept & Alignment** | Problem identification, business justification, feasibility | Business case, stakeholder alignment, alternative evaluation |
| **2. Design & Definition** | Use case specification, requirements, architecture | Requirements, risk assessment, data needs, human oversight design |
| **3. Data & Development** | Data acquisition, model training, system building | Dataset curation, training, fine-tuning, integration |
| **4. Verification & Validation** | Testing, evaluation, pre-deployment assurance | Red-teaming, bias testing, conformity assessment, documentation |
| **5. Deployment** | Production release, operational handover | Gradual rollout, control activation, operator training |
| **6. Operation & Monitoring** | Steady-state production with continuous oversight | Runtime controls, drift detection, incident response, governance |
| **7. Retirement** | End-of-life, decommissioning, data disposition | Shutdown, data retention, lessons learned, registry update |

## Coverage Assessment

### Phase 1: Concept & Alignment (Strong)

The framework's strategy section provides substantive coverage here, which is notable for a runtime-focused framework.

**What's covered:**
- [Business Alignment](../strategy/business-alignment.md) forces honest evaluation of whether the problem justifies investment
- [Use Case Filter](../strategy/use-case-filter.md) asks "is AI the right tool?" before committing to AI (the framework's "first control")
- [From Idea to Production](../strategy/idea-to-production.md) Stage 1 defines the business case structure
- [The Thread](../strategy/the-thread.md) connects strategy decisions to downstream control requirements

**What's missing:**
- **Stakeholder impact assessment.** The EU AI Act requires Fundamental Rights Impact Assessment (FRIA) for high-risk systems. The framework doesn't address impact on affected individuals or communities at the concept stage.
- **Ethical review gates.** ISO 42001 Clause 5.2 expects an AI policy that considers "ethical aspects." The framework addresses security and safety but not ethics review as a lifecycle gate.
- **Portfolio-level governance.** No guidance on how organisations prioritise across multiple AI initiatives competing for governance resources.

**Assessment: 7/10.** Stronger than expected for a runtime framework. The concept-phase coverage is pragmatic and operational. The gaps are in areas the framework consciously defers to organisational governance.

### Phase 2: Design & Definition (Strong)

This is where the framework genuinely excels. The connection between use case definition and control requirements is the framework's signature contribution.

**What's covered:**
- [Use Case Definition](../strategy/use-case-definition.md) provides a structured ten-question methodology that directly drives risk classification
- [Risk Tiers](../core/risk-tiers.md) translates use case attributes into a four-tier classification with six scoring dimensions
- [Control Selection Guide](../extensions/technical/control-selection-guide.md) maps tiers to specific controls
- [Data Reality](../strategy/data-reality.md) assesses data feasibility across five dimensions
- [Human Factors](../strategy/human-factors.md) evaluates operational readiness
- [Platform and Patterns](../strategy/platform-and-patterns.md) addresses architecture decisions
- [Threat Model Template](../extensions/templates/threat-model-template.md) provides structured threat analysis

**What's missing:**
- **Intended use and limitation documentation.** NIST IR 8596 (Gap G1) and the EU AI Act (Article 13) require explicit documentation of what the system is designed to do and its known limitations. The framework captures this implicitly through risk tier classification but doesn't require a standalone intended-use artefact.
- **Fairness and bias assessment at design time.** NIST AI RMF MEASURE 2.3 requires fairness evaluation. The framework provides data collection infrastructure but not fairness criteria definition.
- **Accessibility and inclusivity requirements.** Not addressed. The framework focuses on security properties, not user-facing design requirements.

**Assessment: 8/10.** The ten-question use case definition driving risk classification and control selection is genuinely well-engineered. The gap is that security-focused design doesn't address the full scope of "responsible AI" design that standards now expect.

### Phase 3: Data & Development (Acknowledged Gap)

This is the framework's most significant lifecycle gap, and it's intentional. The framework is explicitly a runtime security framework, not a model development framework.

**What's covered:**
- [Data Reality](../strategy/data-reality.md) evaluates data feasibility (existence, accessibility, quality, legality, usability), but as a pre-commitment gate, not as development governance
- [Supply Chain Controls](../maso/controls/supply-chain.md) address model provenance and AIBOM
- [Build & Test](../strategy/idea-to-production.md) (Stage 6) covers implementing controls alongside the system

**What's missing:**
- **Training data governance.** EU AI Act Article 10 requires that training, validation, and testing datasets meet quality criteria ("relevant, representative, free of errors, complete, with appropriate statistical properties"). The framework doesn't govern dataset curation, labelling, or bias detection in training data.
- **Model training security.** Data poisoning during training, adversarial training methodologies, and secure training infrastructure are out of scope.
- **Fine-tuning governance.** As organisations increasingly fine-tune foundation models, the governance of fine-tuning data, process, and validation is a lifecycle requirement the framework doesn't address.
- **Development environment security.** Secure development practices for AI systems (NIST SP 800-218A focus) beyond what's captured in supply chain controls.
- **Version control and experiment tracking.** Model versioning, experiment reproducibility, and development audit trails are standard development-phase requirements.

**Assessment: 3/10.** This is a known, intentional scope boundary. The framework explicitly states that model training and development are out of scope. However, adopters in regulated environments (EU AI Act, financial services) cannot treat this phase as optional. The gap must be filled by complementary frameworks or organisational processes.

### Phase 4: Verification & Validation (Moderate)

The framework provides strong testing guidance for runtime controls but limited coverage of pre-deployment model evaluation.

**What's covered:**
- [Testing Guidance](../extensions/templates/testing-guidance.md) covers control verification
- [From Idea to Production](../strategy/idea-to-production.md) Stage 6 includes a pre-deployment checklist
- [Judge Assurance](../core/judge-assurance.md) addresses Judge model validation
- [Red Team Playbook](../maso/red-team/red-team-playbook.md) provides 13 structured adversarial test scenarios
- [100-Agent Stress Test](../maso/stress-test/100-agent-stress-test-overview.md) covers multi-agent system validation

**What's missing:**
- **Conformity assessment.** EU AI Act Articles 40–49 require conformity assessment before high-risk AI can be placed on the market. The framework has no controls for this regulatory gate.
- **Pre-market technical documentation.** Article 11 requires documentation "before placing on the market"; the framework addresses documentation as ongoing but not as a pre-deployment regulatory artefact.
- **Bias and fairness testing.** Pre-deployment evaluation of model outputs for demographic bias, fairness across protected characteristics, and disparate impact analysis.
- **Model performance benchmarking.** Systematic evaluation against established benchmarks before production deployment.
- **Independent validation.** Third-party or independent internal validation of model performance, not just control effectiveness.

**Assessment: 5/10.** The control verification coverage is solid. The gap is in model-level evaluation: the framework tests whether controls work, but not whether the model itself is fit for purpose. This is consistent with its runtime focus but creates a lifecycle gap for regulated adopters.

### Phase 5: Deployment (Strong)

The framework provides detailed, tier-appropriate deployment guidance.

**What's covered:**
- [From Idea to Production](../strategy/idea-to-production.md) Stage 7 defines deployment patterns by tier (canary, staged, phased)
- First-30-days monitoring plan with specific activities, owners, and timelines
- PACE activation during deployment (feature flags, fallback states)
- [Quick Start](../QUICK_START.md) provides 30-minute implementation path
- Gradual rollout as an "absorb" control for blast radius containment

**What's missing:**
- **EU database registration.** Article 51 requires registration of high-risk AI systems; not addressed.
- **Operator training and certification.** While [Human Factors](../strategy/human-factors.md) identifies the skills gap, the deployment phase doesn't include structured operator training as a gate.
- **User notification and transparency.** EU AI Act Article 13 requires informing users they're interacting with AI. The framework doesn't address deployment-time transparency obligations.

**Assessment: 8/10.** Deployment guidance is practical, specific, and risk-proportionate. The tier-based rollout patterns and first-30-days plans are operationally mature. Gaps are primarily regulatory procedural requirements.

### Phase 6: Operation & Monitoring (Exceptional)

This is the framework's core domain and it shows. Runtime operation is covered with depth, specificity, and operational maturity that few other frameworks match.

**What's covered:**
- **Three-layer defence model** (Guardrails → Judge → Human Oversight) with circuit breaker
- **PACE resilience methodology** (Primary → Alternate → Contingency → Emergency)
- **128+ MASO controls** for multi-agent systems across 7 domains
- **80+ foundation controls** for single-agent systems
- Comprehensive [incident response playbook](../extensions/templates/ai-incident-playbook.md)
- [SOC integration](../extensions/technical/soc-integration.md) with content packs
- [Anomaly detection operations](../extensions/technical/anomaly-detection-ops.md)
- [Runtime telemetry](../extensions/technical/runtime-telemetry-reference.md)
- Continuous governance with specific metrics, frequencies, and owners
- Judge calibration, guardrail tuning, and drift detection
- [Ongoing Governance](../strategy/idea-to-production.md) (Stage 8) with continuous, periodic, and event-driven activities

**What's missing:**
- **Post-market surveillance as a regulatory obligation.** Distinct from operational monitoring, the EU AI Act (Article 61) requires systematic post-market surveillance procedures and cooperation with market surveillance authorities. The framework's monitoring is technically comprehensive but not framed as regulatory post-market surveillance.
- **Production validation data.** As [MATURITY.md](../MATURITY.md) honestly acknowledges, no organisation has deployed the framework end-to-end and reported operational results. False positive rates, Judge accuracy baselines, and PACE failover performance are designed but untested at scale.

**Assessment: 9/10.** This is the framework's reason for existence and it delivers. The three-layer pattern, PACE resilience, and operational governance model represent genuine contributions to the field. The only meaningful gap is regulatory framing of post-market obligations.

### Phase 7: Retirement (Minimal)

Retirement is addressed but not developed in depth.

**What's covered:**
- [From Idea to Production](../strategy/idea-to-production.md) Stage 8 includes a 7-step retirement process
- Retirement triggers defined (business case invalid, risk exceeds appetite, better solution exists, regulatory change, operational capacity lost)
- Data retention obligations mentioned
- Registry status update to "Retired"

**What's missing:**
- **Model decommissioning security.** Secure deletion of model artefacts, weights, and fine-tuning data. For self-hosted models, secure disposal of training infrastructure.
- **Downstream dependency management.** When a retired AI system fed other systems (especially in multi-agent architectures), the cascade effects of retirement.
- **Knowledge transfer and preservation.** Operational knowledge about the system's behaviour, edge cases, and control tuning that may inform future systems.
- **Regulatory notification.** Some regulations require notifying authorities when high-risk AI systems are withdrawn from service.
- **User transition planning.** Structured migration of users to alternative solutions, not just "users notified with timeline."

**Assessment: 4/10.** The framework acknowledges retirement but treats it as an afterthought. For an ecosystem that emphasises lifecycle governance, the end-of-life phase deserves the same operational rigour as deployment.

## Cross-Cutting Gaps

Beyond phase-specific gaps, several themes emerge across the lifecycle:

### 1. Training and Awareness

NIST AI RMF (GOVERN 2.2), ISO 42001 (Clause 7.3), and NIST IR 8596 (Gap G4) all require AI-specific training programmes. The framework identifies skills requirements in [Human Factors](../strategy/human-factors.md) but doesn't provide training curricula, competency frameworks, or awareness programme guidance. This is flagged as "organisational practice" throughout the standards mappings.

### 2. Fairness and Ethics

The framework is explicitly a security framework, not an ethics framework. But modern AI lifecycle standards (NIST AI RMF MEASURE 2.3, ISO 42001 Annex A.8, EU AI Act Article 10) embed fairness and non-discrimination as lifecycle requirements. Organisations relying solely on the AIRS framework will have a fairness gap.

### 3. Contractual and Procurement Governance

NIST IR 8596 (Gap G2) and ISO 42001 expect contractual terms with AI suppliers. The framework's supply chain controls specify what to require from providers but lack template contract language or procurement assessment frameworks. The [Vendor Assessment Questionnaire](../extensions/templates/vendor-assessment-questionnaire.md) partially addresses this.

### 4. Regulatory Procedural Requirements

The EU AI Act includes procedural requirements (conformity assessment, database registration, post-market surveillance reporting) that are administrative, not technical. The framework maps technical controls to regulatory intent but doesn't address the procedural compliance workflow.

## Summary Scorecard

| Lifecycle Phase | Coverage | Rating | Key Gap |
|----------------|----------|--------|---------|
| 1. Concept & Alignment | Strong | 7/10 | Stakeholder impact assessment, ethical review |
| 2. Design & Definition | Strong | 8/10 | Fairness criteria, intended-use artefact |
| 3. Data & Development | Acknowledged gap | 3/10 | Training data governance, fine-tuning, dev security |
| 4. Verification & Validation | Moderate | 5/10 | Conformity assessment, model-level evaluation |
| 5. Deployment | Strong | 8/10 | Regulatory registration, operator training gates |
| 6. Operation & Monitoring | Exceptional | 9/10 | Post-market surveillance framing |
| 7. Retirement | Minimal | 4/10 | Decommissioning security, dependency management |

**Weighted average (by typical risk exposure): 7.0/10**

The weighting reflects that Phases 5–6 represent the majority of an AI system's operational life and risk exposure, where the framework excels. However, regulated adopters will experience the Phase 3–4 gaps as material compliance risks.

## What This Means for Adopters

### The framework is sufficient when:
- Your organisation has separate model development governance (or uses only managed API services)
- You're deploying commercial AI models, not training your own
- Your regulatory environment focuses on operational safety (runtime behaviour, human oversight, incident response)
- You pair it with complementary frameworks for pre-deployment phases

### The framework needs supplementation when:
- You train or fine-tune models (add training data governance)
- You're subject to the EU AI Act's conformity assessment requirements (add pre-market compliance workflow)
- Your organisation expects a single framework to cover the entire AI lifecycle (add Phases 3, 4, and 7 depth)
- Fairness and ethics obligations are part of your governance requirements (add responsible AI framework)

### Recommended complementary frameworks:
- **NIST AI RMF**: for the Govern and Map functions that require organisational (not technical) implementation
- **ISO 42001**: for AI management system structure, especially Clauses 4–7 (context, leadership, support, planning)
- **NIST SP 800-218A**: for secure software development practices applied to AI
- **Responsible AI frameworks** (e.g., Microsoft RAI, Google AI Principles): for fairness, ethics, and societal impact assessment

## Conclusion

The AIRS framework is honest about its scope: runtime security for AI systems in production. Within that scope, it is exceptionally thorough: the three-layer defence model, PACE resilience, and operational governance guidance represent genuine advances in practical AI security.

The lifecycle review reveals that the framework has also grown beyond its original scope, with the strategy section providing substantive coverage of Phases 1–2 and 5 that many "complete" AI governance frameworks lack. The eight-stage lifecycle in [From Idea to Production](../strategy/idea-to-production.md) and the narrative continuity in [The Thread](../strategy/the-thread.md) demonstrate awareness that runtime security cannot exist in isolation.

The remaining gaps (training data governance, conformity assessment, fairness evaluation, and retirement depth) are real but manageable. They're manageable because the framework is clear about where it stops. An adopter who knows the boundaries can fill them. An adopter who assumes full lifecycle coverage will discover the gaps in production, or in a regulatory review.

The honest assessment: **this framework covers approximately 70% of the AI lifecycle, and covers that 70% better than almost anything else available.** The remaining 30% requires complementary governance that the framework's standards mappings help identify but don't implement.
