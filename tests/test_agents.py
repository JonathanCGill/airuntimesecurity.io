"""Tests for agent identity propagation and delegation enforcement."""

import pytest

from airs.agents.identity import AgentIdentity, AgentContext
from airs.agents.delegation import DelegationPolicy, DelegationEnforcer


# ---------------------------------------------------------------------------
# AgentIdentity
# ---------------------------------------------------------------------------

class TestAgentIdentity:
    def test_create_identity(self):
        agent = AgentIdentity(agent_id="orch-1", agent_name="Orchestrator")
        assert agent.agent_id == "orch-1"
        assert agent.agent_name == "Orchestrator"

    def test_identity_defaults(self):
        agent = AgentIdentity(agent_id="a")
        assert agent.agent_type == ""
        assert agent.model == ""
        assert agent.metadata == {}


# ---------------------------------------------------------------------------
# AgentContext
# ---------------------------------------------------------------------------

class TestAgentContext:
    def _make_ctx(self, **kwargs):
        defaults = dict(
            user_id="user_1",
            origin_agent=AgentIdentity(agent_id="orch"),
        )
        defaults.update(kwargs)
        return AgentContext(**defaults)

    def test_origin_in_chain(self):
        ctx = self._make_ctx()
        assert len(ctx.agent_chain) == 1
        assert ctx.agent_chain[0].agent_id == "orch"

    def test_delegation_depth_starts_zero(self):
        ctx = self._make_ctx()
        assert ctx.delegation_depth == 0

    def test_current_agent(self):
        ctx = self._make_ctx()
        assert ctx.current_agent.agent_id == "orch"

    def test_chain_ids(self):
        ctx = self._make_ctx()
        assert ctx.chain_ids == ["orch"]

    def test_delegate_increments_depth(self):
        ctx = self._make_ctx()
        child = ctx.delegate(to=AgentIdentity(agent_id="ret"))
        assert child.delegation_depth == 1
        assert child.chain_ids == ["orch", "ret"]

    def test_delegate_preserves_user(self):
        ctx = self._make_ctx()
        child = ctx.delegate(to=AgentIdentity(agent_id="ret"))
        assert child.user_id == "user_1"
        assert child.session_id == ctx.session_id

    def test_delegate_preserves_correlation_id(self):
        ctx = self._make_ctx()
        child = ctx.delegate(to=AgentIdentity(agent_id="ret"))
        grandchild = child.delegate(to=AgentIdentity(agent_id="tool"))
        assert ctx.correlation_id == child.correlation_id == grandchild.correlation_id

    def test_delegate_narrows_scope_intersection(self):
        ctx = self._make_ctx(policy_scope={"tools": ["search", "read", "write"]})
        child = ctx.delegate(
            to=AgentIdentity(agent_id="ret"),
            policy_scope={"tools": ["search", "read"]},
        )
        assert set(child.policy_scope["tools"]) == {"search", "read"}

    def test_delegate_cannot_widen_scope(self):
        ctx = self._make_ctx(policy_scope={"tools": ["search"]})
        child = ctx.delegate(
            to=AgentIdentity(agent_id="ret"),
            policy_scope={"tools": ["search", "write"]},  # tries to add "write"
        )
        # "write" not in parent scope, so it's excluded
        assert child.policy_scope["tools"] == ["search"]

    def test_delegate_adds_new_scope_dimension(self):
        ctx = self._make_ctx(policy_scope={"tools": ["search"]})
        child = ctx.delegate(
            to=AgentIdentity(agent_id="ret"),
            policy_scope={"data": ["public"]},
        )
        assert child.policy_scope["tools"] == ["search"]
        assert child.policy_scope["data"] == ["public"]

    def test_deep_chain(self):
        ctx = self._make_ctx()
        current = ctx
        for i in range(10):
            current = current.delegate(to=AgentIdentity(agent_id=f"agent_{i}"))
        assert current.delegation_depth == 10
        assert len(current.agent_chain) == 11  # origin + 10


# ---------------------------------------------------------------------------
# DelegationEnforcer
# ---------------------------------------------------------------------------

class TestDelegationEnforcer:
    def _make_ctx(self, **kwargs):
        defaults = dict(
            user_id="user_1",
            origin_agent=AgentIdentity(agent_id="orch"),
        )
        defaults.update(kwargs)
        return AgentContext(**defaults)

    def test_allowed_delegation(self):
        enforcer = DelegationEnforcer()
        ctx = self._make_ctx()
        result = enforcer.check_delegation(ctx, AgentIdentity(agent_id="ret"))
        assert result.allowed
        assert result.context is not None
        assert result.context.delegation_depth == 1

    def test_max_depth_enforced(self):
        policy = DelegationPolicy(max_depth=2)
        enforcer = DelegationEnforcer(policy)

        ctx = self._make_ctx()
        r1 = enforcer.check_delegation(ctx, AgentIdentity(agent_id="a1"))
        assert r1.allowed
        r2 = enforcer.check_delegation(r1.context, AgentIdentity(agent_id="a2"))
        assert r2.allowed
        r3 = enforcer.check_delegation(r2.context, AgentIdentity(agent_id="a3"))
        assert not r3.allowed
        assert "depth" in r3.reason.lower()

    def test_allowed_agent_types(self):
        policy = DelegationPolicy(allowed_agent_types=["retriever", "tool-caller"])
        enforcer = DelegationEnforcer(policy)

        ctx = self._make_ctx()
        good = enforcer.check_delegation(
            ctx, AgentIdentity(agent_id="r", agent_type="retriever"),
        )
        assert good.allowed

        bad = enforcer.check_delegation(
            ctx, AgentIdentity(agent_id="x", agent_type="admin"),
        )
        assert not bad.allowed
        assert "admin" in bad.reason

    def test_cycle_detection(self):
        policy = DelegationPolicy(allow_cycles=False)
        enforcer = DelegationEnforcer(policy)

        ctx = self._make_ctx()
        r1 = enforcer.check_delegation(ctx, AgentIdentity(agent_id="a1"))
        assert r1.allowed

        # Try to delegate back to "orch" (already in chain)
        cycle = enforcer.check_delegation(r1.context, AgentIdentity(agent_id="orch"))
        assert not cycle.allowed
        assert "cycle" in cycle.reason.lower()

    def test_cycles_allowed_when_policy_permits(self):
        policy = DelegationPolicy(allow_cycles=True)
        enforcer = DelegationEnforcer(policy)

        ctx = self._make_ctx()
        r1 = enforcer.check_delegation(ctx, AgentIdentity(agent_id="a1"))
        r2 = enforcer.check_delegation(r1.context, AgentIdentity(agent_id="orch"))
        assert r2.allowed

    def test_required_scope_keys(self):
        policy = DelegationPolicy(required_scope_keys=["tools"])
        enforcer = DelegationEnforcer(policy)

        ctx = self._make_ctx()
        # No scope — missing required key
        bad = enforcer.check_delegation(ctx, AgentIdentity(agent_id="a1"))
        assert not bad.allowed
        assert "tools" in bad.reason

        # With scope
        good = enforcer.check_delegation(
            ctx, AgentIdentity(agent_id="a1"),
            policy_scope={"tools": ["search"]},
        )
        assert good.allowed

    def test_required_scope_keys_inherited(self):
        policy = DelegationPolicy(required_scope_keys=["tools"])
        enforcer = DelegationEnforcer(policy)

        ctx = self._make_ctx(policy_scope={"tools": ["search"]})
        # scope already on parent — child inherits
        result = enforcer.check_delegation(ctx, AgentIdentity(agent_id="a1"))
        assert result.allowed
