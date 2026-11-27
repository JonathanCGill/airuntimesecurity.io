---
title: Control Handoff Matrix
description: "A bidirectional map from pre-runtime infrastructure controls (aisecuredbydesign.io) to the runtime layers, circuit breaker, and MASO controls that enforce them at runtime (airuntimesecurity.io)."
---

# Control Handoff Matrix

Readers moving between the two sites often struggle to see how a control built *before* deployment connects to the behaviour it produces *at runtime*. This page draws that line explicitly.

- **[Secure by Design](https://aisecuredbydesign.io/)** builds the infrastructure: the sandbox, the gateway, the vault, the network zones. It decides *what* to enforce and makes enforcement possible.
- **AI Runtime Security (AIRS)** runs the behaviour: [Layer 01 Guardrails](../glossary.md#guardrails), [Layer 02 Model-as-Judge](../glossary.md#model-as-judge), [Layer 03 Human Oversight](../glossary.md#human-oversight), and the [Circuit Breaker](../glossary.md#circuit-breaker) behind them.

The mapping is **bidirectional**: read left-to-right to see what a pre-runtime control becomes at runtime; read right-to-left to see which pre-runtime infrastructure a runtime behaviour depends on. Every control ID resolves in the [machine-readable catalog](catalog/README.md) and in the [Infrastructure Controls Reference](reference.md).

!!! abstract "The one-line version"
    Pre-runtime **containment and identity** become runtime **Layer 01 guardrails**. Pre-runtime **logging and isolation** become the substrate for **Layer 02 detection**. Pre-runtime **approval workflows** become **Layer 03 human oversight**. Pre-runtime **rollback and resource limits** become the **circuit breaker** that contains what the layers cannot hold.

## How to read a row

| Column | Meaning |
|--------|---------|
| **Pre-runtime control** | The infrastructure control built on [Secure by Design](https://aisecuredbydesign.io/), with its ID |
| **Established before deploy** | What that control puts in place while the system is still being built |
| **Runtime layer** | The AIRS layer the control most directly enables once the system is live |
| **Runtime behaviour** | What actually happens at request time because the pre-runtime control exists |

## Containment and execution → Layer 01 + Circuit Breaker

| Pre-runtime control | Established before deploy | Runtime layer | Runtime behaviour |
|---------------------|---------------------------|---------------|-------------------|
| **SAND-01** Isolated sandboxes | A micro-VM / gVisor boundary around agent-generated code | [Layer 01](../glossary.md#guardrails) + [Circuit Breaker](../glossary.md#circuit-breaker) | Untrusted code executes inside the boundary; a breakout or overrun trips the breaker and kills the session |
| **SAND-04** Resource limits | CPU / memory / disk ceilings on the sandbox | [Circuit Breaker](../glossary.md#circuit-breaker) | A runaway or fork-bombing agent hits the ceiling and is contained rather than exhausting the host |
| **NET-02** No guardrail-bypass path | Network topology with no route to the model that skips guardrails | [Layer 01](../glossary.md#guardrails) | Every request is forced through the guardrail path; there is no side door at runtime |
| **NET-04** Agent egress control | An egress proxy with a default-deny allowlist | [Layer 01](../glossary.md#guardrails) | Agent calls to non-allowlisted hosts are blocked in-line, closing the exfiltration and SSRF path |

## Identity, tools, and delegation → Layer 01

| Pre-runtime control | Established before deploy | Runtime layer | Runtime behaviour |
|---------------------|---------------------------|---------------|-------------------|
| **IAM-01 / IAM-02** Authenticate, least privilege | Every entity has a verified identity and a minimal permission set | [Layer 01](../glossary.md#guardrails) | Unauthenticated or over-scoped calls are refused at the gateway before reaching the model |
| **TOOL-01 / TOOL-02** Tool manifest, gateway enforcement | A declared, allowlisted tool manifest enforced at the gateway | [Layer 01](../glossary.md#guardrails) | Any tool call outside the manifest is denied deterministically, not left to the agent's discretion |
| **SEC-02 / IAM-06** Short-lived, session-scoped tokens | A token issuer that mints scoped, expiring credentials | [Layer 01](../glossary.md#guardrails) | Tokens that are expired, wildcard-scoped, or unbound to the session are rejected before the call proceeds |
| **DEL-01 / DEL-05** Least delegation, identity propagation | A delegation model that intersects permissions and carries the originating principal | [Layer 01](../glossary.md#guardrails) + [MASO](../maso/README.md) | A worker agent cannot exceed the orchestrator's grant; every action stays attributable to the initiating human |

## Observation and detection → Layer 02

| Pre-runtime control | Established before deploy | Runtime layer | Runtime behaviour |
|---------------------|---------------------------|---------------|-------------------|
| **LOG-01** Log model I/O | A tamper-evident log pipeline for every prompt and response | [Layer 02](../glossary.md#model-as-judge) | The Judge has the raw I/O it needs to evaluate outputs against policy |
| **LOG-04** Log agent decision chains | Structured chain-of-action logging across agents | [Layer 02](../glossary.md#model-as-judge) | Process-aware evaluation can reconstruct what a multi-step agent did and judge whether it was appropriate |
| **NET-03** Isolate Judge infrastructure | A separate network zone for the evaluation stack | [Layer 02](../glossary.md#model-as-judge) | The Judge evaluates independently; the runtime path cannot influence or silence it |
| **LOG-05** Detect behavioural drift | A baseline and drift-detection pipeline | [Layer 02](../glossary.md#model-as-judge) → [Layer 03](../glossary.md#human-oversight) | Drift outside baseline raises a signal that escalates to human review |

## Decision and accountability → Layer 03

| Pre-runtime control | Established before deploy | Runtime layer | Runtime behaviour |
|---------------------|---------------------------|---------------|-------------------|
| **IAM-05** Human approval for high-impact actions | An approval-routing workflow for irreversible actions | [Layer 03](../glossary.md#human-oversight) | High-consequence actions (transfers, deletions) pause for a human decision before they commit |
| **TOOL-04** Classify actions by reversibility | An action-impact classification on every tool | [Layer 03](../glossary.md#human-oversight) | Irreversible actions are routed to oversight; reversible ones proceed, so humans are spent where it matters |
| **SUP-02 / SUP-07** Model risk assessment, AI-BOM | An adoption decision and a component inventory | [Layer 03](../glossary.md#human-oversight) | Humans retain a defensible record of what is deployed and why it was approved |

## Recovery and containment → Circuit Breaker

| Pre-runtime control | Established before deploy | Runtime layer | Runtime behaviour |
|---------------------|---------------------------|---------------|-------------------|
| **IR-04** Model rollback and guardrail hot-reload | A rollback mechanism and hot-reloadable policy | [Circuit Breaker](../glossary.md#circuit-breaker) | A bad model or policy is reverted in place without redeploying the whole system ([PACE](../glossary.md#pace) Emergency) |
| **IR-03** Containment procedures | Pre-defined containment runbooks and kill switches | [Circuit Breaker](../glossary.md#circuit-breaker) | On a confirmed incident the system routes to a non-AI fallback path rather than continuing to serve |
| **SEC-05** Rotate credentials on exposure | Automated rotation triggers | [Circuit Breaker](../glossary.md#circuit-breaker) | Exposed credentials are invalidated automatically, shrinking the window of a compromise |

## Reading it the other way

If you start from a runtime layer and want to know what pre-runtime infrastructure it needs:

| Runtime layer | Depends on pre-runtime controls |
|---------------|--------------------------------|
| [Layer 01 Guardrails](../glossary.md#guardrails) | NET-01/02/04/07, IAM-01/02/04, TOOL-01/02/03/07, SEC-01/02, SAND-01/02/03/07, SESS-06, SUP-09 |
| [Layer 02 Model-as-Judge](../glossary.md#model-as-judge) | LOG-01/03/04/05, NET-03, DAT-08 |
| [Layer 03 Human Oversight](../glossary.md#human-oversight) | IAM-05/08, TOOL-04, LOG-10, IR-01/05/06, SUP-10 |
| [Circuit Breaker](../glossary.md#circuit-breaker) | IR-03/04, SAND-04/05, SEC-05, SESS-05 |

!!! tip "Use the catalog to generate your own view"
    Each control in [`controls.json`](catalog/controls.json) carries a `primary_runtime_layer_code` field (`L1`, `L2`, `L3`, `CB`). Filter on it to build a handoff view scoped to your own control set, or to check coverage of a given layer.

!!! info "References"
    - [The Architecture](../architecture.md)
    - [Infrastructure Controls Reference](reference.md)
    - [Machine-Readable Control Catalog](catalog/README.md)
    - [Glossary and Unified Taxonomy](../glossary.md)
    - [Secure by Design: Infrastructure Controls (aisecuredbydesign.io)](https://aisecuredbydesign.io/infrastructure/)
