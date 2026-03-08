from __future__ import annotations

import time
import uuid
from datetime import UTC, datetime

from core.config import load_settings
from core.errors import DependencyUnavailableError
from core.json_utils import dumps_json, loads_json
from core.types import EvidenceResult, LLMJudgment
from db.models import Conversation, Evaluation, RuleViolation, Turn
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from evaluator.claim_extractor import extract_claims
from evaluator.evidence_verifier import verify_claims
from evaluator.llm_judge import judge_response
from evaluator.pipeline_stats import get_stats_store
from evaluator.rule_eval import evaluate_rules, has_critical_rule
from evaluator.scorer import compute_score


class EvaluationPipeline:
    def __init__(self, session: Session):
        self.session = session
        try:
            self.settings = load_settings()
        except ValueError as exc:
            raise DependencyUnavailableError("runtime", str(exc)) from exc
        self.stats = get_stats_store()

    def _existing_evaluation(self, turn_id: str, evaluator_version: str, prompt_version: str, kb_version: str) -> Evaluation | None:
        stmt = select(Evaluation).where(
            Evaluation.turn_id == turn_id,
            Evaluation.evaluator_version == evaluator_version,
            Evaluation.prompt_version == prompt_version,
            Evaluation.kb_version == kb_version,
        )
        return self.session.scalar(stmt)

    def evaluate_turn(
        self,
        turn_id: str,
        *,
        evaluator_version: str | None = None,
        prompt_version: str | None = None,
        kb_version: str | None = None,
        allow_cache: bool = True,
    ) -> Evaluation:
        evaluator_version = evaluator_version or self.settings.evaluator_version
        prompt_version = prompt_version or self.settings.prompt_version
        kb_version = kb_version or self.settings.kb_version

        try:
            if self.settings.eval_mode == "llm":
                if self.settings.dependency_failure_policy != "strict":
                    raise DependencyUnavailableError(
                        "runtime",
                        "llm mode requires QUALBOT_DEPENDENCY_FAILURE_POLICY=strict",
                    )
                if not self.settings.enable_ollama:
                    raise DependencyUnavailableError("ollama", "QUALBOT_ENABLE_OLLAMA=1 is required in llm mode")
                if not self.settings.enable_chroma:
                    raise DependencyUnavailableError("chroma", "QUALBOT_ENABLE_CHROMA=1 is required in llm mode")
                if self.settings.retrieval_backend != "chroma":
                    raise DependencyUnavailableError("chroma", "llm mode requires QUALBOT_RETRIEVAL_BACKEND=chroma")
                if not self.settings.ollama_judge_model:
                    raise DependencyUnavailableError("ollama", "QUALBOT_OLLAMA_JUDGE_MODEL is required in llm mode")
                if not self.settings.ollama_claim_model:
                    raise DependencyUnavailableError("ollama", "QUALBOT_OLLAMA_CLAIM_MODEL is required in llm mode")
                if not self.settings.ollama_evidence_model:
                    raise DependencyUnavailableError("ollama", "QUALBOT_OLLAMA_EVIDENCE_MODEL is required in llm mode")
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
            cached = self._existing_evaluation(turn_id, evaluator_version, prompt_version, kb_version)
            if cached is not None:
                self.stats.record_cache_hit()
                return cached

        turn = self.session.get(Turn, turn_id)
        if turn is None:
            raise ValueError(f"turn not found: {turn_id}")

        started = time.perf_counter()
        short_circuit = False
        short_circuit_reason: str | None = None

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
                )
            else:
                claims = extract_claims(turn.assistant_response)
                evidence_result = verify_claims(self.session, claims, top_k=3)
                if evidence_result.has_contradiction:
                    short_circuit = True
                    short_circuit_reason = "evidence_contradiction"
                llm_judgment = judge_response(
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
        judge_model = self.settings.ollama_judge_model if self.settings.eval_mode == "llm" else "heuristic-judge"
        model_name = judge_model if judge_model else "n/a"

        evidence_payload = evidence_result.to_dict()
        evidence_payload["meta"] = {
            "short_circuit": short_circuit,
            "short_circuit_reason": short_circuit_reason,
        }

        evaluation = Evaluation(
            id=str(uuid.uuid4()),
            turn_id=turn.id,
            evaluator_version=evaluator_version,
            model_name=model_name,
            prompt_version=prompt_version,
            kb_version=kb_version,
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

        # Flush newly inserted evaluation rows before conversation aggregate query.
        self.session.flush()
        self._refresh_conversation_score(turn.conversation_id)

        elapsed_ms = int((time.perf_counter() - started) * 1000)
        self.stats.record_eval(
            eval_ms=elapsed_ms,
            judge_ms=llm_judgment.judge_ms,
            retrieval_hit_at_k=evidence_result.retrieval_hit_at_k,
            short_circuit=short_circuit,
            judge_model=self.settings.ollama_judge_model or "heuristic-judge",
            claim_model=self.settings.ollama_claim_model or "heuristic-claim",
            evidence_model=self.settings.ollama_evidence_model or "heuristic-evidence",
            retrieval_backend=self.settings.retrieval_backend,
        )

        return evaluation

    def evaluate_conversation(self, conversation_id: str) -> list[Evaluation]:
        stmt = select(Turn.id).where(Turn.conversation_id == conversation_id).order_by(Turn.turn_index.asc())
        turn_ids = list(self.session.scalars(stmt).all())
        return [self.evaluate_turn(turn_id, allow_cache=False) for turn_id in turn_ids]

    def evaluate_turn_ids(self, turn_ids: list[str]) -> list[Evaluation]:
        return [self.evaluate_turn(turn_id, allow_cache=False) for turn_id in turn_ids]

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
        "evaluator_version": evaluation.evaluator_version,
        "model_name": evaluation.model_name,
        "prompt_version": evaluation.prompt_version,
        "kb_version": evaluation.kb_version,
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
        "explanation": evaluation.explanation,
        "created_at": evaluation.created_at.isoformat(),
    }
