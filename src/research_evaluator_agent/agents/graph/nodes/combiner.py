"""Combine metric results from state into overall score placeholder."""

from __future__ import annotations
from .metric_evaluator import logger
from ..types import State, OutputState
from langchain_core.tools import tool
from typing import Annotated
from src.research_evaluator_agent.utils.scoring import combine_scores
from src.research_evaluator_agent.agents.agents import create_agent
from src.research_evaluator_agent.llms.factory import get_llm
from src.research_evaluator_agent.config.agents import AgentType
from src.research_evaluator_agent.prompts.template import apply_template
from src.research_evaluator_agent.utils.json_utils import json_repair
@tool
def combine_score_helper(
 weights: Annotated[dict, "A dictionary of metric names and their corresponding weights."],
 scores: Annotated[dict, "A dictionary of metric names and their corresponding scores."],
 mode: Annotated[str, "The mode to use for combining the scores. Can be 'weighted_mean' or 'weighted_geometric'."] = "weighted",
):
    """
    TODO Combine metric scores into an overall score.
    Args:
        weights (dict): A dictionary of metric names and their corresponding weights.
        scores (dict): A dictionary of metric names and their corresponding scores.
        mode (str): The mode to use for combining the scores. Can be 'weighted_mean' or 'weighted_geometric'.
    """

    return combine_scores(weights, scores, mode)

def combine_metrics(state: State) -> OutputState:
    """Aggregate individual metric scores.

    Current placeholder: 计算简单平均值。
    """
    llm = get_llm(name="basic")
    metric_weights_list = (
        state.get("metrics", []) if isinstance(state, dict) else state.metrics  # type: ignore[attr-defined]
    )

    metric_weights = {m.metric_name: m.weight for m in metric_weights_list}
    metric_scores = {i.metric_name: i.score for i in state.metric_scores}
    logger.info(f"metric score len {len(metric_scores)}. weights: {metric_weights}")

    # TODO: combine metrics based on user requirements.
    overall = combine_scores(metric_weights, metric_scores) if metric_scores else 0.0
    messages = [
        {
            "role": "system",
            "content": apply_template("combiner", variables={"LANGUAGE": "zh"})
        },
        {
            "role": "user",
            "content": f"""{metric_scores}"""
        }
    ]

    # Invoke LLM and parse JSON response robustly
    try:
        raw = llm.invoke(messages)
        parsed = json_repair.repair_json(raw.content)
        summary = json_repair.loads(parsed)["summary"]
    except Exception as e:
        logger.error(f"Failed to parse JSON response: {e}")
        summary = ""
    return OutputState(overall_score=overall,
                       overall_comment=summary)