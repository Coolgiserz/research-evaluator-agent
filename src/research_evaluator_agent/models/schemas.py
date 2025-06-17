from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

__all__ = [
    "EvaluateRequest",
    "EvaluateResponse",
]


class EvaluateRequest(BaseModel):
    """HTTP 请求体 / CLI 传参统一数据结构"""

    text: str = Field(..., description="待评估的文章全文")
    context: Optional[str] = Field(None, description="可选的上下文或参考文本")
    metrics: List[str] = Field(
        default_factory=list,
        description="评估指标名称列表，如 ['breadth', 'depth', 'relevance']",
    )


class EvaluateResponse(BaseModel):
    """评分结果统一输出"""

    metric_scores: List = Field(..., description="各指标得分，区间 [1,5]")
    overall_score: float = Field(..., description="综合得分")
    overall_comment: str = Field(..., description="整体评价")