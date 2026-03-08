from __future__ import annotations

from core.constants import CRITICAL_GRADE, GRADE_BANDS, WEIGHTS
from core.types import EvidenceResult, LLMJudgment, QualityScore, RuleResult


def compute_compliance(rule_results: list[RuleResult]) -> float:
    score = 100.0
    for item in rule_results:
        if item.severity == "critical":
            score -= 100
        else:
            score -= 20
    return max(0.0, score)



def to_grade(total: float) -> str:
    for grade, minimum in GRADE_BANDS:
        if total >= minimum:
            return grade
    return "F"



def compute_score(
    rule_results: list[RuleResult],
    evidence_result: EvidenceResult,
    judgment: LLMJudgment,
) -> QualityScore:
    critical_fail = any(item.severity == "critical" for item in rule_results) or evidence_result.has_contradiction

    compliance = compute_compliance(rule_results)
    if critical_fail:
        failures = [item.failure_type for item in rule_results]
        if evidence_result.has_contradiction:
            failures.append("CONTRADICTED_BY_SOURCE")
        return QualityScore(
            total=0.0,
            grade=CRITICAL_GRADE,
            correctness=judgment.correctness,
            groundedness=evidence_result.groundedness_score,
            compliance=compliance,
            resolution=judgment.resolution,
            communication=judgment.communication,
            failure_types=sorted(set(failures)),
            is_critical=True,
            explanation="Critical violation detected",
        )

    total = (
        WEIGHTS["correctness"] * judgment.correctness
        + WEIGHTS["groundedness"] * evidence_result.groundedness_score
        + WEIGHTS["compliance"] * compliance
        + WEIGHTS["resolution"] * judgment.resolution
        + WEIGHTS["communication"] * judgment.communication
    )

    failure_types = sorted(set(judgment.failure_types + [item.failure_type for item in rule_results]))

    return QualityScore(
        total=round(total, 2),
        grade=to_grade(total),
        correctness=judgment.correctness,
        groundedness=evidence_result.groundedness_score,
        compliance=compliance,
        resolution=judgment.resolution,
        communication=judgment.communication,
        failure_types=failure_types,
        is_critical=False,
        explanation=judgment.explanation,
    )
