---
description: "How model drift degrades every layer of the runtime security architecture, and why continuous behavioral monitoring is the only viable response."
---

# Model Drift Is a Runtime Security Problem

*The model you validated last month is not the model running today. Drift degrades every control layer silently, and the framework is designed to catch it.*

## The Problem

Model drift is not a hypothetical. It is the default state of any AI system in production long enough.

Models change because their providers update them. Models change because the data they process shifts. Models change because fine-tuning datasets age. And sometimes models change for reasons nobody fully understands, because the relationship between training data, weights, and behavior is not transparent enough to predict.

The security consequence is specific: **every control in this framework is calibrated against observed model behavior. When the model drifts, the calibration breaks.**

A guardrail tuned to catch prompt injection at a 0.94 confidence threshold assumes the model's output distribution stays within the range observed during calibration. A Judge configured with a behavioral constitution assumes the model's baseline patterns remain stable enough that deviation is meaningful. Human reviewers develop intuitions about what "normal" looks like for the systems they oversee. All three layers depend on behavioral stability. None of them get it.

## Three Types of Drift That Matter

Not all drift is equal. The framework must handle three distinct failure patterns, each degrading controls differently.

### 1. Provider-Initiated Model Updates

The most common source of drift. A provider releases a new model version, and behavior changes in ways that were not part of any changelog.

This is well documented. OpenAI's GPT-4 showed measurable behavioral changes between the March and June 2023 versions, with chain-of-thought reasoning compliance dropping significantly on certain tasks. Anthropic, Google, and every other provider ship updates that alter safety behavior, instruction-following fidelity, and output distribution. Sometimes the changes are improvements. Sometimes they introduce regressions. Almost always, the deploying organisation learns about the change from production telemetry, not from advance notice.

**Impact on the framework:**

- **Guardrails** may see changed false positive/negative rates overnight. A content filter calibrated for one model version's output style may under-block or over-block with the next version.
- **The Judge** baseline becomes stale. The Judge detects deviation from expected behavior. If the model's expected behavior shifts because the provider updated it, every response looks anomalous, or nothing does, depending on which direction the drift moves.
- **Human reviewers** lose their calibration. Reviewers who have spent weeks building intuition about what the model produces are suddenly reviewing outputs from what is effectively a different system.

### 2. Data Distribution Shift

The world changes. The inputs your model receives today are not the inputs it received six months ago. Customer language evolves, new products launch, regulatory requirements change, seasonal patterns shift query distributions.

The model has not changed. The relationship between the model and its operating environment has.

**Impact on the framework:**

- **Guardrails** designed for one input distribution may miss threats that arrive in a different distribution. A PII detector trained on US formats will miss Australian Medicare numbers. An injection detector calibrated for English-language attacks will miss attacks in other languages as your user base shifts.
- **The Judge** evaluates responses against a behavioral constitution. If the constitution was written for one domain of queries and the queries shift to another, the Judge's coverage has gaps it was never designed to handle.
- **Risk tiering** may become inaccurate. A system classified as Tier 1 based on its original use case may be handling Tier 2 queries because the user population changed.

### 3. Silent Behavioral Degradation

The hardest drift to detect. The model version has not changed. The input distribution has not changed. But output quality degrades gradually, in ways that do not trigger any single threshold.

This manifests as: slightly less accurate summaries, slightly more confident hallucinations, slightly broader scope creep in multi-turn conversations, slightly weaker instruction-following under adversarial pressure. Each individual output passes every check. The aggregate trend is a system that is slowly becoming less reliable.

**Impact on the framework:**

- **Guardrails** do not catch this. Pattern matchers detect discrete violations, not gradual quality degradation.
- **The Judge** may catch individual instances but miss the trend if it evaluates transactions independently without temporal aggregation.
- **Human reviewers** are the most vulnerable. Humans adapt to gradual change. If output quality drops 1% per week, reviewers unconsciously recalibrate their expectations rather than flagging the decline.

## How the Framework Responds

The framework was designed as a closed-loop control system precisely because model drift is inevitable. The architecture does not assume behavioral stability. It continuously measures for its absence.

### Drift Detection as the Comparator

In the [closed-loop control model](why-containment-beats-evaluation.md), drift detection serves as the comparator: the component that measures the error between desired state and actual state.

| Control Element | Implementation |
|---|---|
| **Setpoint** | Declared intent specification: what the model should do |
| **Sensor** | Judge evaluation + observability telemetry: what the model is doing |
| **Comparator** | Drift detection: the gap between should and is |
| **Actuator** | Human oversight escalation + PACE degradation: corrective action |

Without drift detection, the control loop is open. You evaluated the model once, set your controls, and hope nothing changes. With drift detection, the control loop closes. Deviation triggers investigation, investigation triggers correction.

### The Behavioral Anomaly Layer

The [behavioral anomaly detection](behavioral-anomaly-detection.md) architecture aggregates signals across all safety layers to detect drift that no single layer would catch:

- **Volume anomalies**: guardrail block rates increasing beyond baseline
- **Pattern anomalies**: new failure signatures appearing that did not exist during calibration
- **Correlation anomalies**: layers that previously agreed now disagreeing on the same transactions
- **Temporal anomalies**: quality metrics trending in one direction over weeks

The key insight is that drift is visible in the aggregate before it is visible in any individual transaction. A single guardrail block means nothing. A 30% increase in guardrail blocks over two weeks means the model or its environment has changed.

### PACE Responds to Drift

When drift detection identifies a significant deviation, the [PACE resilience model](../PACE-RESILIENCE.md) provides a structured response:

| PACE State | Drift Response |
|---|---|
| **Primary** | Online drift detection active. Rolling baselines updated. Normal operations. |
| **Alternate** | Drift detected but within tolerance. Increase Judge sampling rate. Tighten uncertainty bounds. Alert the operations team. |
| **Contingency** | Significant drift confirmed. Revert to last validated model version. Route all outputs through human review. Pause automated actions. |
| **Emergency** | Drift has compromised control integrity. Circuit breaker fires. Non-AI fallback active. |

The transition from Primary to Alternate is where most drift is handled. The model changed, the controls noticed, the team investigated, and the calibration was updated. Contingency and Emergency exist for the cases where drift has outpaced the control system's ability to compensate.

### Multi-Agent Drift Amplification

In [multi-agent systems](when-agents-talk-to-agents.md), drift compounds. If Agent A's output quality degrades, Agent B processes degraded input and produces lower-quality output, which Agent C then uses as the basis for its own response. The final output may be significantly worse than any individual agent's drift would suggest.

Worse, multi-agent systems can mask drift. As noted in the [MASO observability controls](../maso/controls/observability.md): "drift in one agent may be masked by compensating behavior in another." Agent A starts hallucinating, but Agent B's summarisation smooths over the inaccuracies. The final output looks acceptable while the intermediate data is corrupted.

This is why MASO requires per-agent observability (OB-2.2, OB-2.3) and cross-agent correlation (OB-3.4). Drift must be detected at the individual agent level, not just at the system output level.

## What Organisations Should Do

### 1. Pin Model Versions

Do not use "latest" aliases in production. Pin to specific model versions. Track when versions change. Test before promoting a new version to production. This is basic supply chain hygiene, but most organisations do not do it.

See [The Model You Choose Is a Security Decision](the-model-you-choose.md) for the full argument.

### 2. Establish Behavioral Baselines

You cannot detect drift without a baseline. Capture the model's output distribution during validation: response length distributions, confidence score patterns, guardrail trigger rates, Judge evaluation distributions. These baselines are the "normal" against which drift is measured.

### 3. Monitor Continuously, Not Periodically

Weekly model reviews miss drift that accumulates between reviews. The [observability controls](../maso/controls/observability.md) require rolling baselines with automated alerting on deviation. At minimum, implement OB-2.3 (drift detection with 7-day rolling baseline, alert on >2 sigma deviation).

### 4. Recalibrate After Every Model Change

When a model version updates, the Judge baseline, guardrail thresholds, and human reviewer expectations must all be recalibrated. This is operational overhead, and it is unavoidable. The alternative is controls calibrated against a model that no longer exists.

### 5. Test Drift Response

Include drift scenarios in your testing programme. Simulate a model version change and verify that your observability layer detects it. Simulate gradual quality degradation and verify that your anomaly detection catches the trend before it becomes a production incident. If your drift response only exists on paper, it does not exist.

## The Quantitative Argument

The framework's [risk assessment methodology](../core/risk-assessment.md) calculates residual risk as the product of independent miss rates across layers. Drift increases every miss rate simultaneously.

Consider a system with:

- Guardrail miss rate: 5% (P = 0.05)
- Judge miss rate: 10% (P = 0.10)
- Human review miss rate: 15% (P = 0.15)

Residual risk (no drift): 0.05 x 0.10 x 0.15 = **0.075%**

Now assume drift degrades each layer by a factor of two:

- Guardrail miss rate: 10% (P = 0.10)
- Judge miss rate: 20% (P = 0.20)
- Human review miss rate: 30% (P = 0.30)

Residual risk (with drift): 0.10 x 0.20 x 0.30 = **0.6%**

An eightfold increase in residual risk, from a drift that doubled each layer's miss rate. And the layers degrade together because they are all calibrated against the same model behavior. This is not independent failure. It is correlated degradation, the most dangerous pattern in a defence-in-depth architecture.

This is why drift detection is not optional. It is the mechanism that prevents correlated control degradation from accumulating undetected.

## The Bottom Line

Model drift is not a model problem. It is a control system problem. Every layer of the framework depends on behavioral stability that models do not provide. The framework compensates through closed-loop monitoring, behavioral baselines, anomaly detection, and structured degradation.

The question is not whether your model will drift. It will. The question is whether your controls will notice before your customers do.

!!! info "References"
    - [Why Containment Beats Evaluation](why-containment-beats-evaluation.md) - The closed-loop control architecture that makes drift detection structural
    - [Behavioral Anomaly Detection](behavioral-anomaly-detection.md) - Aggregating safety signals to detect when behavior drifts from normal
    - [Beyond Security](beyond-security.md) - How the framework's architecture applies to drift, fairness, and other AI risks
    - [MASO Observability Controls](../maso/controls/observability.md) - Per-agent drift detection and cross-agent correlation
    - [The Model You Choose Is a Security Decision](the-model-you-choose.md) - Version control and supply chain hygiene for model selection
    - [PACE Resilience](../PACE-RESILIENCE.md) - Structured degradation when drift compromises control integrity
