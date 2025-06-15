"""Research-Evaluator-Agent top-level package."""

from importlib.metadata import version, PackageNotFoundError

from research_evaluator_agent.agents.master import MasterAgent

try:
    __version__ = version("research-evaluator-agent")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

__all__ = [
    "evaluate_article",
    "__version__",
]


# Convenience helper used by README examples
async def _evaluate_async(text: str, context: str | None, metrics: list[str] | None):
    agent = MasterAgent()
    return await agent.aevaluate(text=text, context=context, metrics=metrics)


def evaluate_article(
    text: str,
    context: str | None = None,
    metrics: list[str] | None = None,
):
    """Synchronously evaluate an article using the default MasterAgent."""

    import asyncio

    return asyncio.run(_evaluate_async(text, context, metrics)) 