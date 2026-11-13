---
as_at: "2026-11-13"
description: "MASO identity and access controls for multi-agent AI: per-agent credentials, secrets handling, MCP server credential custody, privilege boundaries, delegation rules, and orchestrator isolation."
---

# MASO (Multi-Agent Security Operations) Control Domain: Identity & Access

> Part of the [MASO Framework](../README.md) · Control Specifications
> Covers: ASI03 (Identity & Privilege Abuse) · ASI07 (Insecure Inter-Agent Comms) · LLM06 (Excessive Agency)
> Also covers: SR-05 (Secrets Leakage) · CR-03 (Role Drift)

## Principle

Every agent is a non-human actor with its own identity, credentials, and permission scope. No agent inherits permissions from the orchestrator. No agent shares credentials with another agent. Trust is verified on every interaction, not assumed from membership in the same orchestration.

This domain is the foundation for all other MASO controls. Without reliable agent identity, you cannot enforce data fencing, attribute actions in the audit trail, or isolate a compromised agent. Get this wrong and every other control domain is undermined.

## Why This Matters in Multi-Agent Systems

In single-model deployments, identity is straightforward - there's one model, one credential set, one permission scope. Multi-agent systems break this model in several ways:

**Transitive permission chains.** If Agent A delegates a task to Agent B, and Agent B has access to Tool X, then Agent A effectively has indirect access to Tool X through the delegation. Without explicit controls, delegation creates implicit privilege escalation.

**Orchestrator over-privilege.** The orchestrator (the component that routes tasks to agents) typically starts with broad permissions because it needs to manage all agents. If task agents inherit the orchestrator's credentials - a common design shortcut - every agent operates with orchestrator-level privilege.

**Credential sharing at scale.** When agents are spun up dynamically, developers often reuse a single service account across all agent instances. This means compromising one agent compromises the credential used by all agents.

**Message bus trust.** If inter-agent messages are not authenticated, any component that can reach the message bus can impersonate an agent. The bus becomes an attack surface rather than a control point.

**MCP servers hold the keys.** When an agent uses a tool through MCP (Model Context Protocol), the MCP server is the component that actually calls the downstream application, so it is the component that needs the application's credential. If that credential is passed in by the agent, returned by a "get secret" tool, written into the MCP client's configuration, or taken from the client's own OAuth token and forwarded, it ends up somewhere a prompt injection can reach. The MCP controls below (IA-1.6, IA-1.7, IA-2.10, IA-2.11, IA-3.7) keep the agent's job to *what* to call, and the MCP server's job to *how* to authenticate. See [MCP Secrets Pattern](#mcp-secrets-pattern) for a worked AWS example.

## Controls by Tier

### Tier 1 - Supervised

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **IA-1.1** Agent identifier | Each agent has a unique string identifier in all log entries | Simple label (e.g., `agent-analyst-01`). No certificate infrastructure required. |
| **IA-1.2** No shared credentials | Each agent authenticates to tools with its own credential set | Verify by auditing credential inventory. |
| **IA-1.3** No orchestrator inheritance | Task agents do not use the orchestrator's credentials | Orchestrator credentials must not appear in task agent configurations. |
| **IA-1.4** Scoped permissions | Agent permissions limited to minimum required for defined task | Read access is the default. Write access requires documented justification. |
| **IA-1.5** Managed secret storage | Every secret an agent uses is held in a managed secrets store and recorded in the credential inventory with owner, scope, and expiry. No secret is stored in system prompts, agent or orchestrator configuration, skill packages, source repositories, container images, or plain `.env` files | Any existing secrets manager meets this (cloud KMS-backed secret stores, HashiCorp Vault, CyberArk). Repository and image secret scanning catches regressions. A secret found outside the store is rotated, not moved. Skill packages are covered by [SC-2.9](supply-chain.md). |
| **IA-1.6** No secrets in MCP client configuration | MCP client configuration (`.mcp.json`, client settings files, the `env` and `headers` blocks of a server entry, and server launch arguments) holds no literal secrets. Where a local server needs a credential, the configuration holds a reference that a launcher resolves from the secrets store at start-up | These files sit in repositories and home directories, are readable by any agent with file or shell access, and are often committed. A literal key found in one is rotated (IA-1.5). For production agents, prefer remote MCP servers with their own workload identity (IA-2.10) over local servers carrying keys. |
| **IA-1.7** No credential-bearing tool interfaces | No MCP tool, or any other tool exposed to an agent, accepts a credential as a parameter or returns one in its result. Tools that read secrets on the agent's behalf (`get_secret`, `read_env`, `get_connection_string`) are not exposed to agents | A tool that returns a secret puts it in the context window, where IA-2.6 says it must never be, and where a prompt injection can ask for it. A tool schema with a `token`, `api_key`, or `password` parameter is a vetting red flag ([Supply Chain MCP vetting](supply-chain.md#mcp-server-vetting-process-tier-2)). |

**What you're building at Tier 1:** A credential inventory, a single managed home for every agent secret, and the organisational discipline to assign unique, scoped credentials per agent. No new agent-specific infrastructure required.

### Tier 2 - Managed

All Tier 1 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **IA-2.1** Non-Human Identity (NHI) | Certificate-based identity per agent from a managed identity provider | NHI includes role, permission scope, and credential expiry. |
| **IA-2.2** Short-lived credentials | Automatic rotation: 1hr for high-privilege agents, 24hr for read-only | Credentials not rotated within the window are automatically revoked. |
| **IA-2.3** Mutual authentication | Agents authenticate to the message bus using NHI certificates | Bus rejects messages from unrecognised or expired identities. |
| **IA-2.4** No transitive permissions | Delegated tasks do not inherit the delegating agent's permissions | Agent B operates within its own NHI scope regardless of what Agent A requested. |
| **IA-2.5** Orchestrator privilege separation | Orchestrator can route tasks and manage lifecycle but cannot invoke tools directly | Tool access scoped exclusively to task agents. |
| **IA-2.6** Secrets exclusion from context | Secrets (API keys, tokens, connection strings) must never appear in agent context windows, inter-agent messages, or logs | Agents access secrets through platform-injected vault references only. DLP scanning for secret patterns on the message bus (cross-ref [DP-2.1](data-protection.md)). |
| **IA-2.7** Vaulted per-flow credential brokering | Orchestrators, gateways, and low-code agent builders hold no standing provider keys, database credentials, or connector tokens; each flow requests a short-lived, scoped token at execution time | An agent orchestrator accumulates every secret its flows need and becomes the highest-value host in the estate. The Langflow chain exploited in the wild ([CVE-2026-9198](../threat-intelligence/incident-tracker.md#inc-21-langflow-orchestrator-remote-code-execution-exploited-2026), August 2026) turned one unauthenticated RCE into access to every system its flows touched. Brokering credentials per flow means a compromised orchestrator yields a host rather than a keyring, and it gives the revocation and expiry that a stored key never has. |
| **IA-2.8** Tool-boundary secret injection | Credentials are attached to a request by the tool gateway or broker at the point of call, outside the model process. Agent processes, sub-agents, and skill scripts do not inherit host environment variables, credential files (`~/.aws`, `~/.ssh`, `~/.npmrc`, `~/.docker/config.json`, `.env`), keychains, or AI coding assistant session tokens | The model works with a handle or a tool name, never the value, so a prompt injection that asks the agent to "print your API key" has nothing to print. Run agent and skill processes with an empty, allow-listed environment. This is the process-level counterpart to IA-2.6, which covers what reaches the context window. Cross-ref [EC-2.2](execution-control.md) sandboxing and [SC-2.9](supply-chain.md). |
| **IA-2.9** Secret redaction at ingress and persistence | Tool results, error messages, stack traces, retrieved documents, and fetched web content are scanned for secret patterns and redacted before they enter an agent's context. Secrets are never written to agent memory, vector stores, conversation checkpoints, or traces | IA-2.6 states the outcome. This control covers the path most often missed: a tool that echoes its own connection string in an error, or a retrieved config file containing a key. A detected secret is redacted, the event is logged without the value, and the secret is flagged for rotation. Cross-ref [DP-2.1](data-protection.md). |
| **IA-2.10** MCP server credential custody | Each MCP server retrieves the credentials it needs for downstream systems itself, from the secrets store, under its own workload identity. That identity can read only the named secrets the server needs, and no two servers share an identity or a secret | On AWS: an ECS task role, Lambda execution role, or EKS pod identity with `secretsmanager:GetSecretValue` on specific secret ARNs, a resource policy on each secret naming that role, and a customer-managed KMS key whose policy names it too. Cache with the AWS Secrets Manager caching library or Lambda extension, not in environment variables, so rotation takes effect. Where the downstream is an AWS service, the role is the credential and no secret is stored at all. Equivalent patterns: Azure managed identity with Key Vault, GCP service account with Secret Manager, HashiCorp Vault with workload auth. Infrastructure detail: [SEC-01, SEC-03](../../infrastructure/controls/secrets-and-credentials.md). |
| **IA-2.11** No MCP token passthrough | A remote MCP server accepts only access tokens issued for it (audience-bound using OAuth resource indicators, RFC 8707) and never forwards the token it received from the MCP client to a downstream API. Downstream calls use the server's own credential (IA-2.10) or a separate token obtained for the downstream audience, for example by OAuth token exchange (RFC 8693) | The MCP authorization specification prohibits token passthrough because it lets a server act as a confused deputy and lets a token issued for one service be replayed at another. Token exchange is the pattern to use when the downstream application must know which agent or user is acting: it keeps that identity without handing the client's token onward. |

**What you're building at Tier 2:** An NHI lifecycle management system, with MCP servers as first-class workload identities that hold their own secrets. This can be an extension of your existing identity provider (Entra ID, Okta, CyberArk) or a dedicated agent identity service.

### Tier 3 - Autonomous

All Tier 2 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **IA-3.1** Sub-hour rotation (all) | No agent holds credentials longer than 60 minutes | High-privilege agents rotate every 15 minutes. |
| **IA-3.2** Behavioral binding | NHI includes a behavioral profile; deviations flagged independently of drift detection | Second detection layer if behavior doesn't match identity profile. |
| **IA-3.3** Delegation mandates | Signed mandates define scope, max permissions, time limit, and expected output for each delegation | Agent B cannot exceed the mandate scope. |
| **IA-3.4** Automated credential revocation | Anomaly detection triggers credential revocation within 30 seconds | Faster than full PACE transition; immediate containment. |
| **IA-3.5** Sender-constrained tokens | Access tokens issued to agents are bound to the agent's NHI key and restricted to a single audience, so a token copied out of an agent cannot be replayed from another host or against another service | Use mutual-TLS certificate-bound tokens ([RFC 8705](https://www.rfc-editor.org/rfc/rfc8705)) or DPoP ([RFC 9449](https://www.rfc-editor.org/rfc/rfc9449)) with an `aud` claim per tool. Bearer tokens remain usable by whoever holds them; bound tokens are not. |
| **IA-3.6** Canary credentials | Decoy credentials are planted where an agent or skill should never look (environment, home directory credential files, memory, configuration). Any use of a canary triggers IA-3.4 revocation of the agent's real credentials and a PACE escalation | Gives a high-confidence signal of credential harvesting, including by a skill that passed review. Canaries are unique per agent so the source of a leak is identified immediately. |
| **IA-3.7** Secret access correlation | Every secret retrieval by an MCP server or broker is logged with the workload identity, and correlated with the tool call and agent identity that caused it. A retrieval with no matching tool call, of a secret outside the server's declared set, or at a volume outside its baseline triggers IA-3.4 revocation | Secrets store audit logs (AWS CloudTrail `GetSecretValue` events, Key Vault diagnostic logs, Vault audit device) joined with the MCP gateway's tool-call log ([OB-1.1](observability.md)). A compromised MCP server pulling secrets it does not normally use is the earliest reliable signal that it has been taken over. |

**What you're building at Tier 3:** Behavioral identity - the NHI is not just a certificate, it's a mandate that includes expected behavior patterns. Tokens are bound to that identity, and canary credentials turn theft attempts into alerts. The identity system becomes a detection layer.

## Testing Criteria

### Tier 1 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| IA-T1.1 | Verify each agent has a unique identifier in logs | No two agents share the same identifier. Every log entry contains the agent ID. |
| IA-T1.2 | Audit credential inventory | Every agent has its own credentials. No credential is used by more than one agent. |
| IA-T1.3 | Check orchestrator credential isolation | Orchestrator credentials do not appear in any task agent's configuration or environment. |
| IA-T1.4 | Attempt out-of-scope action | Agent configured for read-only attempts a write operation. Action is blocked. |
| IA-T1.5 | Secret storage audit | Scan agent and orchestrator configuration, system prompts, skill packages, repositories, and container images for secret patterns. No secrets found outside the managed store. Every inventoried credential has an owner, scope, and expiry. |
| IA-T1.6 | MCP configuration scan | Scan every MCP client configuration in repositories, home directories, and agent images for literal secrets in `env`, `headers`, and launch arguments. None found. |
| IA-T1.7 | Credential-bearing tools | Review the schema of every tool exposed to agents. No tool takes a credential parameter or returns a credential. Ask an agent to retrieve a secret for you. It has no tool that can. |

### Tier 2 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| IA-T2.1 | NHI spoofing | Attempt to send a message on the bus using a forged agent identity. Message is rejected. |
| IA-T2.2 | Credential expiry | Allow an agent's credentials to expire. Agent loses tool and bus access immediately. |
| IA-T2.3 | Transitive permission | Agent A delegates a task requiring Agent A's permissions to Agent B. Agent B cannot use Agent A's permissions; task fails. |
| IA-T2.4 | NHI revocation | Revoke a specific agent's NHI. Verify revocation takes effect within 5 minutes. |
| IA-T2.5 | Orchestrator tool access | Attempt to invoke a tool directly from the orchestrator. Invocation is blocked. |
| IA-T2.6 | Secrets in context | Search agent context windows, inter-agent messages, and logs for secret patterns (API keys, tokens, connection strings). No secrets found. Verify agents access secrets only through vault injection. |
| IA-T2.7 | Role-based tool enforcement | For each agent role, attempt to invoke tools assigned to a different role. All cross-role tool invocations blocked. (Amendment: CR-03) |
| IA-T2.8 | Environment inheritance | From inside an agent process and a skill script, list environment variables and attempt to read `~/.aws/credentials`, `~/.ssh/id_rsa`, and the host's AI assistant session token. No credential values are available. Instruct the agent to reveal the API key for a tool it uses. It has none to reveal. |
| IA-T2.9 | Secret ingress and persistence | Have a tool return an error containing a connection string, and retrieve a document containing an API key. Both values are redacted before reaching the context. Search memory, vector stores, checkpoints, and traces afterwards. Neither value is present. |
| IA-T2.10 | MCP credential custody | Using one MCP server's workload identity, attempt to read a secret belonging to another server, and a secret not on its declared list. Both are denied by IAM and by the secret's resource policy. Rotate a secret and confirm the server picks up the new value without a restart or redeploy. |
| IA-T2.11 | Token passthrough | Present the MCP server with a token issued for a different audience. It is rejected. Capture the server's downstream requests and confirm the client's token never appears in them. |

### Tier 3 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| IA-T3.1 | Rotation enforcement | Monitor credential age across all agents for 24 hours. No credential exceeds 60 minutes (15 minutes for high-privilege). |
| IA-T3.2 | Behavioral mismatch | Agent with a "read-heavy" NHI profile starts making high-volume writes. NHI system flags the mismatch independently of drift detection. |
| IA-T3.3 | Delegation mandate breach | Agent B attempts an action outside the delegation mandate scope. Action is blocked and event is logged. |
| IA-T3.4 | Automated revocation latency | Inject anomalous behavior. Measure time from detection to credential revocation. Must be under 30 seconds. |
| IA-T3.5 | Token replay | Copy a valid access token from an agent and present it from a different host, and against a different tool. Both requests are rejected. |
| IA-T3.6 | Canary trip | Have a test skill read and use a canary credential. Real credentials for that agent are revoked within 30 seconds and a PACE escalation is raised. |
| IA-T3.7 | Unexplained secret access | Using an MCP server's workload identity, retrieve one of its own secrets with no corresponding tool call, then retrieve a secret outside its declared set. Both are flagged, and credentials are revoked within 30 seconds. |

## Maturity Indicators

| Level | Indicator |
|-------|-----------|
| **Initial** | Agents share credentials or use the orchestrator's identity. No credential inventory exists. |
| **Managed** | Each agent has unique credentials held in a managed secrets store. Credential inventory documented. Permissions scoped but not enforced at infrastructure level. |
| **Defined** | NHI per agent. Short-lived credentials with automated rotation. Mutual authentication on the message bus. Transitive permissions explicitly blocked. Secrets injected at the tool boundary and redacted at ingress, never held by the agent process. MCP servers hold their own credentials under their own workload identity, with no token passthrough. |
| **Quantitatively Managed** | Credential rotation compliance measured and reported. Authentication failure rates tracked. NHI revocation SLA measured and met. |
| **Optimising** | Behavioral binding on NHI. Delegation mandates enforced. Sender-constrained tokens and canary credentials. Secret retrievals correlated with tool calls. Automated revocation on anomaly. Credential lifecycle fully automated with no manual intervention. |

## MCP Secrets Pattern

This is the reference flow for an agent that uses an MCP tool to act on an application whose credential is held in AWS Secrets Manager. The same shape applies to other clouds and to HashiCorp Vault.

1. The agent calls a business tool, such as `create_invoice(customer_id, amount)`. No credential appears in the call or in the tool schema (IA-1.7).
2. The MCP gateway authenticates the agent with a token issued for this MCP server (IA-2.11) and logs the call with the agent identity ([OB-1.1](observability.md)).
3. The MCP server, running under its own role (IA-2.10), reads the one secret it needs from Secrets Manager.
4. The server calls the application and returns only the business result. Errors are summarised, never echoed with request headers or connection strings (IA-2.9).
5. CloudTrail records the `GetSecretValue` call, which is correlated with the tool call in step 2 (IA-3.7).

The MCP server's tool:

```python
import boto3
import requests
from aws_secretsmanager_caching import SecretCache
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("billing")
secrets = SecretCache(client=boto3.client("secretsmanager"))  # honours rotation, no env vars
SECRET_ARN = "arn:aws:secretsmanager:eu-west-2:111122223333:secret:billing-api-AbCdEf"


@mcp.tool()
def create_invoice(customer_id: str, amount: float) -> dict:
    """Create an invoice in the billing system."""
    key = secrets.get_secret_string(SECRET_ARN)
    resp = requests.post(
        "https://billing.internal/invoices",
        json={"customer": customer_id, "amount": amount},
        headers={"Authorization": f"Bearer {key}"},
        timeout=10,
    )
    if not resp.ok:
        return {"error": f"billing returned {resp.status_code}"}  # no body, no headers
    return {"invoice_id": resp.json()["id"]}
```

The server role's IAM policy grants one secret, nothing else:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:eu-west-2:111122223333:secret:billing-api-AbCdEf"
    },
    {
      "Effect": "Allow",
      "Action": "kms:Decrypt",
      "Resource": "arn:aws:kms:eu-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab",
      "Condition": {
        "StringEquals": { "kms:ViaService": "secretsmanager.eu-west-2.amazonaws.com" }
      }
    }
  ]
}
```

Add a resource policy on the secret that denies every principal except this role (and, where the server runs in a VPC, every request not arriving through the Secrets Manager VPC endpoint, using `aws:SourceVpce`). The identity policy says what the server may read; the resource policy says who may read the secret, so a mistake in one is caught by the other.

**When the application must know who is acting.** A single stored API key makes every call look like the MCP server. If the application needs the agent's or user's identity, replace the stored key with a short-lived token per call: OAuth token exchange (RFC 8693) for an OAuth-protected application, or STS `AssumeRole` with session tags for an AWS one. This is IA-2.7 applied to MCP, and binding the token to the caller is IA-3.5.

**Local stdio servers.** A server launched by the MCP client on a developer's machine inherits whatever the configuration gives it. If one is unavoidable, use a launcher that resolves the secret at start-up with the developer's own short-lived SSO credentials, so the configuration file holds only a reference (IA-1.6). The secret still lives in a process the agent's shell can reach, which is why production agents use remote servers with their own role.

## Common Pitfalls

**Treating AI coding assistant sessions as developer credentials rather than machine credentials.** The Bitwarden CLI supply chain attack (April 2026) was the first publicly documented malware designed to harvest authenticated sessions for Claude Code, Cursor, Kiro, Codex CLI, and Aider as a primary objective, not as incidental credential theft. These sessions have the access scope of the developer's identity and must be governed as machine credentials: short-lived tokens, rotation on session completion, dedicated credential store separate from human passwords, and monitoring for use outside expected development hours or locations. IA-2.6 (secrets exclusion from context) and IA-2.8 (tool-boundary secret injection) apply: AI coding assistant session tokens must not persist in environment variables, `.env` files, or shell history accessible to agent processes.

**Using API keys instead of certificates.** API keys are long-lived shared secrets. They can be extracted from agent memory, logged accidentally, or leaked through tool manifests. Certificate-based NHI with short-lived tokens is the target state.

**Treating the orchestrator as a trusted intermediary.** The orchestrator routes tasks - it should not proxy tool access. If every tool call goes through the orchestrator, the orchestrator becomes a single point of compromise with maximum privilege.

**Forgetting about dynamic agent creation.** In systems that spin up agents on demand, the identity provisioning must be automated and scoped. A new agent instance should receive a fresh NHI with the minimum permissions for its role, not a clone of an existing agent's identity.

**Assuming the message bus is internal and therefore trusted.** Any component that can reach the bus can send messages. Without mutual authentication, the bus is an open injection point for inter-agent prompt injection (ASI01) and message spoofing (ASI07).

**Building a "get secret" MCP tool.** It is the quickest way to give an agent access to a secrets store and the one design that guarantees the secret ends up in the context window, the model provider's logs, and the reach of every prompt injection. The agent should be able to *use* a capability that needs a secret, never to *read* the secret (IA-1.7, IA-2.10).

**Forwarding the agent's token to the application.** It looks like single sign-on and it is token passthrough: the downstream API cannot tell the MCP server from the agent, and a token stolen from one service works at the other. Use the server's own credential or exchange the token for one issued to the downstream audience (IA-2.11).

**Removing a leaked secret instead of rotating it.** Deleting a key from a prompt, a skill, or a repository does not un-leak it. Logs, caches, model provider retention, and every copy of a distributed skill package may still hold it. Once a secret has been anywhere outside the managed store, revoke and reissue it.

!!! info "References"
    - [RFC 8705: OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
    - [RFC 9449: OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://www.rfc-editor.org/rfc/rfc9449)
    - [OWASP Top 10 for Agentic Applications (ASI03: Identity and Privilege Abuse)](https://genai.owasp.org/)
    - [Model Context Protocol: Authorization (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
    - [Model Context Protocol: Security Best Practices (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)
    - [RFC 8707: Resource Indicators for OAuth 2.0](https://www.rfc-editor.org/rfc/rfc8707)
    - [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
    - [AWS Secrets Manager: Authentication and access control](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access.html)
    - [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
