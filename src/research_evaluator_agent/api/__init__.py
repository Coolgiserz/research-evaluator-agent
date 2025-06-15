from importlib import import_module

_app_module = import_module("research_evaluator_agent.api.fast")
app = _app_module.app  # type: ignore

__all__ = ["app"] 