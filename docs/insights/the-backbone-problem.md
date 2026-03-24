---
description: "Why backbone LLM selection is a measurable security control: the b³ benchmark results, threat snapshot methodology, and what 194,000 adversarial attacks reveal about model-level vulnerability in agentic AI."
---

# The Backbone Problem

*The model you put inside your agent determines how hard it is to break.*

When teams build AI agents, they pick a backbone LLM based on capability: reasoning quality, tool use, instruction following, cost. Security, if it features at all, is assumed to be handled by the layers wrapped around the model: guardrails, system prompts, output filters.

That assumption is now quantifiably wrong. Different backbone LLMs have measurably different attack surfaces, and the differences are large enough to matter more than the defences you put around them.

## The b³ Benchmark

At ICLR 2026, researchers from Lakera AI, the UK AI Security Institute, ETH Zürich, and the University of Oxford published *Breaking Agent Backbones*. They introduced the **b³ benchmark**: a systematic evaluation of how backbone LLM choice affects AI agent security, tested across 34 models using 194,331 crowdsourced adversarial attacks.

The paper makes two contributions. The first is a formal framework called **threat snapshots**. The second is the benchmark itself.

### Threat Snapshots

A threat snapshot captures a single moment in an agent's execution where an LLM vulnerability can manifest. It records:

- **Agent state:** the system description, current state, and full model context at that moment.
- **Threat description:** how the attack is categorised, how it enters the context, and how success is scored.

The key insight is abstraction. By treating each LLM call as stateless (all relevant context is present in the call), you can assess backbone vulnerability at the atomic level without simulating complete agentic flows. This is cheaper and more targeted than full-system red-teaming.

Multi-turn attacks (like Crescendo) and multi-agent attacks are modelled as chains of threat snapshots, with compound risk estimated as the minimum vulnerability score across the chain. If any link holds, the attack fails.

### Attack Taxonomy

The benchmark categorises attacks along two dimensions.

**By vector and objective:**

| Dimension | Categories |
|-----------|------------|
| **Vectors** | Direct (attacker is the user) and indirect (attack embedded in documents, RAG results, tool definitions, memory entries, websites) |
| **Objectives** | Data exfiltration, content injection, decision/behaviour manipulation, denial of service, system/tool compromise, content policy bypass |

**By task type** (what LLM function is being attacked):

| Code | Task Type | Example |
|------|-----------|---------|
| DIO | Direct instruction override | User convinces agent to ignore system prompt |
| IIO | Indirect instruction override | Poisoned document overrides agent behaviour |
| DTI | Direct tool invocation | User tricks agent into calling unauthorised tool |
| ITI | Indirect tool invocation | Malicious tool description triggers unintended action |
| DCE | Direct context extraction | User extracts system prompt or internal state |
| DAIS | Denial of AI service | User causes agent to stop functioning |

### Realistic Scenarios

The benchmark includes 10 threat snapshots covering real-world agent architectures:

- A **cycling coach** (system prompt extraction).
- A **travel planner** (phishing link injection via web content).
- A **desktop chat with MCP tools** (PII exfiltration via poisoned tool description).
- A **mental health chatbot** (profanity elicitation).
- A **personal assistant with memory** (content hijacking via memory poisoning).
- A **financial advisor** (structured output manipulation via uploaded document).
- A **code review assistant** (malicious code injection via rule files).
- A **shopping agent** (tool extraction).
- A **corporate messenger** (unauthorised email via tool invocation).
- A **legal assistant with RAG** (data exfiltration via RAG document).

Each scenario was tested at three defence levels: **L1** (minimal system prompt), **L2** (stronger prompt with more benign context), and **L3** (LLM-as-Judge defence using the same backbone). Attacks were collected through a gamified red-teaming challenge with 947 participants. Only 210 attacks were selected from 194,331 total: a 0.1% selection rate that prioritises quality over volume.

## What the Results Show

### The Rankings

The overall security ranking (most secure first, R = reasoning enabled):

| Rank | Model | Notes |
|------|-------|-------|
| 1 | **claude-haiku-4-5 (R)** | Most secure across all defence levels |
| 2 | claude-sonnet-4-5 (R) | |
| 3 | claude-haiku-4-5 | Strong even without reasoning |
| 4 | grok-4 (R) | |
| 5 | claude-sonnet-4-5 | |
| 6 | grok-4-fast (R) | |
| 7 | claude-sonnet-4 (R) | |
| 8 | gpt-5.1 (R) | High capability, only 8th in security |
| 9 | claude-opus-4-1 (R) | |
| 10 | gpt-5 (R) | |

### Key Findings

**Reasoning improves security.** Enabling reasoning consistently lowered vulnerability scores across most models. The exception: tiny models, where reasoning actually degraded security. For agents handling sensitive operations, enabling reasoning modes is a low-cost security improvement.

**Model size does not correlate with security.** Larger models within the same family showed no significant advantage without reasoning, and only modest gains with reasoning enabled. This directly challenges the assumption that bigger models are inherently safer.

**Capability correlates with security, but insufficiently.** There is a clear correlation with agentic intelligence benchmarks. But the two highest-capability models (gpt-5.1 and kimi-k2-thinking) ranked only 8th and 14th in security. Capability is necessary but not sufficient.

**Closed-weight systems outperform open-weight models.** The top-ranked models are all closed-weight, though this includes provider-side guardrails as a confounding factor. The best open-weight model (kimi-k2-thinking at 0.34) still beats some frontier closed models.

**Rankings vary by task type.** A model that resists indirect instruction override well may be vulnerable to direct tool invocation. Security profiles are not uniform across attack types. Backbone selection should be use-case-specific, not based on overall rankings alone.

**Top models are consistent across defence levels.** claude-haiku-4-5 remained the most secure across L1, L2, and L3. The defence layer you choose does not change which backbone to pick. Good backbones are good backbones regardless of wrapping.

!!! warning "Quality Over Quantity"
    Only 0.1% of the 194,331 collected attacks were selected for the final benchmark. This validates the emphasis on realistic adversarial testing over synthetic or templated attack generation. Automated red-teaming that generates thousands of low-quality probes is not a substitute for skilled human adversaries.

## What This Means for Runtime Security

### Backbone Selection Is a Security Control

This is the central finding. The b³ results give empirical backing to what [The Model You Choose Is a Security Decision](the-model-you-choose.md) argues qualitatively: different backbones have measurably different attack surfaces.

The practical implication is that backbone selection belongs in the risk assessment, not just the capability evaluation. When the framework's [risk tiers](../core/risk-tiers.md) require stronger controls at higher tiers, the choice of backbone LLM is one of those controls.

### Attack Vectors Map to MASO Control Domains

The six-category attack objective taxonomy maps directly to what MASO already monitors:

| b³ Attack Objective | MASO Control Domain |
|--------------------|--------------------|
| Data exfiltration | [Data Protection](../maso/controls/data-protection.md) |
| Content injection | [Prompt, Goal, and Epistemic Integrity](../maso/controls/prompt-goal-and-epistemic-integrity.md) |
| Decision/behaviour manipulation | [Execution Control](../maso/controls/execution-control.md) |
| Denial of service | [Execution Control](../maso/controls/execution-control.md) |
| System/tool compromise | [Supply Chain](../maso/controls/supply-chain.md) |
| Content policy bypass | [Observability](../maso/controls/observability.md) |

The indirect injection vectors, via RAG, MCP tools, memory, and documents, are precisely the attack surfaces that MASO's guardrails layer should be monitoring. The b³ scenarios read like a threat catalogue for the [MCP problem](the-mcp-problem.md), [memory problem](the-memory-problem.md), and [RAG attack surface](rag-is-your-biggest-attack-surface.md) that this framework already identifies.

### Threat Snapshots as a Governance Methodology

The threat snapshot framework offers a practical approach for MASO's evaluation requirements. Rather than testing complete agent flows end to end, security teams can decompose agents into threat snapshots and assess backbone vulnerability at each critical decision point. This is:

- **Cheaper** than full-system red-teaming.
- **More targeted**, because you test the specific states where attacks manifest.
- **Composable**, because multi-turn and multi-agent attacks are chains of snapshots.
- **Repeatable**, because the snapshot is a static artefact you can re-evaluate when you swap backbones or update models.

This fits directly into the [process-aware evaluation](process-aware-evaluation.md) methodology the framework already recommends.

### Size Is Not Security

MASO's risk-tiering should not assume larger models are inherently more secure. The b³ data shows this is empirically false without reasoning, and only weakly true with it. claude-haiku-4-5, one of the smaller frontier models, ranked first in security. Risk assessments that use model size as a proxy for security are building on a false foundation.

### Task-Specific Vulnerability Profiles

A model that is strong against indirect instruction override may be weak against direct tool invocation. This means backbone selection should be driven by the dominant attack vectors for the specific agent architecture:

- An agent exposed to untrusted documents (RAG, file uploads) needs a backbone that resists **indirect instruction override**.
- An agent with tool-calling authority needs a backbone that resists **direct and indirect tool invocation**.
- An agent handling sensitive data needs a backbone that resists **context extraction**.

One backbone does not fit all agents, even within the same organisation.

### Defence-in-Depth Validation

The three-level defence structure in b³ (prompt hardening, context management, LLM-as-Judge) provides independent evidence that prompt-level defences alone are insufficient. This is consistent with the framework's [three-layer architecture](why-guardrails-arent-enough.md): guardrails for speed, Model-as-Judge for depth, human oversight for judgment. No single layer is reliable on its own, but the layers compound.

## What Defenders Should Do

**Include backbone security in model selection.** Use b³ results (or equivalent benchmarks) alongside capability evaluations. A model that scores well on coding benchmarks but poorly on indirect instruction override is a liability for any agent that processes external documents.

**Enable reasoning for sensitive agents.** The data is clear: reasoning modes reduce vulnerability. For agents operating at [Tier 2 and above](../core/risk-tiers.md), reasoning should be enabled by default unless latency constraints make it impractical.

**Match backbones to threat profiles.** Do not use overall security rankings. Look at task-type-specific scores. Pick the backbone that is strongest against the attack vectors your agent architecture is most exposed to.

**Adopt threat snapshots for evaluation.** Decompose your agents into the critical states where LLM vulnerabilities manifest. Test backbone security at those points. Re-test when you change models, update prompts, or modify tool access.

**Do not rely on prompt-level defences alone.** The L1 to L3 progression shows improvement, but even L3 (LLM-as-Judge with the same backbone) does not eliminate vulnerability. The Judge needs a different backbone from the agent it evaluates, and infrastructure controls must exist independently of any LLM layer.

**Invest in quality adversarial testing.** The 0.1% selection rate is the headline number. Thousands of automated attack probes are less valuable than a handful of expert-crafted adversarial inputs. Red-teaming quality beats red-teaming volume.

## Related Reading

| If you need... | Go to |
|----------------|-------|
| Model selection as a security decision | [The Model You Choose Is a Security Decision](the-model-you-choose.md) |
| Prompt injection and indirect attacks | [RAG Is Your Biggest Attack Surface](rag-is-your-biggest-attack-surface.md) |
| MCP tool-based attack vectors | [The MCP Problem](the-mcp-problem.md) |
| Memory poisoning risks | [The Memory Problem](the-memory-problem.md) |
| Judge architecture and independence | [Judge Assurance](../core/judge-assurance.md) |
| Process-aware evaluation methodology | [Process-Aware Evaluation](process-aware-evaluation.md) |
| Risk-proportionate control selection | [Risk Tiers and Control Selection](../core/risk-tiers.md) |
| MASO observability controls | [Observability](../maso/controls/observability.md) |

!!! info "References"
    - [Bazinska, A. et al. (2026) *Breaking Agent Backbones: Benchmarking Backbone LLM Robustness for AI Agents*. ICLR 2026. Lakera AI, UK AISI, ETH Zürich, University of Oxford.](https://arxiv.org/abs/2603.02277)
    - [b³ Benchmark and threat snapshot framework](https://github.com/lakeraai/b3-benchmark)
