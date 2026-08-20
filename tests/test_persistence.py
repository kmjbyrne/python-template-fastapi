"""Tests for the persistence layer. Removed by `bin/template-eject persistence`."""

import sqlite3
from typing import Annotated

from fastapi import Depends
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, select

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


def test_health_reports_the_database(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": True, "database": True}


def test_health_fails_when_the_database_is_gone(client: TestClient) -> None:
    def refuse_connection() -> None:
        raise sqlite3.OperationalError("unable to open database file")

    client.app.state.engine = create_engine("sqlite://", creator=refuse_connection)

    response = client.get("/health")
    assert response.status_code == 503
    assert response.json() == {"status": False, "database": False}
