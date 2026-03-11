from __future__ import annotations

from pathlib import Path

from core.config import load_settings
from db.models import AdminUser, ConversationBatch
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from services.importers import (
    ImportValidationError,
    ensure_storage_dirs,
    import_transcript_jsonl,
    persist_bytes,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.dependencies import get_current_admin, get_session

router = APIRouter(prefix="/api/datasets", tags=["datasets"])


@router.get("")
def list_datasets(
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    rows = list(session.scalars(select(ConversationBatch).order_by(ConversationBatch.created_at.desc())).all())
    return {
        "items": [
            {
                "id": row.id,
                "name": row.name,
                "source_filename": row.source_filename,
                "record_count": row.record_count,
                "is_sample": row.is_sample,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]
    }


@router.post("/import")
async def import_dataset(
    file: UploadFile = File(...),
    name: str | None = Form(None),
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="file is required")
    if not file.filename.lower().endswith(".jsonl"):
        raise HTTPException(status_code=400, detail="dataset import only accepts .jsonl files")

    settings = load_settings()
    storage_root = ensure_storage_dirs(settings)
    payload = await file.read()
    stored_path = persist_bytes(root=storage_root, subdir="datasets", filename=file.filename, content=payload)

    try:
        batch = import_transcript_jsonl(
            session,
            path=Path(stored_path),
            display_name=name or Path(file.filename).stem,
            source_filename=file.filename,
            source_path=str(stored_path),
            is_sample=False,
        )
        session.commit()
    except ImportValidationError as exc:
        session.rollback()
        raise HTTPException(status_code=422, detail={"errors": exc.errors}) from exc

    return {"dataset_id": batch.id, "record_count": batch.record_count, "warnings": []}
