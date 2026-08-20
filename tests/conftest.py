"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.factory import create_app


@pytest.fixture
def settings(tmp_path) -> Settings:
    """Return settings pointed at a throwaway database."""
    return Settings(DATABASE_URL=f"sqlite:///{tmp_path / 'test.db'}")


@pytest.fixture
def client(settings: Settings) -> TestClient:
    """Return a test client for an app built from the throwaway settings."""
    with TestClient(create_app(settings)) as test_client:
        yield test_client
