from __future__ import annotations

import time
import uuid
from datetime import UTC, datetime
from typing import Any

from core.config import load_settings
from core.errors import DependencyUnavailableError
from core.json_utils import dumps_json, loads_json
from core.langfuse_trace import create_trace_envelope
from core.types import EvidenceResult, LineageRecord, LLMJudgment, ProviderAttempt
from db.models import Conversation, Evaluation, EvaluationRun, RuleViolation, Turn
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from evaluator.claim_extractor import extract_claims_with_trace
from evaluator.evidence_verifier import verify_claims_with_trace
from evaluator.llm_judge import judge_response_with_trace
from evaluator.pipeline_stats import get_stats_store
from evaluator.rule_eval import evaluate_rules, has_critical_rule
from evaluator.scorer import compute_score


def _first_success_model(attempts: list[ProviderAttempt], fallback: str) -> str:
    for attempt in attempts:
        if attempt.succeeded and attempt.model:
            return attempt.model
    return fallback


def _lineage_payload(run: EvaluationRun | None, defaults: LineageRecord | None) -> dict[str, Any]:
    if run is not None:
        return {
            "trace_id": run.trace_id,
            "lineage_id": run.lineage_id,
            "run_id": run.id,
            "run_label": run.run_label,
            "dataset": run.dataset_name,
            "evaluator_version": run.evaluator_version,
            "prompt_version": run.prompt_version,
            "kb_version": run.kb_version,
            "retrieval_version": run.retrieval_version,
        }
    if defaults is not None:
        return defaults.to_dict()
    return {}


class EvaluationPipeline:
    def __init__(self, session: Session):
        self.session = session
        try:
            self.settings = load_settings()
        except ValueError as exc:
            raise DependencyUnavailableError("runtime", str(exc)) from exc
        self.stats = get_stats_store()

    def _existing_evaluation(
        self,
        turn_id: str,
        evaluator_version: str,
        prompt_version: str,
        kb_version: str,
        retrieval_version: str,
    ) -> Evaluation | None:
        stmt = select(Evaluation).where(
            Evaluation.turn_id == turn_id,
            Evaluation.evaluator_version == evaluator_version,
            Evaluation.prompt_version == prompt_version,
            Evaluation.kb_version == kb_version,
            Evaluation.retrieval_version == retrieval_version,
        )
        return self.session.scalar(stmt)

    def evaluate_turn(
        self,
        turn_id: str,
        *,
        evaluator_version: str | None = None,
        prompt_version: str | None = None,
        kb_version: str | None = None,
        retrieval_version: str | None = None,
        run: EvaluationRun | None = None,
        allow_cache: bool = True,
    ) -> Evaluation:
        evaluator_version = evaluator_version or self.settings.evaluator_version
        prompt_version = prompt_version or self.settings.prompt_version
        kb_version = kb_version or self.settings.kb_version
        retrieval_version = retrieval_version or self.settings.retrieval_version

        try:
            if self.settings.eval_mode == "llm":
                if self.settings.dependency_failure_policy != "strict":
                    raise DependencyUnavailableError(
                        "runtime",
                        "llm mode requires QUALBOT_DEPENDENCY_FAILURE_POLICY=strict",
                    )
                if not self.settings.enable_chroma:
                    raise DependencyUnavailableError("chroma", "QUALBOT_ENABLE_CHROMA=1 is required in llm mode")
                if self.settings.retrieval_backend != "chroma":
                    raise DependencyUnavailableError("chroma", "llm mode requires QUALBOT_RETRIEVAL_BACKEND=chroma")
                if not self.settings.chroma_persist_dir or not self.settings.chroma_collection:
                    raise DependencyUnavailableError(
                        "chroma",
                        "QUALBOT_CHROMA_PERSIST_DIR and QUALBOT_CHROMA_COLLECTION are required in llm mode",
                    )
            elif self.settings.eval_mode != "heuristic":
                raise DependencyUnavailableError("runtime", f"unsupported eval mode: {self.settings.eval_mode}")
        except DependencyUnavailableError:
            self.stats.record_dependency_failure()
            raise

        if allow_cache:
            cached = self._existing_evaluation(turn_id, evaluator_version, prompt_version, kb_version, retrieval_version)
            if cached is not None:
                self.stats.record_cache_hit()
                return cached

        turn = self.session.get(Turn, turn_id)
        if turn is None:
            raise ValueError(f"turn not found: {turn_id}")

        started = time.perf_counter()
        short_circuit = False
        short_circuit_reason: str | None = None
        claim_attempts: list[ProviderAttempt] = []
        evidence_attempts: list[ProviderAttempt] = []
        judge_attempts: list[ProviderAttempt] = []
        claims: list[Any] = []

        try:
            rule_results = evaluate_rules(
                user_message=turn.user_message,
                assistant_response=turn.assistant_response,
                rules_dir="backend/rules",
            )

            if has_critical_rule(rule_results):
                short_circuit = True
                short_circuit_reason = "critical_rule"
                evidence_result = EvidenceResult(groundedness_score=0.0, has_contradiction=False, retrieval_hit_at_k=0.0)
                llm_judgment = LLMJudgment(
                    correctness=0.0,
                    resolution=0.0,
                    communication=0.0,
                    escalation_needed=True,
                    failure_types=[item.failure_type for item in rule_results],
                    explanation="Critical rule violation short-circuit",
                    judge_ms=0,
                    provider="heuristic",
                    model="critical-short-circuit",
                )
            else:
                claims, claim_attempts = extract_claims_with_trace(turn.assistant_response)
                evidence_result, evidence_attempts = verify_claims_with_trace(self.session, claims, top_k=3)
                if evidence_result.has_contradiction:
                    short_circuit = True
                    short_circuit_reason = "evidence_contradiction"
                llm_judgment, judge_attempts = judge_response_with_trace(
                    user_message=turn.user_message,
                    assistant_response=turn.assistant_response,
                    rule_results=rule_results,
                    evidence_result=evidence_result,
                )
        except DependencyUnavailableError:
            self.stats.record_dependency_failure()
            raise
        except ValueError as exc:
            self.stats.record_dependency_failure()
            raise DependencyUnavailableError("runtime", str(exc)) from exc

        score = compute_score(rule_results, evidence_result, llm_judgment)
        model_name = f"{llm_judgment.provider}:{llm_judgment.model}"

        evidence_payload = evidence_result.to_dict()
        evidence_payload["meta"] = {
            "short_circuit": short_circuit,
            "short_circuit_reason": short_circuit_reason,
        }

        ephemeral_lineage = None
        if run is None:
            envelope = create_trace_envelope(
                self.settings,
                run_label=self.settings.run_label,
                dataset=self.settings.dataset_name,
                metadata={
                    "evaluator_version": evaluator_version,
                    "prompt_version": prompt_version,
                    "kb_version": kb_version,
                    "retrieval_version": retrieval_version,
                },
            )
            ephemeral_lineage = LineageRecord(
                trace_id=envelope.trace_id,
                lineage_id=envelope.lineage_id,
                run_id="",
                run_label=envelope.run_label,
                dataset=envelope.dataset,
                evaluator_version=evaluator_version,
                prompt_version=prompt_version,
                kb_version=kb_version,
                retrieval_version=retrieval_version,
            )

        retrieval_trace = [
            item.retrieval_trace.to_dict()
            for item in evidence_result.claim_results
            if item.retrieval_trace is not None
        ]
        claim_trace = [claim.to_dict() for claim in claims]
        provider_trace = [attempt.to_dict() for attempt in (claim_attempts + evidence_attempts + judge_attempts)]
        judge_trace = {
            "provider": llm_judgment.provider,
            "model": llm_judgment.model,
            "judge_ms": llm_judgment.judge_ms,
            "short_circuit": short_circuit,
            "short_circuit_reason": short_circuit_reason,
            "failure_types": llm_judgment.failure_types,
        }

        evaluation = Evaluation(
            id=str(uuid.uuid4()),
            turn_id=turn.id,
            run_id=run.id if run is not None else None,
            evaluator_version=evaluator_version,
            model_name=model_name,
            prompt_version=prompt_version,
            kb_version=kb_version,
            retrieval_version=retrieval_version,
            correctness_score=score.correctness,
            groundedness_score=score.groundedness,
            compliance_score=score.compliance,
            resolution_score=score.resolution,
            communication_score=score.communication,
            total_score=score.total,
            grade=score.grade,
            failure_types=dumps_json(score.failure_types),
            is_critical=score.is_critical,
            rule_results=dumps_json([item.to_dict() for item in rule_results]),
            evidence_results=dumps_json(evidence_payload),
            llm_judgment=dumps_json(llm_judgment.to_dict()),
            lineage_json=dumps_json(_lineage_payload(run, ephemeral_lineage)),
            provider_trace=dumps_json(provider_trace),
            retrieval_trace=dumps_json(retrieval_trace),
            claim_trace=dumps_json(claim_trace),
            judge_trace=dumps_json(judge_trace),
            explanation=score.explanation,
            created_at=datetime.now(UTC),
        )
        self.session.add(evaluation)

        for item in rule_results:
            self.session.add(
                RuleViolation(
                    turn_id=turn.id,
                    rule_id=item.rule_id,
                    severity=item.severity,
                    failure_type=item.failure_type,
                    evidence=item.evidence,
                )
            )

        self.session.flush()
        self._refresh_conversation_score(turn.conversation_id)

        elapsed_ms = int((time.perf_counter() - started) * 1000)
        self.stats.record_eval(
            eval_ms=elapsed_ms,
            judge_ms=llm_judgment.judge_ms,
            retrieval_hit_at_k=evidence_result.retrieval_hit_at_k,
            short_circuit=short_circuit,
            judge_model=llm_judgment.model,
            claim_model=_first_success_model(claim_attempts, "heuristic-claim"),
            evidence_model=_first_success_model(evidence_attempts, "heuristic-evidence"),
            retrieval_backend=self.settings.retrieval_backend,
        )

        return evaluation

    def evaluate_conversation(
        self,
        conversation_id: str,
        *,
        run: EvaluationRun | None = None,
        retrieval_version: str | None = None,
    ) -> list[Evaluation]:
        stmt = select(Turn.id).where(Turn.conversation_id == conversation_id).order_by(Turn.turn_index.asc())
        turn_ids = list(self.session.scalars(stmt).all())
        return [
            self.evaluate_turn(turn_id, allow_cache=False, run=run, retrieval_version=retrieval_version)
            for turn_id in turn_ids
        ]

    def evaluate_turn_ids(
        self,
        turn_ids: list[str],
        *,
        run: EvaluationRun | None = None,
        retrieval_version: str | None = None,
    ) -> list[Evaluation]:
        return [
            self.evaluate_turn(turn_id, allow_cache=False, run=run, retrieval_version=retrieval_version)
            for turn_id in turn_ids
        ]

    def _refresh_conversation_score(self, conversation_id: str) -> None:
        conv = self.session.get(Conversation, conversation_id)
        if conv is None:
            return

        stmt = (
            select(func.avg(Evaluation.total_score), func.count(Evaluation.id))
            .join(Turn, Turn.id == Evaluation.turn_id)
            .where(Turn.conversation_id == conversation_id)
        )
        avg_score, count = self.session.execute(stmt).one()
        if count:
            conv.session_score = round(float(avg_score or 0.0), 2)
            if conv.session_score >= 90:
                conv.session_grade = "A"
            elif conv.session_score >= 75:
                conv.session_grade = "B"
            elif conv.session_score >= 60:
                conv.session_grade = "C"
            elif conv.session_score >= 40:
                conv.session_grade = "D"
            else:
                conv.session_grade = "F"


def serialize_evaluation(evaluation: Evaluation) -> dict[str, object]:
    return {
        "id": evaluation.id,
        "turn_id": evaluation.turn_id,
        "run_id": evaluation.run_id,
        "evaluator_version": evaluation.evaluator_version,
        "model_name": evaluation.model_name,
        "prompt_version": evaluation.prompt_version,
        "kb_version": evaluation.kb_version,
        "retrieval_version": evaluation.retrieval_version,
        "correctness_score": evaluation.correctness_score,
        "groundedness_score": evaluation.groundedness_score,
        "compliance_score": evaluation.compliance_score,
        "resolution_score": evaluation.resolution_score,
        "communication_score": evaluation.communication_score,
        "total_score": evaluation.total_score,
        "grade": evaluation.grade,
        "failure_types": loads_json(evaluation.failure_types, []),
        "is_critical": evaluation.is_critical,
        "rule_results": loads_json(evaluation.rule_results, []),
        "evidence_results": loads_json(evaluation.evidence_results, {}),
        "llm_judgment": loads_json(evaluation.llm_judgment, {}),
        "lineage": loads_json(evaluation.lineage_json, {}),
        "provider_trace": loads_json(evaluation.provider_trace, []),
        "retrieval_trace": loads_json(evaluation.retrieval_trace, []),
        "claim_trace": loads_json(evaluation.claim_trace, []),
        "judge_trace": loads_json(evaluation.judge_trace, {}),
        "assertion_result": loads_json(evaluation.assertion_result, {}),
        "explanation": evaluation.explanation,
        "created_at": evaluation.created_at.isoformat(),
    }
