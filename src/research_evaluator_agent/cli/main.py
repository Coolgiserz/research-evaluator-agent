import asyncio
import json
from pathlib import Path
from typing import List, Optional

import typer

from research_evaluator_agent.agents.master import MasterAgent

# FIXME: not done
app = typer.Typer(help="Research-Evaluator-Agent CLI")


@app.command()
def evaluate(
    input: Path = typer.Option(..., exists=True, help="Path to article text file"),
    context: Optional[Path] = typer.Option(None, help="Optional context file"),
    metrics: List[str] = typer.Option(
        ["depth", "breadth"], help="Metric names, default to all configured metrics"
    )
):
    """TODO: 评估一篇文章并输出 JSON 结果到 stdout"""
    text = input.read_text(encoding="utf-8")
    ctx_str = context.read_text(encoding="utf-8") if context else None

    agent = MasterAgent()
    result = asyncio.run(agent.aevaluate(text=text, context=ctx_str, metrics=metrics))

    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":  # pragma: no cover
    app() 