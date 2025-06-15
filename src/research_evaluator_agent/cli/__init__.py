from importlib import import_module

_cli_module = import_module("research_evaluator_agent.cli.main")
app = _cli_module.app  # type: ignore

__all__ = ["app"] 