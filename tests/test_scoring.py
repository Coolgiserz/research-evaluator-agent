from research_evaluator_agent.utils.scoring import combine_scores, CombineMode


def test_weighted_mean():
    scores = {"a": 0.2, "b": 0.8}
    weights = {"a": 1, "b": 1}
    res = combine_scores(weights, scores, CombineMode.weighted_mean)
    assert res == 0.5


def test_weighted_geo():
    scores = {"a": 0.25, "b": 0.75}
    weights = {"a": 1, "b": 1}
    res = combine_scores(weights, scores, CombineMode.weighted_geometric)
    assert 0 < res < 1 