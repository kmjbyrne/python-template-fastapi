"""Application configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration.

    Values can be overridden via environment variables or .env file.

    Environment file loading priority:
    1. .env.{ENVIRONMENT} (e.g., .env.development, .env.test)
    2. .env.local (git ignored, for local overrides)
    3. .env (default fallback)
    """

    # Environment
    ENVIRONMENT: str = "development"  # development, test, staging, production
    PROJECT_NAME: str = "CHANGEME"
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "A FastAPI application for task management"

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_FILE: str = "app.log"
    LOG_ROTATION_WHEN: str = "midnight"
    LOG_ROTATION_INTERVAL: int = 1
    LOG_BACKUP_COUNT: int = 30
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Uses lru_cache to ensure settings are loaded only once.
    """
    return Settings()


settings = get_settings()
