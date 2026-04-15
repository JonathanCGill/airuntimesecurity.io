---
description: Deep technical references on AI control implementation, judge model selection, anomaly detection, RAG security, and SOC integration.
---

# Technical Reference

Deep dives on controls, infrastructure, operations, and metrics. Grouped by purpose so you can find the page you need without scanning the whole list.

## Judge Internals

Building, selecting, validating, and operating the judge model.

| Document | Description |
|----------|-------------|
| [Model-as-Judge Implementation](model-as-judge-implementation.md) | Detailed judge implementation, including prompt structure and scoring. |
| [Judge Model Selection](judge-model-selection.md) | Selection principles: family diversity, cost, latency, safety posture. |
| [Judge Precedents](judge-precedents.md) | Building a precedent library so judge decisions stay consistent. |
| [Distilling the Judge into an SLM](distill-judge-slm.md) | Moving from a large-model async judge to an inline sidecar SLM. |
| [Output Evaluator](output-evaluator.md) | Output-side evaluation patterns that complement judge rulings. |

## Detection and SOC

Integrating AI runtime telemetry into security operations.

| Document | Description |
|----------|-------------|
| [SOC Integration](soc-integration.md) | SOC architecture, alert taxonomy, triage procedures. |
| [SOC Content Pack](soc-content-pack.md) | SIEM detection rules, correlation searches, dashboards. |
| [Anomaly Detection Ops](anomaly-detection-ops.md) | Behavioural anomaly detection, operated as a programme. |
| [Behavioral Anomaly Detection](behavioral-anomaly-detection.md) | Detection techniques and baselines for agent behaviour. |
| [Graph-Based Agent Monitoring](graph-based-agent-monitoring.md) | Graph approaches to watching delegation and tool-call networks. |
| [Multi-Agent Failure Analysis](multi-agent-failure-analysis.md) | Post-incident analysis patterns for multi-agent failures. |
| [Runtime Telemetry Reference](runtime-telemetry-reference.md) | Canonical telemetry fields, events, and formats. |
| [Operational Metrics](operational-metrics.md) | Metrics catalogue for judges, guardrails, and the overall stack. |

## Control Catalogues

The working catalogues of controls, solutions, and hardening guidance.

| Document | Description |
|----------|-------------|
| [Agentic Controls Catalogue](agentic-controls-catalogue.md) | The working catalogue of controls for agentic deployments. |
| [Agentic Controls Extended](agentic-controls-extended.md) | Extended agentic control guidance and edge cases. |
| [Technical Controls](technical-controls.md) | Network, WAF, DLP, gateway controls for AI traffic. |
| [Current Solutions](current-solutions.md) | Industry solutions implementing this pattern. |
| [Control Selection Guide](control-selection-guide.md) | Methodology for choosing and sequencing controls. |
| [AI Endpoint Hardening](ai-endpoint-hardening.md) | Hardening the model endpoint, gateway, and tool server. |
| [RAG Security](rag-security.md) | RAG pipeline security, from ingestion to retrieval. |

## Economics and Identity

Cost, governance, and non-human identity considerations.

| Document | Description |
|----------|-------------|
| [Cost and Latency](cost-and-latency.md) | Cost and latency impact of each control layer. |
| [Economic Governance](economic-governance.md) | Budget, attribution, and economic guardrails for AI workloads. |
| [NHI Lifecycle](nhi-lifecycle.md) | Non-human identity lifecycle management. |
| [Supply Chain Controls](supply-chain.md) | AI supply chain security controls, from weights to packages. |
| [Humans in the Business Process](humans-in-the-business-process.md) | Where humans sit in the operational loop, and what they do there. |
