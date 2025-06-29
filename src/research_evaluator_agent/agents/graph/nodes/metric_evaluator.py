"""Generic metric evaluator node.
"""
from __future__ import annotations

from typing import Any

from src.research_evaluator_agent.llms.factory import get_llm
from src.research_evaluator_agent.prompts.template import apply_template
from src.research_evaluator_agent.prompts.vars import MetricVars
from src.research_evaluator_agent.utils.logging import get_logger

from ..types import MetricScoreResult, State

logger = get_logger(__name__)
def metric_evaluator(state: State, *, metric: str, **_: Any):  # noqa: D401
    """Handle evaluation for a single metric.

    Parameters
    ----------
    state : State
        Current shared state.
    metric : str
        Metric identifier this node should evaluate.
    """

    # For demonstration, assign a dummy score (e.g., 0) if not present.
    llm = get_llm("reason").with_structured_output(MetricScoreResult)
    system_prompt = apply_template(metric, MetricVars(metric_name=metric))
    logger.info(f"metric prompt: {system_prompt}")
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"""user_intent:{state.user_intent}\n
                            shared_context:{state.shared_context}\n  
                            article: {state.input_content}"""
        }
    ]
    try:
        response = llm.invoke(messages)
        # Update the metric results dict
        response.metric_name = metric
        logger.info(f"metric evaluator response: {response}")
    except Exception as e:
        logger.error(f"metric evaluator {metric}. error: {e}")
        response = MetricScoreResult(metric_name=metric, score=1, comment="指标评估失败")
    return {"metric_scores": [response]}