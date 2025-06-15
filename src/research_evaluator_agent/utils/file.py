"""File helpers: YAML loader and Jinja2 prompt renderer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import yaml
from jinja2 import Template

__all__ = [
    "load_yaml",
    "render_prompt",
]


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load YAML (or JSON) and return dict."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)

    if p.suffix.lower() in {".json"}:
        return json.loads(p.read_text())

    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def render_prompt(template_path: str | Path, **variables: Any) -> str:
    """Render a prompt template with given variables using Jinja2."""
    tpl_str = Path(template_path).read_text(encoding="utf-8")
    tpl = Template(tpl_str)
    return tpl.render(**variables) 