"""Helper utilities to build LangGraph/LLM agents."""

from __future__ import annotations

from typing import Any, Iterable

from langgraph.prebuilt import create_react_agent

from src.research_evaluator_agent.config.agents import AgentType
from src.research_evaluator_agent.llms.factory import get_llm
from src.research_evaluator_agent.prompts.template import apply_template
from src.research_evaluator_agent.prompts.vars import (InterpreterVars,
                                                       MetricVars)

__all__ = ["create_agent"]


def create_agent(
    *,
    name: str,
    model: Any | None = None,
    tools: Iterable[Any] | None = None,
    agent_type: str = "react",
) -> Any:
    """Factory to create a LangGraph agent ready for use.

    Parameters
    ----------
    name : str
        Logical agent name.
    model : Any, optional
        LLM model instance; if ``None`` will use ``get_llm()`` default.
    tools : iterable, optional
        Tools accessible to the agent.
    prompt_template : str | PromptTemplate, optional
        Prompt guiding the agent. When ``None`` defaults to the standard prompt
        used by `create_react_agent` internally.
    agent_type : str, default "react"
        Currently only supports "react".
    """
    if name == AgentType.INTERPRETER:
        prompt_template = apply_template(name, InterpreterVars())
    else:
        prompt_template = apply_template(name, MetricVars(metric_name=name))
    if model is None:
        print(f"Agent {name}: No model provided, using default model")
        model = get_llm("basic")

    if tools is None:
        print(f"Agent {name}: No tools provided, using default tools")
        tools = []

    if agent_type != "react":
        raise ValueError("Only 'react' agent_type is supported currently.")

    # Convert template str to PromptTemplate if needed
    prompt = None
    if prompt_template is not None:

        pass

    return create_react_agent(name=name, model=model, tools=list(tools), prompt=prompt)