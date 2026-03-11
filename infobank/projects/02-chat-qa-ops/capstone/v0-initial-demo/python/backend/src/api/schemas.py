from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_message: str = Field(min_length=1)
    conversation_id: str | None = None
    prompt_version: str | None = None
    kb_version: str | None = None


class EvaluateTurnRequest(BaseModel):
    evaluator_version: str | None = None
    prompt_version: str | None = None
    kb_version: str | None = None
    allow_cache: bool = True


class EvaluateBatchRequest(BaseModel):
    turn_ids: list[str] = Field(default_factory=list)
    evaluator_version: str | None = None
    prompt_version: str | None = None
    kb_version: str | None = None


class GoldenSetRunRequest(BaseModel):
    evaluator_version: str | None = None
    prompt_version: str | None = None
    kb_version: str | None = None
    limit: int | None = None


class GoldenSetCreateRequest(BaseModel):
    id: str
    category: str
    user_message: str
    expected_failure_types: list[str] = Field(default_factory=list)
    required_evidence_doc_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
