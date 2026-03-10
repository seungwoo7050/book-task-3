from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", enable_decoding=False)

    app_name: str = "identity-service"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    service_name: str = "identity-service"
    secret_key: str = "change-me"
    token_issuer: str = "workspace-backend-v2"
    token_algorithm: str = "HS256"
    database_url: str = "sqlite+pysqlite:///./identity_service.db"
    access_token_ttl_seconds: int = 900
    refresh_token_ttl_seconds: int = 14 * 24 * 60 * 60
    verification_token_ttl_seconds: int = 24 * 60 * 60


@lru_cache
def get_settings() -> Settings:
    return Settings()
