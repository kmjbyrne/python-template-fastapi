"""Tests for logging setup and the request id middleware."""

import json
import logging

from fastapi.testclient import TestClient

from app.config import Settings
from app.factory import create_app
from app.log import JsonFormatter, RequestIdFilter, configure_logging


def test_generates_a_request_id(client: TestClient) -> None:
    response = client.get("/health")
    assert len(response.headers["x-request-id"]) == 32


def test_reuses_an_incoming_request_id(client: TestClient) -> None:
    response = client.get("/health", headers={"X-Request-ID": "abc-123"})
    assert response.headers["x-request-id"] == "abc-123"


class _CaptureIds(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.addFilter(RequestIdFilter())

    def emit(self, record: logging.LogRecord) -> None:
        self.ids.append(record.request_id)


def test_log_lines_carry_the_request_id(client: TestClient) -> None:
    @client.app.get("/_log")
    def log_something() -> dict:
        logging.getLogger("app.test").info("hello")
        return {}

    capture = _CaptureIds()
    logger = logging.getLogger("app.test")
    logger.addHandler(capture)
    try:
        client.get("/_log", headers={"X-Request-ID": "trace-me"})
    finally:
        logger.removeHandler(capture)

    assert capture.ids == ["trace-me"]


def test_json_formatter_emits_one_object_per_line() -> None:
    record = logging.LogRecord("app.x", logging.WARNING, __file__, 1, "boom %s", ("bang",), None)
    line = JsonFormatter().format(record)
    payload = json.loads(line)
    assert payload["level"] == "WARNING"
    assert payload["message"] == "boom bang"
    assert payload["request_id"] == "-"


def test_configure_logging_owns_uvicorn_loggers(tmp_path) -> None:
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.addHandler(logging.NullHandler())
    uvicorn_access.propagate = False

    configure_logging(Settings(DATABASE_URL=f"sqlite:///{tmp_path / 'x.db'}", LOG_JSON=True))

    assert uvicorn_access.handlers == []
    assert uvicorn_access.propagate is True
    assert isinstance(logging.getLogger().handlers[0].formatter, JsonFormatter)
    create_app(Settings(DATABASE_URL=f"sqlite:///{tmp_path / 'y.db'}"))
