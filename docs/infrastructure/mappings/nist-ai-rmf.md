---
description: "Mapping infrastructure controls to NIST AI RMF 1.0 subcategories across Govern, Map, Measure, and Manage functions, covering 51 of the framework's 72 subcategories."
---

# NIST AI Risk Management Framework (AI RMF 1.0) Mapping

> Maps infrastructure controls to NIST AI RMF 1.0 subcategories across all four functions: Govern, Map, Measure, and Manage.
>
> Part of the [AI Security Infrastructure Controls](../README.md) framework.
> Companion to [AI Runtime Security](https://github.com/JonathanCGill/airuntimesecurity.io).

## Scope and Limitations

The NIST AI RMF 1.0 contains **72 subcategories** across 19 categories and four functions. This mapping covers **51 of those 72 subcategories**, focusing on the subcategories where **technical infrastructure** controls make a direct contribution. The remaining 21 subcategories are primarily organisational in nature (workforce diversity, stakeholder engagement, environmental sustainability, decommissioning processes) and fall outside the scope of infrastructure controls. Many mapped subcategories also require organisational processes, policies, and governance structures beyond what infrastructure controls alone provide. Where a subcategory is primarily organisational, the mapping identifies supporting infrastructure controls and notes the organisational gap.

## GOVERN Function (14 subcategories)

The Govern function establishes the organisational context for AI risk management. Most Govern subcategories are primarily organisational; infrastructure controls provide the technical enforcement layer.

| Subcategory | Description | Infrastructure Controls | Notes |
|-------------|-------------|------------------------|-------|
| **GOVERN 1.1** | Legal and regulatory requirements identified | IR-01, IR-08 | Incident categories include regulatory triggers. IR integration connects AI events to compliance workflows. Requirement identification is organisational. |
| **GOVERN 1.2** | Trustworthy AI characteristics integrated | LOG-03, LOG-05, SUP-02 | Judge evaluation logging, drift detection, and risk assessment support trustworthiness measurement. Characteristic definition is organisational. |
| **GOVERN 1.3** | Processes for AI risk management established | SUP-02, IR-01 through IR-08 | Risk assessment and full incident response suite provide process infrastructure. Process design is organisational. |
| **GOVERN 1.4** | Risk management process ongoing | LOG-05, SUP-08, IR-07 | Drift detection, vulnerability monitoring, and post-incident review enable continuous risk management. |
| **GOVERN 1.5** | Organisational risk tolerance determined | TOOL-04, SESS-01, DEL-03 | Action classification, session limits, and delegation depth limits encode risk tolerance technically. Tolerance definition is organisational. |
| **GOVERN 1.6** | Mechanisms for ongoing risk feedback | LOG-10, IR-07, LOG-03 | SIEM correlation, post-incident review, and Judge evaluation logs provide feedback mechanisms. |
| **GOVERN 1.7** | Processes for AI risk management evaluated | IR-07, LOG-03 | Post-incident review and Judge meta-evaluation support process evaluation. |
| **GOVERN 2.1** | Roles and responsibilities defined | IAM-01, IAM-02, IAM-03, IAM-08 | Authentication, least privilege, plane separation, and access auditing enforce role boundaries. Role definition is organisational. |
| **GOVERN 2.2** | Personnel with AI risk knowledge | IAM-03, NET-06 | Control plane restrictions ensure only qualified personnel access AI configuration. Training/qualification is organisational. |
| **GOVERN 2.3** | Executive leadership oversight | IAM-05, IR-06, NET-06 | Human approval routing, communication protocols, and control plane protection support executive oversight. Governance structure is organisational. |
| **GOVERN 3.1** | Decision-making processes documented | LOG-04, DEL-02, TOOL-06 | Agent chain logs, delegation audit trails, and tool invocation logs document AI decision-making. |
| **GOVERN 3.2** | Policies for third-party AI systems | SUP-01, SUP-02, SUP-05, SUP-08 | Full supply chain control suite enforces third-party policies. Policy creation is organisational. |
| **GOVERN 4.1** | Organisational practices for AI design | NET-01, IAM-04, SEC-01, DAT-02 | Zone architecture, tool constraints, credential isolation, and data minimisation are design practices enforced at infrastructure. |
| **GOVERN 4.2** | Measurable activities for risk management | LOG-01 through LOG-10 | Full logging suite provides measurable telemetry for all AI risk activities. |

## MAP Function (12 subcategories)

The Map function identifies AI system context, capabilities, and risks. Infrastructure controls support the technical aspects of context identification and risk characterisation.

| Subcategory | Description | Infrastructure Controls | Notes |
|-------------|-------------|------------------------|-------|
| **MAP 1.1** | Intended purpose documented | TOOL-01, SESS-03, SUP-02 | Tool manifests, session scope constraints, and risk assessment document intended purpose at the technical level. |
| **MAP 1.2** | Interdependencies mapped | SUP-07, DEL-01, DEL-02 | AI-BOM, delegation permission models, and chain audit trails map technical interdependencies. |
| **MAP 1.3** | AI system benefits and costs assessed | SUP-02, TOOL-04 | Risk assessment and action classification inform benefit/cost analysis. Assessment methodology is organisational. |
| **MAP 1.5** | Organisational risk tolerance applied | SESS-01, DEL-03, TOOL-05, SAND-04 | Session limits, delegation depth, rate limits, and resource limits encode tolerance technically. |
| **MAP 1.6** | System requirements understood | NET-01, IAM-01 through IAM-08, DAT-01 through DAT-08 | Network architecture, IAM controls, and data protection controls define system requirements. |
| **MAP 2.1** | AI system categorised for risk | SUP-02, TOOL-04, IR-01 | Risk assessment, action classification, and incident categories support risk categorisation. |
| **MAP 2.2** | Stakeholders identified | IR-06, DEL-05 | Communication protocols and user identity propagation support stakeholder identification. Identification process is organisational. |
| **MAP 2.3** | Scientific integrity of AI | SUP-01, SUP-03, SUP-04 | Provenance, data integrity, and training pipeline security support scientific integrity of AI components. |
| **MAP 3.1** | AI risks identified | SUP-02, IR-01, LOG-06, SUP-08 | Risk assessment, incident categories, injection detection, and vulnerability monitoring support risk identification. |
| **MAP 3.2** | AI system risks along lifecycle | SUP-04, SUP-08, LOG-05, IR-07 | Pipeline security, vulnerability monitoring, drift detection, and post-incident review cover lifecycle risks. |
| **MAP 3.3** | AI risk management integrated with enterprise | IR-08, LOG-10 | Enterprise IR integration and SIEM correlation connect AI risk to enterprise risk management. |
| **MAP 3.5** | AI risks documented | IR-01, SUP-02, SUP-07 | Incident categories, risk assessments, and AI-BOM provide risk documentation infrastructure. |

## MEASURE Function (13 subcategories)

The Measure function quantifies AI risks and evaluates AI systems against requirements. Infrastructure controls provide the measurement infrastructure.

| Subcategory | Description | Infrastructure Controls | Notes |
|-------------|-------------|------------------------|-------|
| **MEASURE 1.1** | Approaches for measurement identified | LOG-01 through LOG-10, LOG-05 | Full logging suite and drift detection provide measurement approaches. Metric selection is organisational. |
| **MEASURE 1.2** | Measurement methods for risk appropriate | LOG-03, LOG-05, SUP-02 | Judge evaluation, drift detection, and risk assessment support appropriate measurement selection. |
| **MEASURE 1.3** | Internal and external assessment conducted | SUP-02, IR-07, LOG-03 | Risk assessment, post-incident review, and Judge evaluation support assessment processes. |
| **MEASURE 2.1** | AI system evaluated for valid and reliable outputs | LOG-01, LOG-03, LOG-05 | Model I/O logging, Judge evaluation, and drift detection measure output validity and reliability. |
| **MEASURE 2.2** | AI system evaluated for safety | LOG-02, LOG-06, SUP-06, NET-02 | Guardrail decision logging, injection detection, safety model integrity, and bypass prevention measure safety. |
| **MEASURE 2.3** | AI system evaluated for fairness | LOG-01, LOG-03, DAT-03 | I/O logging, Judge evaluation, and PII detection provide data for fairness evaluation. Fairness criteria are organisational. |
| **MEASURE 2.5** | AI system evaluated for privacy | DAT-01 through DAT-08, SEC-01, LOG-09 | Full data protection suite, credential isolation, and log redaction support privacy evaluation. |
| **MEASURE 2.6** | AI system evaluated for security | All 80 controls | The entire infrastructure controls framework supports security evaluation. |
| **MEASURE 2.7** | AI system evaluated for resilience | IR-03, IR-04, SESS-05, SAND-01 | Containment, rollback, session cleanup, and sandbox isolation support resilience evaluation. |
| **MEASURE 2.8** | AI system evaluated for interpretability | LOG-01, LOG-04, DEL-02, TOOL-06 | I/O logging, agent chain reconstruction, delegation trails, and tool logs support interpretability. |
| **MEASURE 2.9** | AI system performance monitored in production | LOG-01, LOG-03, LOG-05, LOG-10, NET-08 | I/O logging, Judge evaluation, drift detection, SIEM correlation, and cross-zone monitoring support production monitoring. |
| **MEASURE 3.1** | Monitoring approaches deployed | LOG-01 through LOG-10, IR-02 | Full logging suite and detection triggers provide monitoring deployment. |
| **MEASURE 3.2** | Risk tracking processes in place | SUP-08, LOG-05, IR-07, SUP-07 | Vulnerability monitoring, drift detection, post-incident review, and AI-BOM support risk tracking. |

## MANAGE Function (12 subcategories)

The Manage function addresses risk treatment and response. Infrastructure controls provide the technical response and mitigation capabilities.

| Subcategory | Description | Infrastructure Controls | Notes |
|-------------|-------------|------------------------|-------|
| **MANAGE 1.1** | Risk treatment plans defined | IR-03, IR-04, SUP-08 | Containment procedures, rollback capability, and vulnerability remediation tracking support treatment plans. Plan design is organisational. |
| **MANAGE 1.2** | Treatments proportionate to risk | TOOL-04, SESS-01, DEL-03 | Action classification, session limits, and delegation depth limits enable proportionate treatment. Risk-tiered controls throughout the framework support proportionality. |
| **MANAGE 1.3** | Risks and benefits communicated | IR-06, LOG-10 | Communication protocols and SIEM correlation support risk communication. Communication strategy is organisational. |
| **MANAGE 1.4** | AI risk treatment monitored | LOG-05, SUP-08, IR-07 | Drift detection, vulnerability monitoring, and post-incident review monitor treatment effectiveness. |
| **MANAGE 2.1** | Resources allocated for risk management | SAND-04, SESS-01, IAM-02 | Resource limits, session boundaries, and least privilege allocate resources within risk boundaries. Budget allocation is organisational. |
| **MANAGE 2.2** | Mechanisms for mitigating emerging risks | SUP-08, IR-02, LOG-06, IR-04 | Vulnerability monitoring, detection triggers, injection detection, and hot-reload capability support emerging risk mitigation. |
| **MANAGE 2.3** | Procedures for responding to AI incidents | IR-01 through IR-08 | Full incident response control suite provides response procedures. |
| **MANAGE 2.4** | Mechanisms for escalation | IAM-05, IR-06, LOG-10 | Human approval routing, communication protocols, and SIEM correlation support escalation. |
| **MANAGE 3.1** | AI risks documented and monitored | SUP-07, LOG-05, SUP-08, IR-07 | AI-BOM, drift detection, vulnerability monitoring, and post-incident review document and monitor risks. |
| **MANAGE 3.2** | Pre-deployment risk management reviewed | SUP-01, SUP-02, SUP-06, TOOL-01 | Provenance verification, risk assessment, safety model integrity, and manifest validation support pre-deployment review. |
| **MANAGE 4.1** | Post-deployment monitoring in place | LOG-01 through LOG-10, NET-08, IR-02 | Full logging suite, cross-zone monitoring, and detection triggers provide post-deployment monitoring. |
| **MANAGE 4.2** | Mechanisms for decommissioning | SESS-05, SAND-05, IR-04, DAT-07 | Session cleanup, ephemeral environments, rollback capability, and retention management support decommissioning. |

## Coverage Summary

| Function | Total Subcategories | Mapped Here | Primary Infrastructure Coverage |
|----------|--------------------|--------------------|-------------------------------|
| **Govern** | 21 | 14 | IAM, logging, supply chain, incident response, network controls |
| **Map** | 16 | 12 | Supply chain, session/delegation, logging, incident response |
| **Measure** | 22 | 13 | All logging controls, data protection, supply chain, agentic controls |
| **Manage** | 13 | 12 | Incident response, supply chain, logging, agentic controls |
| **Total** | **72** | **51** | |

**Unmapped subcategories** fall into categories that are primarily organisational: workforce diversity and equity (GOVERN 3, GOVERN 5), stakeholder engagement and feedback (MAP 4, MAP 5, MEASURE 4), environmental sustainability (MEASURE 2.12), decommissioning processes (GOVERN 1.7), and human subject protection (MEASURE 2.2). These require organisational processes, not infrastructure controls.

**Note:** Many mapped subcategories also have organisational dimensions beyond what infrastructure controls address. This mapping identifies the infrastructure controls that support these subcategories technically, but organisational implementation is required for full framework alignment.

