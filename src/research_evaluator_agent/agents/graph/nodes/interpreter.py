from ..types import State
from src.research_evaluator_agent.llms.factory import get_llm
from src.research_evaluator_agent.agents.graph.types import SharedContext
from src.research_evaluator_agent.prompts.template import apply_template
from src.research_evaluator_agent.prompts.vars import  InterpreterVars, MetricVars
from src.research_evaluator_agent.config.metrics import  DEFAULT_METRICS

from src.research_evaluator_agent.utils.logging import  get_logger
logger = get_logger(__name__)
def interpreter(state: State):
    """
    Interpreter node, used to interpret and evaluate the article.
    Args:
        state (State): 当前状态对象，包含用户要求、文章内容和评估结果。
    Returns:
        dict: 包含解释结果的字典。

    """
    if state.metrics is None or len(state.metrics) == 0:
        logger.warning("No metrics found, using default metrics: breadth, depth, relevance, novelty")
        state.metrics = [MetricVars(metric_name=metric_name) for metric_name in DEFAULT_METRICS]
    else:
        logger.info(f"Using metrics: {state.metrics}")
    metrics = [metric_name for metric_name in DEFAULT_METRICS]
    logger.info(f"metrics: {state.metrics}")
    llm = get_llm("reason")
    llm_with_output = llm.with_structured_output(SharedContext)
    system_prompt = apply_template(
        "interpreter",
        InterpreterVars(
            metrics=metrics
        )
    )
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": f"expectation: {state.user_intent}",
        },
    ]
    shared_context = llm_with_output.invoke(messages)
    logger.info(f"interpreter response: {shared_context}")
    return {"shared_context": shared_context,
            "metrics": state.metrics}