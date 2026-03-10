from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", enable_decoding=False)

    app_name: str = "notification-service"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    service_name: str = "notification-service"
    database_url: str = "sqlite+pysqlite:///./notification_service.db"
    redis_url: str | None = None
    redis_stream_name: str = "workspace-events"
    redis_pubsub_channel: str = "gateway.notifications"


@lru_cache
def get_settings() -> Settings:
    return Settings()
