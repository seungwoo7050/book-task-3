from __future__ import annotations

import time
from collections import Counter, defaultdict

from core.json_utils import loads_json
from core.types import VersionCompareResult
from db.models import Evaluation, Turn
from evaluator.pipeline_stats import get_stats_store
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.dependencies import get_session

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard/overview")
def dashboard_overview(session: Session = Depends(get_session)) -> dict[str, object]:
    evals = list(session.scalars(select(Evaluation)).all())
    turns = list(session.scalars(select(Turn)).all())

    avg_score = round(sum(item.total_score for item in evals) / len(evals), 2) if evals else 0.0
    critical_count = sum(1 for item in evals if item.is_critical)
    fail_rate = round((critical_count / len(evals)) * 100, 2) if evals else 0.0

    grade_distribution: dict[str, int] = defaultdict(int)
    failure_counter: Counter[str] = Counter()
    for item in evals:
        grade_distribution[item.grade] += 1
        for failure in loads_json(item.failure_types, []):
            failure_counter[failure] += 1

    avg_latency = round(sum(turn.latency_ms for turn in turns) / len(turns), 2) if turns else 0.0

    return {
        "avg_score": avg_score,
        "fail_rate": fail_rate,
        "critical_count": critical_count,
        "evaluation_count": len(evals),
        "avg_latency_ms": avg_latency,
        "grade_distribution": dict(sorted(grade_distribution.items())),
        "failure_top": [{"failure_type": k, "count": v} for k, v in failure_counter.most_common(10)],
    }


@router.get("/dashboard/failures")
def dashboard_failures(session: Session = Depends(get_session)) -> dict[str, object]:
    evals = list(session.scalars(select(Evaluation)).all())
    by_type: dict[str, dict[str, float]] = {}

    for item in evals:
        failures = loads_json(item.failure_types, [])
        for failure in failures:
            slot = by_type.setdefault(failure, {"count": 0, "score_sum": 0.0, "critical": 0})
            slot["count"] += 1
            slot["score_sum"] += item.total_score
            if item.is_critical:
                slot["critical"] += 1

    items: list[dict[str, object]] = []
    for failure_type, stats in by_type.items():
        avg_score = round(stats["score_sum"] / max(1, stats["count"]), 2)
        items.append(
            {
                "failure_type": failure_type,
                "count": int(stats["count"]),
                "critical_count": int(stats["critical"]),
                "avg_score": avg_score,
            }
        )

    def _count_key(item: dict[str, object]) -> int:
        value = item.get("count")
        return value if isinstance(value, int) else 0

    items.sort(key=_count_key, reverse=True)
    return {"items": items}


@router.get("/dashboard/metrics")
def dashboard_metrics(session: Session = Depends(get_session)) -> dict[str, object]:
    evals = list(session.scalars(select(Evaluation)).all())
    unsupported_claim_count = 0
    for row in evals:
        unsupported_claim_count += loads_json(row.failure_types, []).count("UNSUPPORTED_CLAIM")

    snapshot = get_stats_store().snapshot().to_dict()
    snapshot.update(
        {
            "eval_total": len(evals),
            "eval_critical": sum(1 for item in evals if item.is_critical),
            "eval_unsupported_claim": unsupported_claim_count,
        }
    )
    return snapshot


@router.get("/dashboard/version-compare")
def dashboard_version_compare(
    baseline: str,
    candidate: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    started = time.perf_counter()

    baseline_rows = list(session.scalars(select(Evaluation).where(Evaluation.prompt_version == baseline)).all())
    candidate_rows = list(session.scalars(select(Evaluation).where(Evaluation.prompt_version == candidate)).all())

    def _avg(rows: list[Evaluation]) -> float:
        return round(sum(item.total_score for item in rows) / len(rows), 2) if rows else 0.0

    def _critical(rows: list[Evaluation]) -> int:
        return sum(1 for item in rows if item.is_critical)

    def _failure(rows: list[Evaluation], failure_type: str) -> int:
        return sum(loads_json(item.failure_types, []).count(failure_type) for item in rows)

    result = VersionCompareResult(
        baseline=baseline,
        candidate=candidate,
        baseline_avg=_avg(baseline_rows),
        candidate_avg=_avg(candidate_rows),
        baseline_critical=_critical(baseline_rows),
        candidate_critical=_critical(candidate_rows),
        baseline_forbidden_promise=_failure(baseline_rows, "FORBIDDEN_PROMISE"),
        candidate_forbidden_promise=_failure(candidate_rows, "FORBIDDEN_PROMISE"),
        delta=round(_avg(candidate_rows) - _avg(baseline_rows), 2),
    )

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    get_stats_store().record_version_compare(elapsed_ms)

    return {"result": result.to_dict()}
