"""Main router entrypoint.

Replace the example routes below with your own. Routers that need a database
session depend on ``app.dependencies.get_session``; see ``app/example.py``.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def index() -> dict:
    """Return a placeholder response for the service root."""
    return {"status": True}
