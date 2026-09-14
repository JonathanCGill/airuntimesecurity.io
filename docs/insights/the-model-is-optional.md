---
description: "Five disclosures in one fortnight let an attacker run an agent's tools without the model ever deciding to call them. Guardrails read model input and a Judge reads model output, so both fail open when there is no model turn to read. Why authorisation has to sit on the action, not the utterance."
---

# The Model Is Optional

*Your guardrails read what goes into the model. Your Judge reads what comes out. The attack now happens between them.*

## Five Disclosures, One Shape

In the first two weeks of August 2026, five separate vendors published fixes for what looks at first like five unrelated bugs. They are one bug, described five ways.

| Disclosure | What the attacker sent | Where the model was |
|---|---|---|
| **Amazon Bedrock AgentCore**, CVE-2026-18830 | A tool-use content block in the final message of an `InvokeHarness` request | Never invoked. The event loop dispatched the named tool directly. |
| **Google ADK for Python**, CVE-2026-18236 | A user-authored session event carrying a function-call part | Never invoked. The confirmation processor never checked that the tool belonged to the agent, needed confirmation, or matched the recorded call. |
| **Vercel AI SDK harnesses**, CVE-2026-64650 and CVE-2026-64651 | A process inside the sandbox whose command line contained an approved helper script's path | Never invoked. The relay authorised on a string match and handed over host secret lookups and cloud API calls. |
| **Azure SRE Agent**, CVE-2026-62830 | An ordinary network request from a low-privileged account | Irrelevant. A missing authorisation check in front of the agent gave up everything its managed identity could reach. |
| **Claude Code**, presented at Black Hat USA by Novee Security | A payload in the value of `git push --receive-pack`, inside single quotes | Present, and beside the point. The validator stripped quoted text before its checks ran, so it and git disagreed about what the string was. |

A sixth, **GhostSplice**, is the same lesson from the other direction. The model is present and refuses the request, so the attacker never asks it. A malicious MCP server splits one instruction across a tool description, a tool result, and a sampling message. Each fragment is genuinely harmless. The composition happens in the context window, which is not a place any control is watching.

## Why the Standard Stack Misses All of It

The three-layer architecture has a load-bearing assumption that has gone unexamined because it used to be true: **the model is where the decision happens**, so putting a control on the model's input and another on its output covers the system.

That assumption produces a specific control placement. Guardrails inspect the prompt. The [Model-as-Judge](judge-detects-not-decides.md) inspects the response, the proposed action, the tool call. Both sit on the model's boundary, which is the right place to sit if every action originates in a model turn.

In every disclosure above, the action did not originate in a model turn. There was no prompt to inspect and no response to evaluate. The guardrail did not fail, and neither did the Judge. **Both were bypassed by a path that never crossed them**, which is worse than failing, because a failing control produces a signal and a bypassed one produces nothing.

This is the thing to internalise: an AI-specific control that reads model traffic is not a control over the agent. It is a control over one component of the agent.

## The Control Plane Nobody Modelled

Between the request arriving and a tool executing, a modern agent runs a lot of code that is not a model:

- an **event loop** that decides which content blocks are instructions and which are data
- a **harness or relay** that carries tool calls across a sandbox boundary to the host
- a **confirmation processor** that decides whether a given call needs approval
- a **command validator** that parses a proposed shell string against a policy
- an **MCP client** that multiplexes descriptions, results, and sampling messages into one context
- an **authorisation check** in front of the whole service
- **configuration files** that determine which tools exist at all

Every one of these has now been the vulnerable component in a shipped product. None of them is covered by anything in a typical AI security programme, because the programme's threat model has one AI-shaped box in it and this is all plumbing around the box.

It is not plumbing. It is the control plane. The model proposes; this code disposes. When it disposes without being asked, the model's judgement, its alignment, its refusal training, and every evaluation you ran against it are simply not in the picture.

## Three Ways It Fails

The five disclosures collapse into three failure modes, and each has a known fix that is unglamorous and decades old.

### 1. Data is promoted to instruction at a parse boundary

AgentCore, ADK, and GhostSplice are all this. Something arrived as content and was read as a directive: a caller-supplied tool-use block, a user-authored function-call part, a tool result that reads as a command. The parser was permissive, so the structure decided its own meaning.

The fix is strict deserialisation and a typed boundary. Reject unknown fields. Reject a `function_call` in a message whose author is `user`. Tag every message with what it is (`data`, `instruction`, `claim`) and refuse to act on `data` no matter how imperative it reads. This is [EC-2.14 inter-agent data contracts](../maso/controls/execution-control.md), [EC-2.15 serialisation boundary validation](../maso/controls/execution-control.md), and [PG-1.4 message source tagging](../maso/controls/prompt-goal-and-epistemic-integrity.md), and the reason those controls read as tediously conventional is that the failure is tediously conventional. It is injection. It has always been injection.

### 2. Two components disagree about the same string

The Claude Code validator stripped single-quoted text and then ran twenty-three checks against what was left. Git did not strip anything, and `--receive-pack` is a flag git executes. The validator and the executor were reading different programs. Vercel's relay is the same class: the relay believed a command line containing an approved script's path identified an approved process, and the operating system had no such opinion.

The fix is that the component enforcing a policy must parse exactly what the component executing it will parse, or it is not enforcing a policy. Where that cannot be guaranteed, allow-list at argument granularity rather than command granularity: permitting `git push` while ignoring its flags permits arbitrary execution, and [EC-1.2 tool allow-lists](../maso/controls/execution-control.md) is only as strong as the granularity you write it at.

### 3. Authorisation is checked in the wrong place, or not at all

Azure SRE Agent is the pure case. There was no clever payload. There was a missing check, and behind it an agent whose managed identity could reach runbooks, telemetry, incident tooling, and the resources they touch. The CVSS 9.9 came from the Scope Changed vector, which is a formal way of saying the blast radius was not the agent.

The fix is that an agent's identity is the security boundary, and it has to be scoped before the agent is switched on, not audited after a critical lands. [IA-1.4 scoped permissions](../maso/controls/identity-and-access.md), [IA-2.4 no transitive permissions](../maso/controls/identity-and-access.md), [EC-2.3 blast radius caps](../maso/controls/execution-control.md), and [EC-3.1 infrastructure-enforced blast radius](../maso/controls/execution-control.md) all exist for this, and none of them requires knowing anything about how the compromise happened. That is the point of them.

## Authorise the Action, Not the Utterance

The framework's answer is not a new layer. It is a correction to where the existing layers attach.

**A control that authorises an utterance asks: is this a safe thing for the model to say?** Guardrails do this on the way in. The Judge does it on the way out. Both are valuable and neither is sufficient, because both require a model turn to exist.

**A control that authorises an action asks: is this call permitted, from this identity, to this target, right now?** It does not care what produced the call. A forged tool-use block, a hijacked relay, a malicious MCP server, and a genuine model decision all arrive at the same gate and are judged by the same rule.

Sorted by which question they ask, the MASO controls split cleanly:

| Authorises the utterance | Authorises the action |
|---|---|
| [PG-1.1 input sanitisation per agent](../maso/controls/prompt-goal-and-epistemic-integrity.md) | [EC-1.1 human approval gate](../maso/controls/execution-control.md) |
| [EC-2.5 Model-as-Judge gate](../maso/controls/execution-control.md) | [EC-1.2 tool allow-lists](../maso/controls/execution-control.md) |
| [PG-2.1 inter-agent injection detection](../maso/controls/prompt-goal-and-epistemic-integrity.md) | [EC-2.14 inter-agent data contracts](../maso/controls/execution-control.md) |
| [PG-1.5 anti-manipulation guardrail](../maso/controls/prompt-goal-and-epistemic-integrity.md) | [EC-2.15 serialisation boundary validation](../maso/controls/execution-control.md) |
| | [IA-1.4 scoped permissions](../maso/controls/identity-and-access.md) |
| | [IA-2.4 no transitive permissions](../maso/controls/identity-and-access.md) |
| | [IA-2.5 orchestrator privilege separation](../maso/controls/identity-and-access.md) |
| | [EC-2.3 blast radius caps](../maso/controls/execution-control.md) |

The left column is the column most AI security programmes have built. The right column is the one that held in August. If you are choosing where to spend the next quarter, that is the answer.

One control sits in neither column and deserves separate mention, with a caveat. [PG-2.2 goal integrity monitoring](../maso/controls/prompt-goal-and-epistemic-integrity.md) compares what the agent is *doing* against the declared objective, and it is the one semantic control whose reference point is the action rather than the utterance. Its reach here depends entirely on where it is wired. As written, PG-2.2 has the Judge compare the working goal against the objective **at each decision point**, so an implementation hooked into the agent's own reasoning loop is bypassed by exactly the same skip these disclosures use: no model turn, no decision point, no comparison. The Azure SRE Agent flaw is the clearest case, because the missing authorisation check is exercised outside the agent altogether, and no control inside the agent can see it. What PG-2.2 offers against this class is conditional rather than guaranteed: wire the comparison to the **tool-dispatch path** rather than the reasoning loop, so that every dispatch is checked against the declared objective whoever originated it, and the forged calls in the AgentCore, ADK, and Vercel cases become visible as actions that no declared objective accounts for. That is an implementation choice the control permits and does not currently require, which makes it a gap to close rather than coverage to claim.

## Where the Framework Is Still Short

Being honest about the gaps is more useful than claiming coverage.

**The agent runtime is not inventoried.** [SC-2.1 AIBOM per agent](../maso/controls/supply-chain.md) enumerates models, tools, RAG sources, MCP servers, and dependencies. It does not name the harness, the relay, the event loop, or the validator as components with versions and known vulnerabilities, and August says they belong there. An AIBOM that lists `claude-opus-5` but not `@ai-sdk/harness-opencode@1.0.27` is describing the wrong asset.

**Some of these have no CVE to scan for.** AWS fixed the managed `InvokeHarness` path but not the comparable model-skipping path in the open-source Strands Python SDK, and issued no CVE and no affected-version range for it. [SC-3.3 continuous dependency scanning](../maso/controls/supply-chain.md) will report a self-hosted Strands deployment clean, because there is nothing to match against. A control whose evidence source is empty is not a control, and this is not a scanner problem, it is a disclosure-practice problem the framework cannot fix from the deployer's side.

**The harness is a control, and it is procured, not configured.** GhostSplice ran at 90% under one client and 0% under another on identical weights. Ghostcommit found the same thing in July. Which coding agent your engineers run is, right now, a larger determinant of exposure than which model it calls, and no part of the framework currently treats agent-client selection as a control decision with an assessment behind it. It should.

## The Design Principle

Put the gate where the action is, not where the language is.

A model turn is a useful place to look for intent. It is a terrible place to enforce authority, because it is one component among many and it is increasingly not the one an attacker bothers with. The controls that survived August are the ones that would have worked against a hostile human, a broken script, or a piece of malware, because they never assumed the thing on the other side was reasoning at all.

Assume the model is optional. Build the boundary anyway.

## Where This Connects

| If you want | Read |
|---|---|
| Why enforcement belongs outside the agent | [Infrastructure Beats Instructions](infrastructure-beats-instructions.md) |
| Why bounding capability beats evaluating intent | [Why Containment Beats Evaluation](why-containment-beats-evaluation.md) |
| The limits of pattern-matching controls | [Why Guardrails Aren't Enough](why-guardrails-arent-enough.md) |
| The protocol that multiplexes these channels | [The MCP Problem](the-mcp-problem.md) |
| Tool runtimes as a containment problem | [The Sandbox Escape Problem](the-sandbox-escape-problem.md) |
| The action-authorising controls in full | [Execution Control](../maso/controls/execution-control.md) |
| Agent identity as the real blast radius | [Identity and Access](../maso/controls/identity-and-access.md) |
| The events themselves, as they broke | [AI Runtime Security News](../news.md) |

!!! info "References"
    - [The Hacker News: AWS, Google, and Vercel agent flaws let attackers trigger tools without running the model](https://thehackernews.com/2026/08/aws-google-and-vercel-patch-agent-flaws.html)
    - [TechTimes: AWS fixed its managed agent service but left Strands Python SDK unpatched](https://www.techtimes.com/articles/323397/20260806/aws-fixed-its-managed-agent-service-left-strands-python-sdk-unpatched.htm)
    - [Cloud Security Alliance: Google deletes ADK workflows after agent-to-agent injection](https://labs.cloudsecurityalliance.org/research/csa-research-note-google-adk-trustissues-agent-injection-202/)
    - [Zero Day Initiative: The August 2026 security update review](https://www.zerodayinitiative.com/blog/2026/8/11/the-august-2026-security-update-review)
    - [Novee Security: Critical flaws in Anthropic, Google, and OpenAI's coding agents](https://novee.security/blog/critical-flaws-in-anthropic-google-and-openais-coding-agents/)
    - [ASSET Research Group: GhostSplice proof of concept](https://github.com/asset-group/ghostsplice)
