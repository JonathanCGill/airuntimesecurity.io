# Agent Security

Identity propagation, delegation enforcement, and tool access control for multi-agent systems.

## The Problem

In multi-agent architectures, a single user request can flow through an orchestrator, sub-agents, tool-calling agents, and back. Without explicit identity propagation:

- You can't trace an action back to the originating user
- Agents can delegate without limit, creating unbounded chains
- Tool access is uncontrolled — any agent can call any tool
- Scope creep is invisible — permissions widen as delegation deepens

## Agent Identity

Every agent in the chain carries an `AgentIdentity`:

```python
from airs.agents import AgentIdentity

orchestrator = AgentIdentity(
    agent_id="orchestrator-1",
    agent_name="Main Orchestrator",
    agent_type="orchestrator",
    model="claude-sonnet-4-6",
)

retriever = AgentIdentity(
    agent_id="retriever-1",
    agent_name="RAG Retriever",
    agent_type="retriever",
)
```

## Agent Context

`AgentContext` is the security context that flows through the chain. It tracks who started the request, every agent that touched it, and what permissions narrow at each step.

```python
from airs.agents import AgentIdentity, AgentContext

# Create the root context (user → orchestrator)
ctx = AgentContext(
    user_id="user_123",
    origin_agent=orchestrator,
    policy_scope={"tools": ["search", "read_file", "calculator"]},
)

# Orchestrator delegates to retriever — scope narrows
child_ctx = ctx.delegate(
    to=retriever,
    policy_scope={"tools": ["search", "read_file"]},  # no calculator
)

print(child_ctx.delegation_depth)   # 1
print(child_ctx.chain_ids)          # ["orchestrator-1", "retriever-1"]
print(child_ctx.policy_scope)       # {"tools": ["search", "read_file"]}
print(child_ctx.correlation_id)     # same as parent — traces the full request
```

Key properties:

- **`delegation_depth`** — increments at each delegation
- **`agent_chain`** — full list of `AgentIdentity` objects (oldest first)
- **`chain_ids`** — flat list of agent IDs for logging
- **`policy_scope`** — narrows at each step, never widens
- **`correlation_id`** — same across the entire chain for tracing

### Scope Can Only Narrow

A child cannot grant itself permissions the parent doesn't have:

```python
ctx = AgentContext(
    user_id="u1",
    origin_agent=orchestrator,
    policy_scope={"tools": ["search"]},
)

# Child tries to add "delete" — but parent doesn't have it
child = ctx.delegate(
    to=retriever,
    policy_scope={"tools": ["search", "delete"]},
)

print(child.policy_scope["tools"])  # ["search"] — "delete" was excluded
```

## Delegation Enforcement

`DelegationEnforcer` validates delegation attempts against a `DelegationPolicy` before they happen.

```python
from airs.agents import DelegationPolicy, DelegationEnforcer, AgentIdentity

policy = DelegationPolicy(
    max_depth=3,                                    # no more than 3 hops
    allowed_agent_types=["retriever", "tool-caller"],  # only these types
    required_scope_keys=["tools"],                  # must declare tool scope
    allow_cycles=False,                             # no loops
)

enforcer = DelegationEnforcer(policy)

result = enforcer.check_delegation(
    parent=ctx,
    to=AgentIdentity(agent_id="tool-1", agent_type="tool-caller"),
    policy_scope={"tools": ["calculator"]},
)

if result.allowed:
    child_ctx = result.context  # safe to use
else:
    print(f"Denied: {result.reason}")
```

### What Gets Enforced

| Check | What It Prevents |
|-------|-----------------|
| **Max depth** | Unbounded delegation chains (agent A → B → C → D → ...) |
| **Agent type allow-list** | Untrusted agent types entering the chain |
| **Cycle detection** | A → B → A loops that could run forever |
| **Required scope keys** | Delegations that forget to declare what tools/data they need |

## Tool Access Control

The `ToolPolicyEngine` intercepts tool calls and enforces allow/deny before execution.

```python
from airs.runtime import ToolCall, ToolPolicy, ToolPolicyEngine

policy = ToolPolicy(
    allow_list=["search", "read_file", "calculator"],
    deny_list=["exec_code", "delete_file"],
    per_agent_type={"retriever": ["search", "read_file"]},
    max_argument_size=10_000,  # bytes
)

engine = ToolPolicyEngine(policy)

# Check a tool call
call = ToolCall(tool_name="search", arguments={"q": "hello"})
result = engine.evaluate(call, context=child_ctx)

if result.allowed:
    # execute the tool
    ...
else:
    print(f"Denied: {result.reason}")
```

### Policy Layers (evaluated in order)

1. **Deny list** — always denied, no exceptions
2. **Argument size** — rejects oversized payloads
3. **Per-agent-type** — restricts tools by agent type (from context)
4. **Delegation scope** — respects `policy_scope["tools"]` from the chain
5. **Allow list** — if set, anything not on it is denied

### Integrating with the Pipeline

Attach the `AgentContext` to your `AIRequest` for automatic telemetry:

```python
from airs.core.models import AIRequest
from airs.agents import AgentIdentity, AgentContext

ctx = AgentContext(
    user_id="user_123",
    origin_agent=AgentIdentity(agent_id="orch"),
)

request = AIRequest(
    input_text="Find recent sales data",
    agent_context=ctx,
)

# Pipeline evaluation now includes agent chain in telemetry events
result = await pipeline.evaluate_input(request)
```

## Full Multi-Agent Example

```python
import asyncio
from airs.agents import AgentIdentity, AgentContext, DelegationPolicy, DelegationEnforcer
from airs.runtime import (
    SecurityPipeline, GuardrailChain, RegexGuardrail,
    ToolCall, ToolPolicy, ToolPolicyEngine,
)
from airs.core.models import AIRequest, AIResponse

async def main():
    # Security infrastructure
    pipeline = SecurityPipeline(guardrails=GuardrailChain([RegexGuardrail()]))
    delegation = DelegationEnforcer(DelegationPolicy(max_depth=3))
    tools = ToolPolicyEngine(ToolPolicy(
        allow_list=["search", "read_file"],
        deny_list=["exec_code"],
    ))

    # Orchestrator receives user request
    orch = AgentIdentity(agent_id="orch", agent_type="orchestrator")
    ctx = AgentContext(user_id="user_1", origin_agent=orch,
                       policy_scope={"tools": ["search", "read_file"]})

    request = AIRequest(input_text="Find Q4 revenue", agent_context=ctx)
    input_result = await pipeline.evaluate_input(request)
    if not input_result.allowed:
        return

    # Orchestrator delegates to retriever
    ret = AgentIdentity(agent_id="ret", agent_type="retriever")
    del_result = delegation.check_delegation(ctx, ret,
                                              policy_scope={"tools": ["search"]})
    if not del_result.allowed:
        return

    # Retriever tries to call a tool
    call = ToolCall(tool_name="search", arguments={"q": "Q4 revenue"})
    tool_result = tools.evaluate(call, context=del_result.context)
    if not tool_result.allowed:
        return

    # Tool executes, retriever returns result, orchestrator generates response
    ai_output = "Q4 revenue was $12.3M, up 15% YoY."
    response = AIResponse(request_id=request.request_id, output_text=ai_output)
    output_result = await pipeline.evaluate_output(request, response)

    if output_result.allowed:
        print(ai_output)

asyncio.run(main())
```
