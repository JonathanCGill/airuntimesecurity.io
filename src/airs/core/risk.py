"""Risk classification engine.

Classifies an AI deployment into a risk tier based on context factors,
then recommends the appropriate control set.
"""

from __future__ import annotations

from pydantic import BaseModel

from airs.core.models import RiskTier


class DeploymentProfile(BaseModel):
    """Describes an AI deployment for risk classification.

    Answer these questions about your deployment to get a risk tier
    and prioritized control recommendations.
    """

    # Audience & exposure
    external_facing: bool = False
    user_count: str = "small"  # small (<100), medium (100-10k), large (10k+)

    # Data sensitivity
    handles_pii: bool = False
    handles_regulated_data: bool = False  # HIPAA, SOX, GDPR-sensitive
    handles_financial_data: bool = False

    # Autonomy & impact
    can_take_actions: bool = False  # writes, API calls, transactions
    actions_are_reversible: bool = True
    max_financial_impact: str = "none"  # none, low (<$1k), medium (<$100k), high (>$100k)

    # Architecture
    multi_agent: bool = False
    uses_rag: bool = False
    uses_tools: bool = False
    uses_mcp: bool = False

    # Oversight
    human_reviews_all_outputs: bool = False
    has_existing_guardrails: bool = False

    # Regulatory
    regulated_industry: bool = False  # healthcare, finance, legal, etc.

    name: str = ""
    description: str = ""


class RiskClassifier:
    """Classifies a deployment profile into a risk tier.

    Based on the framework's risk tier criteria:
    - LOW: Internal, read-only, no regulated data, human-reviewed
    - MEDIUM: External or handles PII, but no autonomous actions
    - HIGH: Takes actions, handles regulated data, or large audience
    - CRITICAL: Irreversible high-impact actions in regulated context
    """

    def classify(self, profile: DeploymentProfile) -> RiskTier:
        score = 0
        reasons: list[str] = []

        # Audience exposure
        if profile.external_facing:
            score += 2
            reasons.append("External-facing")
        if profile.user_count == "large":
            score += 2
            reasons.append("Large user base (10k+)")
        elif profile.user_count == "medium":
            score += 1

        # Data sensitivity
        if profile.handles_regulated_data:
            score += 3
            reasons.append("Regulated data")
        if profile.handles_pii:
            score += 2
            reasons.append("Handles PII")
        if profile.handles_financial_data:
            score += 2
            reasons.append("Financial data")

        # Autonomy & impact
        if profile.can_take_actions:
            score += 2
            reasons.append("Can take actions")
            if not profile.actions_are_reversible:
                score += 3
                reasons.append("Irreversible actions")
        if profile.max_financial_impact == "high":
            score += 3
            reasons.append("High financial impact (>$100k)")
        elif profile.max_financial_impact == "medium":
            score += 2
            reasons.append("Medium financial impact")

        # Architecture complexity
        if profile.multi_agent:
            score += 2
            reasons.append("Multi-agent system")
        if profile.uses_mcp:
            score += 1
            reasons.append("Uses MCP")

        # Mitigations (reduce score)
        if profile.human_reviews_all_outputs:
            score -= 2
        if profile.has_existing_guardrails:
            score -= 1

        # Regulatory overlay
        if profile.regulated_industry:
            score += 2
            reasons.append("Regulated industry")

        # Map score to tier
        if score <= 2:
            tier = RiskTier.LOW
        elif score <= 6:
            tier = RiskTier.MEDIUM
        elif score <= 10:
            tier = RiskTier.HIGH
        else:
            tier = RiskTier.CRITICAL

        return tier

    def classify_with_reasons(
        self, profile: DeploymentProfile
    ) -> tuple[RiskTier, list[str], list[str], list[tuple[str, int]]]:
        """Classify and return (tier, risk_factors, mitigations, score_breakdown).

        score_breakdown is a list of (description, points) showing how the
        final score was computed.
        """
        risk_factors: list[str] = []
        mitigations: list[str] = []
        score_breakdown: list[tuple[str, int]] = []

        if profile.external_facing:
            risk_factors.append("External-facing deployment")
            score_breakdown.append(("External-facing deployment", 2))
        if profile.user_count == "large":
            risk_factors.append("Large user base (10,000+)")
            score_breakdown.append(("Large user base (10,000+)", 2))
        elif profile.user_count == "medium":
            score_breakdown.append(("Medium user base (100-10k)", 1))
        if profile.handles_pii:
            risk_factors.append("Handles personally identifiable information")
            score_breakdown.append(("Handles PII", 2))
        if profile.handles_regulated_data:
            risk_factors.append("Handles regulated data (HIPAA/SOX/GDPR)")
            score_breakdown.append(("Regulated data (HIPAA/SOX/GDPR)", 3))
        if profile.handles_financial_data:
            risk_factors.append("Handles financial data")
            score_breakdown.append(("Handles financial data", 2))
        if profile.can_take_actions:
            risk_factors.append("AI can take autonomous actions")
            score_breakdown.append(("AI can take autonomous actions", 2))
        if profile.can_take_actions and not profile.actions_are_reversible:
            risk_factors.append("Actions are irreversible")
            score_breakdown.append(("Actions are irreversible", 3))
        if profile.max_financial_impact == "high":
            risk_factors.append("Financial impact: high")
            score_breakdown.append(("High financial impact (>$100k)", 3))
        elif profile.max_financial_impact == "medium":
            risk_factors.append("Financial impact: medium")
            score_breakdown.append(("Medium financial impact (<$100k)", 2))
        if profile.multi_agent:
            risk_factors.append("Multi-agent architecture")
            score_breakdown.append(("Multi-agent architecture", 2))
        if profile.uses_mcp:
            risk_factors.append("Uses Model Context Protocol (MCP)")
            score_breakdown.append(("Uses MCP", 1))
        if profile.regulated_industry:
            risk_factors.append("Regulated industry")
            score_breakdown.append(("Regulated industry", 2))

        if profile.human_reviews_all_outputs:
            mitigations.append("Human reviews all outputs")
            score_breakdown.append(("Human reviews all outputs", -2))
        if profile.has_existing_guardrails:
            mitigations.append("Existing guardrails in place")
            score_breakdown.append(("Existing guardrails in place", -1))
        if not profile.can_take_actions:
            mitigations.append("Read-only (no autonomous actions)")
        if not profile.external_facing:
            mitigations.append("Internal-only deployment")

        tier = self.classify(profile)
        return tier, risk_factors, mitigations, score_breakdown


def generate_intent_statement(profile: DeploymentProfile) -> str:
    """Synthesize a natural-language intent statement from the deployment profile.

    This describes what the AI is supposed to do, who it serves, and what
    constraints it operates under.  Used as the anchor for judge evaluation
    and displayed in the assessment output so users can verify it.
    """
    # ── Audience ──
    if profile.external_facing:
        audience = "external users (customers or the public)"
    else:
        audience = "internal staff"

    user_scale = {
        "small": "a small user base (under 100)",
        "medium": "a medium user base (100-10k)",
        "large": "a large user base (10,000+)",
    }.get(profile.user_count, "an unknown number of users")

    # ── Purpose / name ──
    name_part = f'"{profile.name}" ' if profile.name else ""

    # ── Data ──
    data_parts: list[str] = []
    if profile.handles_pii:
        data_parts.append("personally identifiable information (PII)")
    if profile.handles_financial_data:
        data_parts.append("financial data")
    if profile.handles_regulated_data:
        data_parts.append("regulated data (HIPAA/SOX/GDPR)")
    data_phrase = ""
    if data_parts:
        data_phrase = f" It processes {', '.join(data_parts)}."

    # ── Actions ──
    action_phrase = ""
    if profile.can_take_actions:
        reversibility = "irreversible" if not profile.actions_are_reversible else "reversible"
        impact_map = {
            "none": "",
            "low": " with low financial impact (under $1k)",
            "medium": " with medium financial impact (under $100k)",
            "high": " with high financial impact (over $100k)",
        }
        impact_part = impact_map.get(profile.max_financial_impact, "")
        action_phrase = (
            f" It can take {reversibility} autonomous actions"
            f" (write data, call APIs, make transactions){impact_part}."
        )
    else:
        action_phrase = " It is read-only and cannot take autonomous actions."

    # ── Architecture ──
    arch_parts: list[str] = []
    if profile.multi_agent:
        arch_parts.append("multi-agent orchestration")
    if profile.uses_rag:
        arch_parts.append("retrieval-augmented generation (RAG)")
    if profile.uses_tools:
        arch_parts.append("tool/function calling")
    if profile.uses_mcp:
        arch_parts.append("Model Context Protocol (MCP)")
    arch_phrase = ""
    if arch_parts:
        arch_phrase = f" Its architecture uses {', '.join(arch_parts)}."

    # ── Oversight ──
    oversight_parts: list[str] = []
    if profile.human_reviews_all_outputs:
        oversight_parts.append("all outputs are reviewed by a human before delivery")
    if profile.has_existing_guardrails:
        oversight_parts.append("existing guardrails are in place")
    oversight_phrase = ""
    if oversight_parts:
        oversight_phrase = f" Current safeguards: {'; '.join(oversight_parts)}."

    # ── Regulatory ──
    reg_phrase = ""
    if profile.regulated_industry:
        reg_phrase = " It operates in a regulated industry (healthcare, finance, or legal)."

    return (
        f"This AI deployment {name_part}serves {audience} across {user_scale}."
        f"{data_phrase}{action_phrase}{arch_phrase}{reg_phrase}{oversight_phrase}"
    )
