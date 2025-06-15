# @Author: weirdgiser
# @Time: 2025/6/14
# @Function:
import operator
from typing import List, Dict, Optional, Annotated
from langgraph.graph import MessagesState, add_messages
from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage
from src.research_evaluator_agent.prompts.vars import MetricVars
class SharedContext(BaseModel):
    """Structured user intent parsed by IntentInterpreter."""

    language: Optional[str] = None  # e.g. "zh" / "en"
    format: Optional[str] = None    # e.g. "table", "bullet"
    focus: List[str] = []           # aspects to focus on
    avoid: List[str] = []           # aspects to avoid

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
