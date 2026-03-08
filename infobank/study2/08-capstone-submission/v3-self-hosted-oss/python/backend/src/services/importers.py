from __future__ import annotations

import json
import uuid
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

from core.config import Settings
from core.json_utils import dumps_json
from db.models import Conversation, ConversationBatch, KnowledgeBaseBundle, KnowledgeDoc, Turn
from db.seed import DOC_METADATA_HINTS
from sqlalchemy.orm import Session


class ImportValidationError(ValueError):
    def __init__(self, errors: list[dict[str, object]]):
        super().__init__("import validation failed")
        self.errors = errors


@dataclass(frozen=True)
class TranscriptRecord:
    conversation_external_id: str
    turn_index: int
    user_message: str
    assistant_response: str
    timestamp: str | None
    tags: list[str]
    metadata: dict[str, Any]


def _utc_now() -> datetime:
    return datetime.now(UTC)


def ensure_storage_dirs(settings: Settings) -> Path:
    root = Path(settings.storage_root)
    (root / "datasets").mkdir(parents=True, exist_ok=True)
    (root / "kb-bundles").mkdir(parents=True, exist_ok=True)
    return root


def persist_bytes(*, root: Path, subdir: str, filename: str, content: bytes) -> Path:
    target = root / subdir / f"{uuid.uuid4()}__{filename}"
    target.write_bytes(content)
    return target


def persist_text(*, root: Path, subdir: str, filename: str, content: str) -> Path:
    target = root / subdir / f"{uuid.uuid4()}__{filename}"
    target.write_text(content, encoding="utf-8")
    return target


def _validate_transcript_line(line_number: int, item: dict[str, Any]) -> TranscriptRecord:
    required_fields = (
        "conversation_external_id",
        "turn_index",
        "user_message",
        "assistant_response",
    )
    missing = [field for field in required_fields if field not in item or item[field] in {None, ""}]
    if missing:
        raise ImportValidationError(
            [{"line": line_number, "message": f"missing required fields: {', '.join(missing)}"}]
        )

    tags_raw = item.get("tags", [])
    metadata_raw = item.get("metadata", {})
    if tags_raw is None:
        tags_raw = []
    if metadata_raw is None:
        metadata_raw = {}
    if not isinstance(tags_raw, list):
        raise ImportValidationError([{"line": line_number, "message": "tags must be a list"}])
    if not isinstance(metadata_raw, dict):
        raise ImportValidationError([{"line": line_number, "message": "metadata must be an object"}])

    try:
        turn_index = int(item["turn_index"])
    except (TypeError, ValueError) as exc:
        raise ImportValidationError([{"line": line_number, "message": "turn_index must be an integer"}]) from exc

    return TranscriptRecord(
        conversation_external_id=str(item["conversation_external_id"]).strip(),
        turn_index=turn_index,
        user_message=str(item["user_message"]).strip(),
        assistant_response=str(item["assistant_response"]).strip(),
        timestamp=str(item["timestamp"]).strip() if item.get("timestamp") else None,
        tags=[str(tag) for tag in tags_raw],
        metadata={str(key): value for key, value in metadata_raw.items()},
    )


def parse_transcript_jsonl(path: Path) -> list[TranscriptRecord]:
    errors: list[dict[str, object]] = []
    records: list[TranscriptRecord] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append({"line": line_number, "message": f"invalid json: {exc.msg}"})
            continue
        if not isinstance(payload, dict):
            errors.append({"line": line_number, "message": "each line must be a JSON object"})
            continue
        try:
            records.append(_validate_transcript_line(line_number, payload))
        except ImportValidationError as exc:
            errors.extend(exc.errors)

    if errors:
        raise ImportValidationError(errors)
    if not records:
        raise ImportValidationError([{"line": 0, "message": "JSONL file did not contain any transcript records"}])
    return records


def import_transcript_jsonl(
    session: Session,
    *,
    path: Path,
    display_name: str,
    source_filename: str,
    source_path: str,
    is_sample: bool = False,
) -> ConversationBatch:
    records = parse_transcript_jsonl(path)
    batch = ConversationBatch(
        id=str(uuid.uuid4()),
        name=display_name,
        source_filename=source_filename,
        source_path=source_path,
        record_count=len(records),
        metadata_json=dumps_json({"import_format": "jsonl", "conversation_count": len({item.conversation_external_id for item in records})}),
        is_sample=is_sample,
        created_at=_utc_now(),
    )
    session.add(batch)
    session.flush()

    conversations: dict[str, Conversation] = {}
    ordered = sorted(records, key=lambda item: (item.conversation_external_id, item.turn_index))
    for record in ordered:
        conversation = conversations.get(record.conversation_external_id)
        if conversation is None:
            conversation = Conversation(
                id=str(uuid.uuid4()),
                batch_id=batch.id,
                external_id=record.conversation_external_id,
                metadata_json=dumps_json({"import_source": batch.source_filename}),
                prompt_version="imported-transcript",
                kb_version="uploaded-kb",
                created_at=_utc_now(),
            )
            session.add(conversation)
            session.flush()
            conversations[record.conversation_external_id] = conversation

        session.add(
            Turn(
                id=str(uuid.uuid4()),
                conversation_id=conversation.id,
                turn_index=record.turn_index,
                user_message=record.user_message,
                assistant_response=record.assistant_response,
                retrieved_doc_ids="[]",
                tags_json=dumps_json(record.tags),
                metadata_json=dumps_json(record.metadata),
                source_timestamp=record.timestamp,
                latency_ms=0,
                created_at=_utc_now(),
            )
        )

    session.flush()
    return batch


def _normalize_doc_id(bundle_id: str, relative_path: PurePosixPath, *, preserve_legacy_ids: bool) -> str:
    rel = str(relative_path).replace("/", "__")
    if preserve_legacy_ids:
        return rel
    return f"{bundle_id}::{rel}"


def _doc_descriptor_from_path(relative_path: PurePosixPath) -> tuple[str, str]:
    parts = relative_path.parts
    category = parts[1] if len(parts) > 2 and parts[0] == "docs" else (parts[0] if len(parts) > 1 else "general")
    title = relative_path.stem.replace("_", " ")
    return title, category


def _manifest_docs(raw_manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    docs = raw_manifest.get("docs", {})
    if not isinstance(docs, dict):
        return {}
    normalized: dict[str, dict[str, Any]] = {}
    for path, metadata in docs.items():
        if isinstance(metadata, dict):
            normalized[str(path)] = metadata
    return normalized


def import_markdown_zip(
    session: Session,
    *,
    path: Path,
    display_name: str,
    source_filename: str,
    source_path: str,
    is_sample: bool = False,
) -> KnowledgeBaseBundle:
    manifest_docs: dict[str, dict[str, Any]] = {}
    doc_entries: list[tuple[PurePosixPath, str]] = []

    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            archive_path = PurePosixPath(info.filename)
            if info.is_dir():
                continue
            if archive_path.name == "manifest.json":
                raw_manifest = json.loads(archive.read(info.filename).decode("utf-8"))
                if isinstance(raw_manifest, dict):
                    manifest_docs = _manifest_docs(raw_manifest)
                continue
            if archive_path.suffix.lower() != ".md":
                continue
            if archive_path.parts[:1] != ("docs",):
                continue
            doc_entries.append((archive_path, archive.read(info.filename).decode("utf-8").strip()))

    if not doc_entries:
        raise ImportValidationError([{"line": 0, "message": "zip must contain docs/**/*.md files"}])

    bundle = KnowledgeBaseBundle(
        id=str(uuid.uuid4()),
        name=display_name,
        source_filename=source_filename,
        source_path=source_path,
        doc_count=len(doc_entries),
        categories_json="[]",
        metadata_json=dumps_json({"import_format": "markdown-zip"}),
        is_sample=is_sample,
        created_at=_utc_now(),
    )
    session.add(bundle)
    session.flush()

    categories: set[str] = set()
    for relative_path, content in sorted(doc_entries, key=lambda item: str(item[0])):
        title, derived_category = _doc_descriptor_from_path(relative_path)
        metadata = manifest_docs.get(str(relative_path), {})
        category = str(metadata.get("category", derived_category))
        categories.add(category)
        doc_id = _normalize_doc_id(bundle.id, relative_path.relative_to("docs"), preserve_legacy_ids=is_sample)
        merged_metadata: dict[str, Any] = {
            "source": str(relative_path),
            "aliases": metadata.get("aliases", []),
            "keywords": metadata.get("keywords", []),
            "risk_tags": metadata.get("risk_tags", []),
        }
        merged_metadata.update(DOC_METADATA_HINTS.get(doc_id, {}))
        session.add(
            KnowledgeDoc(
                id=doc_id,
                bundle_id=bundle.id,
                title=str(metadata.get("title", title)),
                category=category,
                content=content,
                metadata_json=dumps_json(merged_metadata),
                created_at=_utc_now(),
            )
        )

    bundle.categories_json = dumps_json(sorted(categories))
    session.flush()
    return bundle


def import_markdown_directory(
    session: Session,
    *,
    root: Path,
    display_name: str,
    is_sample: bool = False,
) -> KnowledgeBaseBundle:
    bundle = KnowledgeBaseBundle(
        id=str(uuid.uuid4()),
        name=display_name,
        source_filename=root.name,
        source_path=str(root),
        doc_count=0,
        categories_json="[]",
        metadata_json=dumps_json({"import_format": "markdown-directory"}),
        is_sample=is_sample,
        created_at=_utc_now(),
    )
    session.add(bundle)
    session.flush()

    categories: set[str] = set()
    count = 0
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        doc_id = _normalize_doc_id(bundle.id, PurePosixPath(rel.as_posix()), preserve_legacy_ids=is_sample)
        category = rel.parts[0] if len(rel.parts) > 1 else "general"
        title = path.stem.replace("_", " ")
        categories.add(category)
        metadata: dict[str, Any] = {"source": str(rel)}
        metadata.update(DOC_METADATA_HINTS.get(doc_id, {}))
        session.add(
            KnowledgeDoc(
                id=doc_id,
                bundle_id=bundle.id,
                title=title,
                category=category,
                content=path.read_text(encoding="utf-8").strip(),
                metadata_json=dumps_json(metadata),
                created_at=_utc_now(),
            )
        )
        count += 1

    if count == 0:
        raise ImportValidationError([{"line": 0, "message": "knowledge base directory did not contain markdown files"}])
    bundle.doc_count = count
    bundle.categories_json = dumps_json(sorted(categories))
    session.flush()
    return bundle
