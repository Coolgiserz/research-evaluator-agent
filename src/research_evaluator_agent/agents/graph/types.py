# @Author: weirdgiser
# @Time: 2025/6/14
# @Function:
import operator
from typing import Annotated, Dict, List, Optional

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field

from src.research_evaluator_agent.prompts.vars import MetricVars


class SharedContext(BaseModel):
    """Structured user intent parsed by IntentInterpreter."""

    format: Optional[str] = None    # e.g. "table", "bullet"
    focus: Optional[List[str]] = Field(default_factory=list)           # aspects to focus on
    avoid: List[str] = Field(default_factory=list)             # aspects to avoid

class MetricScoreResult(BaseModel):
    """Structured result from MetricEvaluator."""
    metric_name: str = ""
    score: int = 0
    comment: str = Field(default="", description="Explanation for the score")

class State(BaseModel):
    """State for the agent system, extends MessagesState with next field."""

    # Runtime Variables
    locale: str = "zh-CN"
    metrics: Optional[List[MetricVars]] = None
    user_intent: str
    input_content: str
    messages: Annotated[List[AnyMessage], add_messages] = None
    metric_scores: Annotated[List[MetricScoreResult], operator.add] = None
    shared_context: Optional[SharedContext] = None


class OutputState(BaseModel):
    """Output state for the agent system."""
    overall_score: float = 0.0
    overall_comment: str = ""
    metric_scores: Annotated[List[MetricScoreResult], operator.add] = None
