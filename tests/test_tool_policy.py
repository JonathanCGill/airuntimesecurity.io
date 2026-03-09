"""Tests for the tool invocation policy engine."""

import pytest

from airs.runtime.tool_policy import ToolCall, ToolPolicy, ToolPolicyEngine
from airs.agents.identity import AgentIdentity, AgentContext


class TestToolPolicyEngine:
    def test_no_policy_allows_everything(self):
        engine = ToolPolicyEngine()
        result = engine.evaluate(ToolCall(tool_name="anything"))
        assert result.allowed

    def test_deny_list(self):
        policy = ToolPolicy(deny_list=["exec_code", "delete_file"])
        engine = ToolPolicyEngine(policy)

        assert not engine.evaluate(ToolCall(tool_name="exec_code")).allowed
        assert not engine.evaluate(ToolCall(tool_name="delete_file")).allowed
        assert engine.evaluate(ToolCall(tool_name="search")).allowed

    def test_deny_list_overrides_allow_list(self):
        policy = ToolPolicy(
            allow_list=["exec_code", "search"],
            deny_list=["exec_code"],
        )
        engine = ToolPolicyEngine(policy)

        assert not engine.evaluate(ToolCall(tool_name="exec_code")).allowed
        assert engine.evaluate(ToolCall(tool_name="search")).allowed

    def test_allow_list_denies_unlisted(self):
        policy = ToolPolicy(allow_list=["search", "read_file"])
        engine = ToolPolicyEngine(policy)

        assert engine.evaluate(ToolCall(tool_name="search")).allowed
        assert engine.evaluate(ToolCall(tool_name="read_file")).allowed
        assert not engine.evaluate(ToolCall(tool_name="write_file")).allowed

    def test_per_agent_type_restriction(self):
        policy = ToolPolicy(
            per_agent_type={"retriever": ["search", "read_file"]},
        )
        engine = ToolPolicyEngine(policy)

        ctx = AgentContext(
            user_id="u1",
            origin_agent=AgentIdentity(agent_id="ret", agent_type="retriever"),
        )

        assert engine.evaluate(ToolCall(tool_name="search"), context=ctx).allowed
        assert not engine.evaluate(ToolCall(tool_name="delete"), context=ctx).allowed

    def test_per_agent_type_unrestricted_type(self):
        """Agent types not in per_agent_type are not restricted by it."""
        policy = ToolPolicy(
            per_agent_type={"retriever": ["search"]},
        )
        engine = ToolPolicyEngine(policy)

        ctx = AgentContext(
            user_id="u1",
            origin_agent=AgentIdentity(agent_id="o", agent_type="orchestrator"),
        )
        assert engine.evaluate(ToolCall(tool_name="anything"), context=ctx).allowed

    def test_delegation_scope_restriction(self):
        engine = ToolPolicyEngine()

        parent = AgentContext(
            user_id="u1",
            origin_agent=AgentIdentity(agent_id="orch"),
            policy_scope={"tools": ["search", "read_file"]},
        )
        child = parent.delegate(
            to=AgentIdentity(agent_id="ret"),
            policy_scope={"tools": ["search"]},
        )

        assert engine.evaluate(ToolCall(tool_name="search"), context=child).allowed
        assert not engine.evaluate(ToolCall(tool_name="read_file"), context=child).allowed

    def test_argument_size_limit(self):
        policy = ToolPolicy(max_argument_size=50)
        engine = ToolPolicyEngine(policy)

        small = ToolCall(tool_name="search", arguments={"q": "hi"})
        assert engine.evaluate(small).allowed

        big = ToolCall(tool_name="search", arguments={"q": "x" * 100})
        assert not engine.evaluate(big).allowed
        assert "size" in engine.evaluate(big).reason.lower()

    def test_result_includes_agent_id(self):
        engine = ToolPolicyEngine()
        result = engine.evaluate(ToolCall(tool_name="x", agent_id="agent_1"))
        assert result.agent_id == "agent_1"

    def test_result_agent_id_from_context(self):
        engine = ToolPolicyEngine()
        ctx = AgentContext(
            user_id="u1",
            origin_agent=AgentIdentity(agent_id="ctx_agent"),
        )
        result = engine.evaluate(ToolCall(tool_name="x"), context=ctx)
        assert result.agent_id == "ctx_agent"

    def test_latency_recorded(self):
        engine = ToolPolicyEngine()
        result = engine.evaluate(ToolCall(tool_name="x"))
        assert result.latency_ms >= 0
