"""Logging utilities using structlog for structured logs."""

from __future__ import annotations

import logging
from typing import Any

import structlog

__all__ = ["get_logger"]


def _configure_once() -> None:  # pragma: no cover
    """Configure structlog & stdlib logging only once."""

    if getattr(_configure_once, "_configured", False):  # type: ignore[attr-defined]
        return

    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    _configure_once._configured = True  # type: ignore[attr-defined]


def get_logger(name: str | None = None, **kwargs: Any):
    """Return a structlog logger with optional default context."""

    _configure_once()
    logger = structlog.get_logger(name)
    if kwargs:
        logger = logger.bind(**kwargs)
    return logger 