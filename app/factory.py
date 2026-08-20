"""Main factory helpers for FastAPI instances."""

from collections.abc import Callable

from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware

from app.config import Settings
from app.log import configure_logging
from app.middleware import RequestIdMiddleware
from app.router import router


def create_app(settings: Settings) -> FastAPI:
    """Create and configure a FastAPI application.

    :param settings: Settings instance the app is built from.
    :type settings: Settings
    :returns: Configured FastAPI application instance
    :rtype: FastAPI
    """
    configure_logging(settings)

    app = FastAPI(
        title=settings.PROJECT_NAME, version=settings.VERSION, description=settings.DESCRIPTION
    )

    checks: dict[str, Callable[[], bool]] = {}

    # persistence:begin
    # Imported here so 'bin/template-eject persistence' can cut the block out
    # without touching the import list above.
    from app.db import create_db_engine, migrate, ping  # noqa: PLC0415

    engine = create_db_engine(settings.DATABASE_URL)
    migrate(engine)
    app.state.engine = engine
    checks["database"] = lambda: ping(app.state.engine)
    # persistence:end

    @app.get("/health")
    def health_check(response: Response) -> dict:
        """Report liveness, plus the state of each dependency the app has."""
        results = {name: check() for name, check in checks.items()}
        healthy = all(results.values())
        if not healthy:
            response.status_code = 503
        return {"status": healthy, **results}

    app.include_router(router)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
