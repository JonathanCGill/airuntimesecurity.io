---
description: Research insights on why runtime behavioral monitoring solves AI security challenges that pre-deployment testing alone cannot address. The evidence base for risk-proportionate controls.
---

# Insights

The *why* before the *how*. Each article identifies a specific problem that the [core controls](../core/controls.md) and [worked examples](../extensions/examples/README.md) then solve. Together, they make the case for risk-proportionate runtime controls that reduce harm without imposing disproportionate process.

!!! tip "New here? Follow the Golden Thread."
    The [Reading Paths](../reading-paths.md) page sequences these articles into a guided walkthrough of the framework. The **Golden Thread** takes you from *why runtime security?* through *which controls?* to *how do they improve over time?* in roughly two hours. If you do not know where to start, start there.

## Core Arguments

Six articles carry the main argument. Read these, in order, and you have the case for runtime AI security in full. Everything else in **Deep Dives** elaborates, extends, or stress-tests these claims.

| # | Article | The argument |
|---|---------|-------------|
| 1 | [Why AI Security Is a Runtime Problem](why-ai-security-is-a-runtime-problem.md) | AI systems are non-deterministic. Pre-deployment testing cannot prove future safety. Security must be continuous. |
| 2 | [Why Your AI Guardrails Aren't Enough](why-guardrails-arent-enough.md) | Guardrails catch known-bad patterns. Novel attacks, semantic violations, and emergent behaviour walk straight past them. |
| 3 | [The Judge Detects. It Doesn't Decide.](judge-detects-not-decides.md) | An asynchronous LLM evaluator detects unknown-bad against declared intent, without blocking, and informs humans rather than replacing them. |
| 4 | [Infrastructure Beats Instructions](infrastructure-beats-instructions.md) | Telling an agent what not to do fails. Make violations technically impossible through controls enforced outside the agent. |
| 5 | [Humans Remain Accountable](humans-remain-accountable.md) | AI assists decisions; humans own outcomes. The Judge makes oversight scalable, not optional. |
| 6 | [The Feedback Loops That Make It Work](feedback-loops.md) | Four loops at different speeds turn guardrails, judges, humans, and outcomes into a self-improving system. Without them, every layer degrades. |

!!! abstract "After the core six"
    If those six landed and you want more depth on a specific layer, the [Golden Thread](../reading-paths.md#the-golden-thread-guardrails-judges-and-why-they-work-together) adds *Containment Through Intent*, *Process-Aware Evaluation*, *The Constraint Curve*, *Practical Guardrails*, *Judge Assurance*, and *What Works* to fill out the full architecture.

## Deep Dives

The rest of the library, grouped by theme. Expand the section you need. If you are trying to match a specific problem to a specific control, the [core controls index](../core/README.md) and the [worked examples](../extensions/examples/README.md) are usually a faster route.

??? note "Foundations: other framing arguments"
    Alternative entry points into the same thesis. Read these when the core six raise a question or when you want a different angle on the same ground.

    | Article | One-line summary |
    |---------|-----------------|
    | [The First Control: Choosing the Right Tool](the-first-control.md) | The best way to reduce AI risk is to not use AI where it doesn't belong. |
    | [The Model You Choose Is a Security Decision](the-model-you-choose.md) | A flawed model makes every downstream control harder. Evaluate security posture, not just capability. |
    | [Why Containment Beats Evaluation](why-containment-beats-evaluation.md) | You cannot evaluate your way out of non-determinism. Containment bounds what the system can do, regardless of what it tries. |
    | [Security as Enablement, Not Commentary](security-as-enablement.md) | Security creates value when delivered as platform infrastructure, not as narrative that diagnoses teams from the sidelines. |
    | [Risk Tier Is Use Case, Not Technology](risk-tier-is-use-case.md) | Classification is about deployment context, not model capability. |

??? note "Architecture: how the layers fit"
    The internal mechanics of the three-layer pattern, its reference points, and its limits.

    | Article | One-line summary |
    |---------|-----------------|
    | [Practical Guardrails](practical-guardrails.md) | What guardrails should catch: international PII, RAG filtering, exception governance, five pipeline points. |
    | [Containment Through Declared Intent](containment-through-intent.md) | Declared intent is the organising principle that gives every defence layer its reference point. |
    | [The Intent Layer](the-intent-layer.md) | Mechanical controls constrain what agents can do; semantic evaluation determines whether actions align with objectives. |
    | [Process-Aware Evaluation](process-aware-evaluation.md) | Evaluating what an agent produced matters less than evaluating how it got there. |
    | [The Constraint Curve](the-constraint-curve.md) | Proportionate controls find the peak. Over-constraining destroys the value that justified using an LLM. |
    | [The Verification Gap](the-verification-gap.md) | Current safety approaches cannot confirm ground truth. Solved by [Judge Assurance](../core/judge-assurance.md). |
    | [Automated Risk Tiering](automated-risk-tiering.md) | Classification should take two minutes, produce an immediate result, and auto-apply the controls that make the risk manageable. |
    | [The Hallucination Boundary](the-hallucination-boundary.md) | Tolerance for hallucination is a function of decision authority, blast radius, and reversibility. |

??? note "Threats and attack surfaces"
    Where the risk actually lives in production systems: retrieval, tooling, supply chain, memory, and modality.

    | Article | One-line summary |
    |---------|-----------------|
    | [RAG Is Your Biggest Attack Surface](rag-is-your-biggest-attack-surface.md) | Retrieval pipelines bypass your existing access controls. |
    | [The MCP Problem](the-mcp-problem.md) | The protocol everyone is adopting gives agents universal tool access without authentication, authorisation, or monitoring. |
    | [The Supply Chain Problem](the-supply-chain-problem.md) | You don't control the model you deploy. |
    | [The Agent Supply Chain Crisis](the-agent-supply-chain-crisis.md) | The agents you compose are a new supply chain with new failure modes. |
    | [The Memory Problem](the-memory-problem.md) | Long context and persistent memory create new risks. |
    | [Multimodal AI Breaks Your Text-Based Guardrails](multimodal-breaks-guardrails.md) | Images, audio, and video bypass text controls. |
    | [Evaluation Integrity Risks](evaluation-integrity-risks.md) | The evaluator can be gamed, poisoned, or quietly wrong. |
    | [You Don't Know What You're Deploying](you-dont-know-what-youre-deploying.md) | Version drift, silent swaps, and opaque weights turn deployment into a moving target. |
    | [The Sandbox Escape Problem](the-sandbox-escape-problem.md) | Tool runtimes are harder to contain than the models that call them. |

??? note "Agentic AI: where the pattern meets its limits"
    Multi-agent systems, orchestrators, and long-running behaviour.

    | Article | One-line summary |
    |---------|-----------------|
    | [When Agents Talk to Agents](when-agents-talk-to-agents.md) | Multi-agent systems have accountability gaps. |
    | [Agentic Drift](agentic-drift.md) | Objectives, context, and tools drift away from declared intent over time. |
    | [The Orchestrator Problem](the-orchestrator-problem.md) | The most powerful agents in your system have the least controls applied to them. |
    | [The Long-Horizon Problem](the-long-horizon-problem.md) | Security properties you validated on day one may not hold on day thirty. Time itself is an attack vector. |
    | [The Visibility Problem](the-visibility-problem.md) | You can't govern AI you don't know is running. Shadow AI, inventories, and governance KPIs. |
    | [When the Pattern Breaks](when-the-pattern-breaks.md) | The three-layer pattern designed for single-agent systems fails to scale in complex multi-agent architectures. |
    | [Securing the Connective Tissue](securing-the-connective-tissue.md) | The attack surface has shifted from models to the space between them. |

??? note "Models and technology"
    Model-level properties that change what the surrounding controls must do.

    | Article | One-line summary |
    |---------|-----------------|
    | [When AI Thinks Before It Answers](when-ai-thinks.md) | Reasoning models need reasoning-aware controls. |
    | [The Backbone Problem](the-backbone-problem.md) | Concentrated dependency on a handful of backbone models creates systemic risk. |
    | [Open-Weight Models Shift the Burden](open-weight-models-shift-the-burden.md) | Self-hosted models inherit the provider's control responsibilities. |
    | [Temporal Decay](temporal-decay.md) | Correlated model decay degrades every control layer simultaneously. |
    | [You Can't Validate What Hasn't Finished](you-cant-validate-unfinished.md) | Real-time streaming breaks the validation model. |
    | [When Learning Goes Wrong](when-learning-goes-wrong.md) | Online learning and RLHF feedback loops can drift models out of alignment silently. |
    | [Beyond Language Models](beyond-language-models.md) | Code, embeddings, and tool-use models need their own control stories. |

??? note "Evidence and analysis"
    Deeper examinations of where the framework meets production reality: what works, what scales, and what the research actually supports.

    | Article | One-line summary |
    |---------|-----------------|
    | [State of Reality](state-of-reality.md) | The AI security threat is real, specific, and concentrated in measurable failure modes. |
    | [What Works](what-works.md) | Deployed controls are measurably reducing breach detection time and costs. |
    | [What Scales](what-scales.md) | Security controls succeed only if their cost grows slower than the system they protect. |
    | [The Evidence Gap](the-evidence-gap.md) | What research actually supports, and where the science hasn't caught up to the architecture. |
    | [Risk Stories](risk-stories.md) | Real production incidents show where missing controls caused or worsened failures. |
    | [The Flight Recorder Problem](the-flight-recorder-problem.md) | You log what happened but not why, or how to replay it. AI systems need provenance chains, not just event logs. |
    | [PACE Resilience](../PACE-RESILIENCE.md) | How the three-layer architecture achieves operational resilience through layered, independent control redundancy. |
    | [Graph-Based Agent Monitoring](../extensions/technical/graph-based-agent-monitoring.md) | Modelling agent interactions as a live graph to detect anomalous behaviour in near real-time. |

!!! info "References"
    - [Reading Paths](../reading-paths.md)
    - [Minimum Viable AIRS](../minimum-viable-airs.md)
    - [Architecture Overview](../ARCHITECTURE.md)
    - [Core Controls](../core/README.md)
    - [Worked Examples](../extensions/examples/README.md)
    - [Templates](../extensions/templates/README.md)
