---
description: "Infrastructure controls for AI incident response: detection, classification, containment, and recovery procedures for prompt injection, data leakage, and model failures."
---

# Incident Response for AI Systems

> **Control Domain:** Response Controls  
> **Purpose:** Define AI-specific incident detection, classification, response, and recovery procedures that extend the organisation's existing IR capability.  
> **Relationship:** Relies on the Logging controls (LOG-01 through LOG-10) for detection data, the IAM controls for containment actions, and the three-layer model for escalation pathways.

## Why AI Incident Response Is Different

Traditional incident response follows a pattern: detect, contain, eradicate, recover. AI incidents introduce complications that break conventional IR assumptions:

| Assumption | Traditional IR | AI Systems |
|-----------|---------------|------------|
| **You can identify the payload** | Malware has a hash, an exploit has a CVE | Prompt injection is natural language - no signature |
| **You can isolate the affected system** | Take the server offline | The model is stateless - the "infection" is in the prompt, not the system |
| **You can determine impact** | Forensics reveals what the attacker accessed | AI context windows are ephemeral - what the model "saw" may not be fully logged |
| **You can prevent recurrence** | Patch the vulnerability | The same injection technique can be paraphrased infinitely |
| **Root cause is identifiable** | Vulnerability + exploit chain | Model behavior is non-deterministic - the same input might not reproduce the issue |

The core problem: **AI incidents often involve behavioral failures rather than system compromises.** The model isn't "hacked" in the traditional sense - it's manipulated into behaving in ways that violate policy. This requires IR procedures that address behavior, not just infrastructure.

## Control Objectives

| ID | Objective | Risk Tiers |
|----|-----------|------------|
| IR-01 | Define AI-specific incident categories and severity levels | All |
| IR-02 | Establish AI incident detection triggers from logging and monitoring | All |
| IR-03 | Define containment procedures for AI-specific incidents | All |
| IR-04 | Implement model rollback and guardrail emergency update capability | Tier 2+ |
| IR-05 | Define investigation procedures for non-deterministic systems | Tier 2+ |
| IR-06 | Establish communication protocols for AI incidents | Tier 2+ |
| IR-07 | Conduct post-incident review with AI-specific root cause analysis | All |
| IR-08 | Integrate AI IR with enterprise IR processes | All |

## IR-01: AI Incident Categories

Standard incident categories (malware, unauthorised access, data breach) don't adequately describe AI-specific incidents. Define additional categories:

### AI-Specific Incident Types

![AI Incident Classification](../diagrams/incident-classification.svg)

| Category | Description | Example |
|----------|-------------|---------|
| **Prompt injection - successful** | Attacker bypassed guardrails and manipulated model behavior | Model disclosed system prompt, executed unintended tool calls |
| **Prompt injection - attempted** | Guardrails or Judge detected injection attempt | Blocked injection, but technique is novel and needs analysis |
| **Guardrail failure** | Guardrails passed content that should have been blocked | PII in output not caught, harmful content not filtered |
| **Judge disagreement** | Judge flagged content that guardrails passed (or vice versa) at significant rates | Systemic gap between detection layers |
| **Model behavioral drift** | Model behavior shifted outside baseline parameters | Response quality degradation, topic drift, tone changes |
| **Data poisoning** | Malicious content entered the vector store or training pipeline | Manipulated RAG responses, biased fine-tuning outcomes |
| **Agent autonomy violation** | Agent took actions outside its declared permission set | Unauthorised tool invocation, exceeded scope |
| **Credential exposure** | Credentials appeared in model context, output, or logs | API key in model response, token in log file |
| **Context window exfiltration** | Sensitive data extracted from model context via adversarial prompts | System prompt, other users' data, retrieved documents leaked |
| **Evaluation failure** | Judge system failed, producing no evaluations during a period | Monitoring gap, undetected issues during failure window |

### Severity Classification

| Severity | Criteria |
|----------|----------|
| **Critical** | Active data breach via AI system, successful agent autonomy violation with impact, credential compromise with confirmed exploitation |
| **High** | Successful prompt injection with policy violation, guardrail failure on Tier 3+ system, data poisoning confirmed |
| **Medium** | Novel injection technique detected (even if blocked), guardrail/Judge disagreement exceeding threshold, model drift beyond baseline |
| **Low** | Known injection technique blocked, single-instance guardrail false negative, minor drift within recovery parameters |

## IR-02: Detection Triggers

AI incidents are detected through the logging and monitoring infrastructure (LOG-01 through LOG-10). Define specific triggers:

### Automated Detection

| Trigger | Source | Incident Category |
|---------|--------|-------------------|
| Guardrail block rate spike (>2σ) | LOG-05 | Potential injection campaign |
| Judge escalation rate exceeds threshold | LOG-03, LOG-05 | Guardrail failure or model drift |
| Credential pattern in model I/O | SEC-04 | Credential exposure |
| Agent tool call to undeclared endpoint | LOG-04, NET-04 | Agent autonomy violation |
| System prompt hash mismatch | LOG-01, IAM-08 | Configuration tampering |
| Cross-zone traffic anomaly | NET-08 | Potential compromise |
| Single user generating anomalous volume | LOG-05 | Adversarial probing |
| Judge availability below SLA | LOG-03 | Evaluation failure |
| Vector store content classification change | SUP-03 | Potential data poisoning |

### Human-Reported

- User reports unexpected model behavior.
- Security team identifies AI-related IoCs during other investigations.
- Vendor notifies of model vulnerability or incident.
- Regulatory or legal inquiry triggers review.

## IR-03: Containment Procedures

AI containment differs from traditional containment. You can't "quarantine" a stateless model - but you can restrict what reaches it and what it can do.

### Containment Actions by Severity

| Severity | Containment Action |
|----------|-------------------|
| **Critical** | Disable the AI system endpoint. Route traffic to a static fallback. Revoke all agent credentials. Preserve logs. |
| **High** | Increase guardrail strictness (lower thresholds). Disable agent tool access. Enable synchronous Judge evaluation (block on flag). Increase logging verbosity. |
| **Medium** | Add targeted guardrail rules for the detected technique. Increase monitoring for the affected category. Alert human reviewers. |
| **Low** | Log for analysis. Update guardrail rules in next scheduled release. No immediate containment required. |

### AI-Specific Containment Principles

- **Fail safe, not fail open:** If the guardrail system fails, block all traffic rather than allowing unfiltered access to the model.
- **Preserve forensic data:** Before containment actions change system behavior, ensure current logs and configurations are preserved.
- **Contain the session, not the system:** If a single user session is compromised (injection, exfiltration), terminate that session without disabling the entire system (unless the attack vector is systemic).
- **Credential rotation is containment:** Any credential exposure triggers immediate rotation as a containment action, not a later remediation step.

## IR-04: Rollback and Emergency Updates

The ability to rapidly roll back model deployments and update guardrails is critical for AI incident response.

### Requirements

- **Model rollback:** The ability to revert to a previous known-good model version within minutes, not hours.
- **Guardrail emergency update:** The ability to deploy new guardrail rules (to block a newly discovered injection technique) without a full deployment cycle.
- **Judge criteria update:** The ability to update evaluation criteria to catch a newly identified failure mode.
- **Vector store rollback:** The ability to remove recently ingested documents that may be poisoned.
- **Agent permission reduction:** The ability to immediately reduce agent permissions without redeployment.

### Deployment Requirements

- Pre-staged rollback artefacts for current-1 and current-2 model versions.
- Guardrail rule hot-reload capability (update rules without restarting the guardrail service).
- Blue/green or canary deployment for model updates, enabling rapid rollback.
- Agent permission sets managed as configuration, not code - enabling runtime updates.

## IR-05: Investigation Procedures

AI incident investigation must account for non-determinism. The same input may not reproduce the same output, making traditional reproduction-based debugging insufficient.

### Investigation Framework

1. **Reconstruct the interaction:** Use LOG-01 (model I/O) and LOG-04 (agent chains) to reconstruct exactly what happened during the incident.
2. **Identify the trigger:** What input or sequence of inputs caused the undesired behavior? Was it a single prompt or a multi-turn escalation?
3. **Assess guardrail performance:** Did guardrails evaluate the input/output? What was the confidence score? Did they pass content they should have blocked (LOG-02)?
4. **Assess Judge performance:** Did the Judge evaluate the interaction? What was the verdict? Was there a guardrail/Judge disagreement (LOG-03)?
5. **Determine scope:** Was this an isolated incident or part of a pattern? Search logs for similar inputs, techniques, or user behavior.
6. **Assess impact:** What data was exposed, what actions were taken, what decisions were influenced? For agent incidents, reconstruct the full action chain.
7. **Identify the control gap:** Which control failed? Was it a guardrail rule gap, a Judge criteria gap, a network bypass, or a permission misconfiguration?
8. **Attempt reproduction:** Try to reproduce the behavior in a sandboxed environment. Accept that non-determinism may prevent exact reproduction - focus on reproducing the *category* of failure.

## IR-06: Communication Protocols

AI incidents may require communication with stakeholders who don't exist in traditional IR:

| Stakeholder | When to Notify | What to Communicate |
|-------------|---------------|---------------------|
| **Model provider** | Model vulnerability exploited, unexpected model behavior | Technique details (sanitised), impact, request for guidance |
| **Data subjects** | PII exposed via AI system | What was exposed, how, remediation steps |
| **Regulators** | Reportable breach involving AI system, EU AI Act compliance failure | Incident details per regulatory requirements |
| **AI ethics/governance board** | Bias incident, harmful output to vulnerable user, autonomy violation | Full incident report, proposed controls |
| **Affected users** | User received harmful, incorrect, or manipulated AI output | What happened, corrective actions, how to verify |
| **Executive leadership** | Critical or high severity, reputational risk, regulatory exposure | Business impact summary, containment status, timeline |

## IR-07: Post-Incident Review

AI post-incident reviews must go beyond traditional root cause analysis to address the non-deterministic nature of AI failures.

### Review Elements

- **Timeline reconstruction** using LOG-01 through LOG-04 data.
- **Control gap analysis:** Which layer of the three-layer model failed, and why?
- **Guardrail rule update:** If guardrails missed the issue, what new rules are needed?
- **Judge criteria update:** If the Judge missed the issue, what evaluation criteria need refinement?
- **Detection improvement:** How can this incident type be detected earlier/faster?
- **Injection technique catalogue:** If prompt injection was involved, add the technique to the internal injection pattern library (LOG-06).
- **Baseline update:** If model drift was involved, update behavioral baselines (LOG-05).
- **Non-determinism acknowledgement:** Accept that some AI failures may not have a single root cause. Focus on strengthening detection and response capability rather than expecting prevention of all possible failures.

## IR-08: Enterprise IR Integration

AI incident response must integrate with the existing enterprise IR process, not replace it.

### Integration Points

- AI incident categories map to the enterprise incident taxonomy.
- AI severity levels align with enterprise severity levels.
- AI incidents are tracked in the enterprise incident management system.
- AI incidents that involve data breach, unauthorised access, or compliance violations trigger the enterprise IR playbook in parallel.
- AI-specific forensic data (model I/O logs, agent chains, guardrail decisions) is available to the enterprise IR team.
- AI incidents contribute to the enterprise risk register and inform control investment decisions.

## Three-Layer Mapping

| Control | Guardrails | Model-as-Judge | Human Oversight |
|---------|-----------|--------------|-----------------|
| IR-01 Categories | Guardrail failure as incident category | Judge failure as incident category | Humans classify and prioritise |
| IR-02 Detection | Guardrail log anomalies trigger detection | Judge flag rate triggers detection | Humans review escalated alerts |
| IR-03 Containment | Guardrail strictness increased | Judge switched to synchronous mode | Humans authorise containment actions |
| IR-04 Rollback | Guardrail rules hot-reloaded | Judge criteria updated | Humans authorise rollback decisions |
| IR-05 Investigation | Guardrail logs provide evidence | Judge logs provide evidence | Humans conduct investigation |
| IR-06 Communication | Guardrail status communicated | Judge status communicated | Humans manage stakeholder communication |
| IR-07 Post-incident | Guardrail rules updated | Judge criteria refined | Humans lead review process |
| IR-08 Integration | Guardrail data feeds enterprise SIEM | Judge data feeds enterprise SIEM | Humans bridge AI and enterprise IR teams |

## Platform-Neutral Implementation Checklist

- [ ] AI-specific incident categories defined and integrated with enterprise taxonomy
- [ ] Detection triggers configured from logging, monitoring, and cross-zone telemetry
- [ ] Containment procedures defined per severity level with fail-safe defaults
- [ ] Model rollback capability tested and achievable within minutes
- [ ] Guardrail emergency update (hot-reload) capability verified
- [ ] Investigation procedures account for non-determinism and multi-step agent chains
- [ ] Communication protocols defined for AI-specific stakeholders
- [ ] Post-incident review template includes three-layer gap analysis
- [ ] AI incidents tracked in enterprise incident management system
- [ ] Injection technique catalogue maintained and updated from incidents

