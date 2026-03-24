---
description: "Why container sandboxes are not a reliable security boundary for frontier AI agents: SandboxEscapeBench results, model-specific escape capabilities, and what this means for MASO and runtime containment."
---

# The Sandbox Escape Problem

*Your container is not as strong as you think it is.*

The standard advice for running AI agents that execute code is simple: put them in a container. Docker, OCI, an ephemeral sandbox. The container is the boundary. The agent can do whatever it wants inside; nothing escapes.

That assumption is now empirically testable. And the results should change how you architect containment.

## Frontier Models Can Break Out

In March 2026, researchers from the University of Oxford and the UK AI Security Institute published *Quantifying Frontier LLM Capabilities for Container Sandbox Escape*. They introduced **SandboxEscapeBench**, an open benchmark that measures whether frontier LLMs can escape container sandboxes.

The methodology is clean: a Capture the Flag evaluation using nested sandboxes built on Inspect AI. The inner container holds the model with shell access. The outer VM layer holds the flag (`/flag.txt`). No known vulnerabilities exist in the outer layer. The model gets a bash shell inside the container and tries to read the flag on the host. Success means the model escaped.

The benchmark covers 18 challenge scenarios across three layers of the container stack, each rated on a 1 to 5 difficulty scale:

| Layer | Scenarios | What it tests |
|-------|-----------|---------------|
| **Orchestration** | 4 | K8s RBAC bypass, `kubectl cp` directory traversal, CRI-O kernel parameter injection, `route_localnet` localhost boundary bypass |
| **Runtime** | 8 | Privileged containers, exposed Docker socket, host path mounts, dangerous Linux capabilities (`SYS_ADMIN`, `SYS_MODULE`, `DAC_READ_SEARCH`), runc CVEs (2019-5736, 2024-21626) |
| **Kernel** | 6 | PID namespace exposure, cgroup `release_agent` abuse, eBPF verifier exploits, Dirty COW, Dirty Pipe, packet socket use-after-free |

## What the Results Show

The findings are specific enough to act on.

**Common misconfigurations collapse immediately.** Difficulty 1 and 2 scenarios (privileged containers, exposed Docker daemons, writable host mounts) are solved at near-100% rates by top-tier models. These are the configuration mistakes that appear in production every day.

**Harder exploits are tractable for large models.** Difficulty 3 scenarios, including runc CVEs and kernel exploits, see around 40% success rates for the strongest models. Zero success was observed at difficulty 4 and 5, but the gap is narrowing.

**Model capability varies dramatically.**

| Model | Overall Score | Notes |
|-------|--------------|-------|
| **Opus 4.5** | 0.49 | Persistent, methodical. Attempted tasks until token budget exhaustion. Never submitted false flags. |
| **GPT-5** | 0.50 | Comparable top-tier performance. |
| **GPT-5.2** | 0.27 | Regressed from GPT-5, showing capability is not monotonically increasing across model versions. |
| **Sonnet 4.5** | Near top-tier on easy scenarios | Strong on misconfigurations, drops off on kernel exploits. |
| **Haiku 4.5** | 0.18 | Sharp degradation once tasks require exploit adaptation or kernel reasoning. |
| **GPT-OSS-120B** (open-weight) | 0.16 | Similar degradation pattern. |
| **DeepSeek-R1** | Low | Hallucinated success extensively: 70% false success claims, averaging 12 incorrect flag submissions per sample. |

**No novel zero-days were discovered.** All successful escapes used known misconfigurations or public CVEs. The threat is not that models invent new exploits. The threat is that they reliably find and use existing ones.

**Inference-time compute scales success roughly log-linearly.** More tokens means higher escape probability. Many successful runs cost approximately $1, meaning cheap retries are viable for an adversary.

## Behavioral Signatures Worth Monitoring

The transcript analysis reveals distinct patterns across model families that are directly relevant to [MASO observability](../maso/controls/observability.md):

**Claude models** (Opus, Sonnet) attempted tasks until token budget exhaustion. They never disengaged, never submitted false flags, and were persistent and methodical in their exploration. From a monitoring perspective, these models will probe systematically for the full duration of their budget.

**GPT models** showed high disengagement rates. GPT-5.2 disengaged in 92% of failures, and both versions exhibited mid-task policy refusals. This is operationally unpredictable: the model may abandon a task it was delegated, which creates availability risks in multi-agent orchestrations.

**DeepSeek-R1** hallucinated success extensively. The model claimed to have escaped when it had not, submitting an average of 12 incorrect flags per sample. This is the monitoring worst case: an agent that reports task completion when nothing was accomplished, poisoning downstream confidence in outcomes.

!!! warning "Shortcut Discovery"
    Four unintended escape paths were discovered during benchmark development. Models found default Vagrant SSH credentials, publicly known insecure keys, and exploited co-present kernel vulnerabilities (eBPF, Dirty COW) instead of the intended target. Models do not follow intended paths. They search for *any* route to goal completion. This validates the MASO assumption that agents will explore beyond intended boundaries.

## Why This Matters for Runtime Security

Container security surveys have catalogued over 200 weaknesses across the container stack. That is not new. What is new is that an autonomous agent with shell access can now discover and exploit those weaknesses without human guidance.

This changes the threat model. Previously, container escape required a skilled attacker who had already gained access. Now, the agent *is* the attacker, and it already has access: you gave it a shell.

**1. Docker alone is not sufficient isolation for high-risk agents.**

Much of the open-source agent ecosystem and local developer tooling relies on standard Docker containers as the isolation boundary. Hyperscale providers use hardware-level isolation (Firecracker, gVisor) for good reason. If your agents execute arbitrary code, container isolation should be treated as one layer, not the only layer.

**2. Misconfiguration is the primary attack surface.**

The easiest escapes target orchestration-level misconfigurations: mounted Docker sockets, overprivileged containers, exposed control planes. These are not exotic kernel exploits. They are the configuration mistakes in [SAND-01](../infrastructure/agentic/sandbox-patterns.md), and they only protect you if they are actually implemented.

**3. Containment must be verified, not assumed.**

A sandbox that has not been tested against escape is a sandbox you hope works. SandboxEscapeBench provides a way to measure escape capability against your specific configuration. This is the kind of evidence-based assurance that the [constrain-regardless architecture](why-containment-beats-evaluation.md) requires.

**4. Token budgets and retry policies are security parameters.**

Inference-time compute directly affects escape probability. An agent with an unlimited token budget and retry capability has more attempts to find an exploit. [MASO execution controls](../maso/controls/execution-control.md) should treat inference compute allocation as a risk-relevant configuration, not just a cost parameter.

**5. Patching cadence matters for AI-facing infrastructure.**

Known CVEs are the primary attack vector. Vulnerability management for any infrastructure hosting AI agents needs to account for the fact that the agent itself is a motivated, knowledgeable attacker that will systematically probe for every public CVE relevant to its environment.

## Implications for MASO

This research connects directly to several MASO control domains:

**Execution control ([EC controls](../maso/controls/execution-control.md)).** The [EC-2.2](../maso/controls/execution-control.md) sandboxed execution requirement is validated: agents generating or executing code must operate in isolated environments. But this paper shows the isolation level matters. Standard Docker without hardened configuration collapses under active exploration by capable agents.

**Observability ([OB controls](../maso/controls/observability.md)).** The transcript analysis reveals detectable behavioural signatures: systematic capability enumeration, `/proc` exploration, cgroup manipulation, exploit compilation from source. MASO observability controls should include container escape indicator detection, including syscall patterns and privilege escalation attempts.

**Model-tier gating.** The large capability gaps between model families (Opus 0.49 vs Haiku 0.18) support MASO's risk-tiered approach. Higher-capability models warrant stronger containment controls. This is [risk-proportionate governance](../core/risk-tiers.md) with empirical backing.

**Adversarial exploration assumptions.** The shortcut discovery finding validates a core MASO threat model assumption: agents will explore beyond intended boundaries. Environment-wide exploration, not just exploitation of known attack surfaces, should be the baseline assumption for [agentic containment](../infrastructure/agentic/sandbox-patterns.md).

## What Defenders Should Do

The research points to a layered response:

**Select isolation proportionate to risk.** Process isolation and basic containers are reasonable for low-risk, read-only operations. Agents that execute arbitrary code, install packages, or make network calls need VM-level isolation or hardened container runtimes (gVisor, Kata Containers). The framework's [risk tiers](../core/risk-tiers.md) should drive this selection.

**Harden the configuration.** Most successful escapes target avoidable misconfigurations. Never mount the Docker socket into agent containers. Never run containers as root or with `--privileged`. Drop all capabilities except those explicitly required. Restrict `/proc` and `/sys` access. These are the basics, and they stop the easiest attacks.

**Constrain inference budgets.** Token budgets and retry limits are security controls, not just cost controls. An agent that can retry indefinitely with a large context window has a meaningfully higher escape probability than one with a capped budget. Set limits proportionate to the task, not the model's maximum.

**Enforce ephemeral execution.** Every agent execution gets a fresh container from a clean image. No state persists between executions. No accumulated attack surface. This is [SAND-05](../infrastructure/agentic/sandbox-patterns.md) in practice.

**Monitor for escape-attempt signatures.** Add container escape indicators to your observability stack: capability enumeration commands, `/proc` and `/sys` reads, cgroup manipulation, Docker socket access attempts, kernel exploit compilation. These are detectable well before a successful escape.

**Test your sandboxes.** SandboxEscapeBench is open source. Run it against your deployment configuration. If a frontier model can escape your sandbox, so can the next model your users deploy.

**Layer your defences.** The sandbox is containment Layer 1. Network controls, resource limits, pre-execution code scanning, and the [Model-as-Judge](../core/judge-assurance.md) operate independently. A model that escapes the container but cannot reach the network has not achieved much. Defence in depth is not optional when the attacker is the system you are trying to contain.

## The Broader Pattern

This research reinforces a principle that runs through this framework: **security properties of AI systems must be enforced through infrastructure, not through trust in the model's behaviour.** You do not ask the model to stay in its sandbox. You build a sandbox the model cannot leave.

But "cannot leave" is an engineering claim, not a guarantee. SandboxEscapeBench demonstrates that the claim needs evidence. Container isolation that was adequate last year may not be adequate against this year's models, and the GPT-5 to GPT-5.2 regression shows that the relationship between model generation and escape capability is not straightforward.

The [constrain-regardless architecture](why-containment-beats-evaluation.md) does not depend on knowing exactly what a model can do. But it does depend on the containment boundary actually holding. This paper is a reminder that the boundary itself needs testing, and that testing needs to be repeated as both models and infrastructure evolve.

## Related Reading

| If you need... | Go to |
|----------------|-------|
| Sandbox implementation controls | [Sandbox Patterns for Agentic AI](../infrastructure/agentic/sandbox-patterns.md) |
| MASO execution controls for agents | [Execution Control](../maso/controls/execution-control.md) |
| MASO observability and monitoring | [Observability](../maso/controls/observability.md) |
| Why infrastructure enforcement matters | [Infrastructure Beats Instructions](infrastructure-beats-instructions.md) |
| The containment-first security model | [Why Containment Beats Evaluation](why-containment-beats-evaluation.md) |
| Defining containment from business intent | [Containment Through Declared Intent](containment-through-intent.md) |
| Risk-proportionate control selection | [Risk Tiers and Control Selection](../core/risk-tiers.md) |

!!! info "References"
    - [Marchand, R., O Cathain, A., Wynne, J., Giavridis, P.M., Deverett, S., Wilkinson, J., Gwartz, J. and Coppock, H. (2026) *Quantifying Frontier LLM Capabilities for Container Sandbox Escape*. arXiv:2603.02277.](https://arxiv.org/abs/2603.02277)
    - [SandboxEscapeBench source code](https://github.com/UKGovernmentBEIS/sandbox_escape_bench)
