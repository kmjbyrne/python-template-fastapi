"""Reusable FastAPI dependencies."""

from collections.abc import Generator

from fastapi import Request
from sqlmodel import Session


def get_session(request: Request) -> Generator[Session, None, None]:
    """Provide a database session bound to the engine created in ``create_app``.

    Yields session and ensures cleanup after request.
    """
    with Session(request.app.state.engine) as session:
        yield session
