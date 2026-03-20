---
description: "Solving the latency-security paradox with distilled sidecar SLMs: how to compress a large Judge LLM into a fast, local security sensor for action-by-action evaluation in agentic banking."
---

# Distilling the Judge into a Small Language Model

*Solving the Latency-Security Paradox with Distilled Sidecar SLMs*

Financial institutions have moved beyond the chatbot era into **agentic banking**, where autonomous models possess the agency to move funds, modify records, and interact with core ledgers. Traditional security models that rely on large Judge LLMs fail in these environments due to excessive latency, prohibitive token costs, and data sovereignty risks.

This page describes a decentralized security architecture using Small Language Models (SLMs) distilled from frontier models. By deploying these specialized sensors as sidecars within the execution environment, banks can achieve action-by-action security with sub-50ms latency while remaining compliant with the 2026 Treasury FS-AI RMF and [DORA](../../foundations/README.md) mandates.

## The Runtime Security Gap

In a bank, security cannot be a post-hoc audit. It must be a real-time gate. The existing [Judge architecture](model-as-judge-implementation.md) works well as an async assurance mechanism, but for agentic systems that execute tool calls, database queries, and API requests at machine speed, async review is not fast enough to prevent harm.

Large Judge architectures create a trilemma:

| Constraint | Large Judge (Cloud API) | Distilled SLM (Local) |
|------------|------------------------|----------------------|
| **Latency** | 1,200ms to 3,000ms | 10ms to 50ms |
| **Cost per evaluation** | $0.01 to $0.05 | Near zero (compute only) |
| **Deployment** | Cloud API, data leaves VPC | Edge, sidecar, or in-process |
| **Throughput** | Limited by API rate limits | Limited by your hardware |
| **Privacy** | Data traverses the network | Data stays in execution memory |
| **Domain specificity** | Generalist, may miss financial exploits | Trained on banking-specific attack patterns |

There is also a **recursive failure risk**: large models are generalists. They often miss domain-specific financial exploits like limit structuring, shadow PII probes, or lateral privilege escalation between accounts. A distilled SLM trained specifically on these patterns catches what a generalist overlooks.

For a bank, the distilled SLM is the difference between a security check that feels like a loading spinner and one that feels invisible.

## When to Distill (and When Not To)

Distillation trades generality for speed. It only pays off when the evaluation task is narrow and well-defined.

| Scenario | Distill? | Rationale |
|----------|----------|-----------|
| Agentic tool-call validation | Yes | High volume, low latency required, narrow scope |
| Real-time fraud intervention | Yes | Speed-critical, well-defined patterns |
| Inline prompt injection detection | Yes | Pattern recognition task, speed-critical |
| PII/data exfiltration screening | Yes | Well-defined criteria, privacy-sensitive |
| Complex policy compliance review | No | Requires nuanced reasoning a small model will miss |
| Novel threat detection | No | Needs the large model's broad world knowledge |
| Low-volume batch audit | No | Async large model is fine, cost is low |

!!! tip "Rule of thumb"
    If you can write a rubric a junior analyst could follow, the task is a good distillation candidate. If it requires expert judgment on novel situations, keep the large model.

## The Security Sidecar Architecture

The SLM does not run as a separate API call. It deploys as a **sidecar** directly alongside the agent, intercepting actions in-process or in shared memory. In Kubernetes terms, the SLM lives in the same pod as the agent. In simpler environments, it loads as an in-process library.

![Security Sidecar Workflow](../../images/distill-sidecar-workflow.svg){ .arch-diagram }

### How It Works

1. **Intercept.** The agent generates a tool call or response. The sidecar captures the action string in memory before it leaves the local environment.
2. **Policy check.** The SLM evaluates the action against its trained adversarial logic and the bank's policy rules.
3. **Verdict.** The SLM returns GO, NO-GO, or ESCALATE in under 50ms.
4. **Forward or block.** GO actions proceed to the core banking API. NO-GO actions are blocked before they ever hit the network or database. ESCALATE actions are held for the large Judge or a human reviewer.

### Why the Sidecar Wins

**In-memory inspection.** The SLM inspects the action string before it leaves the local network, preventing data exfiltration at the source. Sensitive data never traverses an external API for security evaluation.

**Deterministic latency.** Because the model is small, its inference time is predictable. This allows hard-coded timeouts in the execution pipeline. No more variable 1-to-3-second waits on a cloud Judge API.

**Data sovereignty.** For institutions subject to DORA, GDPR, or data residency requirements, keeping security evaluation local eliminates an entire category of compliance risk.

### Deployment Options

| Pattern | How | Best For |
|---------|-----|----------|
| **Kubernetes sidecar** | Separate container in the same pod | Containerized agent workloads |
| **In-process library** | Loaded into the agent's runtime (ONNX, TensorRT) | Lowest latency, single-process agents |
| **Local inference server** | Lightweight server on the same node (vLLM, Ollama) | Shared across multiple agents on one host |

!!! info "Hardware requirements"
    A 1.5B parameter model quantized to INT4 requires roughly 1GB of RAM and runs comfortably on a single CPU core. GPU acceleration is not required for models at this scale, though it helps if you need sub-10ms latency at high concurrency.

## Reasoning Distillation

The intelligence of the sidecar is not baked in by default. It is **distilled** from a Teacher model using a banking-specific adversarial curriculum.

![Reasoning Distillation: From Teacher to Student](../../images/distill-reasoning-loop.svg){ .arch-diagram }

### Roles

**The Teacher:** A frontier model such as GPT-4o, Claude Sonnet, or equivalent. Deep understanding of nuance, policy, and context. Expensive to run at scale.

**The Student:** A 1.5B to 3B parameter model: Phi-4 Mini, Gemma 2, Qwen 1.5B, or a specialized encoder like a DeBERTa variant. Cheap, fast, deployable anywhere.

### The Adversarial Curriculum

The Teacher is not fed generic examples. It receives a structured curriculum of banking-specific attack patterns:

| Curriculum Category | What the Teacher Labels | Why It Matters |
|--------------------|-----------------------|----------------|
| **Lateral privilege escalation** | Attempts to bridge account permissions | Agent asked to transfer from an unauthorized secondary account |
| **Compliance bypass (structuring)** | Breaking large transactions into smaller ones to evade AML limits | Pattern invisible to generic prompt injection detectors |
| **Inference attacks** | Repeated probing to guess sensitive internal IDs | Low-signal attacks that accumulate over a session |
| **Shadow PII extraction** | Indirect requests for personally identifiable information | "What was the name on the last rejected transaction?" |
| **Payee injection** | Unauthorized recipients inserted into payment flows | Tool call targeting a payee not in the verified list |
| **Temporal manipulation** | Exploiting time-based controls | Scheduling actions for low-oversight or batch-processing windows |
| **Privilege escalation via tool chaining** | Combining permitted tools to achieve an unpermitted outcome | Read-only query result fed into a write tool |

### The Three-Step Process

**Step 1: Synthetic data generation.** Feed the Teacher thousands of realistic examples from the adversarial curriculum, plus a majority of legitimate actions. Use your own production logs (scrubbed of real PII) as seed material. The Teacher labels each example.

**Step 2: Rationalization.** Do not ask the Teacher for a bare Pass/Fail. Ask it to explain *why*. For example: "This tool call is rejected because it attempts to access a secondary account without a transit token." This reasoning becomes training signal. The Student learns to predict the **reasoning path**, not just the output.

**Step 3: Fine-tuning.** Train the Student to predict both the verdict and the reasoning. The Student learns not just "reject this" but "reject this because it matches pattern X." This makes the Student's decisions auditable and its errors diagnosable.

```text
Teacher input:  tool_call(transfer, amount=50000, target=external_account_id)
Teacher output: REJECT — Transfer exceeds session limit and targets
                an account not in the user's verified payee list.
                Matches pattern: unauthorized-payee-escalation.

Student learns: verdict + reasoning + pattern tag
```

Chain-of-thought distillation produces significantly more accurate small models than binary label transfer alone. A Student trained on reasoning chains understands *why* an action is a risk, making it more resilient to novel prompt injections that rearrange familiar attack components.

!!! warning "Training data quality matters more than model size"
    A 1.5B model trained on 50,000 high-quality, Teacher-rationalized examples will outperform a 3B model trained on 200,000 bare labels. Invest in the Teacher's reasoning, not in raw volume.

### Dataset Composition

A well-balanced training set for a banking security SLM:

| Category | Proportion | Rationale |
|----------|-----------|-----------|
| Legitimate actions (clean) | 60% | Model must not over-flag normal behaviour |
| Known attack patterns | 20% | Core detection capability from the adversarial curriculum |
| Edge cases and ambiguous actions | 15% | Where the Teacher's reasoning is most valuable |
| Adversarial variations of known attacks | 5% | Robustness against mutation |

Target a minimum of 30,000 labeled examples for a production deployment, with at least 10,000 covering the attack and edge-case categories.

## The 100/1 Reliability Loop

A distilled model is only as good as its training data. Drift happens. New attack patterns emerge. You need a continuous validation loop to keep the SLM honest, and to satisfy internal Model Risk Management (MRM) teams and external auditors who will rightly ask: "How do you know the small model is still accurate?"

The answer is the **100/1 strategy**: check everything fast, then verify a sample thoroughly.

![The 100/1 Reliability Loop](../../images/distill-reliability-loop.svg){ .arch-diagram }

### How It Works

| Layer | Coverage | Purpose |
|-------|----------|---------|
| **SLM (inline)** | 100% of actions | Real-time screening, sub-50ms |
| **Teacher / Large Judge (async)** | 1% random sample + 100% of blocked actions | Verify SLM accuracy, catch drift |
| **Human review** | All SLM/Teacher disagreements | Ground truth, edge case learning, audit evidence |

### The Feedback Cycle

1. The SLM evaluates every action inline.
2. A random 1% of passed actions (and 100% of blocked actions) are sent asynchronously to the Teacher for a "master review."
3. The Teacher generates its own verdict and reasoning chain.
4. If the SLM and Teacher **agree**, the result is logged as confirmed.
5. If they **disagree**, the case is flagged as a **control failure** and routed to human review.
6. Human-reviewed cases feed back into the next training cycle as new labeled examples.
7. If the SLM's agreement rate with the Teacher drops below a threshold (e.g., 99.5%), trigger an automatic retraining cycle.

This is the same principle as the [sampling strategy](model-as-judge-implementation.md#sampling-strategy) described in the Judge implementation guide, applied to the SLM rather than to the primary AI's output.

!!! tip "Start in shadow mode"
    When first deploying a distilled SLM, run it in shadow mode: let it evaluate every action, but do not let it block anything. Compare its verdicts against the large Judge for two to four weeks. Only switch to enforcement mode once you have confidence in its accuracy on your production traffic.

## Regulatory Alignment

This architecture maps directly to the regulatory frameworks that matter for financial institutions in 2026.

### Treasury FS-AI RMF (2026)

| Control Objective | How the SLM Architecture Satisfies It |
|-------------------|--------------------------------------|
| **CO 4.2: Adversarial Testing** | The adversarial curriculum is built from structured attack categories. The Teacher generates labeled adversarial examples. The SLM is red-teamed before deployment. |
| **CO 6.1: Continuous Performance Monitoring** | The 100/1 loop provides continuous monitoring. Agreement rate, false negative rate, and drift metrics are tracked and alerted on. |

### EU DORA (Digital Operational Resilience Act)

| Requirement | How the SLM Architecture Satisfies It |
|-------------|--------------------------------------|
| **Detection and containment** | The sidecar provides a real-time kill-switch for ICT-related incidents caused by AI. NO-GO verdicts block harmful actions before they reach core systems. |
| **Testing of digital resilience** | The adversarial curriculum and the 100/1 verification loop serve as continuous resilience testing. |
| **Third-party ICT risk** | Local deployment eliminates dependency on external AI APIs for security evaluation, reducing third-party ICT concentration risk. |

### NIST AI RMF 1.0

| Function | How the SLM Architecture Provides Evidence |
|----------|-------------------------------------------|
| **GOVERN** | The 100/1 loop establishes measurable governance over the SLM. Human review of disagreements maintains accountability. |
| **MAP** | The adversarial curriculum documents known risk categories. Dataset composition records the scope of the SLM's training. |
| **MEASURE** | Agreement rate, false negative rate, and drift metrics provide continuous measurement against human ground truth. |
| **MANAGE** | Automatic retraining triggers and the escalation path (SLM to Teacher to human) provide graduated risk management. |

For detailed NIST mappings, see the [NIST AI RMF infrastructure mapping](../../infrastructure/mappings/nist-ai-rmf.md).

## Limitations and Risks

Distillation is powerful, but it is not a silver bullet. Be honest about what the SLM cannot do.

| Limitation | Mitigation |
|------------|-----------|
| **Narrow scope.** The SLM only catches what it was trained on. | Continuous retraining with new patterns. Large Judge covers the long tail. |
| **No novel reasoning.** It pattern-matches; it does not think. | Escalate uncertain cases to the large model. |
| **Training data bias.** If the Teacher was wrong, the Student inherits those errors. | Human review of disagreements. Regular gold-standard recalibration. |
| **Model drift.** Production traffic shifts over time. | Automated drift detection via the 100/1 loop. |
| **Adversarial robustness.** Small models are easier to fool with targeted attacks. | Red-team the SLM specifically. Treat it as a first line, not the only line. |
| **Recursive failure.** The Teacher may share blind spots with the primary AI. | Use a Teacher from a different model family than the primary agent. See [Judge Model Selection](judge-model-selection.md). |

!!! warning "The SLM is a first line of defence, not the last"
    The distilled model replaces the large Judge for routine, high-volume screening. It does not replace the large Judge entirely. The large model remains the backstop for sampled verification, escalated cases, and novel threat patterns.

## Integration with the AIRS Control Stack

The distilled SLM slots into the existing [control layers](model-as-judge-implementation.md#integration-with-controls) as a fast, inline evaluation tier:

| Layer | Function | Timing | Model |
|-------|----------|--------|-------|
| **Input guardrails** | Block known-bad inputs | Inline, pre-execution | Rules / classifier |
| **Distilled SLM** | Screen actions for security patterns | Inline, pre-execution | 1.5B to 3B local model |
| **Output guardrails** | Filter known-bad outputs | Inline, post-execution | Rules / classifier |
| **Large Judge** | Assurance, drift detection, sampled audit | Async, after-the-fact | Frontier LLM |
| **Human oversight** | Decision-making, accountability | As needed | Human |

The SLM does not replace guardrails. Guardrails handle deterministic, rule-based checks (regex, blocklists, format validation). The SLM handles the fuzzy, contextual checks that rules cannot express but that do not require the full weight of a frontier model.

## Cost Impact

Adding an SLM layer changes the economics of action-by-action evaluation significantly. Compare against the [cost and latency analysis](cost-and-latency.md) for the standard pattern.

| Approach | Cost at 1M evaluations/month | Latency per check |
|----------|----------------------------|--------------------|
| Large Judge on 100% of actions | $10,000 to $50,000 | 1,200ms to 3,000ms |
| Large Judge on 5% sample only | $500 to $2,500 | N/A (async) |
| **SLM on 100% + Teacher on 1% sample** | **$100 to $500 + compute** | **10ms to 50ms inline** |

The SLM approach gives you 100% inline coverage at a fraction of the cost of sampled-only coverage with a large model, while adding real-time blocking capability that sampling alone cannot provide.

For a CTO worried about the cloud bill, this is an easier conversation: the security layer costs less than the agent it protects.

## Summary

Distillation turns the Judge from an after-the-fact auditor into a real-time security sensor. The large model's reasoning is compressed into a small, fast, private model that screens every action inline. The large model stays in the loop as a sampled verifier, catching drift and covering the long tail of novel threats.

**The key trade-off:** You give up generality for speed. The SLM is a specialist. It catches what it was trained on, fast and cheap. Everything else escalates.

For agentic systems that take real-world actions at machine speed, this is often the right trade-off. It is the difference between security that slows the system down and security that the system never notices.

!!! info "References"
    - [Distilling Step-by-Step: Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes](https://arxiv.org/abs/2305.02301) (Hsieh et al., 2023)
    - [Knowledge Distillation of Large Language Models](https://arxiv.org/abs/2306.08543) (Gu et al., 2024)
    - [TinyBERT: Distilling BERT for Natural Language Understanding](https://arxiv.org/abs/1909.10351) (Jiao et al., 2020)
    - [U.S. Treasury: Financial Services AI Risk Management Framework](https://home.treasury.gov/), 2026
    - [DORA: Digital Operational Resilience Act](https://www.digital-operational-resilience-act.com/)
    - [NIST AI RMF 1.0](https://www.nist.gov/artificial-intelligence/risk-management-framework)
    - [Judge Model Selection](judge-model-selection.md), AI Runtime Security
    - [Model-as-Judge Implementation](model-as-judge-implementation.md), AI Runtime Security
    - [Cost and Latency](cost-and-latency.md), AI Runtime Security
