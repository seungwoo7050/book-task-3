from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from core.json_utils import dumps_json
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import GoldenSet, KnowledgeDoc


def seed_knowledge_base(session: Session, root: Path) -> int:
    inserted = 0
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        doc_id = str(rel).replace("/", "__")
        title = path.stem
        category = rel.parts[0] if len(rel.parts) > 1 else "general"
        content = path.read_text(encoding="utf-8").strip()
        metadata = {"source": str(rel)}

        existing = session.get(KnowledgeDoc, doc_id)
        if existing is None:
            session.add(
                KnowledgeDoc(
                    id=doc_id,
                    title=title,
                    category=category,
                    content=content,
                    metadata_json=dumps_json(metadata),
                )
            )
            inserted += 1
        else:
            existing.title = title
            existing.category = category
            existing.content = content
            existing.metadata_json = dumps_json(metadata)

    return inserted



def seed_golden_set(session: Session, yaml_path: Path) -> int:
    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    cases: list[dict[str, Any]] = raw.get("cases", [])
    inserted = 0

    for item in cases:
        case_id = str(item["id"])
        existing = session.get(GoldenSet, case_id)
        payload = {
            "expected_failure_types": item.get("expected_failure_types", []),
            "required_evidence_doc_ids": item.get("required_evidence_doc_ids", []),
        }
        tags = item.get("tags", [])

        if existing is None:
            session.add(
                GoldenSet(
                    id=case_id,
                    category=item.get("category", "general"),
                    user_message=item["user_message"],
                    expected_config=dumps_json(payload),
                    tags=dumps_json(tags),
                )
            )
            inserted += 1
        else:
            existing.category = item.get("category", "general")
            existing.user_message = item["user_message"]
            existing.expected_config = dumps_json(payload)
            existing.tags = dumps_json(tags)

    return inserted



def golden_set_count(session: Session) -> int:
    return len(session.scalars(select(GoldenSet.id)).all())
