# AIRS Python SDK

**Turn the framework into running code.**

The AIRS Python SDK implements the three-layer security architecture as a drop-in library for Python AI applications. Instead of reading about controls, you can `pip install` them.

## Bring Your Own Model

The SDK is **model-agnostic**. It does not call AI models for you — it wraps security controls *around* your existing model calls. You continue using whatever model, provider, or framework you already have:

```python
# 1. AIRS checks the input
input_result = await pipeline.evaluate_input(request)

# 2. You call YOUR model — OpenAI, Anthropic, Bedrock, Ollama, local, anything
ai_output = await your_model(request.input_text)

# 3. AIRS checks the output
output_result = await pipeline.evaluate_output(request, response)
```

AIRS only sees the text going in and the text coming out. It doesn't know or care which model you're using, how you're calling it, or what framework it runs on. This means it works with:

- **Any model provider** — OpenAI, Anthropic, Google, Mistral, Cohere, local models
- **Any framework** — LangChain, LlamaIndex, Haystack, raw API calls
- **Any architecture** — single model, RAG, agents, multi-agent orchestration

The one exception is the optional **LLM-as-Judge**, which does call an OpenAI-compatible API to *evaluate* outputs. This is the judge model — a separate, independent model used for security evaluation, not your production model.

## What It Provides

| Component | What It Does |
|-----------|-------------|
| **Guardrails** | Regex-based prompt injection detection, PII filtering, content policy — extensible |
| **LLM-as-Judge** | Rule-based (no API key) or LLM-based (OpenAI-compatible) output evaluation |
| **Circuit Breaker** | Sliding-window failure tracking, auto-trip, manual emergency stop, recovery |
| **PACE Controller** | State machine for structured degradation (Primary → Alternate → Contingency → Emergency) |
| **Security Pipeline** | Orchestrates all layers with configurable behavior per PACE state |
| **CLI Assessment** | Interactive tool that classifies your deployment and recommends controls |
| **FastAPI Middleware** | Drop-in middleware that protects AI endpoints automatically |

## Install

```bash
# Clone the repository
git clone https://github.com/JonathanCGill/ai-runtime-behavior-security.git
cd ai-runtime-behavior-security

# Install core (guardrails, circuit breaker, PACE, CLI)
pip install .

# With FastAPI middleware
pip install ".[fastapi]"

# With LLM-as-Judge (requires OpenAI-compatible API)
pip install ".[judge]"

# Everything
pip install ".[all]"
```

!!! tip "No external dependencies for core"
    The core SDK (guardrails, circuit breaker, PACE) requires only `pydantic`, `rich`, and `typer`. No API keys or external services needed to get started.

## 5-Minute Quick Start

```python
import asyncio
from airs.core.models import AIRequest, AIResponse
from airs.runtime import (
    SecurityPipeline, GuardrailChain, RegexGuardrail,
    CircuitBreaker, PACEController,
)

async def main():
    # Build the pipeline
    pipeline = SecurityPipeline(
        guardrails=GuardrailChain([RegexGuardrail()]),
        circuit_breaker=CircuitBreaker(),
        pace=PACEController(),
    )

    # Evaluate input before calling your model
    request = AIRequest(input_text="What is the capital of France?")
    input_result = await pipeline.evaluate_input(request)

    if not input_result.allowed:
        print(f"Blocked: {input_result.blocked_by}")
        return

    # Call your AI model (replace with your actual model call)
    ai_output = "The capital of France is Paris."

    # Evaluate output before returning to user
    response = AIResponse(request_id=request.request_id, output_text=ai_output)
    output_result = await pipeline.evaluate_output(request, response)

    if output_result.allowed:
        print(ai_output)
    else:
        print(f"Response blocked: {output_result.blocked_by}")

asyncio.run(main())
```

## CLI Assessment

Classify your deployment and get a prioritized implementation plan:

```bash
airs assess
```

The tool asks about your deployment context — audience, data sensitivity, autonomy, architecture — and outputs:

- **Risk tier** (LOW / MEDIUM / HIGH / CRITICAL)
- **Risk factors and mitigations** specific to your deployment
- **PACE resilience posture** — what happens at each degradation level
- **Prioritized control list** — what to implement first
- **Code snippet** to get started

For machine-readable output:

```bash
airs assess --json
```

## What's Next

| Guide | Description |
|-------|-------------|
| [Guardrails](guardrails.md) | Layer 1 — input/output filtering, custom guardrails, chaining |
| [Judge](judge.md) | Layer 2 — rule-based and LLM-based evaluation |
| [Circuit Breaker & PACE](resilience.md) | Emergency stop and structured degradation |
| [Pipeline](pipeline.md) | Full pipeline orchestration and configuration |
| [FastAPI Integration](fastapi.md) | Drop-in middleware for FastAPI apps |
| [Examples](examples.md) | Complete working examples |

## Architecture

![AIRS Security Pipeline](../images/sdk-pipeline-architecture.svg)

## Project Structure

```
src/airs/
├── cli/
│   ├── __init__.py          # CLI app setup
│   └── assess.py            # Interactive assessment
├── core/
│   ├── models.py            # RiskTier, PACEState, AIRequest, LayerResult
│   ├── controls.py          # 25+ controls in queryable registry
│   └── risk.py              # Risk classification engine
├── runtime/
│   ├── guardrail.py         # Layer 1: Regex, ContentPolicy, Chain
│   ├── judge.py             # Layer 2: RuleBased, LLM
│   ├── circuit_breaker.py   # Emergency stop
│   ├── pace.py              # PACE state machine
│   └── pipeline.py          # Full pipeline orchestrator
└── integrations/
    └── fastapi.py           # Drop-in middleware

tests/                       # 52 tests
examples/
├── quickstart.py            # Minimal working example
└── fastapi_app.py           # Complete FastAPI app
```

## Running Tests

```bash
pip install ".[dev]"
pytest tests/ -v
```
