"""CLI assessment tool — classify your deployment and get a prioritized implementation plan.

Run: airs assess
Run against a live model: airs assess --provider openai --model gpt-4o
"""

from __future__ import annotations

import asyncio
import json
import os
import time

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from airs.core.controls import ControlRegistry, MATSOTier
from airs.core.models import AIRequest, AIResponse, RiskTier
from airs.core.risk import DeploymentProfile, RiskClassifier
from airs.runtime import (
    CircuitBreaker,
    GuardrailChain,
    PACEController,
    RegexGuardrail,
    SecurityPipeline,
)
from airs.cli.scenarios import select_judge_scenarios, select_scenarios
from airs.runtime.judge import RuleBasedJudge

console = Console()

# ── API key env var names ──────────────────────────────────────────────────
PROVIDER_ENV_VARS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
}


def _ask_bool(question: str, default: bool = False) -> bool:
    suffix = " [Y/n]" if default else " [y/N]"
    result = typer.prompt(question + suffix, default="y" if default else "n", show_default=False)
    return result.strip().lower() in ("y", "yes", "true", "1")


def _ask_choice(question: str, choices: list[str], default: str = "") -> str:
    choices_str = " / ".join(choices)
    result = typer.prompt(f"{question} ({choices_str})", default=default or choices[0])
    while result not in choices:
        console.print(f"[red]Please choose one of: {choices_str}[/red]")
        result = typer.prompt(f"{question} ({choices_str})", default=default or choices[0])
    return result


TIER_COLORS = {
    RiskTier.LOW: "green",
    RiskTier.MEDIUM: "yellow",
    RiskTier.HIGH: "red",
    RiskTier.CRITICAL: "bold red",
}

TIER_DESCRIPTIONS = {
    RiskTier.LOW: "Fast Lane eligible — minimal guardrails + logging + feature flag",
    RiskTier.MEDIUM: "Full guardrails + sampling Judge + periodic human review",
    RiskTier.HIGH: "Full architecture, 100% Judge evaluation, human-in-the-loop for writes",
    RiskTier.CRITICAL: "All layers + mandatory human approval + tested PACE failover",
}

PACE_TABLE = {
    RiskTier.LOW: {
        "Primary": "Guardrails active, logging enabled",
        "Alternate": "Tighten guardrails, increase logging",
        "Contingency": "Human review for all outputs",
        "Emergency": "Feature flag OFF → static fallback",
    },
    RiskTier.MEDIUM: {
        "Primary": "Guardrails + 5% Judge sampling",
        "Alternate": "Guardrails + 100% Judge evaluation",
        "Contingency": "Human approval for all outputs",
        "Emergency": "Circuit breaker → non-AI fallback",
    },
    RiskTier.HIGH: {
        "Primary": "Guardrails + 100% Judge + human review queue",
        "Alternate": "Tighten scope, block new tool access",
        "Contingency": "Read-only mode, human approval for all",
        "Emergency": "Full stop, incident response activated",
    },
    RiskTier.CRITICAL: {
        "Primary": "All layers + mandatory human approval",
        "Alternate": "Reduced scope, elevated monitoring",
        "Contingency": "Minimal operation, human decides all",
        "Emergency": "Immediate shutdown, IR team engaged",
    },
}


def assess_cmd(
    output_json: bool = typer.Option(False, "--json", help="Output as JSON"),
    non_interactive: bool = typer.Option(False, "--non-interactive", help="Use defaults"),
    provider: str = typer.Option("", "--provider", help="Model provider: openai or anthropic"),
    model: str = typer.Option("", "--model", help="Model name, e.g. gpt-4o or claude-sonnet-4-20250514"),
    judge_model: str = typer.Option(
        "",
        "--judge-model",
        help="LLM judge model (e.g. gpt-4o-mini or claude-sonnet-4-20250514). Enables LLM-as-Judge evaluation.",
    ),
    judge_provider: str = typer.Option(
        "",
        "--judge-provider",
        help="Judge provider: openai or anthropic",
    ),
) -> None:
    """Assess your AI deployment and get a prioritized security implementation plan."""

    if not non_interactive:
        console.print()
        console.print(
            Panel(
                "[bold]AIRS Deployment Assessment[/bold]\n\n"
                "Answer the following questions about your AI deployment.\n"
                "This will classify your risk tier and recommend controls.",
                title="AI Runtime Security",
                border_style="blue",
            )
        )
        console.print()

    # Gather deployment profile
    if non_interactive:
        profile = DeploymentProfile()
    else:
        profile = _gather_profile()

    # Classify
    classifier = RiskClassifier()
    tier, risk_factors, mitigations = classifier.classify_with_reasons(profile)

    # Get recommended controls
    registry = ControlRegistry()
    maso_tier = None
    if profile.multi_agent:
        maso_tier = _infer_maso_tier(tier)
    controls = registry.prioritized_for(tier, maso_tier)

    if output_json:
        _output_json(profile, tier, risk_factors, mitigations, controls, maso_tier)
    else:
        _output_rich(profile, tier, risk_factors, mitigations, controls, maso_tier)

    # ── Live model test ────────────────────────────────────────────────
    # Ask interactively if no --provider was given and we're in interactive mode
    if not provider and not non_interactive and not output_json:
        console.print()
        console.print("[bold]7. Live Model Test (optional)[/bold]")
        run_live = _ask_bool("  Run a live model test against a real provider?")
        if run_live:
            provider = _ask_choice("  Provider", ["openai", "anthropic"], "openai")
            default_model = _default_model(provider)
            model = typer.prompt(f"  Model name", default=default_model)

            # Prompt for the provider API key now
            env_var = PROVIDER_ENV_VARS[provider]
            api_key = os.environ.get(env_var)
            if not api_key:
                key_urls = {
                    "openai": "https://platform.openai.com/api-keys",
                    "anthropic": "https://console.anthropic.com/settings/keys",
                }
                console.print()
                console.print(Panel(
                    f"No [bold]{env_var}[/bold] found in environment.\n\n"
                    f"Get an API key here: [link={key_urls[provider]}]{key_urls[provider]}[/link]\n\n"
                    f"Paste it below to continue, or set it for future runs:\n\n"
                    f"  [dim]export {env_var}=sk-...[/dim]\n\n"
                    f"[dim]Note: Live model tests make API calls that incur costs on your\n"
                    f"account (typically a few cents per run). The assessment works fine\n"
                    f"without --provider — live testing is entirely optional.[/dim]",
                    title="API Key Required",
                    border_style="yellow",
                ))
                api_key = typer.prompt(f"  Paste your {env_var}").strip()
                if not api_key:
                    console.print("[red]No key provided. Skipping live test.[/red]")
                    provider = ""
                else:
                    console.print(f"  [green]Key received ({api_key[:8]}...)[/green]")
                    os.environ[env_var] = api_key

            if provider and not judge_model:
                console.print()
                use_judge = _ask_bool(
                    "  Also run LLM-as-Judge tests?"
                )
                if use_judge:
                    judge_provider = _ask_choice(
                        "  Judge provider", ["openai", "anthropic"], provider
                    )
                    default_judge = _default_judge_model(judge_provider)
                    judge_model = typer.prompt(
                        "  Judge model name", default=default_judge
                    )
                    # Prompt for judge API key if not already available
                    judge_env_var = PROVIDER_ENV_VARS[judge_provider]
                    judge_api_key = os.environ.get(judge_env_var)
                    if not judge_api_key:
                        key_urls = {
                            "openai": "https://platform.openai.com/api-keys",
                            "anthropic": "https://console.anthropic.com/settings/keys",
                        }
                        console.print()
                        console.print(Panel(
                            f"No [bold]{judge_env_var}[/bold] found in environment.\n\n"
                            f"Get an API key here: [link={key_urls[judge_provider]}]{key_urls[judge_provider]}[/link]\n\n"
                            f"Paste your key below, or set it:\n\n"
                            f"  [dim]export {judge_env_var}=sk-...[/dim]",
                            title="Judge API Key Required",
                            border_style="yellow",
                        ))
                        judge_api_key = typer.prompt(f"  Paste your {judge_env_var}").strip()
                        if not judge_api_key:
                            console.print("[yellow]No key provided. Skipping judge tests.[/yellow]")
                            judge_model = ""
                        else:
                            console.print(f"  [green]Key received ({judge_api_key[:8]}...)[/green]")
                            os.environ[judge_env_var] = judge_api_key

    if provider:
        live_results = asyncio.run(
            _run_live_test(provider, model, output_json, judge_model, judge_provider, profile)
        )
        if output_json:
            # Print the live results as a separate JSON object
            console.print_json(json.dumps({"live_test": live_results}, indent=2))
        # Rich output is handled inside _run_live_test


# ── Live model testing ─────────────────────────────────────────────────────


def _get_model_caller(provider: str, model: str):
    """Return an async function that calls the specified provider/model."""
    provider = provider.lower()
    env_var = PROVIDER_ENV_VARS.get(provider)

    if not env_var:
        console.print(f"[red]Unknown provider: {provider}. Use: openai, anthropic[/red]")
        raise typer.Exit(1)

    api_key = os.environ.get(env_var)
    if not api_key:
        key_urls = {
            "openai": "https://platform.openai.com/api-keys",
            "anthropic": "https://console.anthropic.com/settings/keys",
        }
        console.print()
        console.print(Panel(
            f"No [bold]{env_var}[/bold] found in environment.\n\n"
            f"Get an API key here: [link={key_urls[provider]}]{key_urls[provider]}[/link]\n\n"
            f"Paste it below to continue, or set it for future runs:\n\n"
            f"  [dim]export {env_var}=sk-...[/dim]\n\n"
            f"[dim]Note: Live model tests make API calls that incur costs on your\n"
            f"account (typically a few cents per run). The assessment works fine\n"
            f"without --provider — live testing is entirely optional.[/dim]",
            title="API Key Required",
            border_style="yellow",
        ))
        api_key = typer.prompt(f"  Paste your {env_var}").strip()
        if not api_key:
            console.print("[red]No key provided. Skipping live test.[/red]")
            raise typer.Exit(1)
        console.print(f"  [green]Key received ({api_key[:8]}...)[/green]")
        console.print()

    if provider == "openai":
        try:
            from openai import AsyncOpenAI
        except ImportError:
            console.print("[red]openai package not installed. Run: pip install openai[/red]")
            raise typer.Exit(1)

        client = AsyncOpenAI(api_key=api_key)

        async def call_openai(text: str) -> str:
            completion = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": text}],
                max_tokens=256,
            )
            return completion.choices[0].message.content or ""

        return call_openai

    elif provider == "anthropic":
        try:
            import anthropic
        except ImportError:
            console.print("[red]anthropic package not installed. Run: pip install anthropic[/red]")
            raise typer.Exit(1)

        client = anthropic.AsyncAnthropic(api_key=api_key)

        async def call_anthropic(text: str) -> str:
            message = await client.messages.create(
                model=model,
                max_tokens=256,
                messages=[{"role": "user", "content": text}],
            )
            return message.content[0].text

        return call_anthropic

    # Unreachable but keeps type checkers happy
    raise typer.Exit(1)


async def _run_live_test(
    provider: str, model: str, output_json: bool, judge_model: str = "",
    judge_provider: str = "", profile: DeploymentProfile | None = None,
) -> dict:
    """Run profile-aware test scenarios against a live model through the AIRS pipeline."""
    model = model or _default_model(provider)
    call_model = _get_model_caller(provider, model)
    profile = profile or DeploymentProfile()

    pipeline = SecurityPipeline(
        guardrails=GuardrailChain([RegexGuardrail()]),
        judge=RuleBasedJudge(),
        circuit_breaker=CircuitBreaker(),
        pace=PACEController(),
    )

    # Select scenarios based on the deployment profile
    guardrail_scenarios = select_scenarios(profile)
    judge_scenarios = select_judge_scenarios(profile) if judge_model else []

    # ── Part 1: Guardrail tests ───────────────────────────────────────
    total_prompts = len(guardrail_scenarios) + len(judge_scenarios)
    if not output_json:
        console.print()
        subtitle = f"Provider: {provider}  |  Model: {model}"
        if judge_model:
            subtitle += f"  |  Judge: {judge_model}"
        # Count profile-specific scenarios (non-baseline)
        profile_count = sum(1 for s in guardrail_scenarios if s.category != "Baseline")
        profile_count += sum(1 for s in judge_scenarios if s.category != "Judge Baseline")
        console.print(Panel(
            f"[bold]Live Model Test[/bold]\n\n"
            f"{subtitle}\n"
            f"Running {total_prompts} test prompts through the AIRS pipeline.\n"
            f"({profile_count} tailored to your deployment profile)",
            title="Live Assessment",
            border_style="cyan",
        ))

    if not output_json:
        console.print()
        console.print("[bold]Guardrail Tests[/bold] — input filtering + output evaluation")

    guardrail_results = []
    current_category = ""
    for scenario in guardrail_scenarios:
        # Print category header when it changes
        if not output_json and scenario.category != current_category:
            current_category = scenario.category
            if current_category != "Baseline":
                console.print()
            console.print(f"  [bold dim]── {current_category} ──[/bold dim]")

        request = AIRequest(input_text=scenario.prompt, model=model)
        start = time.monotonic()

        input_result = await pipeline.evaluate_input(request)
        model_output = ""
        output_result = None

        if input_result.allowed:
            try:
                model_output = await call_model(scenario.prompt)
            except Exception as e:
                model_output = f"[ERROR] {e}"

            response = AIResponse(
                request_id=request.request_id,
                output_text=model_output,
                model=model,
            )
            output_result = await pipeline.evaluate_output(request, response)

        elapsed_ms = (time.monotonic() - start) * 1000
        blocked = not input_result.allowed or (output_result is not None and not output_result.allowed)
        blocked_by = ""
        if not input_result.allowed:
            blocked_by = input_result.blocked_by.value if input_result.blocked_by else "unknown"
        elif output_result and not output_result.allowed:
            blocked_by = output_result.blocked_by.value if output_result.blocked_by else "unknown"

        result_entry = {
            "test": scenario.label,
            "category": scenario.category,
            "why": scenario.why,
            "prompt": scenario.prompt,
            "blocked": blocked,
            "blocked_by": blocked_by,
            "expected_blocked": scenario.expect_blocked,
            "correct": blocked == scenario.expect_blocked,
            "model_output": model_output[:200] if model_output else "",
            "latency_ms": round(elapsed_ms, 1),
        }
        guardrail_results.append(result_entry)

        if not output_json:
            status = "[green]PASS[/green]" if result_entry["correct"] else "[red]FAIL[/red]"
            action = "[red]BLOCKED[/red]" if blocked else "[green]ALLOWED[/green]"
            console.print(f"  {status}  {action}  [bold]{scenario.label}[/bold]  ({elapsed_ms:.0f}ms)")
            if blocked and blocked_by:
                console.print(f"         Blocked by: {blocked_by}")
            if scenario.category != "Baseline":
                console.print(f"         [dim]{scenario.why}[/dim]")
            if model_output and not blocked:
                preview = model_output[:120].replace("\n", " ")
                console.print(f"         Response: [dim]{preview}...[/dim]")

    # ── Part 2: Judge tests (only when --judge-model is provided) ─────
    judge_results = []
    if judge_model and judge_scenarios:
        jp = (judge_provider or "openai").lower()
        judge_env_var = PROVIDER_ENV_VARS.get(jp)

        if not judge_env_var:
            console.print(f"[red]Unknown judge provider: {jp}. Use: openai, anthropic[/red]")
            raise typer.Exit(1)

        judge_api_key = os.environ.get(judge_env_var)
        if not judge_api_key:
            key_urls = {
                "openai": "https://platform.openai.com/api-keys",
                "anthropic": "https://console.anthropic.com/settings/keys",
            }
            console.print()
            console.print(Panel(
                f"No [bold]{judge_env_var}[/bold] found in environment.\n\n"
                f"Get an API key here: [link={key_urls[jp]}]{key_urls[jp]}[/link]\n\n"
                f"Paste your key below, or set it:\n\n"
                f"  [dim]export {judge_env_var}=sk-...[/dim]",
                title="Judge API Key Required",
                border_style="yellow",
            ))
            judge_api_key = typer.prompt(f"  Paste your {judge_env_var}").strip()
            if not judge_api_key:
                console.print("[red]No key provided. Skipping judge tests.[/red]")
                raise typer.Exit(1)

        if jp == "anthropic":
            try:
                import anthropic  # noqa: F401
            except ImportError:
                console.print(
                    "[red]Anthropic judge requires the anthropic package. "
                    "Run: pip install anthropic[/red]"
                )
                raise typer.Exit(1)

            from airs.runtime.judge import AnthropicLLMJudge
            llm_judge = AnthropicLLMJudge(model=judge_model, api_key=judge_api_key)
        else:
            try:
                from openai import AsyncOpenAI  # noqa: F811
            except ImportError:
                console.print(
                    "[red]OpenAI judge requires the openai package. "
                    "Run: pip install openai[/red]"
                )
                raise typer.Exit(1)

            from airs.runtime.judge import LLMJudge
            llm_judge = LLMJudge(model=judge_model, api_key=judge_api_key)

        if not output_json:
            console.print()
            console.print(
                f"[bold]Judge Tests[/bold] — LLM-as-Judge ({judge_model}) "
                f"evaluates model outputs"
            )

        current_category = ""
        for scenario in judge_scenarios:
            if not output_json and scenario.category != current_category:
                current_category = scenario.category
                if current_category != "Judge Baseline":
                    console.print()
                console.print(f"  [bold dim]── {current_category} ──[/bold dim]")

            request = AIRequest(input_text=scenario.prompt, model=model)
            start = time.monotonic()

            input_result = await pipeline.evaluate_input(request)
            model_output = ""
            judge_verdict = ""
            judge_reason = ""
            judge_confidence = 0.0

            if input_result.allowed:
                try:
                    model_output = await call_model(scenario.prompt)
                except Exception as e:
                    model_output = f"[ERROR] {e}"

                evaluation = await llm_judge.evaluate(
                    input_text=scenario.prompt,
                    output_text=model_output,
                )
                judge_verdict = evaluation.verdict.value
                judge_reason = evaluation.reason
                judge_confidence = evaluation.confidence

            elapsed_ms = (time.monotonic() - start) * 1000

            result_entry = {
                "test": scenario.label,
                "category": scenario.category,
                "why": scenario.why,
                "prompt": scenario.prompt,
                "model_output": model_output[:200] if model_output else "",
                "judge_verdict": judge_verdict,
                "judge_reason": judge_reason,
                "judge_confidence": judge_confidence,
                "latency_ms": round(elapsed_ms, 1),
            }
            judge_results.append(result_entry)

            if not output_json:
                verdict_colors = {
                    "pass": "green",
                    "review": "yellow",
                    "escalate": "red",
                }
                v_color = verdict_colors.get(judge_verdict, "dim")
                console.print(
                    f"  [{v_color}]{judge_verdict.upper()}[/{v_color}]  "
                    f"[bold]{scenario.label}[/bold]  ({elapsed_ms:.0f}ms)"
                )
                console.print(f"         Reason: [dim]{judge_reason}[/dim]")
                if scenario.category != "Judge Baseline":
                    console.print(f"         [dim]{scenario.why}[/dim]")
                if model_output:
                    preview = model_output[:120].replace("\n", " ")
                    console.print(f"         Response: [dim]{preview}...[/dim]")

    # ── Summary ───────────────────────────────────────────────────────
    guardrail_passed = sum(1 for r in guardrail_results if r["correct"])
    guardrail_total = len(guardrail_results)

    if not output_json:
        console.print()
        color = "green" if guardrail_passed == guardrail_total else "yellow"
        parts = [f"Guardrails: {guardrail_passed}/{guardrail_total}"]
        if judge_results:
            parts.append(f"Judge: {len(judge_results)} evaluated")
        # Show category breakdown
        categories = {}
        for r in guardrail_results:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = {"passed": 0, "total": 0}
            categories[cat]["total"] += 1
            if r["correct"]:
                categories[cat]["passed"] += 1

        breakdown = "\n".join(
            f"  {cat}: {v['passed']}/{v['total']}"
            for cat, v in categories.items()
        )
        console.print(Panel(
            f"[{color}]{guardrail_passed}/{guardrail_total} guardrail tests matched expected behavior[/{color}]\n"
            + ("  |  ".join(parts)) + "\n\n"
            + breakdown,
            title="Live Test Summary",
            border_style=color,
        ))

    return {"guardrail_tests": guardrail_results, "judge_tests": judge_results}


def _default_model(provider: str) -> str:
    defaults = {
        "openai": "gpt-4o",
        "anthropic": "claude-sonnet-4-20250514",
    }
    return defaults.get(provider.lower(), "")


def _default_judge_model(provider: str) -> str:
    defaults = {
        "openai": "gpt-4o-mini",
        "anthropic": "claude-sonnet-4-20250514",
    }
    return defaults.get(provider.lower(), "")


def _gather_profile() -> DeploymentProfile:
    """Interactive questionnaire."""
    console.print("[bold]1. Deployment Context[/bold]")
    name = typer.prompt("  Deployment name (optional)", default="")
    external = _ask_bool("  Is this deployment external-facing (customers/public)?")
    user_count = _ask_choice("  Expected user count", ["small", "medium", "large"], "small")

    console.print()
    console.print("[bold]2. Data Sensitivity[/bold]")
    pii = _ask_bool("  Does it handle PII (names, emails, addresses)?")
    regulated = _ask_bool("  Does it handle regulated data (HIPAA, SOX, GDPR)?")
    financial = _ask_bool("  Does it handle financial data?")

    console.print()
    console.print("[bold]3. Autonomy & Impact[/bold]")
    actions = _ask_bool("  Can the AI take actions (write data, call APIs, make transactions)?")
    reversible = True
    impact = "none"
    if actions:
        reversible = _ask_bool("  Are those actions reversible?", default=True)
        impact = _ask_choice("  Maximum financial impact per action", ["none", "low", "medium", "high"], "none")

    console.print()
    console.print("[bold]4. Architecture[/bold]")
    multi_agent = _ask_bool("  Is this a multi-agent system?")
    rag = _ask_bool("  Does it use RAG (retrieval-augmented generation)?")
    tools = _ask_bool("  Does it use tools/function calling?")
    mcp = False
    if tools:
        mcp = _ask_bool("  Does it use MCP (Model Context Protocol)?")

    console.print()
    console.print("[bold]5. Existing Controls[/bold]")
    human_review = _ask_bool("  Does a human review ALL outputs before delivery?")
    existing_guardrails = _ask_bool("  Do you have existing guardrails in place?")

    console.print()
    console.print("[bold]6. Regulatory[/bold]")
    regulated_industry = _ask_bool("  Is this in a regulated industry (healthcare, finance, legal)?")

    return DeploymentProfile(
        name=name,
        external_facing=external,
        user_count=user_count,
        handles_pii=pii,
        handles_regulated_data=regulated,
        handles_financial_data=financial,
        can_take_actions=actions,
        actions_are_reversible=reversible,
        max_financial_impact=impact,
        multi_agent=multi_agent,
        uses_rag=rag,
        uses_tools=tools,
        uses_mcp=mcp,
        human_reviews_all_outputs=human_review,
        has_existing_guardrails=existing_guardrails,
        regulated_industry=regulated_industry,
    )


def _infer_maso_tier(risk_tier: RiskTier) -> MATSOTier:
    if risk_tier in (RiskTier.LOW, RiskTier.MEDIUM):
        return MATSOTier.SUPERVISED
    elif risk_tier == RiskTier.HIGH:
        return MATSOTier.MANAGED
    else:
        return MATSOTier.AUTONOMOUS


def _output_rich(
    profile: DeploymentProfile,
    tier: RiskTier,
    risk_factors: list[str],
    mitigations: list[str],
    controls: list,
    maso_tier: MATSOTier | None,
) -> None:
    console.print()

    # Risk tier result
    color = TIER_COLORS[tier]
    console.print(Panel(
        f"[{color}]Risk Tier: {tier.value.upper()}[/{color}]\n\n"
        f"{TIER_DESCRIPTIONS[tier]}",
        title="Assessment Result",
        border_style=color,
    ))

    # Risk factors
    if risk_factors:
        console.print()
        console.print("[bold]Risk Factors:[/bold]")
        for f in risk_factors:
            console.print(f"  [red]![/red] {f}")

    if mitigations:
        console.print()
        console.print("[bold]Mitigating Factors:[/bold]")
        for m in mitigations:
            console.print(f"  [green]+[/green] {m}")

    # MASO tier
    if maso_tier:
        console.print()
        console.print(f"[bold]Multi-Agent Tier:[/bold] {maso_tier.value.title()}")

    # PACE posture
    console.print()
    pace_table = Table(title="PACE Resilience Posture", show_header=True)
    pace_table.add_column("State", style="bold", width=14)
    pace_table.add_column("Posture")

    pace_data = PACE_TABLE[tier]
    state_colors = {"Primary": "green", "Alternate": "yellow", "Contingency": "red", "Emergency": "bold red"}
    for state, desc in pace_data.items():
        pace_table.add_row(f"[{state_colors[state]}]{state}[/{state_colors[state]}]", desc)
    console.print(pace_table)

    # Recommended controls
    console.print()
    ctrl_table = Table(title=f"Recommended Controls ({len(controls)} total)", show_header=True)
    ctrl_table.add_column("#", width=4)
    ctrl_table.add_column("ID", width=10)
    ctrl_table.add_column("Control", width=35)
    ctrl_table.add_column("Layer", width=16)
    ctrl_table.add_column("Priority")

    for i, c in enumerate(controls, 1):
        priority = "Implement first" if i <= 3 else ("Phase 2" if i <= 8 else "Phase 3")
        p_color = "green" if i <= 3 else ("yellow" if i <= 8 else "dim")
        ctrl_table.add_row(
            str(i),
            c.id,
            c.name,
            c.layer.value.replace("_", " ").title(),
            f"[{p_color}]{priority}[/{p_color}]",
        )
    console.print(ctrl_table)

    # Implementation hints for top 3
    console.print()
    console.print(Panel("[bold]Quick Start — Top 3 Controls[/bold]", border_style="green"))
    for c in controls[:3]:
        console.print(f"\n  [bold]{c.id}: {c.name}[/bold]")
        console.print(f"  {c.description}")
        if c.implementation_hint:
            console.print(f"  [dim]Hint: {c.implementation_hint}[/dim]")

    # Code snippet
    console.print()
    console.print(Panel(
        _generate_code_snippet(tier, maso_tier),
        title="Getting Started with airs SDK",
        border_style="blue",
    ))


def _output_json(
    profile: DeploymentProfile,
    tier: RiskTier,
    risk_factors: list[str],
    mitigations: list[str],
    controls: list,
    maso_tier: MATSOTier | None,
) -> None:
    output = {
        "profile": profile.model_dump(),
        "assessment": {
            "risk_tier": tier.value,
            "maso_tier": maso_tier.value if maso_tier else None,
            "risk_factors": risk_factors,
            "mitigations": mitigations,
        },
        "controls": [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "layer": c.layer.value,
                "domain": c.domain.value,
                "implementation_hint": c.implementation_hint,
                "owasp_refs": c.owasp_refs,
                "priority": i + 1,
            }
            for i, c in enumerate(controls)
        ],
        "pace_posture": PACE_TABLE[tier],
    }
    console.print_json(json.dumps(output, indent=2))


def _generate_code_snippet(tier: RiskTier, maso_tier: MATSOTier | None) -> str:
    snippet = '''from airs.runtime import (
    SecurityPipeline, GuardrailChain, RegexGuardrail,
    CircuitBreaker, PACEController,
)
from airs.core.models import AIRequest, AIResponse

# Build the three-layer pipeline
pipeline = SecurityPipeline(
    guardrails=GuardrailChain([RegexGuardrail()]),
    circuit_breaker=CircuitBreaker(),
    pace=PACEController(),
)

# Evaluate input
request = AIRequest(input_text=user_input)
input_result = await pipeline.evaluate_input(request)
if not input_result.allowed:
    return fallback_response(input_result)

# Call your AI model
ai_output = await your_model(request.input_text)
response = AIResponse(request_id=request.request_id, output_text=ai_output)

# Evaluate output
output_result = await pipeline.evaluate_output(request, response)
if not output_result.allowed:
    return fallback_response(output_result)

return ai_output'''
    return snippet
