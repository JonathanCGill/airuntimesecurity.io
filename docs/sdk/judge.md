# LLM-as-Judge: Layer 2

The Judge catches what guardrails miss. It evaluates AI outputs for subtle policy violations, hallucinations, inappropriate content, and novel attack patterns that can't be detected with pattern matching.

**Key principle: The Judge detects. It doesn't decide.** The Judge outputs `PASS`, `REVIEW`, or `ESCALATE`. Decisions about what to do with `REVIEW` and `ESCALATE` verdicts flow to humans (Layer 3) or automated policy.

## Verdict Types

| Verdict | Meaning | Action |
|---------|---------|--------|
| **PASS** | Output is safe and policy-compliant | Deliver to user |
| **REVIEW** | Uncertain or borderline, needs human review | Queue for review (or log, based on config) |
| **ESCALATE** | Clearly violates policy or is dangerous | Block immediately, alert security team |

## Rule-Based Judge

Start here. No API key needed, no latency, no cost:

```python
from airs.runtime.judge import RuleBasedJudge

judge = RuleBasedJudge(max_output_length=10000)

result = await judge.evaluate(
    input_text="Tell me a story",
    output_text="Here is a normal response.",
)
# result.verdict == JudgeVerdict.PASS
```

The rule-based judge catches:

- **Excessive output length**: outputs exceeding the configured limit get `REVIEW`
- **Refusal-then-comply**: when the model says "I can't do that" but then proceeds to do it anyway (a common jailbreak indicator)

This is useful for:

- Getting started without any external dependencies
- Low-risk deployments where basic checks suffice
- Testing and development environments

## LLM-as-Judge

For production use. Works with any OpenAI-compatible API:

```python
from airs.runtime.judge import LLMJudge

judge = LLMJudge(
    model="gpt-4o-mini",
    api_key="sk-...",               # or set OPENAI_API_KEY env var
)

result = await judge.evaluate(
    input_text="What was our Q3 revenue?",
    output_text="Q3 revenue was $42.7M, up 15% year-over-year.",
    policy="Only provide information verifiable against provided documents.",
)

print(result.verdict)     # JudgeVerdict.REVIEW
print(result.reason)      # "Financial claims without source documents"
print(result.confidence)  # 0.85
```

### Compatible Providers

The `LLMJudge` works with any API that implements the OpenAI chat completions format:

```python
# OpenAI
judge = LLMJudge(model="gpt-4o-mini", api_key="sk-...")

# Ollama (local)
judge = LLMJudge(
    model="llama3",
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # required by client but not validated
)

# Azure OpenAI
judge = LLMJudge(
    model="gpt-4o-mini",
    base_url="https://your-resource.openai.azure.com/openai/deployments/gpt-4o-mini/",
    api_key="your-azure-key",
)

# Any OpenAI-compatible API (vLLM, Together, Groq, etc.)
judge = LLMJudge(
    model="meta-llama/Llama-3-70b",
    base_url="https://api.together.xyz/v1",
    api_key="your-key",
)
```

!!! warning "Use a different model"
    The Judge should be a **different model** from the one being evaluated. Using the same model to judge itself reduces the chance of catching its own errors. Ideally, use a different provider entirely.

### Custom Policy

The default policy checks for hallucination, PII leakage, content policy violations, prompt injection in output, and off-topic responses. Override with your own:

```python
result = await judge.evaluate(
    input_text=user_input,
    output_text=ai_output,
    policy="""
    Evaluate against these rules:
    1. Response must only reference data from the provided knowledge base
    2. No financial advice or predictions
    3. Must include appropriate disclaimers for medical information
    4. Must not reveal internal system details or pricing logic
    """,
)
```

### Custom Prompt Template

For full control over the judge prompt:

```python
judge = LLMJudge(
    model="gpt-4o-mini",
    prompt_template="""You are an expert evaluator for a {domain} application.

## Context
{policy}

## User Query
{input_text}

## AI Response
{output_text}

## Evaluate
Return JSON: {{"verdict": "pass"|"review"|"escalate", "reason": "...", "confidence": 0.0-1.0}}
""",
)
```

The template receives `{policy}`, `{input_text}`, and `{output_text}` as format variables.

## Custom Judge

Implement the `Judge` base class for any evaluation logic:

```python
from airs.runtime.judge import Judge, JudgeEvaluation, JudgeVerdict

class RAGGroundingJudge(Judge):
    """Check if output is grounded in retrieved documents."""

    def __init__(self, similarity_threshold: float = 0.7):
        self.threshold = similarity_threshold

    async def evaluate(self, input_text, output_text, policy="", **kwargs):
        # Get retrieved docs from kwargs
        sources = kwargs.get("sources", [])

        if not sources:
            return JudgeEvaluation(
                verdict=JudgeVerdict.REVIEW,
                reason="No source documents provided for grounding check",
                confidence=0.5,
            )

        # Your grounding logic here
        grounding_score = compute_grounding(output_text, sources)

        if grounding_score < self.threshold:
            return JudgeEvaluation(
                verdict=JudgeVerdict.ESCALATE,
                reason=f"Output not grounded in sources (score: {grounding_score:.2f})",
                confidence=0.9,
            )

        return JudgeEvaluation(
            verdict=JudgeVerdict.PASS,
            reason=f"Output grounded (score: {grounding_score:.2f})",
            confidence=grounding_score,
        )
```

## Judge in the Pipeline

When used within the `SecurityPipeline`, the judge's behavior is controlled by the PACE state:

| PACE State | Judge Behavior |
|------------|---------------|
| **Primary** | 5% sampling (evaluate 1 in 20 requests) |
| **Alternate** | 100% evaluation (every request) |
| **Contingency** | 100% evaluation + human approval required |
| **Emergency** | Disabled (AI is off, circuit breaker active) |

The judge always evaluates if:

- A guardrail **flagged** the request (regardless of sampling rate)
- The pipeline config has `judge_enabled=True` and `pace_enabled=False`

## Judge Deployment Phases

The framework recommends deploying the judge in phases:

1. **Shadow**: Judge evaluates but results are only logged, not acted on. Measure accuracy against human reviews.
2. **Advisory**: Judge verdicts are shown to reviewers as a recommendation but don't block.
3. **Operational**: Judge verdicts drive blocking and escalation.

Use the rule-based judge or FLAG mode guardrails to implement shadow mode without any judge infrastructure.

For latency-critical deployments, shadow mode is also the recommended first step when introducing a [distilled Small Language Model](../../extensions/technical/distill-judge-slm.md) as an inline judge. Run it in shadow alongside the full LLM Judge to validate accuracy before switching to enforcement.
