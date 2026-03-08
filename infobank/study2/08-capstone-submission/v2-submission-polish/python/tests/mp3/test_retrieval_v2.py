from __future__ import annotations

import os

from chatbot.retriever import Retriever
from db.database import session_scope


def _search(query: str, *, version: str) -> list[str]:
    os.environ["QUALBOT_RETRIEVAL_VERSION"] = version
    with session_scope() as session:
        return [doc.doc_id for doc in Retriever(session).search(query, top_k=3, backend="keyword")]


def test_retrieval_v2_promotes_roaming_pack_alias_query():
    baseline = _search("로밍패스 신청 없이 써도 되나요?", version="retrieval-v1")
    candidate = _search("로밍패스 신청 없이 써도 되나요?", version="retrieval-v2")

    assert "plans__roaming_pack.md" not in baseline[:1]
    assert candidate[0] == "plans__roaming_pack.md"


def test_retrieval_v2_combines_family_plan_and_discount_policy():
    baseline = _search("가족결합 할인은 무조건 50%인가요?", version="retrieval-v1")
    candidate = _search("가족결합 할인은 무조건 50%인가요?", version="retrieval-v2")

    assert baseline[0] == "policies__discount_policy.md"
    assert candidate[:2] == ["plans__family_plan.md", "policies__discount_policy.md"]


def test_retrieval_v2_prioritizes_refund_and_verification_documents_together():
    candidate = _search("환불 접수 전에 인증 필수인가요?", version="retrieval-v2")

    assert candidate[:2] == ["policies__refund_policy.md", "procedures__identity_verification.md"]
