from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.config import load_settings
from core.errors import DependencyUnavailableError
from core.json_utils import loads_json
from db.models import KnowledgeDoc
from db.seed import seed_knowledge_base
from sqlalchemy import select
from sqlalchemy.orm import Session


@dataclass
class RetrievedDoc:
    doc_id: str
    title: str
    category: str
    content: str
    score: float


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9가-힣]+")


def tokenize(text: str) -> set[str]:
    return {tok.lower() for tok in TOKEN_PATTERN.findall(text)}


class Retriever:
    def __init__(self, session: Session):
        self.session = session

    def index_directory(self, root: str | Path) -> int:
        return seed_knowledge_base(self.session, Path(root))

    def _all_docs(self) -> list[KnowledgeDoc]:
        return list(self.session.scalars(select(KnowledgeDoc)).all())

    def _search_keyword(self, query: str, top_k: int, category: str | None) -> list[RetrievedDoc]:
        docs = self._all_docs()
        q_tokens = tokenize(query)
        scored: list[RetrievedDoc] = []

        for doc in docs:
            if category and doc.category != category:
                continue
            d_tokens = tokenize(doc.content)
            if not q_tokens or not d_tokens:
                score = 0.0
            else:
                score = len(q_tokens & d_tokens) / len(q_tokens)
            if score > 0:
                scored.append(
                    RetrievedDoc(
                        doc_id=doc.id,
                        title=doc.title,
                        category=doc.category,
                        content=doc.content,
                        score=round(score, 4),
                    )
                )

        scored.sort(key=lambda item: item.score, reverse=True)
        if scored:
            return scored[:top_k]

        fallback = docs[:top_k]
        return [
            RetrievedDoc(
                doc_id=doc.id,
                title=doc.title,
                category=doc.category,
                content=doc.content,
                score=0.0,
            )
            for doc in fallback
        ]

    def _search_chroma(self, query: str, top_k: int, category: str | None) -> list[RetrievedDoc]:
        try:
            settings = load_settings()
        except ValueError as exc:
            raise DependencyUnavailableError("runtime", str(exc)) from exc
        if not settings.enable_chroma:
            raise DependencyUnavailableError("chroma", "QUALBOT_ENABLE_CHROMA=1 is required in llm mode")

        persist_dir = settings.chroma_persist_dir
        collection_name = settings.chroma_collection
        if not persist_dir or not collection_name:
            raise DependencyUnavailableError("chroma", "Missing Chroma config env (persist dir / collection)")

        try:
            import chromadb
        except ImportError as exc:  # pragma: no cover - depends on runtime package
            raise DependencyUnavailableError("chroma", "chromadb package is not installed") from exc

        docs = self._all_docs()
        if not docs:
            return []

        try:
            client: Any = chromadb.PersistentClient(path=persist_dir)
            collection: Any = client.get_or_create_collection(name=collection_name)
            collection.upsert(
                ids=[doc.id for doc in docs],
                documents=[doc.content for doc in docs],
                metadatas=[{"title": doc.title, "category": doc.category} for doc in docs],
            )

            if category:
                result: dict[str, Any] = collection.query(query_texts=[query], n_results=top_k, where={"category": category})
            else:
                result = collection.query(query_texts=[query], n_results=top_k)
        except Exception as exc:  # noqa: BLE001
            raise DependencyUnavailableError("chroma", f"Chroma query failed: {exc}") from exc

        ids = list((result.get("ids") or [[]])[0])
        metadatas = list((result.get("metadatas") or [[]])[0])
        distances = list((result.get("distances") or [[]])[0])
        if not ids:
            return []

        by_id = {doc.id: doc for doc in docs}
        items: list[RetrievedDoc] = []
        for index, doc_id in enumerate(ids):
            source = by_id.get(doc_id)
            if source is None:
                continue
            metadata = metadatas[index] if index < len(metadatas) and isinstance(metadatas[index], dict) else {}
            distance = distances[index] if index < len(distances) and isinstance(distances[index], int | float) else 1.0
            score = 1.0 / (1.0 + float(distance))
            items.append(
                RetrievedDoc(
                    doc_id=source.id,
                    title=str(metadata.get("title", source.title)),
                    category=str(metadata.get("category", source.category)),
                    content=source.content,
                    score=round(score, 4),
                )
            )
        return items[:top_k]

    def search(
        self,
        query: str,
        top_k: int = 3,
        category: str | None = None,
        backend: str | None = None,
    ) -> list[RetrievedDoc]:
        if backend:
            chosen = backend
        else:
            try:
                chosen = load_settings().retrieval_backend
            except ValueError as exc:
                raise DependencyUnavailableError("runtime", str(exc)) from exc
        if chosen == "keyword":
            return self._search_keyword(query, top_k=top_k, category=category)
        if chosen == "chroma":
            return self._search_chroma(query, top_k=top_k, category=category)
        raise ValueError(f"unsupported retrieval backend: {chosen}")

    def get_docs_by_ids(self, doc_ids: list[str]) -> list[KnowledgeDoc]:
        if not doc_ids:
            return []
        stmt = select(KnowledgeDoc).where(KnowledgeDoc.id.in_(doc_ids))
        return list(self.session.scalars(stmt).all())

    @staticmethod
    def parse_metadata(doc: KnowledgeDoc) -> dict[str, str]:
        return loads_json(doc.metadata_json, {})
