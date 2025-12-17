"""Main factory helpers for FastAPI instances."""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import Settings
from app.db import init
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

    init()

    app.include_router(router)
    origins = ["http://localhost:3000", "https://ditloid.org"]
    # noinspection PyTypeChecker
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
