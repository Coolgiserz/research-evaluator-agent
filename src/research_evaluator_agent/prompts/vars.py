from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Dict, Any

__all__ = [
    "BaseVars",
    "MetricVars",
    "CustomMetricVars",
    "InterpreterVars",
    "vars_to_dict",
]


@dataclass
class BaseVars:
    """Common variables shared by most templates."""

    language: str = "zh"
    current_time: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        # Jinja variables use upper-case keys
        return {
            "LANGUAGE": data["language"],
            "CURRENT_TIME": data["current_time"],
        }


@dataclass
class MetricVars(BaseVars):
    """Variables for standard metric evaluator templates (breadth, depth, etc.)."""
    metric_name: str = ""
    weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        return base


@dataclass
class CustomMetricVars(MetricVars):
    """Variables for *custom_metric.md* template."""
    metric_definition: str = ""
    rubric: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update(
            {
                "METRIC_NAME": self.metric_name,
                "METRIC_DEFINITION": self.metric_definition,
                "RUBRIC": self.rubric,
            }
        )
        return data


@dataclass
class InterpreterVars(BaseVars):
    """Variables for *interpreter.md* template."""

    metrics: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update(
            {
                "METRICS": self.metrics,
            }
        )
        return data


def vars_to_dict(var_obj: Any) -> Dict[str, Any]:
    """Convert dataclass instance or mapping to dict suitable for template rendering."""

    # Already dict-like
    if isinstance(var_obj, dict):
        return var_obj  # type: ignore[return-value]

    # Dataclass with `to_dict`
    if hasattr(var_obj, "to_dict"):
        return var_obj.to_dict()  # type: ignore[return-value]

    raise TypeError("Unsupported variables object for template rendering.") 