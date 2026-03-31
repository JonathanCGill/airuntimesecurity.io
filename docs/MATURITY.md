# Maturity & Validation

**An honest assessment of what this reference is, what it's validated against, and where the gaps are.**

> Part of [AI Runtime Security](./)
> Last updated: February 2026

## Status

This reference has **not been deployed end-to-end in a production environment.** No organisation has implemented the full control set and reported back on operational results. The adopters list is empty.

That's an important fact and we're stating it clearly rather than hoping no one notices.

What this reference *is*:

- **A practitioner's synthesis.** 30+ years in IT, 20+ in enterprise security, applied to the specific problem of runtime AI security. The architecture draws on real operational experience in financial services, government, and critical infrastructure - applied to AI, not invented from theory.
- **Aligned to real incidents.** Every major control addresses a documented, public security failure - retroactively analysed, not empirically tested. The [Incident Tracker](maso/threat-intelligence/incident-tracker.md) maps known real-world incidents to specific controls, with [risk stories](insights/risk-stories.md) documenting production failures across industries. The [Validated Against Real Incidents](VALIDATED-AGAINST.md) page inverts this - showing which controls align to the most documented incidents.
- **Aligned to established standards.** Full crosswalks to OWASP LLM Top 10 (2025), OWASP Agentic Top 10 (2026), NIST AI RMF, ISO 42001, EU AI Act, NIST SP 800-218A, and MITRE ATLAS. These aren't surface-level mappings - they're control-by-control alignments.
- **Consistent with production patterns.** The three-layer model (Guardrails, Judge, Human Oversight) exists in production at NVIDIA NeMo, AWS Bedrock, Azure AI Content Safety, LangChain, and Guardrails AI. This reference didn't invent the pattern - it codified it.

What this reference *is not*:

- **Not battle-tested at scale.** No one has run this at 100K+ daily interactions and reported back on false positive rates, Judge accuracy, operational overhead, or PACE failover performance.
- **Not a certification or audit standard.** Implementing this does not constitute compliance with any regulation. It may support compliance - the regulatory crosswalks show how - but that's your assessment to make, not ours.
- **Not complete.** Several control domains are explicitly marked as emerging: multimodal, reasoning models, streaming, epistemic risk detection. These are well-articulated but lack the operational depth of the core three-layer pattern.

## Validation Layers

We distinguish between four types of validation, ordered by strength:

### 1. Production Validation (Strongest)

Controls proven effective through real-world deployment and operational measurement.

**Current status: None.** No organisation has reported production deployment results.

**What would change this:** An organisation implements the framework (or a subset), operates it for 90+ days, and shares operational metrics - false positive rates, Judge accuracy, PACE failover performance, cost per interaction, incidents detected. Even anonymised or aggregated data would be valuable.

### 2. Incident Validation

Controls retroactively mapped to real-world security incidents, showing they would have prevented or detected the failure.

**Current status: Known incidents mapped in the tracker, with additional coverage across the framework.** Each tracked incident includes the specific attack vector, the controls that address it, and a confidence rating for the mapping. The [risk stories](insights/risk-stories.md) provide additional production failure evidence mapped to framework controls.

See: [Validated Against Real Incidents](VALIDATED-AGAINST.md)

This is the strongest current basis for credibility - but it is retroactive analysis, not empirical evidence from running systems. It demonstrates the controls address real attack patterns, not theoretical ones. It does not prove the controls *will* work in your environment.

### 3. Standards Alignment

Controls mapped to established international standards and industry frameworks.

**Current status: 8 standards mapped.** Full crosswalks with control-level alignment.

| Standard | Mapping Depth |
|----------|--------------|
| OWASP LLM Top 10 (2025) | Control-by-control across foundation + MASO |
| OWASP Agentic Top 10 (2026) | Control-by-control in MASO |
| NIST AI RMF | Govern, Map, Measure, Manage functions |
| ISO 42001 | Annex A clause-level alignment |
| ISO 27001 | Information security control mapping |
| EU AI Act | Articles 9, 14, 15 alignment |
| NIST SP 800-218A | Pre-deployment complement |
| MITRE ATLAS | Agent threat intelligence alignment |

Standards alignment doesn't validate effectiveness - it validates *relevance*. These mappings show the reference addresses the same risk categories that international bodies have independently identified as critical.

### 4. Pattern Consistency

The architectural patterns used in this framework exist independently in production systems from multiple vendors.

| Pattern | Production Evidence |
|---------|-------------------|
| Input/output guardrails | NVIDIA NeMo, AWS Bedrock, Azure AI, Guardrails AI |
| Model-as-Judge evaluation | DeepEval, Galileo, LangSmith, custom implementations |
| Human-in-the-loop review | LangChain HITL, custom queue systems |
| Circuit breaker / kill switch | Standard resilience pattern (Netflix Hystrix lineage) |
| Agent sandboxing | Docker/gVisor patterns in LangGraph, CrewAI |
| Non-Human Identity | Service account patterns extended to agents |

Pattern consistency doesn't prove this reference's *specific implementation* works - but it demonstrates the architectural approach is sound and independently adopted.

## Known Gaps

We track what we know we don't know.

| Gap | Status | Impact |
|-----|--------|--------|
| **Production metrics at scale** | No data on false positive rates, latency, cost at >100K interactions/day | Can't quantify operational overhead |
| **Judge accuracy baselines** | Analysis of failure modes exists ([When the Judge Can Be Fooled](core/when-the-judge-can-be-fooled.md)) but no published accuracy benchmarks | Can't specify expected detection rates |
| **PACE failover performance** | Failure scenarios are designed and documented; none have been tested under real incident conditions | Failover timing and reliability unproven |
| **Epistemic risk detection** | Six risk categories identified (groupthink, hallucination amplification, correlated errors, semantic drift, uncertainty stripping, synthetic corroboration); no algorithmic detection published | Detection thresholds are theoretical |
| **Kill switch architecture** | Identified as critical for MASO Tier 3; detailed implementation patterns still emerging | Preferred pattern for agent-to-human emergency communication unclear |
| **Supply chain vetting automation** | AIBOM and MCP vetting controls specified; enterprise tooling not yet mature | Manual review still required for novel components |
| **RAG poisoning detection** | Controls are mostly preventive (integrity checks, provenance); detective controls (finding poisoned data already in corpus) are limited | Retrospective detection weak |

## How You Can Help

### Pilot It

The single most valuable thing for this reference's credibility is a real deployment. If your organisation is implementing AI security controls - even partially - and would be willing to share results (anonymised is fine), we want to hear from you.

What a pilot looks like:

1. **Pick a scope.** One AI system, one risk tier. You don't need the whole framework.
2. **Implement the controls.** Use the [Quick Start](QUICK_START.md) or [Implementation Guide](IMPLEMENTATION_GUIDE.md).
3. **Measure.** Track false positive rates, Judge accuracy, latency impact, operational overhead.
4. **Share.** Open an issue or contact the maintainer directly.

Even negative results are valuable. "We implemented X and it didn't work because Y" improves the framework more than silence.

### Peer Review

If you're an AI security practitioner, red teamer, or compliance professional - review the reference and tell us what's wrong, what's missing, or what doesn't match your experience. Open an issue or submit a PR.

Specific areas where expert review would be most valuable:

- **Judge accuracy** - Have you measured Model-as-Judge performance in production? What accuracy ranges are realistic?
- **Epistemic controls** - Are the six epistemic risk categories we've identified complete? Are there others?
- **PACE resilience** - Have you implemented structured failover for AI systems? What worked?
- **Multi-agent security** - Are the MASO control domains the right decomposition? What's missing?

### Report Incidents

If you're aware of a public AI security incident not in our [Incident Tracker](maso/threat-intelligence/incident-tracker.md), open an issue. We'll map it to controls and add it to the evidence base.

## A Note on Honesty

This section exists because too much guidance presents itself as established when it's theoretical, proven when it's proposed, and comprehensive when it's partial.

We'd rather be honest about where this reference stands and let you judge whether it's useful in its current state, than pretend it has an evidence base it doesn't.

The architecture is sound - the patterns exist independently in production. The controls are grounded - they address real incidents. The standards alignment is thorough. What's missing is the operational proof that comes only from real deployment.

Help us close that gap.

