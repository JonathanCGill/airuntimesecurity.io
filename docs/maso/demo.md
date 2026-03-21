---
description: Interactive demo showing a multi-agent prompt flowing through input judges, planner, tool-call judges, sandboxed execution, and output judges with real-time verdicts.
---

# Interactive Pipeline Demo

This demo plays back pre-recorded scenarios through a seven-stage evaluation pipeline. Select a scenario and press **Run** to watch each stage process the prompt in sequence, with streaming output, colour-coded verdicts, and a live event log.

**Two scenarios are included:**

- **Clean request (allowed)**: a routine data query that passes every judge.
- **Data exfiltration (blocked)**: a prompt that tries to email bulk customer PII to a personal address. The tool-call judge denies it and the pipeline halts.

<iframe src="../demo/multi-agent-risk.html" style="width: 100%; height: 80vh; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px;" loading="lazy" title="Multi-Agent Pipeline Demo"></iframe>

## What each stage does

| Stage | Role |
|-------|------|
| **User prompt received** | Raw input enters the system, untrusted |
| **Input judge** | Classifies the prompt before any execution happens |
| **Planner agent** | Decomposes the request into sub-tasks and assigns tools |
| **Tool-call judge** | Evaluates every tool invocation against policy before it runs |
| **Executor (sandboxed)** | Runs approved tool calls in isolation |
| **Output judge** | Scans the assembled response for PII leakage and policy violations |
| **Response delivered** | Final answer returned to the user, or a block notice |

## Mapping to MASO controls

| Demo stage | MASO control |
|------------|-------------|
| Input judge | [Prompt, Goal & Epistemic Integrity](controls/prompt-goal-and-epistemic-integrity.md) |
| Planner | [Execution Control](controls/execution-control.md) |
| Tool-call judge | [Privileged Agent Governance](controls/privileged-agent-governance.md) |
| Executor | [Execution Control](controls/execution-control.md) |
| Output judge | [Data Protection](controls/data-protection.md) |
| Event log | [Observability](controls/observability.md) |

!!! info "References"
    - [Prompt, Goal & Epistemic Integrity](controls/prompt-goal-and-epistemic-integrity.md)
    - [Execution Control](controls/execution-control.md)
    - [Privileged Agent Governance](controls/privileged-agent-governance.md)
    - [Data Protection](controls/data-protection.md)
    - [Observability](controls/observability.md)
    - [Multi-Agent Risk Demo (detailed walkthrough)](../extensions/examples/multi-agent-risk-demo.md)
