"""Smoke tests that hold regardless of which optional layers are present."""

from fastapi.testclient import TestClient


def test_health_reports_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": True}


def test_root_route_is_registered(client: TestClient) -> None:
    assert client.get("/").status_code == 200


def test_openapi_schema_builds(client: TestClient) -> None:
    assert client.get("/openapi.json").status_code == 200
