from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ============================================================
    # PROJECT
    # ============================================================

    PROJECT_NAME: str = "Market Analyzer API"

    APP_NAME: str = "Market Analyzer API"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    # ============================================================
    # API
    # ============================================================

    API_V1_PREFIX: str = "/api/v1"

    # ============================================================
    # DATABASE
    # ============================================================

    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/pricedb"
    )

    # ============================================================
    # REDIS
    # ============================================================

    REDIS_URL: str = Field(
        default="redis://localhost:6379/0"
    )

    # ============================================================
    # JWT
    # ============================================================

    SECRET_KEY: str = "CHANGE_ME"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ============================================================
    # CORS
    # ============================================================

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]

    # ============================================================
    # LOGGING
    # ============================================================

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def alembic_database_url(self) -> str:
        return self.DATABASE_URL

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()