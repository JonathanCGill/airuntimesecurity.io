# AI Endpoint Hardening

> Securing model inference endpoints, API gateways, and tool servers against adversarial and operational threats.

This guide consolidates endpoint-specific security controls that are distributed across the framework's [network](../../infrastructure/controls/network-and-segmentation.md), [IAM](../../infrastructure/controls/identity-and-access.md), [secrets](../../infrastructure/controls/secrets-and-credentials.md), and [data protection](../../infrastructure/controls/data-protection.md) domains into a single implementation reference. If you're the engineer deploying model endpoints, start here.

## Why AI Endpoints Are Different

Traditional API hardening focuses on authentication, rate limiting, and input validation. AI inference endpoints introduce additional concerns:

| Concern | Traditional API | AI Inference Endpoint |
|---|---|---|
| **Input validation** | Schema validation, type checking | Schema validation + prompt injection detection + content policy enforcement |
| **Output control** | Response schema | Response schema + PII scanning + hallucination detection + system prompt leak prevention |
| **Authentication** | OAuth/API key per client | Per-client + per-agent identity + session-scoped credentials |
| **Rate limiting** | Requests per second | Requests + tokens per second + cost capping per consumer |
| **Resource consumption** | CPU/memory bounds | GPU/TPU bounds + context window limits + max output tokens |
| **Attack surface** | OWASP Top 10 | OWASP Top 10 + OWASP LLM Top 10 + OWASP Agentic Top 10 |

The core difference: **a traditional API processes structured data deterministically. An AI endpoint processes unstructured natural language non-deterministically.** Every input is potentially adversarial, and every output is potentially wrong.

## Endpoint Architecture

AI endpoints must be deployed behind the framework's [zone architecture](../../infrastructure/controls/network-and-segmentation.md#net-01-network-zone-architecture):

```
Consumer → Zone 1 (API Gateway + WAF)
              → Zone 2 (Input Guardrails → Model Endpoint → Output Guardrails)
              → Zone 3 (Judge - async evaluation)
              → Zone 6 (Logging)
```

**The model endpoint is never directly addressable.** All access routes through the API gateway (NET-07) and guardrails (NET-02). This is the non-negotiable foundation.

## Gateway Hardening

The API gateway is the single entry point and first line of defence. Harden it as you would any security-critical reverse proxy - then add AI-specific controls.

### Standard Controls

| Control | Implementation | Notes |
|---|---|---|
| **TLS termination** | TLS 1.2+ with strong cipher suites. Disable TLS 1.0/1.1. | HSTS headers on all responses. |
| **mTLS (Tier 3+)** | Mutual TLS for service-to-service calls within Zone 2. | Certificate pinning for known internal clients. |
| **Authentication** | OAuth 2.0 / OIDC token validation. No API-key-only auth for Tier 2+. | Propagate authenticated identity downstream (IAM-01). |
| **Rate limiting** | Per-consumer limits on requests, tokens, and cost. | See [Token-Based Rate Limiting](#token-based-rate-limiting) below. |
| **WAF integration** | Standard OWASP CRS rules for SQLi, XSS, path traversal. | AI-specific WAF rules for common injection patterns (optional - guardrails are the primary defence). |
| **Schema validation** | Reject malformed requests before they reach the model. | Validate JSON structure, required fields, max prompt length. |
| **Request size limits** | Cap request body size. | Prevent context window stuffing attacks. |
| **Timeout enforcement** | Set max request duration. | Prevents long-running inference from consuming GPU indefinitely. |

### AI-Specific Gateway Controls

| Control | Implementation |
|---|---|
| **Max input tokens** | Enforce a hard limit on prompt length at the gateway. Requests exceeding the limit are rejected before reaching the model. |
| **Max output tokens** | Set `max_tokens` at the gateway level, not just in the prompt. Prevents runaway generation. |
| **Correlation ID injection** | Generate and inject a unique `request_id` / `trace_id` into every request. Propagate through all downstream components. Essential for SOC correlation. |
| **Consumer identification** | Log the authenticated identity, source IP, user agent, and session ID for every request. Required for [identity correlation](soc-integration.md#identity-correlation). |
| **Endpoint routing** | Route to specific model versions via gateway config, not consumer choice. Consumers don't get to select which model version serves their request. |

## Token-Based Rate Limiting

Traditional request-per-second rate limiting is insufficient for AI endpoints because:

- A single request can consume vastly different amounts of compute depending on prompt length and output length.
- A rate-limited attacker can send one request with a massive prompt that consumes more resources than 100 normal requests.
- Token cost varies by model - a request to a large model costs more than the same request to a smaller model.

### Rate Limiting Strategy

| Dimension | Limit Type | Example |
|---|---|---|
| **Requests per minute** | Hard cap per consumer | 60 rpm for standard, 200 rpm for premium |
| **Input tokens per minute** | Hard cap per consumer | 100K tokens/min |
| **Output tokens per minute** | Hard cap per consumer | 50K tokens/min |
| **Cost per hour** | Soft cap with alert, hard cap with block | $10/hr soft, $50/hr hard |
| **Concurrent requests** | Per consumer and global | 5 concurrent per consumer, 100 global |

### Burst Protection

Allow short bursts above the per-minute limit, but enforce a sliding window. This prevents legitimate batch operations from being blocked while still catching sustained abuse.

## Model Endpoint Hardening

The model inference endpoint itself - whether self-hosted, managed, or third-party - requires specific hardening.

### Self-Hosted Endpoints (vLLM, TGI, Ollama, TorchServe)

| Control | Detail |
|---|---|
| **Network binding** | Bind to internal interface only. Never expose on 0.0.0.0 or public IP. |
| **Authentication** | Require authentication even for internal access. No unauthenticated inference. |
| **Health check endpoint** | Expose `/health` or `/ready` on a separate port or path. Return minimal information - model name and status only. Do not expose model version, configuration, or system details. |
| **Metrics endpoint** | Expose Prometheus metrics (`/metrics`) on a separate port, accessible only from Zone 6 (Logging). Do not expose on the inference port. |
| **Resource limits** | Set container memory and GPU limits. Use Kubernetes resource quotas or equivalent. Prevent a single request from exhausting GPU memory. |
| **Process isolation** | Run inference in a dedicated container/pod. Do not co-locate with other services. |
| **Image hardening** | Use minimal base images. Remove unnecessary packages, shells, and debugging tools from production images. |
| **Read-only filesystem** | Mount the container filesystem as read-only. Model weights and config are mounted as read-only volumes. |
| **Non-root execution** | Run the inference process as a non-root user. |
| **No outbound access** | Model inference endpoints should have no outbound network access (except for agent tool calls via egress proxy - NET-04). |

### Managed Endpoints (Azure OpenAI, Bedrock, Vertex AI)

| Control | Detail |
|---|---|
| **Private endpoints** | Use private endpoints / VPC endpoints. Do not call managed AI services over the public internet from production. |
| **Network restrictions** | Apply IP allowlisting or VNet/VPC rules to restrict which networks can reach the managed endpoint. |
| **Content filtering** | Enable the provider's built-in content filtering as a baseline. Layer framework guardrails on top - provider filters are not sufficient alone. |
| **Data residency** | Deploy in regions aligned with data residency requirements. Verify that the provider does not route inference to other regions. |
| **Model version pinning** | Pin to a specific model version. Do not use "latest" or auto-updating model references in production. Provider model updates can change behavior without notice. |
| **Diagnostic logging** | Enable full diagnostic logging to your SIEM. Azure: Diagnostic Settings → Log Analytics. AWS: Bedrock invocation logging → CloudWatch. GCP: Cloud Logging integration. |
| **Customer-managed keys** | For Tier 3+, use customer-managed encryption keys for data at rest on the managed service. |
| **Quota management** | Set provider-level quotas per deployment to prevent cost runaway. Alert at 80% quota consumption. |

## Tool Server Hardening (MCP and Native)

When AI agents invoke tools - via MCP servers, native function calls, or API integrations - the tool endpoints require their own hardening.

| Control | Detail |
|---|---|
| **Allowlisting** | Only pre-approved tool endpoints are reachable by agents. Enforced at the [egress proxy](../../infrastructure/controls/network-and-segmentation.md#net-04-agent-egress-controls) (network layer), not by prompt instructions. |
| **Input validation** | Validate all parameters the agent sends to the tool. Type checking, range checking, allowlisted values. The agent's output is untrusted input to the tool. |
| **Output sanitisation** | Strip credentials, internal metadata, and excessive data from tool responses before they enter the agent's context window (SEC-01). |
| **Authentication** | Tool servers require authentication. Credentials injected by the [authorization gateway](../../infrastructure/controls/identity-and-access.md#iam-04-agent-tool-invocation-constraints), not passed through the model context. |
| **Idempotency** | Tool operations that create, modify, or delete should be idempotent where possible. Agents may retry on failure and should not create duplicates. |
| **Read/write separation** | Distinguish read-only tools from tools that take actions. Read-only tools require lower approval thresholds. Write tools require explicit control (IAM-05 for Tier 3+). |
| **Scope constraints** | Tool access is scoped to the minimum necessary data and operations. A "query customer" tool returns only the fields relevant to the task, not the full record. |
| **MCP server signing** | MCP servers must be signed with verified manifests (SC-2.2). Unsigned or modified MCP servers are blocked. |
| **Timeout enforcement** | Set max execution time per tool call. An agent waiting indefinitely for a tool response is a denial-of-service vector. |
| **Sandboxing** | Code execution tools must run in sandboxed environments with no network access, no filesystem persistence, and hard resource limits (SAND-01 through SAND-06). |

## Deployment Security

### Pre-Deployment Checklist

Before exposing any AI endpoint to traffic:

- [ ] Model endpoint is not directly addressable from outside Zone 2
- [ ] All traffic routes through API gateway with authentication and rate limiting
- [ ] Input and output guardrails are inline on the request path (not bypassable)
- [ ] Health check and metrics endpoints are on separate ports, not externally accessible
- [ ] TLS 1.2+ enforced on all connections
- [ ] mTLS enforced for internal service-to-service calls (Tier 3+)
- [ ] Correlation ID generated and propagated for every request
- [ ] Max input tokens, max output tokens, and request timeout are enforced at gateway
- [ ] Model version is pinned - no auto-updates in production
- [ ] Container runs as non-root with read-only filesystem
- [ ] No outbound network access from model endpoint (except via egress proxy for agents)
- [ ] Diagnostic logs flowing to SIEM with identity correlation
- [ ] Rate limits configured per consumer: requests, tokens, and cost
- [ ] Credential scanning active on model I/O
- [ ] Network policy tests automated in deployment pipeline

### Canary Deployment

When deploying model updates or configuration changes:

1. Route a small percentage of traffic (1–5%) to the new deployment.
2. Monitor guardrail block rates, Judge flag rates, and output token distributions.
3. Compare against baseline metrics from the existing deployment.
4. If anomaly metrics exceed thresholds, roll back automatically.
5. Maintain the previous deployment as a hot standby for immediate rollback.

Model updates are not code updates. A new model version can change behavior in ways that bypass existing guardrails. Treat model deployment with the same caution as infrastructure changes.

## PACE Resilience for Endpoints

Apply the [PACE resilience model](../../PACE-RESILIENCE.md) to endpoint availability:

| State | Condition | Endpoint Behavior |
|---|---|---|
| **Primary** | All layers operational | Full inference with guardrails, Judge evaluation, and human oversight |
| **Alternate** | Guardrails degraded | Switch to cached/static responses for high-risk queries. Continue serving low-risk queries with Judge-only evaluation. |
| **Contingency** | Model endpoint degraded | Return graceful error messages. Queue requests for delayed processing. Activate backup model if available. |
| **Emergency** | Confirmed compromise | Kill switch. All traffic rejected with maintenance response. Incident response activated. |

The kill switch must be infrastructure-level (gateway config or DNS), not dependent on the model endpoint itself being responsive.

## Monitoring and Alerting

Endpoint-specific signals to feed into the [SOC Content Pack](soc-content-pack.md):

| Signal | Threshold | Severity |
|---|---|---|
| Error rate (5xx) | >5% sustained for 5 minutes | High |
| Latency (p99) | >2x baseline for 10 minutes | Medium |
| GPU memory utilisation | >90% sustained | Medium |
| Token throughput drop | >50% below baseline | High |
| Guardrail block rate spike | >3x baseline in 15 minutes | Medium |
| Authentication failure spike | >10 failures from single IP in 1 minute | High |
| Request from unknown consumer | Any | Medium |
| Quota approaching limit | >80% of allocated quota | Low |

## Three-Layer Mapping

| Hardening Area | Guardrails | Model-as-Judge | Human Oversight |
|---|---|---|---|
| **Gateway** | Guardrails enforced at gateway - cannot be bypassed | Gateway logs feed Judge evaluation | Humans configure gateway policies |
| **Rate limiting** | Token-aware limits prevent resource abuse | Judge detects cost anomalies that bypass rate limits | Humans set per-consumer quotas |
| **Model endpoint** | Guardrails inline on request/response path | Judge evaluates output quality independently | Humans approve model version changes |
| **Tool servers** | Parameter validation on tool inputs | Judge evaluates tool invocation patterns | Humans define tool allowlists |
| **Deployment** | Canary deployment monitors guardrail effectiveness | Judge metrics compared between old and new versions | Humans approve production rollout |
| **PACE** | Guardrail degradation triggers Alternate mode | Judge degradation triggers Contingency escalation | Human-activated Emergency kill switch |

## OWASP Mapping

| Hardening Area | OWASP LLM Risk | OWASP Agentic Risk |
|---|---|---|
| Gateway rate limiting | LLM10: Unbounded Consumption | - |
| Input validation | LLM01: Prompt Injection | ASI01: Agent Goal Hijack |
| Output scanning | LLM02: Sensitive Information Disclosure | ASI02: Tool Misuse and Exploitation |
| Token limiting | LLM10: Unbounded Consumption | - |
| Model version pinning | LLM04: Data and Model Poisoning | ASI04: Agentic Supply Chain Compromise |
| Tool server hardening | LLM07: System Prompt Leakage | ASI02: Tool Misuse and Exploitation |
| Private endpoints | LLM06: Excessive Agency | ASI05: Unexpected Code Execution |
| Kill switch | - | ASI08: Cascading Agent Failures |

## Related

- [Network & Segmentation](../../infrastructure/controls/network-and-segmentation.md) - Zone architecture and traffic rules
- [Identity & Access Management](../../infrastructure/controls/identity-and-access.md) - Authentication and authorization controls
- [Secrets & Credentials](../../infrastructure/controls/secrets-and-credentials.md) - Credential management for AI components
- [Data Protection](../../infrastructure/controls/data-protection.md) - Data classification and protection in AI pipelines
- [SOC Content Pack](soc-content-pack.md) - Detection rules for endpoint monitoring
- [SOC Integration](soc-integration.md) - SOC architecture and triage procedures
- [When the Judge Can Be Fooled](../../core/when-the-judge-can-be-fooled.md) - Adversarial failure modes and mitigations

