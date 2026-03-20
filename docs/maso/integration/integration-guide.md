---
description: "MASO integration guide for LangGraph, AutoGen, CrewAI, and AWS Bedrock Agents. Mapping control requirements to framework-specific implementation patterns."
---

# Integration Guide

**Implementing MASO Controls in Agent Orchestration Frameworks**

> Part of the [MASO Framework](../README.md) · Integration

## Purpose

This guide maps MASO control requirements to the specific implementation patterns available in four widely-adopted agent orchestration frameworks: LangGraph, AutoGen, CrewAI, and AWS Bedrock Agents. For each framework, it identifies where MASO controls can be enforced natively, where custom implementation is required, and where architectural gaps exist.

The guide does not endorse any framework. It provides the security architect with a practical mapping: "I need to implement MASO control X - here's how to do it in framework Y."

## Framework Comparison Matrix

| MASO Control | LangGraph | AutoGen | CrewAI | AWS Bedrock Agents |
|--------------|-----------|---------|--------|-------------------|
| **PG-1.1** Input guardrails per agent | Custom node | Custom middleware | Custom tool | Bedrock Guardrails (native) |
| **PG-1.4** Message source tagging | State annotation | Message metadata | N/A - custom needed | N/A - custom needed |
| **PG-2.1** Inter-agent injection detection | Custom edge validator | Custom speaker selection | N/A - custom needed | N/A - custom needed |
| **PG-2.2** Goal integrity monitoring | Checkpointer + custom | Custom termination check | N/A - custom needed | CloudWatch custom metric |
| **IA-1.4** Scoped tool permissions | Per-node tool binding | Per-agent tool list | Per-agent tool list | Action group scoping (native) |
| **IA-2.1** Zero-trust credentials | Custom credential manager | Custom credential manager | Custom credential manager | IAM roles per agent (native) |
| **DP-2.1** DLP on message bus | Custom channel interceptor | Custom middleware | N/A - custom needed | N/A - custom needed |
| **EC-1.1** Human approval for writes | `interrupt_before` (native) | `HumanInputMode` (native) | `human_input=True` (native) | Return control (native) |
| **EC-1.2** Tool allow-lists | Per-node tool binding | Per-agent tool list | Per-agent tool list | Action group definitions (native) |
| **EC-2.5** Model-as-Judge gate | Custom node in graph | Custom agent role | Custom agent role | Custom Lambda function |
| **OB-1.1** Action audit logging | LangSmith integration | Custom logging | Custom logging | CloudTrail + CloudWatch (native) |
| **OB-3.2** Circuit breaker / kill switch | Custom graph termination | Custom termination | Custom termination | Step Functions abort (native) |
| **SC-2.1** AIBOM | External tooling | External tooling | External tooling | External tooling |

**Legend:** Native = framework provides built-in capability. Custom = requires implementation using framework extension points. N/A = no native support; requires external implementation.

## LangGraph

### Architecture Fit

LangGraph's graph-based execution model maps well to MASO's control architecture. Each node in the graph is an agent or control point. Edges define the message flow. State is passed explicitly through the graph, making it auditable and controllable.

**Strengths for MASO:** Explicit state management, native checkpointing, human-in-the-loop via `interrupt_before`, per-node tool binding, conditional edges for routing.

**Gaps:** No built-in message bus security, no DLP, no inter-agent injection detection, no kill switch beyond graph termination. All security controls beyond basic tool scoping require custom implementation.

### Control Implementation Patterns

**Guardrails (PG-1.1):** Implement as a dedicated node that runs before each agent node. The guardrail node validates input against known-bad patterns and returns sanitised content to the next node. Use conditional edges to route flagged content to a review path.

![LangGraph Guardrail Flow](../../images/langgraph-guardrail-flow.svg)

**Message source tagging (PG-1.4):** Extend the graph state schema to include a `source_type` field (instruction | data | user | agent). Each node that adds content to the state must tag it. The Judge node validates that data-tagged content is not treated as instruction.

**Human approval for writes (EC-1.1):** Use `interrupt_before` on any node that executes write operations. LangGraph natively suspends execution and waits for human input before proceeding.

**Model-as-Judge (EC-2.5):** Implement as a dedicated node in the graph that evaluates agent outputs before they reach the output node. The Judge node uses a different model instance than the task agents. Configure conditional edges: pass → output, fail → human review, critical fail → terminate.

**Goal integrity monitoring (PG-2.2):** Use LangGraph's checkpointing to snapshot the original task specification at graph entry. At each subsequent node, compare the current task context against the original checkpoint. Significant deviation triggers an alert or graph termination.

**Kill switch (OB-3.2):** Implement as an external service that can terminate the LangGraph execution thread. The kill switch service monitors a shared signal (Redis key, database flag, or message queue). A background thread in the graph executor checks the signal at each node transition. If triggered, the graph terminates and preserves state for forensics.

**Audit logging (OB-1.1):** Use LangSmith for trace capture. Ensure all node inputs, outputs, and tool calls are logged. Extend with custom callbacks to capture MASO-specific metadata (source tags, confidence scores, goal hashes).

## AutoGen

### Architecture Fit

AutoGen's conversation-based multi-agent model provides flexible agent-to-agent communication with configurable speaker selection and termination conditions. The `GroupChat` pattern maps to MASO's message bus concept.

**Strengths for MASO:** Flexible agent composition, human-in-the-loop via `HumanInputMode`, configurable termination conditions, custom speaker selection for routing control.

**Gaps:** No built-in message signing, no DLP, limited audit trail without custom logging, no native credential isolation between agents. The conversation-based model makes message source tagging harder because all messages are in a shared conversation thread.

### Control Implementation Patterns

**Guardrails (PG-1.1):** Implement as a custom `ConversableAgent` that acts as a filter. Place the guardrail agent as the first speaker in any `GroupChat`. Configure speaker selection to route all incoming messages through the guardrail agent before they reach task agents.

**Inter-agent injection detection (PG-2.1):** Override the `GroupChat` speaker selection function. Before selecting the next speaker, pass the current message to an injection detection function. If injection is detected, route to the human proxy or terminate the conversation.

**Human approval for writes (EC-1.1):** Configure `HumanInputMode.ALWAYS` for any agent that executes write operations. AutoGen natively pauses and requests human input before the agent proceeds.

**Model-as-Judge (EC-2.5):** Add a Judge agent to the `GroupChat` with a different model configuration. Configure speaker selection to route all outputs through the Judge agent before they are returned to the user or passed to execution agents. The Judge agent's system prompt contains evaluation criteria aligned with MASO requirements.

**Scoped permissions (IA-1.4):** Define tool functions per agent. Each agent's `function_map` contains only the tools it is authorised to use. Do not share tool functions across agents. Validate that delegation between agents does not implicitly share tool access.

**Audit logging (OB-1.1):** Register a custom callback handler on the `GroupChat` that logs every message with metadata: sender, recipient, timestamp, message hash, and any tool calls. Store in an append-only log with integrity protection.

## CrewAI

### Architecture Fit

CrewAI's task-based model with explicit agent roles and delegation maps naturally to MASO's execution control patterns. Agents have defined roles, backstories, and tool access. Tasks define the workflow.

**Strengths for MASO:** Clear agent role definitions, explicit delegation control, per-agent tool assignment, human input flag per task, sequential and hierarchical process models.

**Gaps:** Limited inter-agent communication control (agents communicate through the CrewAI framework, not a configurable message bus), no built-in DLP, no message signing, no native anomaly detection. The framework's abstraction level means many MASO controls require implementation below the CrewAI API.

### Control Implementation Patterns

**Guardrails (PG-1.1):** Implement as a custom `Tool` that wraps every other tool. The guardrail tool validates inputs before passing them to the actual tool. Alternatively, implement as a pre-processing step in each agent's `execute_task` method using a subclass.

**Human approval for writes (EC-1.1):** Set `human_input=True` on any task that involves write operations. CrewAI natively pauses execution and requests human input before proceeding.

**Scoped permissions (IA-1.4):** Assign tools to agents explicitly in the agent definition. Each agent receives only the tools required for its role. Use the `allow_delegation` parameter to control whether an agent can delegate tasks to other agents - set to `False` for high-privilege agents to prevent transitive authority.

**Model-as-Judge (EC-2.5):** Create a dedicated "Quality Assurance" agent with its own model configuration. Add it as the final step in the task chain. The QA agent reviews all outputs against MASO criteria before they are returned. Use the hierarchical process model to enforce that the QA agent has authority over task agents.

**Goal integrity (PG-2.2):** Define expected outcomes in the task `expected_output` field. After task execution, compare the actual output against the expected outcome. Significant deviation triggers re-execution or escalation.

**Audit logging (OB-1.1):** CrewAI provides `verbose=True` for detailed execution logging. Extend with a custom output handler that captures agent decisions, tool calls, delegation events, and task outcomes in a structured format.

## AWS Bedrock Agents

### Architecture Fit

AWS Bedrock Agents provides a managed infrastructure for agent orchestration with native IAM integration, Bedrock Guardrails, CloudTrail logging, and Step Functions for workflow control. This is the most enterprise-ready platform for MASO implementation.

**Strengths for MASO:** Native IAM for agent identity (IA-2.1), Bedrock Guardrails for input/output filtering (PG-1.1), CloudTrail for audit logging (OB-1.1), Step Functions for workflow control and human approval, action group scoping for tool permissions (IA-1.4), Lambda functions for custom control logic.

**Gaps:** Limited inter-agent communication control for multi-agent patterns (Bedrock focuses on single-agent with tool use), no native message bus for agent-to-agent communication, no built-in epistemic controls, no challenger agent pattern. Multi-agent orchestration requires custom implementation on top of the managed services.

### Control Implementation Patterns

**Guardrails (PG-1.1):** Use Bedrock Guardrails (native). Configure content filters, denied topics, word filters, sensitive information filters, and contextual grounding checks. Apply guardrails to both agent inputs and outputs.

**Agent identity (IA-2.1):** Create a dedicated IAM role for each agent with least-privilege permissions. Use IAM session policies for dynamic permission scoping. Each agent's role defines exactly which AWS services and resources it can access.

**Tool scoping (IA-1.4):** Define action groups per agent. Each action group specifies the API operations the agent can invoke. Bedrock enforces that agents can only call APIs within their assigned action groups.

**Human approval (EC-1.1):** Use the `RETURN_CONTROL` invocation type. When an agent needs to execute a write operation, it returns control to the calling application with the proposed action. The application presents the action to a human for approval before executing.

**Model-as-Judge (EC-2.5):** Implement as a Lambda function invoked after each agent action. The Lambda calls a separate Bedrock model (different from the task agent's model) with evaluation criteria. The Lambda returns pass/fail, which determines whether the Step Functions workflow proceeds or routes to human review.

**Kill switch (OB-3.2):** Use Step Functions to orchestrate the multi-agent workflow. The kill switch triggers a Step Functions abort, which terminates all active agent executions. Use SNS notifications to alert the security team. CloudTrail captures the full execution history for forensics.

**Audit logging (OB-1.1):** CloudTrail captures all Bedrock API calls. CloudWatch captures agent execution traces. Configure CloudWatch alarms for anomaly detection (unusual API call patterns, high error rates, unexpected tool invocations).

## Cross-Framework Implementation Priorities

Regardless of framework, implement these controls first:

**Priority 1 (Tier 1 minimum):**
1. Human approval for all write operations - every framework supports this natively
2. Per-agent tool scoping - define exactly which tools each agent can use
3. Audit logging - capture every agent action, tool call, and delegation event
4. Input guardrails - filter known-bad patterns at each agent's input boundary

**Priority 2 (Tier 2 minimum):**
5. Model-as-Judge evaluation - add an independent evaluation agent using a different model
6. Message source tagging - distinguish data from instruction in all inter-agent communication
7. Inter-agent injection detection - evaluate messages for injection patterns at the bus level
8. DLP on inter-agent messages - detect sensitive data in agent-to-agent communication

**Priority 3 (Tier 3):**
9. Independent observability agent with kill switch authority
10. Challenger agent for epistemic validation
11. Cryptographic goal integrity verification
12. Model diversity enforcement

## Framework Selection Guidance

| Requirement | Recommended Framework |
|-------------|---------------------|
| Maximum native security controls | AWS Bedrock Agents |
| Maximum flexibility for custom controls | LangGraph |
| Fastest time to basic multi-agent | CrewAI |
| Best conversation-based multi-agent | AutoGen |
| Regulated financial services | AWS Bedrock Agents (IAM, CloudTrail, compliance) |
| Research / experimentation | LangGraph or AutoGen |

No framework provides complete MASO coverage out of the box. Every implementation will require custom security controls beyond what the framework provides natively. The framework's role is to provide extension points - the security architecture is your responsibility.

