from sqlmodel import Session

from app.db import engine


def get_session():
    """Provide database session for dependency injection.

    Yields session and ensures cleanup after request.
    """
    with Session(engine) as session:
        yield session
