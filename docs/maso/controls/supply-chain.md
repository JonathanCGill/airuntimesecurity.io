---
as_at: "2026-11-03"
description: "MASO supply chain controls: inventorying, vetting, and integrity-verifying every model, tool, MCP server, skill, and plugin in multi-agent AI systems. Maps to OWASP LLM03, ASI04, and the Agentic Skills Top 10."
---

# MASO (Multi-Agent Security Operations) Control Domain: Supply Chain

> Part of the [MASO Framework](../README.md) · Control Specifications
> Covers: LLM03 (Supply Chain Vulnerabilities) · ASI04 (Agentic Supply Chain) · AST01-AST10 (OWASP Agentic Skills Top 10, see [mapping](../reference.md#owasp-agentic-skills-top-10-2026))
> Also covers: HF-02 (Accountability - AIBOM component)

## Principle

Every component in the agent system - models, tools, MCP servers, skills, RAG sources, plugins, and protocol endpoints - is a supply chain dependency. Each dependency is inventoried, versioned, integrity-verified, and auditable. No component is loaded at runtime without prior vetting and signing. The supply chain attack surface scales linearly with the number of agents and exponentially with the number of dynamic integrations.

## Why This Matters in Multi-Agent Systems

**The supply chain multiplies with every agent.** A single-model system has one model provider, one set of tools, one RAG configuration. A three-agent system may have three different model providers, nine tool integrations, three RAG sources, and two MCP server connections. Each additional dependency is an additional attack surface.

**Dynamic composition at runtime.** Modern agent frameworks support dynamic tool discovery and composition - an agent can discover and use an MCP server it has never interacted with before. This is powerful for flexibility and catastrophic for security. A poisoned MCP tool descriptor can trick an agent into passing credentials as tool parameters, executing unintended operations, or loading malicious code.

**Model provider changes propagate silently.** When a model provider updates their model (version change, fine-tuning update, safety filter modification), every agent using that model is affected simultaneously. If the update introduces a regression - reduced safety filtering, changed behavior on edge cases, or degraded quality - the agents inherit the regression with no notice.

**Skills are instructions, not just code.** An agent skill (a `SKILL.md` package, a plugin, a hook, or an agent configuration file such as `CLAUDE.md` or `.cursorrules`) bundles natural-language instructions with optional scripts and runs with the full permissions of the agent that loads it. Signing and dependency scanning were built for code. They say nothing about prose that tells the agent to read `~/.ssh` and post it somewhere, or about a URL the skill tells the agent to read at runtime. OWASP's [Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/) (AST10) catalogues the resulting risk class. Controls SC-1.5, SC-2.5 to SC-2.8, and SC-3.6 below exist because of it. In a multi-agent system the exposure compounds: one poisoned skill loaded by an orchestrator shapes every task it delegates.

**Credential harvesting through tool manifests.** A poisoned tool manifest can describe a tool that requires "authentication tokens" as parameters. The agent, following its instructions to use the tool, passes credentials to the attacker's endpoint. This is a supply chain attack that doesn't require compromising the agent's code - only its tool configuration.

## Controls by Tier

### Tier 1 - Supervised

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **SC-1.1** Model inventory | Every model used by every agent is documented: provider, version, API endpoint, date of last known update | Reviewed monthly. |
| **SC-1.2** Tool inventory | Every tool available to every agent is documented: name, source, version, permission scope | No undocumented tool integrations. |
| **SC-1.3** Fixed toolsets | Agents use a predefined, static set of tools. No runtime discovery or dynamic composition | New tools require a change request and security review. |
| **SC-1.4** RAG source inventory | Every RAG/vector database is documented per agent: source, update frequency, access controls | Enables traceability when poisoning is suspected. |
| **SC-1.5** Skill inventory and installation control | Every skill, plugin, hook, and instruction-bearing configuration file loaded by any agent is inventoried with source, version, content hash, installer identity, and accountable owner. Only the platform team installs skills; individual users and agents cannot | Skills from public registries are not installed directly: they are copied into a private curated registry after review, and agents load only from that registry. Ownership is reassigned or the skill revoked when its owner leaves. Addresses AST01, AST02, AST09. |

### Tier 2 - Managed

All Tier 1 controls remain active, plus:

| Control | Requirement | Implementation Notes |
|---------|-------------|---------------------|
| **SC-2.1** AIBOM per agent | AI Bill of Materials generated for each agent: models, tools, RAG sources, MCP servers, dependencies, and their versions | Updated on every deployment. Stored alongside the agent's configuration. |
| **SC-2.2** Signed tool manifests | Tool manifests cryptographically signed; agents reject unsigned or tampered manifests | Signing key managed by the platform team, not the tool provider. |
| **SC-2.3** MCP server allow-listing | Agents can only connect to pre-approved MCP servers | Allow-list maintained by the AI security team. New MCP servers require vetting before addition. |
| **SC-2.4** Runtime integrity checks | Tool, MCP server, and skill integrity verified at load time against signed manifests | Integrity failure blocks loading and triggers an alert. |
| **SC-2.5** Skill definition validation | Skill metadata and definition files (`SKILL.md` front matter, `skill.json`, `manifest.json`, `package.json`) are validated against a strict schema with safe parsers before load. Hidden characters, encoded instruction blocks, and names or publishers that impersonate a known brand are rejected | No unsafe deserialisation (for example PyYAML `!!python/object` tags). Reject zero-width Unicode, bidirectional control characters, and unexplained base64 in instruction text. A skill ported from another platform is re-validated on the target platform, never assumed equivalent. Applies [EC-2.15](execution-control.md) strict parsing to the load path. Addresses AST04, AST10. |
| **SC-2.6** Per-skill permission manifest | Each skill declares the minimum filesystem paths, network destinations, shell access, and credentials it needs. The platform enforces the manifest at runtime; the skill cannot widen it | A skill's effective permissions are the intersection of its manifest and the agent's own scope ([IA-1.4](identity-and-access.md)), never the agent's full scope. A skill whose manifest grants all three legs of the Lethal Trifecta (private data, untrusted content, external communication) is blocked unless a named owner approves it with an egress allow-list. Where the target platform has no manifest format, the permissions are enforced in the sandbox instead ([EC-2.2](execution-control.md)). Addresses AST03, AST10. |
| **SC-2.7** External instruction pinning | Content a skill directs the agent to read at runtime (remote documentation, runbooks, schemas, scripts) is either inlined into the reviewed skill or pinned by content hash and verified on every fetch. Unpinned external content is tagged as data, not instruction | A signed skill that points at a mutable URL is only as trustworthy as whoever controls that URL tomorrow. Hash mismatch fails closed and triggers re-vetting. Fetched content carries `type: "data"` under [PG-1.4](prompt-goal-and-epistemic-integrity.md). Addresses AST05. |
| **SC-2.8** Skill version and source pinning | Skills are pinned by content hash, not by name, tag, or `latest`. Auto-update and hot-reload are disabled. Any new version, change of maintainer, or change of ownership of the source account or repository re-enters review | A "patch" release is an unverified new artefact until reviewed. A skill served from a repository whose owner account was deleted or transferred is treated as compromised until re-vetted. Addresses AST02, AST07. |

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
| Skills | Skills, plugins, and hooks with content hash, source registry, pinned external references, and permission manifest hash | `[{name: "report-formatter", hash: "sha256:mno...", registry: "internal", external_refs: [{url: "https://...", hash: "sha256:pqr..."}]}]` |
| MCP Servers | Connected MCP servers with endpoint and manifest hash | `[{name: "internal-search", endpoint: "https://...", hash: "sha256:def..."}]` |
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
| Credential handling | Does the tool request credentials as parameters? (Red flag - credentials should be injected by the platform, not passed by the agent.) |
| Network behavior | What external endpoints does the MCP server contact? Are they documented and expected? |
| Data handling | What data does the MCP server access, store, or transmit? Does it comply with the agent's data classification? |
| Update mechanism | How is the MCP server updated? Can updates change tool behavior without notice? |
| Signing | Can the manifest be cryptographically signed? Is the signing key managed appropriately? |

**Approval authority:** AI security team for Tier 2. AI Security Architect for Tier 3 (higher bar due to autonomous usage).

**Re-vetting triggers:** Any update to the MCP server, change in maintainer, security advisory affecting the server's dependencies, or a 6-month periodic review - whichever comes first.

## Testing Criteria

### Tier 1 Tests

| Test ID | Test | Pass Criteria |
|---------|------|---------------|
| SC-T1.1 | Inventory accuracy | Compare documented model, tool, and RAG inventories against actual agent configurations. No undocumented components. |
| SC-T1.2 | Fixed toolset enforcement | Attempt to add a tool to an agent's configuration without going through the change process. Attempt is blocked or detected. |
| SC-T1.3 | Inventory freshness | Verify inventories have been reviewed within the last 30 days. |
| SC-T1.4 | Unauthorised skill installation | As a non-platform user, and separately via an agent instruction, attempt to install a skill from a public registry. Installation is blocked and logged. |

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
| **Defined** | AIBOM per agent. Signed tool manifests. MCP server allow-listing with vetting process. Runtime integrity checks. Skills validated, permission-scoped, and pinned by hash, including their external references. |
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

**Allowing agents to discover tools at runtime.** Dynamic tool discovery is the defining feature of MCP-based agent frameworks and the defining vulnerability of their supply chain. At Tier 1 and Tier 2, tool discovery must be disabled in favour of static allow-lists. Even at Tier 3, discovery should be limited to pre-approved registries with signed manifests.

**Treating the model provider as a runtime backstop.** Provider-side abuse monitoring, terms of service, and acceptable-use policies are governance controls, not runtime controls. The April 2026 Mexican government breach used Claude Code across 34 sessions, 1,088 prompts, and 5,317 commands without provider-side intervention interrupting the engagement. The OX Security MCP STDIO disclosure (April 2026) showed Anthropic explicitly declining to change a vulnerable protocol, declaring sanitisation a developer responsibility. Operators must assume that provider monitoring will not catch sustained misuse and that protocol-level fixes are not on a predictable timeline. Every supply chain claim must be enforceable by the operator: signed manifests verified locally, MCP gateways under operator control, and runtime integrity checks that do not depend on the provider's cooperation.

