import pytest

from src.research_evaluator_agent.agents.graph.builder import _load_metric_order, build_graph, State
from src.research_evaluator_agent.config.metrics import MetricConfiguration
from src.research_evaluator_agent.prompts.vars import MetricVars


def test_load_metric_order_sample():
    metrics = _load_metric_order("conf.yaml.sample")
    assert metrics == [
        "breadth",
        "depth",
        "relevance",
        "novelty",
        "factuality",
    ]

def test_build_graph():
    graph = build_graph()
    assert graph is not None

def test_build_graph_dynamic():
    graph = build_graph("conf.yaml.sample")
    # Basic property: object returned, no exception
    assert graph is not None

    # Introspect node names if available
    node_attr = None
    for attr in ("nodes", "_nodes", "graph", "_graph"):
        if hasattr(graph, attr):
            node_attr = getattr(graph, attr)
            break

    if node_attr:
        # convert to string keys list depending on structure
        if isinstance(node_attr, dict):
            names = node_attr.keys()
        elif isinstance(node_attr, (list, set, tuple)):
            names = node_attr
        else:
            names = []
        for m in ["breadth", "depth", "relevance", "novelty", "factuality"]:
            assert any(f"{m}_evaluator" in str(n) for n in names), f"{m}_evaluator not in graph nodes"
    else:
        # Fallback – ensure string repr contains node names
        g_str = str(graph)
        assert "breadth_evaluator" in g_str

def test_graph_execution():
    graph = build_graph()
    metrics = ["depth", "breadth", "relevance", "novelty"]
    metric_vars = [MetricVars(metric_name=m) for m in metrics]
    initial_state = State(
        metrics=metric_vars,
        user_intent="相思",
        input_content="入夜渐微凉，繁华落地成霜，这一篇心茫茫，还故作不痛不痒。不思量，自难相忘。",
    )
    print("\ninitial_state: ", initial_state)
    result = graph.invoke(initial_state)
    print(f"graph result: {result}")
    assert "overall_score" in result
