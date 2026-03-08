from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def utc_now() -> datetime:
    return datetime.now(UTC)


class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    run_label: Mapped[str] = mapped_column(String, nullable=False, index=True)
    dataset_name: Mapped[str] = mapped_column(String, nullable=False)
    baseline_label: Mapped[str | None] = mapped_column(String)
    candidate_label: Mapped[str | None] = mapped_column(String)
    evaluator_version: Mapped[str] = mapped_column(String, nullable=False)
    prompt_version: Mapped[str] = mapped_column(String, nullable=False)
    kb_version: Mapped[str] = mapped_column(String, nullable=False)
    retrieval_version: Mapped[str] = mapped_column(String, nullable=False)
    trace_id: Mapped[str] = mapped_column(String, nullable=False)
    lineage_id: Mapped[str] = mapped_column(String, nullable=False)
    metadata_json: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    run_id: Mapped[str | None] = mapped_column(String, ForeignKey("evaluation_runs.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    prompt_version: Mapped[str] = mapped_column(String, nullable=False)
    kb_version: Mapped[str] = mapped_column(String, nullable=False)
    session_score: Mapped[float | None] = mapped_column(Float)
    session_grade: Mapped[str | None] = mapped_column(String)


class Turn(Base):
    __tablename__ = "turns"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    conversation_id: Mapped[str] = mapped_column(String, ForeignKey("conversations.id"), nullable=False)
    turn_index: Mapped[int] = mapped_column(Integer, nullable=False)
    user_message: Mapped[str] = mapped_column(Text, nullable=False)
    assistant_response: Mapped[str] = mapped_column(Text, nullable=False)
    retrieved_doc_ids: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    turn_id: Mapped[str] = mapped_column(String, ForeignKey("turns.id"), nullable=False)
    run_id: Mapped[str | None] = mapped_column(String, ForeignKey("evaluation_runs.id"))
    evaluator_version: Mapped[str] = mapped_column(String, nullable=False)
    model_name: Mapped[str] = mapped_column(String, nullable=False)
    prompt_version: Mapped[str] = mapped_column(String, nullable=False)
    kb_version: Mapped[str] = mapped_column(String, nullable=False)
    retrieval_version: Mapped[str] = mapped_column(String, nullable=False)
    correctness_score: Mapped[float] = mapped_column(Float, nullable=False)
    groundedness_score: Mapped[float] = mapped_column(Float, nullable=False)
    compliance_score: Mapped[float] = mapped_column(Float, nullable=False)
    resolution_score: Mapped[float] = mapped_column(Float, nullable=False)
    communication_score: Mapped[float] = mapped_column(Float, nullable=False)
    total_score: Mapped[float] = mapped_column(Float, nullable=False)
    grade: Mapped[str] = mapped_column(String, nullable=False)
    failure_types: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    rule_results: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    evidence_results: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    llm_judgment: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    lineage_json: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    provider_trace: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    retrieval_trace: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    claim_trace: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    judge_trace: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    assertion_result: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    explanation: Mapped[str] = mapped_column(Text, default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class RuleViolation(Base):
    __tablename__ = "rule_violations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    turn_id: Mapped[str] = mapped_column(String, nullable=False)
    rule_id: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    failure_type: Mapped[str] = mapped_column(String, nullable=False)
    evidence: Mapped[str] = mapped_column(Text, default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)


class GoldenSet(Base):
    __tablename__ = "golden_set"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    category: Mapped[str] = mapped_column(String, nullable=False)
    user_message: Mapped[str] = mapped_column(Text, nullable=False)
    expected_config: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    tags: Mapped[str] = mapped_column(Text, default="[]", nullable=False)


class KnowledgeDoc(Base):
    __tablename__ = "knowledge_docs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
