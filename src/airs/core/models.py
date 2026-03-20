"""Core data models for the AIRS framework.

Defines the fundamental types: risk tiers, PACE states, control layers,
and the verdict/decision schemas that flow between layers.
"""

from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class RiskTier(str, Enum):
    """Risk classification for an AI deployment.

    Determines which controls are required and at what stringency.
    Classification is based on use-case context, not the model itself.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PACEState(str, Enum):
    """PACE resilience state — structured degradation model.

    P - Primary:     All controls active, normal operation.
    A - Alternate:   One control degraded, backup active, scope tightened.
    C - Contingency: Multiple controls degraded, human-in-the-loop for all.
    E - Emergency:   Confirmed compromise, circuit breaker fires, full stop.
    """

    PRIMARY = "primary"
    ALTERNATE = "alternate"
    CONTINGENCY = "contingency"
    EMERGENCY = "emergency"


class ControlLayer(str, Enum):
    """The four layers of the AIRS defense model."""

    GUARDRAIL = "guardrail"
    JUDGE = "judge"
    HUMAN = "human"
    CIRCUIT_BREAKER = "circuit_breaker"


class GuardrailVerdict(str, Enum):
    """Outcome of a guardrail (Layer 1) evaluation."""

    PASS = "pass"
    BLOCK = "block"
    FLAG = "flag"  # pass-through but flag for judge


class JudgeVerdict(str, Enum):
    """Outcome of an Model-as-Judge (Layer 2) evaluation."""

    PASS = "pass"
    REVIEW = "review"  # queue for human review
    ESCALATE = "escalate"  # immediate escalation


# ---------------------------------------------------------------------------
# Schemas — the interface contracts between layers
# ---------------------------------------------------------------------------

class AIRequest(BaseModel):
    """Inbound request to an AI system, as seen by the security pipeline."""

    request_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    input_text: str
    model: str = ""
    user_id: str = ""
    session_id: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)

    # Agent context for multi-agent identity propagation (optional).
    # When set, the pipeline includes agent chain info in telemetry events.
    agent_context: Any | None = None  # airs.agents.identity.AgentContext


class AIResponse(BaseModel):
    """Outbound response from an AI system, before security evaluation."""

    request_id: str
    output_text: str
    model: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class LayerResult(BaseModel):
    """Result of a single security layer evaluation.

    This is the universal interface contract: every layer emits one of these.
    """

    layer: ControlLayer
    passed: bool
    verdict: str  # layer-specific verdict enum value
    reason: str = ""
    confidence: float = 1.0  # 0.0–1.0, relevant for judge layer
    latency_ms: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class PipelineResult(BaseModel):
    """Aggregate result of the full security pipeline evaluation."""

    request_id: str
    allowed: bool
    pace_state: PACEState = PACEState.PRIMARY
    layer_results: list[LayerResult] = Field(default_factory=list)
    blocked_by: ControlLayer | None = None
    total_latency_ms: float = 0.0

    @property
    def guardrail_result(self) -> LayerResult | None:
        return next((r for r in self.layer_results if r.layer == ControlLayer.GUARDRAIL), None)

    @property
    def judge_result(self) -> LayerResult | None:
        return next((r for r in self.layer_results if r.layer == ControlLayer.JUDGE), None)


# ---------------------------------------------------------------------------
# Objective Intent — developer-declared behavioral contracts
# ---------------------------------------------------------------------------

class IntentEvaluationLevel(str, Enum):
    """The level at which intent evaluation operates."""

    TACTICAL = "tactical"      # single agent against its OISpec
    STRATEGIC = "strategic"    # aggregate agents against workflow OISpec
    JUDGE = "judge"            # judge against its own OISpec


class IntentEvaluationFrequency(str, Enum):
    """How often an agent's actions are evaluated against its OISpec."""

    EVERY_ACTION = "every_action"
    PER_PHASE = "per_phase"
    POST_EXECUTION = "post_execution"


class IntentViolationSeverity(str, Enum):
    """Severity of an OISpec violation."""

    LOW = "low"          # minor deviation, log only
    MEDIUM = "medium"    # notable deviation, flag for review
    HIGH = "high"        # material violation, escalate
    CRITICAL = "critical"  # severe violation, quarantine output


class ObjectiveIntentSpec(BaseModel):
    """Objective Intent Specification (OISpec) — a developer-declared
    behavioral contract for an agent, judge, or workflow.

    Consumed by tactical judges, strategic evaluators, and the
    judge meta-evaluator to assess whether actual behavior aligns
    with declared purpose.
    """

    oisspec_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    oisspec_version: str = "1.0"
    agent_id: str
    agent_role: str = ""  # "task", "orchestrator", "evaluator", "observer"
    created_by: str = ""
    version: int = 1

    # What the agent is supposed to accomplish
    goal: str
    success_criteria: list[str] = Field(default_factory=list)
    failure_criteria: list[str] = Field(default_factory=list)

    # Operational parameters
    permitted_tools: list[str] = Field(default_factory=list)
    prohibited_actions: list[str] = Field(default_factory=list)
    data_scope: str = ""
    output_constraints: dict[str, Any] = Field(default_factory=dict)

    # Authority boundaries
    can_delegate: bool = False
    max_delegation_depth: int = 0
    can_create_agents: bool = False
    can_modify_workflow: bool = False

    # Evaluation configuration
    risk_classification: RiskTier = RiskTier.MEDIUM
    evaluation_frequency: IntentEvaluationFrequency = IntentEvaluationFrequency.PER_PHASE

    # Integrity
    oisspec_hash: str = ""
    timestamp: float = Field(default_factory=time.time)
    metadata: dict[str, Any] = Field(default_factory=dict)


class IntentEvaluationResult(BaseModel):
    """Result of evaluating an agent's behavior against its OISpec."""

    evaluation_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    oisspec_id: str
    agent_id: str
    evaluation_level: IntentEvaluationLevel
    compliant: bool
    alignment_score: float = 1.0  # 0.0–1.0
    violations: list[str] = Field(default_factory=list)
    violation_severity: IntentViolationSeverity = IntentViolationSeverity.LOW
    reason: str = ""
    timestamp: float = Field(default_factory=time.time)
    metadata: dict[str, Any] = Field(default_factory=dict)
