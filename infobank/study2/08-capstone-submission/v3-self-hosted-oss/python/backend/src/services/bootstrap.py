from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from core.auth import hash_password
from core.config import Settings
from db.models import AdminUser, ConversationBatch, KnowledgeBaseBundle
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.importers import (
    ensure_storage_dirs,
    import_markdown_directory,
    import_transcript_jsonl,
)


def bootstrap_admin_user(session: Session, settings: Settings) -> AdminUser:
    admin = session.scalar(select(AdminUser).order_by(AdminUser.created_at.asc()).limit(1))
    if admin is None:
        admin = AdminUser(
            id="admin-user",
            email=settings.admin_email,
            password_hash=hash_password(settings.admin_password),
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        session.add(admin)
        session.flush()
        return admin

    if admin.email != settings.admin_email:
        admin.email = settings.admin_email
    admin.password_hash = hash_password(settings.admin_password)
    admin.updated_at = datetime.now(UTC)
    session.flush()
    return admin


def bootstrap_sample_assets(session: Session, settings: Settings) -> None:
    ensure_storage_dirs(settings)

    sample_batch = session.scalar(
        select(ConversationBatch).where(ConversationBatch.is_sample.is_(True)).limit(1)
    )
    if sample_batch is None:
        sample_path = Path("backend/data/sample_transcripts/sample_dataset.jsonl")
        import_transcript_jsonl(
            session,
            path=sample_path,
            display_name="sample-transcripts",
            source_filename=sample_path.name,
            source_path=str(sample_path),
            is_sample=True,
        )

    sample_bundle = session.scalar(
        select(KnowledgeBaseBundle).where(KnowledgeBaseBundle.is_sample.is_(True)).limit(1)
    )
    if sample_bundle is None:
        import_markdown_directory(
            session,
            root=Path("backend/knowledge_base"),
            display_name="sample-knowledge-base",
            is_sample=True,
        )

    session.flush()
