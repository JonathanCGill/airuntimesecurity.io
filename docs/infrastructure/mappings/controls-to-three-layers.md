# Controls to Three-Layer Mapping

> Maps all 80 infrastructure controls to the three-layer behavioral security pattern: **Guardrails → Model-as-Judge → Human Oversight**.
>
> Part of the [AI Security Infrastructure Controls](../README.md) framework.
> Companion to [AI Runtime Security](https://github.com/JonathanCGill/airuntimesecurity.io).

## How to Read This Mapping

Every infrastructure control supports all three layers of the behavioral security pattern. The table below summarises how each control contributes to each layer. Detailed descriptions are in the individual control documents.

The three layers operate as concentric defences:

- **Guardrails** prevent - they block or constrain before or during model execution.
- **Judge** detects - it evaluates outputs and behavior against policy, asynchronously.
- **Human Oversight** decides - humans review, approve, investigate, and adjust.

Infrastructure controls make these layers enforceable. Without the infrastructure, the behavioral pattern is aspirational.

## Identity & Access Management

| Control | Guardrails | Judge | Human Oversight |
|---------|-----------|-------|-----------------|
| **IAM-01** Authenticate all entities | Authentication gates prevent unauthorised access to model endpoints and tools | Judge receives verified identity context for evaluation, ensuring attributable actions | Human reviewers can trace every action to an authenticated identity |
| **IAM-02** Enforce least privilege | Permission boundaries limit what each entity can do - the primary access guardrail | Judge can detect actions that fall within permissions but outside expected behavioral patterns | Humans define and review permission sets; least privilege reduces scope of decisions requiring oversight |
| **IAM-03** Separate control/data planes | Prevents runtime paths from modifying security configuration - structural guardrail | Judge configuration is protected from manipulation via the data plane | Humans access control plane via MFA/VPN; configuration changes are human-only |
| **IAM-04** Constrain agent tool invocation | Gateway enforces tool manifest - the guardrail for all agent actions | Gateway logs feed Judge evaluation of agent tool usage patterns | Humans define manifests and review agent behavior against declared scope |
| **IAM-05** Human approval for high-impact actions | Approval routing pauses irreversible actions - guardrail that defers to humans | Judge evaluates the pattern of actions requiring approval and approval outcomes | Direct human involvement in high-impact decisions; the oversight layer in action |
| **IAM-06** Session-scoped credentials | Credential scope limits blast radius of compromise - time-bounded guardrail | Judge monitors credential usage patterns within sessions for anomalies | Session scope gives humans a bounded window to review; credentials expire automatically |
| **IAM-07** Prevent credential exposure in context | Out-of-band credential injection prevents extraction via prompt injection - fundamental guardrail | Judge monitors for credential-like patterns in model outputs as a detection signal | Humans design credential architecture; exposure incidents trigger human investigation |
| **IAM-08** Audit all access changes | Audit trail deters unauthorised changes - indirect guardrail via accountability | Judge can correlate access changes with subsequent behavioral changes in the system | Humans review access change audit trails; changes are attributable and reviewable |

## Logging & Observability

| Control | Guardrails | Judge | Human Oversight |
|---------|-----------|-------|-----------------|
| **LOG-01** Log all model I/O | Logged I/O enables guardrail effectiveness measurement and tuning | Model I/O logs are the primary input for Judge evaluation of outputs | I/O logs give humans the raw data to review what the model actually said |
| **LOG-02** Log guardrail decisions | Guardrail decision logs prove enforcement is active and measure block/pass rates | Judge uses guardrail decision logs to evaluate whether guardrails are functioning correctly | Humans review guardrail decision logs to tune rules and investigate bypasses |
| **LOG-03** Log Judge evaluations | Guardrail tuning is informed by Judge evaluation trends (feedback loop) | Judge evaluation logs enable meta-evaluation - assessing whether the Judge itself is effective | Humans review Judge logs to calibrate thresholds and assess Judge accuracy |
| **LOG-04** Log agent decision chains | Chain logs reveal when guardrails are being tested or probed by agent behavior | Judge reconstructs full agent chains to evaluate whether multi-step behavior was appropriate | Humans can forensically reconstruct what an agent did and why |
| **LOG-05** Detect behavioral drift | Drift detection is a guardrail that triggers when model behavior moves outside baseline bounds | Judge evaluation criteria can be updated based on drift detection signals | Drift alerts bring humans into the loop when automated systems detect change |
| **LOG-06** Detect prompt injection | Injection detection is a direct guardrail - blocking or flagging injection attempts | Judge evaluates whether injection attempts correlate with unusual model outputs | Injection detection alerts trigger human investigation of targeted attacks |
| **LOG-07** Protect log integrity | Log integrity ensures guardrail decision records cannot be tampered with | Judge relies on trustworthy logs - tampered logs produce unreliable evaluations | Humans need tamper-proof logs for audit, compliance, and investigation |
| **LOG-08** Enforce retention policies | Retention ensures guardrail and evaluation data is available for the required period | Judge evaluation data is retained for trend analysis and meta-evaluation | Humans have historical data for audits, investigations, and compliance |
| **LOG-09** Redact sensitive data in logs | PII redaction in logs prevents logging infrastructure from becoming a data leakage vector | Judge evaluates redacted logs - it does not need PII to assess behavioral patterns | Humans can review logs without exposure to unnecessary sensitive data |
| **LOG-10** Correlate with enterprise SIEM | SIEM correlation connects AI guardrail events with broader security monitoring | Judge signals (evaluation failures, drift alerts) feed enterprise detection capabilities | Security operations teams gain visibility into AI-specific events alongside traditional alerts |

## Network & Segmentation

| Control | Guardrails | Judge | Human Oversight |
|---------|-----------|-------|-----------------|
| **NET-01** Define network zone architecture | Zone boundaries are structural guardrails - they physically enforce separation | Judge infrastructure is isolated in its own zone, protecting evaluation independence | Zone architecture is designed by humans and enforced by infrastructure, not instructions |
| **NET-02** Prevent guardrail bypass at network level | Network-enforced guardrail bypass prevention - no path to the model that skips guardrails | Judge can verify from logs that all model interactions transited the guardrail path | Humans can audit network policy to confirm no bypass paths exist |
| **NET-03** Isolate Judge evaluation infrastructure | Judge isolation ensures guardrails cannot influence Judge evaluation | Direct protection of Judge independence - separate zone, async data flow, no runtime influence | Humans can verify Judge isolation through network policy review |
| **NET-04** Control agent egress destinations | Egress proxy is a network-level guardrail on agent external communications | Judge can evaluate egress patterns against expected behavior | Humans define egress allowlists and review blocked egress attempts |
| **NET-05** Separate ingestion from runtime | Ingestion isolation prevents poisoned data from reaching runtime directly - structural guardrail | Judge can monitor ingestion pipeline outputs independently from runtime | Humans control ingestion approval processes without runtime pressure |
| **NET-06** Protect control plane network path | Control plane protection prevents unauthorised modification of guardrail and Judge configuration | Judge configuration is protected by control plane network restrictions | Only authorised humans (MFA + VPN) can modify system configuration |
| **NET-07** Enforce API gateway as single entry | Single entry point ensures all guardrails are applied to every request | All model interactions transit a path that generates Judge-consumable logs | Gateway provides humans with a single point of monitoring and control |
| **NET-08** Monitor cross-zone traffic | Cross-zone monitoring detects anomalous traffic patterns that may indicate guardrail circumvention | Judge can incorporate cross-zone traffic anomalies as evaluation signals | Anomalous traffic alerts trigger human investigation |

## Data Protection

| Control | Guardrails | Judge | Human Oversight |
|---------|-----------|-------|-----------------|
| **DAT-01** Classify data at AI boundaries | Classification drives guardrail rules - what data can enter or leave the model context | Judge can evaluate whether data classification policies are being followed in model I/O | Classification provides humans with context for data handling decisions |
| **DAT-02** Enforce data minimisation | Minimisation is a guardrail that reduces the data available for exfiltration | Judge can evaluate whether model context contains more data than necessary for the task | Humans define minimisation policies based on data sensitivity and task requirements |
| **DAT-03** Detect and redact PII | PII detection and redaction is a direct input/output guardrail | Judge can evaluate PII detection effectiveness by monitoring for PII in post-guardrail outputs | PII incidents trigger human review and guardrail tuning |
| **DAT-04** Enforce access-controlled RAG | RAG access control is a guardrail ensuring users only retrieve documents they are authorised to see | Judge can detect patterns where RAG retrieval returns content inconsistent with user permissions | Humans define RAG access policies and review retrieval audit logs |
| **DAT-05** Encrypt data at rest and in transit | Encryption is an infrastructure guardrail protecting data if other controls fail | Judge evaluation data is encrypted, protecting evaluation integrity | Encryption provides humans with confidence that data is protected across all states |
| **DAT-06** Prevent sensitive data leakage via responses | Output scanning is a direct output guardrail - blocking responses containing sensitive data | Judge evaluates response patterns for data leakage that may not match known patterns | Leakage incidents trigger human investigation and guardrail rule updates |
| **DAT-07** Manage conversation history retention | Retention limits are a guardrail on context window accumulation - old data is purged | Judge can evaluate conversation history scope relative to task requirements | Humans define retention policies balancing utility with privacy requirements |
| **DAT-08** Protect evaluation data sent to Judge | Tokenisation of evaluation data is a guardrail protecting PII that transits to the Judge | Judge receives necessary context without unnecessary PII exposure | Humans define what data the Judge needs and how it is protected |

## Secrets & Credentials

| Control | Guardrails | Judge | Human Oversight |
|---------|-----------|-------|-----------------|
| **SEC-01** Never inject credentials into context windows | Context window exclusion is the fundamental credential guardrail - no credentials in the attack surface | Judge monitors for credential-like patterns in model I/O as a detection layer | Architecture designed by humans; violations trigger investigation |
| **SEC-02** Use short-lived, scoped tokens | Token scope and expiry are time-bounded guardrails that limit credential utility if compromised | Judge can detect token usage patterns outside expected scope or time windows | Short-lived tokens reduce the window humans have to respond to compromise |
| **SEC-03** Centralise secrets in a vault | Centralised vault is a structural guardrail - secrets have one controlled access path | Judge can monitor vault access patterns for anomalies | Humans manage vault policies and review access logs |
| **SEC-04** Scan model I/O for credential patterns | Credential pattern scanning is a direct I/O guardrail | Judge evaluates scanning effectiveness and correlates with other exfiltration signals | Scan alerts trigger human investigation and incident response |
| **SEC-05** Rotate credentials on exposure | Automatic rotation is a guardrail that limits the utility window of exposed credentials | Judge monitors for continued use of rotated credentials as a compromise indicator | Rotation events trigger human investigation of the exposure source |
| **SEC-06** Isolate agent credentials per session | Per-session isolation is a blast radius guardrail - compromise of one session doesn't affect others | Judge can detect credential usage inconsistent with session scope | Humans review session credential patterns and policy effectiveness |
| **SEC-07** Protect model endpoint credentials | Endpoint credential protection prevents unauthorised model access - an access guardrail | Judge can detect anomalous patterns in model endpoint authentication | Humans manage endpoint credential policies and rotation schedules |
| **SEC-08** Scan code and config for embedded credentials | Pre-deployment scanning is a preventive guardrail catching credentials before they reach production | Judge evaluation of deployment artefacts can include credential scanning results | Scan findings require human remediation before deployment proceeds |

## Supply Chain

| Control | Guardrails | Judge | Human Oversight |
|---------|-----------|-------|-----------------|
| **SUP-01** Verify model provenance | Provenance verification is a deployment guardrail - unverified models are blocked | Judge baselines are model-specific; verified provenance ensures valid baselines | Humans approve models for deployment based on provenance evidence |
| **SUP-02** Assess model risk before adoption | Risk assessment determines guardrail configuration requirements per model | Assessment results calibrate Judge evaluation criteria and thresholds | Humans conduct assessments and make adoption decisions |
| **SUP-03** Verify RAG data source integrity | Source allowlisting and content scanning are guardrails on the RAG ingestion path | Judge can evaluate whether retrieved content appears anomalous relative to known sources | Humans maintain source allowlists and review ingestion logs |
| **SUP-04** Secure fine-tuning pipeline | Pipeline security prevents training-time attacks - a guardrail on model creation | Post-training evaluation provides Judge with validated safety baselines | Humans approve training data, review evaluation results, and authorise deployment |
| **SUP-05** Audit tool and plugin supply chain | Tool registry and security assessment are guardrails on agent capability expansion | Judge can evaluate tool usage against declared capabilities, detecting anomalous patterns | Humans assess, approve, and monitor tools in the registry |
| **SUP-06** Verify guardrail and safety model integrity | Integrity verification protects the guardrails themselves - the most critical supply chain control | Judge model integrity is directly protected; compromise would defeat the evaluation layer | Humans approve guardrail/Judge changes and review tamper detection alerts |
| **SUP-07** Maintain AI-BOM | AI-BOM enables systematic guardrail coverage verification | AI-BOM tracks Judge model associations, ensuring consistent evaluation configuration | AI-BOM gives humans a single source of truth for what is deployed |
| **SUP-08** Monitor for vulnerabilities | Vulnerability monitoring triggers guardrail rule updates for new attack patterns | New vulnerabilities may require Judge evaluation criteria updates | Humans assess vulnerability impact and prioritise remediation |

## Incident Response

| Control | Guardrails | Judge | Human Oversight |
|---------|-----------|-------|-----------------|
| **IR-01** Define AI-specific incident categories | Category definitions guide guardrail monitoring - each category has associated detection rules | Judge evaluation failures are an explicit incident category, integrating Judge into IR | Humans use category definitions to triage and prioritise incidents |
| **IR-02** Establish detection triggers | Detection triggers are automated guardrails that escalate anomalies to incident status | Judge evaluations are a primary source of detection triggers | Detection triggers bring humans into the loop when automated systems detect problems |
| **IR-03** Define containment procedures | Containment procedures include guardrail hot-reload for rapid policy update | Containment may include Judge threshold adjustment to increase sensitivity | Humans execute containment decisions based on severity classification |
| **IR-04** Implement model rollback and hot-reload | Rollback and hot-reload enable rapid guardrail and model restoration | Judge configuration can be rolled back alongside model changes | Humans authorise rollback decisions and verify system recovery |
| **IR-05** Define investigation procedures | Investigation uses guardrail decision logs as primary evidence | Judge evaluation logs provide investigation context for output-related incidents | Humans conduct investigations using logs from all three layers |
| **IR-06** Establish communication protocols | Guardrail status is included in incident communications to stakeholders | Judge evaluation findings inform communication about impact assessment | Humans manage communications, disclosures, and stakeholder engagement |
| **IR-07** Conduct post-incident review | Post-incident reviews assess guardrail effectiveness and identify gaps | Post-incident reviews evaluate Judge detection performance and calibration | Humans lead reviews and implement improvements across all three layers |
| **IR-08** Integrate with enterprise IR | AI guardrail events feed enterprise IR workflows and SIEM | Judge signals integrate with enterprise detection and response capabilities | AI incidents are handled within existing human IR structures and escalation paths |

## Agentic - Tool Access

| Control | Guardrails | Judge | Human Oversight |
|---------|-----------|-------|-----------------|
| **TOOL-01** Declare tool permissions | Tool manifest is the guardrail - allowlist-based, deny by default | Judge evaluates whether tool usage patterns align with manifest intent | Humans define and approve manifests |
| **TOOL-02** Enforce at gateway | Gateway is the enforcement point - deterministic, injection-proof | Gateway logs are ground truth for Judge evaluation of agent actions | Gateway enforcement means human-approved policies are actually enforced |
| **TOOL-03** Constrain parameters | Parameter schemas are fine-grained guardrails within permitted tool access | Judge evaluates parameter patterns for anomalies within technically valid bounds | Humans define parameter constraints in the manifest |
| **TOOL-04** Classify by reversibility | Classification drives guardrail escalation - irreversible actions require more oversight | Judge calibrates evaluation depth by action class | Classification determines when humans are brought into the loop |
| **TOOL-05** Rate-limit invocations | Rate limits are quantitative guardrails preventing accumulation attacks | Rate limit proximity feeds Judge anomaly detection | Rate limit alerts surface sessions for human review |
| **TOOL-06** Log every invocation | Invocation logs prove guardrails are active and measure enforcement | Complete invocation logs are primary Judge input for agent evaluation | Logs give humans full visibility into agent actions |

## Agentic - Session & Scope

| Control | Guardrails | Judge | Human Oversight |
|---------|-----------|-------|-----------------|
| **SESS-01** Define session boundaries | Time/token/action limits are structural guardrails on agent runtime | Judge evaluates whether sessions approach or reach limits, signalling potential issues | Humans define session limits based on task requirements and risk |
| **SESS-02** Isolate sessions | Session isolation prevents cross-contamination - a blast radius guardrail | Judge evaluates each session independently; isolation ensures evaluation integrity | Humans review sessions individually without cross-session confusion |
| **SESS-03** Limit session scope | Task scope constraints prevent agents from exceeding their declared purpose | Judge evaluates whether actions within a session are consistent with the declared task | Humans define task scope and review sessions where scope boundaries were tested |
| **SESS-04** Implement progressive trust | Progressive trust starts with minimal permissions - a conservative guardrail that relaxes with evidence | Judge evaluates whether trust escalation is justified by the session's clean behavior history | Humans define trust escalation criteria and review escalation decisions |
| **SESS-05** Clean up session state | Session cleanup prevents state leakage - a guardrail on persistent attack surface | Judge evaluates cleanup completeness, detecting residual state that could affect future sessions | Humans define cleanup policies and review cleanup audit logs |

## Agentic - Delegation Chains

| Control | Guardrails | Judge | Human Oversight |
|---------|-----------|-------|-----------------|
| **DEL-01** Enforce least delegation | Permission intersection is the guardrail preventing privilege escalation through delegation | Judge evaluates delegation patterns for escalation attempts, even within technically valid permissions | Humans define permission sets; intersection ensures human-approved boundaries hold |
| **DEL-02** Maintain audit trail | Audit trail proves delegation guardrails are functioning | Complete chain logs are primary Judge input for multi-agent evaluation | Humans can reconstruct full chains for investigation and review |
| **DEL-03** Limit delegation depth | Depth limits are structural guardrails on chain complexity | Shorter chains are within Judge evaluation capacity; limits ensure evaluability | Depth limits keep chains tractable for human review |
| **DEL-04** Require explicit authorisation | Delegation manifests are guardrails on agent-to-agent trust | Judge verifies all delegations match declared authorisations | Humans define delegation topology through manifests |
| **DEL-05** Propagate user identity | Identity propagation ensures user permissions constrain the entire chain - a fundamental guardrail | User identity enables Judge to evaluate actions against user-level behavioral baselines | Every action in every chain is attributable to the initiating human |

## Agentic - Sandbox Patterns

| Control | Guardrails | Judge | Human Oversight |
|---------|-----------|-------|-----------------|
| **SAND-01** Execute in isolated sandboxes | Sandbox isolation is the guardrail boundary for generated code execution | Judge evaluates code behavior within the sandbox, using execution logs as evidence | Humans define isolation levels based on risk tier |
| **SAND-02** Restrict file system access | File system restrictions prevent generated code from accessing data outside declared scope | Judge monitors file access patterns for anomalies | Humans define allowed paths and review access violations |
| **SAND-03** Restrict network access | Default-deny network is a guardrail preventing code from communicating externally | Judge evaluates any permitted network access for anomalous patterns | Humans approve exceptions to default-deny network policy |
| **SAND-04** Enforce resource limits | Resource limits are guardrails against denial of service and resource abuse | Judge monitors resource consumption patterns for anomalies | Humans define resource limits and review high-consumption sessions |
| **SAND-05** Prevent persistent state | Ephemeral environments prevent state accumulation - a guardrail on long-term compromise | Judge evaluates that session state does not persist beyond session boundaries | Humans verify ephemeral policy compliance |
| **SAND-06** Scan code before execution | Pre-execution scanning is a guardrail catching malicious or dangerous code before it runs | Judge evaluates scanning results alongside execution behavior | Humans review scan findings and define scanning policy |

