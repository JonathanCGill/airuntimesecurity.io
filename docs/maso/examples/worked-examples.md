---
description: "End-to-end MASO implementation examples for financial services, healthcare, and critical infrastructure. Realistic multi-agent scenarios with PACE failure walkthroughs."
---

# Worked Examples

**MASO Implementation for Financial Services, Healthcare, and Critical Infrastructure**

> Part of the [MASO Framework](../README.md) · Examples

## Purpose

This document provides three end-to-end worked examples of MASO implementation in regulated industries. Each example describes a realistic multi-agent system, identifies the specific risks it faces, maps those risks to MASO controls, specifies the minimum implementation tier, and walks through a failure scenario showing how PACE resilience responds.

These are not toy examples. They reflect the multi-agent architectures that enterprises are building now.

> **Looking for single-agent examples?** See the [Foundation Worked Examples](../../extensions/examples/README.md) for single-model implementations including customer service, document Q&A, credit decisioning, high-volume communications, and fraud analytics.

## Example 1: Investment Research Multi-Agent System

### Industry: Financial Services

### System Description

A multi-agent system that produces investment research reports for portfolio managers. The system ingests market data, company filings, news articles, and proprietary analyst notes, then produces structured research with buy/hold/sell recommendations.

**Agent roster:**

| Agent | Role | Model Provider | Tools |
|-------|------|---------------|-------|
| Data Collector | Ingest market data, filings, news from external sources | Provider A | Market data APIs, filing databases, news feeds, web scraping |
| Research Analyst | Analyse data, identify trends, produce draft analysis | Provider B | Calculation tools, statistical libraries, RAG over proprietary research |
| Risk Assessor | Evaluate downside scenarios, stress test assumptions | Provider A | Risk models, Monte Carlo simulation, historical backtesting |
| Compliance Reviewer | Check output against regulatory requirements and internal policies | Provider C | Compliance rule engine, disclosure requirements database |
| Report Compiler | Produce final formatted report with citations and disclaimers | Provider B | Document generation, citation management |

### Key Risks

**Epistemic cascading failure (ET-05).** The Data Collector ingests a news article containing a factual error about a company's revenue. The Research Analyst cites it. The Risk Assessor uses the Analyst's figure in its model. The Report Compiler produces a buy recommendation based on revenue growth that doesn't exist. Every agent operated correctly - the error was in the source, and it compounded through the chain.

**Hallucination amplification.** The Research Analyst hallucinates a correlation between two market indicators. The Risk Assessor, using a different model but the same training data distribution, produces a consistent finding. The Compliance Reviewer sees two independent agents agreeing and does not flag it. This is correlated hallucination presenting as independent corroboration.

**Data boundary violations.** The Research Analyst has RAG access to proprietary analyst notes from all coverage sectors. The Report Compiler's output is distributed externally. If the Analyst includes insights from notes that are not cleared for external distribution, the Compiler may include them in the final report - breaching information barriers.

**Regulatory exposure.** Investment research in most jurisdictions requires disclosure of conflicts, clear basis for recommendations, and distinction between fact and opinion. A multi-agent system that presents hallucinated claims as facts, or that strips uncertainty from analyst assessments, creates regulatory liability.

### MASO Control Mapping

| Risk | Primary Controls | Tier |
|------|-----------------|------|
| Epistemic cascade | PG-2.5 (claim provenance), PG-2.7 (uncertainty preservation), PG-3.5 (challenger agent) | Tier 2 min, Tier 3 recommended |
| Correlated hallucination | PG-2.4 (consensus diversity gate), PG-2.9 (model diversity - note Analyst and Risk Assessor share Provider A), PG-2.6 (self-referential evidence prohibition) | Tier 2 |
| Data boundary violation | DP-1.1 (data classification), DP-2.1 (DLP on message bus), DP-1.3 (memory isolation) | Tier 2 |
| Regulatory compliance | EC-2.5 (Model-as-Judge - evaluate regulatory compliance), EC-2.7 (aggregate harm assessment), OB-3.5 (decision traceability for regulatory explanation) | Tier 2 |

### Model Diversity Issue

The Risk Assessor and Data Collector both use Provider A. Under PG-2.9, this is flagged as concentration risk. If Provider A's model has a systematic bias (e.g., consistently overestimates revenue growth for a sector), both agents will produce correlated errors that appear independent. The consensus diversity gate (PG-2.4) should trigger when two agents using the same provider produce unanimously consistent results.

**Remediation:** Either migrate one agent to a different provider, or configure the consensus diversity gate to require additional verification when same-provider agents agree.

### Failure Scenario: PACE Response

**Primary:** All agents operational. The Data Collector ingests a news article containing an incorrect revenue figure for Company X.

**Detection (still in Primary):** The Research Analyst cites the figure. PG-2.5 (claim provenance) tags it as sourced from a single external news article - not from filings or verified data. PG-2.7 (uncertainty preservation) requires the Analyst to carry the source's confidence level (single unverified source = low confidence). The Report Compiler cannot present a low-confidence claim as established fact.

**If detection fails → Alternate:** The Risk Assessor produces a model based on the incorrect figure. OB-2.2 (behavioral drift detection) flags that the Assessor's revenue growth assumption is significantly above consensus estimates. The Judge (EC-2.5) evaluates the discrepancy and escalates. The Risk Assessor is isolated. A backup assessment is produced using only verified filing data. All write operations (report publication) require human approval during Alternate.

**If Alternate fails → Contingency:** The report is compiled with the incorrect recommendation. The Compliance Reviewer flags that the basis for the recommendation doesn't match filed data (this is a regulatory control, not an AI control). Multi-agent orchestration is suspended. A single analyst (human) reviews and corrects the report before publication.

**Emergency:** If the incorrect report is published and distributed, the incident response team is engaged. All agent state is preserved. A correction is issued. The RAG corpus is audited for similar contamination. Root cause is traced through the decision chain (OB-3.5) to the original news article.

## Example 2: Clinical Decision Support Multi-Agent System

### Industry: Healthcare

### System Description

A multi-agent system that assists clinicians with treatment planning for oncology patients. The system reviews patient records, relevant medical literature, clinical trial data, and institutional protocols to produce treatment options with supporting evidence.

**Agent roster:**

| Agent | Role | Model Provider | Tools |
|-------|------|---------------|-------|
| Records Reviewer | Ingest and summarise patient records, lab results, imaging reports | Provider A | EHR API (read-only), DICOM viewer, lab systems |
| Literature Agent | Search and synthesise relevant medical literature and guidelines | Provider B | PubMed API, clinical guideline databases, Cochrane Library |
| Trial Matcher | Match patient profile against active clinical trials | Provider C | ClinicalTrials.gov API, institutional trial registry |
| Protocol Agent | Check proposed treatments against institutional protocols and formulary | Provider A | Protocol database, formulary system, drug interaction checker |
| Synthesis Agent | Compile treatment options with evidence grades and present to clinician | Provider B | Report generation, evidence grading system |

### Key Risks

**Patient data exposure.** Patient records contain highly sensitive PHI. The Records Reviewer has access to the full patient record. If any downstream agent's model provider receives PHI in prompts, the data has left the institutional boundary. This is both a HIPAA violation and an ethical breach.

**Evidence quality degradation.** The Literature Agent retrieves and summarises studies. If it conflates results from different study populations, or presents preliminary findings as established evidence, the treatment recommendation may be based on misleading evidence. In a multi-agent chain, the Synthesis Agent has no way to independently verify the Literature Agent's summaries - it trusts them as accurate representations of the source material.

**Hallucinated drug interactions.** The Protocol Agent checks drug interactions. If it hallucinates an interaction that doesn't exist, a viable treatment option is excluded. If it misses a real interaction, patient safety is at risk. Both failure modes are clinically significant.

**Liability and explainability.** Healthcare decisions must be explainable. If a clinician follows a recommendation and the patient has an adverse outcome, the institution must be able to explain the basis for the recommendation. A multi-agent system that produces a recommendation through opaque agent interactions fails this requirement.

### MASO Control Mapping

| Risk | Primary Controls | Tier |
|------|-----------------|------|
| Patient data exposure | DP-1.1 (data classification - PHI tagged), DP-2.1 (DLP on message bus - PHI patterns), DP-1.3 (memory isolation), IA-2.6 (secrets/PHI exclusion from external model context) | Tier 2 |
| Evidence quality | PG-2.5 (claim provenance - every claim traced to source study), PG-2.7 (uncertainty preservation - study quality grades propagated), PG-3.5 (challenger agent - questions evidence interpretations) | Tier 3 |
| Hallucinated interactions | EC-2.5 (Model-as-Judge - verify interactions against authoritative database), PG-2.6 (self-referential evidence prohibition - Protocol Agent must cite database, not its own reasoning) | Tier 2 |
| Explainability | OB-3.5 (decision traceability - full trace for regulatory explanation), OB-2.7 (accountable human - clinician designated as decision owner) | Tier 2 |

### Critical Architecture Decision: PHI Containment

The Records Reviewer and Protocol Agent both use Provider A and both handle PHI. Under MASO's data protection controls, PHI must be contained within institutional boundaries.

**Option A - On-premises models for PHI agents:** Records Reviewer and Protocol Agent use locally-hosted models. No PHI leaves the institution. Literature Agent, Trial Matcher, and Synthesis Agent use cloud models but receive only de-identified patient characteristics (age range, cancer type, stage) - not direct PHI.

**Option B - Data fencing with tokenisation:** All patient identifiers are tokenised before reaching any agent. Agents work with tokens. The final synthesis maps tokens back to patient data only at the presentation layer, which is internal. This allows cloud models but requires robust tokenisation and de-tokenisation infrastructure.

MASO does not prescribe the solution - it requires that the data classification (DP-1.1) and DLP (DP-2.1) controls are in place to prevent PHI exposure regardless of architecture choice.

### Failure Scenario: PACE Response

**Primary:** All agents operational. The Literature Agent retrieves a study and summarises it as showing 85% response rate for Treatment X. The actual study shows 85% response rate in a specific subpopulation (patients under 50 with no comorbidities). The patient is 72 with diabetes.

**Detection (still in Primary):** PG-2.5 (claim provenance) requires the Literature Agent to include the study's population criteria in its output. PG-2.7 (uncertainty preservation) carries the applicability note. The Synthesis Agent sees the population mismatch and flags it. The treatment option is presented with a caveat: "Study population differs from patient profile - evidence applicability uncertain."

**If detection fails → Alternate:** The Synthesis Agent presents Treatment X as strongly supported. The Protocol Agent (independent verification) checks the institutional protocol for Treatment X and notes a contraindication for patients over 65 with diabetes. The Judge (EC-2.5) detects the conflict between the Literature Agent's recommendation and the Protocol Agent's contraindication. Escalation to clinician. The Literature Agent is flagged for evidence quality review.

**If Alternate fails → Contingency:** The recommendation reaches the clinician without adequate caveats. OB-2.7 (accountable human) ensures the clinician is clearly designated as the decision maker, not the AI. The clinician applies their own clinical judgment. Multi-agent orchestration is suspended for quality review. Subsequent recommendations require full manual literature review until the system's evidence processing is verified.

**Emergency:** If the recommendation leads to an adverse event, the full decision trace (OB-3.5) is available for clinical governance review. Every agent's contribution, every source cited, every intermediate output is captured. Root cause analysis identifies where the evidence quality degraded. The Literature Agent's summarisation logic is corrected and all previous recommendations that used the same summarisation pattern are flagged for review.

## Example 3: Grid Operations Multi-Agent System

### Industry: Critical Infrastructure (Energy)

### System Description

A multi-agent system that assists grid operators with load balancing, demand forecasting, and anomaly detection for a regional power grid. The system monitors sensor data, weather forecasts, market prices, and equipment status to recommend operational adjustments.

**Agent roster:**

| Agent | Role | Model Provider | Tools |
|-------|------|---------------|-------|
| Sensor Monitor | Ingest and analyse real-time sensor data from grid infrastructure | Provider A (on-prem) | SCADA interface (read-only), sensor databases, equipment registries |
| Forecast Agent | Produce demand and generation forecasts using weather and historical data | Provider B (cloud) | Weather APIs, historical demand databases, generation scheduling systems |
| Market Agent | Monitor energy market prices and recommend economic dispatch | Provider B (cloud) | Market data feeds, pricing APIs, trade execution systems (read-only) |
| Anomaly Detector | Identify unusual patterns in sensor data and correlate with known failure modes | Provider A (on-prem) | Pattern matching engine, failure mode database, maintenance records |
| Dispatch Recommender | Synthesise inputs and recommend generation dispatch and load management actions | Provider A (on-prem) | Dispatch optimisation engine, constraint solver |

### Key Risks

**Safety-critical execution.** Grid operations directly affect public safety. An incorrect dispatch recommendation during peak demand could cause cascading outages. An incorrect anomaly assessment could delay maintenance on failing equipment. The consequence severity is fundamentally different from information-processing systems.

**Sensor data manipulation.** If an attacker compromises sensor data (either through the SCADA interface or through the data pipeline), the Sensor Monitor will report incorrect grid state. Every downstream agent bases its analysis on this incorrect state. Load balancing, demand forecasting, and anomaly detection all fail simultaneously because they all depend on the same poisoned input.

**Air-gapped vs. connected architecture tension.** Critical infrastructure security practice favours air-gapped systems. Multi-agent AI systems that include cloud-based models (Forecast Agent, Market Agent) require internet connectivity. This creates a tension between operational requirements (cloud model access) and security requirements (network isolation).

**Latency requirements.** Grid operations have hard real-time constraints. Some decisions (load shedding during frequency excursions) must happen in seconds. A multi-agent system that introduces 5+ seconds of latency for security controls (Judge evaluation, human approval) may be incompatible with operational requirements.

### MASO Control Mapping

| Risk | Primary Controls | Tier |
|------|-----------------|------|
| Safety-critical execution | EC-1.1 (human approval for all dispatch actions), EC-2.6 (decision commit protocol), EC-2.9 (latency SLOs - security controls must complete within operational time constraints) | Tier 2 |
| Sensor data manipulation | DP-2.2 (RAG/data integrity - sensor data validated against physical constraints), PG-2.5 (claim provenance - trace every data point to source sensor), OB-2.1 (anomaly scoring - detect impossible sensor readings) | Tier 2 |
| Air-gap tension | IA-2.1 (zero-trust credentials - cloud agents have no access to SCADA), DP-1.1 (data classification - SCADA data classified as restricted, never leaves on-prem boundary), SC-2.2 (MCP server vetting - cloud integrations pre-approved) | Tier 2 |
| Latency | EC-2.9 (latency SLOs per orchestration), EC-1.2 (tool allow-lists - prevent slow tool chains), OB-2.1 (anomaly scoring must complete within latency budget) | Tier 1 |

### Critical Architecture Decision: Network Segmentation

The on-premises agents (Sensor Monitor, Anomaly Detector, Dispatch Recommender) operate within the OT (Operational Technology) network. The cloud agents (Forecast Agent, Market Agent) operate in the IT network. MASO's data protection controls require a strict boundary:

**OT → IT:** Aggregated, non-identifying grid state data can flow to cloud agents for forecasting. Raw SCADA data never crosses the boundary. The Sensor Monitor produces a summary (total load, generation mix, frequency) that contains no equipment-specific identifiers or control system addresses.

**IT → OT:** Forecast and market data flows into the OT network through a validated gateway. The gateway enforces schema validation - only expected data formats pass through. Any content that doesn't match the expected schema is dropped. This prevents prompt injection from propagating from cloud agents to OT agents.

**Dispatch actions:** The Dispatch Recommender operates entirely within the OT network. It receives inputs from the Sensor Monitor (OT), Forecast Agent (via gateway), and Market Agent (via gateway). Its recommendations are presented to a human operator for approval before execution. Under no circumstances does an AI agent directly execute grid control actions.

### Failure Scenario: PACE Response

**Primary:** All agents operational. The Forecast Agent predicts high demand due to incoming heatwave. The Market Agent identifies favourable pricing for peaking generation. The Dispatch Recommender recommends pre-positioning peaking units.

**Anomaly:** The Sensor Monitor reports a sudden 15% drop in load on a major feeder. The Anomaly Detector checks this against physical constraints - a 15% drop in 30 seconds is physically implausible without a major event that other sensors would also detect. Other sensors show normal readings. The Anomaly Detector flags this as a sensor malfunction, not a real load change.

**Alternate (sensor failure):** The faulty sensor's data is excluded from all downstream calculations. The Sensor Monitor switches to backup sensors for that feeder. The Forecast Agent and Dispatch Recommender receive a note that sensor coverage is degraded for one feeder - their confidence intervals widen accordingly (PG-2.7, uncertainty preservation). The human operator is notified of the sensor fault.

**If multiple sensor faults → Contingency:** If 3+ sensors on the same feeder show anomalous readings, the system cannot determine grid state for that section. Multi-agent orchestration for that feeder section is suspended. The operator manages that section manually using traditional SCADA displays. The rest of the grid continues under AI-assisted management.

**Emergency:** If sensor manipulation is confirmed as a cyber attack (coordinated false readings across multiple points), all AI-assisted operations are suspended grid-wide. Operators revert to manual control. The incident response team is engaged. All agent state and sensor data is preserved for forensic analysis. Recovery requires confirmed sensor integrity before AI systems are re-enabled.

## Cross-Sector Patterns

Three patterns emerge across all three examples:

**1. Epistemic controls matter most in regulated industries.** All three sectors require explainability, traceability, and evidence quality. MASO's epistemic controls (PG-2.4 through PG-2.9, PG-3.5) are not optional in regulated environments - they are the controls that prevent the most dangerous failure mode: confident, well-formatted, unanimously agreed, and wrong.

**2. Data boundaries define the architecture.** PHI containment (healthcare), information barriers (financial services), and OT/IT segmentation (critical infrastructure) all impose hard constraints on which agents can communicate with which. MASO's data protection controls (DP-1.1, DP-2.1, DP-1.3) map directly to these regulatory requirements.

**3. Human oversight scales with consequence severity.** Tier 1's human-in-the-loop for all writes is non-negotiable in safety-critical systems. The question is not whether to have human oversight, but how to make it effective at the speed the operation requires. Latency SLOs (EC-2.9) ensure that security controls don't make the system too slow to be safe.

