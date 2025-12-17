from datetime import UTC, date, datetime
from typing import ClassVar
from uuid import uuid4

from sqlalchemy.util import hybridproperty
from sqlmodel import Field, Relationship, SQLModel


class DitloidBase(SQLModel):
    """Base DB model for storing Ditloid objects."""

    guid: str = Field(default_factory=lambda: str(uuid4()), unique=True, nullable=False)
    active: bool = Field(default=True, nullable=False)
    created: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    updated: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    short: str
    schedule: date = Field()


class Ditloid(DitloidBase, table=True):
    """Main DB model for storing Ditloid objects."""

    id: int | None = Field(default=None, primary_key=True)
    guesses: list["GuessModel"] = Relationship()
    solution: str
    guess_count: ClassVar

    @hybridproperty
    def guess_count(self) -> int:
        """Get the number of guesses on a specific Ditloid."""
        return len(self.guesses)


class GuessBase(SQLModel):
    """Base model for Guest guesses."""

    id: int | None = Field(default=None, primary_key=True)
    guest_guid: str = Field(default_factory=lambda: str(uuid4()), nullable=False)
    created: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    guess_value: str
    solved: bool


class GuessModel(GuessBase, table=True):
    """Low level Guess model for DB entity."""

    __tablename__ = "guess"
    ditloid_id: int = Field(foreign_key="ditloid.id")
