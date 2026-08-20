"""Database / engine components."""

import importlib
import logging
from pathlib import Path
from typing import Any

from sqlalchemy import event
from sqlmodel import SQLModel, create_engine

from app.config import settings

engine = create_engine(settings.DATABASE_URL)

logger = logging.getLogger(__name__)


if engine.url.get_backend_name() == "sqlite":

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection: Any, _: Any) -> None:
        """Enable foreign keys for every connection. SQLite defaults to off."""
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


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


def drop() -> None:
    """Drop all table entities."""
    import_all_models()
    SQLModel.metadata.drop_all(engine)


def init() -> None:
    """Primary DB creation entrypoint."""
    import_all_models()
    if engine.url.database and engine.url.get_backend_name() == "sqlite":
        Path(engine.url.database).parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)
