from __future__ import annotations

from pathlib import Path

from core.config import load_settings
from core.json_utils import loads_json
from db.models import AdminUser, KnowledgeBaseBundle
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from services.importers import (
    ImportValidationError,
    ensure_storage_dirs,
    import_markdown_zip,
    persist_bytes,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.dependencies import get_current_admin, get_session

router = APIRouter(prefix="/api/kb-bundles", tags=["knowledge-base"])


@router.get("")
def list_kb_bundles(
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    rows = list(session.scalars(select(KnowledgeBaseBundle).order_by(KnowledgeBaseBundle.created_at.desc())).all())
    return {
        "items": [
            {
                "id": row.id,
                "name": row.name,
                "source_filename": row.source_filename,
                "doc_count": row.doc_count,
                "categories": loads_json(row.categories_json, []),
                "is_sample": row.is_sample,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]
    }


@router.post("/import")
async def import_kb_bundle(
    file: UploadFile = File(...),
    name: str | None = Form(None),
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="file is required")
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="knowledge base import only accepts .zip files")

    settings = load_settings()
    storage_root = ensure_storage_dirs(settings)
    payload = await file.read()
    stored_path = persist_bytes(root=storage_root, subdir="kb-bundles", filename=file.filename, content=payload)

    try:
        bundle = import_markdown_zip(
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

    return {
        "kb_bundle_id": bundle.id,
        "doc_count": bundle.doc_count,
        "derived_categories": loads_json(bundle.categories_json, []),
    }
