---
description: "What MASO and ASO are responsible for at runtime, which adjacent functions own the rest, a three-question boundary test, and a RACI for running AI agents in production."
---

# Scope and Responsibilities

MASO and ASO are runtime disciplines for **AI agents you operate**. They govern what an agent can reach, what it can do, what it loads, how its behaviour is watched, how it is stopped, and what evidence it leaves behind. They do not patch software, run the SOC, train models, or decide which use cases the business should pursue. Those jobs belong to other functions, and a runtime control programme that tries to absorb them ends up doing none of them well.

There is a second point that matters more for anyone building a team around this framework. **MASO mostly specifies and verifies. It rarely implements.** Identity teams issue the credentials, platform teams build the sandboxes and egress controls, and the SOC runs the SIEM that agent telemetry lands in. The framework says what has to be true at runtime; other teams make it true. That is why the RACI below assigns people and teams, not frameworks.

This page is the third axis of responsibility on the site:

| Axis | Question it answers | Page |
|------|---------------------|------|
| **Vendor** | When you buy AI rather than build it, who owns each control? | [Shared Responsibility](shared-responsibility.md) |
| **Time** | Which pre-runtime infrastructure does each runtime behaviour depend on? | [Control Handoff Matrix](../infrastructure/handoff-matrix.md) |
| **Function** | Inside your organisation, what is MASO's job and what belongs to other functions? | This page |

## What MASO and ASO are responsible for

Six responsibilities cover everything the framework's controls do. ASO applies them to a single AI system; MASO applies the same six to a fleet, where delegation, inter-agent messages, and privileged orchestrator and observer agents add new ways for each one to fail.

| Responsibility | What it means at runtime | Control domains |
|----------------|--------------------------|-----------------|
| **Reach** | What each agent's identity and network paths can touch | [Identity & Access](../maso/controls/identity-and-access.md), EC-2.18 in [Execution Control](../maso/controls/execution-control.md) |
| **Action** | What an agent may do, which actions escalate to a human, and the ceiling on damage | [Execution Control](../maso/controls/execution-control.md), [Agentic Task Mandate](../maso/controls/agentic-task-mandate.md) |
| **Composition** | Which models, tools, MCP servers, and skills an agent loads, and whether they are the ones approved | [Supply Chain](../maso/controls/supply-chain.md) |
| **Detection** | Noticing when behaviour departs from the mandate: guardrails, the Judge, anomaly scoring, and an independent observer | [Observability](../maso/controls/observability.md), [Prompt, Goal & Epistemic Integrity](../maso/controls/prompt-goal-and-epistemic-integrity.md), [Model Cognition Assurance](../maso/controls/model-cognition-assurance.md) |
| **Stopping** | Circuit breakers, kill switches, and PACE fallbacks that hold when the other layers fail | [PACE Resilience](../pace-resilience.md), [Privileged Agent Governance](../maso/controls/privileged-agent-governance.md) |
| **Evidence** | What happened, in what order, and which named human was accountable | [Observability](../maso/controls/observability.md), [Data Protection](../maso/controls/data-protection.md) |

## The boundary test

!!! tip "Is it MASO's job?"
    Ask three questions about the failure or the control:

    1. Is it an agent **you operate**, rather than an attacker's agent or a vendor's internal one?
    2. Is the failure in the agent's **behaviour or authority**, rather than in the code or infrastructure underneath it?
    3. Does the control act **while the agent is running**, rather than before deployment or after an incident is closed?

    Three yeses: it is MASO's job. Any no: another function owns it, and MASO's job is to name that function and state what it needs from them.

The test is deliberately strict. Plenty of failures pass two questions and fail the third. A zero-day in an AI annotation server passes the first and fails the second: you operate it, but the failure is in the code, so it belongs to vulnerability management, with MASO contributing the inventory that tells them it exists. The [news page](../news.md) applies this test to every incident, and each verdict's **Not covered** line points to the function below that owns the gap.

## Where responsibility sits elsewhere

Each function below owns something MASO depends on or touches. For each one: what they own, what MASO gives them, what MASO needs from them, and news entries where the boundary showed.

### Vulnerability management and application security { #vulnerability-management }

- **Owns**: Finding, prioritising, and patching vulnerabilities in AI frameworks, gateways, MCP servers, model-serving tools, and the code your teams write around them.
- **MASO gives them**: The inventory that turns an advisory into a list of affected agents: [SC-1.2](../maso/controls/supply-chain.md), [SC-2.1](../maso/controls/supply-chain.md), and continuous dependency scanning ([SC-3.3](../maso/controls/supply-chain.md)).
- **MASO needs from them**: Patch timelines that reflect agent-speed exploitation, and notice when an AI component cannot be patched, so blast-radius limits can tighten in the meantime.
- **Seen in the news**: [Cairn agents exploit a MONAI Label zero-day](../news.md#2026-11-20-amazon-watches-cairn-agents-find-a-zero-day-in-a-medical-imaging-tool-and-take-root-in-eleven-minutes) &middot; [MCP git server runs code from the repository](../news.md#2026-11-18-the-official-mcp-git-server-runs-code-from-the-repository-it-was-asked-to-read) &middot; [GitLab AI gateway template injection](../news.md#2026-10-02-gitlabs-self-hosted-ai-gateway-ships-a-cvss-99-and-it-is-template-injection)

### Vendors and product security { #vendors }

- **Owns**: The code and internal controls of products you buy: SaaS agents, hosted MCP servers, model APIs, SDKs, and agent platforms.
- **MASO gives them**: A specific list of runtime requirements to meet and evidence, through [Shared Responsibility](shared-responsibility.md) and the [vendor assessment questionnaire](../extensions/templates/vendor-assessment-questionnaire.md).
- **MASO needs from them**: Evidence the controls exist, disclosure of agentic capability ([AT-2.14](../maso/controls/agentic-task-mandate.md)), and notice of fixes, including silent ones with no CVE.
- **Seen in the news**: [SalesBleed in Salesforce Agentforce](../news.md#2026-09-24-salesbleed-turns-a-public-web-to-lead-form-into-zero-click-crm-exfiltration) &middot; [Mittwald's MCP server](../news.md#2026-11-07-a-german-web-hosts-mcp-server-handed-an-intruder-56-customers-session-tokens) &middot; [MCP SDK OAuth issuer confusion](../news.md#2026-10-23-the-mcp-server-picks-the-authorization-server-and-two-official-sdks-and-opencode-trusted-the-choice)

### Enterprise identity and platform security { #enterprise-identity }

- **Owns**: The identity platform itself, human accounts, credential hygiene across the estate, exposed endpoints, and rate limiting on internal applications.
- **MASO gives them**: Requirements for agent identities specifically: one identity per agent, scoped, short-lived, never in context, and revocable in seconds ([Identity & Access](../maso/controls/identity-and-access.md)).
- **MASO needs from them**: A platform that can issue and revoke non-human identities at that rate, and the hygiene that keeps an escaped or hostile agent from walking in through a guessable credential.
- **Seen in the news**: [WorkOS, the target of an escaped agent](../news.md#2026-11-06-the-workos-breach-was-a-researchers-benchmark-agent-that-got-out) &middot; [AgentCorruption's default execution role](../news.md#2026-10-08-agentcorruption-where-one-prompt-gets-an-agentcore-agents-role-and-aws-calls-it-documented-behaviour)

### Security operations and endpoint security { #security-operations }

- **Owns**: Detection and response across the whole estate, including attacks by agents you do not run, and the endpoints where developers run coding agents.
- **MASO gives them**: Agent telemetry and decision chains forwarded to the SIEM ([OB-2.4](../maso/controls/observability.md)), automated credential revocation they can trigger ([IA-3.4](../maso/controls/identity-and-access.md)), and runbooks for agent incidents.
- **MASO needs from them**: Correlation of agent activity with endpoint and network signals, response at machine speed, and coverage of coding agents on developer machines, which often sit outside any AI programme.
- **Seen in the news**: [CrowdStrike's four crews running intrusions through agents](../news.md#2026-10-24-crowdstrike-names-four-crews-running-intrusions-through-ai-agents-one-reaching-a-domain-controller-in-twenty-minutes) &middot; [Google's exploit_agent report](../news.md#2026-11-16-google-finds-an-attackers-exploit_agent-turning-patches-into-exploits-without-a-human) &middot; [PixelLeak](../news.md#2026-09-29-pixelleak-where-coding-agents-solved-a-tool-limitation-by-publishing-13000-screenshots)

### Model providers { #model-providers }

- **Owns**: The model: training, alignment, refusals, misuse detection on their own platform, and documented limitations.
- **MASO gives them**: Nothing, deliberately. MASO assumes the model can be manipulated or misaligned and builds controls that hold anyway.
- **MASO needs from them**: Capability disclosure, notice of material alignment findings ([MC-2.9, MC-2.10](../maso/controls/model-cognition-assurance.md)), and stable, pinnable versions ([SC-3.1](../maso/controls/supply-chain.md)).
- **Seen in the news**: [Provider refusals bypassed with a pentest framing](../news.md#2026-10-24-crowdstrike-names-four-crews-running-intrusions-through-ai-agents-one-reaching-a-domain-controller-in-twenty-minutes) &middot; [Three labs gate cyber-capable models](../news.md#2026-09-02-three-labs-ship-cyber-capable-models-on-the-same-day-each-behind-a-different-access-gate)

### Platform engineering { #platform-engineering }

- **Owns**: Building the infrastructure that makes enforcement possible: sandboxes, network zones, egress proxies, secret vaults, gateways, and logging pipelines.
- **MASO gives them**: The runtime requirement each piece has to meet, mapped in the [Control Handoff Matrix](../infrastructure/handoff-matrix.md) and the [infrastructure controls](../infrastructure/README.md).
- **MASO needs from them**: Enforcement below the agent's reach ([EC-3.1](../maso/controls/execution-control.md)), and egress that is tested rather than assumed ([EC-2.18](../maso/controls/execution-control.md)).
- **Seen in the news**: [OpenAI agent escapes through DNS](../news.md#2026-09-25-an-openai-agent-escapes-through-an-unrestricted-dns-resolver-and-training-pauses-again) &middot; [Nvidia's hardware kill switch](../news.md#2026-09-28-nvidia-ships-an-agent-kill-switch-in-silicon-with-100-partners-and-no-openai)

### Data governance { #data-governance }

- **Owns**: The classification scheme, data ownership, retention rules, and decisions about which data AI may use at all.
- **MASO gives them**: Enforcement of their classifications at the agent boundary, including on images and other non-text outputs ([Data Protection](../maso/controls/data-protection.md)).
- **MASO needs from them**: Classifications that exist and are current. An agent cannot respect a label nobody applied.
- **Seen in the news**: [PixelLeak's unclassified screenshots](../news.md#2026-09-29-pixelleak-where-coding-agents-solved-a-tool-limitation-by-publishing-13000-screenshots)

### Risk, compliance, and legal { #risk-and-compliance }

- **Owns**: Use-case approval, risk tiering policy, formal acceptance of residual risk, and reporting to regulators.
- **MASO gives them**: The evidence: decision chains, incident timelines, control test results, and a named accountable human for every workflow ([OB-2.7](../maso/controls/observability.md)).
- **MASO needs from them**: A risk tier for each use case before agents are built, and a decision on what counts as a reportable incident before one happens.
- **Seen in the news**: [The first EU AI Act serious-incident report](../news.md#2026-09-08-the-first-eu-ai-act-serious-incident-report-is-filed-for-something-outsiders-found-first) &middot; [NSA, CISA, and NIST incident guidance](../news.md#2026-10-16-nsa-cisa-and-nist-publish-incident-guidance-for-agents-that-act-without-instruction)

### Internal audit { #internal-audit }

- **Owns**: Independent assurance that the controls exist and work as described.
- **MASO gives them**: Testable control statements, testing criteria per tier, and the evidence MASO requires the first line to keep.
- **MASO needs from them**: Testing against the agent as deployed, not as documented, because an agent's actual reach is the thing most likely to differ.

## RACI for runtime activities

The matrix covers the activities that make up running agents in production. It assumes an organisation that builds or operates its own agents; for consumed AI, read it alongside [Shared Responsibility](shared-responsibility.md), where the vendor takes the implementation work and the AI security function moves to verifying it.

### Roles

| Role | Who it usually is |
|------|-------------------|
| **Agent owner** | The named, accountable human for a workflow ([OB-2.7](../maso/controls/observability.md)), usually the business or product owner. Accountable for the agent's outcomes and its residual risk. |
| **AI security** | The function that owns the MASO control set: sets requirements per risk tier, verifies they hold, and runs adversarial testing. |
| **AI platform** | The engineering team that builds and runs the agent runtime, orchestrators, gateways, sandboxes, and Judge infrastructure. |
| **IAM** | The enterprise identity team. |
| **SOC** | Security operations, including incident response. |
| **Vuln mgmt** | Vulnerability management and application security. |
| **Risk** | Second-line risk, compliance, and legal. |
| **Vendor** | Suppliers of models, tools, MCP servers, and agent platforms. |

Internal audit is not in the matrix because it is independent of all of it: audit reviews every row and is accountable for none.

### Matrix

**R** responsible (does the work), **A** accountable (one per row, signs off), **C** consulted, **I** informed.

<div class="raci-matrix" markdown>

| Activity | Agent owner | AI security | AI platform | IAM | SOC | Vuln mgmt | Risk | Vendor |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Declare and approve the agent's mandate ([AT-1.1](../maso/controls/agentic-task-mandate.md)) | **A**, R | C | C | | | | C | |
| Assign the risk tier ([Risk Tiers](risk-tiers.md)) | R | C | | | | | **A** | |
| Accept residual risk ([AT-2.15](../maso/controls/agentic-task-mandate.md)) | **A**, R | C | | | | | C | |
| Specify the MASO controls for the tier | C | **A**, R | C | | | | C | |
| Issue and scope agent identities ([Identity & Access](../maso/controls/identity-and-access.md)) | C | **A** | C | R | | | | |
| Build sandboxes, egress limits, and blast-radius caps ([EC-2.2, EC-2.18, EC-3.1](../maso/controls/execution-control.md)) | I | **A** | R | | | | | |
| Inventory and verify models, tools, MCP servers, and skills ([Supply Chain](../maso/controls/supply-chain.md)) | C | **A** | R | | | C | | C |
| Patch AI frameworks and tools | I | C | R | | | **A** | | R |
| Operate guardrails and the Judge ([Judge Assurance](judge-assurance.md)) | C | **A** | R | | | | | |
| Approve escalated agent actions ([EC-2.1](../maso/controls/execution-control.md)) | **A**, R | I | | | | | | |
| Monitor agent behaviour and alert ([Observability](../maso/controls/observability.md)) | I | **A** | R | | C | | | |
| Trip a circuit breaker or kill switch ([EC-2.4](../maso/controls/execution-control.md), [PA-2.6](../maso/controls/privileged-agent-governance.md)) | I | **A** | R | | R | | | |
| Investigate and respond to an agent incident ([Incident Playbook](../extensions/templates/ai-incident-playbook.md)) | C | **A** | C | C | R | | I | C |
| Report an incident to regulators | C | C | | | | | **A**, R | |
| Test that controls work, including red teaming ([Red Team Playbook](../maso/red-team/red-team-playbook.md)) | I | **A**, R | C | | C | | I | |
| Verify vendor controls ([Shared Responsibility](shared-responsibility.md)) | C | **A** | | | | | C | R |

</div>

Three patterns in the matrix are worth stating directly:

- **The agent owner holds the business accountability; AI security holds the control accountability.** The owner decides what the agent is for and accepts what is left over. AI security decides what has to be true for that to be safe, and checks it is. Neither can sign off the other's row.
- **AI security is accountable for far more rows than it is responsible for.** That is the "specifies and verifies" point in practice. If an AI security team finds itself building sandboxes and issuing credentials, it has absorbed platform and IAM work, and the independence of its verification goes with it.
- **Stopping an agent does not wait for its owner.** AI security is accountable for the decision, and both the platform and the SOC can trigger it. An owner who must be consulted before a breaker trips is a breaker that trips late, which is the [OpenAI DNS escape](../news.md#2026-09-25-an-openai-agent-escapes-through-an-unrestricted-dns-resolver-and-training-pauses-again) in one line.

## Fitting this to your organisation

Most organisations place the AI security function either in the first line, inside a security engineering group, or as a specialist second-line function under the [AI governance operating model](../extensions/regulatory/ai-governance-operating-model.md). The matrix holds either way, as long as the function that verifies the controls is not the one that built them.

Privileged agents need owners too. Orchestrators, evaluators, and observers are agents with authority over other agents, and each belongs on the [privileged agent inventory](../maso/controls/privileged-agent-governance.md) with its own agent owner. A fleet where the orchestrator is owned by "the platform" is a fleet with no accountable human at the top of the delegation chain, which is the accountability blur recorded as HF-02 in the [Emergent Risk Register](../maso/controls/risk-register.md).

!!! info "References"
    - [Shared Responsibility for AI Systems](shared-responsibility.md)
    - [Control Handoff Matrix](../infrastructure/handoff-matrix.md)
    - [AI Governance Operating Model](../extensions/regulatory/ai-governance-operating-model.md)
    - [Use Case Definition: the RACI model](../strategy/use-case-definition.md)
    - [CSA AI Controls Matrix v1.1](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix-v1-1)
    - [The Institute of Internal Auditors: The Three Lines Model](https://www.theiia.org/en/content/position-papers/2020/the-iias-three-lines-model-an-update-of-the-three-lines-of-defense/)
