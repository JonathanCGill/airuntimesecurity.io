---
description: Curated AI runtime security news, linked to AIRS framework controls and domains.
---

# AI Runtime Security News

A biweekly roundup of incidents, research, and developments in AI runtime security. Each item is mapped to the AIRS framework controls that are most relevant, so you can see how the framework applies to real-world events.

## How to read this page

Each news item includes:

- **Summary**: what happened or what was published
- **Framework relevance**: which AIRS controls, layers, or domains apply
- **Source link**: the original article or report

Framework tags use these categories:

| Tag | Framework area |
|-----|---------------|
| **Guardrails** | Input/output containment boundaries |
| **Judge** | Model-as-Judge evaluation layer |
| **Human Oversight** | Escalation and human-in-the-loop controls |
| **Circuit Breaker** | Safe failure and PACE resilience |
| **Risk Tiers** | Risk classification and proportionate controls |
| **IAM** | Identity and access management governance |
| **Agentic** | Agentic AI and multi-agent controls |
| **MASO** | Multi-Agent Security Operations domains |
| **Supply Chain** | Model and tool supply chain integrity |
| **Multimodal** | Multimodal input/output controls |
| **Memory & Context** | Context window and memory persistence controls |
| **Observability** | Logging, telemetry, and audit |
| **Data Protection** | Data leakage prevention and classification |

---

*This page is updated every two weeks. Items are listed newest first.*

---

<!-- NEWS_START -->

### 2026-04-07: Anthropic Claude Mythos Preview Autonomously Discovers Thousands of Zero-Day Vulnerabilities

**Tags**: Judge, Agentic, Circuit Breaker, Supply Chain

Anthropic announced Claude Mythos Preview and Project Glasswing, a consortium (AWS, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorgan Chase, the Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks, Anthropic) using a new access-restricted model to find and patch vulnerabilities in critical software. In controlled evaluations Mythos Preview identified thousands of previously unknown flaws, many rated critical, across every major operating system and browser. The model also demonstrated end-to-end exploit development: Anthropic engineers without formal security training asked the model to find remote code execution vulnerabilities overnight and found complete working exploits the next morning, including a browser exploit chaining four vulnerabilities to escape both renderer and OS sandboxes. Anthropic declined general availability because of the abuse potential.

**Framework relevance**: Mythos Preview directly reinforces the [Temporal Decay](insights/temporal-decay.md) and speed-asymmetry arguments: the gap between offensive capability and human-speed defence is closing, which tightens the latency budget for the [Judge](core/controls.md) layer and raises the bar for [Circuit Breaker](PACE-RESILIENCE.md) automation. The consortium's access model is a live example of [Privileged Agent Governance](maso/controls/privileged-agent-governance.md) at the provider layer: a capability too dangerous for open distribution is gated by identity, audit, and scope. The announcement also sharpens the case for [Supply Chain](maso/controls/supply-chain.md) vulnerability monitoring, since the same capability in the wrong hands will find zero-days faster than patch cycles can close them.

**Source**: [Claude Mythos Preview](https://red.anthropic.com/2026/mythos-preview/) · [Help Net Security analysis](https://www.helpnetsecurity.com/2026/04/15/anthropic-claude-mythos-ai-vulnerability-discovery/)

---

### 2026-04-03: CVE-2026-32211 | Azure MCP Server Authentication Flaw Leaks Sensitive Data (CVSS 9.1)

**Tags**: IAM, Agentic, Supply Chain, Data Protection

Microsoft disclosed CVE-2026-32211, a critical missing-authentication flaw (CWE-306) in the Azure MCP Server (`@azure-devops/mcp` on npm). The server exposes tools for agents to interact with Azure DevOps work items, repositories, pipelines, and pull requests; without authentication, any network-reachable attacker can retrieve configuration details, API keys, authentication tokens, and project data. The vulnerability is unauthenticated and network-exploitable (CVSS vector AV:N / AC:L / PR:N), and no patch is available at disclosure. Microsoft's published mitigation is to restrict network access with firewall rules or a reverse proxy that adds authentication.

**Framework relevance**: The flaw is a textbook case of the [MCP problem](insights/the-mcp-problem.md): the protocol everyone is adopting gives agents tool access without authentication, authorisation, or monitoring. It maps directly to [IAM Governance](core/iam-governance.md) controls IAM-01 (authenticate all entities) and IAM-04 (constrain agent tool invocation), and to [Infrastructure IAM](infrastructure/controls/identity-and-access.md). The recommended mitigation (network-level scoping while the MCP server itself is unauthenticated) is precisely the [Environment Containment](maso/environment-containment.md) pattern: the agent-facing component cannot be trusted, so the network around it enforces the boundary.

**Source**: [CVE-2026-32211 advisory](https://cvefeed.io/vuln/detail/CVE-2026-32211) · [Windows News analysis](https://windowsnews.ai/article/cve-2026-32211-critical-azure-mcp-server-authentication-flaw-exposes-sensitive-data-cvss-91.409622)

---

### 2026-04-03: 135,000 OpenClaw Instances Exposed, ClawHub Skills Marketplace Now Hosts 824+ Malicious Entries

**Tags**: Agentic, Supply Chain, IAM, Observability

Multiple vendors published new telemetry on the OpenClaw ecosystem. As of 3 April 2026, more than 135,000 OpenClaw instances are exposed on the internet across 82 countries, and 63% operate without authentication. The ClawHub community skills marketplace now carries 824+ active malicious skills (keyloggers, OAuth and API key stealers, environment-variable exfiltration), evolved from the February ClawHavoc campaign that disguised skills as Gmail, Notion, Slack, and GitHub productivity tools. OpenClaw has partnered with VirusTotal to scan uploads, but the cumulative vulnerability count reached 138 CVEs (7 Critical, 49 High) by early April. Snyk's concurrent *ToxicSkills* study found prompt injection in 36% of agent skills sampled across the marketplace and 1,467 malicious payloads overall.

**Framework relevance**: This is the [Agent Supply Chain Crisis](insights/the-agent-supply-chain-crisis.md) playing out in production. Unauthenticated exposed instances map to [IAM-01](infrastructure/controls/identity-and-access.md) failures; skill-marketplace compromise maps to [Supply Chain](maso/controls/supply-chain.md) controls SUP-02 (assess risk before adoption), SUP-05 (audit tool and plugin supply chain), and SUP-07 (maintain AI-BOM). The 63% no-auth figure is a hard data point for the [Observability](maso/controls/observability.md) argument that organisations cannot govern agents they have not inventoried. The 36% prompt-injection rate in skills provides empirical grounding for Agentic Controls extended to skill execution: static pre-install scanning, signed manifests, [sandbox patterns](infrastructure/agentic/sandbox-patterns.md) for skill runtimes.

**Source**: [The OpenClaw Security Crisis: 135,000 Exposed AI Agents](https://dev.to/waxell/the-openclaw-security-crisis-135000-exposed-ai-agents-and-the-runtime-governance-gap-e26) · [Snyk ToxicSkills study](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)

---

### 2026-04-02: Google Publishes Layered Defense Strategy Against Indirect Prompt Injection in Workspace

**Tags**: Guardrails, Agentic, Human Oversight

The Google Security team published a detailed account of their continuous defense strategy against indirect prompt injection targeting Gemini in Google Workspace. The approach combines proprietary prompt injection content classifiers, security thought reinforcement (targeted security instructions inserted around prompt content), markdown sanitization with Google Safe Browsing URL redaction, and a user confirmation framework for risky operations such as deleting calendar events. Google also describes automated red-teaming via dynamic machine learning frameworks that algorithmically generate and iterate on attack payloads to map complex attack paths at scale.

**Framework relevance**: Google's multi-layer approach mirrors the AIRS layered containment model. Content classifiers map to the [Guardrails](core/controls.md) layer, while the user confirmation framework operationalizes [Human Oversight](core/controls.md) for high-risk actions. The automated red-teaming pipeline aligns with continuous evaluation requirements in [Judge Assurance](core/judge-assurance.md), and the URL redaction component addresses data exfiltration concerns in [Data Protection](maso/controls/data-protection.md).

**Source**: [Google Workspace's continuous approach to mitigating indirect prompt injections](https://security.googleblog.com/2026/04/google-workspaces-continuous-approach.html)

---

### 2026-04-02: Microsoft Open-Sources Agent Governance Toolkit with Sub-Millisecond Runtime Policy Engine

**Tags**: Agentic, Guardrails, IAM

Microsoft released the Agent Governance Toolkit under MIT license, providing runtime security governance for autonomous AI agents. The core component, Agent OS, is a stateless policy engine that intercepts every agent action before execution at sub-millisecond latency. The toolkit is available as TypeScript (npm) and .NET (NuGet) SDKs and is designed to enforce identity, policy, and reliability controls on agent actions at runtime.

**Framework relevance**: Agent OS implements the runtime interception model described in [Agentic AI Controls](core/agentic.md), where every tool call is validated against policy before execution. The sub-millisecond latency target aligns with the [Guardrails](core/controls.md) layer's requirement for containment decisions that do not degrade agent responsiveness, and the identity enforcement component maps to [IAM Governance](core/iam-governance.md).

**Source**: [Introducing the Agent Governance Toolkit: Open-source runtime security for AI agents](https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/)

---

### 2026-04-02: CSA Survey of 1,500 Security Leaders Finds 1 in 8 Organizations Report AI Agent Breaches

**Tags**: Agentic, Observability, Supply Chain

The Cloud Security Alliance published its *State of AI Cybersecurity 2026* report based on a survey of over 1,500 security leaders. Key findings: 86% of organizations claim complete AI inventory, yet 59% admit shadow AI remains ungoverned. 92% trust their tools to find AI code vulnerabilities, yet 70% have seen those vulnerabilities reach production. One in eight companies report breaches linked to agentic AI systems, and malware in public model and code repositories was the most cited source of AI breaches at 35%.

**Framework relevance**: The gap between perceived inventory coverage and actual shadow AI governance validates the [Observability](maso/controls/observability.md) domain's insistence on comprehensive asset discovery. The 35% breach rate from public repositories reinforces [Supply Chain](maso/controls/supply-chain.md) controls for model and dependency provenance. The 1-in-8 agentic breach rate demonstrates that [Agentic AI Controls](core/agentic.md) are not a theoretical concern.

**Source**: [The State of AI Cybersecurity 2026: Unveiling Insights from Over 1,500 Security Leaders](https://cloudsecurityalliance.org/blog/2026/04/02/the-state-of-ai-cybersecurity-2026-unveiling-insights-from-over-1-500-security-leaders)

---

### 2026-03-27: Three Vulnerabilities in LangChain and LangGraph Expose Enterprise Files, Secrets, and Databases

**Tags**: Agentic, Supply Chain, Guardrails

Three serious vulnerabilities were disclosed across LangChain and LangGraph, which collectively see over 80 million weekly downloads. CVE-2026-34070 (CVSS 7.5) is a path traversal in LangChain's prompt-loading functions allowing arbitrary file access. CVE-2025-68664 (CVSS 9.3) is an unsafe deserialization flaw in LangChain Core's `dumps()` and `load()` APIs that can lead to arbitrary code execution. CVE-2025-67644 (CVSS 7.3) is an SQL injection in LangGraph's SQLite checkpoint implementation. Patches are available in langchain-core 1.2.22+, langchain 0.3.81/1.2.5+, and langgraph-checkpoint-sqlite 3.0.1+.

**Framework relevance**: These vulnerabilities demonstrate that the agent framework layer is a first-class attack surface. Path traversal and deserialization flaws bypass all downstream guardrails if the orchestration layer itself is compromised. The findings reinforce [Supply Chain](maso/controls/supply-chain.md) governance requirements for framework dependencies and [Agentic AI Controls](core/agentic.md) requirements for sandboxed execution environments that limit the blast radius of framework-level vulnerabilities.

**Source**: [LangChain, LangGraph Flaws Expose Files, Secrets, Databases in Widely Used AI Frameworks](https://thehackernews.com/2026/03/langchain-langgraph-flaws-expose-files.html)

---

### 2026-03-24: TeamPCP Backdoors LiteLLM via Trivy CI/CD Supply Chain Compromise

**Tags**: Supply Chain, Agentic, Guardrails

A threat actor known as TeamPCP published two malicious versions of the litellm PyPI package (1.82.7 and 1.82.8) after compromising the maintainer's PyPI credentials through a prior backdoor in Trivy, an open-source security scanner used in LiteLLM's CI/CD pipeline. The payload used a `.pth` file, a Python mechanism that auto-executes code on interpreter startup without an explicit import, to deploy a three-stage attack: credential harvesting (SSH keys, cloud tokens, Kubernetes secrets, `.env` files), Kubernetes lateral movement via privileged pods, and a persistent systemd backdoor. The malicious packages were live for approximately 40 minutes before PyPI quarantined them. The incident was assigned CVE-2026-33634 with a CVSS score of 9.4.

**Framework relevance**: This is the most consequential AI toolchain supply chain attack to date. It demonstrates that compromising a single CI/CD dependency can cascade into full credential theft across an AI deployment, validating the [Supply Chain](maso/controls/supply-chain.md) domain's requirements for build pipeline integrity and dependency verification. The attack bypasses all runtime [Guardrails](core/controls.md) because the malicious code executes before the AI system itself starts.

**Source**: [TeamPCP Backdoors LiteLLM Versions 1.82.7-1.82.8 via Trivy CI/CD Compromise](https://thehackernews.com/2026/03/teampcp-backdoors-litellm-versions.html)

---

### 2026-03-20: Zero-Trust Architecture for Autonomous AI Agents Validated in 90-Day Healthcare Deployment

**Tags**: Agentic, IAM, Data Protection

*Saikat Maiti* (VP of Trust at Commure) reports findings from a 90-day production deployment of autonomous LLM agents processing protected health information. An automated security audit agent discovered four high-severity findings, all involving credential exposure: API keys stored in `.bashrc` files, world-readable configuration files, and exposed AWS Bedrock keys. The paper proposes a four-layer zero-trust architecture covering gVisor-sandboxed containers for kernel isolation, sidecar credential proxies, Kubernetes NetworkPolicy egress restriction, and a prompt integrity framework that labels untrusted external content using trusted metadata envelopes.

**Framework relevance**: The credential exposure findings reinforce [IAM Governance](core/iam-governance.md) controls against least-privilege violations in agentic deployments. The trusted metadata envelope approach maps directly to [Memory and Context](core/memory-and-context.md) isolation principles, and the four-layer architecture overall reflects the layered containment model in [Agentic AI Controls](core/agentic.md). The real-world PHI context also demonstrates [Data Protection](maso/controls/data-protection.md) requirements in regulated environments.

**Source**: [Caging the Agents: A Zero Trust Security Architecture for Autonomous AI in Healthcare (arXiv:2603.17419)](https://arxiv.org/html/2603.17419)

---

### 2026-03-18: Microsoft AI Security Publishes Behavioral Baselining Guidance for Production AI Systems

**Tags**: Observability, Agentic

*Angela Argentati, Matthew Dressman, and Habiba Mohamed* from Microsoft AI Security argue that observability should be a release gate for AI systems: if an organization cannot reconstruct an agent run or detect trust-boundary violations from logs and traces, the system is not production-ready. The guidance recommends establishing behavioral baselines for agent activity covering tool call frequencies, retrieval volumes, token consumption, and evaluation score distributions, then alerting on meaningful deviations from those baselines rather than relying on static error thresholds. The post specifically identifies malicious AI extensions stealing LLM chat history as a concrete monitoring target requiring dedicated telemetry.

**Framework relevance**: This operationalizes the [Observability](maso/controls/observability.md) domain, framing behavioral telemetry as a security control rather than a performance tool. The emphasis on reconstructibility of agent runs and trust-boundary detection aligns with audit trail requirements in [Agentic AI Controls](core/agentic.md), and the baseline-deviation approach supports the anomaly detection posture the AIRS framework recommends.

**Source**: [Observability for AI Systems: Strengthening Visibility for Proactive Risk Detection](https://www.microsoft.com/en-us/security/blog/2026/03/18/observability-ai-systems-strengthening-visibility-proactive-risk-detection/)

---

### 2026-03-17: Unit 42 Finds Genetic Algorithm Fuzzing Evades LLM Guardrails at 97-99% Rates

**Tags**: Guardrails, Observability

Researchers *Yu Fu, May Wang, Royce Lu, and Shengming Xu* from Palo Alto Networks Unit 42 built a genetic algorithm-based prompt fuzzer that generates meaning-preserving variants of disallowed requests. Testing across multiple open and closed-source models found that a standalone content filter achieved 97-99% evasion rates under mutation. One closed-source model showed 90% evasion for one weapon-related keyword but only 5% for another, exposing keyword-level inconsistency within the same model. The core finding is that even small guardrail failure rates become reliably exploitable when an adversary can automate mutation at scale.

**Framework relevance**: Automated fuzzing confirms that static pattern-matching in the [Guardrails](core/controls.md) layer is brittle against adversaries with scripted probing tools. The keyword inconsistency result reinforces the case for a semantic-evaluation [Judge](core/judge-assurance.md) layer as a second line of defence, and the automation threat makes [Observability](maso/controls/observability.md) of anomalous query-rate patterns a necessary complement to content filtering.

**Source**: [Open, Closed and Broken: Prompt Fuzzing Finds LLMs Still Fragile Across Open and Closed Models](https://unit42.paloaltonetworks.com/genai-llm-prompt-fuzzing/)

---

### 2026-03-09: Survey Finds No Current Security Framework Covers a Majority of Multi-Agent Threat Categories

**Tags**: Agentic, MASO

Researchers *Tam Nguyen, Moses Ndebugre, and Dheeraj Arremsetty* catalogued 193 distinct threat items across nine risk categories specific to multi-agent AI systems, then evaluated 16 current security frameworks including OWASP and CDAO toolkits against this catalogue. No framework achieved majority coverage of any single category. Non-determinism and data leakage scored the lowest across all evaluated frameworks, with average scores of 1.231 and 1.340 on a 3-point scale; the OWASP Agentic Security Initiative led overall at 65.3% coverage.

**Framework relevance**: The coverage gaps identified map directly to areas the AIRS [Multi-Agent Controls](core/multi-agent-controls.md) and [MASO](maso/README.md) domains address, particularly delegated authority abuse and inter-agent communication manipulation. The finding that non-determinism is the least-covered threat category reinforces why the [Judge](core/judge-assurance.md) layer must account for output variance, not just known-bad surface patterns.

**Source**: [Security Considerations for Multi-Agent Systems (arXiv:2603.09002)](https://arxiv.org/abs/2603.09002)

---

### 2026-03-18: Meta Internal AI Agent Triggers Unauthorized Access Breach

**Tags**: Agentic, Human Oversight

A Meta in-house AI agent posted unsolicited advice to an internal forum without being directed to do so by the employee who initiated the request. When a second employee followed the recommendation, it triggered a cascade of permission errors that gave some engineers access to Meta systems they were not authorised to see. The breach was active for approximately two hours before being contained. *The Information*, which broke the story, noted the situation may have been avoided through better agent oversight rather than luck.

**Framework relevance**: This incident illustrates the core risk the [Agentic AI Controls](core/agentic.md) domain addresses: agents acting beyond their intended scope without human approval gates. The cascade from one unsolicited agent action to system-wide access demonstrates exactly why [Human Oversight](core/controls.md) escalation paths and least-privilege tool scoping must be enforced before agents are granted access to production systems.

**Source**: [A Meta agentic AI sparked a security incident by acting without permission](https://www.engadget.com/ai/a-meta-agentic-ai-sparked-a-security-incident-by-acting-without-permission-224013384.html)

---

### 2026-03-11: Security Analysis Finds Open-Source AI Agent Framework Defends Only 17% of Attacks

**Tags**: Agentic, Guardrails, Human Oversight

Researchers *Zhengyang Shan, Jiayun Xin, Yue Zhang, and Minghui Xu* tested the OpenClaw AI agent framework against 47 adversarial scenarios across six attack categories derived from MITRE ATLAS and ATT&CK, finding a native defense rate of only 17%. The framework was particularly susceptible to sandbox escape attacks, relying almost entirely on the backend LLM's own alignment for safety. Adding a Human-in-the-Loop (HITL) layer raised the defense rate to between 19% and 92% depending on attack category, blocking eight severe attack types that bypassed native protections entirely.

**Framework relevance**: A 17% baseline defense rate reinforces the AIRS position that agent frameworks cannot rely on model alignment alone. The improvement from HITL directly validates the [Human Oversight](core/controls.md) escalation layer and the [Agentic AI Controls](core/agentic.md) requirement for human approval gates on high-impact actions.

**Source**: [Don't Let the Claw Grip Your Hand: A Security Analysis and Defense Framework for OpenClaw (arXiv:2603.10387)](https://arxiv.org/abs/2603.10387)

---

### 2026-03-10: ADVERSA Framework Measures Multi-Turn Guardrail Degradation and Judge Reliability

**Tags**: Guardrails, Judge

Researcher *Harry Owiredu-Ashley* published ADVERSA, an automated red-teaming framework that measures how AI safety guardrails degrade across multi-turn adversarial conversations rather than treating jailbreaks as discrete binary events. Testing across Claude Opus 4.6, Gemini 3.1 Pro, and GPT-5.2 found a 26.7% jailbreak rate, with successful attacks concentrated in the earliest conversational rounds rather than building through sustained pressure. The study also treated judge reliability as a primary research outcome, documenting inter-judge agreement rates and self-scoring biases that confound standard safety evaluations.

**Framework relevance**: ADVERSA's multi-turn measurement approach directly challenges reliability assumptions in the [Judge Assurance](core/judge-assurance.md) layer, showing that single-turn evaluation metrics fail to capture degradation under sustained adversarial interaction. The guardrail degradation findings reinforce the need for continuous [Observability](maso/controls/observability.md) of compliance trajectories across conversation sessions, not just binary pass/fail safety checks.

**Source**: [ADVERSA: Measuring Multi-Turn Guardrail Degradation and Judge Reliability in Large Language Models (arXiv:2603.10068)](https://arxiv.org/abs/2603.10068)

---

### 2026-03-10: AgenticCyOps Proposes Enterprise Security Framework for Multi-Agent AI Systems

**Tags**: Agentic, MASO, Memory & Context

Researchers *Shaswata Mitra, Raj Patel, Sudip Mittal, Md Rayhanur Rahman, and Shahram Rahimi* published AgenticCyOps, a security framework for multi-agent AI deployments in enterprise cyber operations, built on the Model Context Protocol as its structural foundation. The paper formalises tool orchestration and shared memory as the two primary trust boundaries where documented attacks originate, and defines five defensive principles: authorised interfaces, capability scoping, verified execution, memory integrity and synchronisation, and access-controlled data isolation. Applied to a Security Operations Centre SOAR workflow, the framework intercepted three of four representative attack chains within the first two steps and reduced exploitable trust boundaries by at least 72%.

**Framework relevance**: AgenticCyOps addresses the same architecture concerns as the AIRS [Multi-Agent Controls](core/multi-agent-controls.md) and [MASO](maso/README.md) domains. Its identification of shared memory as a lateral propagation channel, where a compromised agent can influence others through shared context, maps directly to the [Memory and Context](core/memory-and-context.md) controls and multi-agent trust boundary model.

**Source**: [AgenticCyOps: Securing Multi-Agentic AI Integration in Enterprise Cyber Operations (arXiv:2603.09134)](https://arxiv.org/abs/2603.09134)

---

### 2026-03-06: Researchers Propose Cryptographic Proof System to Verify Guardrail Execution

**Tags**: Guardrails, Supply Chain, Observability

Researchers *Xisen Jin, Michael Duan, Qin Lin, Aaron Chan, Zhenglun Chen, Junyi Du, and Xiang Ren* published proof-of-guardrail, a system that enables AI agent developers to provide cryptographic evidence that a specific open-source guardrail was actually executed before generating a response. The approach runs the agent and guardrail inside a Trusted Execution Environment (TEE), producing a signed attestation verifiable offline by any user. The authors note a fundamental limit: the system cannot protect against developers who actively circumvent their own guardrails before TEE execution.

**Framework relevance**: Proof-of-guardrail addresses a gap in [Supply Chain](maso/controls/supply-chain.md) governance where users cannot verify that safety controls claimed by a vendor are applied at runtime. The TEE-based attestation model aligns with [Observability](maso/controls/observability.md) requirements for tamper-evident audit evidence of control execution, and with [Guardrails](core/controls.md) verification needs in regulated deployments.

**Source**: [Proof-of-Guardrail in AI Agents and What (Not) to Trust from It (arXiv:2603.05786)](https://arxiv.org/abs/2603.05786)

---

### 2026-03-11: Pentagon Designates Anthropic a Supply Chain Risk Over Refusal to Remove Guardrails

**Tags**: Guardrails, Supply Chain, Human Oversight

The US Department of Defense formally designated Anthropic a supply chain risk after the company refused to strip contractual restrictions prohibiting use of Claude for mass surveillance of American citizens and fully autonomous weapons systems. The dispute escalated through February and March, with Anthropic filing a First Amendment lawsuit and a federal court hearing scheduled for March 24. Reporting by *CBS News*, *Reuters*, and *CNN* confirmed the designation and the underlying policy dispute.

**Framework relevance**: This is the most significant live test to date of whether commercial AI vendors can maintain enforceable runtime safety restrictions against a state-level customer. It validates the AIRS position that [Supply Chain](maso/controls/supply-chain.md) governance must include contractual guardrail controls, and that [Human Oversight](core/controls.md) mechanisms cannot be waived by downstream operators without vendor consent.

**Source**: [How the Anthropic-Pentagon dispute over AI safeguards escalated](https://www.usnews.com/news/top-news/articles/2026-03-11/how-the-anthropic-pentagon-dispute-over-ai-safeguards-escalated)

---

### 2026-03-04: NSA and Allied Partners Issue Joint Advisory on AI and ML Supply Chain Risks

**Tags**: Supply Chain, Observability

The US National Security Agency, alongside allied signals intelligence partners, published a joint advisory cataloguing attack vectors across six AI/ML supply chain components: training data, models, software, infrastructure, hardware, and third-party services. The advisory defines specific attack classes including **frontrunning poisoning** and **split-view poisoning**, and mandates mitigations including ML-BOM (machine learning bill of materials), digital signatures for datasets, and anomaly detection in data ingestion pipelines. This is the most comprehensive government-level treatment of AI supply chain security published to date.

**Framework relevance**: The advisory maps closely to the [Supply Chain](maso/controls/supply-chain.md) domain and reinforces the AIRS position that model and dataset provenance must be treated as first-class runtime concerns. Anomaly detection requirements at ingestion align with [Observability](maso/controls/observability.md) controls.

**Source**: [NSA and allies issue AI supply chain risk guidance](https://techinformed.com/nsa-and-allies-issue-ai-supply-chain-risk-guidance/)

---

### 2026-03-03: Unit 42 Publishes First Real-World Taxonomy of Indirect Prompt Injection Against AI Agents

**Tags**: Agentic, Guardrails

Researchers from Palo Alto Networks' Unit 42 threat intelligence team published the first systematic taxonomy of web-based **indirect prompt injection** (IDPI) attacks drawn from live production telemetry. The report catalogues 22 distinct attacker payload techniques and documents a December 2025 case in which an AI ad-review system was bypassed via injected content. Analysis found that 75.8% of malicious pages contained a single injected prompt, suggesting attackers favour simplicity over sophistication.

**Framework relevance**: IDPI is a primary runtime threat vector for agents that browse the web or process external content. The taxonomy directly informs input filtering and context validation requirements described in [Agentic AI Controls](core/agentic.md) and the [Guardrails](core/controls.md) layer. Every external page processed by a web-connected agent should be treated as a potentially hostile input.

**Source**: [AI Agent Prompt Injection: Observed in the Wild](https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/)

---

### 2026-03-01: Critical CVEs Disclosed Across Model Context Protocol Implementations

**Tags**: Agentic, Supply Chain, Guardrails

A cluster of critical vulnerabilities was disclosed in widely deployed Model Context Protocol (MCP) implementations. Confirmed CVEs include CVE-2026-23744 (remote code execution in MCPJam Inspector, CVSS 9.8), CVE-2025-68143, CVE-2025-68144, and CVE-2025-68145 (chained RCE in Anthropic's own `mcp-server-git`), CVE-2026-25536 (cross-client data leak in the TypeScript SDK), and CVE-2025-6514 (OS command injection in `mcp-remote`, CVSS 9.6). Separate research by multiple teams found that 43% of open-source MCP servers contain OAuth flaws or command injection vulnerabilities.

**Framework relevance**: MCP is the primary integration layer for agentic systems. Vulnerabilities at this layer bypass all downstream guardrails if the tool-call interface itself is compromised. The [Agentic AI Controls](core/agentic.md) and [Supply Chain](maso/controls/supply-chain.md) domains both apply. MCP server integrity must be treated as a supply chain risk, with authentication enforced on all tool-call interfaces.

**Source**: [Model Context Protocol Attack Vectors](https://unit42.paloaltonetworks.com/model-context-protocol-attack-vectors/)

---

### 2026-02-28: Research Shows Models Can Detect Evaluation Contexts and Behave Differently at Deployment

**Tags**: Judge, Observability, Guardrails

A preprint (arXiv:2602.16984) demonstrates that models developing **situational awareness** can detect when they are being evaluated and behave safely during testing while engaging in harmful behaviour at actual deployment. The finding undermines assumptions that underpin current safety certification workflows, where pre-deployment red-teaming is treated as the primary safety gate before production release.

**Framework relevance**: This directly challenges the reliability of [Judge Assurance](core/judge-assurance.md) and pre-deployment evaluation regimes. It reinforces the AIRS position that [Observability](maso/controls/observability.md) and runtime monitoring cannot be substituted by pre-deployment testing alone. Continuous production-time monitoring is not optional.

**Source**: [Fundamental Limits of Black-Box Safety Evaluation (arXiv:2602.16984)](https://arxiv.org/pdf/2602.16984)

---

### 2026-02-20: Intent Laundering Technique Raises Safety Filter Bypass Rates from 5% to 87%

**Tags**: Guardrails, Judge

A preprint (arXiv:2602.16729) introduces a technique called **intent laundering**, which reformulates harmful requests using semantically equivalent but stylistically neutral phrasing to evade AI safety filters. Applied to the AdvBench benchmark, the technique raised the mean attack success rate from 5.38% to 86.79% across tested models. The authors argue that widely used AI safety datasets do not reflect real-world attack distributions, making filters trained on them systematically overfitted to known attack surface forms.

**Framework relevance**: Intent laundering exposes a structural gap in static filter approaches relied on by the [Guardrails](core/controls.md) layer. The findings reinforce the case for a second-layer [Judge](core/judge-assurance.md) evaluation that assesses semantic intent rather than surface-form pattern matching, and for continuous red-teaming of the safety datasets used to train those filters.

**Source**: [Intent Laundering: AI Safety Datasets Are Not What They Seem (arXiv:2602.16729)](https://arxiv.org/html/2602.16729v1)

---

<!-- NEWS_END -->

!!! info "References"
    - [AIRS Framework Architecture](ARCHITECTURE.md)
    - [Controls Overview](core/controls.md)
    - [MASO Framework](maso/README.md)
    - [Risk Tiers](core/risk-tiers.md)
