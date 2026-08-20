"""SQLModel table definitions.

Every module in this package is imported automatically at startup by
``app.db.import_all_models``, so tables declared here are created without any
further registration.
"""

from datetime import UTC, datetime
from uuid import uuid4

from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    """Fields shared between the table model and API schemas."""

    guid: str = Field(default_factory=lambda: str(uuid4()), unique=True, nullable=False)
    created: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    name: str


class Item(ItemBase, table=True):
    """Example table. Delete it once you have real models."""

    id: int | None = Field(default=None, primary_key=True)
