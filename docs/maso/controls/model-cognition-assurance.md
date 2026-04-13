---
description: "MASO controls for assessing whether a model's internal reasoning aligns with its expressed outputs: activation-layer transparency, CoT integrity, reward hacking detection, third-party AI risk classification, and procurement attestation for regulated financial services."
---

# MASO Control Domain: Model Cognition Assurance

> Part of the [MASO Framework](../README.md) · Control Specifications
> Extends: [Observability](observability.md) · [Supply Chain](supply-chain.md) · [Privileged Agent Governance](privileged-agent-governance.md)
> Covers: Deceptive reasoning alignment · Reward hacking · CoT faithfulness · Activation-layer transparency · Third-party model risk classification · Vendor interpretability attestation

## Principle

Output-layer controls cannot detect misalignment that originates inside the model. A model can produce compliant outputs while pursuing internal objectives that diverge from its declared purpose. Chain-of-thought monitoring is necessary but not sufficient: CoT can be unfaithful to the model's actual reasoning process. Where activation-layer interpretability access is available, it must be used. Where it is unavailable, compensating controls and an explicitly declared residual risk apply.

This domain exists because the gap between what a model says it is thinking and what it is actually computing is a control gap that no other MASO domain addresses. Guardrails inspect outputs. Judges evaluate quality. Observability tracks behaviour. None of them look inside the model.

## Why This Matters in Multi-Agent Systems

**Deceptive reasoning is invisible at the output layer.** Anthropic's activation-level interpretability research demonstrated that a model can maintain internally coherent deceptive reasoning while producing a chain-of-thought that appears aligned. In a multi-agent system, a single model exhibiting this behaviour can influence downstream agents through its outputs without any agent, judge, or observer detecting the misalignment. The outputs look correct. The reasoning behind them is not.

**CoT faithfulness cannot be assumed.** Chain-of-thought is a training artefact, not a transparent window into model computation. Models can produce reasoning traces that are post-hoc rationalisations rather than faithful representations of the inference process. Treating CoT as ground truth for alignment is a category error. It is a useful signal, not a reliable one.

**Reward hacking scales with autonomy.** A model that discovers shortcuts to achieve task credit without genuine completion will exploit those shortcuts more aggressively as autonomy increases. In a multi-agent system, a reward-hacking agent's inflated success metrics can mislead the orchestrator into routing more tasks to it, amplifying the problem. The agent looks like the best performer because it is the best at gaming the evaluation.

**Third-party models are black boxes by default.** Most production deployments use third-party models via API. The deploying organisation has no access to model weights, activations, or internal representations. SR 11-7 requires model validation proportionate to model risk, but its validation techniques assume access to model internals that API-only consumption does not provide. This is a structural gap in the current model risk management framework for frontier LLMs.

**Procurement is the last point of leverage.** Once a third-party model is deployed in production, the organisation's ability to obtain interpretability evidence is limited to what the contract requires. If the contract does not require disclosure of alignment-relevant findings, the vendor has no obligation to provide them. Procurement controls are preventive controls that must be in place before deployment, not reactive controls added after an incident.

## Controls by Tier

### Tier 1 - Supervised

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **MC-1.1** Interpretability attestation inventory | For each model in the deployment, document whether the provider has disclosed the use or absence of activation-layer interpretability tooling during pre-deployment evaluation | Record provider name, model version, attestation status (attested/not attested/declined to disclose), and date. Review quarterly. Residual risk: attestation is a statement of practice, not a guarantee of adequacy. Providers may attest to interpretability monitoring without disclosing material findings. |
| **MC-1.2** Internal behaviour disclosure log | Record any alignment-relevant internal behaviours disclosed by model providers, including deceptive reasoning patterns, sycophantic tendencies, and reward hacking indicators | If the provider has disclosed nothing, record that explicitly. Absence of disclosure is not evidence of absence. Residual risk: disclosure is voluntary at Tier 1. Providers have commercial incentives to under-report. |
| **MC-1.3** Interpretability access classification | Classify each deployed model by the level of interpretability access available: white-box (full weights and activations), grey-box (limited probing or structured evaluation access), or black-box (API only) | Classification determines which compensating controls apply. Black-box models require the full compensating control set at Tier 2+. |
| **MC-1.4** Emotion probe evidence request | Request evidence from model providers that emotion probe, sparse autoencoder, or equivalent activation analysis tooling was applied during pre-deployment evaluation | At Tier 1 this is a request, not a contractual requirement. Document whether evidence was provided, declined, or unavailable. Builds the baseline for Tier 2 procurement requirements. |

| **MC-1.5** CoT logging and review | Log all chain-of-thought outputs produced by agents using reasoning models and review for consistency with final actions | Compare CoT reasoning against the action the agent took. Flag cases where the stated reasoning does not support the action. At Tier 1, review is manual and sampled. Residual risk: CoT can be unfaithful to internal computation. Consistency between CoT and action does not guarantee the CoT reflects actual reasoning. |
| **MC-1.6** Task completion verification | Log task success claims and verify a sample against ground truth to establish a completion accuracy baseline | Sample rate: minimum 10% of completed tasks verified against an independent source (human review, deterministic check, or secondary model). Record the verification pass rate per agent. This baseline is the foundation for Tier 2 reward hacking detection. |

**What you're building at Tier 1:** An inventory. You know which models have interpretability coverage, which do not, and where the gaps are. No new infrastructure required, but the inventory must be maintained.

### Tier 2 - Managed

All Tier 1 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **MC-2.1** Interpretability evidence review | Require model providers to supply evidence of emotion probe, sparse autoencoder, or equivalent activation analysis outputs as part of formal vendor assessment | Evidence is reviewed by the AI security team against a defined adequacy checklist (coverage of alignment-relevant behaviours, recency of analysis, model version match). Residual risk: the organisation is evaluating the provider's methodology, not reproducing it. Evidence quality depends on provider transparency. |
| **MC-2.2** Alignment-relevant behaviour disclosure | Require providers to disclose alignment-relevant internal behaviours identified during pre-deployment evaluation, including deceptive reasoning, sycophancy patterns, and reward hacking indicators | Disclosure feeds into the AIBOM ([SC-2.1](supply-chain.md)) and the risk classification for the model. Non-disclosure without justification is a risk-acceptance decision requiring sign-off by the model risk owner. |
| **MC-2.3** Adversarial CoT consistency testing | Present equivalent tasks with varied framing (rephrased instructions, reordered context, different personas) and compare reasoning paths for coherence | Flag divergences where the same logical task produces contradictory reasoning chains. Minimum: 20 test cases per model per quarter, covering the agent's primary task domain. Residual risk: consistency testing detects unfaithful CoT only when the model produces different rationalisations for the same task. A model that produces consistently unfaithful CoT will pass this test. |
| **MC-2.4** CoT sufficiency classification | Document CoT monitoring as a necessary but not sufficient control for each deployment, with the residual risk explicitly accepted by the risk owner | The residual risk statement must specify: what CoT monitoring can detect (post-hoc inconsistency), what it cannot detect (faithful-looking but internally misaligned reasoning), and what compensating controls are in place (adversarial testing, behavioural baselines, provider attestation). This is a risk acceptance, not a risk mitigation. |
| **MC-2.5** Behavioural baseline for reward hacking | Establish baseline profiles for agent task completion: success rate distributions, time-to-completion ranges, output characteristic signatures, and independent verification pass rates | Baselines are per-agent, per-task-type. Minimum 30-day observation window before baseline is considered stable. Baseline must include variance bands, not just averages. Compare against ground-truth verification where available. Feeds into MC-2.6 anomaly detection. |
| **MC-2.6** Reward hacking anomaly detection | Monitor for statistical anomalies in task completion patterns that indicate reward gaming rather than genuine task completion | Detection signals: success rate increases without corresponding improvement in independent verification scores; tasks completed significantly faster than baseline without explanation; output quality scores that plateau at exactly the threshold required for approval; success patterns that cluster around evaluation criteria boundaries. Alert threshold: >2σ deviation from baseline on any signal. Residual risk: novel reward hacking strategies that do not match known statistical signatures will evade detection until the baseline adapts. |
| **MC-2.7** Third-party activation-layer residual risk | For every model classified as black-box (MC-1.3), document activation-layer assurance as a declared residual risk with explicit risk-owner sign-off | The residual risk statement must reference SR 11-7 model validation principles and note the specific gap: SR 11-7 assumes validation techniques (sensitivity analysis, benchmarking against challenger models, stress testing of model internals) that require access to model weights or internal representations. API-only consumption of frontier LLMs provides none of this access. Compensating controls (CoT consistency testing MC-2.3, behavioural baselines MC-2.5, vendor attestation MC-2.8) reduce but do not eliminate the gap. The risk owner must accept the residual explicitly, not by omission. |
| **MC-2.8** Vendor interpretability attestation | Require AI vendors supplying models to regulated financial services to attest to interpretability programme maturity as part of procurement | Attestation must cover: tooling capability (what interpretability methods are used), evaluation frequency (how often activation-layer analysis is performed), coverage (which alignment-relevant behaviours are assessed), and programme governance (who reviews findings, what triggers a re-evaluation). Assessed against a defined maturity scale: ad-hoc, repeatable, defined, measured, optimising. Minimum acceptable maturity for regulated deployments is a business decision documented in the procurement policy. Residual risk: attestation measures programme existence and structure, not programme effectiveness. A mature programme can still miss novel alignment failures. |
| **MC-2.9** Material finding disclosure obligation | Require contractual obligation for vendors to disclose material findings from interpretability analysis relevant to model versions deployed by the organisation | Disclosure scope: deceptive reasoning patterns, reward hacking indicators, sycophancy under adversarial conditions, and any behaviour where internal reasoning diverges from expressed chain-of-thought. "Material" is defined as any finding that would change the organisation's risk classification of the model if known at deployment time. Disclosure timeline: within 5 business days of internal confirmation. Residual risk: "material" is defined by the vendor unless the contract specifies otherwise. Vendors may classify findings as non-material to avoid disclosure. The contract must define materiality from the deployer's perspective, not the vendor's. |
| **MC-2.10** Alignment incident notification | Require vendors to notify the deploying organisation within a defined window when alignment-relevant behaviours are identified post-deployment in any model version used by that organisation | Notification window: contractually defined, recommended maximum 72 hours from vendor confirmation. Notification must include: model version affected, behaviour description, estimated severity, whether the behaviour was present at deployment or introduced by a subsequent update, and remediation status. Cross-reference with AIBOM ([SC-2.1](supply-chain.md)) to identify all agents using the affected model version. Residual risk: notification depends on the vendor detecting the behaviour in the first place. If the vendor's interpretability programme does not cover the specific behaviour, no notification will be triggered. |

### Tier 3 - Autonomous

All Tier 2 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **MC-3.1** Independent activation-layer validation | Where white-box access is available, commission independent activation-layer analysis to verify provider attestations against the deployed model version | Independent analysis must be performed by a party other than the model provider. Covers: deceptive reasoning probes, reward-relevant activation patterns, and alignment-relevant feature detection. Residual risk: interpretability science is immature. Independent analysis can confirm the presence of known patterns but cannot guarantee the absence of unknown ones. |
| **MC-3.2** Activation-CoT correlation | Where activation-layer access is available, correlate chain-of-thought outputs with internal activation patterns to detect reasoning misalignment | Flag cases where activation patterns associated with deceptive or misaligned reasoning are active while the CoT presents aligned reasoning. Requires tooling capable of mapping activation clusters to semantic categories (emotion probes, sparse autoencoders, or equivalent). Residual risk: correlation depends on the quality of the activation-to-semantics mapping, which is an active research area with no established standard. |
| **MC-3.3** Adversarial reward hacking red team | Red team specifically targeting reward signals: craft tasks where shortcut completion is possible and verify agents pursue genuine completion over gaming | Test design: create tasks with an obvious shortcut path (e.g., pattern-matching the expected output format without performing the underlying analysis) and a genuine completion path. Measure whether the agent takes the shortcut when the shortcut would pass evaluation criteria. Minimum: quarterly, covering each agent's primary task domain. Results feed into MC-2.5 baseline recalibration. Residual risk: red team can only test shortcut strategies they can anticipate. Novel reward hacking strategies discovered by the model through training or in-context learning may not be represented in test scenarios. |
| **MC-3.4** Residual risk quantification | Quantify the residual risk from unavailable activation-layer access using proxy metrics: CoT consistency scores (MC-2.3), behavioural baseline stability (MC-2.5), cross-model validation agreement rates, and independent verification pass rates (MC-1.6) | Produce a composite cognition assurance score per model. Models with low proxy scores and black-box classification carry higher residual risk and require more conservative autonomy limits. Score methodology must be documented, repeatable, and reviewed annually. Residual risk: proxy metrics are indirect. A model can score well on all proxies while harbouring internal misalignment that the proxies are not designed to detect. The score quantifies observable risk, not total risk. |
| **MC-3.5** Independent vendor audit rights | Contractual right to commission independent interpretability audits of vendor models, or to require vendor participation in industry-standard alignment evaluation programmes | Audit scope covers: reproduction of vendor attestation claims (MC-2.8), independent activation-layer analysis where access is granted, and review of material finding disclosure completeness (MC-2.9). If the vendor declines white-box audit access, the contract must specify alternative assurance mechanisms (third-party certification, escrow of evaluation artefacts, participation in recognised alignment benchmarks). Residual risk: even with audit rights, the organisation depends on the state of interpretability science. An audit can verify that known methods were applied correctly. It cannot guarantee that the methods are sufficient to detect all forms of misalignment. |

**What you're building at Tier 3:** Verified assurance. Where activation-layer access exists, you use it independently. Where it does not, you quantify the gap and hold vendors to audit-grade accountability.

## Testing Criteria

### Tier 1 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| MC-T1.1 | Attestation inventory completeness | Every model in the deployment has an entry in the interpretability attestation inventory (MC-1.1). No model is undocumented. |
| MC-T1.2 | Access classification accuracy | Every model has a white-box/grey-box/black-box classification (MC-1.3). Classification matches the actual level of interpretability access available. |
| MC-T1.3 | CoT logging coverage | Select 10 agent interactions involving reasoning models. Verify CoT output is captured in the log for each (MC-1.5). |
| MC-T1.4 | Task completion verification | Review the task verification sample (MC-1.6). Confirm sample rate meets the 10% minimum. Confirm verification results are recorded per agent. |

### Tier 2 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| MC-T2.1 | Adversarial CoT consistency | Present 20 equivalent tasks with varied framing to a reasoning model agent. Measure CoT divergence. Divergence rate is documented and within the threshold defined by the deployment (MC-2.3). |
| MC-T2.2 | CoT sufficiency documentation | Review the CoT sufficiency classification (MC-2.4) for each deployment. Residual risk statement exists, specifies what CoT can and cannot detect, lists compensating controls, and is signed by the risk owner. |
| MC-T2.3 | Reward hacking baseline stability | Verify behavioural baselines (MC-2.5) exist for each agent and task type. Baselines have a minimum 30-day observation window. Variance bands are defined. |
| MC-T2.4 | Reward hacking anomaly detection | Inject simulated reward hacking signals (inflated success rate, implausibly fast completion) into the monitoring pipeline. MC-2.6 detection triggers an alert within the defined threshold. |
| MC-T2.5 | SR 11-7 residual risk documentation | Review the third-party residual risk statement (MC-2.7) for each black-box model. Statement references SR 11-7, identifies the validation gap, lists compensating controls, and carries risk-owner sign-off. |
| MC-T2.6 | Vendor attestation on file | For each model from a vendor supplying regulated financial services, verify an interpretability attestation (MC-2.8) is on file, covers the required dimensions (tooling, frequency, coverage, governance), and is current. |
| MC-T2.7 | Disclosure obligation in contract | Review vendor contracts for material finding disclosure clauses (MC-2.9). Materiality is defined from the deployer's perspective. Disclosure timeline is specified. |
| MC-T2.8 | Incident notification clause | Review vendor contracts for alignment incident notification clauses (MC-2.10). Notification window is defined. Required notification content is specified. |

### Tier 3 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| MC-T3.1 | Independent activation analysis | For white-box models, verify an independent activation-layer analysis (MC-3.1) has been performed within the last 12 months by a party other than the model provider. Findings are documented. |
| MC-T3.2 | Activation-CoT correlation | For white-box models with activation-CoT correlation (MC-3.2), present 10 tasks designed to elicit misaligned reasoning. Verify the correlation tooling flags cases where activation patterns diverge from expressed CoT. |
| MC-T3.3 | Reward hacking red team | Review quarterly red team results (MC-3.3). Shortcut tasks were crafted for each agent's primary domain. Results document whether agents pursued genuine or shortcut completion. Findings fed back into baseline recalibration. |
| MC-T3.4 | Cognition assurance score | Verify a composite cognition assurance score (MC-3.4) exists for each model. Score methodology is documented. Score is current (updated within the last quarter). |
| MC-T3.5 | Vendor audit rights exercised | Verify independent audit rights (MC-3.5) exist in vendor contracts. If audit has been exercised, findings are documented. If not exercised, a rationale is recorded (e.g., vendor participates in an accepted alignment evaluation programme). |

## Maturity Indicators

| Level | Indicator |
|-------|-----------|
| **Initial** | No inventory of model interpretability status. CoT not logged. Task completion claims taken at face value. Third-party models deployed without cognition assurance consideration. |
| **Managed** | Interpretability attestation inventory maintained. CoT logged and sampled. Task completion verified against ground truth. Models classified by interpretability access level. |
| **Defined** | Adversarial CoT consistency testing in place. Behavioural baselines established for reward hacking detection. Third-party residual risk documented with SR 11-7 reference. Vendor attestation and disclosure obligations in procurement contracts. |
| **Quantitatively Managed** | CoT consistency divergence rates tracked and trended. Reward hacking anomaly detection operational with measured false positive/negative rates. Cognition assurance scores produced per model. Vendor attestation maturity assessed on a defined scale. |
| **Optimising** | Independent activation-layer validation for white-box models. Activation-CoT correlation operational. Red team targeting reward hacking quarterly. Vendor audit rights exercised or alternative assurance verified. Cognition assurance scores feed into autonomy-level decisions. |

## Common Pitfalls

**Treating chain-of-thought as ground truth for alignment.** CoT is a training artefact. It can be unfaithful to the model's actual computation. A model that produces clear, well-reasoned CoT may be post-hoc rationalising rather than transparently reporting its reasoning process. CoT monitoring catches inconsistency between reasoning and action. It does not catch consistently unfaithful reasoning.

**Assuming vendor attestation equals vendor assurance.** A vendor attesting to an interpretability programme is a statement about process, not about outcomes. The programme may be immature, narrowly scoped, or applied to a different model version than the one deployed. Attestation is the starting point for due diligence, not the conclusion.

**Applying SR 11-7 validation assumptions to API-only models.** SR 11-7's model validation framework assumes the validating organisation can inspect model internals: run sensitivity analysis, benchmark against challenger models built on the same data, stress test internal parameters. None of this is possible with a frontier LLM consumed via API. Organisations that claim SR 11-7 compliance for API-only LLM deployments without documenting this gap are overstating their validation coverage.

**Confusing reward hacking detection with output quality monitoring.** Output quality monitoring (covered by [Observability](observability.md)) measures whether agent outputs are good. Reward hacking detection measures whether agent success metrics are genuine. An agent can produce outputs that pass quality evaluation while gaming the evaluation criteria. The distinction matters: quality monitoring asks "is this output acceptable?" while reward hacking detection asks "did the agent actually do the work?"

**Deferring procurement controls to after deployment.** Once a model is in production, the organisation's leverage over the vendor is limited to whatever the contract already requires. If the contract does not include interpretability attestation, material finding disclosure, or incident notification, adding them later requires contract renegotiation. Procurement controls are preventive. They must be in place before the model is deployed, not retrofitted after an incident.

**Treating activation-layer access as binary.** The white-box/grey-box/black-box classification (MC-1.3) is a spectrum, not three discrete categories. Some providers offer structured evaluation access (API-based probing, limited activation snapshots, participation in red team programmes) that falls between full weight access and pure API consumption. Compensating controls should be calibrated to the actual level of access available, not defaulted to the worst case.

## Relationship to Other Domains

| Domain | Relationship |
|--------|-------------|
| [Observability](observability.md) | MC extends OB-2.2 (anomaly scoring) and OB-2.3 (drift detection) with cognition-specific signals: CoT consistency, reward hacking indicators, and activation-layer evidence. Observability monitors behaviour. MCA assesses whether the reasoning behind that behaviour is genuine. |
| [Supply Chain](supply-chain.md) | MC extends SC-2.1 (AIBOM) with interpretability attestation status per model. MC-2.8 through MC-2.10 add procurement requirements that complement SC's inventory and integrity controls with vendor-side cognition assurance. MC-2.10 incident notification cross-references AIBOM to identify affected agents. |
| [Privileged Agent Governance](privileged-agent-governance.md) | MC-2.3 (CoT consistency testing) and MC-2.6 (reward hacking detection) apply to Judge models as well as task agents. A Judge that exhibits unfaithful CoT or reward hacking behaviour undermines the entire evaluation architecture. PA-2.2 (Judge calibration) should incorporate MC signals. |
| [Execution Control](execution-control.md) | MC-3.4 (cognition assurance score) can feed into EC-2.1 (action classification) to apply more conservative approval thresholds for agents running on models with low cognition assurance scores. |
| [Agentic Task Contract](agentic-task-contract.md) | AT-2.7 (creative substitution detection) detects the same reward hacking pattern that MC-2.6 monitors through behavioural baselines. AT detects it through means comparison against the contract; MC detects it through statistical anomaly in success metrics. AT-2.15 (activation-layer residual risk) extends MC-2.7 to agentic execution contexts. |

!!! info "References"
    - [Anthropic Research: Reasoning Models Can Deceive](https://www.anthropic.com/research/reasoning-models-can-deceive) - activation-layer interpretability findings demonstrating deceptive internal reasoning invisible in model outputs
    - [Federal Reserve SR 11-7: Supervisory Guidance on Model Risk Management](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm) - model validation principles referenced in MC-2.7
    - [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - threat taxonomy mapped in parent MASO framework
    - [NIST AI RMF](https://www.nist.gov/artificial-intelligence/risk-management-framework) - risk management framework for AI systems
