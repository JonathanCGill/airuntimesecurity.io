"""Agent delegation enforcement.

Prevents unbounded delegation chains, enforces scope boundaries,
and validates that agents stay within their granted permissions.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, Field

from airs.agents.identity import AgentContext, AgentIdentity

logger = logging.getLogger(__name__)


class DelegationPolicy(BaseModel):
    """Policy governing agent-to-agent delegation.

    Usage:
        policy = DelegationPolicy(
            max_depth=3,
            allowed_agent_types=["retriever", "tool-caller"],
            required_scope_keys=["tools"],
        )
    """

    # Maximum delegation depth (0 = no delegation allowed)
    max_depth: int = 5

    # If set, only these agent types may appear in the chain
    allowed_agent_types: list[str] = Field(default_factory=list)

    # Scope keys that must be present in every delegation
    required_scope_keys: list[str] = Field(default_factory=list)

    # Whether the same agent can appear twice in a chain (cycle detection)
    allow_cycles: bool = False


class DelegationResult(BaseModel):
    """Outcome of a delegation check."""

    allowed: bool
    reason: str = ""
    context: AgentContext | None = None


class DelegationEnforcer:
    """Enforces delegation policy on agent contexts.

    Usage:
        enforcer = DelegationEnforcer(policy)

        # Before delegating
        result = enforcer.check_delegation(parent_ctx, child_agent)
        if not result.allowed:
            raise PermissionError(result.reason)
        child_ctx = result.context  # safe to use
    """

    def __init__(self, policy: DelegationPolicy | None = None) -> None:
        self.policy = policy or DelegationPolicy()

    def check_delegation(
        self,
        parent: AgentContext,
        to: AgentIdentity,
        policy_scope: dict[str, Any] | None = None,
    ) -> DelegationResult:
        """Check whether delegation is allowed and return the child context.

        Returns a DelegationResult with allowed=False if any policy
        constraint is violated.
        """
        # Depth check
        new_depth = parent.delegation_depth + 1
        if new_depth > self.policy.max_depth:
            reason = (
                f"Delegation depth {new_depth} exceeds max {self.policy.max_depth}"
            )
            logger.warning(reason)
            return DelegationResult(allowed=False, reason=reason)

        # Agent type check
        if (
            self.policy.allowed_agent_types
            and to.agent_type
            and to.agent_type not in self.policy.allowed_agent_types
        ):
            reason = (
                f"Agent type '{to.agent_type}' not in allowed types: "
                f"{self.policy.allowed_agent_types}"
            )
            logger.warning(reason)
            return DelegationResult(allowed=False, reason=reason)

        # Cycle detection
        if not self.policy.allow_cycles:
            existing_ids = {a.agent_id for a in parent.agent_chain}
            if to.agent_id in existing_ids:
                reason = (
                    f"Cycle detected: agent '{to.agent_id}' already in chain "
                    f"{parent.chain_ids}"
                )
                logger.warning(reason)
                return DelegationResult(allowed=False, reason=reason)

        # Required scope keys
        merged_scope = dict(parent.policy_scope)
        if policy_scope:
            merged_scope.update(policy_scope)
        for key in self.policy.required_scope_keys:
            if key not in merged_scope:
                reason = f"Required scope key '{key}' missing from delegation"
                logger.warning(reason)
                return DelegationResult(allowed=False, reason=reason)

        # All checks passed — create the child context
        child = parent.delegate(to=to, policy_scope=policy_scope)
        return DelegationResult(allowed=True, context=child)
