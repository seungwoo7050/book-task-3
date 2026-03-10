from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", enable_decoding=False)

    app_name: str = "workspace-service"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    service_name: str = "workspace-service"
    secret_key: str = "change-me"
    token_issuer: str = "workspace-backend-v2"
    token_algorithm: str = "HS256"
    database_url: str = "sqlite+pysqlite:///./workspace_service.db"
    access_token_ttl_seconds: int = 900
    redis_url: str | None = None
    redis_stream_name: str = "workspace-events"


@lru_cache
def get_settings() -> Settings:
    return Settings()
