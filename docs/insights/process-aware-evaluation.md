# Process-Aware Evaluation: Judge the Trace, Not Just the Output

*Evaluating what an agent did is less important than evaluating how it got there*

An agent produces a correct answer. The customer gets the right information. The output passes guardrails, passes the Judge, looks clean in the audit log.

But the agent got there by calling a tool it shouldn't have accessed, reading a document outside the user's permission scope, and discarding two intermediate results that contradicted its final answer.

The output was fine. The process was a security incident.

## The Output Trap

Most evaluation architectures - including well-designed ones - focus on **what came out**. The guardrails check the output for known-bad patterns. The Judge evaluates the output for policy compliance, tone, accuracy. The human reviews the output and decides whether it's acceptable.

This is necessary. It is not sufficient.

Output-only evaluation misses three categories of failure:

### 1. Correct outputs from compromised processes

An agent that has been subject to indirect prompt injection may still produce correct outputs most of the time. The injected instruction might only activate under specific conditions - a particular user, a particular query, a particular time window. Between activations, the agent looks normal. The outputs are fine. The process is compromised.

If you only evaluate outputs, you won't see the compromise until the payload fires.

### 2. Reasoning that happened to land right

An agent that hallucinates an intermediate step but arrives at a correct final answer has not demonstrated reliability - it has demonstrated luck. The next query, with slightly different context, may trigger the same flawed reasoning with a wrong answer.

Output evaluation scores this as a pass. Process evaluation catches the fragile reasoning chain.

### 3. Policy-compliant outputs from policy-violating paths

An agent told to "summarise this document" might achieve the summary by first exfiltrating the document to an external API for processing, then returning the result. The summary is accurate. The exfiltration is a data breach.

The output is compliant. The trace is not.

## What Process-Aware Evaluation Means

Process-aware evaluation examines the **full reasoning and action trace** - not just the final output. It asks:

| Question | What It Catches |
|----------|----------------|
| Which tools were invoked, in what order? | Unexpected tool access, privilege escalation, tool-chain abuse |
| What intermediate results were generated? | Hallucinated reasoning steps, discarded contradictory evidence |
| What data was accessed at each step? | Scope violations, unauthorised data retrieval, cross-tenant leakage |
| Were any actions retried or revised? | Self-correction that masks instability, retry loops that indicate confusion |
| Did the reasoning chain follow a coherent path to the conclusion? | Motivated reasoning, post-hoc rationalisation, reasoning shortcuts |
| Were delegation decisions appropriate? | Over-delegation, under-delegation, delegation to inappropriate agents |

This is not a new idea - it is how aviation investigates incidents. The flight data recorder captures every input, every control surface movement, every system state change. Investigators don't just ask "did the plane land?" - they reconstruct the entire flight path. A safe landing after an unstable approach is not a pass. It's an incident requiring investigation.

## The Framework Already Has the Data

The architecture for process-aware evaluation already exists within this framework. It just isn't framed as an evaluation methodology.

**Observability controls capture the trace.** [OB-2.1](../maso/controls/observability.md) (Immutable decision chain) records the full causal chain from input through each agent's reasoning and actions to final output. [OB-3.2](../maso/controls/observability.md) (Causal chain reconstruction) provides automated trace reconstruction on demand.

**The Judge evaluates outputs.** [Judge Assurance](../core/judge-assurance.md) measures Judge accuracy against human ground truth, tracks drift, and adversarially tests the evaluation layer.

**The anomaly scoring model detects behavioral deviation.** [OB-2.2](../maso/controls/observability.md) scores agents against established baselines using seven input signals including tool usage patterns, output quality, and content drift.

The gap is between these components. The observability layer captures the trace. The Judge evaluates the output. But the trace itself is not systematically evaluated for security-relevant patterns - it feeds anomaly scoring (which detects statistical deviation) and forensic investigation (which happens after something goes wrong).

Process-aware evaluation closes that gap by making trace analysis a **routine evaluation function**, not just a forensic tool.

## How It Works in Practice

Process-aware evaluation operates as a periodic or triggered analysis - not on every transaction (that would be cost-prohibitive), but on a risk-proportionate sample and on every flagged event.

### Tier 1 - Manual Trace Review

During the weekly manual review ([OB-1.3](../maso/controls/observability.md)), reviewers examine not just the output but the full action sequence for a sample of agent workflows. The review checklist includes:

- Were all tool invocations appropriate for the task?
- Did the agent access data within the user's permission scope?
- Were intermediate reasoning steps coherent and supported?
- Did the agent follow the expected workflow pattern?

This is low-tech. It builds the organisational muscle for process-level thinking.

### Tier 2 - Automated Trace Pattern Matching

At Tier 2, define expected trace patterns for common workflows and flag deviations automatically:

- Agent called tool X before tool Y (expected order is Y then X)
- Agent accessed data source outside the workflow's declared scope
- Agent generated and discarded more than N intermediate results
- Agent's reasoning chain length deviated >2σ from the baseline for this query type

These pattern checks run against the immutable decision chain ([OB-2.1](../maso/controls/observability.md)). They are cheaper than full LLM evaluation and catch mechanical violations that output-only analysis would miss.

### Tier 3 - Judge-on-Trace

At Tier 3, deploy an Model-as-Judge against the trace itself - not just the final output. The Judge evaluates:

- Whether the reasoning chain supports the conclusion
- Whether tool selection was appropriate for the stated goal
- Whether data access patterns match the task requirements
- Whether delegation decisions followed the principle of least privilege

This is the most expensive evaluation mode. Reserve it for CRITICAL-tier workflows and for deep investigation of anomalies flagged by Tier 2 pattern matching.

## What This Changes

Process-aware evaluation doesn't replace output evaluation. It complements it. The combination catches failures that neither approach catches alone:

| Evaluation Type | Catches | Misses |
|----------------|---------|--------|
| Output-only | Wrong answers, policy violations in text, toxic content, hallucinated facts | Compromised processes with correct outputs, scope violations, tool abuse |
| Process-only | Unusual tool access, scope violations, reasoning instability, workflow deviation | Subtle output quality issues, tone violations, factual errors in otherwise well-constructed traces |
| **Both** | All of the above | Novel attack patterns that produce normal-looking traces and outputs (the hardest case) |

The key insight from recent research is that the agent's decision-making trace is itself a security artefact. Treating it as merely a log - useful for forensics but not for evaluation - leaves a category of failures undetected until they cause harm.

## Research Context

The concept of process-aware evaluation is emerging across the agentic AI security literature.

[Datta, Nahin, Chhabra, and Mohapatra (2025)](https://arxiv.org/abs/2510.23883) identify the shift toward "process-aware evaluation" as a frontier in security benchmarking - analysing not just whether an agent succeeded or failed, but *how* it reached its outcome. Their survey notes that current benchmarks like AgentDojo, InjectAgent, and Agent Security Bench primarily evaluate outcomes, and that trace-level analysis is necessary to identify subtle vulnerabilities that output checks would miss. The finding that 94.4% of LLM agents are vulnerable to prompt injection reinforces the need to examine *how* agents process inputs, not just what they produce.

[Arora and Hastings (2025)](https://arxiv.org/abs/2512.18043) reach a complementary conclusion through their MAAIS (Multilayer Agentic AI Security) framework, which extends the CIA triad to CIAA - adding Accountability as a first-class security property. Accountability requires traceability, and traceability requires the trace to be evaluated, not merely stored. Their lifecycle-aware approach - spanning development, deployment, operations, and governance - provides additional context for where in the agent lifecycle process-aware evaluation adds the most value.

[Dal Cin, Kendzior, Seedat, and Marinho (2025)](https://www.proquest.com/openview/d82e8ca1463253c1aeaf55c6dde38841/1?pq-origsite=gscholar&cbl=6831990) frame the practitioner case through a healthcare deployment where AI agents process patient exam requests across OCR, LLMs, cloud APIs, legacy databases, and billing platforms. Their three-phase model (threat modelling, security testing, runtime protections) identifies data poisoning and prompt injection as the primary risks - both of which manifest in the trace before they manifest in the output.

This aligns with the broader trajectory in AI evaluation: moving from "did it get the right answer?" to "did it get the right answer for the right reasons?" - a question that matters not just for accuracy, but for security.

## Related

- [Observability Controls](../maso/controls/observability.md) - The immutable decision chain that provides the trace data
- [Judge Assurance](../core/judge-assurance.md) - Measuring evaluation accuracy
- [The Judge Detects. It Doesn't Decide.](judge-detects-not-decides.md) - Why async evaluation matters
- [Behavioral Anomaly Detection](behavioral-anomaly-detection.md) - Statistical deviation from baselines
- [The Verification Gap](the-verification-gap.md) - The limits of confirming ground truth

