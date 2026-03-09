from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", enable_decoding=False)

    app_name: str = "a-auth-lab"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "change-me"
    token_issuer: str = "a-auth-lab-local"
    token_algorithm: str = "HS256"

    database_url: str = "sqlite+pysqlite:///./a_auth_lab.db"
    redis_url: str | None = None
    mailpit_base_url: str = "http://localhost:8025"

    access_token_ttl_seconds: int = 900
    refresh_token_ttl_seconds: int = 14 * 24 * 60 * 60
    verification_token_ttl_seconds: int = 24 * 60 * 60
    password_reset_ttl_seconds: int = 30 * 60

    secure_cookies: bool = False
    cookie_domain: str | None = None
    allowed_origins: list[str] = Field(default_factory=list)

    access_cookie_name: str = "access_token"
    refresh_cookie_name: str = "refresh_token"
    csrf_cookie_name: str = "csrf_token"
    csrf_header_name: str = "X-CSRF-Token"

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        if not value:
            return []
        return [origin.strip() for origin in value.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
