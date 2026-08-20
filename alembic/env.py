"""Alembic environment.

Runs in two modes:

- From the CLI (``uv run alembic ...``): connects using ``DATABASE_URL`` from
  app settings.
- From ``app.db.migrate`` at startup: reuses the application's engine, handed
  over through ``config.attributes["connection"]``.
"""

from sqlalchemy import Connection, engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context
from app.config import get_settings
from app.db import import_all_models

config = context.config

import_all_models()
target_metadata = SQLModel.metadata


def _configure(connection: Connection) -> None:
    # Batch mode lets SQLite apply ALTER TABLE operations it does not support natively.
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,
        compare_type=True,
    )


def run_migrations_offline() -> None:
    """Emit SQL to stdout without a live connection."""
    context.configure(
        url=get_settings().DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against the app engine or a fresh one built from settings."""
    connection = config.attributes.get("connection")
    if connection is not None:
        _configure(connection)
        with context.begin_transaction():
            context.run_migrations()
        return

    config.set_main_option("sqlalchemy.url", get_settings().DATABASE_URL)
    engine = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with engine.connect() as fresh_connection:
        _configure(fresh_connection)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
