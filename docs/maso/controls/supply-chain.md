---
as_at: "2026-11-13"
description: "MASO supply chain controls: inventorying, vetting, and integrity-verifying every model, tool, MCP server, skill, and plugin in multi-agent AI systems. Maps to OWASP LLM03, ASI04, the Agentic Skills Top 10, and the Agent Skills open specification."
---

# MASO (Multi-Agent Security Operations) Control Domain: Supply Chain

> Part of the [MASO Framework](../README.md) · Control Specifications
> Covers: LLM03 (Supply Chain Vulnerabilities) · ASI04 (Agentic Supply Chain) · AST01-AST10 (OWASP Agentic Skills Top 10, see [mapping](../reference.md#owasp-agentic-skills-top-10-2026))
> Also covers: HF-02 (Accountability - AIBOM component) · SR-05 (Secrets Leakage, skill packages)
> Conforms to: [Agent Skills specification](https://agentskills.io/specification) (`SKILL.md` format, see [conformance](#agent-skills-specification-conformance))

## Principle

Every component in the agent system - models, tools, MCP servers, skills, RAG sources, plugins, and protocol endpoints - is a supply chain dependency. Each dependency is inventoried, versioned, integrity-verified, and auditable. No component is loaded at runtime without prior vetting and signing. The supply chain attack surface scales linearly with the number of agents and exponentially with the number of dynamic integrations.

## Why This Matters in Multi-Agent Systems

**The supply chain multiplies with every agent.** A single-model system has one model provider, one set of tools, one RAG configuration. A three-agent system may have three different model providers, nine tool integrations, three RAG sources, and two MCP server connections. Each additional dependency is an additional attack surface.

**Dynamic composition at runtime.** Modern agent frameworks support dynamic tool discovery and composition - an agent can discover and use an MCP server it has never interacted with before. This is powerful for flexibility and catastrophic for security. A poisoned MCP tool descriptor can trick an agent into passing credentials as tool parameters, executing unintended operations, or loading malicious code.

**Model provider changes propagate silently.** When a model provider updates their model (version change, fine-tuning update, safety filter modification), every agent using that model is affected simultaneously. If the update introduces a regression - reduced safety filtering, changed behavior on edge cases, or degraded quality - the agents inherit the regression with no notice.

**Skills are instructions, not just code.** An agent skill (a `SKILL.md` package, a plugin, a hook, or an agent configuration file such as `CLAUDE.md` or `.cursorrules`) bundles natural-language instructions with optional scripts and runs with the full permissions of the agent that loads it. Signing and dependency scanning were built for code. They say nothing about prose that tells the agent to read `~/.ssh` and post it somewhere, or about a URL the skill tells the agent to read at runtime. OWASP's [Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/) (AST10) catalogues the resulting risk class. Controls SC-1.5, SC-1.6, SC-2.5 to SC-2.10, and SC-3.6 below exist because of it. In a multi-agent system the exposure compounds: one poisoned skill loaded by an orchestrator shapes every task it delegates.

**Credential harvesting through tool manifests.** A poisoned tool manifest can describe a tool that requires "authentication tokens" as parameters. The agent, following its instructions to use the tool, passes credentials to the attacker's endpoint. This is a supply chain attack that doesn't require compromising the agent's code - only its tool configuration.

## Controls by Tier

### Tier 1 - Supervised

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **SC-1.1** Model inventory | Every model used by every agent is documented: provider, version, API endpoint, date of last known update | Reviewed monthly. |
| **SC-1.2** Tool inventory | Every tool available to every agent is documented: name, source, version, permission scope | No undocumented tool integrations. |
| **SC-1.3** Fixed toolsets | Agents use a predefined, static set of tools. No runtime discovery or dynamic composition | New tools require a change request and security review. |
| **SC-1.4** RAG source inventory | Every RAG/vector database is documented per agent: source, update frequency, access controls | Enables traceability when poisoning is suspected. |
| **SC-1.5** Skill inventory and installation control | Every skill, plugin, hook, and instruction-bearing configuration file loaded by any agent is inventoried with source, version, content hash, installer identity, and accountable owner. Only the platform team installs skills; individual users and agents cannot | The content hash covers the whole skill directory (`SKILL.md` plus every file under `scripts/`, `references/`, and `assets/`), not `SKILL.md` alone, because bundled scripts and reference files are loaded or executed on activation. Skills from public registries are not installed directly: they are copied into a private curated registry after review, and agents load only from that registry. Ownership is reassigned or the skill revoked when its owner leaves. Addresses AST01, AST02, AST09. |
| **SC-1.6** Agent Skills format conformance | Every skill entering the curated registry conforms to the [Agent Skills specification](https://agentskills.io/specification) and passes the reference validator (`skills-ref validate`) before it is inventoried. Non-conforming skills are rejected, not repaired at load | The validator is the floor, not the security review: it confirms the format that SC-2.5 then inspects. Conformance gives every client in a multi-agent estate the same reading of the same skill, which is what makes a single review and a single hash meaningful across agents. See [Agent Skills specification conformance](#agent-skills-specification-conformance). Addresses AST04, AST10. |

### Tier 2 - Managed

All Tier 1 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **SC-2.1** AIBOM per agent | AI Bill of Materials generated for each agent: models, tools, RAG sources, MCP servers, dependencies, and their versions | Updated on every deployment. Stored alongside the agent's configuration. |
| **SC-2.2** Signed tool manifests | Tool manifests cryptographically signed; agents reject unsigned or tampered manifests | Signing key managed by the platform team, not the tool provider. |
| **SC-2.3** MCP server allow-listing | Agents can only connect to pre-approved MCP servers | Allow-list maintained by the AI security team. New MCP servers require vetting before addition. |
| **SC-2.4** Runtime integrity checks | Tool, MCP server, and skill integrity verified at load time against signed manifests | Integrity failure blocks loading and triggers an alert. |
| **SC-2.5** Skill definition validation | Skill metadata and definition files (`SKILL.md` front matter, `skill.json`, `manifest.json`, `package.json`) are validated against a strict schema with safe parsers before load. For `SKILL.md` the schema is the Agent Skills specification plus an explicit allow-list of the extension fields each target client supports. Any other key is rejected. Hidden characters, encoded instruction blocks, and names or publishers that impersonate a known brand are rejected. File references resolve inside the skill directory | No unsafe deserialisation (for example PyYAML `!!python/object` tags). Reject zero-width Unicode, bidirectional control characters, and unexplained base64 in instruction text. The `description` field gets the same hidden-character and injection checks as the body: it is loaded into every agent's context at start-up, before the skill is ever activated. Validation happens at intake, not in the client: Claude Code loads a skill whose YAML fails to parse with no fields set rather than refusing it, so a malformed `disable-model-invocation` or `paths` setting silently disappears. Reject absolute paths, `..` segments, and symlinks that leave the skill root (Claude Code follows symlinked skill folders). A skill ported from another platform is re-validated on the target platform, never assumed equivalent. Applies [EC-2.15](execution-control.md) strict parsing to the load path. Addresses AST04, AST10. |
| **SC-2.6** Per-skill permission manifest | Each skill declares the minimum filesystem paths, network destinations, shell access, and credentials it needs. The platform enforces the manifest at runtime; the skill cannot widen it | A skill's effective permissions are the intersection of its manifest and the agent's own scope ([IA-1.4](identity-and-access.md)), never the agent's full scope. A skill whose manifest grants all three legs of the Lethal Trifecta (private data, untrusted content, external communication) is blocked unless a named owner approves it with an egress allow-list. Where the target platform has no manifest format, the permissions are enforced in the sandbox instead ([EC-2.2](execution-control.md)). The skill's own `allowed-tools` and `compatibility` fields are author claims: the reviewer compares them with the approved manifest, and the manifest held by the registry is what is enforced. Where a client treats `allowed-tools` as a pre-approval (Claude Code does, without a workspace-trust check), review it as a permission grant and restrict it by managed policy (see [Claude Code profile](#platform-profile-claude-code)). Addresses AST03, AST10. |
| **SC-2.7** External instruction pinning | Content a skill directs the agent to read at runtime (remote documentation, runbooks, schemas, scripts) is either inlined into the reviewed skill or pinned by content hash and verified on every fetch. Unpinned external content is tagged as data, not instruction | A signed skill that points at a mutable URL is only as trustworthy as whoever controls that URL tomorrow. Hash mismatch fails closed and triggers re-vetting. Fetched content carries `type: "data"` under [PG-1.4](prompt-goal-and-epistemic-integrity.md). Addresses AST05. |
| **SC-2.8** Skill version and source pinning | Skills are pinned by content hash, not by name, tag, or `latest`. Auto-update and hot-reload are disabled. Where a client re-reads skill files live, the skill directories are made read-only to the agent and its user ([EC-2.19](execution-control.md)) so that "hot reload" cannot be used to swap content. Any new version, change of maintainer, or change of ownership of the source account or repository re-enters review | A "patch" release is an unverified new artefact until reviewed. A skill served from a repository whose owner account was deleted or transferred is treated as compromised until re-vetted. Addresses AST02, AST07. |
| **SC-2.9** Skill secret hygiene | Skill packages contain no secrets: no API keys, tokens, passwords, private keys, connection strings, or `.env` files anywhere in the skill directory or its front matter. Skill scripts obtain credentials only from the platform broker at execution time, scoped to the skill's permission manifest (SC-2.6). Skill instructions that direct the agent to read, print, export, or pass a credential are rejected | Run secret scanning over every file in the skill directory at intake and on every version (SC-2.8). A secret found in a skill is treated as exposed: it is revoked and rotated, not just removed from the package, because the package has already been distributed. Credential access goes through [IA-2.7](identity-and-access.md) brokering and [IA-2.8](identity-and-access.md) tool-boundary injection, so a skill script never reads the host agent's environment, keychain, or credential files. Addresses AST01, AST03, SR-05. |
| **SC-2.10** Skill invocation-time execution | Skills cannot run commands or register hooks at load or invocation time unless that skill has been approved for it. Clients that support it (Claude Code `` !`command` `` and ```` ```! ```` blocks, and the `hooks` front-matter field) have it disabled by managed policy for all other skills. Command output injected into a skill never contains secrets | Shell injection runs on the host before the model sees the skill, with no prompt, so a review of the instructions alone misses it. Hooks declared by a skill stay registered for the rest of the session, beyond the skill's own task. Injected output enters the context as plain text, so a command that prints environment variables or config files is a secret leak under [IA-2.6](identity-and-access.md). Addresses AST01, AST06. |

### Tier 3 - Autonomous

All Tier 2 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **SC-3.1** Model version pinning | Each agent pinned to a specific model version; automatic rollback if provider changes the model without notice | Requires model version detection and comparison with expected version. |
| **SC-3.2** Automated rollback | If a model provider change causes quality degradation (detected by Model-as-Judge baseline comparison), the system rolls back to the previous known-good version | Rollback is automated within the PACE Alternate phase. |
| **SC-3.3** Continuous dependency scanning | Automated scanning of all agent dependencies for known vulnerabilities and indicators of tampering | Minimum: daily scan. Results feed into the observability layer and trigger alerts on findings. |
| **SC-3.4** A2A trust chain validation | Agent-to-agent protocol endpoints (A2A, MCP, custom) validated against a trust chain before interaction | Prevents a compromised external service from injecting itself into the agent orchestration. |
| **SC-3.5** CI/CD pipeline integrity | CI/CD pipelines that produce signed artifacts must be monitored for integrity: OIDC token scope validation at runtime, build environment isolation, and anomaly detection on attestation workflows | Addresses SLSA attestation bypass via mid-build token hijacking. Signed provenance is only as trustworthy as the signing pipeline itself. See Common Pitfalls. |
| **SC-3.6** Behavioural skill evaluation | Before production approval, each skill is executed in an instrumented sandbox and its file, network, process, and memory-write behaviour compared against its permission manifest (SC-2.6). Evaluation runs under elevated-permission and sensitive-data conditions, not only benign defaults | Static and signature scanning is an input, never the approval gate: skill scanners have been bypassed in under an hour. Running the skill with realistic privileges is what exposes trust-tiered poisoning that stays dormant under test. Re-run on every version change (SC-2.8). Addresses AST01, AST08. |

## AIBOM Specification (Tier 2+)

The AI Bill of Materials is the supply chain equivalent of an SBOM (Software Bill of Materials). It provides a complete, versioned inventory of every component that contributes to an agent's behavior.

**Required fields per agent:**

| Field | Description | Example |
|-------|-------------|---------|
| Agent ID | Unique identifier | `agent-analyst-01` |
| NHI Reference | Link to agent's NHI record | `NHI-A-2026-0142` |
| Primary Model | Provider, model name, version, API endpoint | `Anthropic / claude-sonnet-4-5-20250929 / messages/v1` |
| Fallback Model | Backup model for PACE Alternate phase | `Google / gemini-2.0-flash / v1` |
| Model-as-Judge | Model-as-Judge (must differ from task model) | `OpenAI / gpt-4o / chat/completions` |
| Tools | List of tools with versions and manifest hashes | `[{name: "document-reader", version: "2.1.3", hash: "sha256:abc..."}]` |
| Skills | Skills, plugins, and hooks with spec `name`, content hash of the whole skill directory, source registry, pinned external references, and permission manifest hash | `[{name: "report-formatter", hash: "sha256:mno...", registry: "internal", external_refs: [{url: "https://...", hash: "sha256:pqr..."}]}]` |
| MCP Servers | Connected MCP servers with endpoint, manifest hash, workload identity, and the secrets each may read (references only, never values) | `[{name: "internal-search", endpoint: "https://...", hash: "sha256:def...", identity: "arn:aws:iam::...:role/mcp-search", secrets: ["arn:aws:secretsmanager:...:secret:search-api-..."]}]` |
| RAG Sources | Knowledge bases with integrity checksums | `[{name: "policy-docs", checksum: "sha256:ghi...", last_verified: "2026-02-14"}]` |
| Dependencies | Runtime libraries and framework versions | `[{name: "langchain", version: "0.3.12"}]` |
| Last Updated | Timestamp of AIBOM generation | `2026-02-15T08:00:00Z` |
| Accountable Human | Named human owner responsible for this agent's design, data sources, and approval | `jonathan.gill@example.com` (Amendment: HF-02) |
| Deployment Hash | Hash of the complete agent deployment configuration | `sha256:jkl...` |

The AIBOM should be generated automatically as part of the deployment pipeline and stored alongside the agent's configuration in version control. Any discrepancy between the deployed agent and its AIBOM indicates either a deployment error or tampering.

## MCP Server Vetting Process (Tier 2+)

MCP (Model Context Protocol) servers extend agent capabilities by providing tools and data. They are the most dynamic component of the supply chain and require structured vetting before agents can connect.

**Vetting checklist:**

| Check | Description |
|-------|-------------|
| Source verification | Who built it? Is the source code available for review? |
| Manifest inspection | Do the tool descriptions match the actual tool behavior? Are parameter schemas well-defined? |
| Credential handling | Does any tool take a credential as a parameter or return one in its result? Does the server expose a "get secret" style tool? (Red flag for both: credentials are held by the server or injected by the platform, never passed or seen by the agent. [IA-1.7](identity-and-access.md)) |
| Secret custody | Where does the server get its downstream credentials? It should read them from a secrets store under its own workload identity, scoped to named secrets ([IA-2.10](identity-and-access.md)), not from environment variables set in the client configuration ([IA-1.6](identity-and-access.md)) |
| Token handling | Does the server validate that client tokens were issued for it, and does it avoid forwarding them downstream? Token passthrough is a rejection ([IA-2.11](identity-and-access.md)) |
| Network behavior | What external endpoints does the MCP server contact? Are they documented and expected? |
| Data handling | What data does the MCP server access, store, or transmit? Does it comply with the agent's data classification? |
| Update mechanism | How is the MCP server updated? Can updates change tool behavior without notice? |
| Signing | Can the manifest be cryptographically signed? Is the signing key managed appropriately? |

**Approval authority:** AI security team for Tier 2. AI Security Architect for Tier 3 (higher bar due to autonomous usage).

**Re-vetting triggers:** Any update to the MCP server, change in maintainer, security advisory affecting the server's dependencies, or a 6-month periodic review - whichever comes first.

## Agent Skills Specification Conformance

The [Agent Skills specification](https://agentskills.io/specification) is the open format for `SKILL.md` packages, adopted across Claude Code, Codex, Cursor, VS Code, and other agent clients. MASO does not redefine the format. It treats conformance as the entry condition (SC-1.6) and layers security controls on each part of the format. The table records how each element of the specification is handled.

| Spec element | What the specification requires | MASO handling |
|---|---|---|
| Directory | A folder whose name matches the skill `name`, containing `SKILL.md` and optional `scripts/`, `references/`, `assets/` | Whole directory hashed and inventoried (SC-1.5), signed and verified at load (SC-2.2, SC-2.4), pinned by hash (SC-2.8), scanned for secrets (SC-2.9) |
| `name` | Required. 1 to 64 characters, lowercase letters, digits, and hyphens, no leading, trailing, or consecutive hyphens, matches the directory name | Validated (SC-1.6). Checked for brand and publisher impersonation and look-alike names of approved skills (SC-2.5) |
| `description` | Required. 1 to 1,024 characters, says what the skill does and when to use it | Loaded into every agent's start-up context, so it is an instruction surface before activation. Hidden-character and injection checks (SC-2.5, [PG-1.1](prompt-goal-and-epistemic-integrity.md)) |
| `license` | Optional. Licence name or a reference to a bundled licence file | Recorded in the inventory and AIBOM (SC-1.5, SC-2.1) |
| `compatibility` | Optional. Up to 500 characters on environment needs such as products, system packages, or network access | Network needs compared with the approved egress allow-list ([EC-2.18](execution-control.md)). A mismatch blocks approval |
| `metadata` | Optional. A map of string keys to string values | Parsed with safe parsers only (SC-2.5). Never a place for secrets (SC-2.9) or for permission grants |
| `allowed-tools` | Optional and experimental. Space-delimited list of pre-approved tools; support varies by client | Treated as an author claim. Enforcement comes from the registry-held permission manifest and the sandbox (SC-2.6, [EC-2.2](execution-control.md)), never from the field alone. On clients where it pre-approves tools, it is also reviewed as a grant |
| Body | Markdown instructions, kept short; detail moved to referenced files | Judge review of instructions (PG-2.1). Instructions to fetch remote content are pinned or inlined (SC-2.7) |
| File references | Relative paths from the skill root, kept one level deep | Resolved inside the skill root only; traversal and escaping symlinks rejected (SC-2.5) |
| Progressive disclosure | `name` and `description` loaded at start-up, the body on activation, other files on demand | Every stage is a load event: integrity is verified at each one, not only at start-up (SC-2.4) |
| Validation | `skills-ref validate` reference tool | Required at intake as the floor (SC-1.6). Security validation (SC-2.5) and behavioural evaluation (SC-3.6) follow it |

**Conformance is necessary, not sufficient.** A skill can conform to the specification and still carry a credential stealer in its scripts or a hidden instruction in its description. The specification defines a format. It does not define trust, signing, or permissions, which is why SC-2.2, SC-2.6, SC-2.9, and SC-3.6 sit on top of it.

### Platform Profile: Claude Code

Claude Code implements the Agent Skills specification and extends it. The [Claude Code skills documentation](https://code.claude.com/docs/en/skills) sets out the differences below, and each one changes how the controls above are applied. Other clients need a profile of their own; SC-2.5 re-validates a skill for each platform it runs on.

| Claude Code behaviour | Risk | MASO handling |
|---|---|---|
| Extension fields beyond the spec: `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`. Unknown keys are ignored, not rejected. Outside Claude Code (claude.ai upload, the Skills API) only the six spec fields are accepted | A skill that passes in one client fails or behaves differently in another. A mistyped security field is silently dropped | Allow-list of extension fields per client (SC-2.5). Skills meant to run on more than one platform use spec fields only (SC-1.6) |
| `allowed-tools` pre-approves the listed tools for the turn that invokes the skill. It does not restrict other tools, and a project skill's grant applies even in an untrusted folder | A skill checked into a repository can grant itself shell access without a prompt | Review as a grant (SC-2.6). Set `allowManagedPermissionRulesOnly` in managed settings so that project and personal skills cannot pre-approve tools. Use `disallowed-tools` to narrow, not `allowed-tools` |
| `` !`command` `` and ```` ```! ```` blocks run shell commands on invocation, before the model sees the skill, and put the output into context | Code runs with no human prompt. Output may carry secrets | `disableSkillShellExecution: true` in managed settings, with exceptions only for reviewed skills (SC-2.10). Injected commands must not print credentials ([IA-2.9](identity-and-access.md)) |
| `hooks` in front matter are registered on invocation and kept for the session | A skill gains persistent execution beyond its task | Managed policy restricts hook sources (`strictPluginOnlyCustomization`), and skill hooks are reviewed as code (SC-2.10) |
| `context: fork` runs the skill as a subagent, with `agent` choosing the subagent type | A skill can start a new agent with its own tool set | The subagent gets its own scope under [IA-2.4](identity-and-access.md). Delegation rules apply as for any other agent |
| Skills load from managed, personal (`~/.claude/skills/`), project (`.claude/skills/`), nested project directories, `--add-dir` directories, and plugins. Managed beats personal, and personal beats project | Cloning a repository adds skills. A personal skill can shadow a project skill with the same name | Only the managed location counts as the curated registry for production agents (SC-1.5). Repository-shipped skills are untrusted input until reviewed |
| Skill descriptions are always in context (except `disable-model-invocation: true`), capped at 1,536 characters with `when_to_use`. The spec caps `description` at 1,024 | Descriptions shape agent behaviour before any skill is invoked | Hold to the spec's 1,024-character limit for portability (SC-1.6). Use `disable-model-invocation: true` for skills with side effects, so only a human can start them |
| `SKILL.md` edits are picked up live | Content can change between review and use | Read-only skill directories (SC-2.8, [EC-2.19](execution-control.md)) |
| Skill names with zero-width, bidi-control, private-use, or unusual whitespace characters are refused, and `anthropic-skills` and `synced` are reserved | Covers names only, not descriptions or bodies | Hidden-character checks still run on every field and file (SC-2.5) |

## Testing Criteria

### Tier 1 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| SC-T1.1 | Inventory accuracy | Compare documented model, tool, and RAG inventories against actual agent configurations. No undocumented components. |
| SC-T1.2 | Fixed toolset enforcement | Attempt to add a tool to an agent's configuration without going through the change process. Attempt is blocked or detected. |
| SC-T1.3 | Inventory freshness | Verify inventories have been reviewed within the last 30 days. |
| SC-T1.4 | Unauthorised skill installation | As a non-platform user, and separately via an agent instruction, attempt to install a skill from a public registry. Installation is blocked and logged. |
| SC-T1.5 | Format conformance | Submit skills with a `name` that does not match its directory, an uppercase `name`, a `description` over 1,024 characters, and an unknown front-matter key. All four fail `skills-ref validate` and are rejected before inventory. |

### Tier 2 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| SC-T2.1 | AIBOM completeness | Generate AIBOM for each agent. Every field is populated. AIBOM matches deployed configuration. |
| SC-T2.2 | Manifest tampering | Modify a tool manifest after signing. Agent rejects the tampered manifest at load time. |
| SC-T2.3 | Unsigned tool | Attempt to load a tool without a signed manifest. Agent blocks the tool. |
| SC-T2.4 | Unapproved MCP server | Configure an agent to connect to an MCP server not on the allow-list. Connection is blocked. |
| SC-T2.5 | Runtime integrity | Modify a tool binary after deployment. Runtime integrity check detects the modification and blocks execution. |
| SC-T2.6 | Malformed skill metadata | Submit skills containing an unsafe YAML tag, zero-width Unicode in the instructions, and a brand-impersonating name. All three are rejected before load. |
| SC-T2.7 | Permission manifest enforcement | Load a skill whose manifest allows one directory, then instruct the agent (directly and via injected content) to have the skill read outside it and reach an undeclared host. Both are blocked. |
| SC-T2.8 | External reference drift | Change the content behind a hash-pinned URL that a skill references. The fetch fails closed and the skill is flagged for re-vetting. |
| SC-T2.9 | Skill update drift | Publish a new version of an approved skill upstream, and separately transfer ownership of its source repository. Neither change reaches a running agent without review. |
| SC-T2.10 | Secrets in skill packages | Submit skills with an API key in a file under `scripts/`, a token in a `metadata` value, a committed `.env` file, and an instruction telling the agent to print its environment variables. All four are rejected at intake. |
| SC-T2.11 | Skill path escape | Submit a skill whose body references `../../.ssh/id_rsa` and one with a symlink under `references/` pointing outside the skill root. Both are rejected at validation. |
| SC-T2.12 | Invocation-time execution | Load an unapproved skill containing a `` !`env` `` block and a `hooks` field, and a repository skill whose `allowed-tools` grants `Bash(*)`. The command does not run, the hook is not registered, and the tool grant is ignored by managed policy. |

### Tier 3 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| SC-T3.1 | Model version change detection | Simulate a model provider updating their model (change the version identifier). System detects the change and pins to the previous version. |
| SC-T3.2 | Automated rollback | Deploy a model version that produces lower Model-as-Judge scores than baseline. System triggers rollback within the PACE Alternate phase. |
| SC-T3.3 | Dependency vulnerability detection | Introduce a dependency with a known CVE into the agent's environment. Continuous scanning detects it within 24 hours. |
| SC-T3.4 | A2A trust chain | Introduce a new A2A endpoint not in the trust chain. Agent rejects the connection. |
| SC-T3.5 | Dormant skill payload | Submit a skill that behaves benignly under default test conditions but exfiltrates when it detects credentials or elevated permissions. Behavioural evaluation detects the undeclared access before approval. |

## Maturity Indicators

| Level | Indicator |
|-------|-----------|
| **Initial** | No inventory of models, tools, skills, or RAG sources. Agents use whatever tools are available. MCP servers and skills added without review. |
| **Managed** | Model, tool, and RAG inventories maintained. Fixed toolsets enforced. Changes go through a documented process. |
| **Defined** | AIBOM per agent. Signed tool manifests. MCP server allow-listing with vetting process. Runtime integrity checks. Skills conform to the Agent Skills specification, are validated, permission-scoped, secret-free, and pinned by hash, including their external references. |
| **Quantitatively Managed** | AIBOM accuracy measured (deployed vs. documented). Manifest verification failure rate tracked. MCP vetting completion time measured. |
| **Optimising** | Model version pinning with automated rollback. Continuous dependency scanning. A2A trust chain validation. Behavioural evaluation of every skill version before approval. AIBOM generation fully automated in CI/CD pipeline. |

## Common Pitfalls

**Treating a skill scanner verdict as approval.** Trail of Bits (June 2026) bypassed every skill scanner it tested, including registry-side scanning backed by a guard model, each in under an hour. Scanning finds the careless attacker. It does not find the one who has read the scanner's rules. SC-3.6 puts behavioural evaluation behind the scanner, and SC-1.5 keeps unreviewed public-registry skills out of production entirely, so a scanner miss is not by itself an incident.

**Pinning the skill but not what it reads.** A skill can be signed, hash-pinned, and reviewed, and still tell the agent to fetch its real instructions from a URL its author can change after review. Air Security's scan of 142,836 live skills (June 2026) found roughly one in eight resting on at least one such external resource. SC-2.7 closes this by pinning or inlining external references, and the separate SkillJacking case (a popular skill served from a GitHub account that had been deleted and could be re-registered) is why SC-2.8 treats a source-ownership change as a new artefact.

**Treating build provenance attestation as proof of artifact safety.** The Mini Shai-Hulud campaign (May 2026) produced the first malicious npm packages carrying valid SLSA Build Level 3 Sigstore attestations by hijacking a legitimate OIDC token mid-CI/CD workflow, compromising OpenAI's code-signing certificates in the process. Attestation proves the artifact was built as claimed; it does not prove the build pipeline was uncompromised. SC-3.5 addresses this, but only if CI/CD pipeline integrity monitoring is active: runtime OIDC token scope validation, build environment isolation, and anomaly detection on attestation workflows are all required.

**Registry listing is not provenance, and the agent is now the one searching.** Island's *AgentBaiting* research (August 2026) mapped roughly 7,600 malicious GitHub repositories, more than 800 posing as AI Skills or MCP servers, listed over 600 times across public registries and catalogues including LobeHub, Glama, MCP.so, and MCP Market, delivering the SmartLoader loader and the StealC infostealer. Presence in a public registry is an artefact of publishing, not of review, and must be excluded from the evidence set for SC-2.2 and SC-3.1: it carries no provenance weight for a human and none for an agent. The change that matters more is who performs discovery. Claude Code, Gemini, and ChatGPT all surfaced campaign repositories on their own, without being shown a link, because the attacker optimised the README and repository metadata for the agent's retrieval and ranking rather than for a developer's search. SC-1.3 therefore applies at the *discovery* step and not only at install: a capability an agent proposes is an untrusted proposal requiring human verification against a maintained allow-list, and an agent must never be able to install, clone, or register a name that is not already approved. See [ET-13](../threat-intelligence/emerging-threats.md#et-13-agent-ecosystem-supply-chain-compromise-at-scale).

**Agent configuration files are an instruction injection surface.** The TrapDoor supply chain campaign (May 2026) weaponized `CLAUDE.md`, `.cursorrules`, and equivalent AI coding tool configuration files by embedding hidden instructions using zero-width Unicode characters, invisible to human reviewers but parsed by the agent. These files are consumed as instruction context, not inert configuration, and must be treated as untrusted input when loaded from repositories or shared directories not under the operator's direct control. SC-2.2 (signed tool manifests) should be extended to cover any configuration file the agent reads as instruction context, alongside tool manifests and MCP server descriptors. This provenance concern extends to the agent's *own local settings*, not just files pulled from repositories: the AWS Kiro flaw (CVE-2026-10591, July 2026) let a hidden web prompt make the agent rewrite its own `~/.kiro/settings/mcp.json` to register and auto-launch an attacker-controlled MCP server. A file that lists the agent's tools is execution policy; provenance validation here has a write-side counterpart in [Execution Control](execution-control.md) EC-2.19 (config-file immutability), which keeps the agent from silently editing its own MCP manifest, hooks, and task runners in the first place.

**Treating model provider updates as safe by default.** Model providers update their models regularly - sometimes with notice, sometimes without. Each update is a supply chain change that can affect every agent in the system. Model version pinning (Tier 3) is the defensive measure, but even at Tier 2, organisations should monitor provider change logs and test updates before promoting them to production.

**Vetting MCP servers once and never again.** An MCP server that was safe at vetting time can become unsafe through updates, dependency changes, or maintainer compromise. Re-vetting must be periodic and triggered by any change. The 6-month periodic review is a backstop, not a target.

**AIBOM as a compliance document rather than an operational tool.** The AIBOM is useful only if it is compared against the deployed configuration automatically. A beautifully formatted AIBOM that sits in a wiki and diverges from reality is worse than no AIBOM - it provides false assurance.

**Approving a skill without checking it against the Lethal Trifecta.** A skill that combines access to private data (credentials, wallet files), exposure to untrusted content (its own instructions, retrieved documents), and the ability to communicate externally (network egress) has everything it needs to exfiltrate silently - this combination is what made the ClawHub/OpenClaw skills dangerous. OWASP's [Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/) (AST01-AST10) tracks this class separately from ASI04. Vet each skill against the trifecta explicitly before approval, not just against signing and provenance. SC-2.6 makes this enforceable: a manifest that grants all three legs is blocked by default. See [The Agent Supply Chain Crisis](../../insights/the-agent-supply-chain-crisis.md#the-lethal-trifecta).

**Trusting `allowed-tools` as a permission boundary.** The Agent Skills specification marks `allowed-tools` as experimental, and clients differ in whether and how they honour it. In Claude Code it is not a boundary at all: it pre-approves the listed tools and restricts nothing. It is written by the skill's author, so a malicious skill declares whatever it needs. Use it as a review input that should match the approved manifest, and enforce permissions from the registry, managed policy, and the sandbox (SC-2.6).

**Allowing agents to discover tools at runtime.** Dynamic tool discovery is the defining feature of MCP-based agent frameworks and the defining vulnerability of their supply chain. At Tier 1 and Tier 2, tool discovery must be disabled in favour of static allow-lists. Even at Tier 3, discovery should be limited to pre-approved registries with signed manifests.

**Treating the model provider as a runtime backstop.** Provider-side abuse monitoring, terms of service, and acceptable-use policies are governance controls, not runtime controls. The April 2026 Mexican government breach used Claude Code across 34 sessions, 1,088 prompts, and 5,317 commands without provider-side intervention interrupting the engagement. The OX Security MCP STDIO disclosure (April 2026) showed Anthropic explicitly declining to change a vulnerable protocol, declaring sanitisation a developer responsibility. Operators must assume that provider monitoring will not catch sustained misuse and that protocol-level fixes are not on a predictable timeline. Every supply chain claim must be enforceable by the operator: signed manifests verified locally, MCP gateways under operator control, and runtime integrity checks that do not depend on the provider's cooperation.

!!! info "References"
    - [Agent Skills specification](https://agentskills.io/specification)
    - [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)
    - [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)
    - [OWASP Top 10 for Agentic Applications (ASI04: Agentic Supply Chain)](https://genai.owasp.org/)
    - [SLSA: Supply-chain Levels for Software Artifacts](https://slsa.dev/)
