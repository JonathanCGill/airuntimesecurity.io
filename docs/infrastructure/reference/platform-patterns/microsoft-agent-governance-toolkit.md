---
description: "Microsoft Agent Governance Toolkit implementation patterns for AI agent runtime security: policy enforcement, execution rings, compliance automation, and OWASP Agentic Top 10 coverage."
---

# Microsoft Agent Governance Toolkit Patterns

> **Purpose:** Reference patterns for implementing AI agent runtime security using Microsoft's open-source Agent Governance Toolkit (AGT), released April 2026 under the MIT licence.
> **Status:** Reference patterns. AGT is new (v0.1.x at time of writing). Evaluate maturity for your use case.

## Overview

The Agent Governance Toolkit is a seven-package system covering policy enforcement, identity, execution sandboxing, reliability engineering, compliance automation, plugin lifecycle, and RL training governance. It is the first open-source toolkit to address all 10 OWASP Agentic Top 10 risks with deterministic, sub-millisecond policy enforcement.

Available in Python, TypeScript, Rust, Go, and .NET. Framework integrations exist for LangChain, CrewAI, Google ADK, and Microsoft Agent Framework.

## Architecture Mapping

| Framework Zone | AGT Component | Function |
|---------------|--------------|----------|
| **Zone 1 - Ingress** | Agent OS | Stateless policy engine intercepts every agent action before execution (p99 < 0.1ms) |
| **Zone 2 - Runtime** | Agent Runtime | Execution rings, saga orchestration, kill switch |
| **Zone 3 - Evaluation** | Agent OS (policy rules) | Deterministic policy evaluation against declared manifests |
| **Zone 5 - Control Plane** | Agent Compliance, Agent Marketplace | Compliance grading, plugin lifecycle, trust-tiered gating |
| **Zone 6 - Logging** | Agent SRE | SLOs, error budgets, structured telemetry |
| **Cross-cutting** | Agent Lightning | RL training governance with policy-enforced runners |

## Agent OS: Policy Enforcement

Agent OS is the core component. It functions as a stateless policy engine that intercepts every agent action before execution.

### How it maps to AIRS controls

| AIRS Control | Agent OS Feature |
|-------------|-----------------|
| **TOOL-01 (Manifests)** | Agents declare permitted tools in a manifest. Agent OS rejects any tool call not in the manifest |
| **TOOL-02 (Gateway)** | All tool invocations transit Agent OS. Agents cannot self-authorise |
| **TOOL-03 (Parameters)** | Parameter constraints defined in policy, enforced at interception |
| **TOOL-04 (Classification)** | Actions classified by reversibility. Irreversible actions require human approval |
| **TOOL-05 (Rate Limits)** | Per-agent, per-tool rate limiting with configurable windows |
| **NET-02 (Bypass Prevention)** | Architecture enforces that all actions pass through the policy engine |

### Configuration pattern

```yaml
# agent-policy.yaml
agent:
  id: customer-service-agent
  manifest:
    tools:
      - name: search_knowledge_base
        max_calls_per_minute: 30
        parameters:
          query:
            type: string
            max_length: 500
      - name: create_ticket
        classification: reversible
        max_calls_per_minute: 10
      - name: issue_refund
        classification: irreversible
        requires_human_approval: true
        max_amount: 100.00
    denied_tools:
      - execute_code
      - send_email
```

## Agent Runtime: Execution Rings

Agent Runtime introduces execution rings modelled on CPU privilege levels. Each ring restricts what the agent can do.

| Ring | Privilege Level | Use Case |
|------|----------------|----------|
| **Ring 0** | Full system access | Platform operators only. Not for agents |
| **Ring 1** | Scoped tool access with approval gates | Production agents handling sensitive operations |
| **Ring 2** | Read-only tools, no side effects | Information retrieval agents, research assistants |
| **Ring 3** | Sandboxed execution, no external access | Code generation, data analysis, testing |

### AIRS mapping

| AIRS Control | Execution Rings Feature |
|-------------|------------------------|
| **SAND-01 (Isolation)** | Ring assignment determines isolation level |
| **IAM-02 (Least Privilege)** | Agents assigned to the minimum ring for their task |
| **IAM-04 (Tool Constraints)** | Ring determines which tool categories are available |

### Saga orchestration

Multi-step agent operations use the saga pattern: each step has a compensating action. If any step fails or is rejected, previous steps are automatically rolled back.

This maps to **IR-04 (Rollback)** and addresses **ASI08 (Cascading Failures)** in the OWASP Agentic Top 10.

### Kill switch

Emergency agent termination halts all in-flight operations and triggers compensating actions. This implements the circuit breaker pattern described in the AIRS PACE model.

## Agent SRE: Reliability Engineering

Agent SRE applies site reliability engineering practices to agent systems.

| SRE Concept | Agent Application | AIRS Mapping |
|------------|-------------------|-------------|
| **SLOs** | Target success rates, latency bounds, error rates per agent | LOG-05 (Drift Detection) |
| **Error budgets** | Agents with exhausted error budgets are automatically throttled or paused | Circuit Breaker |
| **Circuit breakers** | Open on SLO violation, close after recovery period | PACE resilience model |
| **Chaos engineering** | Inject tool failures, latency, and policy violations to test agent resilience | Red team methodology |
| **Progressive delivery** | Canary agent deployments with automatic rollback on SLO regression | Deployment controls |

## Agent Compliance: Automated Governance

Agent Compliance automates compliance verification against regulatory frameworks.

| Framework | AGT Coverage |
|-----------|-------------|
| **EU AI Act** | High-risk obligations mapping, evidence collection |
| **HIPAA** | PHI handling verification for healthcare agents |
| **SOC 2** | Control evidence for Type II audits |
| **OWASP Agentic Top 10** | All 10 risk categories assessed and graded |

### Compliance grading

Each agent receives a compliance grade (A through F) based on:

- Policy coverage (are all required controls in place?)
- Enforcement verification (are controls actually enforced, not just declared?)
- Evidence completeness (can you prove compliance to an auditor?)

This maps to the AIRS framework's maturity levels and supports the regulatory mapping requirements in the compliance section.

## Agent Marketplace: Plugin Lifecycle

Agent Marketplace governs how agents discover and use plugins (skills, tools, integrations).

| Feature | What It Does | AIRS Mapping |
|---------|-------------|-------------|
| **Ed25519 signing** | Cryptographic verification of plugin authorship | SUP-01 (Provenance) |
| **Manifest verification** | Plugin declares permissions, data access, and network requirements | TOOL-01, SUP-05 |
| **Trust-tiered gating** | Plugins categorised by trust level; higher-tier plugins require more verification | SUP-02 (Risk Assessment) |
| **Lifecycle management** | Version pinning, deprecation tracking, vulnerability alerts | SUP-07, SUP-08 |

This directly addresses the agent supply chain risks demonstrated by the OpenClaw incident, where 1 in 5 packages in an agent skill registry were malicious.

## Agent Lightning: RL Training Governance

Agent Lightning governs reinforcement learning training workflows.

| Feature | What It Does | AIRS Relevance |
|---------|-------------|---------------|
| **Policy-enforced runners** | RL training runs within policy boundaries; reward functions cannot bypass safety constraints | Training-time safety extension |
| **Reward shaping** | Governance-aware reward signals that penalise policy violations | Addresses reward hacking risk |
| **Zero violation target** | Training halts on any policy violation | Circuit breaker for training |

This is relevant to the emergent misalignment risk documented in [When Learning Goes Wrong](../../../insights/when-learning-goes-wrong.md), where RL training spontaneously produced misaligned behaviour.

## Framework Integration Patterns

AGT integrates via each framework's native extension points:

| Framework | Integration Method |
|-----------|-------------------|
| **LangChain** | Callback handlers on chain execution |
| **CrewAI** | Task decorators wrapping agent actions |
| **Google ADK** | Plugin system hooks |
| **Microsoft Agent Framework** | Middleware pipeline injection |

### LangChain example

```python
from agent_governance_toolkit import AgentOS
from langchain.callbacks import BaseCallbackHandler

class AGTCallback(BaseCallbackHandler):
    def __init__(self, policy_path: str):
        self.policy = AgentOS.load_policy(policy_path)

    def on_tool_start(self, tool, input_str, **kwargs):
        decision = self.policy.evaluate(tool.name, input_str)
        if decision.denied:
            raise PolicyViolation(decision.reason)
```

## OWASP Agentic Top 10 Coverage

| OWASP Risk | AGT Component | Coverage |
|-----------|--------------|---------|
| ASI01 Agent Goal Hijack | Agent OS (policy enforcement) | Tool-level containment limits hijack impact |
| ASI02 Tool Misuse | Agent OS (manifests, parameters) | Declared tool boundaries enforced deterministically |
| ASI03 Identity Abuse | Agent Runtime (execution rings) | Ring-based privilege prevents escalation |
| ASI04 Supply Chain | Agent Marketplace (signing, gating) | Cryptographic provenance for all plugins |
| ASI05 Code Execution | Agent Runtime (Ring 3 sandbox) | Sandboxed execution with no external access |
| ASI06 Memory Poisoning | Agent Runtime (saga rollback) | State rollback on detected corruption |
| ASI07 Inter-Agent Comms | Agent OS (per-hop policy) | Policy evaluation on every inter-agent message |
| ASI08 Cascading Failures | Agent SRE (circuit breakers) | SLO-based circuit breaking with error budgets |
| ASI09 Trust Exploitation | Agent OS (approval gates) | Irreversible actions require human confirmation |
| ASI10 Rogue Agents | Agent SRE + Agent OS | Behavioural SLOs detect deviation; kill switch terminates |

## Limitations

- **New project (v0.1.x).** Production maturity is unproven. Evaluate carefully before deploying to HIGH or CRITICAL systems
- **Policy, not detection.** Agent OS enforces declared policies. It does not perform semantic evaluation (no Judge equivalent). Pair with the AIRS Judge layer for full coverage
- **No multimodal support.** Current policies are text and tool-action based. Image, voice, and video inputs are not covered
- **Framework lock-in risk.** Deep integration with a specific agent framework may make migration difficult. Use the abstraction layer where possible

!!! info "References"
    - [Introducing the Agent Governance Toolkit (Microsoft Open Source Blog, April 2026)](https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/)
    - [Agent Governance Toolkit on GitHub](https://github.com/microsoft/agent-governance-toolkit)
    - [Microsoft releases open-source toolkit to govern autonomous AI agents (Help Net Security)](https://www.helpnetsecurity.com/2026/04/03/microsoft-ai-agent-governance-toolkit/)
    - [Running 11 AI agents in production: how the Agent Governance Toolkit secures our workflows (Medium)](https://medium.com/@isiddique/running-11-ai-agents-in-production-how-the-agent-governance-toolkit-secures-our-workflows-10a6399638fc)
