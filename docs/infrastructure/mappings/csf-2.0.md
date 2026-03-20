---
description: "Mapping 80 infrastructure controls to NIST Cybersecurity Framework 2.0 Functions, Categories, and Subcategories with three-layer pattern alignment."
---

# NIST Cybersecurity Framework 2.0 Mapping

**How the framework's 80 infrastructure controls map to NIST CSF 2.0 Functions, Categories, and Subcategories.**

## Relationship

This framework provides AI-specific infrastructure controls that implement CSF 2.0 outcomes at the deployment layer. CSF 2.0 defines *what* cybersecurity outcomes to achieve. This framework defines *how* to achieve them for AI systems in production.

The mapping below covers the CSF 2.0 "Secure" focus area as described in NIST IR 8596 (Cyber AI Profile). The "Defend" (using AI for cybersecurity) and "Thwart" (defending against AI-enabled attacks) focus areas are outside this framework's scope.

### Three-Layer Pattern → CSF Functions

| Framework Layer | Primary CSF Function | Role |
| --- | --- | --- |
| **Guardrails** | PROTECT (PR) | Preventive controls - block known-bad inputs and outputs |
| **Model-as-Judge** | DETECT (DE) | Detective controls - evaluate outputs against policy |
| **Human Oversight** | GOVERN (GV) | Decision authority - humans accountable for high-risk outcomes |

The infrastructure controls that enforce these layers map across all six CSF Functions.

## Mapping by CSF Function

### GOVERN (GV)

The GOVERN Function addresses organisational context, risk management strategy, roles and responsibilities, policy, oversight, and supply chain risk management. This framework's risk tiers, governance model, and supply chain controls map here.

| CSF Subcategory | Description | Framework Domain | AI-Specific Notes |
| --- | --- | --- | --- |
| **GV.OC-01** | Organisational mission is understood and informs cybersecurity risk management | Risk Tiers | Risk tier classification (Tier 1–3, Agentic) determines control requirements based on organisational context and use case criticality |
| **GV.OC-02** | Internal and external stakeholders are understood, and their needs and expectations regarding cybersecurity risk management are understood and considered | Risk Tiers | Risk tiers account for regulatory exposure, data sensitivity, and autonomy level - all stakeholder-driven considerations |
| **GV.OC-03** | Legal, regulatory, and contractual requirements regarding cybersecurity - including privacy and civil liberties obligations - are understood and managed | Risk Tiers, Logging & Observability (LO) | AI-specific regulations (EU AI Act, sector-specific guidance) drive tier classification. LO controls support audit and compliance evidence |
| **GV.RM-01** | Risk management objectives are established and expressed as statements that the implementation of policies and procedures address | Risk Tiers | Risk tier definitions establish acceptable risk levels for each AI deployment category |
| **GV.RM-02** | Risk appetite and risk tolerance statements are established, communicated, and maintained | Risk Tiers | Tier boundaries define tolerance: Tier 1 accepts higher residual risk; Tier 3 requires defence-in-depth with all three layers |
| **GV.RM-07** | Strategic opportunities (i.e., positive risks) are characterised and are included in the organisation's cybersecurity risk discussions | - | Out of scope. This framework addresses risk mitigation, not opportunity identification |
| **GV.RR-01** | Organisational leadership is responsible and accountable for cybersecurity risk and fosters a culture that is risk-aware, ethical, and continually improving | Human Oversight layer | Human Oversight layer requires defined accountability for AI system decisions. Escalation paths ensure leadership engagement at appropriate risk levels |
| **GV.RR-02** | Roles, responsibilities, and authorities related to cybersecurity risk management are established, communicated, understood, and enforced | Human Oversight layer, Delegation Chains (DC) | DC controls define who can approve what actions. Human Oversight layer specifies escalation triggers and decision authority |
| **GV.RR-04** | Cybersecurity is included in human resources practices | - | Organisational practice, not infrastructure control. Framework assumes this is in place |
| **GV.PO-01** | Policy for managing cybersecurity risks is established based on organisational context, cybersecurity strategy, and priorities and is communicated and enforced | Controls (core), Risk Tiers | Framework provides the policy implementation mechanism - controls enforce policy at infrastructure layer rather than relying on procedural compliance |
| **GV.PO-02** | Policy for managing cybersecurity risks is reviewed, updated, communicated, and enforced to reflect changes in requirements, threats, technology, and organisational mission | Incident Response (IR) | IR post-incident review (IR-07, IR-08) feeds back into control and policy updates |
| **GV.OV-01** | Cybersecurity risk management strategy outcomes are reviewed to inform and adjust strategy and direction | Logging & Observability (LO) | LO controls provide the data needed for strategy review - behavioral drift, anomaly trends, Judge override rates |
| **GV.OV-02** | The cybersecurity risk management strategy is reviewed and adjusted to ensure coverage of organisational requirements and risks | Risk Tiers | Periodic tier reassessment as AI capabilities and threat landscape evolve |
| **GV.OV-03** | Organisational cybersecurity risk management is improved based on lessons learned | Incident Response (IR) | IR-07 (Post-incident review) and IR-08 (Lessons learned) drive continuous improvement |
| **GV.SC-01** | A cybersecurity supply chain risk management program, strategy, objectives, policies, and processes are established and agreed to by organisational stakeholders | Supply Chain (SC) | SC controls address AI-specific supply chain: model provenance, component integrity, dependency management |
| **GV.SC-02** | Cybersecurity roles and responsibilities for suppliers, customers, and partners are established, communicated, and coordinated internally and externally | Supply Chain (SC) | Defines responsibilities for model providers vs. deployers - who patches, who monitors, who responds |
| **GV.SC-03** | Cybersecurity supply chain risk management is integrated into cybersecurity and enterprise risk management, risk assessment, and improvement processes | Supply Chain (SC), Risk Tiers | Supply chain risk (model provenance, training data integrity) factors into tier classification |
| **GV.SC-04** | Suppliers are known and prioritised by criticality | Supply Chain (SC) | SC-05 (Asset inventory) tracks which models, from which providers, power which systems |
| **GV.SC-05** | Requirements to address cybersecurity risks in supply chains are established, prioritised, and integrated into contracts and other types of agreements with suppliers and other relevant third parties | Supply Chain (SC) | SC controls specify what to require from model providers: integrity verification, provenance data, vulnerability disclosure |
| **GV.SC-06** | Planning and due diligence are conducted to reduce risks before entering into formal supplier or other third-party relationships | Supply Chain (SC) | SC-01 (Provenance verification) and SC-02 (Integrity checking) apply before deploying any acquired model |
| **GV.SC-07** | The risks posed by a supplier, their products and services, and other third parties are understood, recorded, prioritised, assessed, responded to, and monitored over the relationship lifecycle | Supply Chain (SC), Logging & Observability (LO) | Ongoing monitoring of model provider risk: API changes, security incidents, model deprecation |
| **GV.SC-09** | Supply chain security practices are integrated into cybersecurity and enterprise risk management programs, and their performance is monitored throughout the technology product and service life cycle | Supply Chain (SC) | SC-06 (SBOM/dependency tracking) provides lifecycle visibility |
| **GV.SC-10** | Cybersecurity supply chain risk management plans include provisions for activities that occur after the conclusion of a partnership or service agreement | Supply Chain (SC) | Model retirement, data deletion, credential revocation when changing providers |

### IDENTIFY (ID)

The IDENTIFY Function covers asset management, risk assessment, and improvement. This framework's risk classification and asset tracking controls map here.

| CSF Subcategory | Description | Framework Domain | AI-Specific Notes |
| --- | --- | --- | --- |
| **ID.AM-01** | Inventories of hardware managed by the organisation are maintained | Network & Segmentation (NS) | GPU infrastructure, inference endpoints, and edge devices hosting AI systems |
| **ID.AM-02** | Inventories of software, services, and systems managed by the organisation are maintained | Supply Chain (SC) | SC-05 (Asset inventory) covers model inventory: which models, versions, configurations are deployed where |
| **ID.AM-03** | Representations of the organisation's authorised network communication and internal and external network data flows are maintained | Network & Segmentation (NS) | NS controls map data flows between AI components: client → guardrails → model → Judge → response path |
| **ID.AM-05** | Assets are prioritised based on classification, criticality, resources, and impact on the mission | Risk Tiers | Risk tier classification determines control requirements proportionate to asset criticality |
| **ID.AM-07** | Inventories of data and corresponding metadata for designated data types are maintained | Data Protection (DP) | DP controls address AI-specific data: training data lineage, prompt/response logs, context window contents, RAG source data |
| **ID.AM-08** | Systems, hardware, software, services, and data are managed throughout their life cycles | Supply Chain (SC), Incident Response (IR) | Model lifecycle management: deployment, monitoring, patching, retirement. IR controls cover end-of-life decommissioning |
| **ID.RA-01** | Vulnerabilities in assets are identified, validated, and recorded | Logging & Observability (LO) | AI-specific vulnerabilities: prompt injection susceptibility, jailbreak vectors, data leakage paths. LO controls detect these in production |
| **ID.RA-02** | Cyber threat intelligence is received from information sharing forums and sources | - | Organisational practice. Framework assumes threat intelligence feeds into risk tier and control decisions |
| **ID.RA-03** | Internal and external threats to the organisation are identified and recorded | Risk Tiers, threat model templates | Threat models in [Templates](../../extensions/templates/) address AI-specific threats: adversarial inputs, model manipulation, supply chain compromise |
| **ID.RA-04** | Potential impacts and likelihoods of threats exploiting vulnerabilities are identified and recorded | Risk Tiers | Risk tier classification incorporates impact assessment: what happens when the AI system fails or is compromised |
| **ID.RA-05** | Threats, vulnerabilities, likelihoods, and impacts are used to understand inherent risk and inform risk response prioritisation | Risk Tiers | Tier-based control selection: higher risk → more layers → more controls |
| **ID.RA-06** | Risk responses are chosen, prioritised, planned, tracked, and communicated | Risk Tiers, Controls (core) | Three-layer pattern is the risk response architecture. Control selection driven by tier |
| **ID.RA-07** | Changes and exceptions are managed, assessed for risk impact, recorded, and tracked | Logging & Observability (LO) | LO controls track configuration changes, model updates, guardrail modifications |
| **ID.RA-09** | The authenticity and integrity of hardware and software are assessed prior to acquisition and use | Supply Chain (SC) | SC-01 (Provenance verification), SC-02 (Integrity checking), SC-04 (Build pipeline integrity) |
| **ID.RA-10** | Critical suppliers are assessed prior to acquisition | Supply Chain (SC) | Model provider assessment: security practices, incident history, vulnerability disclosure policies |
| **ID.IM-01** | Improvements are identified from evaluations | Incident Response (IR), Logging & Observability (LO) | IR post-incident reviews and LO trend analysis identify control improvements |
| **ID.IM-02** | Improvements are identified from security tests and exercises, including those done in coordination with suppliers and relevant third parties | Logging & Observability (LO) | Red-team testing results, Judge accuracy metrics, guardrail bypass rates feed improvement cycle |
| **ID.IM-03** | Improvements are identified from execution of operational processes, procedures, and activities | Logging & Observability (LO) | Operational metrics: false positive rates, escalation volumes, human override patterns |
| **ID.IM-04** | Incident response plans and other cybersecurity plans that affect operations are established, communicated, maintained, and improved | Incident Response (IR) | IR controls provide AI-specific incident playbooks covering model failure, data leakage, adversarial attack scenarios |

### PROTECT (PR)

The PROTECT Function covers identity management, access control, awareness and training, data security, platform security, and infrastructure resilience. The majority of this framework's infrastructure controls map here.

| CSF Subcategory | Description | Framework Domain | AI-Specific Notes |
| --- | --- | --- | --- |
| **PR.AA-01** | Identities and credentials for authorised users, services, and hardware are managed by the organisation | Identity & Access Management (IA), Secrets & Credentials (SK) | IA controls manage who/what can invoke AI systems. SK controls manage API keys, model access tokens, service credentials |
| **PR.AA-02** | Identities are proofed and bound to credentials based on the context of interactions | Identity & Access Management (IA) | Authentication context for AI system access: user identity, calling service identity, agent identity |
| **PR.AA-03** | Users, services, and hardware are authenticated | Identity & Access Management (IA) | IA controls enforce authentication for model endpoints, tool access, and human oversight interfaces |
| **PR.AA-04** | Identity assertions are protected, conveyed, and verified | Identity & Access Management (IA), Delegation Chains (DC) | DC controls verify identity assertions across agent delegation chains - who authorised this agent to act? |
| **PR.AA-05** | Access permissions, entitlements, and authorisations are defined in a policy, managed, enforced, and reviewed, and incorporate the principles of least privilege and separation of duties | Identity & Access Management (IA), Tool Access (TA), Session & Scope (SS) | IA: role-based access to AI systems. TA: least-privilege tool permissions for agents. SS: scoped context access per session |
| **PR.AA-06** | Physical access to assets is managed, monitored, and enforced commensurate with risk | - | Physical security is out of scope for this framework. Relevant for self-hosted GPU infrastructure |
| **PR.AT-01** | Personnel are provided with awareness and training so that they possess the knowledge and skills to perform general tasks with cybersecurity risks in mind | - | Organisational practice. Framework provides the controls; training on their use is an operational concern |
| **PR.AT-02** | Individuals in specialised roles are provided with awareness and training so that they possess the knowledge and skills to perform relevant tasks with cybersecurity risks in mind | - | Organisational practice. Human Oversight layer effectiveness depends on trained reviewers |
| **PR.DS-01** | The confidentiality, integrity, and availability of data-at-rest are protected | Data Protection (DP) | DP controls protect stored AI data: model weights, training data, prompt/response logs, RAG knowledge bases |
| **PR.DS-02** | The confidentiality, integrity, and availability of data-in-transit are protected | Data Protection (DP), Network & Segmentation (NS) | NS controls enforce encrypted communication between AI components. DP controls protect data crossing trust boundaries |
| **PR.DS-10** | The confidentiality, integrity, and availability of data-in-use are protected | Data Protection (DP), Session & Scope (SS) | **Key AI subcategory.** SS controls limit what data is accessible within an AI session context window. DP controls prevent data leakage through model outputs. Context window contents are data-in-use |
| **PR.PS-01** | Configuration management practices are established and applied | Network & Segmentation (NS), Sandbox Patterns (SB) | Infrastructure-as-code for AI deployment configurations. SB controls define sandbox boundaries. NS controls define network topology |
| **PR.PS-02** | Software is maintained, replaced, and removed commensurate with risk | Supply Chain (SC) | Model version management: patching, updating, retiring models as vulnerabilities are discovered or newer versions released |
| **PR.PS-03** | Hardware is maintained, replaced, and removed commensurate with risk | - | Physical infrastructure management is out of scope |
| **PR.PS-04** | Log records are generated and made available for continuous monitoring | Logging & Observability (LO) | **Key AI subcategory.** LO controls generate AI-specific logs: prompts, responses, guardrail decisions, Judge evaluations, human override actions, tool invocations, token usage |
| **PR.PS-05** | Installation and execution of unauthorised software is prevented | Sandbox Patterns (SB), Tool Access (TA) | SB controls restrict agent execution environments. TA controls limit which tools agents can invoke. Prevents unauthorised code execution by AI systems |
| **PR.PS-06** | Secure software development practices are integrated, and their performance is monitored throughout the software development life cycle | Supply Chain (SC) | SC-03 (Dependency scanning), SC-04 (Build pipeline integrity) for AI application code. For model development practices, see NIST SP 800-218A |
| **PR.IR-01** | Networks and environments are protected from unauthorised logical access and usage | Network & Segmentation (NS) | NS controls segment AI infrastructure: model endpoints isolated from general network, guardrail services in dedicated segments, Judge layer independently hosted |
| **PR.IR-02** | The organisation's technology assets are protected from environmental threats | - | Physical/environmental protection is out of scope |
| **PR.IR-03** | Mechanisms are implemented to achieve resilience requirements in normal and adverse situations | Network & Segmentation (NS), Incident Response (IR) | Circuit breakers, fallback models, graceful degradation patterns. IR controls define when to activate these mechanisms |
| **PR.IR-04** | Adequate resource capacity to ensure availability is maintained | - | Capacity planning for inference infrastructure is an operational concern, not a security control |

### DETECT (DE)

The DETECT Function covers continuous monitoring and adverse event analysis. This framework's Logging & Observability controls and the LLM-as-Judge layer map directly here.

| CSF Subcategory | Description | Framework Domain | AI-Specific Notes |
| --- | --- | --- | --- |
| **DE.CM-01** | Networks and network services are monitored to find potentially adverse events | Network & Segmentation (NS), Logging & Observability (LO) | Monitor AI network segments for anomalous traffic: unusual API call patterns, data exfiltration attempts, unexpected model-to-model communication |
| **DE.CM-02** | The physical environment is monitored to find potentially adverse events | - | Out of scope |
| **DE.CM-03** | Personnel activity and technology usage are monitored to find potentially adverse events | Logging & Observability (LO) | LO controls track user interactions with AI systems: prompt patterns, access frequency, data retrieval behavior |
| **DE.CM-06** | External service provider activities and services are monitored to find potentially adverse events | Supply Chain (SC), Logging & Observability (LO) | Monitor model provider APIs for: latency changes, behavior drift, unexpected response patterns that may indicate compromise |
| **DE.CM-09** | Computing hardware and software, runtime environments, and their data are monitored to find potentially adverse events | Logging & Observability (LO), Model-as-Judge layer | **Primary mapping for the Judge layer.** LO provides the telemetry. The Judge evaluates model outputs against policy criteria. Together they detect: harmful outputs, policy violations, behavioral anomalies, prompt injection attempts, data leakage |
| **DE.AE-02** | Potentially adverse events are analysed to better understand associated activities | Logging & Observability (LO), Model-as-Judge layer | Judge evaluation provides structured analysis of why an output was flagged. LO correlation identifies attack patterns across sessions |
| **DE.AE-03** | Information is correlated from multiple sources | Logging & Observability (LO) | LO controls correlate: guardrail decisions + Judge evaluations + human override patterns + model telemetry to identify systemic issues |
| **DE.AE-04** | The estimated impact and scope of adverse events are understood | Logging & Observability (LO), Risk Tiers | Impact assessment informed by risk tier: Tier 3 incident has different blast radius than Tier 1 |
| **DE.AE-06** | Information on adverse events is provided to authorised staff and tools | Logging & Observability (LO), Incident Response (IR) | LO-05 (Alert generation) routes to appropriate responders based on severity. IR controls define escalation paths |
| **DE.AE-07** | Cyber threat intelligence and other contextual information are integrated into the analysis | - | Organisational practice. Framework assumes threat intelligence informs guardrail and Judge criteria |
| **DE.AE-08** | Incidents are declared when adverse events meet the defined incident criteria | Incident Response (IR) | IR controls define AI-specific incident declaration criteria: sustained guardrail bypass, Judge degradation, confirmed data leakage |

### RESPOND (RS)

The RESPOND Function covers incident management, analysis, mitigation, reporting, and communication. This framework's Incident Response controls map here.

| CSF Subcategory | Description | Framework Domain | AI-Specific Notes |
| --- | --- | --- | --- |
| **RS.MA-01** | The incident response plan is executed in coordination with relevant third parties once an incident is declared or detected | Incident Response (IR) | AI-specific playbooks for: model compromise, prompt injection campaigns, data exfiltration via model outputs, agent misbehavior |
| **RS.MA-02** | Incident reports are triaged and validated | Incident Response (IR), Logging & Observability (LO) | LO telemetry (prompts, responses, Judge decisions) provides evidence for triage. IR-02 (Severity classification) accounts for AI-specific impact factors |
| **RS.MA-03** | Incidents are categorised and prioritised | Incident Response (IR), Risk Tiers | Risk tier informs prioritisation: Tier 3 system compromise takes precedence |
| **RS.MA-04** | Incidents are escalated or elevated as needed | Incident Response (IR), Human Oversight layer | Human Oversight escalation paths activate during incidents. IR controls define when to escalate from automated response to human decision |
| **RS.MA-05** | The criteria for initiating incident recovery are applied | Incident Response (IR) | Recovery criteria account for AI-specific factors: model integrity verification before restoration, guardrail/Judge re-validation |
| **RS.AN-03** | Analysis is performed to determine what has taken place during an incident and the root cause of the incident | Incident Response (IR), Logging & Observability (LO) | Forensic analysis of AI incidents requires: prompt/response logs, guardrail decision logs, Judge evaluation records, model configuration state, tool invocation history |
| **RS.AN-06** | Actions performed during an investigation are recorded, and the records' integrity and provenance are preserved | Logging & Observability (LO) | LO controls ensure tamper-evident logging of all AI system interactions. Critical for post-incident forensics |
| **RS.AN-07** | Incident data and metadata are collected, and their integrity and provenance are preserved | Logging & Observability (LO) | LO-03 (Audit logging) captures AI-specific incident evidence with integrity protection |
| **RS.AN-08** | An incident's magnitude is estimated and validated | Incident Response (IR), Logging & Observability (LO) | Magnitude assessment for AI incidents: how many users affected, what data exposed, what decisions made based on compromised outputs |
| **RS.CO-02** | Internal and external stakeholders are notified of incidents | Incident Response (IR) | IR controls specify notification procedures including to model providers when provider-side issues are suspected |
| **RS.CO-03** | Information is shared with designated internal and external stakeholders | Incident Response (IR) | Responsible disclosure of AI-specific vulnerabilities to model providers and the broader community |
| **RS.MI-01** | Incidents are contained | Incident Response (IR), Network & Segmentation (NS), Tool Access (TA) | AI-specific containment: circuit breakers disable model endpoints, TA controls revoke agent tool access, NS controls isolate compromised segments, guardrail rules tightened |
| **RS.MI-02** | Incidents are eradicated | Incident Response (IR) | AI-specific eradication: model rollback, guardrail/Judge criteria reset, credential rotation for all AI service accounts, cache purge |

### RECOVER (RC)

The RECOVER Function covers recovery plan execution and communication. This framework's Incident Response controls address recovery for AI-specific scenarios.

| CSF Subcategory | Description | Framework Domain | AI-Specific Notes |
| --- | --- | --- | --- |
| **RC.RP-01** | The recovery portion of the incident response plan is executed once initiated from the incident response process | Incident Response (IR) | AI recovery includes: model re-deployment from verified source, guardrail/Judge re-validation, session state reset, confidence monitoring during ramp-up |
| **RC.RP-02** | Recovery actions are selected, scoped, and prioritised | Incident Response (IR), Risk Tiers | Risk tier determines recovery priority and sequence |
| **RC.RP-03** | The integrity of backups and other restoration assets is verified before using them for restoration | Supply Chain (SC), Data Protection (DP) | Verify model weights and configuration integrity before re-deployment. Validate backup guardrail/Judge configurations |
| **RC.RP-04** | Critical functions and cybersecurity risk management are considered to establish post-incident operational norms | Incident Response (IR) | Post-recovery monitoring: heightened logging, reduced autonomy, tighter guardrail thresholds until confidence restored |
| **RC.RP-05** | The integrity of restored assets is verified, stakeholders are informed, and normal operations are declared | Incident Response (IR), Logging & Observability (LO) | Behavioral validation of restored AI system: does it produce expected outputs? Judge evaluation rates normal? No residual compromise indicators? |
| **RC.RP-06** | The end of incident recovery is declared based on criteria, and incident-related documentation is completed | Incident Response (IR) | IR-07 (Post-incident review) includes AI-specific lessons: what controls failed, what was the attack vector, what detection worked |
| **RC.CO-03** | Recovery activities and progress in restoring operational capabilities are communicated to designated internal and external stakeholders | Incident Response (IR) | Stakeholder communication includes: model provider notification, regulatory reporting where required, user notification if AI decisions affected |
| **RC.CO-04** | Public updates on incident recovery are shared using approved methods and messaging | Incident Response (IR) | Organisational communication practice. Framework provides the forensic evidence; communications are an operational concern |

## Coverage Summary

### By CSF Function

| CSF Function | Subcategories with Framework Mapping | Primary Framework Domains |
| --- | --- | --- |
| **GOVERN** | 23 | Risk Tiers, Supply Chain, Human Oversight, Delegation Chains, Incident Response, Logging & Observability |
| **IDENTIFY** | 19 | Risk Tiers, Supply Chain, Logging & Observability, Data Protection, Network & Segmentation, Incident Response |
| **PROTECT** | 21 | Identity & Access Management, Data Protection, Network & Segmentation, Secrets & Credentials, Tool Access, Session & Scope, Sandbox Patterns, Supply Chain, Logging & Observability |
| **DETECT** | 11 | Logging & Observability, LLM-as-Judge layer, Network & Segmentation, Supply Chain, Incident Response |
| **RESPOND** | 13 | Incident Response, Logging & Observability, Network & Segmentation, Tool Access, Human Oversight |
| **RECOVER** | 8 | Incident Response, Supply Chain, Data Protection, Logging & Observability, Risk Tiers |

### By Framework Domain

| Domain (Controls) | Primary CSF Functions | Key Subcategories |
| --- | --- | --- |
| **Identity & Access Management** (8) | PR | PR.AA-01 through PR.AA-05 |
| **Logging & Observability** (10) | DE, RS, ID | DE.CM-09, DE.AE-02, DE.AE-03, PR.PS-04, RS.AN-03 |
| **Network & Segmentation** (8) | PR, DE | PR.IR-01, PR.DS-02, DE.CM-01, ID.AM-03 |
| **Data Protection** (8) | PR | PR.DS-01, PR.DS-02, PR.DS-10 |
| **Secrets & Credentials** (8) | PR | PR.AA-01 |
| **Supply Chain** (8) | GV, ID, PR | GV.SC-01 through GV.SC-10, ID.AM-02, PR.PS-02 |
| **Incident Response** (8) | RS, RC, GV | RS.MA-01 through RS.MA-05, RC.RP-01 through RC.RP-06, GV.OV-03 |
| **Tool Access** (6) | PR | PR.AA-05, PR.PS-05 |
| **Session & Scope** (5) | PR | PR.AA-05, PR.DS-10 |
| **Delegation Chains** (5) | GV, PR | GV.RR-02, PR.AA-04 |
| **Sandbox Patterns** (6) | PR | PR.PS-01, PR.PS-05, PR.IR-01 |

### Three-Layer Pattern

| Layer | CSF Functions | Key Subcategories |
| --- | --- | --- |
| **Guardrails** | PROTECT | PR.DS-10 (data-in-use), PR.AA-05 (access control), PR.PS-05 (unauthorised execution prevention) |
| **Model-as-Judge** | DETECT | DE.CM-09 (runtime monitoring), DE.AE-02 (event analysis), DE.AE-03 (correlation) |
| **Human Oversight** | GOVERN, RESPOND | GV.RR-01 (accountability), GV.RR-02 (roles/authorities), RS.MA-04 (escalation) |

## Subcategories Not Mapped

The following CSF 2.0 subcategory areas have no direct mapping to this framework's infrastructure controls. This is expected - the framework addresses AI deployment security, not full enterprise cybersecurity.

| CSF Area | Reason |
| --- | --- |
| Physical security (PR.AA-06, PR.IR-02, DE.CM-02) | Physical security is out of scope for an AI deployment controls framework |
| Awareness and training (PR.AT-01, PR.AT-02) | Organisational practice, not infrastructure control |
| Hardware maintenance (PR.PS-03) | Physical infrastructure management is out of scope |
| Capacity planning (PR.IR-04) | Operational concern, not security control |
| Positive risk / opportunity (GV.RM-07) | Framework addresses risk mitigation only |
| Threat intelligence integration (DE.AE-07) | Organisational practice; framework assumes it informs control decisions |

## Using This Mapping

**For organisations already running CSF 2.0:** Use this mapping to identify which CSF outcomes are addressed by this framework's AI-specific controls. Overlay the framework onto your existing CSF programme rather than replacing it.

**For CSF gap assessments:** This mapping shows where AI deployments introduce new control requirements within existing CSF subcategories. PR.DS-10 (data-in-use), DE.CM-09 (runtime monitoring), and the GV.SC supply chain subcategories are most significantly affected by AI.

**For audit and compliance:** The mapping provides traceability from this framework's 80 infrastructure controls to CSF 2.0 outcomes, supporting compliance evidence for organisations that report against CSF.

