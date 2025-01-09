"""Main factory helpers for FastAPI instances."""

from fastapi import FastAPI

from app.config import Settings


def create_app(settings: Settings) -> FastAPI:
    """Create and configure a FastAPI application.

    :param settings: Optional settings instance. Defaults to production settings.
    :type settings: Settings
    :returns: Configured FastAPI application instance
    :rtype: FastAPI
    """
    app = FastAPI(
        title=settings.PROJECT_NAME, version=settings.VERSION, description=settings.DESCRIPTION
    )

    @app.get("/health")
    async def health_check() -> dict:
        return {"status": True}

    return app
