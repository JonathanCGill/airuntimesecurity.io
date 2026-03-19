# The Orchestrator Problem

*The most powerful agents in your system have the least security controls applied to them.*

## The Implicit Trust

Multi-agent security frameworks - including this one, until now - share a structural assumption: the orchestrator is trusted. It routes tasks, manages lifecycle, sequences execution. The controls focus on task agents - the ones that read data, call tools, generate outputs. The orchestrator sits above them, assumed to be benign.

This assumption is wrong. And its consequences are significant.

In production multi-agent systems - LangGraph, AutoGen, CrewAI, AWS Bedrock multi-agent - the orchestrator is not a simple router. It is an LLM. It decomposes goals into sub-tasks. It selects which agents to invoke. It interprets intermediate results. It decides what to do next.

It is, by every meaningful definition, an agent. But it operates outside the control architecture designed for agents.

## Why the Orchestrator Is the Highest-Value Target

The orchestrator has the broadest view of any component in the system. It sees:

- The original user intent
- Every agent's output
- Every intermediate state
- The full task decomposition plan

It controls:

- Which agents are invoked and in what order
- What information flows between agents
- When to retry, escalate, or terminate
- How results are aggregated into a final output

A compromised task agent can misuse one tool. A compromised orchestrator can **route sensitive data to a compromised agent**, **suppress evaluation steps**, **select the weakest agent for the hardest task**, or **decompose a harmful goal into individually benign sub-tasks** that no per-agent control catches.

The orchestrator doesn't need tool access to cause harm. It causes harm through decisions.

## Three Privileged Roles, One Governance Gap

The problem extends beyond orchestrators. Multi-agent systems have three classes of agent with elevated authority that the current framework treats differently from task agents - but shouldn't:

### 1. The Orchestrator

**What it does:** Decomposes goals, selects agents, sequences execution, interprets results, aggregates outputs.

**Current controls:** IA-2.5 prevents direct tool invocation. IA-1.3 blocks credential inheritance. That's it.

**What's missing:** Behavioral monitoring of orchestrator decisions. Goal integrity verification of the orchestrator's own planning. Controls for when the orchestrator's task decomposition itself is the attack vector.

**The threat:** An orchestrator that decomposes "summarise customer complaints" into "extract all customer email addresses" and "send to external endpoint" has not violated any tool restriction. It has violated intent through planning.

### 2. The Evaluator (Model-as-Judge)

**What it does:** Assesses task agent outputs for quality, safety, policy compliance. Approves, escalates, or blocks.

**Current controls:** Must be an independent model, ideally different provider. Operates as Layer 2 defence. EC-3.3 adds multi-model cross-validation at Tier 3.

**What's missing:** Governance of the Judge's own criteria. Drift detection on Judge performance. Disagreement resolution procedures beyond "escalate to human." Monitoring of whether the Judge is itself being influenced through adversarial inputs.

**The threat:** If the Judge's evaluation criteria drift - through prompt injection in criteria templates, training data poisoning of the judge model, or gradual calibration decay - Layer 2 collapses silently. Every task agent output passes because the standard has shifted. The system reports green while the controls have effectively been disabled.

### 3. The Observer

**What it does:** Monitors all agents, scores anomalies, triggers PACE escalation. At Tier 3, operates on separate infrastructure with kill switch authority.

**Current controls:** OB-3.3 requires separate infrastructure and read-only access. Cannot be influenced by task agents.

**What's missing:** Monitoring of the observer itself. Secondary authorisation for kill switch activation. Controls for observer miscalibration (false positives that degrade system availability, false negatives that miss real threats).

**The threat:** An observer that has drifted into over-sensitivity repeatedly triggers kill switches, degrading the system into permanent Contingency mode. Operators disable the observer to restore service. The system now runs without its safety net, and nobody has formally accepted that risk.

## The Recursion Problem

Each of these privileged agents exists to provide assurance over the layer below it. The orchestrator plans for task agents. The Judge evaluates task agents. The observer monitors everyone.

But who monitors the privileged agents?

The classical answer is "another layer" - a meta-judge, a super-observer, an orchestrator-of-orchestrators. This creates infinite recursion. Every watchman needs a watchman.

The practical answer is: **you break the recursion with independence and measurement, not with more layers.**

- The orchestrator's decisions are measured against the original user intent using a model that is not the orchestrator
- The Judge's performance is calibrated against known-good and known-bad test cases, independently of the Judge's own self-assessment
- The observer's accuracy is measured by injecting known anomalies (red team) and verifying detection

You don't need a meta-judge. You need **calibration testing** - periodic verification that each privileged agent still does what you think it does.

## Nested Orchestration

Production systems are already moving beyond flat topologies. A planning agent decomposes a complex task. A sub-orchestrator manages a cluster of specialist agents. Another sub-orchestrator handles a different cluster. Results flow up through aggregation agents before reaching the user.

This creates multi-level hierarchies where MASO's current controls - designed for a single orchestration level - face ambiguity:

**Does IA-2.4 (no transitive permissions) apply at every level?** In principle, yes. In practice, if Sub-orchestrator B manages Agents C, D, and E, and Sub-orchestrator B was invoked by Orchestrator A, the delegation chain is: User → A → B → C. Each boundary needs explicit permission scoping, not just the first.

**Where does the Judge sit in a nested topology?** Per-agent evaluation at the leaf level catches individual failures. But who evaluates the sub-orchestrator's aggregation decisions? Who evaluates the top-level orchestrator's decomposition? A single Judge instance evaluating final output misses failures that occurred and were smoothed over at intermediate levels.

**What is the blast radius of a compromised sub-orchestrator?** If Sub-orchestrator B is compromised, its entire agent cluster is potentially affected. EC-2.3 (blast radius caps) currently applies per-agent, not per-orchestration-subtree. A compromised sub-orchestrator can coordinate its agents within their individual caps but achieve aggregate harm that exceeds any single cap.

## What Needs to Change

The core principle: **every agent with authority over other agents must have controls proportionate to that authority.**

An orchestrator that plans, selects, and sequences has more influence over the system outcome than any individual task agent. Its controls should reflect that. An evaluator that approves or blocks every output is a single point of trust. Its governance should reflect that.

The current MASO framework handles task agents well. The gap is privileged agents - the agents that control, evaluate, and monitor other agents. They need:

1. **Behavioral monitoring that matches their role.** Orchestrator decisions are measured against user intent, not just tool invocations. Judge accuracy is tracked and calibrated, not assumed. Observer precision is verified through injection testing.

2. **Independence that is verified, not assumed.** Saying "the Judge uses a different model" is a design decision. Verifying that the Judge is still producing independent evaluations - not drifting toward the task agents' outputs - is an ongoing control.

3. **Governance at every orchestration boundary.** In nested topologies, each delegation level needs explicit permission scoping, evaluation coverage, and blast radius containment. A compromised sub-orchestrator is a different threat from a compromised task agent - the controls should recognise this.

4. **Calibration as a first-class control.** Red team testing of privileged agents - injecting known-bad orchestrator plans, presenting the Judge with known policy violations, triggering known anomalies for the observer - is not optional. It's the mechanism that breaks the recursive "who watches the watchmen" problem.

## The Design Principle

The three-layer control architecture says: no single control is sufficient. Layer your defences.

For task agents, the layers are guardrails, Judge, and human oversight.

For privileged agents, the layers are: **role constraints** (what the agent can decide), **independent measurement** (whether its decisions are correct), and **calibration testing** (whether its judgement is still reliable).

The privileged agent is not exempt from the architecture. It is subject to a version of the architecture that matches its threat model.

