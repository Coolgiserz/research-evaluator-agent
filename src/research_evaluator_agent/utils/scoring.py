"""Scoring utilities with strategy pattern for combination methods."""

from __future__ import annotations

import math
from enum import Enum
from typing import Callable, Dict, Mapping

__all__ = ["CombineMode", "combine_scores"]


class CombineMode(str, Enum):
    weighted_mean = "weighted_mean"
    weighted_geometric = "weighted_geometric"


# Strategy functions ---------------------------------------------------------

def _weighted_mean(weights: Mapping[str, float], scores: Mapping[str, float]) -> float:
    total_w = 0.0
    total = 0.0
    for m, s in scores.items():
        w = weights.get(m, 1.0)
        total_w += w
        total += w * s
    return total / total_w if total_w else 0.0


def _weighted_geo(weights: Mapping[str, float], scores: Mapping[str, float]) -> float:
    log_sum = 0.0
    total_w = 0.0
    for m, s in scores.items():
        w = weights.get(m, 1.0)
        if s <= 0:
            return 0.0  # geometric undefined for non-positive
        log_sum += w * math.log(s)
        total_w += w
    return math.exp(log_sum / total_w) if total_w else 0.0


_STRATEGIES: Dict[CombineMode, Callable[[Mapping[str, float], Mapping[str, float]], float]] = {
    CombineMode.weighted_mean: _weighted_mean,
    CombineMode.weighted_geometric: _weighted_geo,
}


def combine_scores(
    weights: Mapping[str, float],
    scores: Mapping[str, float],
    mode: CombineMode | str = CombineMode.weighted_mean,
) -> float:
    """Combine individual metric scores into overall score.

    Parameters
    ----------
    weights : mapping metric->weight (not required to be normalized)
    scores : mapping metric->score (0-1)
    mode : combination strategy
    """
    mode_enum = CombineMode(mode)  # type: ignore[arg-type]
    func = _STRATEGIES[mode_enum]
    return func(weights, scores) 