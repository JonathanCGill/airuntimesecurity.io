# The Model You Choose Is a Security Decision

*Choosing a flawed model makes every control downstream harder. The first security question isn't "how do we monitor it?" It's "should we trust it?"*

## The Question Nobody Asks Early Enough

Teams evaluate models on capability. Can it code? Can it reason? Can it follow instructions? Can it handle our domain?

These are important questions. They are not security questions.

The security question is different: **does this model behave predictably enough, transparently enough, and reliably enough that the controls we wrap around it will actually work?**

A model that hallucinates confidently defeats your grounding checks. A model with poor instruction-following defeats your system prompt guardrails. A model trained on undisclosed data exposes you to risks you can't enumerate. A model from a provider with no security disclosure process means vulnerabilities found by researchers may never reach you.

Capability evaluation and security evaluation are different activities. Most organisations do the first. Few do the second.

## What "Reputable" Actually Means

"We're using a reputable model" is not a security statement. It is a popularity statement. Reputation in the AI model market currently tracks funding, benchmarks, and adoption - none of which correlate reliably with security posture.

A model is security-reputable when you can answer these questions:

### 1. Do you know what it was trained on?

Not in detail - no provider discloses full training corpora. But in principle: does the provider publish a model card? Does the model card describe the training data at a level that lets you assess risk? Or does it say "trained on a large corpus of internet text" and leave it there?

What you're looking for:

- **Data filtering practices.** Was harmful content filtered? How? What was the threshold?
- **Known limitations disclosed.** Every model has failure modes. Providers that document them are more trustworthy than those that don't.
- **Language and domain coverage.** A model trained primarily on English text will behave differently on regulatory documents in German. If the provider doesn't tell you the distribution, you can't assess the risk.

A model card that is vague is not neutral. It is a signal that the provider has not done the work, or has done the work and chosen not to share it.

### 2. Does the provider have a security process?

Not a marketing page. A process.

- **Vulnerability disclosure.** Is there a way for researchers to report security issues? Is there a published policy?
- **Security advisories.** When vulnerabilities are found, how does the provider communicate them? Do they issue advisories? Do they notify API customers?
- **Incident history.** Has the provider experienced security incidents? More importantly: how did they respond? Transparency after an incident is a stronger signal than never having had one.
- **Red team results.** Has the provider published results from adversarial testing? Third-party evaluations carry more weight than internal ones.

A provider that treats security as a feature to market rather than a process to operate is a risk.

### 3. Can you test it before you trust it?

Security evaluation requires testing the model against your specific threat scenarios - not the provider's generic benchmarks.

- **Prompt injection resistance.** Run known injection techniques against the model with your system prompt. Does it hold?
- **Instruction-following fidelity.** Give it a system prompt with constraints. Does it respect them under adversarial user input?
- **Refusal behavior.** Ask it to do things it shouldn't. Does it refuse consistently, or does the refusal vary with phrasing?
- **Output consistency.** Run the same input multiple times. How much does the output vary? High variance means your guardrails need to handle a wider range of outputs.

If you can't test a model against your threat scenarios before deployment, you are deploying a control you haven't verified. The framework's [risk assessment methodology](../core/risk-assessment.md) requires measured effectiveness rates. You can't measure what you haven't tested.

### 4. Do you control the version?

A model that silently updates is a model that silently changes your security posture.

- **API models.** Does the provider support version pinning? Will they notify you before deprecating a version? What's the migration timeline?
- **Self-hosted models.** Do you hash-verify the weights? Do you pull from official sources only? Do you store approved versions in your own artefact repository?
- **Fine-tuned models.** Can you trace the full lineage - base model version, training data, hyperparameters?

Version control for models is not optional. It is the difference between "we know what we're running" and "we think we know what we're running."

### 5. What happens when it goes wrong?

Every model will produce outputs you didn't anticipate. The question is whether the provider's response to problems helps you or hurts you.

- **Update cadence.** How frequently does the provider release safety improvements? Is there a pattern, or is it reactive?
- **Rollback capability.** If a new version introduces a security regression, can you revert to the previous version? How quickly?
- **Shared responsibility model.** Does the provider clearly define what they are responsible for vs. what you are responsible for? Or is the boundary ambiguous?

## The Asymmetry You Cannot Eliminate

With traditional software, you can audit the source code. With models, you cannot.

You cannot inspect why a model produces a given output. You cannot verify that safety training was applied correctly. You cannot confirm that a disclosed vulnerability has been fully patched in the weights. You are trusting the provider's process, not verifying their product.

This is why the framework's three-layer pattern exists. You cannot eliminate the asymmetry, but you can compensate for it:

- **Guardrails** catch outputs that violate known constraints - regardless of why the model produced them.
- **The Judge** evaluates outputs against your policies - regardless of what the model intended.
- **Human review** applies judgment - regardless of what the model claims.

The layers don't trust the model. They verify its outputs. But the layers work *better* when the model is better. A model with strong instruction-following produces fewer guardrail triggers. A model with good safety training produces fewer Judge flags. A model with consistent behavior produces fewer surprises for human reviewers.

Choosing a trustworthy model doesn't replace controls. It makes controls more effective and less costly to operate.

## A Practical Evaluation

When assessing a model for security, not capability, ask:

| Question | Strong Signal | Weak Signal |
|---|---|---|
| **Training data transparency** | Published model card with data sources, filtering methodology, and known limitations | "Trained on diverse internet data" |
| **Vulnerability disclosure** | Published policy, named security contact, history of advisories | No disclosure process, or "contact support" |
| **Red team results** | Third-party adversarial testing results published | "We conduct internal safety testing" with no details |
| **Version control** | Explicit version pinning, deprecation timeline, migration support | "Latest" alias with no advance notice of changes |
| **Incident response** | Documented incident history with post-mortems and remediation timelines | No disclosed incidents (which may mean no transparency, not no incidents) |
| **Instruction-following** | Consistent constraint adherence under adversarial pressure | Works in demo, unpredictable under edge cases |
| **Safety training** | Published alignment methodology, quantified refusal rates | "We've applied safety measures" with no specifics |

No model will score perfectly. The point is not to find a perfect model. It is to make the selection with open eyes and to calibrate your controls accordingly.

A model that scores poorly on transparency needs stronger runtime controls. A model that scores well on instruction-following may need less aggressive guardrail coverage. The model choice and the control investment are connected decisions.

The b³ benchmark (Bazinska et al., ICLR 2026) now provides empirical data for this: across 34 models and 194,331 adversarial attacks, backbone LLMs show measurably different vulnerability profiles, and those profiles vary by attack type. A model that resists indirect instruction override may be weak against tool invocation attacks. For the full analysis, see [The Backbone Problem](the-backbone-problem.md).

## What This Does Not Replace

This is not a model evaluation framework. It does not tell you how to benchmark accuracy, measure latency, or compare reasoning capability. Those are capability assessments with mature tooling and methodology.

This is a security lens on model selection. It sits upstream of the framework's [supply chain controls](../extensions/technical/supply-chain.md), which handle the technical mechanics - hash verification, version pinning, dependency scanning. And it complements the [vendor assessment questionnaire](../extensions/templates/vendor-assessment-questionnaire.md), which structures the contractual relationship.

The sequence is:

1. **Evaluate the model's security posture** - is it trustworthy enough to deploy? *(this document)*
2. **Verify what you deploy** - is it the model you evaluated? *([supply chain controls](../extensions/technical/supply-chain.md))*
3. **Monitor what it does** - is it behaving as expected in production? *([core controls](../core/controls.md))*

Skip step one and you're verifying the integrity of a model you never assessed, then monitoring outputs from a system whose baseline risk you don't understand.

## The Bottom Line

The model is the foundation. Every control in this framework - guardrails, Judge, human review, PACE resilience - operates on the model's outputs. If the model is fundamentally untrustworthy, the controls work harder, cost more, and catch less.

Choosing a model is not just a capability decision. It is the first security decision you make.

Make it deliberately.

