from __future__ import annotations

import asyncio
from typing import List, Optional, Dict
from .graph.builder import build_graph
from .graph.types import State, MetricVars
class MasterAgent:
    """协调多个 PromptEvaluator，并聚合分数。

    此处为最小可运行实现，后续可替换为基于 Langgraph 的真实实现。
    """

    def __init__(self) -> None:
        self._graph = build_graph()


    async def _dummy_evaluate_metric(self, metric: str, text: str, context: Optional[str]) -> float:
        """占位符评估逻辑：返回固定分数 0.5，用于接口连通性测试。"""
        await asyncio.sleep(0.01)  # 模拟异步调用
        return 0.5

    async def aevaluate(
        self,
        text: str,
        context: Optional[str] = None,
        metrics: Optional[List[str]] = None,
    ) -> Dict:
        if metrics is None:
            metrics = ["breadth", "depth", "relevance", "novelty", "factuality"]
        metric_vars = [MetricVars(metric_name=m) for m in metrics]
        initial_state = State(
            metrics=metric_vars,
            user_intent=context,
            input_content=text,
        )
        # 计算综合得分（加权平均）
        response = await self._graph.ainvoke(initial_state)

        return response

    def evaluate(
        self,
        text: str,
        context: Optional[str] = None,
        metrics: Optional[List[str]] = None,
    ) -> Dict:
        metric_vars = [MetricVars(metric_name=m) for m in metrics]
        initial_state = State(
            metrics=metric_vars,
            user_intent=context,
            input_content=text,
        )
        # 计算综合得分（加权平均）
        response = self._graph.invoke(initial_state)

        return response