"""Shared test fixtures."""

import importlib
from importlib.util import find_spec

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch) -> TestClient:
    """Return a test client backed by a throwaway database.

    ``app.db`` builds its engine at import time from the cached settings
    singleton, so the environment has to be set and the module reloaded before
    the app is created. Absent entirely once persistence has been ejected.
    """
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")

    import app.config

    app.config.get_settings.cache_clear()
    settings = app.config.get_settings()
    monkeypatch.setattr(app.config, "settings", settings)

    if find_spec("app.db"):
        import app.db

        importlib.reload(app.db)

    from app.factory import create_app

    with TestClient(create_app(settings)) as test_client:
        yield test_client

    app.config.get_settings.cache_clear()
