from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.errors import AppError
from app.core.security import (
    build_access_token,
    build_pending_auth_token,
    hash_secret,
    now_utc,
)
from app.db.models.auth import RefreshToken
from app.db.models.user import User
from app.domain.services.two_factor import TwoFactorService
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
        self.two_factor_service = TwoFactorService()

    def sync_google_user(self, *, profile: dict[str, object]) -> User:
        subject = str(profile["sub"])
        email = str(profile["email"])
        email_verified = bool(profile.get("email_verified", False))
        display_name = str(profile.get("name") or email.split("@")[0])
        avatar_url = str(profile.get("picture")) if profile.get("picture") else None

        user = self.user_repository.get_by_external_identity("google", subject)
        if user is None:
            if email_verified:
                user = self.user_repository.get_by_email(email)
            if user is None:
                handle_seed = str(profile.get("preferred_username") or email.split("@")[0])
                user = User(
                    handle=self.user_repository.ensure_unique_handle(handle_seed),
                    email=email,
                    display_name=display_name,
                    avatar_url=avatar_url,
                )
                self.user_repository.save(user)

        user.email = email
        user.display_name = display_name
        user.avatar_url = avatar_url
        self.user_repository.save(user)
        self.user_repository.link_external_identity(
            user=user,
            provider="google",
            subject=subject,
            provider_email=email,
            email_verified=email_verified,
            profile=profile,
        )
        self.session.commit()
        self.session.refresh(user)
        return user

    def start_pending_second_factor(
        self,
        *,
        user: User,
        ip_address: str | None,
        user_agent: str | None,
    ) -> str:
        self.auth_repository.store_audit_event(
            event_type="auth.login.challenge_required",
            user_id=user.id,
            details={"provider": "google"},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.commit()
        return build_pending_auth_token(user.id, self.settings)

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
            access_token=access_token, refresh_token=refresh_token, csrf_token=csrf_token
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
            self.auth_repository.store_audit_event(
                event_type="auth.refresh.expired",
                user_id=token.user_id,
                details={"family_id": token.family_id},
                ip_address=ip_address,
                user_agent=user_agent,
            )
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

    def begin_two_factor_setup(self, user: User) -> tuple[str, str]:
        if user.two_factor_enabled:
            raise AppError(
                code="TWO_FACTOR_ALREADY_ENABLED",
                message="Two-factor authentication is already enabled.",
                status_code=409,
            )
        secret, provisioning_uri = self.two_factor_service.build_setup_material(
            email=user.email,
            issuer_name=self.settings.app_name,
        )
        user.pending_two_factor_secret = secret
        self.user_repository.save(user)
        self.session.commit()
        return secret, provisioning_uri

    def confirm_two_factor_setup(
        self,
        *,
        user: User,
        code: str,
        ip_address: str | None,
        user_agent: str | None,
    ) -> list[str]:
        pending_secret = user.pending_two_factor_secret
        if not pending_secret:
            raise AppError(
                code="TWO_FACTOR_NOT_PENDING",
                message="Two-factor setup has not been started.",
                status_code=400,
            )
        if not self.two_factor_service.verify_totp(secret=pending_secret, code=code):
            raise AppError(
                code="INVALID_TWO_FACTOR_CODE",
                message="The TOTP code is invalid.",
                status_code=401,
            )

        user.two_factor_secret = pending_secret
        user.pending_two_factor_secret = None
        user.two_factor_enabled = True
        recovery_codes = self.two_factor_service.generate_recovery_codes()
        self.auth_repository.replace_recovery_codes(
            user_id=user.id,
            code_hashes=[hash_secret(code_value, self.settings) for code_value in recovery_codes],
        )
        self.auth_repository.store_audit_event(
            event_type="auth.2fa.enabled",
            user_id=user.id,
            details={},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.commit()
        return recovery_codes

    def verify_two_factor_challenge(
        self,
        *,
        user: User,
        code: str | None,
        recovery_code: str | None,
        ip_address: str | None,
        user_agent: str | None,
    ) -> None:
        if not user.two_factor_enabled or not user.two_factor_secret:
            raise AppError(
                code="TWO_FACTOR_NOT_ENABLED",
                message="Two-factor authentication is not enabled for this user.",
                status_code=400,
            )

        if code:
            if not self.two_factor_service.verify_totp(secret=user.two_factor_secret, code=code):
                raise AppError(
                    code="INVALID_TWO_FACTOR_CODE",
                    message="The TOTP code is invalid.",
                    status_code=401,
                )
        elif recovery_code:
            recovery = self.auth_repository.get_unused_recovery_code(
                user_id=user.id,
                code_hash=hash_secret(recovery_code, self.settings),
            )
            if recovery is None:
                raise AppError(
                    code="INVALID_RECOVERY_CODE",
                    message="The recovery code is invalid or already used.",
                    status_code=401,
                )
            self.auth_repository.mark_recovery_code_used(recovery)
        else:
            raise AppError(
                code="MISSING_TWO_FACTOR_PROOF",
                message="Provide either a TOTP code or a recovery code.",
                status_code=400,
            )

        self.auth_repository.store_audit_event(
            event_type="auth.2fa.verified",
            user_id=user.id,
            details={},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.commit()

    def regenerate_recovery_codes(
        self,
        *,
        user: User,
        code: str | None,
        recovery_code: str | None,
        ip_address: str | None,
        user_agent: str | None,
    ) -> list[str]:
        self.verify_two_factor_challenge(
            user=user,
            code=code,
            recovery_code=recovery_code,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        recovery_codes = self.two_factor_service.generate_recovery_codes()
        self.auth_repository.replace_recovery_codes(
            user_id=user.id,
            code_hashes=[hash_secret(code_value, self.settings) for code_value in recovery_codes],
        )
        self.auth_repository.store_audit_event(
            event_type="auth.2fa.recovery_codes_regenerated",
            user_id=user.id,
            details={},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.commit()
        return recovery_codes

    def disable_two_factor(
        self,
        *,
        user: User,
        code: str | None,
        recovery_code: str | None,
        ip_address: str | None,
        user_agent: str | None,
    ) -> None:
        self.verify_two_factor_challenge(
            user=user,
            code=code,
            recovery_code=recovery_code,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        user.two_factor_secret = None
        user.pending_two_factor_secret = None
        user.two_factor_enabled = False
        self.auth_repository.replace_recovery_codes(user_id=user.id, code_hashes=[])
        self.auth_repository.store_audit_event(
            event_type="auth.2fa.disabled",
            user_id=user.id,
            details={},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.commit()

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
