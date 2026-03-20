"""Control definitions and registry.

Maps the framework's 80+ foundation controls and 128 MASO controls
into a queryable registry, filterable by domain, risk tier, layer, and tier.
"""

from __future__ import annotations

from enum import Enum
from typing import Iterator

from pydantic import BaseModel, Field

from airs.core.models import ControlLayer, RiskTier


class ControlDomain(str, Enum):
    """Control domains from Foundations + MASO frameworks."""

    # Foundations
    INPUT_GUARDRAILS = "input_guardrails"
    OUTPUT_GUARDRAILS = "output_guardrails"
    JUDGE = "judge"
    HUMAN_OVERSIGHT = "human_oversight"
    CIRCUIT_BREAKER = "circuit_breaker"

    # MASO domains
    PROMPT_GOAL_EPISTEMIC = "prompt_goal_epistemic"
    IDENTITY_ACCESS = "identity_access"
    DATA_PROTECTION = "data_protection"
    EXECUTION_CONTROL = "execution_control"
    OBSERVABILITY = "observability"
    SUPPLY_CHAIN = "supply_chain"
    PRIVILEGED_GOVERNANCE = "privileged_governance"

    # Infrastructure
    IAM = "iam"
    LOGGING = "logging"
    NETWORK = "network"
    SECRETS = "secrets"
    INCIDENT_RESPONSE = "incident_response"


class MATSOTier(str, Enum):
    """MASO implementation tiers."""

    SUPERVISED = "supervised"    # Tier 1 — human approves all writes
    MANAGED = "managed"         # Tier 2 — auto-approve low risk, escalate high
    AUTONOMOUS = "autonomous"   # Tier 3 — full PACE, red-team validated


class Control(BaseModel):
    """A single security control from the AIRS framework."""

    id: str
    name: str
    description: str
    domain: ControlDomain
    layer: ControlLayer
    min_risk_tier: RiskTier = RiskTier.LOW
    maso_tier: MATSOTier | None = None
    owasp_refs: list[str] = Field(default_factory=list)
    implementation_hint: str = ""


class ControlRegistry:
    """Queryable registry of all AIRS controls.

    Provides filtering by domain, risk tier, layer, and MASO tier,
    plus prioritized implementation plans per deployment profile.
    """

    def __init__(self) -> None:
        self._controls: dict[str, Control] = {}
        self._load_defaults()

    def register(self, control: Control) -> None:
        self._controls[control.id] = control

    def get(self, control_id: str) -> Control | None:
        return self._controls.get(control_id)

    def all(self) -> list[Control]:
        return list(self._controls.values())

    def by_domain(self, domain: ControlDomain) -> list[Control]:
        return [c for c in self._controls.values() if c.domain == domain]

    def by_layer(self, layer: ControlLayer) -> list[Control]:
        return [c for c in self._controls.values() if c.layer == layer]

    def by_risk_tier(self, tier: RiskTier) -> list[Control]:
        """Return controls required at or below the given risk tier."""
        order = [RiskTier.LOW, RiskTier.MEDIUM, RiskTier.HIGH, RiskTier.CRITICAL]
        tier_idx = order.index(tier)
        return [
            c for c in self._controls.values()
            if order.index(c.min_risk_tier) <= tier_idx
        ]

    def by_maso_tier(self, tier: MATSOTier) -> list[Control]:
        order = [MATSOTier.SUPERVISED, MATSOTier.MANAGED, MATSOTier.AUTONOMOUS]
        tier_idx = order.index(tier)
        return [
            c for c in self._controls.values()
            if c.maso_tier is not None and order.index(c.maso_tier) <= tier_idx
        ]

    def prioritized_for(
        self,
        risk_tier: RiskTier,
        maso_tier: MATSOTier | None = None,
    ) -> list[Control]:
        """Return controls in recommended implementation order."""
        controls = self.by_risk_tier(risk_tier)
        if maso_tier:
            maso_controls = self.by_maso_tier(maso_tier)
            seen = {c.id for c in controls}
            controls.extend(c for c in maso_controls if c.id not in seen)

        # Priority: circuit_breaker first (cheap, high impact), then guardrails,
        # then observability, then judge, then human oversight, then everything else
        layer_priority = {
            ControlLayer.CIRCUIT_BREAKER: 0,
            ControlLayer.GUARDRAIL: 1,
            ControlLayer.JUDGE: 2,
            ControlLayer.HUMAN: 3,
        }
        return sorted(controls, key=lambda c: layer_priority.get(c.layer, 4))

    def __len__(self) -> int:
        return len(self._controls)

    def __iter__(self) -> Iterator[Control]:
        return iter(self._controls.values())

    def _load_defaults(self) -> None:
        """Load the framework's core controls."""
        defaults = [
            # --- Circuit Breaker (implement first — cheapest, highest impact) ---
            Control(
                id="CB-01",
                name="Feature Flag Kill Switch",
                description="Non-AI fallback activated via feature flag. All AI traffic stops immediately.",
                domain=ControlDomain.CIRCUIT_BREAKER,
                layer=ControlLayer.CIRCUIT_BREAKER,
                min_risk_tier=RiskTier.LOW,
                owasp_refs=["LLM06"],
                implementation_hint="Use LaunchDarkly, Unleash, or environment variable. "
                "Route: if flag off → static/cached response.",
            ),
            Control(
                id="CB-02",
                name="Anomaly-Triggered Circuit Breaker",
                description="Auto-trip based on error rate, latency spike, or guardrail block rate exceeding threshold.",
                domain=ControlDomain.CIRCUIT_BREAKER,
                layer=ControlLayer.CIRCUIT_BREAKER,
                min_risk_tier=RiskTier.MEDIUM,
                owasp_refs=["LLM06", "LLM10"],
                implementation_hint="Monitor block_rate > 20% over 5min window → trip breaker. "
                "Use sliding window counter.",
            ),

            # --- Input Guardrails ---
            Control(
                id="GR-IN-01",
                name="Prompt Injection Detection",
                description="Detect and block known prompt injection patterns in user input.",
                domain=ControlDomain.INPUT_GUARDRAILS,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.LOW,
                owasp_refs=["LLM01"],
                implementation_hint="Regex + ML classifier. Start with known patterns "
                "(ignore previous, system prompt override). Add ML classifier at MEDIUM+.",
            ),
            Control(
                id="GR-IN-02",
                name="PII Detection (Input)",
                description="Detect and redact PII in user input before it reaches the model.",
                domain=ControlDomain.INPUT_GUARDRAILS,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.MEDIUM,
                owasp_refs=["LLM02"],
                implementation_hint="Use presidio, comprehend, or regex for SSN/email/phone/CC. "
                "Redact or tokenize before model call.",
            ),
            Control(
                id="GR-IN-03",
                name="Content Policy Filter (Input)",
                description="Block inputs that violate content policy (hate speech, violence, illegal content).",
                domain=ControlDomain.INPUT_GUARDRAILS,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.LOW,
                owasp_refs=["LLM01"],
                implementation_hint="Keyword blocklist + toxicity classifier. Cloud providers "
                "offer this natively (Bedrock Guardrails, Azure Content Safety).",
            ),
            Control(
                id="GR-IN-04",
                name="Input Length & Rate Limiting",
                description="Enforce maximum input length and per-user rate limits.",
                domain=ControlDomain.INPUT_GUARDRAILS,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.LOW,
                owasp_refs=["LLM10"],
                implementation_hint="Max tokens, requests/minute per user. "
                "Implement at API gateway layer.",
            ),

            # --- Output Guardrails ---
            Control(
                id="GR-OUT-01",
                name="PII Detection (Output)",
                description="Detect and redact PII in model output before delivery to user.",
                domain=ControlDomain.OUTPUT_GUARDRAILS,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.LOW,
                owasp_refs=["LLM02"],
                implementation_hint="Same PII detector as input, applied to output. "
                "Block response if PII detected at HIGH+ tier.",
            ),
            Control(
                id="GR-OUT-02",
                name="Output Content Policy Filter",
                description="Block outputs containing harmful, toxic, or policy-violating content.",
                domain=ControlDomain.OUTPUT_GUARDRAILS,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.LOW,
                owasp_refs=["LLM05"],
                implementation_hint="Toxicity classifier + keyword filter on output. "
                "Return safe fallback message if blocked.",
            ),
            Control(
                id="GR-OUT-03",
                name="Grounding / Source Attribution Check",
                description="Verify output is grounded in provided context (RAG) or flag ungrounded claims.",
                domain=ControlDomain.OUTPUT_GUARDRAILS,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.HIGH,
                owasp_refs=["LLM09", "LLM08"],
                implementation_hint="Compare output claims to retrieved context. "
                "NLI model or embedding similarity. Flag if <0.7 similarity.",
            ),
            Control(
                id="GR-OUT-04",
                name="System Prompt Leakage Detection",
                description="Detect if the model output contains system prompt content.",
                domain=ControlDomain.OUTPUT_GUARDRAILS,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.MEDIUM,
                owasp_refs=["LLM07"],
                implementation_hint="Substring match + semantic similarity between output "
                "and system prompt. Block if similarity > threshold.",
            ),

            # --- Model-as-Judge ---
            Control(
                id="JG-01",
                name="Policy Adherence Judge",
                description="Independent LLM evaluates whether the response adheres to defined policies.",
                domain=ControlDomain.JUDGE,
                layer=ControlLayer.JUDGE,
                min_risk_tier=RiskTier.MEDIUM,
                owasp_refs=["LLM01", "LLM05", "LLM09"],
                implementation_hint="Separate model (different provider recommended). "
                "Structured output: {verdict: pass|review|escalate, reason: str, confidence: float}.",
            ),
            Control(
                id="JG-02",
                name="Factual Accuracy Judge",
                description="Evaluate output for hallucination and factual accuracy against known sources.",
                domain=ControlDomain.JUDGE,
                layer=ControlLayer.JUDGE,
                min_risk_tier=RiskTier.HIGH,
                owasp_refs=["LLM09"],
                implementation_hint="Cross-reference with retrieved docs. "
                "Use entailment model or second LLM with source docs as context.",
            ),
            Control(
                id="JG-03",
                name="Safety & Appropriateness Judge",
                description="Evaluate whether the output is safe and appropriate for the context.",
                domain=ControlDomain.JUDGE,
                layer=ControlLayer.JUDGE,
                min_risk_tier=RiskTier.MEDIUM,
                owasp_refs=["LLM05", "LLM06"],
                implementation_hint="Evaluate tone, audience-appropriateness, and safety. "
                "Can combine with policy judge or run as separate evaluation.",
            ),

            # --- Human Oversight ---
            Control(
                id="HO-01",
                name="Review Queue for Flagged Outputs",
                description="Human review queue with SLA-based triage for outputs flagged by guardrails or judge.",
                domain=ControlDomain.HUMAN_OVERSIGHT,
                layer=ControlLayer.HUMAN,
                min_risk_tier=RiskTier.MEDIUM,
                owasp_refs=["LLM06"],
                implementation_hint="Queue with SLAs: Critical=1h, High=4h, Standard=24h. "
                "Track reviewer accuracy with canary cases.",
            ),
            Control(
                id="HO-02",
                name="Mandatory Human Approval for High-Impact Actions",
                description="Require human approval before AI-initiated actions with financial, legal, or safety impact.",
                domain=ControlDomain.HUMAN_OVERSIGHT,
                layer=ControlLayer.HUMAN,
                min_risk_tier=RiskTier.HIGH,
                owasp_refs=["LLM06"],
                implementation_hint="Define action categories requiring approval. "
                "Implement async approval workflow with timeout fallback to deny.",
            ),
            Control(
                id="HO-03",
                name="Statistical Sampling Review",
                description="Random sample of AI outputs reviewed by humans for quality assurance.",
                domain=ControlDomain.HUMAN_OVERSIGHT,
                layer=ControlLayer.HUMAN,
                min_risk_tier=RiskTier.LOW,
                owasp_refs=["LLM09"],
                implementation_hint="Sample 1-5% of outputs. Log reviewer feedback. "
                "Use disagreements to tune guardrails and judge prompts.",
            ),

            # --- Observability ---
            Control(
                id="OB-01",
                name="Request/Response Logging",
                description="Log all AI requests and responses with correlation IDs for audit trail.",
                domain=ControlDomain.LOGGING,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.LOW,
                implementation_hint="Structured logs with request_id, user_id, model, "
                "input hash, output hash, latency, all layer verdicts.",
            ),
            Control(
                id="OB-02",
                name="Behavioral Drift Detection",
                description="Monitor aggregate patterns for behavioral drift — block rate changes, topic shifts.",
                domain=ControlDomain.OBSERVABILITY,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.MEDIUM,
                implementation_hint="Track rolling averages: block rate, judge escalation rate, "
                "avg confidence. Alert on >2 std dev change.",
            ),

            # --- MASO: Prompt, Goal & Epistemic Integrity ---
            Control(
                id="PG-01",
                name="System Prompt Isolation",
                description="Prevent cross-agent system prompt extraction or modification.",
                domain=ControlDomain.PROMPT_GOAL_EPISTEMIC,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.MEDIUM,
                maso_tier=MATSOTier.SUPERVISED,
                owasp_refs=["LLM01", "LLM07", "ASI01"],
                implementation_hint="Each agent has isolated system prompt. "
                "Inter-agent messages stripped of system-level content.",
            ),
            Control(
                id="PG-02",
                name="Goal Integrity Monitoring",
                description="Detect when an agent's operational goal drifts from its assigned objective.",
                domain=ControlDomain.PROMPT_GOAL_EPISTEMIC,
                layer=ControlLayer.JUDGE,
                min_risk_tier=RiskTier.HIGH,
                maso_tier=MATSOTier.MANAGED,
                owasp_refs=["ASI01"],
                implementation_hint="Periodically compare agent's recent actions/outputs "
                "to its defined goal using semantic similarity.",
            ),
            Control(
                id="PG-03",
                name="Epistemic Integrity — Anti-Groupthink",
                description="Detect when multiple agents converge on identical conclusions without independent reasoning.",
                domain=ControlDomain.PROMPT_GOAL_EPISTEMIC,
                layer=ControlLayer.JUDGE,
                min_risk_tier=RiskTier.HIGH,
                maso_tier=MATSOTier.MANAGED,
                owasp_refs=["ASI01"],
                implementation_hint="Compare agent outputs for suspiciously high similarity. "
                "Flag if >90% semantic overlap between independent assessments.",
            ),

            # --- MASO: Identity & Access ---
            Control(
                id="IA-01",
                name="Non-Human Identity Per Agent",
                description="Each agent has a unique NHI — no shared credentials between agents.",
                domain=ControlDomain.IDENTITY_ACCESS,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.MEDIUM,
                maso_tier=MATSOTier.SUPERVISED,
                owasp_refs=["ASI03"],
                implementation_hint="Issue short-lived tokens per agent. "
                "Rotate on every session. Log all credential usage.",
            ),
            Control(
                id="IA-02",
                name="Least-Privilege Tool Access",
                description="Each agent can only access tools explicitly granted for its role.",
                domain=ControlDomain.IDENTITY_ACCESS,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.LOW,
                maso_tier=MATSOTier.SUPERVISED,
                owasp_refs=["ASI02", "ASI03"],
                implementation_hint="Define tool allow-list per agent role. "
                "Deny by default. Log all tool invocations.",
            ),

            # --- MASO: Execution Control ---
            Control(
                id="EC-01",
                name="Sandboxed Execution",
                description="Agent tool executions run in isolated sandbox with resource limits.",
                domain=ControlDomain.EXECUTION_CONTROL,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.MEDIUM,
                maso_tier=MATSOTier.SUPERVISED,
                owasp_refs=["ASI02", "ASI05"],
                implementation_hint="Container or VM isolation per agent. "
                "CPU/memory/network limits. No host filesystem access.",
            ),
            Control(
                id="EC-02",
                name="Blast Radius Caps",
                description="Limit the maximum impact of any single agent action (e.g., max dollar amount, max records).",
                domain=ControlDomain.EXECUTION_CONTROL,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.MEDIUM,
                maso_tier=MATSOTier.SUPERVISED,
                owasp_refs=["ASI02", "ASI08"],
                implementation_hint="Define per-action limits. "
                "E.g., max $1000 per transaction, max 100 records modified.",
            ),

            # --- MASO: Data Protection ---
            Control(
                id="DP-01",
                name="Cross-Agent Data Fencing",
                description="Prevent uncontrolled data flow between agents. Enforce data classification boundaries.",
                domain=ControlDomain.DATA_PROTECTION,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.MEDIUM,
                maso_tier=MATSOTier.SUPERVISED,
                owasp_refs=["ASI07", "LLM02"],
                implementation_hint="Tag data with classification. "
                "Message bus enforces: agent X cannot send CONFIDENTIAL to agent Y.",
            ),
            Control(
                id="DP-02",
                name="Memory Poisoning Detection",
                description="Detect when an agent's memory or context has been tampered with.",
                domain=ControlDomain.DATA_PROTECTION,
                layer=ControlLayer.JUDGE,
                min_risk_tier=RiskTier.HIGH,
                maso_tier=MATSOTier.MANAGED,
                owasp_refs=["ASI06"],
                implementation_hint="Hash memory state at checkpoints. "
                "Alert on unexpected mutations. Periodically validate with judge.",
            ),

            # --- MASO: Supply Chain ---
            Control(
                id="SC-01",
                name="AI Bill of Materials (AIBOM)",
                description="Maintain inventory of all models, tools, and MCP servers in the agent system.",
                domain=ControlDomain.SUPPLY_CHAIN,
                layer=ControlLayer.GUARDRAIL,
                min_risk_tier=RiskTier.MEDIUM,
                maso_tier=MATSOTier.SUPERVISED,
                owasp_refs=["ASI04", "LLM03"],
                implementation_hint="JSON manifest: {models: [...], tools: [...], mcp_servers: [...]}. "
                "Version-pinned. Reviewed on change.",
            ),
        ]

        for control in defaults:
            self.register(control)
