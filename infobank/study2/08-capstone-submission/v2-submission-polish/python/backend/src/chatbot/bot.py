from __future__ import annotations

import time
from collections.abc import Sequence
from dataclasses import dataclass, field

from core.config import load_settings
from core.provider_chain import ProviderChain
from core.types import ProviderAttempt
from sqlalchemy.orm import Session

from chatbot.guardrail import run_online_guardrail
from chatbot.retriever import RetrievedDoc, Retriever


@dataclass
class ChatbotReply:
    assistant_response: str
    retrieved_doc_ids: list[str]
    latency_ms: int
    guardrail_hits: list[dict[str, str]]
    provider_trace: list[dict[str, object]] = field(default_factory=list)


class ChatbotService:
    def __init__(self, session: Session):
        self.session = session
        self.retriever = Retriever(session)
        self.settings = load_settings()
        self.provider_chain = ProviderChain(self.settings)

    def _compose_fallback(self, user_message: str, doc_snippets: list[str]) -> str:
        if doc_snippets:
            return (
                f"문의 주신 내용은 다음 정책을 참고해 안내드릴 수 있습니다: {doc_snippets[0]} "
                "정확한 개인별 적용 여부는 상담원 확인이 필요할 수 있습니다."
            )
        if any(keyword in user_message for keyword in ["분쟁", "민원", "환불 거절", "피해"]):
            return "분쟁 또는 민원 이슈로 보여 상담원 또는 전문 부서 이관 기준을 먼저 안내드리겠습니다."
        return "현재 즉시 확인 가능한 근거 문서가 없어 상담원 연결을 권장드립니다."

    def _compose_retrieval_v2(self, user_message: str, docs: Sequence[RetrievedDoc]) -> str:
        if not docs:
            return "현재 즉시 확인 가능한 문서가 부족합니다. 상담원 연결로 정확한 적용 기준을 확인해 드리겠습니다."
        selected_docs: list[RetrievedDoc] = []

        def add_doc(doc: RetrievedDoc | None) -> None:
            if doc is not None and all(existing.doc_id != doc.doc_id for existing in selected_docs):
                selected_docs.append(doc)

        add_doc(docs[0])
        if any(keyword in user_message for keyword in ["분쟁", "민원", "환불 거절", "피해"]):
            add_doc(next((doc for doc in docs if doc.doc_id == "policies__escalation_policy.md"), None))
        if any(keyword in user_message for keyword in ["주민번호", "카드번호", "개인정보"]):
            add_doc(next((doc for doc in docs if doc.doc_id == "policies__privacy_policy.md"), None))
        if any(keyword in user_message for keyword in ["본인인증", "본인확인", "인증", "명의변경", "해지", "환불"]):
            add_doc(next((doc for doc in docs if doc.doc_id == "procedures__identity_verification.md"), None))
        for doc in docs[1:]:
            add_doc(doc)
            if len(selected_docs) >= 2:
                break

        snippets: list[str] = []
        for doc in selected_docs[:2]:
            snippet = " ".join(line.strip() for line in doc.content.splitlines() if line.strip())
            if snippet and snippet not in snippets:
                snippets.append(snippet)

        return " ".join(snippets) if snippets else "현재 확인 가능한 근거 문서가 부족해 상담원 연결이 필요합니다."

    def answer(self, user_message: str) -> ChatbotReply:
        start = time.perf_counter()
        docs = self.retriever.search(user_message, top_k=3)
        retrieved_doc_ids = [doc.doc_id for doc in docs]
        doc_snippets = [doc.content[:180] for doc in docs]

        if self.settings.retrieval_version == "retrieval-v1":
            assistant = self._compose_fallback(user_message, doc_snippets)
        else:
            assistant = self._compose_retrieval_v2(user_message, docs)
        provider_attempts: list[ProviderAttempt] = []
        if self.settings.eval_mode == "llm":
            try:
                assistant, provider_attempts = self.provider_chain.generate_text(
                    system_prompt=(
                        "당신은 통신사 상담 QA 데모용 챗봇이다. "
                        "정책 문서에 없는 내용은 확정하지 말고, 필요한 경우 상담원 이관과 본인확인을 명시하라."
                    ),
                    user_prompt=(
                        f"사용자 질문: {user_message}\n\n"
                        f"근거 문서:\n" + "\n".join(f"- {snippet}" for snippet in doc_snippets)
                    ),
                )
            except Exception:  # noqa: BLE001 - v1 keeps live failure outside chat UX and falls back locally
                provider_attempts = []

        guardrail = run_online_guardrail(assistant)
        if any(hit.severity == "critical" for hit in guardrail):
            assistant = "정책상 확정 안내가 어려워 상담원 연결로 도와드리겠습니다."

        latency_ms = int((time.perf_counter() - start) * 1000)
        return ChatbotReply(
            assistant_response=assistant,
            retrieved_doc_ids=retrieved_doc_ids,
            latency_ms=latency_ms,
            guardrail_hits=[hit.to_dict() for hit in guardrail],
            provider_trace=[attempt.to_dict() for attempt in provider_attempts],
        )
