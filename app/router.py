"""Main router entrypoint.

Replace the example route below with your own. Routes that need a database
session take ``Depends(app.dependencies.get_session)``.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def index() -> dict:
    """Return a placeholder response for the service root."""
    return {"status": True}
