# Behavioral Anomaly Detection

**Aggregating safety signals to detect when agent behavior drifts from normal.**

## The Opportunity

Every safety layer generates signals:

| Layer | Signal Type | What It Catches |
|-------|-------------|-----------------|
| Guardrails | Block events | Known-bad patterns |
| Model-as-Judge | Flag events | Policy violations, quality issues |
| Formal Verification | Validation failures | Rule non-compliance |
| Knowledge Graph | Fact mismatches | Factual errors |
| Token Detection | Uncertainty scores | Low-confidence claims |
| Self-Consistency | Disagreement scores | Unstable responses |
| Human Review | Escalation outcomes | Edge cases, false positives |

Individually, each signal catches specific problems. **Aggregated, they reveal behavioral patterns invisible to any single layer.**

## What Aggregation Enables

### 1. Drift Detection

Normal behavior establishes a baseline. Deviation indicates something changed:

- **Model drift**: New model version produces more guardrail blocks
- **Attack campaigns**: Spike in similar prompt injection attempts
- **Topic sensitivity**: Certain subjects trigger disproportionate failures
- **User anomalies**: Single user probing system boundaries

```
Week 1: 0.3% of requests flagged
Week 2: 0.3% of requests flagged
Week 3: 0.8% of requests flagged  ← Something changed
```

### 2. Correlated Failure Discovery

When multiple layers flag the same request, it's more significant than any single flag:

```
Request X:
  - Guardrail: PASS (no pattern match)
  - Judge: FLAG (inappropriate tone)
  - Formal Verify: FAIL (policy violation)
  - Human Review: BLOCK
  
Pattern: Formal + Human correlation = guardrails need updating
```

### 3. Unknown Attack Vector Identification

Adversaries probe for gaps. Aggregated signals reveal probing patterns before they succeed:

```
User Y (last 24 hours):
  - 47 requests with unusual token patterns
  - 12 guardrail near-misses (passed but close to threshold)
  - 3 judge flags for "boundary testing" language
  - Zero blocks

Assessment: Potential adversarial probing - add to watchlist
```

### 4. Effectiveness Measurement

Which layers catch what? Where are the gaps?

```
Last 30 days:
  - 1,247 total blocks/flags
  - 892 caught by guardrails alone (72%)
  - 234 caught by judge after guardrail pass (19%)
  - 89 caught by formal verification (7%)
  - 32 caught only by human review (2%)

Insight: 28% of issues pass guardrails - judge layer is load-bearing
```

## Architecture

![Behavioral Anomaly Detection](../images/behavioral-anomaly-detection.svg)

### Signal Collection

Every safety layer emits structured events:

```json
{
  "timestamp": "2024-01-15T14:32:01Z",
  "request_id": "req_abc123",
  "session_id": "sess_xyz789",
  "user_id": "user_456",
  "model_version": "gpt-4-0125",
  "layer": "guardrail",
  "event_type": "block",
  "category": "prompt_injection",
  "confidence": 0.94,
  "input_hash": "a1b2c3...",
  "metadata": {
    "pattern_matched": "ignore_previous",
    "input_length": 1247
  }
}
```

### Aggregation Pipeline

![Aggregation Pipeline](../images/aggregation-pipeline.svg)

### ML Anomaly Detection

**Baseline modeling**:
- Historical alert rates by category, user segment, time of day
- Normal distribution of confidence scores
- Typical failure correlation patterns

**Anomaly signals**:
- Volume anomalies: Alert rate exceeds X standard deviations
- Pattern anomalies: New failure signature not seen before
- Correlation anomalies: Layers that don't usually correlate suddenly do
- User anomalies: Individual behavior deviates from cohort
- Temporal anomalies: Unusual time-of-day patterns

**Example detections**:

| Anomaly Type | Signal | Possible Cause |
|--------------|--------|----------------|
| Volume spike | 3x guardrail blocks in 1 hour | Coordinated attack, viral jailbreak |
| New pattern | Unknown prompt structure triggering judge | Novel attack vector |
| Correlation shift | KG failures now correlate with judge flags | Model hallucinating in new domain |
| User outlier | One user generating 40% of flags | Adversarial probing |
| Temporal | 4am spike in high-risk requests | Bot activity, different timezone attackers |

## Implementation Levels

### Level 1: Centralized Logging
- Collect all safety events in one place
- Basic dashboards and queries
- Manual review of patterns
- **Effort**: Low | **Value**: Foundation

### Level 2: Automated Alerting
- Threshold-based alerts (>X blocks/hour)
- Category-specific monitoring
- On-call integration
- **Effort**: Medium | **Value**: Reactive detection

### Level 3: Statistical Anomaly Detection
- Baseline modeling with moving averages
- Z-score based anomaly flagging
- Seasonal adjustment (time of day, day of week)
- **Effort**: Medium | **Value**: Proactive detection

### Level 4: ML-Based Pattern Discovery
- Unsupervised clustering of failure patterns
- User behavior modeling
- Cross-layer correlation analysis
- Emerging attack signature detection
- **Effort**: High | **Value**: Unknown-unknown discovery

## What to Track

### Request-Level Metrics
- Pass/block/flag rates by layer
- Confidence score distributions
- Latency impact of safety checks
- False positive rates (from human review)

### Session-Level Metrics
- Flags per session
- Escalation patterns within session
- Session termination reasons

### User-Level Metrics
- Flag rate compared to cohort
- Category distribution of flags
- Behavioral trajectory over time

### Model-Level Metrics
- Performance by model version
- Drift between versions
- Category-specific accuracy

### System-Level Metrics
- Overall safety layer effectiveness
- Coverage gaps (what passes all checks but fails human review)
- Alert-to-incident conversion rate

## Integration with Existing Observability

This isn't a separate system - it's an extension of standard observability:

| Traditional Observability | AI Behavioral Monitoring |
|---------------------------|--------------------------|
| Error rates | Flag rates |
| Latency percentiles | Confidence score percentiles |
| Request tracing | Safety decision tracing |
| Anomaly detection on metrics | Anomaly detection on behaviors |
| Alerting on thresholds | Alerting on behavioral drift |

**Platforms already doing this**:
- Datadog LLM Observability
- Arize AI
- WhyLabs
- Galileo
- Langfuse
- Weights & Biases

The difference is framing: not just "is the model performing well?" but "is the model behaving safely?"

## Privacy and Compliance Considerations

Aggregating safety signals creates a detailed behavioral record. Consider:

- **Data retention**: How long to keep alert data?
- **PII in alerts**: Scrub or hash user identifiers?
- **Access control**: Who can query behavioral patterns?
- **Audit logging**: Track who accessed what analysis?
- **Cross-user analysis**: Legal basis for cohort comparisons?

The same data that enables security enables surveillance. Design constraints upfront.

## Connection to Risk Tiers

Monitoring depth should match risk:

| Tier | Monitoring Level | Anomaly Detection |
|------|------------------|-------------------|
| **Tier 1** (Minimal) | Basic logging | Threshold alerts |
| **Tier 2** (Moderate) | Aggregated dashboards | Statistical baselines |
| **Tier 3** (Significant) | Real-time monitoring | ML anomaly detection |
| **Tier 4** (Critical) | Full behavioral analysis | Continuous ML + human review |

## The Insider Risk Parallel

Enterprise security has been solving this exact problem for humans since 2015. User and Entity Behavior Analytics (UEBA) - originally UBA before Gartner added the "E" - monitors users and non-human entities against behavioral baselines, flags deviations, and scores risk across multiple dimensions.

The "E" is the key. UEBA was extended specifically to cover non-human entities: service accounts, bots, IoT devices, automated processes. Agents are the next entity type. The entire analytical framework transfers.

### Three insider threat categories → three agent threat categories

Insider risk programs classify threats into three types. Each maps to an agent equivalent:

| Insider Type | Human Example | Agent Equivalent |
|---|---|---|
| **Negligent insider** | Employee accidentally exposes data through carelessness | Agent drifting through accumulated context - not malicious, but degrading from policy through noise, stale memory, or unchecked context growth |
| **Compromised insider** | Employee whose credentials are stolen by an external attacker | Agent that's been prompt-injected, memory-poisoned, or whose NHI credentials are being used from an unexpected context |
| **Malicious insider** | Employee deliberately exfiltrating data | Agent with misaligned objectives - a sleeper agent, a training-time backdoor, or an agent that has been deliberately reprogrammed through persistent manipulation |

The detection challenge is the same in all three cases: the entity has legitimate access. The activity looks authorised. The anomaly is behavioral, not structural.

### UEBA indicators that apply directly to agents

Insider risk programs monitor specific behavioral dimensions. Each translates to agent monitoring:

| UEBA Indicator (Humans) | Agent Equivalent | What It Catches |
|---|---|---|
| **Unusual working hours** - logins at 3am, weekend activity | Agent activity at unusual times - processing requests when no users or scheduled triggers should be activating it | Compromised agent being used out-of-band; unauthorised automation; external attacker operating in a different timezone |
| **Access beyond role** - accessing data irrelevant to job function | Agent accessing tools, data sources, or APIs outside its declared scope | Scope creep through prompt injection; memory-driven misrouting; tool-chain exploitation |
| **Privilege escalation** - requesting elevated permissions | Agent requesting broader tool access, higher-tier APIs, or cross-tenant data | Prompt injection attempting to widen blast radius; delegated authority abuse |
| **Data volume anomalies** - bulk downloads, unusual transfer volumes | Agent processing or transmitting significantly more data than baseline | Data exfiltration; RAG over-retrieval; runaway loops |
| **New communication destinations** - emails to unknown external addresses | Agent calling new external APIs, unknown endpoints, or previously unused tools | Exfiltration via tool invocation; supply chain compromise through redirected API calls |
| **Peer group deviation** - behaving differently from colleagues in the same role | Agent behaving differently from other agents with the same role and configuration | Individual agent compromise when peers remain normal; configuration drift; selective poisoning |
| **Session anomalies** - unusual duration, frequency, concurrency | Unusual session length, invocation frequency, or concurrent execution patterns | Agent being driven by an attacker with different usage patterns than legitimate users |
| **Behavioral change after events** - behavior shift correlating with known events | Agent behavior shift correlating with model updates, config changes, or memory additions | Regression from model update; memory poisoning taking effect; configuration tampering |

The temporal dimension deserves emphasis. Your example - the agent starts working at weekends when it did not before - is a classic UEBA indicator. In human insider risk, unusual working hours are one of the strongest early signals of compromised credentials or malicious intent. For agents, the same logic applies: if an agent's activity pattern changes without a corresponding change in its triggering conditions, something has changed about *who or what is driving it*.

### Peer group comparison: the signal UEBA adds that we don't have

The most powerful UEBA technique that's missing from the current framework is **peer group comparison**. In human insider risk, an individual's behavior is compared not just against their own baseline but against the baseline of their peer group - people in the same role, department, and access tier.

For agents, this means: if you run five customer service agents with the same configuration, and one starts behaving differently from the other four, that's a stronger signal than any individual-baseline deviation. The peer group filters out environmental changes (new data, seasonal patterns, updated prompts) that affect all agents equally, isolating the anomaly to the individual.

Peer comparison catches what individual baselines miss:

- A global shift in query patterns (new product launch, news event) moves all agents' baselines together - **not anomalous**
- A model update changes all agents' response patterns equally - **not anomalous**
- One agent's responses diverge while its peers remain stable - **anomalous, investigate**

Microsoft Sentinel's UEBA builds both individual entity profiles and peer group profiles specifically for this purpose. The same architecture applies to agent fleets.

### What this means for the framework

The insider risk parallel is not a metaphor. It is a direct technical mapping. Agents are entities with identities, access privileges, behavioral baselines, and the potential for compromise. The 15+ years of UEBA engineering that enterprise security has invested in detecting compromised, negligent, and malicious humans transfers directly to detecting the same patterns in agents.

The practical implication: organisations that already run insider risk programs - with UEBA, SIEM correlation, and behavioral baselines - should extend those programs to cover agent identities. The agent's NHI should be enrolled in the same behavioral analytics pipeline as human user accounts. The same SIEM rules that flag "service account active at unusual hours" should flag "agent active at unusual hours."

This is not a new capability to build. It is an existing capability to extend.

## Key Takeaways

1. **Individual safety layers are necessary but not sufficient** - aggregation reveals patterns invisible to any single layer

2. **Behavioral baselines enable drift detection** - you can't detect anomalies without knowing what's normal

3. **Correlated failures are more significant** - when multiple independent layers flag the same thing, pay attention

4. **ML finds unknown-unknowns** - clustering and anomaly detection surface attack patterns you didn't anticipate

5. **This is observability, not a new system** - extend existing monitoring to include behavioral signals

The question isn't just "did we catch the bad request?" It's "is the agent behaving the way we expect, across all the requests we can see?"

## Related

- [The Verification Gap](./the-verification-gap.md) - Why independent verification matters
- [Judge Detects, Not Decides](./judge-detects-not-decides.md) - Async evaluation for pattern analysis
- [Current Solutions Reference](../extensions/technical/current-solutions.md) - Platforms implementing this
- [Beyond Security](./beyond-security.md) - How the framework's architecture applies to drift, fairness, and other AI risks beyond security

