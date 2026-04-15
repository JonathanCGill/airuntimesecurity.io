---
description: "AIRS framework guide for insider risk analysts, extending UEBA and behavioural analytics programmes to monitor AI agent behaviour as non-human entities."
---

# Insider Threat Teams

**Insider Risk Analysts, UEBA Engineers, Behavioral Analytics Teams - your programme already solves the problem AI agents create. Here's how to extend it.**

> *Part of [Stakeholder Views](README.md) · [AI Runtime Security](../README.md)*

## The Problem You Already Solve

You monitor humans for behavioral anomalies. You build baselines for how people normally work - when they log in, what they access, how much data they move, who they communicate with. When behavior deviates from that baseline, you investigate.

You classify threats into three categories: negligent insiders who create risk through carelessness, compromised insiders whose credentials have been stolen, and malicious insiders who deliberately abuse their access.

You use UEBA to score risk across multiple dimensions - temporal patterns, access scope, data volume, peer group deviation, communication destinations. You correlate weak signals into strong ones. You've been doing this since Gartner coined UEBA in 2015.

**AI agents are the next entity in your programme.**

An agent has an identity (a non-human identity - NHI). It has access privileges (tools, APIs, data sources). It has a behavioral baseline (what it normally does, when, how often, at what volume). It can be negligent (drifting through accumulated context), compromised (prompt-injected, memory-poisoned), or malicious (sleeper agent, training-time backdoor).

Everything you built for humans applies. The analytical framework transfers. The detection techniques transfer. The risk scoring transfers.

The question isn't whether to monitor agents for insider risk. It's whether you're already doing it - and if not, how quickly you can extend what you have.

## What This Framework Gives You

### A direct mapping from UEBA indicators to agent monitoring

The framework's [Insider Risk Parallel](../extensions/technical/behavioral-anomaly-detection.md#the-insider-risk-parallel) maps your existing indicators directly to agent equivalents:

| Your Indicator (Humans) | Agent Equivalent | What It Catches |
|---|---|---|
| **Unusual working hours** | Agent active when no users or triggers should be driving it | Compromised agent used out-of-band; attacker in a different timezone |
| **Access beyond role** | Agent accessing tools, data, or APIs outside its declared scope | Prompt injection widening blast radius; tool-chain exploitation |
| **Privilege escalation** | Agent requesting broader tool access or cross-tenant data | Delegated authority abuse; injection attempting to escalate |
| **Data volume anomalies** | Agent processing or transmitting significantly more data than baseline | Exfiltration; RAG over-retrieval; runaway loops |
| **New communication destinations** | Agent calling new external APIs or previously unused tools | Exfiltration via tool invocation; supply chain redirect |
| **Peer group deviation** | One agent in a fleet diverges while peers remain stable | Individual compromise; selective poisoning; configuration drift |
| **Session anomalies** | Unusual invocation frequency, duration, or concurrency | Agent driven by attacker with different usage patterns |
| **Behavioral change after events** | Behavior shift correlating with model updates, config changes, or memory additions | Regression; memory poisoning taking effect; configuration tampering |

These aren't analogies. They're the same indicators, applied to a different entity type.

### Three insider threat categories that map to three agent threat categories

| Your Category | Agent Equivalent | Detection Approach |
|---|---|---|
| **Negligent insider** - creates risk through carelessness | Agent drifting through accumulated context, stale memory, or unchecked growth - not malicious, but degrading from policy | Baseline drift detection; long-window analysis; periodic re-validation against acceptance criteria |
| **Compromised insider** - credentials stolen or account taken over | Agent that's been prompt-injected, memory-poisoned, or whose NHI credentials are used from an unexpected context | Temporal anomalies; access pattern changes; peer group divergence; tool usage deviations |
| **Malicious insider** - deliberately abusing access | Agent with misaligned objectives - sleeper agent, training-time backdoor, deliberately reprogrammed through persistent manipulation | Long-horizon monitoring; dormant payload detection; cross-agent temporal correlation |

### An anomaly scoring model your SIEM already understands

The framework's [Observability Controls](../maso/controls/observability.md) define a nine-signal anomaly scoring model (Tier 2+) that maps to your existing UEBA scoring:

| Signal | Weight | Your UEBA Equivalent |
|---|---|---|
| Tool usage pattern | 0.15 | Application access pattern |
| Output quality | 0.20 | Work product quality metrics |
| Response latency | 0.05 | Session timing |
| Message volume | 0.10 | Communication volume |
| Error rate | 0.10 | Failed access attempts |
| Content drift | 0.15 | Behavioral drift from role baseline |
| Cost trajectory | 0.05 | Resource consumption |
| **Temporal profile** | 0.10 | **Working hours analysis** - your strongest signal |
| **Peer group deviation** | 0.10 | **Peer comparison** - your most powerful technique |

The last two were added specifically because your discipline has proven them. The scoring model feeds into PACE escalation (0–40 normal, 40–60 elevated, 60–80 high, 80–100 critical) - the same threshold logic your UEBA risk scoring already uses.

### SIEM/SOAR integration already specified

[OB-2.4](../maso/controls/observability.md) requires agent observability events to be forwarded to enterprise security operations. This means agent anomaly events should appear in your SIEM alongside network, endpoint, and identity alerts - correlated, not siloed.

The agent's NHI should be enrolled in your identity analytics the same way a service account is. The same rules that flag "service account active at unusual hours" should flag "agent active at unusual hours."

## Your Starting Path

Read these in order. Total time: ~60 minutes.

| # | Document | Why You Need It |
|---|---|---|
| 1 | [Behavioral Anomaly Detection](../extensions/technical/behavioral-anomaly-detection.md) | The full insider risk parallel - your indicators mapped to agents, peer group comparison, three threat categories |
| 2 | [Observability Controls](../maso/controls/observability.md) | The anomaly scoring model, nine signals, SIEM integration, decision chain format |
| 3 | [The Long-Horizon Problem](../insights/the-long-horizon-problem.md) | Why short-window detection misses slow attacks - and how anchored baselines and temporal analysis close the gap |
| 4 | [Process-Aware Evaluation](../insights/process-aware-evaluation.md) | Evaluating the agent's reasoning trace, not just its output - the equivalent of reviewing an insider's full activity timeline |
| 5 | [Oversight Readiness](../core/oversight-readiness-problem.md) | How humans become attack vectors, not just reviewers - social engineering the approver, weaponising alert fatigue |

**If you run UEBA on Microsoft Sentinel:** Your entity profiles and peer group profiles already support non-human entities. Adding agent NHIs to the monitored entity set is a configuration change, not a new capability.

**If you run Splunk/Exabeam/Securonix:** The same principle applies - agent identities are entities. Enrol them in your existing behavioral analytics pipeline.

## What You Can Do Monday Morning

1. **Inventory your organisation's AI agent NHIs.** Work with the IAM team to identify every non-human identity associated with an AI agent. Many organisations don't track these separately from service accounts. You can't monitor what you haven't inventoried.

2. **Enrol agent NHIs in your existing UEBA pipeline.** If your UEBA platform supports entity types beyond users (most do - that's what the "E" is for), add agent identities as monitored entities. Start with temporal profiling - when is each agent normally active?

3. **Create agent-specific correlation rules.** Adapt your existing insider risk rules for agents:
    - "Entity active outside established schedule" → flag and investigate
    - "Entity accessing resources outside declared scope" → flag and investigate
    - "Entity data transfer volume >2σ above baseline" → flag and investigate
    - "Entity behavior diverges from peer group" → flag and investigate

4. **Add agent scenarios to your next insider threat exercise.** Your red team tests whether employees can exfiltrate data. Add a scenario where an agent is the exfiltration vector - prompt-injected to send data to an external endpoint, or memory-poisoned to gradually widen its access scope.

5. **Establish a 30-day baseline.** Before you can detect anomalies, you need to know what normal looks like. Collect 30 days of agent activity data - invocation times, tool usage, data volumes, session patterns. This becomes your anchored reference point.

## Common Objections - With Answers

**"Agents aren't insiders - they're software."**
So are service accounts, and your programme already monitors those. The "E" in UEBA exists precisely because non-human entities exhibit the same behavioral patterns as human users - and the same deviations when compromised. An agent with an NHI, access privileges, and a behavioral baseline *is* an entity in your programme. The only question is whether you've enrolled it.

**"The AI security team handles this."**
The AI security team builds guardrails and evaluation layers. You build behavioral baselines and detect anomalies. These are complementary, not competing. The guardrails catch known-bad patterns in real-time. Your UEBA catches behavioral drift, temporal anomalies, and peer group deviations that guardrails don't look for. The [three-layer model](../core/controls.md) needs both.

**"We don't have the data to baseline agents."**
You have the same data you use for service accounts - authentication logs, API call logs, access logs, session metadata. Agent frameworks (LangChain, CrewAI, AutoGen) generate structured logs. The framework's [Observability Controls](../maso/controls/observability.md) specify exactly what to capture. Start with 30 days of collection; refine from there.

**"Our UEBA platform doesn't support AI agents as an entity type."**
It doesn't need to explicitly. If it supports custom entity types or service account monitoring, you can model agents the same way. The behavioral signals (temporal patterns, access scope, volume, peer comparison) are platform-agnostic. The entity type label matters less than the data feeding the model.

**"This doubles the workload for our team."**
It extends existing capability, it doesn't duplicate it. Your correlation rules, risk scoring models, investigation workflows, and escalation procedures all apply. The new work is: inventorying agent NHIs, enrolling them, and tuning thresholds during the initial baselining period. After that, agents are just another set of entities in your existing programme.

## The Bigger Picture

Insider risk programmes exist because organisations learned that perimeter security isn't enough - threats come from inside too. AI agents create the same lesson for a new era: the entity inside your perimeter, with legitimate access, behaving anomalously.

The 15+ years your discipline has invested in UEBA, behavioral baselines, peer group comparison, and composite risk scoring is directly applicable. Agents are entities. Entities have baselines. Deviations from baselines are investigated. The analytical framework doesn't change. The entity type does.

The organisations that extend their insider risk programmes to cover AI agents will detect compromises that organisations relying solely on guardrails and output evaluation will miss. Your programme is the missing layer.

