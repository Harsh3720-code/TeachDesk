"""FastAPI application factory.

Run locally with ``make run`` (uvicorn ``--factory app.main:create_app``).
"""

import logging

from fastapi import FastAPI

from app.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the application. Tests pass their own ``Settings``."""
    settings = settings or Settings()
    logging.basicConfig(level=settings.log_level)

    app = FastAPI(title="TeachDesk")

    @app.get("/health")
    def health() -> dict[str, str]:
        """Liveness check: the process is up and serving requests."""
        return {"status": "ok"}

    return app
