from __future__ import annotations

from datetime import timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.errors import AppError
from app.core.security import build_access_token, generate_csrf_token, hash_password, hash_secret, now_utc, verify_password
from app.db.models.auth import ExternalIdentity, RefreshToken, User
from app.repositories.auth_repository import AuthRepository


class AuthService:
    def __init__(self, session: Session, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.repository = AuthRepository(session)

    def register(self, *, handle: str, email: str, password: str, mailbox: list[dict[str, str]]) -> User:
        if self.repository.get_user_by_email(email.lower()):
            raise AppError(code="EMAIL_ALREADY_REGISTERED", message="Email already registered.", status_code=409)
        user = User(
            handle=handle.lower(),
            email=email.lower(),
            password_hash=hash_password(password),
            display_name=handle,
        )
        self.repository.save(user)
        raw_token = f"{uuid4()}-{uuid4()}"
        self.repository.replace_email_token(
            user_id=user.id,
            kind="verify_email",
            token_hash=hash_secret(raw_token, self.settings),
            expires_at=now_utc() + timedelta(seconds=self.settings.verification_token_ttl_seconds),
        )
        mailbox.append({"kind": "verify_email", "email": user.email, "token": raw_token})
        self.session.commit()
        self.session.refresh(user)
        return user

    def verify_email(self, *, raw_token: str) -> None:
        token = self.repository.get_email_token(kind="verify_email", token_hash=hash_secret(raw_token, self.settings))
        if token is None:
            raise AppError(code="INVALID_VERIFICATION_TOKEN", message="Invalid verification token.", status_code=400)
        user = self.repository.get_user(token.user_id)
        if user is None:
            raise AppError(code="USER_NOT_FOUND", message="User not found.", status_code=404)
        user.email_verified_at = now_utc()
        token.used_at = now_utc()
        self.session.commit()

    def login_local(self, *, email: str, password: str) -> User:
        user = self.repository.get_user_by_email(email.lower())
        if user is None or user.password_hash is None or not verify_password(user.password_hash, password):
            raise AppError(code="INVALID_CREDENTIALS", message="Invalid credentials.", status_code=401)
        if user.email_verified_at is None:
            raise AppError(code="EMAIL_NOT_VERIFIED", message="Email not verified.", status_code=403)
        return user

    def login_google(self, *, subject: str, email: str, display_name: str) -> User:
        user = self.repository.get_user_by_identity("google", subject)
        if user is None:
            user = self.repository.get_user_by_email(email.lower())
        if user is None:
            user = User(
                handle=email.split("@")[0].lower(),
                email=email.lower(),
                password_hash=None,
                display_name=display_name,
                email_verified_at=now_utc(),
            )
            self.repository.save(user)
        if user.email_verified_at is None:
            user.email_verified_at = now_utc()
        self.repository.save(
            ExternalIdentity(
                user_id=user.id,
                provider="google",
                provider_subject=subject,
                provider_email=email.lower(),
            )
        )
        self.session.commit()
        self.session.refresh(user)
        return user

    def issue_session(self, *, user: User, family_id: str | None = None, parent_token_id: str | None = None) -> tuple[str, str, str]:
        raw_refresh = f"{uuid4()}-{uuid4()}"
        token = RefreshToken(
            user_id=user.id,
            family_id=family_id or str(uuid4()),
            parent_token_id=parent_token_id,
            token_hash=hash_secret(raw_refresh, self.settings),
            issued_at=now_utc(),
            expires_at=now_utc() + timedelta(seconds=self.settings.refresh_token_ttl_seconds),
        )
        self.repository.create_refresh_token(token)
        self.session.commit()
        return (
            build_access_token(user.id, user.handle, user.email, user.display_name, self.settings),
            raw_refresh,
            generate_csrf_token(),
        )

    def rotate_refresh(self, *, raw_token: str) -> tuple[User, tuple[str, str, str]]:
        token = self.repository.get_refresh_token(hash_secret(raw_token, self.settings))
        if token is None:
            raise AppError(code="INVALID_REFRESH_TOKEN", message="Unknown refresh token.", status_code=401)
        if token.revoked_at is not None:
            self.repository.revoke_token_family(token.family_id)
            self.session.commit()
            raise AppError(code="REFRESH_TOKEN_REUSED", message="Refresh token reuse detected.", status_code=401)
        token.revoked_at = now_utc()
        user = self.repository.get_user(token.user_id)
        if user is None:
            raise AppError(code="USER_NOT_FOUND", message="User not found.", status_code=404)
        return user, self.issue_session(user=user, family_id=token.family_id, parent_token_id=token.id)

    def revoke_refresh(self, *, raw_token: str | None) -> None:
        if not raw_token:
            return
        token = self.repository.get_refresh_token(hash_secret(raw_token, self.settings))
        if token:
            token.revoked_at = now_utc()
            self.session.commit()
