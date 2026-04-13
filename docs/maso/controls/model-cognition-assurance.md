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

**What you're building at Tier 1:** An inventory. You know which models have interpretability coverage, which do not, and where the gaps are. No new infrastructure required, but the inventory must be maintained.
