from __future__ import annotations

from chatbot.retriever import RetrievedDoc, Retriever, tokenize
from core.config import load_settings
from core.errors import DependencyUnavailableError
from core.ollama import chat_json_with_ollama
from core.types import Claim, EvidenceClaimResult, EvidenceResult
from sqlalchemy.orm import Session

NEGATIVE_WORDS = {"없음", "없습니다", "불가", "안됨", "불가능"}
POSITIVE_WORDS = {"있음", "있습니다", "가능", "제공", "지원", "부과"}


def _heuristic_verdict(claim_text: str, doc_text: str) -> str:
    claim_has_negative = any(word in claim_text for word in NEGATIVE_WORDS)
    doc_has_positive = any(word in doc_text for word in POSITIVE_WORDS)
    claim_has_positive = any(word in claim_text for word in POSITIVE_WORDS)
    doc_has_negative = any(word in doc_text for word in NEGATIVE_WORDS)

    overlap = tokenize(claim_text) & tokenize(doc_text)
    coverage = len(overlap) / max(1, len(tokenize(claim_text)))

    if claim_has_negative and doc_has_positive:
        return "contradict"
    if claim_has_positive and doc_has_negative:
        return "contradict"
    if coverage >= 0.2:
        return "support"
    return "not_found"


def _llm_verdict(claim: Claim, docs: list[RetrievedDoc]) -> tuple[str, list[str], float]:
    settings = load_settings()
    if not settings.ollama_evidence_model:
        raise DependencyUnavailableError("ollama", "QUALBOT_OLLAMA_EVIDENCE_MODEL is required in llm mode")

    evidence_lines = []
    for doc in docs:
        evidence_lines.append(
            f"[{doc.doc_id}] (category={doc.category}, score={doc.score})\n{doc.content[:600]}"
        )
    evidence_blob = "\n\n".join(evidence_lines) if evidence_lines else "(no documents)"
    system_prompt = (
        "당신은 claim 근거 검증기다. 반드시 JSON object만 반환한다. "
        "스키마: {\"verdict\":\"support|contradict|not_found\","
        "\"confidence\":0.0,\"evidence_doc_ids\":[\"doc-id\"]}."
    )
    user_prompt = (
        f"Claim:\n{claim.statement}\n\n"
        f"Evidence documents:\n{evidence_blob}\n\n"
        "규칙: claim을 명확히 뒷받침하면 support, 반대면 contradict, 불충분하면 not_found."
    )
    parsed = chat_json_with_ollama(
        model=settings.ollama_evidence_model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        retries=1,
    )
    verdict = str(parsed.get("verdict", "not_found")).strip().lower()
    if verdict not in {"support", "contradict", "not_found"}:
        verdict = "not_found"
    confidence_raw = parsed.get("confidence", 0.5)
    confidence = float(confidence_raw) if isinstance(confidence_raw, int | float) else 0.5
    confidence = max(0.0, min(confidence, 1.0))
    evidence_doc_ids_raw = parsed.get("evidence_doc_ids", [])
    evidence_doc_ids: list[str] = []
    allowed_ids = {doc.doc_id for doc in docs}
    if isinstance(evidence_doc_ids_raw, list):
        for item in evidence_doc_ids_raw:
            item_str = str(item)
            if item_str in allowed_ids:
                evidence_doc_ids.append(item_str)
    if not evidence_doc_ids and verdict in {"support", "contradict"} and docs:
        evidence_doc_ids = [docs[0].doc_id]
    return verdict, evidence_doc_ids, round(confidence, 4)


def verify_claims(session: Session, claims: list[Claim], top_k: int = 3) -> EvidenceResult:
    try:
        settings = load_settings()
    except ValueError as exc:
        raise DependencyUnavailableError("runtime", str(exc)) from exc
    retriever = Retriever(session)

    if not claims:
        return EvidenceResult(claim_results=[], groundedness_score=0.0, has_contradiction=False, retrieval_hit_at_k=0.0)

    if settings.eval_mode == "llm" and settings.retrieval_backend != "chroma":
        raise DependencyUnavailableError("chroma", "llm mode requires QUALBOT_RETRIEVAL_BACKEND=chroma")

    claim_results: list[EvidenceClaimResult] = []
    support_count = 0
    contradiction_count = 0
    retrieval_hits = 0

    for claim in claims:
        backend = "keyword" if settings.eval_mode == "heuristic" else settings.retrieval_backend
        docs = retriever.search(claim.statement, top_k=top_k, backend=backend)
        if docs:
            retrieval_hits += 1

        verdict = "not_found"
        evidence_doc_ids: list[str] = []
        confidence = 0.5

        if settings.eval_mode == "llm":
            verdict, evidence_doc_ids, confidence = _llm_verdict(claim, docs)
        else:
            for doc in docs:
                current = _heuristic_verdict(claim.statement, doc.content)
                if current == "contradict":
                    verdict = "contradict"
                    evidence_doc_ids = [doc.doc_id]
                    confidence = 0.9
                    break
                if current == "support" and verdict != "support":
                    verdict = "support"
                    evidence_doc_ids = [doc.doc_id]
                    confidence = 0.95
            if verdict == "not_found":
                confidence = 0.5

        if verdict == "support":
            support_count += 1
        if verdict == "contradict":
            contradiction_count += 1

        claim_results.append(
            EvidenceClaimResult(
                claim_id=claim.claim_id,
                verdict=verdict,
                evidence_doc_ids=evidence_doc_ids,
                confidence=confidence,
            )
        )

    groundedness = (support_count / len(claims)) * 100.0
    retrieval_hit_at_k = retrieval_hits / len(claims)

    return EvidenceResult(
        claim_results=claim_results,
        groundedness_score=round(groundedness, 2),
        has_contradiction=contradiction_count > 0,
        retrieval_hit_at_k=round(retrieval_hit_at_k, 4),
    )
