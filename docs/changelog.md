# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Agent Skills specification conformance and agent secret controls in MASO.** `maso/controls/supply-chain.md` now adopts the [Agent Skills specification](https://agentskills.io/specification) as the format baseline for `SKILL.md` packages, with a new *Agent Skills Specification Conformance* section that maps each element of the spec (directory, `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`, file references, progressive disclosure, `skills-ref validate`) to the MASO control that secures it. New controls: **SC-1.6** Agent Skills format conformance, **SC-2.9** skill secret hygiene, and **SC-2.10** skill invocation-time execution (shell injection and skill hooks off by managed policy unless approved). A *Platform Profile: Claude Code* subsection maps Claude Code's extensions to the spec (`allowed-tools` as a pre-approval, `` !`command` `` injection, skill `hooks`, `context: fork`, skill locations and precedence, live reload) to the controls and managed settings that address them. SC-1.5 hashes the whole skill directory, SC-2.5 rejects unknown front-matter keys and path escapes and treats `description` as a start-up instruction surface, and SC-2.6 treats `allowed-tools` as an author claim rather than a permission boundary. `maso/controls/identity-and-access.md` gains **IA-1.5** managed secret storage, **IA-2.8** tool-boundary secret injection (no inherited environment or credential files), **IA-2.9** secret redaction at ingress and persistence, **IA-3.5** sender-constrained tokens (RFC 8705, RFC 9449), and **IA-3.6** canary credentials, each with tests. SR-05 (secrets leakage) moves to covered in the risk register, and the AST10 mapping is updated. The headline count is recomputed from the control files at 233 (Tier 1: 64), which also picks up controls added since the last recount.
- **README kept in sync automatically.** Fixed eleven broken README links and stale counts (MASO controls, domains, emergent risks, red-team scenarios, SDK tests). Added `.github/scripts/readme_facts.py`, which derives each count from source and checks or rewrites the README, and a `README facts` workflow that fails a pull request when the README drifts.
- **OWASP Agentic Skills Top 10 (AST10) mapping in MASO.** Added a full AST01-AST10 coverage table to `maso/reference.md` alongside the LLM and Agentic Top 10 tables, with a stated limit of coverage (runtime discovery from public registries is outside what MASO assures). The mapping showed the Supply Chain domain treated skills as tools, so `maso/controls/supply-chain.md` gains six controls with matching tests: **SC-1.5** skill inventory and installation control (no direct installs from public registries), **SC-2.5** skill definition validation (safe parsers, hidden-character and impersonation rejection, re-validation when ported), **SC-2.6** per-skill permission manifest with a default block on the Lethal Trifecta, **SC-2.7** external instruction pinning, **SC-2.8** skill version and source pinning, and **SC-3.6** behavioural skill evaluation. Skills added to the AIBOM. Closed the two open ET-13 gaps in `emerging-threats.md`, extended INC-10 in the incident tracker, and added AST10 to `validated-against.md` and `references.md`. Headline control count is now 218 (Tier 1: 62).
- **Mid-July 2026 threat review.** Added **ET-30 (AI Gateway and Inference-Proxy Compromise)** to `maso/threat-intelligence/emerging-threats.md`, recording Darktrace's cryptojacking of an Amazon Bedrock model gateway (an internet-exposed `LiteLLM-Proxy` EC2 instance with a Bedrock instance profile, hijacked for XMRig mining) and the LiteLLM MCP authentication-bypass CVE-2026-59822 as the same privileged choke point reached without credentials, distinguished from ET-19, ET-23, and ET-27, with the threat-landscape table extended to match. Sharpened **ET-27** with the ASSET Research Group's *Ghostcommit* (prompt injection hidden in a PNG referenced from an `AGENTS.md` file, bypassing text-based code reviewers that treat images as opaque blobs) and **ET-13** with *HalluSquatting* (predictable, transferable resource-name hallucinations pre-registered to pull adversarial prompts into an agentic botnet, arXiv:2607.07433). Added **INC-16** (Amazon Bedrock AI gateway cryptojacking) to the incident tracker, and three matching `news.md` items (Ghostcommit, AI gateway cryptojacking, HalluSquatting) mapped to framework controls.
- **Autonomous-attacker threat additions (July 2026).** Added **ET-29 (Fully Autonomous Offensive Agents / Agentic Ransomware)** to `maso/threat-intelligence/emerging-threats.md`, recording Sysdig's *JadePuffer* as the first ransomware operation run end to end by an LLM agent (initial access via Langflow CVE-2025-3248, autonomous kill chain, unrecoverable extortion) and distinguishing it from ET-08 and ET-26, with the updated threat-landscape table extended to match. Sharpened **ET-22** with LayerX's *BioShocking* as a cross-vendor demonstration of refusal-logic exploitation by reality-reframing against six agentic browsers. Added two matching `news.md` items (BioShocking, JadePuffer).
- **July 2026 news batch** on `news.md`, four items mapped to framework controls: *Governance Decay* (context compaction silently drops in-context safety constraints in long-horizon agents, arXiv:2606.22528), *From Shield to Target* (denial-of-service against LLM guardrails themselves, arXiv:2606.14517), the *Mastra* npm agent-framework backdoor attributed to Sapphire Sleet, and a systematic study of *memory poisoning* aligned to OWASP ASI06 (arXiv:2606.04329). Sharpened the affected Emerging Threats with the new evidence and mitigations: **ET-15** now names Governance Decay and Constraint Pinning as the concrete mechanism and control behind its long-horizon drift gap, **ET-19** extends Reasoning DoS to the guardrail and Judge tiers plus shared-infrastructure blast radius, and **ET-13** records Mastra as the supply chain class reaching the agent framework itself. Added **INC-15** (Mastra) to the incident tracker and refreshed both threat-intelligence pages to July 2026.
- **Reviewing reading path** on `reading-paths.md`. New "I need to review and verify what the AI produced" goal path leads with [The Verification Gap](insights/the-verification-gap.md) so reviewing reads as matching the right verification tool to the claim, not defaulting to an LLM Judge. Rebalanced the Golden Thread's Judge-heavy Act II by promoting the [Semantic Firewall](core/controls/semantic-firewall.md) to a numbered article (now article 7 of 15, semantic checks and context validation, placed before the Judge articles), renumbering the per-page "Part of the Golden Thread" chrome across the sequence, and adding a "Match the review control to latency and accuracy" comparison table covering the wider set of review processes (guardrails, semantic firewall, knowledge-graph and API lookups, token-level uncertainty, formal verification, Model-as-Judge, human review) with their latency and accuracy trade-offs.
- **Semantic Firewall** standalone page (`core/controls/semantic-firewall.md`), documenting intent-level boundary enforcement between Guardrails and Model-as-Judge. Linked from the homepage's Reviewing Controls bullet, the three-layer controls page, LOG-06 (injection detection), and NET-03 (Judge isolation) on AWS Bedrock and Databricks.
- **Lethal Trifecta** heuristic and **OWASP Agentic Skills Top 10 (AST01-AST10)** reference, added to `insights/the-agent-supply-chain-crisis.md`, `maso/threat-intelligence/emerging-threats.md` (ET-13), and `maso/controls/supply-chain.md` (Common Pitfalls). Tracks a class of risk OWASP scoped separately from ASI04 after the ClawHub/OpenClaw incident.
- **Least Agency** as a named principle distinct from least privilege, added to `core/iam-governance.md` - autonomy is scoped per task independently of permission scope.

### Changed
- **Consistent reviewing framing across the site.** Following the `reading-paths.md` rebalance, swept pages that presented the middle of the stack as the Model-as-Judge alone and reframed the detection tier as a spectrum of controls reaching the same goal at different speeds and depths (semantic firewall for known-bad intent in milliseconds, Judge for deeper behavioural evaluation, independent verification for facts), keeping the three-layer model intact. Touched `quick-start.md`, `faq.md`, `core/controls.md`, `infrastructure/mappings/controls-to-three-layers.md`, `infrastructure/mappings/csf-2.0.md`, `stakeholders/risk-and-governance.md`, `stakeholders/compliance-and-legal.md`, `stakeholders/ai-engineers.md`, `extensions/regulatory/eu-ai-act-risk-tiering.md`, `extensions/regulatory/high-risk-financial-services.md`, and the Golden Thread articles `insights/why-guardrails-arent-enough.md`, `insights/containment-through-intent.md`, and `insights/reference.md`.
- **Reviewing-controls sweep across the MASO pages.** Extended the same reframing into the MASO framework surfaces, which still routed evaluation to the Model-as-Judge alone. `maso/controls/objective-intent.md` gained a "Matching Reviewing Controls to Intent Criteria" section mapping each OISpec criterion type to the control that can verify it (deterministic check, semantic firewall, independent verification, Judge, human), with token-level uncertainty kept as an escalation signal rather than a factual verifier. Broadened the "Model-as-Judge (Layer 2)" architecture labels in `maso/implementation/tier-1-supervised.md` and `tier-2-managed.md`, the decision table in `maso/controls/privileged-agent-governance.md`, the risk-proportionate table in `maso/reference.md`, per-message/per-action framing in `maso/stress-test/100-agent-stress-test-overview.md` and `ecommerce-10k-stress-test.md`, the control-set summaries in `maso/environment-containment.md`, the EC-2.5 gate note in `maso/controls/execution-control.md`, and a fact-lookup mapping row in `maso/examples/worked-examples.md` (fact checks routed to independent verification, not the Judge). Also fixed a `Model-as-Model-as-Judge` typo in `maso/controls/supply-chain.md` and reframed the Verification Gap summary in `insights/reference.md` from "solved by Judge Assurance" to matching each claim to a verification method along the spectrum.

### Planned
- Cost model with production data
- Platform-specific implementation guides (detailed)
- Case studies from production deployments
- Judge accuracy benchmarks from real deployments
- Epistemic risk detection algorithm specifications

## [0.10.0] - 2026-04-15

Reorganised the site into a product-shaped structure with five top-level tabs (**Home**, **Start**, **Framework**, **For Your Role**, **Library**), added colour affordances across risk tables, wired up missing maintenance features (edit links, last-updated stamps, per-page social cards), and added an April news batch covering Anthropic Claude Mythos, CVE-2026-32211 in the Azure MCP Server, and the OpenClaw supply chain crisis.

### Added

- **Start landing page** (`start.md`) as a 30-second triage for five entry points: AIRSLite, Fast Lane, Quick Start, Reading Paths, FAQ. Chosen by reader situation, not feature name.
- **Library landing page** (`library.md`) indexing Insights, Implementation (Infrastructure, Strategy, SDK), Reference (Regulatory, Technical Reference, Templates, Examples, Downloads), and Project (Changes, About) as a scannable shelf index.
- **Find Your Role cards on Home.** All nine stakeholder roles visible as cards with their core question in italics, directly on the landing page.
- **Golden Thread context chrome** on 14 reading-path articles. Each carries a "Part of the Golden Thread (N of 14)" admonition with Previous / Next links.
- **Risk-tier pill styling** across 107 table cells in 27 files. Green Low, amber Medium, orange High, red Critical, with dark-mode variants.
- **Four Control Layers colour accents** on the Home page: Guardrails green (prevention), Judge blue (detection), Human Oversight amber (accountability), Circuit Breakers red (failsafe).
- **Header tab icons**: flag (Start), hexagon (Framework), person (For Your Role), book stack (Library). Rendered as inline SVG mask-image so they inherit text colour in both light and dark schemes.
- **Edit on GitHub links.** `repo_url`, `repo_name`, and `edit_uri: edit/main/docs/` wired up so the previously dormant `content.action.edit` and `content.action.view` theme features now work.
- **Automatic "Last updated" dates** per page via `mkdocs-git-revision-date-localized-plugin`. Workflow uses `fetch-depth: 0` so CI has full history.
- **Per-page social cards** via Material's `social` plugin. Each page now gets a unique OG / Twitter card image instead of the single static `architecture-overview.png`.
- **MASO (Multi-Agent Security Operations) File Structure block** updated to reflect all promoted documents (extraction-integrity, privileged-agent-governance, threat-intelligence-review, ecommerce stress test, judge-proliferation review, MASO 2.0 roadmap).

### Changed

- **Top navigation** consolidated from 10 tabs to 5: Home, Start, Framework, For Your Role, Library. The four non-Home tabs are now visible (the old `.md-tabs { display: none }` rule was hiding everything).
- **Home page** rewritten with Three Doors matching the core user questions (how to run AI securely, how to secure AI at runtime, how to get the most out of AI safely), followed by Find Your Role, Framework at a Glance, and Four Control Layers. Trimmed "The Problem AIRS Solves" section (duplicated the hero framing).
- **Stakeholder page** converted from a dense 9-row table to three themed card groups (Security and risk, Technology and architecture, Product and business). Page title changed from "Stakeholder Views" to "For Your Role" so the H1 matches the nav label.
- **Foundations landing** (`foundations/README.md`) rewritten as a concise 74-line Single-Agent Overview that hands off to Core Controls for the control reference, rather than duplicating it.
- **Architecture Overview** tightened: the three-layer pattern is now defined once in the headline table rather than twice; bullets in Single-Agent section reworked to lead with practical choices rather than restating the table; Circuit Breaker added as a fourth bullet so the list matches the table.
- **Regulatory section** grouped by jurisdiction: International Standards, EU, Sector-Specific, Operational. Same shape as Technical Reference.
- **Technical Reference** landing page regrouped into Judge Internals, Detection and SOC, Control Catalogues, and Economics and Identity.
- **Changelog** older entries (0.8.4 and below) collapsed into a single `<details>` block so the top of the page shows only the current release.
- **MASO risk register** fixed: added the missing EP-09 "Task ambiguity as silent failure" row, corrected the frontmatter count (34 → 35), changed four US spellings to UK English, and rewrote seven hyphen-as-dash violations.
- **AI Engineers stakeholder page** wording: Judge described as "an independent model (SLM or LLM)" instead of "an independent LLM", for consistency with the rest of the site.

### Removed

- **Hand-maintained `docs/sitemap.xml`** (1,054 lines). It was overwritten on every build by MkDocs' auto-generated sitemap and missed 56 pages including the new Start and Library landings.
- **Dead CSS** (~120 lines): `.home-subtitle`, `.home-tldr`, `.home-primary-cta`, `.home-paths`, `.home-path`, `.pull-quote`. All leftover from the pre-reorganisation Home page and not referenced anywhere.

### Fixed

- **117 "unrecognized relative link" notices** in the MkDocs build log. All directory-style links (`../maso/`, `../infrastructure/`, `./`) rewritten to explicit README targets across 45 files so IDE link resolvers and MkDocs both see an explicit target.
- **Orphan pages** promoted into nav: PACE-RESILIENCE, FAST-LANE, MATURITY, VALIDATED-AGAINST, IMPLEMENTATION_GUIDE, CHANGELOG, REFERENCES, strategy orphans (the-thread, use-case-definition, platform-and-patterns, data-reality, progression), MASO orphans (objective-intent, emerging-threats, threat-intelligence-review, stress tests, judge-proliferation review, MASO 2.0 roadmap), infrastructure orphans (session-and-scope, csf-2.0, nist-sp800-218a, controls-to-three-layers, agentic supply-chain), and the `core/pace-*-section` fragments.
- **ABOUT author image** path (preserved the original `../images/` path after investigating a false-positive audit report).
- **Octicons shortcodes** on Home that rendered as literal text because the `pymdownx.emoji` extension was not configured.
- **`.cache/`** added to `.gitignore` to stop the mkdocs-material social plugin cache from being committed.

### News

Three news items added for April 3-15 2026: Anthropic's Claude Mythos Preview and Project Glasswing consortium (autonomous zero-day discovery); CVE-2026-32211, a CVSS 9.1 missing-authentication flaw in the Azure MCP Server; and the ongoing OpenClaw supply chain crisis (135,000 exposed instances, 824+ malicious skills on ClawHub, Snyk's ToxicSkills study finding 36% prompt injection rate).

## [0.9.1] - 2026-03-09

### Added

- **MASO 2.0 Anticipated Changes** (`maso/maso-2.0-anticipated-changes.md`) - Forward-looking analysis of six AI capability trajectories that will stress or break the current framework, with architectural responses and a three-phase roadmap. Covers: Judge ceiling (primary models exceeding evaluation capability), human oversight scaling (transaction review becoming untenable), session boundary dissolution (persistent/ambient agents), multi-agent emergent behaviors (fleet-level unanticipated states), AI-vs-AI adversarial dynamics (machine-speed offense vs. human-speed defense), and regulatory divergence (conflicting jurisdictional requirements). Defines MASO 2.0 priority roadmap across three phases: Extend (0–6 months), Architect (6–18 months), and Paradigm Shift (18–36 months).

### Changed

- **MASO README** (`maso/README.md`) - Added MASO 2.0 Anticipated Changes section with evolution vector summary table and roadmap overview. Positioned between Stress Testing and What's Next sections.

### Rationale

The v0.9.0 threat intelligence review identified three structural gaps in the current framework. This analysis extends that work forward: given observable AI capability trajectories, where will the framework's current architecture become insufficient, and what architectural changes must be planned now? Six vectors were identified; each is assessed for timeline, confidence, impact on current controls, and specific MASO 2.0 response. The deeper finding: the framework's "constrain regardless" principle becomes more important, not less, as evaluation and oversight become harder. Infrastructure-level action-space constraints are the control layer that scales with model capability.

## [0.9.0] - 2026-03-09

### Added

- **Output Evaluator** (`extensions/technical/output-evaluator.md`) - New solution architecture document addressing three structural blind spots identified through 2025–2026 threat intelligence analysis. Provides a three-layer evaluation model operating at real-time (per-action), session (per-task), and campaign (cross-session) timescales. Includes action classification, pre-action Judge prompt structure, intent coherence scoring, session state tracking, cross-session correlation, cost/latency impact analysis, and tiered implementation guide (Tier 1–3).

- **Session-Level Intent Analysis** (`core/agentic.md` §6) - **Major addition.** New core control addressing task decomposition attacks, where adversaries break malicious goals into individually benign sub-tasks that pass all per-interaction controls. Adds session-level action sequence analysis, intent coherence tracking, cumulative scope monitoring, and session-level circuit breakers with aggregate thresholds. Driven by: Anthropic September 2025 espionage disclosure (80–90% autonomous campaign via task decomposition), CrowdStrike documentation of adversary frameworks designed for sub-task decomposition.

- **Synchronous Pre-Action Evaluation** (`core/agentic.md` §7) - **Major addition.** New core control extending the Judge with a synchronous pre-action evaluation mode for agentic systems. Risk-based action routing: low-risk actions proceed with async evaluation; elevated-risk actions require synchronous Judge approval before execution. Includes action classification taxonomy, architecture diagram, and cost/latency tradeoff analysis. Driven by: CrowdStrike fastest eCrime breakout time (27 seconds) vs. async Judge evaluation cycle (500ms–5s + queue), creating a structural prevention gap for agentic systems.

- **Tool and Integration Supply Chain** (`core/agentic.md` §8) - **Major addition.** Elevated supply chain and integration layer controls from MASO extensions to core agentic controls. Includes minimum controls (provenance verification, tool output sanitisation, network isolation, permission scoping, behavior monitoring, dependency scanning) and MCP-specific controls (server allowlisting, schema validation, capability restriction, update verification). Driven by: Cisco 2025 finding that attackers target integration components over models; 43% MCP server vulnerability rate; CVE-2025-6514 (CVSS 10.0 RCE via MCP); fake npm MCP package and GitHub issue injection attacks.

- **Threat Intelligence Review** (`maso/threat-intelligence/threat-intelligence-review.md`) - Comprehensive analysis of 2025–2026 threat landscape covering CrowdStrike, Microsoft, Anthropic, Cisco, Kiteworks, and academic research. 18 priority recommendations across framework domains. Identifies three structural gaps: task decomposition defeating per-interaction controls, speed asymmetry making async Judge a liability for agentic contexts, and integration layer as primary attack surface.

### Changed

- **Agentic Controls** (`core/agentic.md`) - Extended Judge for Agents criteria with session coherence and trace integrity. Updated Key Takeaways from 8 to 11 items, adding aggregate intent detection, pre-action evaluation, and integration layer security.

### Rationale

Threat intelligence analysis (CrowdStrike 2025 Global Threat Report, Microsoft Digital Defense Report 2025, Anthropic September 2025 disclosure, Cisco AI Defense Report 2025, Kiteworks 2025 Data Exposure Report, AISI Frontier AI Trends December 2025) revealed three architectural gaps in the framework's control model:

1. **Task decomposition defeats per-interaction controls.** The three-layer pattern evaluates at the interaction level. Adversaries, including AI-orchestrated campaigns, decompose malicious goals into sub-tasks that individually pass every layer. This is an architectural gap, not a tuning problem.

2. **Speed asymmetry makes async Judge evaluation a liability for agentic systems.** The 27-second breakout window is shorter than async Judge evaluation cycles. For agents with tool access, post-action detection is forensic, not preventive.

3. **Integration layer is the primary attack surface but was positioned as an extension.** MCP vulnerability rates (43%), critical CVEs (CVSS 10.0), and supply chain attacks through tool packages demonstrate that tool supply chain security is a prerequisite for agentic deployments, not an optional add-on.

These are the first **major** additions to core controls since v0.5.0. The framework's core architecture (Guardrails → Judge → Human) remains sound for per-interaction threats. These additions extend it to handle campaign-level, speed-critical, and supply-chain threats that the 2025–2026 landscape has made operationally relevant.

<details markdown>
<summary><strong>Earlier versions (0.8.4 and older)</strong></summary>

## [0.8.4] - 2026-03-01

### Added
- **Why Containment Beats Evaluation** - New position paper page articulating the constrain-regardless architecture for sandbagging-resistant AI governance. Covers closed-loop vs open-loop control, action-space vs reasoning-space constraints, compound defence by design, enterprise-owned Judge positioning, and honest acknowledgement of limits. Aligns the framework with the published position paper.

### Changed
- **Architecture Overview** - Added closed-loop control system framing, constrain-regardless language, and enterprise-owned Judge positioning.
- **Foundations README** - Added action-space constraint language, enterprise-owned Judge emphasis, and compound defence by design framing.
- **Evaluation Integrity Risks** - Reframed from "mitigate sandbagging" to "sandbagging is operationally irrelevant as a breakout vector" under the constrain-regardless architecture.
- **Containment Through Declared Intent** - Added constrain-regardless framing, action-space vs reasoning-space distinction, parental analogy, and closed-loop control system language.

## [0.8.3] - 2026-03-01

### Added
- **Containment Through Declared Intent** - New insights page articulating the framework's unified defence thesis. Declared intent is the organising principle that gives every layer (guardrails, Judge, monitoring, human oversight, PACE) its reference point. Covers how intent flows through the defence stack, downstream intent awareness between agents, the confinement model, and honest assessment of where the theory breaks down.

## [0.8.2] - 2026-03-01

### Added
- **CoSAI Principles Alignment** - Updated References with full alignment mapping to CoSAI's Principles for Secure-by-Design Agentic Systems (July 2025). Demonstrates how the framework's three-layer pattern, PACE resilience, and MASO controls operationalise CoSAI's three principles.
- **Producer/Implementer/Principal Accountability** - Added supply chain accountability model to the AI Governance Operating Model. Complements the three-lines governance model with a supply chain lens for distributing responsibility across technology producers, service implementers, and human principals. Credit to CoSAI.
- **SLSA-Style Supply Chain Provenance** - Added to ET-04 (MCP as Attack Surface). Recommends adapting SLSA for verifiable provenance of agent and model artifacts: signed build provenance, content hashes for tool definitions, and verifiable chain from source to deployment.

## [0.8.1] - 2026-03-01

### Added
- **E-Commerce 10K Stress Test** - New MASO stress test scenario: 6 agent types, 10,000 concurrent customers, 60,000 agent instances on EKS. Complements the 100-agent breadth test with a depth-and-volume test covering type-level observability, risk-tiered Judge sampling, exception-driven human oversight, Kubernetes-native identity, PCI scope containment, two-level PACE, graduated shutdown, and volume-based compound attacks.

### Changed
- **100-Agent Stress Test** - Added cross-reference to the new e-commerce stress test in the relationship table.

## [0.8.0] - 2026-03-01

### Added
- **Evaluation Integrity Risks** - New insights page covering sandbagging, evaluation evasion, and the AISI finding that black-box monitors lose accuracy on harder tasks. Includes mitigations: canary interactions, evaluation signature elimination, multi-model cross-validation, behavioral consistency monitoring.
- **AISI 5-Level MCP Autonomy Classification** - Added to The MCP Problem page. Maps MCP server autonomy levels (read-only through unbounded autonomous) to MASO implementation tiers, with specific guidance for financial services.
- **Self-Replication Capabilities (ET-09)** - New emerging threat in MASO threat intelligence. Documents RepliBench progression from 5% to 60% success rates (2023–2025) and implications for kill switch architecture.
- **Capability Acceleration (ET-10)** - New emerging threat documenting the ~8-month doubling time for autonomous task complexity, with implications for control framework evolution cadence.
- **Persuasion Scaling Risk** - Added to Emerging Trends. Documents AISI finding that persuasive capability increases with model scale while accuracy decreases, and post-training amplifies persuasion more than scaling.
- **Emotional Dependence Data** - Added to Emerging Trends. Documents AISI finding on 33% AI emotional support usage and 30x negative sentiment spikes during outages. PACE implications for service continuity.
- **AISI Reference** - Added UK AI Security Institute Frontier AI Trends Report (December 2025) to References & Sources page with full finding summary and cross-references to all updated pages. Added 6 new key statistics.

### Changed
- **Risk Tiers** - Added Domain-Specific Guardrail Tuning section with AISI evidence for uneven safeguard coverage across risk categories (R² = 0.097 capability-safety correlation, 40x jailbreak effort increase for targeted categories).
- **When the Judge Can Be Fooled** - Expanded sandbagging section with AISI empirical data on black-box monitor accuracy degradation. Added cross-reference to new Evaluation Integrity Risks page.
- **Open-Weight Models** - Added AISI confirmation that safeguards can be "quickly and cheaply removed" and 4–8 month open-to-closed source capability gap data. Strengthens case for runtime monitoring as primary control.
- **Emerging Threats** - Updated threat landscape summary table to include ET-09 and ET-10.

### Rationale
The UK AI Security Institute's Frontier AI Trends Report (December 2025) is the strongest empirical backing for runtime behavioral security from a government body. Its findings directly validate the framework's core thesis (runtime controls matter more than deployment-time security alone) and provide concrete data points that strengthen multiple framework sections. Credit given throughout via source attribution.

## [0.7.0] - 2026-02-15

### Added
- **maturity.md** - Honest assessment of framework validation status
  - Four-level validation model (production, incident, standards, pattern consistency)
  - Explicit documentation of known gaps
  - Call for pilot partners and peer review
- **validated-against.md** - Control-by-control incident validation
  - Controls mapped to known real-world incidents with confidence ratings
  - Evidence strength ratings (Strong: 3+ incidents, Moderate: 1–2, Threat-modelled: 0)
  - Validation coverage map by MASO domain
  - Top 5 most-validated controls identified
- **EVOLUTION.md** - Narrative history of framework development
  - Decision rationale for every major version
  - What drove each change (incidents, feedback, architectural shifts)
  - Timeline from v0.1.0 (Dec 2025) through current

### Changed
- Updated site navigation to include Credibility section (Maturity, Validated Against, Evolution)
- Changelog now links to narrative Evolution page for context

### Rationale
The framework is comprehensive but has no production deployments. Rather than ignoring this gap, these additions address it directly: honest status assessment, retroactive alignment against real incidents, and a living record of how the framework evolves in response to real-world events. Credibility comes from transparency, not claims.

## [0.6.0] - 2026-02-08

### Changed
- **Renamed: AI Security Blueprint → Enterprise AI Security Framework**
  - Better reflects the content scope (governance, compliance, org structure)
  - "Blueprint" implied buildable artifacts; "Framework" is accurate
  - Later renamed to **AI Runtime Security** (February 2026)
  
### Added
- **implementation-guide.md** - New practical guide with working code
  - Input guardrails (regex + Bedrock + NeMo examples)
  - Output guardrails (PII, forbidden phrases, structured validation)
  - Model-as-Judge (prompts, sampling strategies, async processing)
  - Human-in-the-loop queue (Redis implementation, FastAPI endpoints)
  - Telemetry and logging (structured logs, Prometheus metrics)
  - Complete request flow example
  - Test suite templates (unit tests, red team inputs)
  - ~1,500 lines of copy-paste-ready Python

### Rationale
Reality check revealed the framework was thought leadership, not a buildable blueprint. Now there are two clear paths:
- **Implementors**: Start with implementation-guide.md (code)
- **Architects/Governance**: Use the full Framework (strategy)

## [0.5.0] - 2026-02-07

### Changed
- **Major restructure: Core + Extensions model**
- New `/core/` folder with 5 essential documents:
  - README.md - Overview and quick start
  - risk-tiers.md - Classification and control selection
  - controls.md - Guardrails, Judge, HITL combined
  - agentic.md - Agent-specific controls
  - checklist.md - Implementation tracking
- New `/extensions/` folder for reference material:
  - regulatory/ - ISO 42001, EU AI Act, banking
  - technical/ - Bypass prevention, infrastructure, metrics
  - templates/ - Playbooks, assessments
  - examples/ - Worked examples
- Root README now serves as navigation hub
- Previous detailed documents preserved in extensions

### Rationale
Framework had grown to 48 files. Core + Extensions model provides clear "start here" path (5 docs) while preserving depth for those who need it.

## [0.4.1] - 2026-02-06

### Added
- Bypass Prevention document - comprehensive guide to preventing and detecting control circumvention across 5 bypass categories (guardrails, intent, agentic, architectural, process)
- Technical Controls document - network, firewall, WAF, AI gateway, DLP, proxy, endpoint, cloud, and IAM controls for infrastructure-level enforcement
- 14 new SVG diagrams:
  - bypass-taxonomy.svg - 5 bypass categories visual
  - defence-in-depth.svg - 8-layer control stack
  - technical-controls-architecture.svg - infrastructure overview
  - ai-gateway-architecture.svg - gateway internals
  - network-zones.svg - network segmentation
  - agent-sandbox.svg - infrastructure constraints
  - action-validator-flow.svg - action validation pipeline
  - tool-output-sanitiser.svg - tool output handling
  - canary-testing.svg - control verification programme
  - dlp-inspection-points.svg - 4 DLP layers
  - casb-ai-classification.svg - sanctioned/tolerated/blocked apps
  - bypass-learning-loop.svg - continuous improvement cycle
  - infra-vs-instruction.svg - enforcement comparison
  - multi-layer-input-validation.svg - input processing pipeline

### Changed
- Updated bypass-prevention.md and technical-controls.md to reference SVG diagrams instead of ASCII art
- Clarified lifecycle scope in README - framework is operationally focused (deployment → operation → incident response), not full AI/ML lifecycle

## [0.4.0] - 2026-02-05

### Added
- AI Incident Response Playbook - 10 playbooks for AI-specific incidents
- Vendor Assessment Questionnaire - comprehensive due diligence template
- Operational Metrics document - KPIs, dashboards, alerting thresholds
- Data Retention Guidance - requirements by tier and jurisdiction
- Templates README - index of all templates
- Standard repo files: code-of-conduct.md, GOVERNANCE.md, LICENSE (MIT), SECURITY.md

### Changed
- Updated README with Templates section and new document links
- Moved "Threats" section to "Threats and Risks" with expanded content

## [0.3.0] - 2026-02-05

### Added
- Novel AI Risks document - 12 risks unique to AI systems
- Support Systems Risk document - operational risks that matter most
- Banking Cyber Risks document - top 10 banking risks through AI lens
- Feeder systems analysis with diagram
- 10 new controls: AI.3.4, AI.5.4, AI.6.4, AI.6.5, AI.7.4, AI.8.5, AI.9.5, AI.10.6, AI.13.4
- Support systems risk heat map SVG
- Banking AI feeder systems diagram SVG
- Model card template
- Reference materials (glossary, bibliography)
- Future work roadmap

### Changed
- Strengthened AI.4.2 (Testing) with statistical testing for non-determinism
- Strengthened AI.6.2 (Model Validation) with bias testing and continuous validation
- Strengthened AI.6.3 (Model Monitoring) with degradation detection
- Strengthened AI.7.1 (Input Guardrails) with semantic analysis and RAG filtering
- Strengthened AI.7.2 (Output Guardrails) with grounding checks
- Strengthened AI.7.3 (Guardrail Maintenance) with semantic adversarial testing
- Strengthened AI.8.1 (Judge Evaluation) with hallucination and override detection
- Strengthened AI.8.2 (Sampling Strategy) with baseline integration
- Strengthened AI.9.1 (HITL) with automation bias mitigation
- Strengthened AI.11.1 (Logging) with full context capture
- Strengthened AI.13.1 (Vendor Assessment) with training data practices
- Strengthened AI.14.1 (Training) with cognitive bias training
- Strengthened AG.2.3 (Scope Enforcement) with outcome boundaries
- Updated README with new documentation links

### Fixed
- XML entity escaping in SVG files (ampersand encoding)

## [0.2.0] - 2026-01-15

### Added
- Agentic Controls (AG.1-AG.4) for autonomous AI systems
- AG.2.5 Tool Protocol Security for MCP, function calling
- ISO 42001 alignment document
- EU AI Act crosswalk
- Platform integration guide (Bedrock, Databricks, Foundry)
- Control selection guide
- Tube map visualisation
- Multiple architecture diagrams

### Changed
- Expanded risk tier definitions
- Enhanced HITL model documentation
- Improved Model-as-Judge selection guidance

## [0.1.0] - 2025-12-01

### Added
- Initial framework release
- Three-layer control model (Guardrails, Judge, HITL)
- AI control families AI.1-AI.16
- Risk tiering framework (CRITICAL/HIGH/MEDIUM/LOW)
- Model-as-Judge pattern and operating model
- HITL operating model
- ISO 27001 alignment
- OWASP LLM Top 10 threat mapping
- Implementation guide
- Maturity model
- Example implementations (customer service, document assistant, credit decision)

</details>

## Categories

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes

