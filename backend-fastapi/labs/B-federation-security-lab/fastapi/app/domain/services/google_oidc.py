from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlencode

import httpx
import jwt

from app.core.config import Settings
from app.core.errors import AppError
from app.core.security import build_pkce_challenge, generate_pkce_verifier, generate_random_token


@dataclass
class GoogleAuthorizationRequest:
    authorization_url: str
    state: str
    nonce: str
    code_verifier: str


class GoogleOIDCService:
    provider_name = "google"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def build_authorization_request(self) -> GoogleAuthorizationRequest:
        state = generate_random_token()
        nonce = generate_random_token()
        code_verifier = generate_pkce_verifier()
        params = {
            "client_id": self.settings.google_oidc_client_id,
            "redirect_uri": self.settings.google_oidc_redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.settings.google_oidc_scopes),
            "state": state,
            "nonce": nonce,
            "code_challenge": build_pkce_challenge(code_verifier),
            "code_challenge_method": "S256",
            "access_type": "offline",
            "prompt": "consent",
        }
        return GoogleAuthorizationRequest(
            authorization_url=f"{self.settings.google_oidc_authorization_endpoint}?{urlencode(params)}",
            state=state,
            nonce=nonce,
            code_verifier=code_verifier,
        )

    def exchange_code_for_tokens(self, code: str, code_verifier: str) -> dict[str, object]:
        try:
            response = httpx.post(
                self.settings.google_oidc_token_endpoint,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": self.settings.google_oidc_client_id,
                    "client_secret": self.settings.google_oidc_client_secret,
                    "redirect_uri": self.settings.google_oidc_redirect_uri,
                    "code_verifier": code_verifier,
                },
                timeout=10,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise AppError(
                code="OIDC_TOKEN_EXCHANGE_FAILED",
                message="Could not exchange the authorization code with Google.",
                status_code=502,
            ) from exc
        return response.json()

    def validate_id_token(self, id_token: str, nonce: str) -> dict[str, object]:
        try:
            jwk_client = jwt.PyJWKClient(self.settings.google_oidc_jwks_uri)
            signing_key = jwk_client.get_signing_key_from_jwt(id_token)
            payload = jwt.decode(
                id_token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.settings.google_oidc_client_id,
                issuer=self.settings.google_oidc_issuer,
            )
        except jwt.PyJWTError as exc:
            raise AppError(
                code="OIDC_ID_TOKEN_INVALID",
                message="Google ID token validation failed.",
                status_code=401,
            ) from exc

        if payload.get("nonce") != nonce:
            raise AppError(
                code="OIDC_NONCE_MISMATCH",
                message="Google ID token nonce did not match the expected value.",
                status_code=401,
            )
        return payload

    def fetch_userinfo(self, access_token: str) -> dict[str, object]:
        try:
            response = httpx.get(
                self.settings.google_oidc_userinfo_endpoint,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise AppError(
                code="OIDC_USERINFO_FAILED",
                message="Could not load Google user information.",
                status_code=502,
            ) from exc
        return response.json()
