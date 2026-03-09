"""Structured security event schema.

Every security-relevant action emits an AISecurityEvent with a fixed
schema.  This is the AIRS equivalent of an OpenTelemetry span — a
single, self-contained record of what happened and why.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Types of security events emitted by the pipeline."""

    GUARDRAIL_INPUT = "guardrail.input"
    GUARDRAIL_OUTPUT = "guardrail.output"
    JUDGE_DECISION = "judge.decision"
    TOOL_POLICY = "tool.policy"
    DELEGATION = "delegation"
    PACE_TRANSITION = "pace.transition"
    CIRCUIT_BREAKER = "circuit_breaker.state_change"
    PIPELINE_INPUT = "pipeline.input"
    PIPELINE_OUTPUT = "pipeline.output"


class AISecurityEvent(BaseModel):
    """A single structured security event.

    Designed for SOC ingestion: every field is typed, every event
    has a correlation ID, and the agent chain is always present.
    """

    # Identity
    event_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    event_type: EventType
    timestamp: float = Field(default_factory=time.time)

    # Correlation
    correlation_id: str = ""   # ties events across the full request
    request_id: str = ""       # ties events to a specific AIRequest

    # Agent chain (who did this)
    user_id: str = ""
    agent_chain: list[str] = Field(default_factory=list)  # list of agent IDs
    delegation_depth: int = 0

    # Decision
    allowed: bool = True
    verdict: str = ""          # layer-specific verdict value
    reason: str = ""
    confidence: float = 1.0

    # Context
    layer: str = ""            # which control layer
    tool_name: str = ""        # for tool policy events
    pace_state: str = ""       # current PACE state
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_json(self) -> str:
        """Serialize to a JSON string for log shipping."""
        return self.model_dump_json()

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dict for programmatic access."""
        return self.model_dump()


# ---------------------------------------------------------------------------
# Module-level emitter — thin global hook for pipeline integration
# ---------------------------------------------------------------------------

_sinks: list[Any] = []  # list of AuditSink instances


def register_sink(sink: Any) -> None:
    """Register a global audit sink. Events are sent to all registered sinks."""
    _sinks.append(sink)


def clear_sinks() -> None:
    """Remove all registered sinks."""
    _sinks.clear()


def emit(event: AISecurityEvent) -> None:
    """Emit a security event to all registered sinks.

    If no sinks are registered, the event is logged at DEBUG level
    as structured JSON — ensuring events are never silently lost.
    """
    if _sinks:
        for sink in _sinks:
            try:
                sink.handle(event)
            except Exception:
                logger.exception("Audit sink error for event %s", event.event_id)
    else:
        logger.debug("airs.security_event: %s", event.to_json())
