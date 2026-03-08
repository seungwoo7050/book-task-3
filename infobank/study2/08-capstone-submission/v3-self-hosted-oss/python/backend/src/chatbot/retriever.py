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
QUERY_ALIASES: dict[str, tuple[str, ...]] = {
    "가족결합": ("패밀리", "회선 결합", "가족 할인"),
    "로밍패스": ("로밍 패스", "사전 신청", "추가 과금"),
    "번호이동": ("자동 해지", "해지 절차", "해지 접수"),
    "본인인증": ("본인확인", "인증", "추가 확인"),
    "명의변경": ("본인확인", "인증", "명의 변경"),
    "환불 거절": ("분쟁", "민원", "전문 부서"),
}
DOMAIN_TO_CATEGORY = {
    "policy": "policies",
    "procedure": "procedures",
    "pricing": "plans",
}
CATEGORY_TRIGGERS: dict[str, tuple[str, ...]] = {
    "policies": ("위약금", "약정", "환불", "분쟁", "민원", "주민번호", "카드번호", "개인정보", "할인"),
    "procedures": ("절차", "신청", "접수", "순서", "인증", "본인확인", "변경", "청구", "연결"),
    "plans": ("요금제", "요금", "데이터", "베이직", "프리미엄", "가족결합", "패밀리", "부가팩", "로밍패스"),
}
RISK_DOC_IDS: dict[str, tuple[str, ...]] = {
    "escalation": ("policies__escalation_policy.md",),
    "privacy": ("policies__privacy_policy.md",),
    "verification": ("procedures__identity_verification.md", "policies__refund_policy.md"),
}


def tokenize(text: str) -> set[str]:
    return {tok.lower() for tok in TOKEN_PATTERN.findall(text)}


@dataclass(frozen=True)
class RetrievalPlan:
    categories: tuple[str, ...]
    expanded_terms: tuple[str, ...]
    risk_flags: tuple[str, ...]


def _build_retrieval_plan(query: str, category_hint: str | None) -> RetrievalPlan:
    normalized_query = query.lower()
    expanded_terms = set(tokenize(query))
    risk_flags: list[str] = []
    categories: list[str] = []

    if category_hint:
        mapped = DOMAIN_TO_CATEGORY.get(category_hint, category_hint)
        if mapped in {"policies", "procedures", "plans"}:
            categories.append(mapped)

    for trigger, aliases in QUERY_ALIASES.items():
        if trigger in normalized_query:
            expanded_terms.update(tokenize(" ".join(aliases)))

    for category, triggers in CATEGORY_TRIGGERS.items():
        if any(trigger in normalized_query for trigger in triggers):
            categories.append(category)

    if any(term in normalized_query for term in ("분쟁", "민원", "환불 거절", "피해")):
        categories.insert(0, "policies")
        risk_flags.append("escalation")
    if any(term in normalized_query for term in ("주민번호", "카드번호", "개인정보")):
        categories.insert(0, "policies")
        risk_flags.append("privacy")
    if any(term in normalized_query for term in ("본인인증", "본인확인", "인증", "명의변경", "해지", "환불")):
        categories.insert(0, "procedures")
        risk_flags.append("verification")

    deduped_categories = tuple(dict.fromkeys(categories)) or ("policies", "procedures", "plans")
    deduped_risks = tuple(dict.fromkeys(risk_flags))
    return RetrievalPlan(
        categories=deduped_categories,
        expanded_terms=tuple(sorted(expanded_terms)),
        risk_flags=deduped_risks,
    )


class Retriever:
    def __init__(self, session: Session):
        self.session = session

    def index_directory(self, root: str | Path) -> int:
        return seed_knowledge_base(self.session, Path(root))

    def _all_docs(self, bundle_id: str | None = None) -> list[KnowledgeDoc]:
        stmt = select(KnowledgeDoc)
        if bundle_id:
            stmt = stmt.where(KnowledgeDoc.bundle_id == bundle_id)
        return list(self.session.scalars(stmt).all())

    def _search_keyword_v1(self, query: str, top_k: int, category: str | None, bundle_id: str | None) -> list[RetrievedDoc]:
        docs = self._all_docs(bundle_id=bundle_id)
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

    def _fallback_docs(self, docs: list[KnowledgeDoc], top_k: int, plan: RetrievalPlan) -> list[RetrievedDoc]:
        preferred = [doc for doc in docs if doc.category in plan.categories]
        pool = preferred or docs
        return [
            RetrievedDoc(
                doc_id=doc.id,
                title=doc.title,
                category=doc.category,
                content=doc.content,
                score=0.0,
            )
            for doc in pool[:top_k]
        ]

    def _search_keyword_v2(self, query: str, top_k: int, category: str | None, bundle_id: str | None) -> list[RetrievedDoc]:
        docs = self._all_docs(bundle_id=bundle_id)
        plan = _build_retrieval_plan(query, category)
        q_tokens = set(plan.expanded_terms)
        if not docs:
            return []

        scored: list[RetrievedDoc] = []
        for doc in docs:
            metadata = self.parse_metadata(doc)
            doc_terms = tokenize(doc.content) | tokenize(doc.title)
            metadata_terms = tokenize(" ".join(str(item) for item in metadata.get("aliases", [])))
            metadata_terms |= tokenize(" ".join(str(item) for item in metadata.get("keywords", [])))

            content_overlap = len(q_tokens & doc_terms) / max(1, len(q_tokens))
            metadata_overlap = len(q_tokens & metadata_terms) / max(1, len(q_tokens))
            category_bonus = 0.0
            if doc.category in plan.categories:
                rank = plan.categories.index(doc.category)
                category_bonus = 0.28 - min(rank, 2) * 0.06

            alias_bonus = 0.0
            for alias in metadata.get("aliases", []):
                alias_text = str(alias).strip().lower()
                if alias_text and alias_text in query.lower():
                    alias_bonus = 0.25
                    break

            risk_bonus = 0.0
            for risk in plan.risk_flags:
                if doc.id in RISK_DOC_IDS.get(risk, ()):
                    risk_bonus += 0.35

            total = round(content_overlap * 0.7 + metadata_overlap * 0.9 + category_bonus + alias_bonus + risk_bonus, 4)
            if total > 0:
                scored.append(
                    RetrievedDoc(
                        doc_id=doc.id,
                        title=doc.title,
                        category=doc.category,
                        content=doc.content,
                        score=total,
                    )
                )

        scored.sort(key=lambda item: (item.score, -len(item.content)), reverse=True)
        if scored:
            return scored[:top_k]
        return self._fallback_docs(docs, top_k=top_k, plan=plan)

    def _search_chroma(self, query: str, top_k: int, category: str | None, bundle_id: str | None) -> list[RetrievedDoc]:
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
        except BaseException as exc:  # pragma: no cover - dependency import can fail before ImportError
            raise DependencyUnavailableError("chroma", f"chromadb import failed: {exc}") from exc

        docs = self._all_docs(bundle_id=bundle_id)
        if not docs:
            return []

        plan = _build_retrieval_plan(query, category)
        query_text = query
        if settings.retrieval_version != "retrieval-v1":
            query_text = " ".join(dict.fromkeys([query, *plan.expanded_terms]))

        try:
            client: Any = chromadb.PersistentClient(path=persist_dir)
            collection: Any = client.get_or_create_collection(name=collection_name)
            collection.upsert(
                ids=[doc.id for doc in docs],
                documents=[doc.content for doc in docs],
                metadatas=[{"title": doc.title, "category": doc.category} for doc in docs],
            )

            preferred_category = next((name for name in plan.categories if name in {"policies", "procedures", "plans"}), None)
            if preferred_category:
                result: dict[str, Any] = collection.query(
                    query_texts=[query_text],
                    n_results=top_k,
                    where={"category": preferred_category},
                )
            else:
                result = collection.query(query_texts=[query_text], n_results=top_k)
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
        bundle_id: str | None = None,
    ) -> list[RetrievedDoc]:
        if backend:
            chosen = backend
        else:
            try:
                settings = load_settings()
                chosen = settings.retrieval_backend
            except ValueError as exc:
                raise DependencyUnavailableError("runtime", str(exc)) from exc
        if not backend:
            retrieval_version = settings.retrieval_version
        else:
            try:
                retrieval_version = load_settings().retrieval_version
            except ValueError as exc:
                raise DependencyUnavailableError("runtime", str(exc)) from exc
        if chosen == "keyword":
            if retrieval_version == "retrieval-v1":
                return self._search_keyword_v1(query, top_k=top_k, category=category, bundle_id=bundle_id)
            return self._search_keyword_v2(query, top_k=top_k, category=category, bundle_id=bundle_id)
        if chosen == "chroma":
            return self._search_chroma(query, top_k=top_k, category=category, bundle_id=bundle_id)
        raise ValueError(f"unsupported retrieval backend: {chosen}")

    def get_docs_by_ids(self, doc_ids: list[str]) -> list[KnowledgeDoc]:
        if not doc_ids:
            return []
        stmt = select(KnowledgeDoc).where(KnowledgeDoc.id.in_(doc_ids))
        return list(self.session.scalars(stmt).all())

    @staticmethod
    def parse_metadata(doc: KnowledgeDoc) -> dict[str, Any]:
        return loads_json(doc.metadata_json, {})
