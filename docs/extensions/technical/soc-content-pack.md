# SOC Content Pack for AI Security

> Ready-to-deploy detection rules, correlation searches, and dashboard definitions for AI system monitoring.

This content pack extends the [SOC Integration](soc-integration.md) architecture guide with concrete, platform-specific detection content. Import what applies to your SIEM. Ignore the rest.

## Prerequisites

Before deploying these rules, ensure:

1. AI security events are flowing to your SIEM in the [standard log format](soc-integration.md#log-format).
2. The `ai_security` index (or equivalent) is created and receiving data.
3. Correlation IDs are propagated across API gateway → application → LLM provider → Judge (see [SOC Integration: Identity Correlation](soc-integration.md#identity-correlation)).
4. Alert routing is configured to the AI Platform Team and SOC queues.

## Detection Rules

### 1. Prompt Injection - Repeated Attempts

**What it detects:** A single user making multiple prompt injection attempts in a short window, indicating active adversarial probing.

**Splunk SPL:**
```spl
index=ai_security category="prompt_attack"
| stats count as attempt_count, dc(endpoint) as endpoints_targeted,
        values(endpoint) as target_list by user_id, src_ip
| where attempt_count > 3
| eval severity=case(attempt_count > 10, "critical", attempt_count > 5, "high", 1=1, "medium")
```

**Sentinel KQL:**
```kql
AISecurity_CL
| where category_s == "prompt_attack"
| summarize attempt_count=count(), endpoints_targeted=dcount(endpoint_s),
            target_list=make_set(endpoint_s) by user_id_s, src_ip_s, bin(TimeGenerated, 15m)
| where attempt_count > 3
| extend severity = case(attempt_count > 10, "critical", attempt_count > 5, "high", "medium")
```

**Datadog Log Query:**
```
service:ai_security @category:prompt_attack | stats count by @user_id,@src_ip | filter count > 3
```

| Field | Value |
|---|---|
| **Severity** | Medium–Critical (scales with volume) |
| **MITRE ATLAS** | AML.T0051 - LLM Prompt Injection |
| **Framework Control** | LOG-06, NET-02 |
| **Response** | Block user after 10 attempts. Capture full payloads for threat intel. |

### 2. Judge Flag Clustering - High-Severity Burst

**What it detects:** Multiple high-confidence Judge flags for the same user or endpoint in a short period, indicating sustained policy violation or coordinated attack.

**Splunk SPL:**
```spl
index=ai_security category="judge_flag" judge_score>0.8
| stats count as flag_count, avg(judge_score) as avg_score,
        values(policy_violated) as policies by user_id, endpoint
| where flag_count > 5
| sort -flag_count
```

**Sentinel KQL:**
```kql
AISecurity_CL
| where category_s == "judge_flag" and judge_score_d > 0.8
| summarize flag_count=count(), avg_score=avg(judge_score_d),
            policies=make_set(policy_violated_s) by user_id_s, endpoint_s, bin(TimeGenerated, 1h)
| where flag_count > 5
| order by flag_count desc
```

| Field | Value |
|---|---|
| **Severity** | High |
| **Framework Control** | Judge Assurance, LOG-01 |
| **Response** | Triage per [Judge Flag procedure](soc-integration.md#judge-flag-medium-severity). Escalate if multiple policies violated. |

### 3. Data Exfiltration - Anomalous Output Volume

**What it detects:** Model responses significantly larger than baseline, suggesting bulk data extraction or structured data exfiltration.

**Splunk SPL:**
```spl
index=ai_security
| stats avg(tokens_out) as baseline_tokens by endpoint
| join endpoint [
    search index=ai_security
    | where tokens_out > 0
    | eval ratio=tokens_out/tokens_in
]
| where tokens_out > (baseline_tokens * 5) OR ratio > 20
| table _time, user_id, endpoint, tokens_in, tokens_out, ratio, baseline_tokens
```

**Sentinel KQL:**
```kql
let baseline = AISecurity_CL
| summarize avg_tokens=avg(tokens_out_d) by endpoint_s;
AISecurity_CL
| join kind=inner baseline on endpoint_s
| extend ratio = tokens_out_d / max_of(tokens_in_d, 1)
| where tokens_out_d > (avg_tokens * 5) or ratio > 20
| project TimeGenerated, user_id_s, endpoint_s, tokens_in_d, tokens_out_d, ratio
```

| Field | Value |
|---|---|
| **Severity** | High |
| **MITRE ATLAS** | AML.T0024 - Exfiltration via ML Inference API |
| **Framework Control** | DAT-06, NET-04 |
| **Response** | Investigate user activity. Check if output contains structured data, PII, or credential patterns. |

### 4. Agent Boundary Violation - Unauthorised Tool Use

**What it detects:** An agent attempting to invoke tools outside its declared permission set, indicating prompt injection, goal hijacking, or misconfiguration.

**Splunk SPL:**
```spl
index=ai_security category="agent_boundary_violation"
| stats count as violation_count, values(tool_attempted) as tools_attempted,
        values(agent_id) as agents by user_id, endpoint
| where violation_count >= 1
```

**Sentinel KQL:**
```kql
AISecurity_CL
| where category_s == "agent_boundary_violation"
| summarize violation_count=count(), tools_attempted=make_set(tool_attempted_s),
            agents=make_set(agent_id_s) by user_id_s, endpoint_s, bin(TimeGenerated, 1h)
| where violation_count >= 1
```

| Field | Value |
|---|---|
| **Severity** | High (single event is significant) |
| **OWASP Agentic** | ASI02 (Tool Misuse and Exploitation), ASI03 (Identity and Privilege Abuse) |
| **Framework Control** | IAM-04, TOOL-01, TOOL-02 |
| **Response** | Halt agent immediately. Determine if prompt injection triggered the tool call. Review full conversation context. |

### 5. Guardrail Bypass - Successful Attack

**What it detects:** A guardrail passed a request but the Judge subsequently flagged the same transaction as a policy violation - indicating the guardrail was bypassed.

**Splunk SPL:**
```spl
index=ai_security guardrail_result="pass" category="judge_flag" judge_score>0.9
| stats count as bypass_count by user_id, endpoint, policy_violated
| where bypass_count >= 1
| eval severity="critical"
```

**Sentinel KQL:**
```kql
AISecurity_CL
| where guardrail_result_s == "pass" and category_s == "judge_flag" and judge_score_d > 0.9
| summarize bypass_count=count() by user_id_s, endpoint_s, policy_violated_s, bin(TimeGenerated, 1h)
| where bypass_count >= 1
```

| Field | Value |
|---|---|
| **Severity** | Critical |
| **Framework Control** | Guardrails + Judge Assurance, bypass-prevention |
| **Response** | This is a confirmed guardrail gap. Escalate to AI Security team. Update guardrail rules. Review all transactions from this user in the window. |

### 6. Model Drift - Judge Accuracy Degradation

**What it detects:** Judge evaluation metrics shifting over time - increasing false positive/negative rates or declining agreement with human reviewers.

**Splunk SPL:**
```spl
index=ai_security category="judge_flag"
| bin _time span=1d
| stats count as total_flags, avg(judge_score) as avg_score by _time, judge_model
| streamstats window=7 avg(avg_score) as rolling_avg_score
| where abs(avg_score - rolling_avg_score) > 0.15
```

**Sentinel KQL:**
```kql
AISecurity_CL
| where category_s == "judge_flag"
| summarize total_flags=count(), avg_score=avg(judge_score_d) by bin(TimeGenerated, 1d), judge_model_s
| order by TimeGenerated asc
| serialize
| extend rolling_avg = avg_of(prev(avg_score, 1), prev(avg_score, 2), prev(avg_score, 3),
                               prev(avg_score, 4), prev(avg_score, 5), prev(avg_score, 6), avg_score)
| where abs(avg_score - rolling_avg) > 0.15
```

| Field | Value |
|---|---|
| **Severity** | Medium |
| **Framework Control** | Judge Assurance, operational-metrics |
| **Response** | Investigate whether the model provider updated the Judge model. Trigger human calibration review per [Judge Assurance](../../core/judge-assurance.md). |

### 7. Credential Exposure - Secrets in Model I/O

**What it detects:** Credential patterns (API keys, tokens, connection strings) appearing in model inputs or outputs despite guardrail scanning.

**Splunk SPL:**
```spl
index=ai_security (category="credential_detected" OR category="guardrail_block" policy_violated="credential_exposure")
| stats count as detection_count, values(credential_type) as cred_types by user_id, endpoint, direction
| where detection_count >= 1
```

**Sentinel KQL:**
```kql
AISecurity_CL
| where category_s == "credential_detected" or
        (category_s == "guardrail_block" and policy_violated_s == "credential_exposure")
| summarize detection_count=count(), cred_types=make_set(credential_type_s) by user_id_s, endpoint_s, direction_s
| where detection_count >= 1
```

| Field | Value |
|---|---|
| **Severity** | High |
| **Framework Control** | SEC-04, SEC-05, IAM-07 |
| **Response** | Treat exposed credential as compromised. Trigger immediate rotation (SEC-05). Investigate whether credential was exfiltrated. |

### 8. Anomalous Usage Pattern - Off-Hours / Geo Shift

**What it detects:** AI system usage from a user during unusual hours or from an unexpected geographic location, correlated with AI-specific indicators.

**Splunk SPL:**
```spl
index=ai_security
| iplocation src_ip
| stats count as request_count, values(Country) as countries,
        earliest(_time) as first_seen, latest(_time) as last_seen by user_id
| where (request_count > 50 AND (date_hour < 6 OR date_hour > 22))
        OR mvcount(countries) > 1
```

**Sentinel KQL:**
```kql
AISecurity_CL
| extend geo = geo_info_from_ip_address(src_ip_s)
| summarize request_count=count(), countries=make_set(tostring(geo.country)),
            first_seen=min(TimeGenerated), last_seen=max(TimeGenerated) by user_id_s
| where request_count > 50 or array_length(countries) > 1
```

| Field | Value |
|---|---|
| **Severity** | Medium |
| **Framework Control** | LOG-01, IAM-01 |
| **Response** | Cross-reference with HR/IdP for travel. If not explained, treat as potential account compromise. |

## Correlation Searches

These rules combine multiple AI security signals to surface compound threats.

### Compound: Injection Followed by Exfiltration

A prompt injection attempt from a user, followed by a high-volume output within the same session, suggests a successful attack leading to data extraction.

**Splunk SPL:**
```spl
index=ai_security (category="prompt_attack" OR (tokens_out > 5000))
| transaction user_id maxspan=30m
| where eventcount > 1 AND mvfind(category, "prompt_attack") >= 0 AND max(tokens_out) > 5000
| eval severity="critical"
| table _time, user_id, eventcount, category, max(tokens_out)
```

**Sentinel KQL:**
```kql
let attacks = AISecurity_CL | where category_s == "prompt_attack" | project attack_time=TimeGenerated, user_id_s;
let large_outputs = AISecurity_CL | where tokens_out_d > 5000 | project output_time=TimeGenerated, user_id_s, tokens_out_d;
attacks
| join kind=inner (large_outputs) on user_id_s
| where output_time between (attack_time .. (attack_time + 30m))
| project attack_time, output_time, user_id_s, tokens_out_d
```

### Compound: Boundary Violation + Escalation Attempt

An agent boundary violation followed by a successful tool invocation on a different tool suggests progressive privilege escalation.

**Splunk SPL:**
```spl
index=ai_security (category="agent_boundary_violation" OR category="tool_invocation")
| transaction agent_id maxspan=10m
| where mvfind(category, "agent_boundary_violation") >= 0
        AND mvfind(category, "tool_invocation") >= 0
| eval severity="critical"
```

## Dashboard Panels

Use these queries as the basis for SOC dashboard panels. Adapt to your visualisation platform.

### Panel 1: AI Security Event Volume (Timeseries)

**Purpose:** Trending view of all AI security events by category.

**Splunk SPL:**
```spl
index=ai_security
| timechart span=1h count by category
```

**Sentinel KQL:**
```kql
AISecurity_CL
| summarize count() by category_s, bin(TimeGenerated, 1h)
| render timechart
```

### Panel 2: Top Users by Alert Count

**Purpose:** Identify users generating the most AI security alerts.

**Splunk SPL:**
```spl
index=ai_security severity IN ("high", "critical")
| stats count as alert_count by user_id
| sort -alert_count
| head 10
```

### Panel 3: Guardrail Effectiveness Ratio

**Purpose:** Track what percentage of threats guardrails catch versus what the Judge catches post-guardrail (indicating guardrail gaps).

**Splunk SPL:**
```spl
index=ai_security (category="guardrail_block" OR (category="judge_flag" AND guardrail_result="pass"))
| stats count(eval(category="guardrail_block")) as guardrail_caught,
        count(eval(category="judge_flag" AND guardrail_result="pass")) as judge_caught
| eval guardrail_pct=round(guardrail_caught/(guardrail_caught+judge_caught)*100, 1)
| eval judge_pct=round(judge_caught/(guardrail_caught+judge_caught)*100, 1)
```

### Panel 4: Risk Tier Heatmap

**Purpose:** Show alert distribution across risk tiers and categories. Higher-tier systems generating alerts require faster response.

**Splunk SPL:**
```spl
index=ai_security
| stats count by risk_tier, category
| sort risk_tier, -count
```

### Panel 5: Judge Score Distribution

**Purpose:** Track Judge confidence distribution to detect drift or calibration issues.

**Splunk SPL:**
```spl
index=ai_security category="judge_flag"
| bin judge_score span=0.1
| stats count by judge_score
| sort judge_score
```

## SOC Analyst Quick Reference

AI security alerts look different from traditional security events. This reference maps AI concepts to SOC-familiar equivalents.

| AI Concept | SOC Equivalent | Key Difference |
|---|---|---|
| Prompt injection | SQL injection / XSS | Attack is in natural language, not code. No signature match - requires semantic analysis. |
| Judge flag | IDS alert | Async detection, not inline blocking. May fire minutes after the event. |
| Guardrail block | WAF block | Inline, deterministic. May have false positives for legitimate edge-case queries. |
| Agent boundary violation | Privilege escalation alert | The "user" is an AI agent, not a human. The escalation may be caused by injected instructions. |
| Model drift | Baseline deviation | The AI model's behavior changed - could be provider update, adversarial manipulation, or data shift. |
| Token volume spike | Data exfiltration alert | Large output doesn't always mean exfiltration - some queries legitimately produce long answers. Check content, not just volume. |
| Credential in output | Secret exposure | Model may have memorised a credential from training data or tool output. Treat as compromised regardless of source. |

### Triage Decision Tree

```
AI Security Alert Received
├── Is the user a human or an AI agent?
│   ├── Human → Follow standard user investigation
│   └── Agent → Check: was the agent's action triggered by user input (prompt injection)?
│       ├── Yes → Investigate the user who triggered the agent
│       └── No → Investigate agent configuration and tool permissions
│
├── Did the guardrail block or did the Judge flag?
│   ├── Guardrail block → Known pattern. Verify guardrail is current. Close if single event.
│   └── Judge flag → Possible new pattern. Review full I/O. Feed back to guardrail team.
│
└── Is this a single event or a pattern?
    ├── Single → Log and monitor
    └── Pattern → Escalate. Check for coordinated activity across users/endpoints.
```

## Deployment Notes

**Import order:** Deploy detection rules before correlation searches. Correlation searches depend on detection rule output.

**Tuning period:** Run all rules in alert-only mode (no automated response) for 2 weeks. Review false positive rates. Adjust thresholds to your environment's baseline before enabling automated actions.

**Maintenance:** Review and update detection rules when:
- New guardrail categories are added
- New AI endpoints are deployed
- The Judge model is updated
- New agent tools are onboarded
- Threat intelligence identifies new attack patterns

## Related

- [SOC Integration](soc-integration.md) - Architecture, alert taxonomy, and triage procedures
- [Anomaly Detection Ops](anomaly-detection-ops.md) - Behavioral anomaly detection operations
- [Operational Metrics](operational-metrics.md) - Metrics that feed SOC dashboards
- [Logging & Observability](../../infrastructure/controls/logging-and-observability.md) - Infrastructure-level logging controls

