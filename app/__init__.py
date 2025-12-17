"""Application initialization and logging configuration."""

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from app.config import settings

logging.basicConfig(level=logging.DEBUG)


def setup_logging() -> None:
    """Configure application logging using Python's logging hierarchy.

    Sets up two log files:
    - app.log: Application logs (app.*, core.*)
    - activity.log: HTTP access logs (uvicorn.access)

    This creates a proper logging hierarchy:
    - app.services.draft_planning
    - app.adapters.api.tasks
    - core.services.tasks_service
    etc.

    Each module should use: logger = logging.getLogger(__name__)

    Handlers configured:
    - TimedRotatingFileHandler: Rotates at midnight (ISO date suffix)
    - StreamHandler: Console output
    """
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    app_log_file = log_dir / settings.LOG_FILE
    activity_log_file = log_dir / "activity.log"
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    formatter = logging.Formatter(settings.LOG_FORMAT)

    app_file_handler = TimedRotatingFileHandler(
        filename=app_log_file,
        when=settings.LOG_ROTATION_WHEN,
        interval=settings.LOG_ROTATION_INTERVAL,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    app_file_handler.setLevel(log_level)
    app_file_handler.setFormatter(formatter)

    activity_file_handler = TimedRotatingFileHandler(
        filename=activity_log_file,
        when=settings.LOG_ROTATION_WHEN,
        interval=settings.LOG_ROTATION_INTERVAL,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    activity_file_handler.setLevel(logging.INFO)
    activity_file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    app_logger = logging.getLogger("app")
    app_logger.setLevel(log_level)
    app_logger.addHandler(app_file_handler)
    app_logger.addHandler(console_handler)
    app_logger.propagate = False

    core_logger = logging.getLogger("core")
    core_logger.setLevel(log_level)
    core_logger.addHandler(app_file_handler)
    core_logger.addHandler(console_handler)
    core_logger.propagate = False

    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.handlers = []
    uvicorn_access.addHandler(activity_file_handler)
    uvicorn_access.addHandler(console_handler)
    uvicorn_access.propagate = False

    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.handlers = []
    uvicorn_error.addHandler(app_file_handler)
    uvicorn_error.addHandler(console_handler)
    uvicorn_error.propagate = False

    app_logger.info("Logging initialized")
    app_logger.info(f"Application log: {app_log_file.absolute()}")
    app_logger.info(f"Activity log: {activity_log_file.absolute()}")
    app_logger.info(f"Log level: {settings.LOG_LEVEL}")
    app_logger.info(
        f"Rotation: {settings.LOG_ROTATION_WHEN} (interval: {settings.LOG_ROTATION_INTERVAL})"
    )
    app_logger.info(f"Backup count: {settings.LOG_BACKUP_COUNT} days")
