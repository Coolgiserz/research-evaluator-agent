"""Graph builder that wires IntentInterpreter and metric evaluators dynamically."""

from __future__ import annotations

from pathlib import Path
from typing import List

from langgraph.graph import END, START, StateGraph

from src.research_evaluator_agent.utils.file import load_yaml

from .nodes import combine_metrics, interpreter, metric_evaluator
from .types import OutputState, State


def _load_metric_order(config_path: str | Path = "conf.yaml") -> List[str]:
    """Load metric keys from YAML config; fallback to default order."""

    cfg_path = Path(config_path)
    if not cfg_path.exists():
        # Default metric order if configuration missing
        return [
            "breadth",
            "depth",
            "relevance",
            "novelty",
            "factuality",
        ]

    cfg = load_yaml(cfg_path)
    metrics_cfg = cfg.get("metrics", {})
    if isinstance(metrics_cfg, dict):
        return list(metrics_cfg.keys())
    # fallback
    return []


def build_graph(config_path: str | Path = "conf.yaml"):
    """Construct a StateGraph with interpreter + N metric evaluator nodes.

    Parameters
    ----------
    config_path : str | Path, optional
        YAML file containing `metrics` section. Each key will become a metric
        evaluator node in the graph. Missing file defaults to a preset order.
    """

    metrics = _load_metric_order(config_path)
    graph = StateGraph(State, output=OutputState)

    # 1) Intent Interpreter node
    graph.add_node("intent_interpreter", interpreter)

    # 2) Dynamically add metric evaluator nodes
    evaluator_nodes = []
    for metric_name in metrics:
        node_name = f"{metric_name}_evaluator"

        def _make_metric_node(name: str):
            def _node(state):
                return metric_evaluator(state, metric=name)

            _node.__name__ = f"evaluator_{name}"
            return _node

        graph.add_node(node_name, _make_metric_node(metric_name))
        graph.add_edge("intent_interpreter", node_name)
        evaluator_nodes.append(node_name)

    graph.add_node("combine_metrics", combine_metrics)

    for node_name in evaluator_nodes:
        graph.add_edge(node_name, "combine_metrics")

    # terminate
    graph.add_edge("combine_metrics", END)

    # add start edge
    graph.add_edge(START, "intent_interpreter")

    return graph.compile()
