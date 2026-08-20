"""Application configuration."""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

_ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


class Settings(BaseSettings):
    """Application settings and configuration.

    Real environment variables always win. Below those, env files are read in
    increasing order of precedence:

    1. .env (default fallback)
    2. .env.local (git ignored, for local overrides)
    3. .env.{ENVIRONMENT} (e.g. .env.development, .env.test)

    Missing files are skipped.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", f".env.{_ENVIRONMENT}"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Environment
    ENVIRONMENT: str = "development"  # development, test, staging, production
    PROJECT_NAME: str = "CHANGEME"
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "A FastAPI application"

    # Origins permitted by the CORS middleware
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Database (ignored when the persistence layer is ejected)
    DATABASE_URL: str = "sqlite:///instance/database.db"

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
