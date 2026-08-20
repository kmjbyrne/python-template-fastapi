"""Tests for the persistence layer. Removed by `bin/template-eject persistence`."""

from typing import Annotated

from fastapi import Depends
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.adapter.repository.sqlite.models import Item
from app.dependencies import get_session


def test_item_round_trips(client: TestClient) -> None:
    engine = client.app.state.engine

    with Session(engine) as session:
        session.add(Item(name="example"))
        session.commit()

    with Session(engine) as session:
        stored = session.exec(select(Item)).one()
        assert stored.name == "example"
        assert stored.guid


def test_get_session_uses_app_engine(client: TestClient) -> None:
    @client.app.get("/_items")
    def list_items(session: Annotated[Session, Depends(get_session)]) -> list[str]:
        return [item.name for item in session.exec(select(Item)).all()]

    with Session(client.app.state.engine) as session:
        session.add(Item(name="via-dependency"))
        session.commit()

    assert client.get("/_items").json() == ["via-dependency"]
