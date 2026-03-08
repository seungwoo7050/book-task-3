from __future__ import annotations

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=3)


class ChatRequest(BaseModel):
    user_message: str = Field(min_length=1)
    conversation_id: str | None = None
    prompt_version: str | None = None
    kb_version: str | None = None
    kb_bundle_id: str | None = None


class EvaluateTurnRequest(BaseModel):
    evaluator_version: str | None = None
    prompt_version: str | None = None
    kb_version: str | None = None
    retrieval_version: str | None = None
    allow_cache: bool = True


class EvaluateBatchRequest(BaseModel):
    turn_ids: list[str] = Field(default_factory=list)
    evaluator_version: str | None = None
    prompt_version: str | None = None
    kb_version: str | None = None
    retrieval_version: str | None = None
    run_label: str | None = None
    dataset: str | None = None
    kb_bundle_id: str | None = None


class JobCreateRequest(BaseModel):
    dataset_id: str
    kb_bundle_id: str
    prompt_version: str | None = None
    kb_version: str | None = None
    evaluator_version: str | None = None
    retrieval_version: str | None = None
    run_label: str | None = None
    baseline_label: str | None = None
    candidate_label: str | None = None


class GoldenSetRunRequest(BaseModel):
    evaluator_version: str | None = None
    prompt_version: str | None = None
    kb_version: str | None = None
    retrieval_version: str | None = None
    run_label: str | None = None
    dataset: str | None = None
    baseline_label: str | None = None
    candidate_label: str | None = None
    limit: int | None = None


class GoldenSetCreateRequest(BaseModel):
    id: str
    category: str
    user_message: str
    expected_failure_types: list[str] = Field(default_factory=list)
    required_evidence_doc_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
