"""Objective Intent registry and evaluation support.

Developer-declared intent specifications (OISpecs) define what each agent,
judge, and workflow is supposed to accomplish and within what parameters.
This module provides the registry that stores OISpecs and the types that
support tactical, strategic, and judge-level intent evaluation.

Usage:
    registry = IntentRegistry()

    # Register an agent's OISpec
    spec = ObjectiveIntentSpec(
        agent_id="agent-analyst-01",
        agent_role="task",
        goal="Analyse market data and produce a risk score",
        success_criteria=["Risk score traceable to data points"],
        failure_criteria=["Score produced without citing sources"],
        permitted_tools=["market-data-api"],
        risk_classification=RiskTier.HIGH,
        evaluation_frequency=IntentEvaluationFrequency.EVERY_ACTION,
    )
    registry.register(spec)

    # Register a workflow OISpec that aggregates agent intents
    workflow = WorkflowIntentSpec(
        workflow_id="portfolio-risk-assessment",
        goal="Produce risk assessment for portfolio X",
        agent_oisspec_ids=["oisspec-analyst", "oisspec-sentiment"],
        aggregate_success_criteria=["Final output internally consistent"],
    )
    registry.register_workflow(workflow)

    # Check intent coverage before execution
    gaps = registry.check_coverage(workflow)
"""

from __future__ import annotations

import time
import uuid
from typing import Any

from pydantic import BaseModel, Field

from airs.core.models import (
    IntentEvaluationFrequency,
    IntentEvaluationLevel,
    IntentViolationSeverity,
    ObjectiveIntentSpec,
    RiskTier,
)


class WorkflowIntentSpec(BaseModel):
    """Workflow-level Objective Intent Specification.

    Aggregates individual agent OISpecs and defines the success/failure
    criteria for the workflow as a whole.  Used by the strategic
    evaluation agent to assess whether combined agent actions satisfy
    the declared workflow objective.
    """

    workflow_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    workflow_name: str = ""
    created_by: str = ""
    version: int = 1

    # What the workflow as a whole should achieve
    goal: str
    aggregate_success_criteria: list[str] = Field(default_factory=list)
    aggregate_failure_criteria: list[str] = Field(default_factory=list)

    # References to participating agent and judge OISpecs
    agent_oisspec_ids: list[str] = Field(default_factory=list)
    judge_oisspec_ids: list[str] = Field(default_factory=list)

    # Evaluation configuration
    tactical_evaluation: IntentEvaluationFrequency = (
        IntentEvaluationFrequency.EVERY_ACTION
    )
    strategic_evaluation: IntentEvaluationFrequency = (
        IntentEvaluationFrequency.PER_PHASE
    )
    intent_coverage_check: bool = True

    risk_classification: RiskTier = RiskTier.MEDIUM
    timestamp: float = Field(default_factory=time.time)
    metadata: dict[str, Any] = Field(default_factory=dict)


class IntentCoverageGap(BaseModel):
    """A gap identified during intent coverage analysis.

    Represents a workflow success criterion that is not covered
    by any participating agent's OISpec.
    """

    workflow_id: str
    criterion: str
    gap_type: str = "uncovered"  # "uncovered", "partial", "conflicting"
    details: str = ""


class IntentRegistry:
    """In-memory registry for Objective Intent Specifications.

    Stores agent OISpecs and workflow OISpecs and provides coverage
    analysis to identify intent gaps before workflow execution.
    """

    def __init__(self) -> None:
        self._agent_specs: dict[str, ObjectiveIntentSpec] = {}
        self._workflow_specs: dict[str, WorkflowIntentSpec] = {}

    # -- Registration -------------------------------------------------------

    def register(self, spec: ObjectiveIntentSpec) -> None:
        """Register or update an agent/judge OISpec."""
        self._agent_specs[spec.oisspec_id] = spec

    def register_workflow(self, spec: WorkflowIntentSpec) -> None:
        """Register or update a workflow OISpec."""
        self._workflow_specs[spec.workflow_id] = spec

    # -- Lookup -------------------------------------------------------------

    def get_agent_spec(self, oisspec_id: str) -> ObjectiveIntentSpec | None:
        return self._agent_specs.get(oisspec_id)

    def get_by_agent_id(self, agent_id: str) -> ObjectiveIntentSpec | None:
        """Look up an OISpec by the agent it belongs to."""
        for spec in self._agent_specs.values():
            if spec.agent_id == agent_id:
                return spec
        return None

    def get_workflow_spec(self, workflow_id: str) -> WorkflowIntentSpec | None:
        return self._workflow_specs.get(workflow_id)

    # -- Coverage analysis --------------------------------------------------

    def check_coverage(
        self, workflow: WorkflowIntentSpec
    ) -> list[IntentCoverageGap]:
        """Check whether every workflow success criterion is covered by
        at least one participating agent's OISpec.

        Returns a list of coverage gaps.  An empty list means full coverage.
        """
        gaps: list[IntentCoverageGap] = []

        # Collect all agent success criteria text for simple keyword overlap
        agent_criteria_text: list[str] = []
        for oisspec_id in workflow.agent_oisspec_ids:
            spec = self._agent_specs.get(oisspec_id)
            if spec:
                agent_criteria_text.extend(spec.success_criteria)
                agent_criteria_text.append(spec.goal)

        for criterion in workflow.aggregate_success_criteria:
            criterion_lower = criterion.lower()
            # Simple heuristic: check if any agent criterion shares
            # significant keyword overlap.  A production implementation
            # would use semantic similarity.
            covered = any(
                _keyword_overlap(criterion_lower, ac.lower()) >= 0.3
                for ac in agent_criteria_text
            )
            if not covered:
                gaps.append(
                    IntentCoverageGap(
                        workflow_id=workflow.workflow_id,
                        criterion=criterion,
                        gap_type="uncovered",
                        details=(
                            "No participating agent's OISpec covers this "
                            "workflow success criterion."
                        ),
                    )
                )

        return gaps


def _keyword_overlap(a: str, b: str) -> float:
    """Jaccard similarity of word sets — a rough coverage proxy."""
    words_a = set(a.split())
    words_b = set(b.split())
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / len(words_a | words_b)
