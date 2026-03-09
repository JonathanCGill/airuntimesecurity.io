"""Security Pipeline — orchestrates the three-layer architecture.

    Input → [Guardrail] → Model → [Guardrail] → [Judge] → [Human?] → Output
                                                              ↑
                                                    Circuit Breaker monitors all

This is the main entry point for integrating AIRS into an AI application.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Callable

from pydantic import BaseModel

from airs.core.models import (
    AIRequest,
    AIResponse,
    ControlLayer,
    GuardrailVerdict,
    JudgeVerdict,
    LayerResult,
    PACEState,
    PipelineResult,
)
from airs.runtime.circuit_breaker import CircuitBreaker, CircuitState
from airs.runtime.guardrail import GuardrailChain
from airs.runtime.judge import Judge, RuleBasedJudge
from airs.runtime.pace import PACEController
from airs.telemetry.events import AISecurityEvent, EventType, emit

logger = logging.getLogger(__name__)


class PipelineConfig(BaseModel):
    """Configuration for the security pipeline."""

    # Whether to run guardrails on input
    input_guardrails: bool = True
    # Whether to run guardrails on output
    output_guardrails: bool = True
    # Whether to run the judge (controlled by PACE if enabled)
    judge_enabled: bool = True
    # Whether PACE state controls judge behavior
    pace_enabled: bool = True
    # Fallback response when circuit breaker is open
    fallback_response: str = (
        "This service is temporarily unavailable. "
        "Your request has been logged and will be processed when service resumes."
    )
    # Whether to block on judge REVIEW (vs. just logging it)
    block_on_review: bool = False


class SecurityPipeline:
    """The three-layer security pipeline.

    Orchestrates: Guardrails → Judge → Circuit Breaker, with PACE
    controlling the operational posture at each layer.

    Usage:
        # Build the pipeline
        pipeline = SecurityPipeline(
            guardrails=GuardrailChain([RegexGuardrail()]),
            judge=RuleBasedJudge(),
        )

        # Evaluate input
        input_result = await pipeline.evaluate_input(request)
        if not input_result.allowed:
            return blocked_response(input_result)

        # Call your AI model
        response = await call_model(request)

        # Evaluate output
        output_result = await pipeline.evaluate_output(request, response)
        if not output_result.allowed:
            return blocked_response(output_result)

        return response
    """

    def __init__(
        self,
        guardrails: GuardrailChain | None = None,
        judge: Judge | None = None,
        circuit_breaker: CircuitBreaker | None = None,
        pace: PACEController | None = None,
        config: PipelineConfig | None = None,
        on_block: Callable[[PipelineResult], None] | None = None,
        on_escalate: Callable[[PipelineResult], None] | None = None,
    ) -> None:
        self.guardrails = guardrails or GuardrailChain()
        self.judge = judge or RuleBasedJudge()
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self.pace = pace or PACEController()
        self.config = config or PipelineConfig()
        self._on_block = on_block
        self._on_escalate = on_escalate

    def _emit(
        self,
        event_type: EventType,
        request: AIRequest,
        result: PipelineResult,
    ) -> None:
        """Emit a structured telemetry event for a pipeline evaluation."""
        ctx = request.agent_context
        emit(AISecurityEvent(
            event_type=event_type,
            correlation_id=ctx.correlation_id if ctx else "",
            request_id=request.request_id,
            user_id=ctx.user_id if ctx else request.user_id,
            agent_chain=ctx.chain_ids if ctx else [],
            delegation_depth=ctx.delegation_depth if ctx else 0,
            allowed=result.allowed,
            verdict=result.blocked_by.value if result.blocked_by else "pass",
            reason=(
                result.layer_results[-1].reason
                if result.layer_results else ""
            ),
            layer=result.blocked_by.value if result.blocked_by else "",
            pace_state=result.pace_state.value,
        ))

    async def evaluate_input(self, request: AIRequest) -> PipelineResult:
        """Evaluate an inbound request through the security pipeline."""
        start = time.monotonic()
        layers: list[LayerResult] = []

        # Circuit breaker check
        if not self.circuit_breaker.allow_request():
            return PipelineResult(
                request_id=request.request_id,
                allowed=False,
                pace_state=self.pace.state,
                blocked_by=ControlLayer.CIRCUIT_BREAKER,
                layer_results=[
                    LayerResult(
                        layer=ControlLayer.CIRCUIT_BREAKER,
                        passed=False,
                        verdict="open",
                        reason="Circuit breaker is open — AI traffic blocked",
                    )
                ],
                total_latency_ms=(time.monotonic() - start) * 1000,
            )

        # Layer 1: Input guardrails
        if self.config.input_guardrails:
            gr_result = self.guardrails.check_input(request.input_text)
            layers.append(gr_result)

            if not gr_result.passed:
                self.circuit_breaker.record_failure("input_guardrail_block")
                result = PipelineResult(
                    request_id=request.request_id,
                    allowed=False,
                    pace_state=self.pace.state,
                    layer_results=layers,
                    blocked_by=ControlLayer.GUARDRAIL,
                    total_latency_ms=(time.monotonic() - start) * 1000,
                )
                if self._on_block:
                    self._on_block(result)
                self._emit(EventType.PIPELINE_INPUT, request, result)
                return result

        self.circuit_breaker.record_success()
        result = PipelineResult(
            request_id=request.request_id,
            allowed=True,
            pace_state=self.pace.state,
            layer_results=layers,
            total_latency_ms=(time.monotonic() - start) * 1000,
        )
        self._emit(EventType.PIPELINE_INPUT, request, result)
        return result

    async def evaluate_output(
        self,
        request: AIRequest,
        response: AIResponse,
    ) -> PipelineResult:
        """Evaluate an outbound response through the security pipeline."""
        start = time.monotonic()
        layers: list[LayerResult] = []
        result: PipelineResult | None = None

        # Layer 1: Output guardrails
        if self.config.output_guardrails:
            gr_result = self.guardrails.check_output(response.output_text)
            layers.append(gr_result)

            if not gr_result.passed:
                self.circuit_breaker.record_failure("output_guardrail_block")
                result = PipelineResult(
                    request_id=request.request_id,
                    allowed=False,
                    pace_state=self.pace.state,
                    layer_results=layers,
                    blocked_by=ControlLayer.GUARDRAIL,
                    total_latency_ms=(time.monotonic() - start) * 1000,
                )
                if self._on_block:
                    self._on_block(result)

        # Layer 2: Judge (controlled by PACE)
        if result is None:
            should_judge = (
                self.config.judge_enabled
                and (not self.config.pace_enabled or self.pace.should_judge())
            )

            # Also judge if guardrails flagged (regardless of sampling)
            if (
                not should_judge
                and layers
                and layers[0].verdict == GuardrailVerdict.FLAG.value
            ):
                should_judge = True

            if should_judge:
                judge_result = await self.judge.to_layer_result(
                    request.input_text, response.output_text
                )
                layers.append(judge_result)

                if judge_result.verdict == JudgeVerdict.ESCALATE.value:
                    self.circuit_breaker.record_failure("judge_escalate")
                    if self.config.pace_enabled:
                        self.pace.escalate("Judge escalation")

                    result = PipelineResult(
                        request_id=request.request_id,
                        allowed=False,
                        pace_state=self.pace.state,
                        layer_results=layers,
                        blocked_by=ControlLayer.JUDGE,
                        total_latency_ms=(time.monotonic() - start) * 1000,
                    )
                    if self._on_escalate:
                        self._on_escalate(result)

                elif (
                    judge_result.verdict == JudgeVerdict.REVIEW.value
                    and self.config.block_on_review
                ):
                    result = PipelineResult(
                        request_id=request.request_id,
                        allowed=False,
                        pace_state=self.pace.state,
                        layer_results=layers,
                        blocked_by=ControlLayer.JUDGE,
                        total_latency_ms=(time.monotonic() - start) * 1000,
                    )
                    if self._on_escalate:
                        self._on_escalate(result)

        # Layer 3: Human approval check (PACE-driven)
        if result is None and self.config.pace_enabled and self.pace.requires_human_approval():
            layers.append(
                LayerResult(
                    layer=ControlLayer.HUMAN,
                    passed=False,
                    verdict="pending",
                    reason="PACE state requires human approval — queued for review",
                )
            )
            result = PipelineResult(
                request_id=request.request_id,
                allowed=False,
                pace_state=self.pace.state,
                layer_results=layers,
                blocked_by=ControlLayer.HUMAN,
                total_latency_ms=(time.monotonic() - start) * 1000,
            )

        # All layers passed
        if result is None:
            self.circuit_breaker.record_success()
            result = PipelineResult(
                request_id=request.request_id,
                allowed=True,
                pace_state=self.pace.state,
                layer_results=layers,
                total_latency_ms=(time.monotonic() - start) * 1000,
            )

        self._emit(EventType.PIPELINE_OUTPUT, request, result)
        return result
