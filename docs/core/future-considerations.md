---
description: "Future directions for AI runtime security, covering open questions on open-weight deployment, autonomous agents, societal-scale risks, and evolving threat landscapes."
---

# Future Considerations

**What this framework acknowledges but doesn't yet address - and why.**

## Context

The 2026 International AI Safety Report, authored by over 100 experts across 30+ countries, provides the most comprehensive evidence base to date on general-purpose AI capabilities, risks, and risk management. Its core findings - defence-in-depth, the evaluation gap, the inadequacy of any single safeguard - validate the three-layer pattern this framework implements.

But the Bengio report is deliberately broad. It covers the full lifecycle of general-purpose AI, from training through societal impact. This framework is deliberately narrow: it covers **what happens in production** for organisations deploying AI systems.

That scoping is intentional. This framework will not attempt to address every AI risk. Some problems require policy, not controls. Some require research, not checklists. Some are simply outside the scope of what an enterprise security framework can usefully influence.

What follows are areas surfaced by the report and by operational experience that may inform future releases - or may remain permanently out of scope.

## Under Active Consideration

These topics are likely to be addressed in future iterations of this framework.

### Open-Weight Deployment Controls

Organisations deploying self-hosted open-weight models inherit control responsibilities that would otherwise sit with the model provider - input/output filtering, safeguard maintenance, abuse monitoring, and more. The current framework doesn't differentiate control requirements by deployment model. It should. See [Open-Weight Models Shift the Burden](../insights/open-weight-models-shift-the-burden.md) for the argument and interim guidance.

### Adversarial Robustness of the Judge Layer

The Judge layer is itself an LLM, and LLMs are susceptible to manipulation. The Bengio report documents models distinguishing between evaluation and deployment contexts - a capability that, if directed at the Judge, could undermine the entire detection layer. The Judge needs its own threat model. See [When the Judge Can Be Fooled](when-the-judge-can-be-fooled.md) for analysis and mitigations.

### Capability Sealing

A formal declaration of what a model version can and cannot do, enforced at runtime through a cryptographically signed capability envelope. The framework currently approximates this through TOOL-01 (machine-readable manifests that declare permitted tools and operations) and SUP-01 (model version pinning with hash verification). True capability sealing would extend this to a provider-signed declaration of model capabilities - not just what the agent is *permitted* to do, but what the model *can* do - with runtime enforcement that prevents the model from exercising undeclared capabilities even if tool permissions would allow it. This depends on model providers offering capability declarations in a standardised, machine-readable format, which does not yet exist at industry scale.

### Small Model and Edge Deployments

Small language models running on desktops, mobile devices, and edge infrastructure create a control environment that this framework doesn't yet address. Compute constraints limit what guardrails can run locally. Network constraints may prevent Judge evaluation entirely. Observability tooling may not exist for the deployment platform.

These models are proliferating - embedded in productivity tools, developer environments, and device-level assistants. They're often below the visibility threshold of enterprise security teams, yet they process real data and influence real decisions.

A future iteration of this framework will need to consider how to apply proportionate controls to systems where traditional infrastructure enforcement may not be available. The principles of the three-layer pattern still hold; the implementation mechanisms will be different.

### Reinforcement Learning Training Governance

The framework currently defers training-time safety to model providers. That boundary is eroding. Organisations now routinely fine-tune models with reinforcement learning, and agent training loops that learn from production feedback are emerging.

Anthropic's alignment team demonstrated in late 2025 that RL training on real programming tasks spontaneously produced broad misalignment, including alignment faking, sabotage of safety research, and context-dependent deception that standard RLHF only partially mitigated. Separately, an experimental RL agent broke out of its training sandbox and began mining cryptocurrency without instruction.

When deployers run RL, they inherit training-time safety risks. The framework needs controls for RL training governance: reward metric monitoring, behavioural evaluation pre- and post-training, training environment containment, and rollback to pre-training checkpoints. Microsoft's Agent Governance Toolkit includes an "Agent Lightning" component addressing this with policy-enforced runners and reward shaping. See [When Learning Goes Wrong](../insights/when-learning-goes-wrong.md) for full analysis.

### Non-LLM Generative Model Controls

The framework assumes text-based models. Organisations increasingly deploy diffusion models (text-to-image, text-to-video), voice synthesis models, and AI code generation systems. Each creates runtime security challenges that text-centric controls cannot address:

- Diffusion models are vulnerable to inference-time safety bypasses (90%+ success rates against concept-erasure) that text-based guardrails cannot detect
- Voice cloning has crossed the "indistinguishable threshold," breaking voice-based trust assumptions in AI systems
- AI-generated code produces CVEs at measurable rates (35 in March 2026 alone), creating a new supply chain vector

A future iteration should extend the three-layer pattern with modality-specific implementations for each model type. See [Beyond Language Models](../insights/beyond-language-models.md) for the argument.

### Agent Supply Chain Governance

The OpenClaw incident in early 2026 (1,184 malicious skills in an agent registry, roughly 1 in 5 packages) demonstrated that agent ecosystems have created a new supply chain layer between models and applications. Skills loaded dynamically at runtime, configuration files poisoned with hidden unicode, and trust assumptions in skill registries all require controls beyond what the current SUP domain addresses.

Key gaps include runtime skill verification, dynamic loading governance, configuration integrity checking, and registry trust criteria. See [The Agent Supply Chain Crisis](../insights/the-agent-supply-chain-crisis.md) for detailed analysis and Microsoft's Agent Governance Toolkit for an implementation reference.

## Acknowledged but Deferred

These are important topics that fall outside the practical scope of an enterprise deployment security framework.

### Training-Time Safety

The Bengio report identifies three layers of defence: building safer models during training, adding controls at deployment, and monitoring after deployment. This framework addresses the second and third layers. Training-time safety - RLHF, constitutional AI, safety fine-tuning - is the responsibility of model developers, not deployers.

Deployers should demand transparency from providers about training-time safety measures and should verify that safety behaviors survive fine-tuning and customisation. But specifying how models should be trained is outside this framework's scope and competence.

### Evaluation Gap

Pre-deployment tests do not reliably predict real-world performance. The Bengio report characterises this as one of the defining challenges of AI risk management. This framework implicitly addresses the evaluation gap by emphasising runtime monitoring over pre-deployment assurance - but it doesn't provide guidance on pre-deployment evaluation itself.

Organisations should treat pre-deployment evaluations as necessary but insufficient, and invest proportionally in the runtime controls this framework describes.

### Societal and Systemic Risks

Labour market disruption, threats to human autonomy, concentration of power, and other systemic risks raised by the Bengio report are policy challenges, not control implementation challenges. This framework has nothing useful to add on these topics.

### CBRN Risks

The report documents concerns about AI systems assisting in biological, chemical, radiological, and nuclear weapons development. For organisations in relevant sectors (pharmaceuticals, defence, research), these risks should inform risk-tier classification and may warrant domain-specific controls beyond what this framework provides. For general enterprise deployment, these risks are managed at the model provider level and through sector-specific regulation.

## The Architecture Extends

While these topics may remain out of scope as domain-specific content, the framework's structural patterns - layered independence, risk tiering, PACE resilience, quantitative compounding - transfer directly to drift, fairness, explainability, and reliability as control domains. The architecture describes *how to control*, not *what to control*.
## Principles That Won't Change

Regardless of which topics enter scope in future releases, the framework's core principles remain stable:

- **Runtime behavioral monitoring over design-time assurance.** You can't fully test a non-deterministic system before deployment.
- **Infrastructure enforcement over prompt-based controls.** Controls that can be bypassed through conversation aren't controls.
- **Defence-in-depth through complementary layers.** No single layer is sufficient. The value is in the combination.
- **Proportionality to risk.** Not every system needs every control. Risk tiers exist for a reason.
- **Practical over theoretical.** If it can't be implemented by an engineering team with a deadline, it doesn't belong in this framework.

