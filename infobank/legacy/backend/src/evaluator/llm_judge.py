from __future__ import annotations

import time

from core.config import load_settings
from core.errors import DependencyUnavailableError
from core.ollama import chat_json_with_ollama
from core.types import EvidenceResult, LLMJudgment, RuleResult


def _communication_score(text: str) -> float:
    polite = ["안내", "도와드", "확인", "권장", "부탁"]
    has_polite = any(token in text for token in polite)
    base = 70.0 + (10.0 if has_polite else 0.0)
    if len(text) > 140:
        base += 5.0
    return min(base, 95.0)


def _resolution_score(user_message: str, assistant_response: str) -> float:
    action_terms = ["신청", "변경", "연결", "확인", "절차", "방법"]
    score = 65.0
    if any(term in assistant_response for term in action_terms):
        score += 20.0
    if "상담원" in assistant_response and "연결" in assistant_response:
        score += 5.0
    if len(user_message) > 10 and len(assistant_response) > 20:
        score += 5.0
    return min(score, 95.0)


def _heuristic_judge(
    user_message: str,
    assistant_response: str,
    rule_results: list[RuleResult],
    evidence_result: EvidenceResult,
) -> LLMJudgment:
    start = time.perf_counter()

    critical_count = sum(1 for item in rule_results if item.severity == "critical")
    warning_count = sum(1 for item in rule_results if item.severity != "critical")

    correctness = 80.0
    correctness -= critical_count * 25
    correctness -= warning_count * 8
    correctness -= 30 if evidence_result.has_contradiction else 0
    correctness = max(0.0, min(100.0, correctness))

    resolution = _resolution_score(user_message, assistant_response)
    communication = _communication_score(assistant_response)

    failure_types = [item.failure_type for item in rule_results]
    if evidence_result.has_contradiction:
        failure_types.append("CONTRADICTED_BY_SOURCE")

    escalation_needed = critical_count > 0 or evidence_result.has_contradiction
    explanation = "Rule/Evidence 기반 휴리스틱 판정 결과"
    judge_ms = int((time.perf_counter() - start) * 1000)

    return LLMJudgment(
        correctness=round(correctness, 2),
        resolution=round(resolution, 2),
        communication=round(communication, 2),
        escalation_needed=escalation_needed,
        failure_types=sorted(set(failure_types)),
        explanation=explanation,
        judge_ms=judge_ms,
    )


def _llm_judge(
    user_message: str,
    assistant_response: str,
    rule_results: list[RuleResult],
    evidence_result: EvidenceResult,
) -> LLMJudgment:
    try:
        settings = load_settings()
    except ValueError as exc:
        raise DependencyUnavailableError("runtime", str(exc)) from exc
    if not settings.ollama_judge_model:
        raise DependencyUnavailableError("ollama", "QUALBOT_OLLAMA_JUDGE_MODEL is required in llm mode")

    start = time.perf_counter()
    system_prompt = (
        "당신은 상담 품질 평가 전문가다. 반드시 JSON object만 출력한다. "
        "스키마: {\"correctness\":0-100,\"resolution\":0-100,\"communication\":0-100,"
        "\"escalation_needed\":true|false,\"failure_types\":[\"...\"],\"explanation\":\"...\"}"
    )
    user_prompt = (
        f"고객 질문:\n{user_message}\n\n"
        f"챗봇 답변:\n{assistant_response}\n\n"
        f"규칙 평가 결과:\n{[item.to_dict() for item in rule_results]}\n\n"
        f"근거 검증 결과:\n{evidence_result.to_dict()}\n\n"
        "평가 기준: 정확성, 해결성, 대화 품질. "
        "실패 유형은 규칙/근거 모순을 반영하라."
    )
    parsed = chat_json_with_ollama(
        model=settings.ollama_judge_model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        retries=1,
    )

    def _score(name: str, fallback: float) -> float:
        raw = parsed.get(name, fallback)
        value = float(raw) if isinstance(raw, int | float) else fallback
        return round(max(0.0, min(100.0, value)), 2)

    failure_types_raw = parsed.get("failure_types", [])
    failure_types = []
    if isinstance(failure_types_raw, list):
        failure_types = sorted({str(item) for item in failure_types_raw if str(item).strip()})
    if evidence_result.has_contradiction:
        failure_types = sorted(set(failure_types + ["CONTRADICTED_BY_SOURCE"]))

    escalation_needed = bool(parsed.get("escalation_needed", False)) or evidence_result.has_contradiction
    explanation = str(parsed.get("explanation", "")).strip() or "LLM Judge 결과"

    return LLMJudgment(
        correctness=_score("correctness", 70.0),
        resolution=_score("resolution", 70.0),
        communication=_score("communication", 70.0),
        escalation_needed=escalation_needed,
        failure_types=failure_types,
        explanation=explanation,
        judge_ms=int((time.perf_counter() - start) * 1000),
    )


def judge_response(
    user_message: str,
    assistant_response: str,
    rule_results: list[RuleResult],
    evidence_result: EvidenceResult,
) -> LLMJudgment:
    try:
        settings = load_settings()
    except ValueError as exc:
        raise DependencyUnavailableError("runtime", str(exc)) from exc
    if settings.eval_mode == "heuristic":
        return _heuristic_judge(user_message, assistant_response, rule_results, evidence_result)
    if settings.eval_mode == "llm":
        return _llm_judge(user_message, assistant_response, rule_results, evidence_result)
    raise ValueError(f"unsupported eval mode: {settings.eval_mode}")
