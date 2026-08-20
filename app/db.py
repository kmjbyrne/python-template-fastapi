"""Database / engine components."""

import importlib
import logging
from pathlib import Path
from typing import Any

from alembic.config import Config
from sqlalchemy import Engine, event
from sqlmodel import SQLModel, create_engine

from alembic import command

logger = logging.getLogger(__name__)

ALEMBIC_INI = Path(__file__).resolve().parent.parent / "alembic.ini"


def create_db_engine(database_url: str) -> Engine:
    """Build an engine for ``database_url`` and apply backend-specific setup."""
    engine = create_engine(database_url)

    if engine.url.get_backend_name() == "sqlite":
        if engine.url.database:
            Path(engine.url.database).parent.mkdir(parents=True, exist_ok=True)

        @event.listens_for(engine, "connect")
        def enable_foreign_keys(dbapi_connection: Any, _: Any) -> None:
            """Enable foreign keys for every connection. SQLite defaults to off."""
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


def import_all_models(models_path: str = "app.adapter.repository.sqlite") -> None:
    """Automatically discover and import all SQLModel classes."""
    models_module = importlib.import_module(models_path)
    models_dir = Path(str(models_module.__file__)).parent

    imported_count = 0
    for py_file in models_dir.glob("*.py"):
        if py_file.name.startswith("_"):
            continue

        module_name = f"{models_path}.{py_file.stem}"
        importlib.import_module(module_name)
        imported_count += 1
        logger.debug(f"Imported models from: {module_name}")

    logger.debug(f"Total model modules imported: {imported_count}")


def drop(engine: Engine) -> None:
    """Drop all table entities."""
    import_all_models()
    SQLModel.metadata.drop_all(engine)


def migrate(engine: Engine, revision: str = "head") -> None:
    """Bring the database up to ``revision`` using the Alembic migrations.

    Runs over ``engine`` so tests and the app share one connection setup, and
    so an in-memory SQLite database is migrated in place.
    """
    config = Config(str(ALEMBIC_INI))
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, revision)
