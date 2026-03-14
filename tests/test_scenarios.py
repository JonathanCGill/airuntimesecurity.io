"""Tests for profile-aware scenario selection."""

from airs.cli.scenarios import (
    BASELINE_SCENARIOS,
    JUDGE_SCENARIOS,
    Scenario,
    select_judge_scenarios,
    select_scenarios,
)
from airs.core.risk import DeploymentProfile


class TestBaselineAlwaysIncluded:
    """Baseline scenarios must appear regardless of profile."""

    def test_default_profile_gets_baseline(self):
        scenarios = select_scenarios(DeploymentProfile())
        labels = {s.label for s in scenarios}
        for baseline in BASELINE_SCENARIOS:
            assert baseline.label in labels

    def test_complex_profile_still_has_baseline(self):
        profile = DeploymentProfile(
            handles_pii=True,
            handles_financial_data=True,
            can_take_actions=True,
            multi_agent=True,
        )
        scenarios = select_scenarios(profile)
        labels = {s.label for s in scenarios}
        for baseline in BASELINE_SCENARIOS:
            assert baseline.label in labels


class TestPIIScenarios:
    def test_pii_profile_includes_pii_scenarios(self):
        profile = DeploymentProfile(handles_pii=True)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "PII Protection" in categories

    def test_no_pii_profile_excludes_pii_scenarios(self):
        profile = DeploymentProfile(handles_pii=False)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "PII Protection" not in categories


class TestFinancialScenarios:
    def test_financial_profile_includes_financial_scenarios(self):
        profile = DeploymentProfile(handles_financial_data=True)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Financial Data" in categories

    def test_no_financial_profile_excludes_financial_scenarios(self):
        profile = DeploymentProfile(handles_financial_data=False)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Financial Data" not in categories


class TestRegulatedDataScenarios:
    def test_regulated_data_includes_scenarios(self):
        profile = DeploymentProfile(handles_regulated_data=True)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Regulated Data" in categories

    def test_no_regulated_data_excludes_scenarios(self):
        profile = DeploymentProfile(handles_regulated_data=False)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Regulated Data" not in categories


class TestActionScenarios:
    def test_action_profile_includes_action_scenarios(self):
        profile = DeploymentProfile(can_take_actions=True)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Action Safety" in categories

    def test_no_action_profile_excludes_action_scenarios(self):
        profile = DeploymentProfile(can_take_actions=False)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Action Safety" not in categories

    def test_irreversible_actions_get_extra_scenarios(self):
        profile = DeploymentProfile(
            can_take_actions=True, actions_are_reversible=False
        )
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Irreversible Actions" in categories

    def test_reversible_actions_skip_irreversible_scenarios(self):
        profile = DeploymentProfile(
            can_take_actions=True, actions_are_reversible=True
        )
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Irreversible Actions" not in categories


class TestMultiAgentScenarios:
    def test_multi_agent_includes_scenarios(self):
        profile = DeploymentProfile(multi_agent=True)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Multi-Agent" in categories

    def test_single_agent_excludes_scenarios(self):
        profile = DeploymentProfile(multi_agent=False)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Multi-Agent" not in categories


class TestToolScenarios:
    def test_tools_includes_scenarios(self):
        profile = DeploymentProfile(uses_tools=True)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Tool Safety" in categories

    def test_no_tools_excludes_scenarios(self):
        profile = DeploymentProfile(uses_tools=False)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Tool Safety" not in categories


class TestMCPScenarios:
    def test_mcp_includes_scenarios(self):
        profile = DeploymentProfile(uses_mcp=True)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "MCP Safety" in categories

    def test_no_mcp_excludes_scenarios(self):
        profile = DeploymentProfile(uses_mcp=False)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "MCP Safety" not in categories


class TestRAGScenarios:
    def test_rag_includes_scenarios(self):
        profile = DeploymentProfile(uses_rag=True)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "RAG Safety" in categories

    def test_no_rag_excludes_scenarios(self):
        profile = DeploymentProfile(uses_rag=False)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "RAG Safety" not in categories


class TestExternalFacingScenarios:
    def test_external_includes_scenarios(self):
        profile = DeploymentProfile(external_facing=True)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "External Exposure" in categories

    def test_internal_excludes_scenarios(self):
        profile = DeploymentProfile(external_facing=False)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "External Exposure" not in categories


class TestRegulatedIndustryScenarios:
    def test_regulated_industry_includes_scenarios(self):
        profile = DeploymentProfile(regulated_industry=True)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Regulatory Compliance" in categories

    def test_non_regulated_excludes_scenarios(self):
        profile = DeploymentProfile(regulated_industry=False)
        scenarios = select_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Regulatory Compliance" not in categories


class TestScenarioCount:
    """More complex profiles should produce more scenarios."""

    def test_default_profile_only_baseline(self):
        scenarios = select_scenarios(DeploymentProfile())
        assert len(scenarios) == len(BASELINE_SCENARIOS)

    def test_complex_profile_has_more_scenarios(self):
        simple = select_scenarios(DeploymentProfile())
        complex_profile = DeploymentProfile(
            handles_pii=True,
            handles_financial_data=True,
            can_take_actions=True,
            multi_agent=True,
            uses_tools=True,
            external_facing=True,
        )
        complex_scenarios = select_scenarios(complex_profile)
        assert len(complex_scenarios) > len(simple)

    def test_every_scenario_has_required_fields(self):
        profile = DeploymentProfile(
            handles_pii=True,
            handles_financial_data=True,
            handles_regulated_data=True,
            can_take_actions=True,
            actions_are_reversible=False,
            multi_agent=True,
            uses_tools=True,
            uses_mcp=True,
            uses_rag=True,
            external_facing=True,
            regulated_industry=True,
        )
        for scenario in select_scenarios(profile):
            assert scenario.label, "Scenario must have a label"
            assert scenario.prompt, "Scenario must have a prompt"
            assert scenario.category, "Scenario must have a category"
            assert scenario.why, "Scenario must explain why it's relevant"


class TestJudgeScenarioSelection:
    def test_default_profile_gets_judge_baseline(self):
        scenarios = select_judge_scenarios(DeploymentProfile())
        labels = {s.label for s in scenarios}
        for baseline in JUDGE_SCENARIOS:
            assert baseline.label in labels

    def test_default_profile_only_judge_baseline(self):
        scenarios = select_judge_scenarios(DeploymentProfile())
        assert len(scenarios) == len(JUDGE_SCENARIOS)

    def test_pii_profile_gets_judge_pii_scenarios(self):
        profile = DeploymentProfile(handles_pii=True)
        scenarios = select_judge_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Judge: PII" in categories

    def test_regulated_profile_gets_judge_compliance_scenarios(self):
        profile = DeploymentProfile(regulated_industry=True)
        scenarios = select_judge_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Judge: Compliance" in categories

    def test_regulated_data_also_gets_compliance_scenarios(self):
        profile = DeploymentProfile(handles_regulated_data=True)
        scenarios = select_judge_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Judge: Compliance" in categories

    def test_financial_profile_gets_judge_financial_scenarios(self):
        profile = DeploymentProfile(handles_financial_data=True)
        scenarios = select_judge_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Judge: Financial" in categories

    def test_action_profile_gets_judge_action_scenarios(self):
        profile = DeploymentProfile(can_take_actions=True)
        scenarios = select_judge_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Judge: Actions" in categories

    def test_external_profile_gets_judge_external_scenarios(self):
        profile = DeploymentProfile(external_facing=True)
        scenarios = select_judge_scenarios(profile)
        categories = {s.category for s in scenarios}
        assert "Judge: External" in categories

    def test_complex_profile_gets_many_judge_scenarios(self):
        profile = DeploymentProfile(
            handles_pii=True,
            handles_financial_data=True,
            can_take_actions=True,
            external_facing=True,
            regulated_industry=True,
        )
        scenarios = select_judge_scenarios(profile)
        assert len(scenarios) > len(JUDGE_SCENARIOS)
