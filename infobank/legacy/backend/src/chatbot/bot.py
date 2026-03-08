from __future__ import annotations

import time
from dataclasses import dataclass

from core.ollama import chat_with_ollama
from sqlalchemy.orm import Session

from chatbot.guardrail import run_online_guardrail
from chatbot.retriever import Retriever


@dataclass
class ChatbotReply:
    assistant_response: str
    retrieved_doc_ids: list[str]
    latency_ms: int
    guardrail_hits: list[dict[str, str]]


class ChatbotService:
    def __init__(self, session: Session):
        self.session = session
        self.retriever = Retriever(session)

    def answer(self, user_message: str) -> ChatbotReply:
        start = time.perf_counter()
        docs = self.retriever.search(user_message, top_k=3)
        retrieved_doc_ids = [doc.doc_id for doc in docs]

        ollama_result = chat_with_ollama(
            system_prompt=(
                "당신은 통신사 상담 봇입니다. 불확실한 내용은 확정하지 말고 근거 중심으로 답변하세요."
            ),
            user_prompt=(
                f"사용자 질문: {user_message}\n\n"
                f"근거 문서:\n" + "\n".join(f"- {doc.content[:180]}" for doc in docs)
            ),
        )

        if ollama_result and "message" in ollama_result:
            assistant = str(ollama_result["message"].get("content", "")).strip()
        elif docs:
            assistant = (
                f"문의 주신 내용은 다음 정책을 참고해 안내드릴 수 있습니다: {docs[0].content[:220]} "
                "정확한 개인별 적용 여부는 상담원 확인이 필요할 수 있습니다."
            )
        else:
            assistant = "현재 즉시 확인 가능한 근거 문서가 없어 상담원 연결을 권장드립니다."

        guardrail = run_online_guardrail(assistant)
        if any(hit.severity == "critical" for hit in guardrail):
            assistant = "정책상 확정 안내가 어려워 상담원 연결로 도와드리겠습니다."

        latency_ms = int((time.perf_counter() - start) * 1000)
        return ChatbotReply(
            assistant_response=assistant,
            retrieved_doc_ids=retrieved_doc_ids,
            latency_ms=latency_ms,
            guardrail_hits=[hit.to_dict() for hit in guardrail],
        )
