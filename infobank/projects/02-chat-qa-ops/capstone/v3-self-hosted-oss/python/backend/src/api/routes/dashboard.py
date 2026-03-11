from __future__ import annotations

import time
from collections import Counter, defaultdict

from core.json_utils import loads_json
from core.types import VersionCompareResult
from db.models import AdminUser, Evaluation, EvaluationJob, EvaluationRun, Turn
from evaluator.pipeline_stats import get_stats_store
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.dependencies import get_current_admin, get_session

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def _resolve_run(session: Session, *, run_id: str | None, job_id: str | None) -> tuple[EvaluationRun | None, EvaluationJob | None]:
    if run_id:
        run = session.get(EvaluationRun, run_id)
        return run, session.scalar(select(EvaluationJob).where(EvaluationJob.run_id == run_id).limit(1))
    if job_id:
        job = session.get(EvaluationJob, job_id)
        if job is None or not job.run_id:
            return None, job
        return session.get(EvaluationRun, job.run_id), job
    job = session.scalar(select(EvaluationJob).where(EvaluationJob.run_id.is_not(None)).order_by(EvaluationJob.created_at.desc()).limit(1))
    if job is None or not job.run_id:
        return None, None
    return session.get(EvaluationRun, job.run_id), job


def _filtered_evaluations(session: Session, *, run_id: str | None, job_id: str | None) -> tuple[list[Evaluation], EvaluationRun | None, EvaluationJob | None]:
    run, job = _resolve_run(session, run_id=run_id, job_id=job_id)
    if run is None:
        return list(session.scalars(select(Evaluation)).all()), None, job
    return list(session.scalars(select(Evaluation).where(Evaluation.run_id == run.id)).all()), run, job


@router.get("/overview")
def dashboard_overview(
    run_id: str | None = None,
    job_id: str | None = None,
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    evals, run, job = _filtered_evaluations(session, run_id=run_id, job_id=job_id)
    turn_ids = [item.turn_id for item in evals]
    turns = list(session.scalars(select(Turn).where(Turn.id.in_(turn_ids))).all()) if turn_ids else []

    avg_score = round(sum(item.total_score for item in evals) / len(evals), 2) if evals else 0.0
    critical_count = sum(1 for item in evals if item.is_critical)
    fail_rate = round((critical_count / len(evals)) * 100, 2) if evals else 0.0

    grade_distribution: dict[str, int] = defaultdict(int)
    failure_counter: Counter[str] = Counter()
    run_labels: set[str] = set()
    for item in evals:
        grade_distribution[item.grade] += 1
        lineage = loads_json(item.lineage_json, {})
        run_label = lineage.get("run_label")
        if isinstance(run_label, str) and run_label:
            run_labels.add(run_label)
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
        "failure_top": [{"failure_type": key, "count": value} for key, value in failure_counter.most_common(10)],
        "run_labels": sorted(run_labels),
        "selected_run_id": run.id if run is not None else None,
        "selected_job_id": job.id if job is not None else None,
    }


@router.get("/failures")
def dashboard_failures(
    run_id: str | None = None,
    job_id: str | None = None,
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    evals, run, job = _filtered_evaluations(session, run_id=run_id, job_id=job_id)
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
    items.sort(key=lambda item: item["count"] if isinstance(item["count"], int) else 0, reverse=True)
    return {
        "selected_run_id": run.id if run is not None else None,
        "selected_job_id": job.id if job is not None else None,
        "items": items,
    }


@router.get("/metrics")
def dashboard_metrics(
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    evals = list(session.scalars(select(Evaluation).order_by(Evaluation.created_at.desc())).all())
    unsupported_claim_count = 0
    evaluation_runs = list(session.scalars(select(EvaluationRun)).all())
    for row in evals:
        unsupported_claim_count += loads_json(row.failure_types, []).count("UNSUPPORTED_CLAIM")

    snapshot = get_stats_store().snapshot().to_dict()
    snapshot.update(
        {
            "eval_total": len(evals),
            "eval_critical": sum(1 for item in evals if item.is_critical),
            "eval_unsupported_claim": unsupported_claim_count,
            "run_total": len(evaluation_runs),
        }
    )
    return snapshot


def _query_rows_for_label(session: Session, label: str, dataset: str | None) -> list[Evaluation]:
    stmt = select(Evaluation).join(EvaluationRun, EvaluationRun.id == Evaluation.run_id).where(EvaluationRun.run_label == label)
    if dataset:
        stmt = stmt.where(EvaluationRun.dataset_name == dataset)
    return list(session.scalars(stmt).all())


def _query_assertions(rows: list[Evaluation]) -> tuple[int, int]:
    pass_count = 0
    fail_count = 0
    for row in rows:
        assertion = loads_json(row.assertion_result, {})
        if assertion.get("passed") is True:
            pass_count += 1
        elif assertion:
            fail_count += 1
    return pass_count, fail_count


def _failure_breakdown(rows: list[Evaluation]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        for failure in loads_json(row.failure_types, []):
            counter[failure] += 1
    return dict(counter)


@router.get("/version-compare")
def dashboard_version_compare(
    baseline: str,
    candidate: str,
    dataset: str | None = None,
    _: AdminUser = Depends(get_current_admin),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    started = time.perf_counter()

    baseline_rows = _query_rows_for_label(session, baseline, dataset)
    candidate_rows = _query_rows_for_label(session, candidate, dataset)

    def _avg(rows: list[Evaluation]) -> float:
        return round(sum(item.total_score for item in rows) / len(rows), 2) if rows else 0.0

    def _critical(rows: list[Evaluation]) -> int:
        return sum(1 for item in rows if item.is_critical)

    baseline_pass, baseline_fail = _query_assertions(baseline_rows)
    candidate_pass, candidate_fail = _query_assertions(candidate_rows)

    result = VersionCompareResult(
        baseline=baseline,
        candidate=candidate,
        dataset=dataset or "all",
        baseline_avg=_avg(baseline_rows),
        candidate_avg=_avg(candidate_rows),
        baseline_critical=_critical(baseline_rows),
        candidate_critical=_critical(candidate_rows),
        baseline_pass_count=baseline_pass,
        candidate_pass_count=candidate_pass,
        baseline_fail_count=baseline_fail,
        candidate_fail_count=candidate_fail,
        baseline_failures=_failure_breakdown(baseline_rows),
        candidate_failures=_failure_breakdown(candidate_rows),
        delta=round(_avg(candidate_rows) - _avg(baseline_rows), 2),
        pass_delta=candidate_pass - baseline_pass,
        fail_delta=candidate_fail - baseline_fail,
        critical_delta=_critical(candidate_rows) - _critical(baseline_rows),
    )

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    get_stats_store().record_version_compare(elapsed_ms)
    return {"result": result.to_dict()}
