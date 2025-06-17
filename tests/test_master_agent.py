import asyncio

import pytest

from research_evaluator_agent.agents.master import MasterAgent


@pytest.mark.asyncio
async def test_evaluate_default_metrics():
    agent = MasterAgent()
    result = await agent.aevaluate(text="dummy")

    # Check basic structure
    assert "overall_comment" in result and "overall_score" in result

@pytest.mark.asyncio
async def test_evaluate_subset_metrics():
    agent = MasterAgent()
    metrics = ["breadth", "novelty"]
    result = await agent.aevaluate(text="dummy", metrics=metrics)

    assert set(result["scores"].keys()) == set(metrics)
    # Weighted mean with default weights 0.2 and 0.1 over subset -> need normalization inside agent (it normalizes) so still 0.5
    assert result["overall_score"] == pytest.approx(0.5) 