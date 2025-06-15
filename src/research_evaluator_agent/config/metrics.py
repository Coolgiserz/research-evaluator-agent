from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping

from src.research_evaluator_agent.utils.file import load_yaml

__all__ = ["MetricConfiguration"]
DEFAULT_METRICS = [
    "breadth",
    "depth",
    "relevance",
    "novelty",
    "factuality",
]

@dataclass(slots=True)
class MetricInfo:
    """Container for single metric meta information."""

    name: str
    template_path: Path
    weight: float = 1.0

    def load_prompt(self) -> str:
        """Read prompt template text from the template_path."""

        if not self.template_path.exists():
            raise FileNotFoundError(f"Metric '{self.name}': template not found at {self.template_path}")
        return self.template_path.read_text(encoding="utf-8")


class MetricConfiguration(Mapping[str, MetricInfo]):
    """Load and expose metric definitions from YAML configuration.

    The YAML layout is expected to follow below structure::

        metrics:
          breadth:
            template: prompts/breadth.md
            weight: 0.2
          depth:
            template: prompts/depth.md
            weight: 0.2

    Parameters
    ----------
    conf_path : str | Path, default "conf.yaml"
        Path to configuration file.
    project_root : Path | None, optional
        Base directory for resolving *relative* template paths. When *None*, it
        uses the parent of the configuration file.
    """

    def __init__(self, conf_path: str | Path = "conf.yaml", *, project_root: Path | None = None):
        self._conf_path = Path(conf_path).expanduser().resolve()
        if not self._conf_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self._conf_path}")

        self._raw_cfg = load_yaml(self._conf_path)
        self._metrics: Dict[str, MetricInfo] = {}

        metrics_section = self._raw_cfg.get("metrics", {})
        if not isinstance(metrics_section, dict) or not metrics_section:
            raise ValueError("No 'metrics' section found in configuration or it is empty.")

        # Determine root for relative template paths
        root_dir = project_root or self._conf_path.parent

        for name, meta in metrics_section.items():
            if not isinstance(meta, dict):
                raise TypeError(f"Metric '{name}' definition must be mapping, got {type(meta).__name__}")

            tpl_path = meta.get("template")
            if not tpl_path:
                raise KeyError(f"Metric '{name}' missing 'template' field in config")

            weight = float(meta.get("weight", 1.0))
            if weight <= 0:
                raise ValueError(f"Metric '{name}' weight must be positive, got {weight}")

            tpl_path = Path(tpl_path)
            if not tpl_path.is_absolute():
                tpl_path = root_dir / tpl_path

            self._metrics[name] = MetricInfo(name=name, template_path=tpl_path, weight=weight)

    # Mapping protocol impl -------------------------------------------------
    def __getitem__(self, key: str) -> MetricInfo:  # type: ignore[override]
        return self._metrics[key]

    def __iter__(self):  # type: ignore[override]
        return iter(self._metrics)

    def __len__(self) -> int:  # type: ignore[override]
        return len(self._metrics)

    # Convenience helpers ---------------------------------------------------
    @property
    def names(self) -> List[str]:
        """Return list of metric names preserving config order."""

        return list(self._metrics.keys())

    def weights(self) -> Dict[str, float]:
        """Return {metric: weight} mapping."""

        return {name: info.weight for name, info in self._metrics.items()}

    def templates(self) -> Dict[str, str]:
        """Load and return {metric: prompt_text} mapping."""

        return {name: info.load_prompt() for name, info in self._metrics.items()}