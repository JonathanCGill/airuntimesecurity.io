"""Tool invocation policy engine.

Implements: tool_call → policy → allow/deny

This is the "infrastructure beats instructions" principle in code.
Instead of telling a model not to use dangerous tools via prompts,
enforce it outside the model at the runtime layer.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from pydantic import BaseModel, Field

from airs.agents.identity import AgentContext

logger = logging.getLogger(__name__)


class ToolCall(BaseModel):
    """A tool invocation request from an agent."""

    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    agent_id: str = ""       # which agent is calling
    description: str = ""    # optional human-readable description
    timestamp: float = Field(default_factory=time.time)


class ToolPolicyResult(BaseModel):
    """Outcome of a tool policy check."""

    allowed: bool
    tool_name: str
    reason: str = ""
    agent_id: str = ""
    latency_ms: float = 0.0


class ToolPolicy(BaseModel):
    """Policy for tool access control.

    Supports allow-lists, deny-lists, and per-agent-type restrictions.
    Deny-by-default: if an allow_list is set, anything not on it is denied.

    Usage:
        policy = ToolPolicy(
            allow_list=["search", "read_file", "calculator"],
            deny_list=["delete_file", "exec_code"],
            per_agent_type={"retriever": ["search", "read_file"]},
        )
    """

    # Global allow-list. If non-empty, only these tools are permitted.
    allow_list: list[str] = Field(default_factory=list)

    # Global deny-list. Always denied, even if on the allow-list.
    deny_list: list[str] = Field(default_factory=list)

    # Per agent-type allow-lists. Overrides the global allow_list for that type.
    per_agent_type: dict[str, list[str]] = Field(default_factory=dict)

    # Maximum arguments payload size (bytes, 0 = no limit)
    max_argument_size: int = 0


class ToolPolicyEngine:
    """Enforces tool access control before execution.

    Usage:
        engine = ToolPolicyEngine(policy)

        call = ToolCall(tool_name="search", arguments={"q": "hello"})
        result = engine.evaluate(call)
        # or with agent context:
        result = engine.evaluate(call, context=agent_ctx)

        if not result.allowed:
            raise PermissionError(result.reason)
    """

    def __init__(self, policy: ToolPolicy | None = None) -> None:
        self.policy = policy or ToolPolicy()

    def evaluate(
        self,
        call: ToolCall,
        context: AgentContext | None = None,
    ) -> ToolPolicyResult:
        """Evaluate a tool call against the policy.

        If an AgentContext is provided, the engine also checks:
        - per-agent-type restrictions
        - policy_scope["tools"] from the delegation chain
        """
        start = time.monotonic()
        agent_id = call.agent_id or (
            context.current_agent.agent_id if context else ""
        )

        # Deny-list always wins
        if call.tool_name in self.policy.deny_list:
            return self._result(
                False, call.tool_name, agent_id,
                f"Tool '{call.tool_name}' is on the deny list",
                start,
            )

        # Argument size check
        if self.policy.max_argument_size > 0:
            import json
            arg_size = len(json.dumps(call.arguments))
            if arg_size > self.policy.max_argument_size:
                return self._result(
                    False, call.tool_name, agent_id,
                    f"Arguments size {arg_size}B exceeds limit "
                    f"{self.policy.max_argument_size}B",
                    start,
                )

        # Per-agent-type restrictions (if context provides agent type)
        if context and context.current_agent.agent_type:
            agent_type = context.current_agent.agent_type
            if agent_type in self.policy.per_agent_type:
                allowed_tools = self.policy.per_agent_type[agent_type]
                if call.tool_name not in allowed_tools:
                    return self._result(
                        False, call.tool_name, agent_id,
                        f"Tool '{call.tool_name}' not allowed for agent type "
                        f"'{agent_type}' (allowed: {allowed_tools})",
                        start,
                    )

        # Delegation scope check — policy_scope["tools"] from the chain
        if context and "tools" in context.policy_scope:
            scope_tools = context.policy_scope["tools"]
            if isinstance(scope_tools, list) and call.tool_name not in scope_tools:
                return self._result(
                    False, call.tool_name, agent_id,
                    f"Tool '{call.tool_name}' not in delegation scope "
                    f"(scope: {scope_tools})",
                    start,
                )

        # Global allow-list
        if self.policy.allow_list and call.tool_name not in self.policy.allow_list:
            return self._result(
                False, call.tool_name, agent_id,
                f"Tool '{call.tool_name}' not on allow list",
                start,
            )

        return self._result(True, call.tool_name, agent_id, "", start)

    def _result(
        self,
        allowed: bool,
        tool_name: str,
        agent_id: str,
        reason: str,
        start: float,
    ) -> ToolPolicyResult:
        latency = (time.monotonic() - start) * 1000
        if not allowed:
            logger.warning(
                "Tool policy DENIED: tool=%s agent=%s reason=%s",
                tool_name, agent_id, reason,
            )
        return ToolPolicyResult(
            allowed=allowed,
            tool_name=tool_name,
            agent_id=agent_id,
            reason=reason,
            latency_ms=latency,
        )
