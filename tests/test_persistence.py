"""Tests for the persistence layer. Removed by `bin/template-eject persistence`."""

from sqlmodel import Session, select

from app.adapter.repository.sqlite.models import Item


def test_item_round_trips(tmp_path) -> None:
    from sqlmodel import SQLModel, create_engine

    engine = create_engine(f"sqlite:///{tmp_path / 'round-trip.db'}")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Item(name="example"))
        session.commit()

    with Session(engine) as session:
        stored = session.exec(select(Item)).one()
        assert stored.name == "example"
        assert stored.guid
