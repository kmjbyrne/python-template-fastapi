"""Database / engine components."""

import importlib
import logging
from pathlib import Path

from sqlalchemy import event
from sqlmodel import SQLModel, create_engine

sqlite_file_name = "database.db"
path = f"instance/{sqlite_file_name}"
sqlite_url = f"sqlite:///{path}"
engine = create_engine(sqlite_url)

logger = logging.getLogger(__name__)


# Enable foreign keys for every connection
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, _):
    """Enable foreign keys event hook for SQLite."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def import_all_models(models_path: str = "app.adapter.repository.sqlite"):
    """Automatically discover and import all SQLModel classes."""
    models_module = importlib.import_module(models_path)
    models_dir = Path(models_module.__file__).parent

    imported_count = 0
    for py_file in models_dir.glob("*.py"):
        if py_file.name.startswith("_"):
            continue

        module_name = f"{models_path}.{py_file.stem}"
        importlib.import_module(module_name)
        imported_count += 1
        logger.debug(f"Imported models from: {module_name}")

    logger.debug(f"Total model modules imported: {imported_count}")


def drop():
    """Drop all table entities."""
    import_all_models()
    SQLModel.metadata.drop_all(engine)


def init():
    """Primary DB creation entrypoint."""
    import_all_models()
    Path.mkdir(Path(path).parent, parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)
