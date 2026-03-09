from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Select, delete, select
from sqlalchemy.orm import Session

from app.db.models.auth import AuthAuditLog, RefreshToken, TwoFactorRecoveryCode


class AuthRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_refresh_token(self, token: RefreshToken) -> RefreshToken:
        self.session.add(token)
        self.session.flush()
        return token

    def get_refresh_token_by_hash(self, token_hash: str) -> RefreshToken | None:
        stmt: Select[tuple[RefreshToken]] = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def revoke_refresh_token(
        self, token: RefreshToken, *, revoked_at: datetime | None = None
    ) -> None:
        token.revoked_at = revoked_at or datetime.now(UTC)
        self.session.add(token)
        self.session.flush()

    def revoke_token_family(self, family_id: str, *, revoked_at: datetime | None = None) -> None:
        when = revoked_at or datetime.now(UTC)
        stmt = select(RefreshToken).where(
            RefreshToken.family_id == family_id,
            RefreshToken.revoked_at.is_(None),
        )
        for token in self.session.execute(stmt).scalars():
            token.revoked_at = when
        self.session.flush()

    def store_audit_event(
        self,
        *,
        event_type: str,
        user_id: str | None,
        details: dict[str, object] | None,
        ip_address: str | None,
        user_agent: str | None,
    ) -> AuthAuditLog:
        event = AuthAuditLog(
            user_id=user_id,
            event_type=event_type,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.add(event)
        self.session.flush()
        return event

    def replace_recovery_codes(self, *, user_id: str, code_hashes: list[str]) -> None:
        self.session.execute(
            delete(TwoFactorRecoveryCode).where(TwoFactorRecoveryCode.user_id == user_id)
        )
        now = datetime.now(UTC)
        for code_hash in code_hashes:
            self.session.add(
                TwoFactorRecoveryCode(
                    user_id=user_id,
                    code_hash=code_hash,
                    created_at=now,
                )
            )
        self.session.flush()

    def get_unused_recovery_code(
        self, *, user_id: str, code_hash: str
    ) -> TwoFactorRecoveryCode | None:
        stmt = select(TwoFactorRecoveryCode).where(
            TwoFactorRecoveryCode.user_id == user_id,
            TwoFactorRecoveryCode.code_hash == code_hash,
            TwoFactorRecoveryCode.used_at.is_(None),
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def mark_recovery_code_used(self, recovery_code: TwoFactorRecoveryCode) -> None:
        recovery_code.used_at = datetime.now(UTC)
        self.session.add(recovery_code)
        self.session.flush()
