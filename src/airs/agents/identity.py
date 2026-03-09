"""Agent identity propagation.

Every action in a multi-agent system must be traceable to the originating
user through the full agent chain.  This module provides the identity
primitives that flow through the security pipeline.
"""

from __future__ import annotations

import time
import uuid
from typing import Any

from pydantic import BaseModel, Field


class AgentIdentity(BaseModel):
    """Identity of a single agent in a chain."""

    agent_id: str
    agent_name: str = ""
    agent_type: str = ""  # e.g. "orchestrator", "retriever", "tool-caller"
    model: str = ""       # the backing model, if any
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentContext(BaseModel):
    """Security context that propagates through an agent chain.

    Attach this to an AIRequest to enable identity tracking, delegation
    depth enforcement, and policy scope propagation.

    Usage:
        ctx = AgentContext(
            user_id="user_123",
            origin_agent=AgentIdentity(agent_id="orchestrator"),
        )
        # Agent delegates to a sub-agent
        child_ctx = ctx.delegate(
            to=AgentIdentity(agent_id="retriever"),
            policy_scope={"tools": ["search"]},
        )
    """

    # Who initiated the chain
    user_id: str
    session_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])

    # The agent that created this context
    origin_agent: AgentIdentity

    # Full chain from origin to current agent (oldest first)
    agent_chain: list[AgentIdentity] = Field(default_factory=list)

    # How deep we are in delegation (0 = origin agent)
    delegation_depth: int = 0

    # Policy scope narrows as delegation deepens
    # Each key is an arbitrary scope dimension (e.g. "tools", "data", "actions")
    policy_scope: dict[str, Any] = Field(default_factory=dict)

    # Correlation ID for tracing across the entire request
    correlation_id: str = Field(default_factory=lambda: uuid.uuid4().hex)

    timestamp: float = Field(default_factory=time.time)

    def model_post_init(self, __context: Any) -> None:
        """Ensure origin agent is in the chain."""
        if not self.agent_chain:
            self.agent_chain = [self.origin_agent]

    def delegate(
        self,
        to: AgentIdentity,
        policy_scope: dict[str, Any] | None = None,
    ) -> AgentContext:
        """Create a child context for a delegated agent.

        The child inherits the full chain, increments depth, and
        optionally narrows the policy scope.  Policy scope can only
        be narrowed, never widened — a child cannot grant itself
        permissions the parent doesn't have.
        """
        merged_scope = dict(self.policy_scope)
        if policy_scope:
            for key, value in policy_scope.items():
                if key in merged_scope and isinstance(merged_scope[key], list):
                    # Intersection: child can only use tools the parent allows
                    parent_set = set(merged_scope[key])
                    merged_scope[key] = [v for v in value if v in parent_set]
                else:
                    # New dimension — child introduces a restriction
                    merged_scope[key] = value

        return AgentContext(
            user_id=self.user_id,
            session_id=self.session_id,
            origin_agent=self.origin_agent,
            agent_chain=[*self.agent_chain, to],
            delegation_depth=self.delegation_depth + 1,
            policy_scope=merged_scope,
            correlation_id=self.correlation_id,
        )

    @property
    def current_agent(self) -> AgentIdentity:
        """The agent at the end of the chain (the one currently acting)."""
        return self.agent_chain[-1]

    @property
    def chain_ids(self) -> list[str]:
        """Flat list of agent IDs in the chain, for logging."""
        return [a.agent_id for a in self.agent_chain]
