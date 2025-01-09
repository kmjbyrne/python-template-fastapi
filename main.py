"""Main entry point for the FastAPI application.

Uses factory pattern to create app instance.
"""

import uvicorn

from app.config import settings
from app.factory import create_app

settings.print()
app = create_app(settings)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
