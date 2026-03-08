from __future__ import annotations

import re

from core.config import load_settings
from core.errors import DependencyUnavailableError
from core.ollama import chat_json_with_ollama
from core.types import Claim

CLAIM_SPLIT = re.compile(r"[.!?\n]+")
CRITICAL_KEYWORDS = {"위약금", "환불", "개인정보", "해지", "할인", "요금", "면제"}
DOMAIN_MAP = {
    "policy": {"정책", "위약금", "약관", "해지", "고지"},
    "procedure": {"절차", "신청", "변경", "인증"},
    "pricing": {"요금", "할인", "부과", "원", "금액"},
    "technical": {"데이터", "로밍", "속도", "품질", "네트워크"},
}


def _pick_domain(text: str) -> str:
    for domain, keywords in DOMAIN_MAP.items():
        if any(keyword in text for keyword in keywords):
            return domain
    return "other"


def _extract_claims_heuristic(assistant_response: str) -> list[Claim]:
    raw_sentences = [part.strip() for part in CLAIM_SPLIT.split(assistant_response) if part.strip()]
    candidates: list[str] = []

    for sentence in raw_sentences:
        if len(sentence) < 8:
            continue
        if any(char.isdigit() for char in sentence) or any(
            keyword in sentence for keyword in ["가능", "불가", "처리", "필요", "없", "있"]
        ):
            candidates.append(sentence)

    if not candidates and assistant_response.strip():
        candidates = [assistant_response.strip()[:120]]

    claims: list[Claim] = []
    for idx, sentence in enumerate(candidates, start=1):
        criticality = "critical" if any(keyword in sentence for keyword in CRITICAL_KEYWORDS) else "normal"
        claims.append(
            Claim(
                claim_id=f"claim-{idx}",
                statement=sentence,
                criticality=criticality,
                domain=_pick_domain(sentence),
                source_span=sentence,
            )
        )

    return claims


def _extract_claims_llm(assistant_response: str) -> list[Claim]:
    try:
        settings = load_settings()
    except ValueError as exc:
        raise DependencyUnavailableError("runtime", str(exc)) from exc
    if not settings.ollama_claim_model:
        raise DependencyUnavailableError("ollama", "QUALBOT_OLLAMA_CLAIM_MODEL is required in llm mode")

    system_prompt = (
        "당신은 상담 답변에서 검증 가능한 claim을 추출하는 평가기다. "
        "반드시 JSON object만 출력하고, 스키마는 "
        "{\"claims\":[{\"claim_id\":\"claim-1\",\"statement\":\"...\",\"criticality\":\"critical|normal\","
        "\"domain\":\"policy|procedure|pricing|technical|other\",\"source_span\":\"...\"}]} 이다."
    )
    user_prompt = (
        "아래 상담사 답변에서 사실 검증 가능한 claim만 추출하라.\n"
        "필드 누락 없이 작성하고, claim이 없으면 claims=[]를 반환하라.\n\n"
        f"답변:\n{assistant_response}"
    )
    parsed = chat_json_with_ollama(
        model=settings.ollama_claim_model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        retries=1,
    )
    if "claims" not in parsed:
        raise DependencyUnavailableError("ollama", "LLM claim extractor returned invalid schema: missing claims")
    raw_claims = parsed.get("claims", [])
    if not isinstance(raw_claims, list):
        raise DependencyUnavailableError("ollama", "LLM claim extractor returned invalid schema: claims must be list")

    claims: list[Claim] = []
    for idx, raw in enumerate(raw_claims, start=1):
        if not isinstance(raw, dict):
            raise DependencyUnavailableError("ollama", "LLM claim extractor returned invalid schema: claim must be object")
        statement_raw = raw.get("statement")
        if not isinstance(statement_raw, str):
            raise DependencyUnavailableError("ollama", "LLM claim extractor returned invalid schema: statement must be string")
        statement = statement_raw.strip()
        if not statement:
            continue
        claim_id = str(raw.get("claim_id", f"claim-{idx}"))
        criticality = str(raw.get("criticality", "normal"))
        if criticality not in {"critical", "normal"}:
            criticality = "critical" if any(keyword in statement for keyword in CRITICAL_KEYWORDS) else "normal"
        domain = str(raw.get("domain", "other"))
        if domain not in {"policy", "procedure", "pricing", "technical", "other"}:
            domain = _pick_domain(statement)
        source_span = str(raw.get("source_span", statement))
        claims.append(
            Claim(
                claim_id=claim_id,
                statement=statement,
                criticality=criticality,
                domain=domain,
                source_span=source_span,
            )
        )

    return claims


def extract_claims(assistant_response: str) -> list[Claim]:
    try:
        settings = load_settings()
    except ValueError as exc:
        raise DependencyUnavailableError("runtime", str(exc)) from exc
    if settings.eval_mode == "heuristic":
        return _extract_claims_heuristic(assistant_response)
    if settings.eval_mode == "llm":
        return _extract_claims_llm(assistant_response)
    raise ValueError(f"unsupported eval mode: {settings.eval_mode}")
