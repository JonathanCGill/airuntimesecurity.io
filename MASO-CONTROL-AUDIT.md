# MASO Control Catalogue — Audit / Trim List

**As-at: 2026-11-13.** Point-in-time snapshot. Verify current requirements against official sources before relying on this.

Working document. Every defined control ID with its title, grouped by the eleven domains.
Trim entries that are sub-controls rather than top-level controls, then the headline number follows from the count.

_Not part of the published site (lives outside `docs/`)._
| Domain | Prefix | Count |
|---|---|--:|
| Identity & Access | IA | 25 |
| Data Protection | DP | 15 |
| Extraction Integrity | EI | 15 |
| Execution Control | EC | 36 |
| Observability | OB | 17 |
| Prompt, Goal & Epistemic Integrity | PG | 24 |
| Supply Chain | SC | 22 |
| Objective Intent | OI | 18 |
| Privileged Agent Governance | PA | 19 |
| Model Cognition Assurance | MC | 21 |
| Agentic Task Mandate | AT | 26 |
| **Core total (11 domains)** | | **238** |
| Environment Containment (cross-cutting) | ENV | 24 |
| **With ENV** | | **262** |

## Summary


## Identity & Access (IA) — 25

- [ ] **IA-1.1** Agent identifier
- [ ] **IA-1.2** No shared credentials
- [ ] **IA-1.3** No orchestrator inheritance
- [ ] **IA-1.4** Scoped permissions
- [ ] **IA-1.5** Managed secret storage
- [ ] **IA-1.6** No secrets in MCP client configuration
- [ ] **IA-1.7** No credential-bearing tool interfaces
- [ ] **IA-2.1** Non-Human Identity (NHI)
- [ ] **IA-2.2** Short-lived credentials
- [ ] **IA-2.3** Mutual authentication
- [ ] **IA-2.4** No transitive permissions
- [ ] **IA-2.5** Orchestrator privilege separation
- [ ] **IA-2.6** Secrets exclusion from context
- [ ] **IA-2.7** Vaulted per-flow credential brokering
- [ ] **IA-2.8** Tool-boundary secret injection
- [ ] **IA-2.9** Secret redaction at ingress and persistence
- [ ] **IA-2.10** MCP server credential custody
- [ ] **IA-2.11** No MCP token passthrough
- [ ] **IA-3.1** Sub-hour rotation (all)
- [ ] **IA-3.2** Behavioral binding
- [ ] **IA-3.3** Delegation mandates
- [ ] **IA-3.4** Automated credential revocation
- [ ] **IA-3.5** Sender-constrained tokens
- [ ] **IA-3.6** Canary credentials
- [ ] **IA-3.7** Secret access correlation

## Data Protection (DP) — 15

- [ ] **DP-1.1** Data classification
- [ ] **DP-1.2** Logical separation
- [ ] **DP-1.3** Output logging
- [ ] **DP-1.4** RAG inventory
- [ ] **DP-1.5** Data flow diagram
- [ ] **DP-1.6** Classification metadata propagation
- [ ] **DP-2.1** DLP on message bus
- [ ] **DP-2.2** RAG integrity and freshness validation
- [ ] **DP-2.3** Infrastructure data fencing
- [ ] **DP-2.4** Memory isolation
- [ ] **DP-2.5** Derived data reclassification
- [ ] **DP-3.1** Real-time RAG integrity
- [ ] **DP-3.2** Memory decay
- [ ] **DP-3.3** Cross-session memory analysis
- [ ] **DP-3.4** Data provenance chain

## Extraction Integrity (EI) — 15

- [ ] **EI-1.1** Field-level risk classification
- [ ] **EI-1.2** Per-field confidence scores
- [ ] **EI-1.3** Extraction provenance record
- [ ] **EI-1.4** Human validation on critical fields
- [ ] **EI-1.5** Pre-extraction document checks
- [ ] **EI-2.1** Confidence thresholds by field class
- [ ] **EI-2.2** Authoritative source cross-referencing
- [ ] **EI-2.3** Mismatch halt and route
- [ ] **EI-2.4** Adversarial input detection
- [ ] **EI-2.5** Confidence propagation on the message bus
- [ ] **EI-2.6** Cumulative uncertainty enforcement
- [ ] **EI-3.1** Real-time authoritative cross-check at decision point
- [ ] **EI-3.2** Independent dual extraction for critical fields
- [ ] **EI-3.3** Field-level reconstructability
- [ ] **EI-3.4** Synthetic document detection

## Execution Control (EC) — 36

- [ ] **EC-1.1** Human approval gate
- [ ] **EC-1.2** Tool allow-lists
- [ ] **EC-1.3** Per-agent rate limits
- [ ] **EC-1.4** Read auto-approval
- [ ] **EC-1.5** Interaction timeout
- [ ] **EC-1.6** Reversibility assessment
- [ ] **EC-1.7** Agent health check
- [ ] **EC-1.8** Output format verification
- [ ] **EC-1.9** Token budget monitoring
- [ ] **EC-1.10** Retry budget caps
- [ ] **EC-2.1** Action classification
- [ ] **EC-2.2** Sandboxed execution
- [ ] **EC-2.3** Blast radius caps
- [ ] **EC-2.4** Circuit breakers
- [ ] **EC-2.5** Model-as-Judge gate
- [ ] **EC-2.6** Decision commit protocol
- [ ] **EC-2.7** Aggregate harm assessment
- [ ] **EC-2.8** Tool completion attestation
- [ ] **EC-2.9** Latency SLOs and oversight SLA enforcement
- [ ] **EC-2.10** Agent failover
- [ ] **EC-2.11** Chain reversibility assessment
- [ ] **EC-2.12** Multimodal boundary validation
- [ ] **EC-2.13** Output schema enforcement
- [ ] **EC-2.14** Inter-agent data contracts
- [ ] **EC-2.15** Serialisation boundary validation
- [ ] **EC-2.16** Context rotation with structured state preservation
- [ ] **EC-2.17** Judge context isolation
- [ ] **EC-2.18** Egress path validation
- [ ] **EC-2.19** Config-file immutability
- [ ] **EC-2.20** Scenario and content egress validation
- [ ] **EC-3.1** Infrastructure-enforced blast radius
- [ ] **EC-3.2** Self-healing circuit breakers
- [ ] **EC-3.3** Multi-model cross-validation
- [ ] **EC-3.4** Time-boxing
- [ ] **EC-3.5** Automated rollback scope
- [ ] **EC-3.6** Transformation integrity chain

## Observability (OB) — 17

- [ ] **OB-1.1** Action audit log
- [ ] **OB-1.2** Inter-agent message log
- [ ] **OB-1.3** Weekly manual review
- [ ] **OB-1.4** Output quality log
- [ ] **OB-2.1** Immutable decision chain
- [ ] **OB-2.2** Continuous anomaly scoring
- [ ] **OB-2.3** Drift detection
- [ ] **OB-2.4** SIEM/SOAR integration
- [ ] **OB-2.5** Cost and consumption monitoring
- [ ] **OB-2.6** Log security
- [ ] **OB-2.7** Accountable human
- [ ] **OB-2.8** Emergent failure accountability
- [ ] **OB-3.1** Long-window behavioral analysis
- [ ] **OB-3.2** Causal chain reconstruction
- [ ] **OB-3.3** Independent observability agent
- [ ] **OB-3.4** Cross-agent correlation
- [ ] **OB-3.5** Decision traceability

## Prompt, Goal & Epistemic Integrity (PG) — 24

- [ ] **PG-1.1** Input sanitisation per agent
- [ ] **PG-1.2** System prompt isolation
- [ ] **PG-1.3** Immutable task specification
- [ ] **PG-1.4** Message source tagging
- [ ] **PG-1.5** Anti-manipulation guardrail
- [ ] **PG-1.6** Task clarity threshold
- [ ] **PG-2.1** Inter-agent injection detection
- [ ] **PG-2.2** Goal integrity monitoring
- [ ] **PG-2.3** System prompt boundary enforcement
- [ ] **PG-2.4** Consensus diversity gate
- [ ] **PG-2.5** Claim provenance enforcement
- [ ] **PG-2.6** Self-referential evidence prohibition
- [ ] **PG-2.7** Uncertainty preservation
- [ ] **PG-2.8** Assumption isolation
- [ ] **PG-2.9** Model diversity policy
- [ ] **PG-2.10** Inter-agent clarification protocol
- [ ] **PG-2.11** Assembled-context evaluation
- [ ] **PG-2.12** Control-reasoning non-disclosure
- [ ] **PG-3.1** Multi-layer injection defence
- [ ] **PG-3.2** Goal integrity hash chain
- [ ] **PG-3.3** Constraint fidelity check
- [ ] **PG-3.4** Plan-execution conformance
- [ ] **PG-3.5** Challenger agent
- [ ] **PG-3.6** Prompt leakage red team

## Supply Chain (SC) — 22

- [ ] **SC-1.1** Model inventory
- [ ] **SC-1.2** Tool inventory
- [ ] **SC-1.3** Fixed toolsets
- [ ] **SC-1.4** RAG source inventory
- [ ] **SC-1.5** Skill inventory and installation control
- [ ] **SC-1.6** Agent Skills format conformance
- [ ] **SC-2.1** AIBOM per agent
- [ ] **SC-2.2** Signed tool manifests
- [ ] **SC-2.3** MCP server allow-listing
- [ ] **SC-2.4** Runtime integrity checks
- [ ] **SC-2.5** Skill definition validation
- [ ] **SC-2.6** Per-skill permission manifest
- [ ] **SC-2.7** External instruction pinning
- [ ] **SC-2.8** Skill version and source pinning
- [ ] **SC-2.9** Skill secret hygiene
- [ ] **SC-2.10** Skill invocation-time execution
- [ ] **SC-3.1** Model version pinning
- [ ] **SC-3.2** Automated rollback
- [ ] **SC-3.3** Continuous dependency scanning
- [ ] **SC-3.4** A2A trust chain validation
- [ ] **SC-3.5** CI/CD pipeline integrity
- [ ] **SC-3.6** Behavioural skill evaluation

## Objective Intent (OI) — 18

- [ ] **OI-1.1** Agent OISpec declaration
- [ ] **OI-1.2** Workflow OISpec declaration
- [ ] **OI-1.3** OISpec immutability
- [ ] **OI-1.4** Manual intent review
- [ ] **OI-1.5** Intent coverage check
- [ ] **OI-2.1** Automated tactical evaluation
- [ ] **OI-2.2** Automated strategic evaluation
- [ ] **OI-2.3** Judge OISpec declaration
- [ ] **OI-2.4** Judge intent monitoring
- [ ] **OI-2.5** OISpec violation escalation
- [ ] **OI-2.6** Intent alignment scoring
- [ ] **OI-2.7** Combined action evaluation
- [ ] **OI-3.1** Continuous intent compliance
- [ ] **OI-3.2** Predictive intent analysis
- [ ] **OI-3.3** Cross-workflow intent learning
- [ ] **OI-3.4** Judge rotation with intent continuity
- [ ] **OI-3.5** Adversarial intent testing
- [ ] **OI-3.6** Intent decomposition validation

## Privileged Agent Governance (PA) — 19

- [ ] **PA-1.1** Role declaration
- [ ] **PA-1.2** Orchestrator plan logging
- [ ] **PA-1.3** Judge decision logging
- [ ] **PA-1.4** Privileged agent inventory
- [ ] **PA-2.1** Orchestrator intent verification
- [ ] **PA-2.2** Judge calibration testing
- [ ] **PA-2.3** Judge criteria versioning
- [ ] **PA-2.4** Judge disagreement protocol
- [ ] **PA-2.5** Observer precision monitoring
- [ ] **PA-2.6** Kill switch dual authorisation
- [ ] **PA-2.7** Orchestrator behavioral baseline
- [ ] **PA-2.8** Privileged agent red team
- [ ] **PA-3.1** Orchestrator output evaluation
- [ ] **PA-3.2** Nested orchestration scoping
- [ ] **PA-3.3** Sub-tree blast radius
- [ ] **PA-3.4** Model-as-Judge rotation
- [ ] **PA-3.5** Continuous calibration
- [ ] **PA-3.6** Observer self-test
- [ ] **PA-3.7** Cross-level evaluation

## Model Cognition Assurance (MC) — 21

- [ ] **MC-1.1** Interpretability attestation inventory
- [ ] **MC-1.2** Internal behaviour disclosure log
- [ ] **MC-1.3** Interpretability access classification
- [ ] **MC-1.4** Emotion probe evidence request
- [ ] **MC-1.5** CoT logging and review
- [ ] **MC-1.6** Task completion verification
- [ ] **MC-2.1** Interpretability evidence review
- [ ] **MC-2.2** Alignment-relevant behaviour disclosure
- [ ] **MC-2.3** Adversarial CoT consistency testing
- [ ] **MC-2.4** CoT sufficiency classification
- [ ] **MC-2.5** Behavioural baseline for reward hacking
- [ ] **MC-2.6** Reward hacking anomaly detection
- [ ] **MC-2.7** Third-party activation-layer residual risk
- [ ] **MC-2.8** Vendor interpretability attestation
- [ ] **MC-2.9** Material finding disclosure obligation
- [ ] **MC-2.10** Alignment incident notification
- [ ] **MC-3.1** Independent activation-layer validation
- [ ] **MC-3.2** Activation-CoT correlation
- [ ] **MC-3.3** Adversarial reward hacking red team
- [ ] **MC-3.4** Residual risk quantification
- [ ] **MC-3.5** Independent vendor audit rights

## Agentic Task Mandate (AT) — 26

- [ ] **AT-1.1** Solution mandate declaration
- [ ] **AT-1.2** Agent mandate declaration
- [ ] **AT-1.3** Mandate library and version control
- [ ] **AT-1.4** Tool allow-list enforcement
- [ ] **AT-1.5** Execution trace logging
- [ ] **AT-1.6** Plan attempt logging
- [ ] **AT-1.7** Hard stop conditions
- [ ] **AT-2.1** Mandate inheritance enforcement
- [ ] **AT-2.2** Mandate review cycle
- [ ] **AT-2.3** Least privilege tool provisioning
- [ ] **AT-2.4** Execution sequence enforcement
- [ ] **AT-2.5** Idempotency requirement
- [ ] **AT-2.6** Four-state deviation classification
- [ ] **AT-2.7** Creative substitution detection
- [ ] **AT-2.8** Plan attempt trend analysis
- [ ] **AT-2.9** Mandate escalation path enforcement
- [ ] **AT-2.10** Soft escalation and mandate amendment
- [ ] **AT-2.11** Anti-Mythos judge deployment
- [ ] **AT-2.12** Judge mandate
- [ ] **AT-2.13** Judge verdict schema
- [ ] **AT-2.14** Vendor agentic capability disclosure
- [ ] **AT-2.15** Activation-layer residual risk declaration
- [ ] **AT-2.16** Mandate-environment reconciliation
- [ ] **AT-3.1** Cross-session drift detection
- [ ] **AT-3.2** Judge evaluation scope
- [ ] **AT-3.3** Judge independence

## (Cross-cutting) Environment Containment (ENV) — 24

- [ ] **ENV-1** Strict input validation
- [ ] **ENV-2** Schema-first design
- [ ] **ENV-3** Allowlist over denylist
- [ ] **ENV-4** Request-scoped authorization
- [ ] **ENV-5** Binary success/failure
- [ ] **ENV-6** No stack traces or internal state
- [ ] **ENV-7** Separate diagnostic logging
- [ ] **ENV-8** Stored procedures only
- [ ] **ENV-9** Parameterized queries
- [ ] **ENV-10** Row-level security
- [ ] **ENV-11** Database-level constraints
- [ ] **ENV-12** Read replicas for read-heavy agents
- [ ] **ENV-13** System prompt no-retry directive
- [ ] **ENV-14** Server-side retry blocking
- [ ] **ENV-15** Retry budget at gateway
- [ ] **ENV-16** DLP on all agent-accessible channels
- [ ] **ENV-17** Fraud detection on agent transactions
- [ ] **ENV-18** WAF on agent-facing APIs
- [ ] **ENV-19** SIEM correlation
- [ ] **ENV-20** Network segmentation
- [ ] **ENV-21** Infrastructure kill switch
- [ ] **ENV-22** Automated kill switch triggers
- [ ] **ENV-23** Kill switch independence
- [ ] **ENV-24** Post-kill forensics

## Proportionality (why the total is a ceiling, not a requirement)

Controls are numbered by tier: X-1.n = Tier 1 (Supervised), X-2.n = Tier 2 (Managed), X-3.n = Tier 3 (Autonomous). Each tier is cumulative.

| Tier | Adds | Cumulative |
|---|--:|--:|
| Tier 1 (Supervised) | 66 | 66 |
| Tier 2 (Managed) | 113 | 179 |
| Tier 3 (Autonomous) | 59 | 238 |

A Tier 1 deployment applies 66 controls, not 238. The full catalogue is the Tier-3 maximum.
