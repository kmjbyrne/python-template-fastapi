"""Main factory helpers for FastAPI instances."""

from importlib.util import find_spec

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import Settings
from app.router import router


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

    # Deferred: app.db is absent once persistence is ejected, so a top-level
    # import would break the app for consumers who removed that layer.
    if find_spec("app.db"):
        from app.db import init  # noqa: PLC0415

        init()

    app.include_router(router)
    # noinspection PyTypeChecker
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
