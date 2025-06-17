"""HTTP Server based on FastAPI exposing evaluation endpoints.

This file supersedes the previous `api.fast` module, aligning with the
`server/` package naming convention.
"""
__version__ = "0.1.0"
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
import time

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from research_evaluator_agent.agents.master import MasterAgent
from research_evaluator_agent.models.schemas import (EvaluateRequest,
                                                     EvaluateResponse)
from research_evaluator_agent.utils.logging import get_logger

logger = get_logger(__name__)



def get_agent() -> MasterAgent:  # pragma: no cover
    """Return singleton MasterAgent; split for easier testing."""
    _master_agent = MasterAgent()
    return _master_agent


# Rate limiter configuration
RATE_LIMIT = 60       # max requests
RATE_PERIOD = 60.0    # time window in seconds
_clients: dict[str, tuple[float, int]] = {}

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host or "unknown"
        now = time.time()
        last_reset, count = _clients.get(client_ip, (now, 0))
        if now - last_reset > RATE_PERIOD:
            last_reset, count = now, 0
        count += 1
        _clients[client_ip] = (last_reset, count)
        if count > RATE_LIMIT:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={"detail": "Too Many Requests"})
        return await call_next(request)


# FastAPI App -----------------------------------------------------------------

def create_app() -> FastAPI:
    app = FastAPI(
        title="Research Evaluator Agent API",
        description="Evaluate generated articles on multiple metrics via prompt-driven agents",
        version=__version__,
    )

    # Add rate limiting middleware
    app.add_middleware(RateLimitMiddleware)
    return app


app = create_app()


# Health check endpoint
@app.get("/healthcheck", tags=["Health"])
async def healthcheck():
    logger.info("Health check passed")
    return {"status": "ok"}

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
    except Exception as exc:
        logger.error(exc)# pragma: no cover
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    return EvaluateResponse(metric_scores=result.get("metric_scores", []),
                            overall_score=result.get("overall_score", 0.0),
                            overall_comment=result.get("overall_comment", ""))
