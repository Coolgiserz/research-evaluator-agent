"""HTTP Server based on FastAPI exposing evaluation endpoints.

This file supersedes the previous `api.fast` module, aligning with the
`server/` package naming convention.
"""
__version__ = "0.1.0"

from fastapi import FastAPI, HTTPException, Depends, status
from research_evaluator_agent.models.schemas import EvaluateRequest, EvaluateResponse
from research_evaluator_agent.agents.master import MasterAgent
from research_evaluator_agent.utils.logging import get_logger
logger = get_logger(__name__)

# Dependency -----------------------------------------------------------------

_master_agent = MasterAgent()

def get_agent() -> MasterAgent:  # pragma: no cover
    """Return singleton MasterAgent; split for easier testing."""
    return _master_agent


# FastAPI App -----------------------------------------------------------------

def create_app() -> FastAPI:
    app = FastAPI(
        title="Research Evaluator Agent API",
        description="Evaluate generated articles on multiple metrics via prompt-driven agents",
        version=__version__,
    )

    return app


app = create_app()

@app.post("/evaluate", response_model=EvaluateResponse, tags=["Evaluation"])
async def evaluate(  # noqa: D401  # type: ignore
    request: EvaluateRequest,
    agent: MasterAgent = Depends(get_agent),
) -> EvaluateResponse:
    """Evaluate an article and return scores."""
    try:
        result = await agent.aevaluate(
            text=request.text,
            context=request.context,
            metrics=request.metrics
        )
        logger.info(f"evaluate result: {result}")
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    return EvaluateResponse(metric_scores=result.get("metric_scores", []),
                            overall_score=result.get("overall_score", 0.0),
                            overall_comment=result.get("overall_comment", ""))
