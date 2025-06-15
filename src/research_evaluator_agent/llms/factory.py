"""LLM factory – build cached ChatOpenAI (or compatible) instances from YAML config.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from langchain_openai import ChatOpenAI

from src.research_evaluator_agent.utils.file import load_yaml
from src.research_evaluator_agent.utils.logging import get_logger

logger = get_logger(__name__)

_DEFAULT_CONF = "conf.yaml"


def _resolve_conf_path(custom_path: str | None = None) -> Path:
    if custom_path:
        return Path(custom_path).expanduser().resolve()
    # allow ENV override
    env_path = os.getenv("REA_CONF")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return Path(__file__).parent.parent.parent.parent / _DEFAULT_CONF  # project root


def _build_chat_openai(cfg: Dict[str, Any]) -> ChatOpenAI:
    """Instantiate ChatOpenAI wrapper from single model config dict."""
    api_key = cfg.get("api_key") or os.getenv("OPENAI_API_KEY")
    base_url = cfg.get("base_url")
    model = cfg.get("model")
    temperature = cfg.get("temperature", 0.0)

    if not api_key or not base_url or not model:
        raise ValueError("Invalid LLM config – requires api_key, base_url, model")

    logger.info("Creating ChatOpenAI", model=model, base_url=str(base_url))
    return ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
        temperature=temperature,
        extra_body={
            "enable_thinking": False
        },
        timeout=120,
    )


@lru_cache(maxsize=3)
def get_llm(name: str = "basic", *, conf_path: str | None = None) -> ChatOpenAI:  # noqa: D401
    """Return cached LLM instance by logical name (e.g. 'basic', 'reason')."""
    path = _resolve_conf_path(conf_path)
    cfg = load_yaml(path)
    if "llm" not in cfg or name not in cfg["llm"]:
        raise KeyError(f"LLM config for '{name}' not found in {path}")

    model_cfg = cfg["llm"][name]
    return _build_chat_openai(model_cfg) 