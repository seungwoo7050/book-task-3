from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", enable_decoding=False)

    app_name: str = "b-federation-security-lab"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "change-me"
    token_issuer: str = "b-federation-security-lab-local"
    token_algorithm: str = "HS256"

    database_url: str = "sqlite+pysqlite:///./b_federation_security_lab.db"
    redis_url: str | None = None

    access_token_ttl_seconds: int = 900
    pending_auth_ttl_seconds: int = 300
    refresh_token_ttl_seconds: int = 14 * 24 * 60 * 60

    secure_cookies: bool = False
    cookie_domain: str | None = None
    allowed_origins: list[str] = Field(default_factory=list)

    google_oidc_client_id: str = "google-client-id"
    google_oidc_client_secret: str = "google-client-secret"
    google_oidc_redirect_uri: str = "http://localhost:8000/api/v1/auth/google/callback"
    google_oidc_authorization_endpoint: str = "https://accounts.google.com/o/oauth2/v2/auth"
    google_oidc_token_endpoint: str = "https://oauth2.googleapis.com/token"
    google_oidc_userinfo_endpoint: str = "https://openidconnect.googleapis.com/v1/userinfo"
    google_oidc_jwks_uri: str = "https://www.googleapis.com/oauth2/v3/certs"
    google_oidc_issuer: str = "https://accounts.google.com"
    google_oidc_scopes: list[str] = Field(default_factory=lambda: ["openid", "email", "profile"])

    access_cookie_name: str = "access_token"
    refresh_cookie_name: str = "refresh_token"
    pending_auth_cookie_name: str = "pending_auth_token"
    csrf_cookie_name: str = "csrf_token"
    oauth_state_cookie_name: str = "oauth_state"
    csrf_header_name: str = "X-CSRF-Token"

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        if not value:
            return []
        return [origin.strip() for origin in value.split(",") if origin.strip()]

    @field_validator("google_oidc_scopes", mode="before")
    @classmethod
    def parse_scopes(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return [scope.strip() for scope in value.split(",") if scope.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
