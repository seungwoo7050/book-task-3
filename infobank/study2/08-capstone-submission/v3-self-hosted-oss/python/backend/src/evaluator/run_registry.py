from __future__ import annotations

import uuid

from core.config import Settings, load_settings
from core.json_utils import dumps_json
from core.langfuse_trace import create_trace_envelope
from core.types import LineageRecord
from db.models import EvaluationRun
from sqlalchemy.orm import Session


def create_evaluation_run(
    session: Session,
    *,
    job_id: str | None = None,
    batch_id: str | None = None,
    kb_bundle_id: str | None = None,
    run_label: str | None = None,
    dataset_name: str | None = None,
    baseline_label: str | None = None,
    candidate_label: str | None = None,
    prompt_version: str | None = None,
    kb_version: str | None = None,
    evaluator_version: str | None = None,
    retrieval_version: str | None = None,
    settings: Settings | None = None,
) -> EvaluationRun:
    current = settings or load_settings()
    effective_run_label = run_label or current.run_label
    effective_dataset = dataset_name or current.dataset_name
    effective_prompt = prompt_version or current.prompt_version
    effective_kb = kb_version or current.kb_version
    effective_eval = evaluator_version or current.evaluator_version
    effective_retrieval = retrieval_version or current.retrieval_version
    envelope = create_trace_envelope(
        current,
        run_label=effective_run_label,
        dataset=effective_dataset,
        metadata={
            "baseline_label": baseline_label,
            "candidate_label": candidate_label,
            "prompt_version": effective_prompt,
            "kb_version": effective_kb,
            "evaluator_version": effective_eval,
            "retrieval_version": effective_retrieval,
        },
    )
    row = EvaluationRun(
        id=str(uuid.uuid4()),
        job_id=job_id,
        batch_id=batch_id,
        kb_bundle_id=kb_bundle_id,
        run_label=effective_run_label,
        dataset_name=effective_dataset,
        baseline_label=baseline_label,
        candidate_label=candidate_label,
        evaluator_version=effective_eval,
        prompt_version=effective_prompt,
        kb_version=effective_kb,
        retrieval_version=effective_retrieval,
        trace_id=envelope.trace_id,
        lineage_id=envelope.lineage_id,
        metadata_json=dumps_json(envelope.to_dict()),
    )
    session.add(row)
    session.flush()
    return row


def to_lineage_record(run: EvaluationRun) -> LineageRecord:
    return LineageRecord(
        trace_id=run.trace_id,
        lineage_id=run.lineage_id,
        run_id=run.id,
        run_label=run.run_label,
        dataset=run.dataset_name,
        evaluator_version=run.evaluator_version,
        prompt_version=run.prompt_version,
        kb_version=run.kb_version,
        retrieval_version=run.retrieval_version,
    )
