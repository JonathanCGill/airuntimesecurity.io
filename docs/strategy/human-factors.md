---
description: "The human constraints in AI strategy: skills gaps, learning capacity, available time, willingness to change, and the organisational readiness nobody audits."
---

# Human Factors

*Skills, time, learning capacity, and the organisational readiness nobody wants to audit.*

> Part of [From Strategy to Production](./)

## The Missing Variable

AI strategies account for technology, data, and budget. They rarely account for people.

Not "headcount" - that's a budget line. People: their skills, their capacity to learn new things, their available time, their willingness to change how they work, and their ability to operate AI systems safely day after day.

Automation bias, deskilling, and accountability gaps are risks that emerge from how humans work alongside AI. But these aren't just runtime risks. They're strategic risks. If your AI strategy assumes human capabilities that don't exist, it will fail before any security control is tested.

## The Five Human Constraints

### 1. Skills: What People Can Do Today

AI systems require skills across three domains - and most organisations have significant gaps in at least two.

![Human Factors Skills Map](../images/strategy-human-factors.svg)

| Skill Domain | Who Needs It | Current Gap |
|--------------|-------------|-------------|
| **AI technical** - Building, deploying, maintaining AI systems | Engineering team | Competitive market; experienced AI engineers are expensive and scarce |
| **AI operational** - Monitoring, tuning guardrails, operating Judge, managing HITL queues | Security/ops team | Almost nobody has this skill set yet; it didn't exist 3 years ago |
| **AI-aware domain expertise** - Using AI outputs critically, knowing when to trust and when to challenge | Business users | Most domain experts have never worked with non-deterministic tools |

#### The Build Skills Gap

Can your team build the AI system the strategy requires?

| What You Need | Typical Availability | Realistic Option |
|---------------|---------------------|-----------------|
| Prompt engineering | Increasingly common | Train existing developers - 2-4 weeks |
| RAG pipeline development | Common among senior engineers | Hire or upskill - 1-3 months |
| Fine-tuning / model training | Specialist skill | Hire ML engineers or use vendor services |
| Guardrail implementation | Rare (emerging) | Train security engineers using framework guides - 1-2 months |
| Judge evaluation design | Very rare | Train using [Judge prompt examples](../extensions/templates/judge-prompt-examples.md) - ongoing |
| Multi-agent orchestration | Very rare | Hire specialists or partner with vendor |
| AI security architecture | Very rare | This framework is a starting point; experience takes time |

**Strategic implication:** The skills required to build a [Fast Lane](../FAST-LANE.md) deployment (basic guardrails, logging, feature flag) can be acquired in weeks. The skills required for a Tier 3 autonomous agent system take months to years. Strategy must align ambition with available (or realistically acquirable) skills.

#### The Operate Skills Gap

Building the system is only half the problem. Who operates it?

The framework's [governance operating model](../extensions/regulatory/ai-governance-operating-model.md) specifies these roles:

| Role | What They Do | Where They Come From |
|------|-------------|---------------------|
| **HITL reviewers** | Review AI outputs flagged by Judge | Domain experts redeployed from existing roles |
| **Judge operators** | Calibrate Judge prompts, manage sampling rates, review accuracy | Security or QA analysts - retrained |
| **Guardrail maintainers** | Update guardrail patterns, manage false positives | Security operations - retrained |
| **AI incident responders** | Investigate AI-specific incidents | Security incident team - with additional training |
| **AI risk analysts** | Classify risk, assess controls, report to governance | Risk team - with AI-specific training |

These are not new hires (in most cases). They're existing people who need new skills. But the training takes time, and the people need to be freed from their current responsibilities to learn and then to operate.

**Real-world scenario:** A retail bank implements an AI customer service assistant classified as HIGH tier. The framework requires human review of all flagged outputs within a 4-hour SLA. The bank assigns this to the existing customer complaints team. The problems:

- Complaints team has no training on AI-specific failure modes
- They don't understand what hallucination looks like vs. a genuinely unusual response
- They apply their existing judgement framework (customer intent, complaint handling) rather than AI-specific criteria (accuracy, policy compliance, data leakage)
- Review times are 3x longer than estimated because they don't know what they're evaluating
- SLA compliance drops below 60% within the first month

The system works. The people don't. Not because they're incapable - because they weren't prepared.

### 2. Time: What People Can Learn

Every AI initiative requires people to learn new things. The question is whether there's time to learn them *before* the system goes live.

#### Learning Time Estimates

These are realistic, not optimistic. They assume motivated professionals with relevant background.

| Skill | Target Audience | Time to Basic Competence | Time to Operational Competence |
|-------|----------------|--------------------------|-------------------------------|
| Understanding AI limitations (non-determinism, hallucination) | All AI users | 2-4 hours (awareness) | 2-4 weeks (working knowledge) |
| Using AI tools critically (not trusting blindly) | Business users | 1 day | 1-2 months (habit formation) |
| HITL review for AI outputs | Domain experts | 2-3 days (training) | 1 month (calibrated judgement) |
| Guardrail configuration and tuning | Security engineers | 1-2 weeks | 2-3 months |
| Judge prompt design and calibration | QA/security analysts | 2-4 weeks | 3-6 months |
| AI risk classification | Risk analysts | 1-2 weeks | 3 months |
| AI incident investigation | Security incident team | 2-3 weeks | 6 months |
| Multi-agent security operations | Security architects | 1-2 months | 6-12 months |

**The gap that matters:** The time between "basic competence" and "operational competence" is where mistakes happen. People know enough to do the job but not enough to do it well. For LOW and MEDIUM tier systems, this is acceptable - errors are low-impact and recoverable. For HIGH and CRITICAL tier systems, this gap is dangerous.

#### The Learning Capacity Problem

Organisations have a finite capacity to absorb change. AI is not the only thing people are being asked to learn.

| Competing Demands | Reality |
|-------------------|---------|
| Cloud migration | Still ongoing in many organisations |
| Regulatory changes | Continuous compliance burden |
| Security awareness | Annual training, phishing exercises |
| New tooling | Every year brings new platforms and processes |
| Business-as-usual | The work that was there before AI arrived |

Adding "learn AI" to an already-full training calendar doesn't work by simply mandating it. Something else needs to give. Strategy should identify *what* gets deprioritised to make room for AI capability building.

### 3. Capacity: What People Can Absorb

Even with time and training, there's a limit to how much change people can absorb at once.

**The absorption curve:**

| Phase | What Happens | Duration |
|-------|-------------|----------|
| **Awareness** | "I know AI is coming" | Days |
| **Understanding** | "I understand what it means for my role" | Weeks |
| **Competence** | "I can do the new things" | Months |
| **Confidence** | "I trust my judgement with AI systems" | Months-years |
| **Mastery** | "I know when to trust AI and when to override" | Years |

Most AI strategies plan for the **Competence** phase. The framework's controls - particularly HITL review - require the **Confidence** phase to work properly. A human reviewer who has reached Competence can follow the review process. A human reviewer who has reached Confidence knows when the process isn't capturing the right thing.

**The automation bias problem** (framework risk #12) is a confidence-phase problem. At the Competence phase, reviewers follow the process. At the Confidence phase, they develop genuine independent judgement. In between, there's a dangerous period where they're fast enough to process high volumes but not experienced enough to catch subtle AI failures.

### 4. Willingness: What People Will Actually Do

Training assumes willingness. Willingness isn't guaranteed.

| Resistance Factor | What It Looks Like | Impact |
|-------------------|-------------------|--------|
| **Fear of replacement** | "This AI is going to take my job" | People undermine adoption; withhold domain knowledge; don't engage with training |
| **Expertise threat** | "I have 20 years of experience and now a chatbot is doing my job" | Senior experts disengage; HITL quality drops because experts don't take review seriously |
| **Workflow disruption** | "This is slower than what I was doing before" | Workarounds; shadow processes; people bypass the AI system |
| **Trust deficit** | "I don't trust this thing" | Over-checking (inefficient) or ignoring AI outputs entirely (defeats the purpose) |
| **Change fatigue** | "Not another transformation programme" | Compliance without engagement; minimum effort |

**Strategic implication:** Willingness is not a training problem. It's a communication and leadership problem. People need to understand:

- What the AI does and doesn't replace
- How their role changes (specifically, not vaguely)
- What new skills they need and how they'll be supported in acquiring them
- That their domain expertise is *more* valuable with AI, not less - because the AI needs humans who can judge its outputs

The framework's principle "[Humans Remain Accountable](../insights/humans-remain-accountable.md)" is the right message, but it needs to reach the people doing the work, not just the governance committee.

### 5. Sustainability: What People Can Maintain

Day 1 is not the problem. Month 6 is the problem.

| Sustainability Risk | What Happens | When |
|---------------------|-------------|------|
| **Alert fatigue** | HITL reviewers stop reading flagged outputs carefully | 2-3 months |
| **Guardrail drift** | Nobody updates guardrail patterns as threats evolve | 3-6 months |
| **Judge calibration decay** | Judge prompts aren't recalibrated; accuracy drops silently | 3-6 months |
| **Knowledge attrition** | Key people leave; replacements aren't trained | 6-12 months |
| **Process erosion** | Shortcuts become normal; reviews happen in name only | 6-12 months |

The framework's PACE resilience model addresses technical degradation. But human degradation follows the same pattern:

| PACE Phase | Technical Equivalent | Human Equivalent |
|------------|---------------------|-----------------|
| **Primary** | All controls active | All roles staffed, trained, engaged |
| **Alternate** | One layer degraded | Key person leaves; coverage maintained by remaining team |
| **Contingency** | Multiple layers degraded | Team understaffed; reviews backlogged; guardrails stale |
| **Emergency** | Full stop | Nobody qualified to operate the system; knowledge lost |

**The framework doesn't have a human PACE model.** This is a gap. Technical systems have failover; human systems typically don't. When the one person who understands Judge calibration leaves, there's no automatic failover to a backup.

## Human Factors by Risk Tier

The human requirements scale with risk tier, just as technical controls do:

| Factor | Fast Lane / LOW | MEDIUM | HIGH | CRITICAL |
|--------|----------------|--------|------|----------|
| **Users** | Basic AI awareness training | AI limitations training; know when to distrust | Detailed training on system-specific failure modes | Expert users only; mandatory certification |
| **HITL reviewers** | None required | General domain knowledge; spot-check capability | Domain experts with AI-specific training; calibrated judgement | Senior experts; independent judgement; regular accuracy testing |
| **Operators** | Any engineer | Engineer with guardrail experience | Dedicated AI security engineer | Specialist team with 24/7 coverage |
| **Training frequency** | Annual refresher | Quarterly | Monthly recalibration | Continuous (part of role) |
| **Backup personnel** | Not required | Identified but not dedicated | Trained and available | Active rotation; no single point of failure |

## Real-World Scenarios

### Scenario 1: The Under-Skilled HITL

**Context:** Healthcare organisation deploys AI to summarise patient notes for clinicians. Classified as HIGH tier.

**Assumption:** Clinicians will review AI summaries before making clinical decisions.

**Reality:** Clinicians are overworked. Average consultation time is 10 minutes. They don't have time to cross-reference AI summaries against full notes. They scan the summary, confirm it looks plausible, and move on. Effective review rate: near zero.

**Framework impact:** The HITL control exists on paper. In practice, the human layer isn't functioning. The system is operating as if it were at MEDIUM or LOW tier - basic guardrails only, with no effective human oversight.

**Strategic response:**
- Redesign the AI output to highlight uncertainty ("confidence: low on medication history")
- Reduce the review burden - instead of reviewing every summary, review only those the Judge flags
- Measure actual review behavior (time spent, override rate) not just claimed process compliance
- Consider whether the risk tier is appropriate given realistic human capacity

### Scenario 2: The Missing Operator

**Context:** Financial services firm deploys AI fraud detection with Judge evaluation of flagged transactions. Classified as CRITICAL tier.

**Assumption:** Security operations team will manage Judge calibration, guardrail updates, and escalation triage.

**Reality:** The security operations team has one person who understands the Judge system. That person also manages three other security tools. Judge calibration happens when they have time - roughly once a quarter instead of the weekly cadence specified. When they take holiday, nobody monitors Judge accuracy.

**Framework impact:** Judge accuracy degrades without calibration. The invisible degradation risk materialises not through technical failure, but through human capacity failure.

**Strategic response:**
- Fund a dedicated AI security operations role (the governance model's "Technical Operations Team")
- Cross-train at least one additional person on Judge operations
- Automate what can be automated (calibration alerts, accuracy dashboards)
- Accept that until staffing is adequate, the system should operate at a lower autonomy level

### Scenario 3: The Resistant Expert

**Context:** Insurance company deploys AI to assist claims assessors. Classified as MEDIUM tier.

**Assumption:** Claims assessors will use AI recommendations as input to their decisions.

**Reality:** Senior assessors with 15+ years experience refuse to use the system. "I don't need a computer to tell me how to assess a claim." Junior assessors use it for everything without critical evaluation. The senior experts' knowledge isn't being captured; the junior assessors aren't developing independent judgement.

**Framework impact:** The system works technically but creates two failure modes:
1. Senior assessors bypass the AI, gaining no benefit
2. Junior assessors trust it uncritically - automation bias (framework risk #12)

**Strategic response:**
- Engage senior assessors in Judge calibration - their expertise is exactly what's needed to evaluate AI quality
- Position the AI as a second opinion, not a replacement for expertise
- Monitor override rates - very high (seniors ignoring AI) and very low (juniors trusting blindly) are both warning signals
- Structure HITL so senior and junior assessors review each other's AI-assisted decisions

## The Deskilling Problem

Deskilling is both a runtime risk and a strategic risk.

When AI handles tasks that humans used to do, humans lose the ability to do those tasks. This matters because:

1. **PACE resilience requires human fallback.** If the AI fails and humans can't do the task manually, there's no contingency.
2. **HITL quality depends on domain expertise.** If reviewers have lost domain knowledge, they can't effectively evaluate AI outputs.
3. **Model drift is detected by humans.** If nobody remembers what "normal" looks like, nobody notices when the AI drifts.

| Deskilling Timeline | What's Lost | Impact |
|---------------------|-------------|--------|
| **3-6 months** | Speed at manual process | Inconvenient but manageable if AI fails |
| **6-12 months** | Routine judgement calls | Errors increase when reverting to manual |
| **1-2 years** | Nuanced expertise | Manual fallback quality degrades significantly |
| **2+ years** | Institutional knowledge | Organisation cannot operate without AI - single point of failure |

**Strategic mitigation:**
- Maintain manual process capability through periodic exercises (like disaster recovery testing)
- Rotate staff between AI-assisted and manual work
- Document manual processes before they're automated - not after
- Build deskilling risk into the PACE plan: if humans can't fall back, the Emergency phase is incomplete

## What to Do About This

### Before Starting an AI Initiative

| Action | Purpose | Time |
|--------|---------|------|
| **Skills audit** | Identify gaps in build, operate, and use capabilities | 1-2 weeks |
| **Training plan** | What skills, who needs them, how they'll be acquired | 1 week to plan |
| **Capacity assessment** | Do people have time to learn and operate this? | 1 week |
| **Resistance assessment** | Where will resistance come from? How will it be addressed? | 1 week |
| **Sustainability plan** | Who operates this on day 180? What happens when they leave? | 1 week |

### During Implementation

| Action | Purpose | When |
|--------|---------|------|
| **Train before deploy** | People are ready when the system goes live | 2-4 weeks before launch |
| **Shadow period** | AI runs but humans make all decisions; builds competence | 2-4 weeks after launch |
| **Graduated autonomy** | AI takes on more responsibility as human confidence grows | Months 2-6 |
| **Measure human performance** | Are reviews effective? Are overrides appropriate? | Continuously |

### After Deployment

| Action | Purpose | When |
|--------|---------|------|
| **Recalibration training** | Refresh skills, share lessons learned | Quarterly |
| **Override rate monitoring** | Detect automation bias or excessive distrust | Monthly |
| **Backup personnel check** | Is there someone who can cover every role? | Quarterly |
| **Manual process exercise** | Verify the fallback still works | Bi-annually |
| **Exit interview knowledge capture** | When operators leave, capture what they know | Every departure |

## The Framework Gap

The framework treats human factors as an implementation detail. It specifies that HITL reviewers should exist, that they should have domain expertise, and that they should review within SLAs. But it doesn't address:

- How those humans are trained
- How long training takes
- What happens when they're unavailable
- How to detect when they're not performing effectively
- How to prevent deskilling over time
- How to sustain human capability as the AI portfolio grows

This is partly by design - the framework is a security controls framework, not an organisational change management programme. But strategy cannot treat human factors as somebody else's problem. The controls don't work if the humans operating them aren't ready, willing, and sustainably capable.

**Recommendation:** For any deployment above Fast Lane, include a human factors assessment alongside the technical risk assessment. The framework's risk classification asks "what can this system do?" The human factors assessment asks "can our people safely operate this system?" Both questions need answers before deployment.

One approach to the scalability gap: [Humans in the Business Process](../extensions/technical/humans-in-the-business-process.md) - instead of adding dedicated HITL reviewers, use the existing human decision points in the business workflow as a detection and correction layer. The concept works because business process humans encounter AI outputs in full domain context (making their review more effective) and because it's their actual job (making their engagement sustainable).

