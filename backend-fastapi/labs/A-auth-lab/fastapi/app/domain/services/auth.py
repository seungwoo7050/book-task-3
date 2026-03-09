from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.errors import AppError
from app.core.security import (
    build_access_token,
    hash_password,
    hash_secret,
    now_utc,
    verify_password,
)
from app.db.models.auth import RefreshToken
from app.db.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.repositories.user_repository import UserRepository


@dataclass
class SessionBundle:
    access_token: str
    refresh_token: str
    csrf_token: str


class AuthService:
    def __init__(self, session: Session, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.user_repository = UserRepository(session)
        self.auth_repository = AuthRepository(session)

    def register_user(
        self,
        *,
        email: str,
        handle: str,
        password: str,
        mailbox: list[dict[str, str]],
    ) -> User:
        normalized_email = email.strip().lower()
        if self.user_repository.get_by_email(normalized_email):
            raise AppError(
                code="EMAIL_ALREADY_REGISTERED",
                message="A user with that email already exists.",
                status_code=409,
            )
        if self.user_repository.get_by_handle(handle.strip().lower()):
            raise AppError(
                code="HANDLE_ALREADY_TAKEN",
                message="That handle is already taken.",
                status_code=409,
            )
        if len(password) < 8:
            raise AppError(
                code="PASSWORD_TOO_SHORT",
                message="Password must be at least 8 characters long.",
                status_code=400,
            )

        user = User(
            handle=self.user_repository.ensure_unique_handle(handle),
            email=normalized_email,
            password_hash=hash_password(password),
        )
        self.user_repository.save(user)
        token = self._issue_email_token(user_id=user.id, kind="verify_email")
        self._queue_email(mailbox=mailbox, to_email=user.email, kind="verify_email", token=token)
        self.auth_repository.store_audit_event(
            event_type="auth.registered",
            user_id=user.id,
            details={},
            ip_address=None,
            user_agent=None,
        )
        self.session.commit()
        self.session.refresh(user)
        return user

    def verify_email(self, *, raw_token: str) -> User:
        token = self.auth_repository.get_email_token_by_hash(
            kind="verify_email",
            token_hash=hash_secret(raw_token, self.settings),
        )
        if token is None or self._ensure_aware(token.expires_at) <= now_utc():
            raise AppError(
                code="INVALID_VERIFICATION_TOKEN",
                message="Verification token is invalid or expired.",
                status_code=400,
            )

        user = self.user_repository.get_by_id(token.user_id)
        if user is None:
            raise AppError(code="USER_NOT_FOUND", message="User not found.", status_code=404)

        user.email_verified_at = now_utc()
        self.auth_repository.mark_email_token_used(token)
        self.auth_repository.store_audit_event(
            event_type="auth.email_verified",
            user_id=user.id,
            details={},
            ip_address=None,
            user_agent=None,
        )
        self.session.commit()
        self.session.refresh(user)
        return user

    def authenticate_user(self, *, email: str, password: str) -> User:
        user = self.user_repository.get_by_email(email.strip().lower())
        if user is None or not verify_password(user.password_hash, password):
            raise AppError(
                code="INVALID_CREDENTIALS",
                message="Email or password is incorrect.",
                status_code=401,
            )
        if user.email_verified_at is None:
            raise AppError(
                code="EMAIL_NOT_VERIFIED",
                message="Verify the email address before signing in.",
                status_code=403,
            )
        return user

    def request_password_reset(
        self,
        *,
        email: str,
        mailbox: list[dict[str, str]],
    ) -> None:
        user = self.user_repository.get_by_email(email.strip().lower())
        if user is None:
            return
        token = self._issue_email_token(user_id=user.id, kind="password_reset")
        self._queue_email(
            mailbox=mailbox,
            to_email=user.email,
            kind="password_reset",
            token=token,
        )
        self.auth_repository.store_audit_event(
            event_type="auth.password_reset.requested",
            user_id=user.id,
            details={},
            ip_address=None,
            user_agent=None,
        )
        self.session.commit()

    def reset_password(self, *, raw_token: str, new_password: str) -> None:
        if len(new_password) < 8:
            raise AppError(
                code="PASSWORD_TOO_SHORT",
                message="Password must be at least 8 characters long.",
                status_code=400,
            )
        token = self.auth_repository.get_email_token_by_hash(
            kind="password_reset",
            token_hash=hash_secret(raw_token, self.settings),
        )
        if token is None or self._ensure_aware(token.expires_at) <= now_utc():
            raise AppError(
                code="INVALID_PASSWORD_RESET_TOKEN",
                message="Password reset token is invalid or expired.",
                status_code=400,
            )

        user = self.user_repository.get_by_id(token.user_id)
        if user is None:
            raise AppError(code="USER_NOT_FOUND", message="User not found.", status_code=404)

        user.password_hash = hash_password(new_password)
        self.auth_repository.mark_email_token_used(token)
        self.auth_repository.store_audit_event(
            event_type="auth.password_reset.completed",
            user_id=user.id,
            details={},
            ip_address=None,
            user_agent=None,
        )
        self.session.commit()

    def issue_session(
        self,
        *,
        user: User,
        ip_address: str | None,
        user_agent: str | None,
        family_id: str | None = None,
        parent_token_id: str | None = None,
        audit_event_type: str | None = None,
    ) -> SessionBundle:
        refresh_token = self._issue_refresh_token(
            user=user,
            family_id=family_id or str(uuid4()),
            parent_token_id=parent_token_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        access_token = build_access_token(user.id, user.handle, self.settings)
        csrf_token = self._issue_csrf_token(user=user)
        if audit_event_type:
            self.auth_repository.store_audit_event(
                event_type=audit_event_type,
                user_id=user.id,
                details={},
                ip_address=ip_address,
                user_agent=user_agent,
            )
        self.session.commit()
        return SessionBundle(
            access_token=access_token,
            refresh_token=refresh_token,
            csrf_token=csrf_token,
        )

    def rotate_refresh_token(
        self,
        *,
        raw_refresh_token: str,
        ip_address: str | None,
        user_agent: str | None,
    ) -> tuple[User, SessionBundle]:
        token_hash = hash_secret(raw_refresh_token, self.settings)
        token = self.auth_repository.get_refresh_token_by_hash(token_hash)
        if token is None:
            raise AppError(
                code="INVALID_REFRESH_TOKEN",
                message="Refresh token is unknown.",
                status_code=401,
            )
        if self._ensure_aware(token.expires_at) <= now_utc():
            self.auth_repository.revoke_refresh_token(token)
            self.session.commit()
            raise AppError(
                code="EXPIRED_REFRESH_TOKEN",
                message="Refresh token is expired.",
                status_code=401,
            )
        if token.revoked_at is not None:
            if token.reuse_detected_at is None:
                token.reuse_detected_at = now_utc()
            self.auth_repository.revoke_token_family(token.family_id, revoked_at=now_utc())
            self.auth_repository.store_audit_event(
                event_type="auth.refresh.reuse_detected",
                user_id=token.user_id,
                details={"family_id": token.family_id},
                ip_address=ip_address,
                user_agent=user_agent,
            )
            self.session.commit()
            raise AppError(
                code="REFRESH_TOKEN_REUSED",
                message="Refresh token reuse was detected. The whole session family was revoked.",
                status_code=401,
            )

        user = self.user_repository.get_by_id(token.user_id)
        if user is None or not user.is_active:
            raise AppError(
                code="USER_NOT_FOUND",
                message="User for the refresh token no longer exists.",
                status_code=404,
            )

        self.auth_repository.revoke_refresh_token(token)
        bundle = self.issue_session(
            user=user,
            family_id=token.family_id,
            parent_token_id=token.id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.auth_repository.store_audit_event(
            event_type="auth.refresh.rotated",
            user_id=user.id,
            details={"family_id": token.family_id},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.commit()
        return user, bundle

    def revoke_refresh_token(
        self,
        *,
        raw_refresh_token: str | None,
        ip_address: str | None,
        user_agent: str | None,
    ) -> None:
        if not raw_refresh_token:
            return
        token_hash = hash_secret(raw_refresh_token, self.settings)
        token = self.auth_repository.get_refresh_token_by_hash(token_hash)
        if token is None:
            return
        self.auth_repository.revoke_refresh_token(token)
        self.auth_repository.store_audit_event(
            event_type="auth.logout",
            user_id=token.user_id,
            details={"family_id": token.family_id},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.commit()

    def _issue_email_token(self, *, user_id: str, kind: str) -> str:
        raw_token = f"{uuid4()}-{uuid4()}"
        ttl = (
            self.settings.verification_token_ttl_seconds
            if kind == "verify_email"
            else self.settings.password_reset_ttl_seconds
        )
        self.auth_repository.replace_email_token(
            user_id=user_id,
            kind=kind,
            token_hash=hash_secret(raw_token, self.settings),
            expires_at=now_utc() + timedelta(seconds=ttl),
        )
        return raw_token

    @staticmethod
    def _queue_email(
        *,
        mailbox: list[dict[str, str]],
        to_email: str,
        kind: str,
        token: str,
    ) -> None:
        mailbox.append({"to": to_email, "kind": kind, "token": token})

    def _issue_csrf_token(self, *, user: User) -> str:
        return hash_secret(f"{user.id}:{uuid4()}", self.settings)

    def _issue_refresh_token(
        self,
        *,
        user: User,
        family_id: str,
        parent_token_id: str | None,
        ip_address: str | None,
        user_agent: str | None,
    ) -> str:
        raw_token = f"{uuid4()}-{uuid4()}"
        expires_at = now_utc() + timedelta(seconds=self.settings.refresh_token_ttl_seconds)
        token = RefreshToken(
            user_id=user.id,
            family_id=family_id,
            parent_token_id=parent_token_id,
            token_hash=hash_secret(raw_token, self.settings),
            issued_at=now_utc(),
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.auth_repository.create_refresh_token(token)
        return raw_token

    @staticmethod
    def _ensure_aware(value):
        if value.tzinfo is None:
            return value.replace(tzinfo=now_utc().tzinfo)
        return value
