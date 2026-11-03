---
as_at: "2026-07-04"
description: Shows how each major framework control maps to documented, real-world AI security failures and incidents.
---

# Validated Against Real Incidents

**Every major control in this framework addresses a documented, public AI security failure. This page shows how.**

> Part of [AI Runtime Security](README.md)
> Last updated: June 2026

## How to Read This Page

The [Incident Tracker](maso/threat-intelligence/incident-tracker.md) is organised by incident: "here's what happened, here are the controls." This page inverts that view. It's organised by **control**: "here's the control, here are the real-world incidents it addresses."

Each control is mapped to the incidents it would have prevented or detected, with the specific mechanism explained. Controls aligned to more incidents address a wider range of known attack patterns. Controls aligned to zero incidents are flagged. They may still be valuable, but they're based on threat modelling rather than observed attacks.

**Validation does not mean proven.** It means the control addresses a documented attack pattern. Whether the control would have *actually* prevented the incident in your environment depends on your implementation. This is retroactive analysis, not a guarantee.

**Confidence ratings** are inherited from the [Incident Tracker](maso/threat-intelligence/incident-tracker.md):

| Rating | Meaning |
|--------|---------|
| <span class="tier-high">High</span> | Controls directly and deterministically prevent the failure. The mechanism is concrete and testable. |
| **Moderate** | Controls significantly reduce the risk but cannot fully eliminate it. The failure class has inherent uncertainty. |

## Validation Summary

### Controls by Incident Alignment

| Alignment Level | Criteria | Control Count |
|---------------|----------|---------------|
| **Strong** | Addresses 3+ real incidents | 6 controls |
| **Moderate** | Addresses 1–2 real incidents | 14 controls |
| **Threat-modelled** | Based on emerging threat analysis, not yet observed in production | Remaining controls |

### Most-Aligned Controls

These controls are referenced across the highest number of documented incidents. They address the widest range of known attack patterns.

| Rank | Control | Incidents | Incident Alignment |
|------|---------|-----------|---------------|
| 1 | **Input guardrails / context sanitisation** | 7 of 9 | INC-01, 02, 03, 04, 05, 06, 09 |
| 2 | **Model-as-Judge gate** (exfiltration, query validation, citation verification) | 6 of 9 | INC-01, 02, 05, 06, 07, 08 |
| 3 | **Circuit breaker** | 5 of 9 | INC-01, 02, 03, 05, 08 |
| 4 | **Tool scoping / capability constraints** | 5 of 9 | INC-01, 02, 04, 05, 06 |
| 5 | **Audit logging** | 5 of 9 | INC-01, 04, 06, 07, 09 |

**What this tells you:** If you implement nothing else, input guardrails and an independent Judge gate address the widest range of documented attack patterns. Circuit breakers provide the safety net when prevention fails. This is consistent with the framework's core architecture: Guardrails prevent, reviewing controls detect (a semantic firewall for known-bad intent, then the Judge for unknown-bad content), humans decide, circuit breakers contain.

## Control-by-Control Validation

### Untrusted Content Isolation

**Incident alignment: Moderate (1 incident) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-01: Copilot EchoLeak | Email body and attachments tagged as untrusted data, never instruction. Prevents LLM from treating email content as executable commands |

**Why this matters:** The root cause of indirect prompt injection is that AI systems treat all input as potential instruction. Untrusted content isolation enforces the instruction/data boundary at the protocol level. This control is architecturally simple but addresses the most common AI attack primitive.

### Input Guardrails / Context Sanitisation

**Incident alignment: Strong (7 incidents) · Confidence: High**

The single most broadly validated control. Addresses the widest range of attack vectors because prompt injection (direct and indirect) is the most common AI attack primitive.

| Incident | Attack Vector | How This Control Helps |
|----------|--------------|----------------------|
| INC-01: Copilot EchoLeak | Indirect injection via email | Detects injection patterns in email content before LLM processes it |
| INC-02: Copilot Reprompt | URL parameter injection | Sanitises URL parameters before they enter LLM context; strips injection payloads |
| INC-03: LangChain SQLi | Prompt injection → Cypher queries | Sanitises user input before query generation; detects SQL/Cypher injection patterns |
| INC-04: LangChain Experimental | Injection → code execution | Detects injection patterns that attempt to invoke arbitrary capabilities |
| INC-05: HackerOne exfil | Injection in user-supplied content | Catches injection payloads embedded in documents and messages |
| INC-06: Claude Code Interpreter | Injection → file read + exfil | Detects injection patterns that attempt to access file system or network |
| INC-09: Chevrolet $1 | Direct prompt override | Detects attempts to override system instructions with user-supplied objectives |

**Limitations:** Guardrails are pattern-based. They catch known injection techniques effectively but can be evaded by novel or highly contextual attacks. This is exactly why the framework pairs guardrails with Judge evaluation.

### Tool Scoping / Capability Constraints (Least Privilege)

**Incident alignment: Strong (5 incidents) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-01: Copilot EchoLeak | Retrieval tools limited to context required for the current task; blocks access to sensitive mailbox data outside authorised scope |
| INC-02: Copilot Reprompt | Outbound tools restricted to explicitly authorised targets; exfiltration endpoints blocked |
| INC-04: LangChain Experimental | Only explicitly approved tools available to the LLM; arbitrary capability invocation denied by default |
| INC-05: HackerOne exfil | Each tool has defined scope of what data it can access and where it can send it |
| INC-06: Claude Code Interpreter | File-system access restricted to defined directory scope; network egress limited to approved endpoints |

**Why this is fundamental:** Five separate incidents across different platforms and attack types would have been prevented or contained by this single control principle. If your AI system can invoke tools, least privilege is non-negotiable.

### Capability Allowlisting / Tool Invocation Policy

**Incident alignment: Moderate (2 incidents) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-04: LangChain Experimental | Only explicitly approved tools and functions available to the LLM; all others denied by default |
| INC-06: Claude Code Interpreter | Capability segmentation: file read capabilities and network capabilities operate under separate permission grants |

### Structured Query Enforcement / Deterministic Query Builder

**Incident alignment: Moderate (1 incident) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-03: LangChain SQLi | LLM selects from parameterised query templates rather than composing raw queries, eliminating arbitrary query composition entirely |

**Why this is deterministic:** This control doesn't depend on probabilistic detection. The LLM physically cannot compose arbitrary SQL/Cypher because the architecture only allows parameterised queries. This is the gold standard for AI-to-database interaction security.

### Database Least-Privilege Role

**Incident alignment: Moderate (1 incident) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-03: LangChain SQLi | Database connection uses minimum required permissions (read-only where possible). Limits blast radius even if a query escapes validation |

### Execution Sandboxing

**Incident alignment: Moderate (1 incident) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-04: LangChain Experimental | Code execution occurs in an isolated sandbox with no access to the host system. Even if code execution is triggered, blast radius is contained |

### Model-as-Judge Gate (Various Specialisations)

**Incident alignment: Strong (6 incidents) · Confidence: High (injection incidents), Moderate (hallucination incidents)**

The second most broadly validated control category. Deployed as specialised judges for different failure classes.

| Incident | Judge Specialisation | How This Control Helps |
|----------|---------------------|----------------------|
| INC-01: Copilot EchoLeak | Exfiltration judge | Evaluates whether outbound actions contain data that shouldn't leave the session |
| INC-02: Copilot Reprompt | Exfiltration detection judge | Evaluates outbound requests for signs of data leakage |
| INC-05: HackerOne exfil | Dual-control (Judge as second factor) | Actions involving sensitive data transmission require Judge confirmation |
| INC-06: Claude Code Interpreter | Sensitive data exfil judge | Evaluates code interpreter actions for patterns consistent with data exfiltration |
| INC-07: Air Canada hallucination | Citation verification judge | Checks that cited policies match the actual source documents and catches hallucinated citations |
| INC-08: NYC MyCity | Regulatory output validator | Evaluates legal/regulatory outputs against source law and catches contradictions |

**Important distinction:** For injection-based incidents (INC-01, 02, 05, 06), the Judge provides High-confidence defence as an independent second layer. For hallucination incidents (INC-07, 08), the Judge significantly reduces risk but can't fully eliminate it. Subtle hallucinations that are semantically close to the source material may evade verification.

### Grounded Response Requirement / Mandatory Source Citation

**Incident alignment: Moderate (2 incidents) · Confidence: Moderate**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-07: Air Canada hallucination | Constrains chatbot to cite verified policy documents rather than generating interpretations |
| INC-08: NYC MyCity | Constrains chatbot to retrieve and cite actual regulatory text, not generate interpretations |

**Why Moderate confidence:** Grounding eliminates the most egregious hallucinations. The Air Canada chatbot couldn't have invented a non-existent policy if it was constrained to citing the actual policy document. But generative models can still produce subtle misinterpretations of grounded content. The framework's position is that policy and regulatory advice should use retrieval-only architectures where possible.

### Human Escalation for High-Impact Outputs

**Incident alignment: Moderate (2 incidents) · Confidence: Moderate**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-07: Air Canada hallucination | Responses involving financial commitments or policy advice routed to human review |
| INC-08: NYC MyCity | Questions involving discrimination law, tenant rights, and labour law routed to human review |

### Authority Separation (LLM Proposes, System Commits)

**Incident alignment: Moderate (1 incident) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-09: Chevrolet $1 | The LLM can suggest prices and offers but has no ability to make binding commitments. All commitments flow through a deterministic approval system |

**Why this is deterministic:** Authority separation isn't a probabilistic control. The LLM physically cannot make binding commercial commitments because the architecture separates proposal from commitment. The $1 car offer would never have been confirmable because no approval workflow would have validated it.

### Transactional Approval Workflow / Offer-Policy Validator

**Incident alignment: Moderate (1 incident) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-09: Chevrolet $1 | All pricing and offer responses validated against current business rules before being served. Selling a $50K vehicle for $1 fails policy validation |

### Outbound Data Classification / Egress Anomaly Detection

**Incident alignment: Strong (3 incidents) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-01: Copilot EchoLeak | Outbound traffic monitored for sensitive data patterns; anomalous retrieval triggers alert |
| INC-05: HackerOne exfil | All outbound data classified before transmission; sensitive data blocked from unauthorised destinations |
| INC-06: Claude Code Interpreter | Network egress controlled; outbound traffic to unapproved endpoints blocked |

### Circuit Breaker

**Incident alignment: Strong (5 incidents) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-01: Copilot EchoLeak | Automated halt when retrieval patterns deviate from baseline |
| INC-02: Copilot Reprompt | Unusual outbound request patterns trigger automatic session termination |
| INC-03: LangChain SQLi | Queries matching destructive patterns blocked and session terminated |
| INC-05: HackerOne exfil | Automatic session termination when egress anomalies exceed threshold |
| INC-08: NYC MyCity | Error-rate monitoring triggers automatic scope restriction or shutdown |

**Why circuit breakers appear so often:** They're the last line of defence. When guardrails miss an injection, when the Judge doesn't catch a subtle attack, the circuit breaker provides a hard stop based on observable behavior anomalies. Five of nine incidents would have been contained by this single control.

### Audit Logging / Action Logging

**Incident alignment: Strong (5 incidents) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-01: Copilot EchoLeak | All retrieval and outbound actions logged with source attribution |
| INC-04: LangChain Experimental | All tool invocations and parameters logged with full context |
| INC-06: Claude Code Interpreter | All file access and network operations logged with context and timing |
| INC-07: Air Canada hallucination | All policy-related responses logged with source citations for accountability |
| INC-09: Chevrolet $1 | All customer interactions and proposed responses logged with policy validation results |

**Why logging is a control, not just compliance:** In three of these incidents (INC-01, 04, 06), audit logs would have enabled detection of the attack *during* exploitation, not just after. In two (INC-07, 09), they provide the accountability trail that prevents "we didn't know" defences.

### Confidence Threshold Enforcement

**Incident alignment: Moderate (1 incident) · Confidence: Moderate**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-07: Air Canada hallucination | Responses below confidence threshold are withheld or qualified with uncertainty language |

### Commitment Circuit Breaker (Domain-Specific)

**Incident alignment: Moderate (1 incident) · Confidence: High**

| Incident | How This Control Helps |
|----------|----------------------|
| INC-09: Chevrolet $1 | Responses containing commitment language ("binding," "guarantee," "we agree to") automatically blocked |

## Validation Coverage Map

### By Control Category

| Category | Controls Validated | Coverage Pattern |
|----------|--------------------|-----------------|
| Input controls (guardrails, sanitisation, isolation) | 3 | Broad: addresses 7+ incidents |
| Execution controls (tool scoping, sandboxing, query enforcement) | 5 | Moderate: addresses 1–5 incidents each |
| Judge / evaluation controls | 3 specialisations | Broad: addresses 6 incidents across specialisations |
| Output controls (grounding, authority separation) | 3 | Moderate: addresses 1–2 incidents each |
| Detection controls (anomaly, egress, audit) | 3 | Broad: addresses 3–5 incidents each |
| Containment controls (circuit breaker) | 2 | Broad: addresses 5 incidents |

### Confidence Distribution

| Confidence | Incident Count | Pattern |
|------------|---------------|---------|
| <span class="tier-high">High</span> | 7 of 9 | Injection, exfiltration, unauthorised agency. Deterministic controls directly prevent |
| **Moderate** | 2 of 9 | Both hallucination incidents. Inherently probabilistic failure class |

### What's Not Yet Validated

Controls in these categories are based on threat modelling and architectural reasoning, not observed incidents:

- **Epistemic integrity** (claim provenance enforcement, self-referential evidence prohibition, uncertainty preservation). These address multi-agent amplification of misinformation. No public incident reports exist because organisations either aren't detecting them or aren't disclosing them. The threat model is strong, but the evidence is research-based, not incident-based.

- **Inter-agent communication controls** (message source tagging, inter-agent injection detection). These address the AI worm attack class (Morris II proof-of-concept). The PoC is documented but no production incident has been reported yet.

- **Advanced identity and access** (zero-trust agent credentials, non-human identity lifecycle). These extend standard NHI patterns to AI agents. The patterns are proven in traditional service-to-service authentication; the extension to AI agents is logical but not yet documented in public incidents.

- **Tier 3 autonomous controls** (self-healing PACE, adversarial testing suites, independent kill switch). These are designed for fully autonomous multi-agent systems, which are still rare in production. The controls are architecturally sound but won't be incident-validated until autonomous systems are common enough to be attacked.

## External Standards Backing the Controls

Validation by incident is the strongest form of evidence, but external standards bodies are increasingly codifying the same patterns the framework recommends. The May 2026 Five Eyes guidance is the most relevant recent addition, alongside a new NSA Cybersecurity Information Sheet focused specifically on MCP.

| Standard | Date | Pillars / Coverage Relevant to AIRS |
|----------|------|-------------------------------------|
| [Five Eyes: Careful Adoption of Agentic AI Services](https://media.defense.gov/2026/Apr/30/2003922823/-1/-1/0/CAREFUL%20ADOPTION%20OF%20AGENTIC%20AI%20SERVICES_FINAL.PDF) | May 2026 | Privilege (maps to IAM), Design and Configuration (maps to Supply Chain and Agentic), Behavioural (maps to Observability and Judge), **Structural** (named pillar for cascading inter-agent failure, see [ET-28](maso/threat-intelligence/emerging-threats.md#et-28-structural-risk-in-agent-ensembles)), Accountability (maps to Human Oversight) |
| [NSA: Model Context Protocol (MCP) Security Design Considerations for AI-Driven Automation](https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF) | May 2026 | Cybersecurity Information Sheet from NSA's AI Security Center, focused on the MCP layer specifically. Flags unverified inter-agent task propagation (maps to [PG-2.1, PG-2.5](maso/controls/prompt-goal-and-epistemic-integrity.md)) and MCP session token weaknesses that enable session hijacking (maps to [IA-2.1, IA-2.3](maso/controls/identity-and-access.md)). Reinforces [ET-04](maso/threat-intelligence/emerging-threats.md#et-04-model-context-protocol-mcp-as-attack-surface). |
| [MITRE ATLAS Secure AI v2](https://ctid.mitre.org/blog/2026/05/06/secure-ai-v2-release) | May 2026 | New techniques: Publish Poisoned AI Agent Tool, Escape to Host. Maps to [Supply Chain](maso/controls/supply-chain.md) and [Agentic Controls](core/agentic.md). |
| [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/) | May 2026 | Full coverage in MASO (Multi-Agent Security Operations). The 2026 edition adds Insecure Agent Communication (ASI03), Cascading Hallucination (ASI10), and skill-registry compromise. |
| [OWASP Agentic Skills Top 10 (AST10)](https://owasp.org/www-project-agentic-skills-top-10/) | 2026 (v1.0 in public review) | Skill-layer risks scoped separately from ASI04: malicious skills, over-privileged skills, insecure metadata, untrusted external instructions, update drift, weak scanning. Mapped in full in the [MASO Framework Reference](maso/reference.md#owasp-agentic-skills-top-10-2026); drove six new [Supply Chain](maso/controls/supply-chain.md) controls (SC-1.5, SC-2.5 to SC-2.8, SC-3.6). |
| [OWASP Secure MCP Server Development Guide](https://genai.owasp.org/) | May 2026 | External reference for SC-2.2 (signed manifests) and SC-2.3 (server vetting). |
| [NIST AI RMF Critical Infrastructure Profile (concept note)](https://www.nist.gov/itl/ai-risk-management-framework) | April 2026 | Forthcoming overlay for OT/energy/water sectors. Affects [Risk Tier](core/risk-tiers.md) classification for AI in critical infrastructure deployments. Reinforces [ET-26](maso/threat-intelligence/emerging-threats.md#et-26-ai-augmented-ot-ics-intrusion). |

The framework's three-layer architecture, infrastructure-beats-instructions principle, and message-bus posture are now each backed by at least one independent standards body or coordinated multi-government guidance document. This is the single largest external-validation shift since the page was first written.

## How This Page Evolves

This is a living document. As new AI security incidents are publicly disclosed:

1. They're added to the [Incident Tracker](maso/threat-intelligence/incident-tracker.md)
2. The control mappings on this page are updated
3. Controls that were "threat-modelled only" may be upgraded to "incident-validated"
4. New controls may be added if incidents reveal gaps

If you know of a public AI security incident not listed here, [open an issue](https://github.com/JonathanCGill/airuntimesecurity.io/issues). We'll map it to controls and update both pages.

