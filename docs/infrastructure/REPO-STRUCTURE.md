# AI Security Infrastructure Controls - Repo Structure

> Complements [AI Runtime Security](https://github.com/JonathanCGill/airuntimesecurity.io), which defines the *behavioral* security pattern (Guardrails → Model-as-Judge → Human Oversight). This repo defines the *infrastructure* controls that make that pattern enforceable.

## Repo Layout

```
ai-security-infrastructure-controls/
│
├── README.md                          # Overview, control inventory, architecture
├── REPO-STRUCTURE.md                  # This file
├── LICENSE                            # MIT
│
├── controls/
│   ├── identity-and-access.md         # IAM-01 to IAM-08 (8 controls)
│   ├── logging-and-observability.md   # LOG-01 to LOG-10 (10 controls)
│   ├── network-and-segmentation.md    # NET-01 to NET-08 (8 controls)
│   ├── data-protection.md             # DAT-01 to DAT-08 (8 controls)
│   ├── secrets-and-credentials.md     # SEC-01 to SEC-08 (8 controls)
│   ├── supply-chain.md                # SUP-01 to SUP-08 (8 controls)
│   └── incident-response.md           # IR-01 to IR-08 (8 controls)
│
├── agentic/
│   ├── tool-access-controls.md        # TOOL-01 to TOOL-06 (6 controls)
│   ├── session-and-scope.md           # SESS-01 to SESS-05 (5 controls)
│   ├── delegation-chains.md           # DEL-01 to DEL-05 (5 controls)
│   └── sandbox-patterns.md            # SAND-01 to SAND-06 (6 controls)
│
├── diagrams/
│   ├── iam-control-layers.svg         # IAM architecture for AI systems
│   ├── iam-identity-chain.svg         # Identity chain: user → app → model → agent → tool
│   ├── iam-auth-gateway-flow.svg      # Authorization gateway decision flow
│   ├── iam-approval-flow.svg          # Human approval routing for high-impact actions
│   ├── logging-architecture.svg       # Logging pipeline and detection points
│   ├── agent-chain-reconstruction.svg # Agent decision chain forensic reconstruction
│   ├── relationship-to-parent.svg     # How this repo relates to the parent framework
│   ├── network-zones.svg              # Six-zone network architecture
│   ├── guardrail-bypass-prevention.svg # Correct vs blocked paths to model
│   ├── agent-egress-proxy.svg         # Agent egress proxy enforcement flow
│   ├── data-classification-points.svg # Data classification at AI pipeline boundaries
│   ├── credential-isolation.svg       # Out-of-band credential injection architecture
│   ├── incident-classification.svg    # AI incident severity taxonomy
│   └── delegation-permissions.svg     # Permission intersection model for delegation
│
├── mappings/
│   ├── controls-to-three-layers.md    # All 80 controls × Guardrails/Judge/Human
│   ├── iso42001-annex-a.md            # ISO 42001 Annex A mapping
│   ├── nist-ai-rmf.md                 # NIST AI RMF mapping (51 subcategories)
│   └── owasp-llm-top10.md            # OWASP LLM Top 10 + Agentic Top 10 mapping
│
└── reference/
    └── platform-patterns/
        ├── aws-bedrock.md             # AWS Bedrock implementation patterns
        ├── microsoft-foundry.md        # Microsoft Foundry implementation patterns
        └── databricks.md              # Databricks implementation patterns
```

## Control Inventory

| Domain | File | Controls | IDs |
|--------|------|----------|-----|
| Identity & Access | `controls/identity-and-access.md` | 8 | IAM-01 to IAM-08 |
| Logging & Observability | `controls/logging-and-observability.md` | 10 | LOG-01 to LOG-10 |
| Network & Segmentation | `controls/network-and-segmentation.md` | 8 | NET-01 to NET-08 |
| Data Protection | `controls/data-protection.md` | 8 | DAT-01 to DAT-08 |
| Secrets & Credentials | `controls/secrets-and-credentials.md` | 8 | SEC-01 to SEC-08 |
| Supply Chain | `controls/supply-chain.md` | 8 | SUP-01 to SUP-08 |
| Incident Response | `controls/incident-response.md` | 8 | IR-01 to IR-08 |
| Tool Access | `agentic/tool-access-controls.md` | 6 | TOOL-01 to TOOL-06 |
| Session & Scope | `agentic/session-and-scope.md` | 5 | SESS-01 to SESS-05 |
| Delegation Chains | `agentic/delegation-chains.md` | 5 | DEL-01 to DEL-05 |
| Sandbox Patterns | `agentic/sandbox-patterns.md` | 6 | SAND-01 to SAND-06 |
| **Total** | **11 files** | **80** | |

## Design Principles

1. **Vendor-neutral first.** Platform-specific guidance lives in `reference/platform-patterns/`, never in the core control definitions.
2. **Three-layer alignment.** Every technical control maps back to how it enables or strengthens the Guardrails → Judge → Human Oversight pattern.
3. **Risk-tiered.** Controls specify which risk tiers (from the parent framework) they apply to, so implementers can right-size.
4. **Practitioner audience.** Written for security architects and engineers who will implement these controls. Not executive summaries.
5. **Agentic AI treated separately.** Agentic systems introduce trust delegation, tool invocation, and autonomous action - these deserve their own control domain.
6. **Infrastructure beats instructions.** Security controls enforced via deterministic infrastructure (gateways, network policy, vaults), never via prompt instructions.

## Implementation Sequence

| Phase | Control Domain | Rationale |
|-------|---------------|-----------|
| 1 | Identity & Access | Without IAM, nothing else is enforceable |
| 2 | Logging & Observability | You can't detect what you can't see |
| 3 | Network & Segmentation | Reduce blast radius, enforce zone boundaries |
| 4 | Data Protection | PII, model I/O, context window data flows |
| 5 | Secrets & Credentials | API keys, tokens, vault patterns |
| 6 | Supply Chain | Model provenance, dependency integrity, AI-BOM |
| 7 | Incident Response | AI-specific IR extending enterprise processes |

Agentic controls (TOOL, SESS, DEL, SAND) are implemented in parallel with the relevant phase when agentic systems are in scope.

## Relationship to Parent Framework

The parent framework ([airuntimesecurity.io](https://github.com/JonathanCGill/airuntimesecurity.io)) defines the behavioral pattern:

- **What** to enforce (Guardrails prevent, Judge detects, Humans decide)
- **Why** it's necessary (non-determinism, emergent behavior, adversarial inputs)
- **When** to apply controls (risk tier classification)

This repo defines:

- **How** to enforce it at the infrastructure level (80 technical controls)
- **Where** the boundaries are (network zones, identity chains, data flows)
- **Which platforms** implement it (AWS, Azure, Databricks patterns)

The parent framework answers *what*. This repo answers *how*.

