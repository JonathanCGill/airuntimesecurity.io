# Module 6: Applying MASO to Your Solution

**Practical guidance for designing and building multi-agent systems with MASO.**

## The Design Flow

Applying MASO to a solution follows a consistent progression: define the use case, classify the risk, select and implement controls, design PACE transitions, then test.

```
  Define Use Case
        │
        ▼
  Classify Risk Tier  ──→  LOW / MEDIUM / HIGH / CRITICAL
        │
        ▼
  Select Control Baseline  ──→  From 128 controls across 7 domains
        │
        ▼
  Design PACE Transitions  ──→  P → A → C → E and recovery
        │
        ▼
  Implement Three-Layer Defence  ──→  Guardrails, Judge, Human Oversight
        │
        ▼
  Test and Validate  ──→  Red team, PACE drills, baseline calibration
        │
        ▼
  Deploy at Tier 1  ──→  Graduate to Tier 2/3 with operational evidence
```

## Step 1: Define Your Use Case

Answer these ten questions before designing controls:

1. **What does the system do?** (Specific tasks, not "AI assistant")
2. **What decisions does it make or influence?**
3. **What data does it access?** (Classification levels, sensitivity)
4. **Who are the users?** (Internal, customer-facing, regulated populations)
5. **What happens when it is wrong?** (Financial loss, safety impact, reputational damage)
6. **What is the expected volume?** (Transactions per hour, concurrent agents)
7. **What is the regulatory context?** (EU AI Act, DORA, HIPAA, SOX, industry-specific)
8. **What tools and actions are available?** (APIs, databases, file systems, external services)
9. **Where does this sit in the business process?** (Advisory, decision support, autonomous execution)
10. **Who is accountable when it fails?**

The answers to these questions determine your risk tier and control baseline.

## Step 2: Classify Your Risk Tier

Risk tier is determined by the combination of autonomy, decision authority, data sensitivity, reversibility, and regulatory impact.

| Factor | Lower Risk | Higher Risk |
|--------|-----------|-------------|
| Autonomy | Human approves all actions | Agents act independently |
| Decision authority | Advisory, suggestions | Binding decisions, automated execution |
| Data sensitivity | Public data, internal docs | PII, financial, health, classified |
| Reversibility | Actions can be undone | Actions are permanent or hard to reverse |
| Regulatory impact | Unregulated domain | Regulated industry, compliance obligations |

**Tier selection determines:**
- Which controls are mandatory vs. recommended
- PACE formality requirements
- Testing frequency
- Human oversight scope
- Fail posture defaults

**Start at Tier 1 (Supervised).** Always. Build operational evidence — behavioral baselines, failure mode catalogs, trust calibration data — before graduating to higher autonomy.

## Step 3: Design Your Agent Architecture with Security Built In

### Per-Agent Identity

Every agent in your system needs:

- A unique Non-Human Identity (NHI) — not a shared service account
- Scoped credentials that expire and rotate automatically
- An explicit tool allow-list — only the tools this agent needs, nothing more
- Defined blast radius caps — maximum records, maximum financial value, maximum API calls

Do not let agents inherit the orchestrator's credentials or permissions.

### Inter-Agent Communication

All agent-to-agent communication should pass through a controlled message bus:

- Messages are signed with the sender's NHI
- Rate-limited per agent
- Schema-validated at both ends
- Source-tagged to distinguish data from instructions
- Extended with provenance, confidence, assumptions, and unknowns fields

No direct agent-to-agent communication outside the bus.

### Role Separation

Define each agent's role with clear boundaries:

- **What it can read** (data scope)
- **What it can write** (action scope)
- **What it can delegate** (authority scope)
- **What it cannot do** (explicit prohibitions)

Enforce these at the infrastructure level (tool ACLs, API permissions), not at the prompt level. A critic should physically lack write tools. An executor should physically lack approval authority.

## Step 4: Implement the Three-Layer Defence

### Layer 1: Guardrails

Deploy at every agent boundary — not just the system's external interface.

**Checklist:**
- [ ] Input validation on user inputs, inter-agent messages, tool outputs, and RAG results
- [ ] Output sanitization before delivery to users, other agents, and tools
- [ ] PII detection and redaction on all channels
- [ ] Prompt injection pattern blocking on all input sources
- [ ] Per-agent tool allow-lists enforced at infrastructure level
- [ ] Rate limits per agent, per delegation chain, per session
- [ ] Content policy enforcement appropriate to use case

### Layer 2: LLM-as-Judge

Deploy using a different model from your task agents.

**Checklist:**
- [ ] Judge model is from a different provider or architecture than task agents
- [ ] Evaluates final outputs AND inter-agent communications
- [ ] Evaluation criteria include: accuracy, safety, goal integrity, epistemic validity
- [ ] Escalation paths defined: pass → commit, fail → human review, critical fail → terminate
- [ ] Judge cannot be overridden by task agents
- [ ] For multi-step plans: evaluates the aggregate plan, not just individual steps
- [ ] Includes anti-gaming criteria (depth of analysis, evidence quality, not just format)

### Layer 3: Human Oversight

Scale to consequence, not volume.

**Checklist:**
- [ ] Action classes categorized by consequence (read, low-impact write, high-impact write)
- [ ] Approval workflows defined for each consequence level
- [ ] Escalation queues with SLA tracking
- [ ] Challenge rate monitoring (100% approval rate = oversight not functioning)
- [ ] Canary tests to verify reviewer engagement
- [ ] Audit trails for all human decisions

### Circuit Breaker

Make it real.

**Checklist:**
- [ ] Infrastructure-level control (network routing, feature flags) — not prompt-level
- [ ] Can terminate all agent sessions within seconds
- [ ] Triggers defined: error rate thresholds, confirmed compromise, cascading failure
- [ ] Non-AI fallback path exists and has been tested
- [ ] Memory and context snapshots preserved on activation for forensics

## Step 5: Design PACE Transitions

For every control, document:

| Question | Your Answer |
|----------|------------|
| What is the Primary mechanism? | |
| What triggers a transition to Alternate? | |
| What is the Alternate mechanism? | |
| What triggers Contingency? | |
| What does Contingency look like operationally? | |
| What triggers Emergency? | |
| What is the non-AI fallback? | |
| What are the conditions for recovery to Primary? | |

**Key design decisions:**

- **Automated transitions at Tier 2+.** Multi-agent cascading failures propagate faster than humans can respond. The system should transition from P→A automatically and notify humans, not wait for human approval.
- **Recovery requires chain verification.** Before returning from Contingency or Emergency, verify no poisoned data persists in any agent's memory, context, or RAG corpus.
- **Test transitions before production.** If you have never activated your circuit breaker in a test, it does not work.

## Step 6: Address Token Exhaustion

Token exhaustion is an operational control concern, not just a cost concern. Design for it:

- **Context rotation.** Periodically summarize and reset agent context to prevent attention dilution
- **Summarization checkpoints.** At each handoff, produce a structured summary rather than forwarding raw context
- **Session time-boxing.** Maximum execution duration per agent prevents unbounded context growth
- **Budget monitoring.** Track token consumption per agent and alert when approaching thresholds
- **Retry limits.** Cap retry attempts to prevent error-message accumulation that accelerates degradation

## Step 7: Map to Your Orchestration Framework

MASO provides integration patterns for common frameworks. Use the native capabilities where they exist and build custom controls where they do not.

| Capability | LangGraph | AutoGen | CrewAI | AWS Bedrock Agents |
|-----------|-----------|---------|--------|-------------------|
| Per-node guardrails | Graph node wrappers | Pre/post-process hooks | Task callbacks | Native guardrails |
| Checkpointing | Native checkpointing | Conversation logging | Task state | CloudTrail logging |
| Tool allow-lists | Per-node tool binding | Agent tool assignment | Per-agent tools | IAM action policies |
| Inter-agent validation | Edge validators | Speaker selection override | Task delegation hooks | Agent collaboration config |
| Circuit breaker | Graph interruption | Conversation termination | Process control | Lambda circuit breakers |

Refer to the [Integration Guide](../integration/integration-guide.md) for detailed framework-specific patterns.

## Common Pitfalls

**1. Prompt-only security.** If your security controls are in the system prompt and nowhere else, they will fail under context pressure, adversarial input, or model update. Enforce at infrastructure level.

**2. Same-model Judge.** Using the same model (or same provider) for both task agents and the Judge creates correlated failures. Their errors will look like independent corroboration.

**3. Skipping Tier 1.** Jumping directly to Tier 2 or Tier 3 without operational evidence means you do not know your system's failure modes, behavioral baselines, or true blast radius.

**4. Testing controls individually but not together.** Controls interact. A guardrail that works perfectly in isolation may create false confidence that masks a gap elsewhere. Test the full chain.

**5. Ignoring epistemic risks.** The most dangerous multi-agent failures are not adversarial attacks — they are agents reinforcing each other's mistakes with no attacker present. Design for groupthink, hallucination amplification, and uncertainty stripping.

**6. No non-AI fallback.** If your Emergency phase plan is "restart the agents," you do not have an Emergency plan. Define what happens when AI is completely unavailable.

---

**Next:** [Module 7: Key Takeaways and Quick Reference](07-quick-reference.md)
