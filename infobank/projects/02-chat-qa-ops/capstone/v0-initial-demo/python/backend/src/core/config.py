from __future__ import annotations

import os
from dataclasses import dataclass

VALID_EVAL_MODES = {"llm", "heuristic"}
VALID_RETRIEVAL_BACKENDS = {"chroma", "keyword"}
VALID_DEPENDENCY_POLICIES = {"strict"}


@dataclass(frozen=True)
class Settings:
    db_url: str
    ollama_base_url: str
    ollama_model: str
    ollama_timeout_seconds: float
    enable_ollama: bool
    enable_chroma: bool
    eval_mode: str
    retrieval_backend: str
    ollama_judge_model: str | None
    ollama_claim_model: str | None
    ollama_evidence_model: str | None
    chroma_persist_dir: str | None
    chroma_collection: str | None
    dependency_failure_policy: str
    prompt_version: str
    kb_version: str
    evaluator_version: str
    api_host: str
    api_port: int


def _validate_enum(name: str, value: str, allowed: set[str]) -> str:
    normalized = value.strip().lower()
    if normalized not in allowed:
        allowed_text = ", ".join(sorted(allowed))
        raise ValueError(f"{name} must be one of [{allowed_text}], got '{value}'")
    return normalized



def load_settings() -> Settings:
    eval_mode = _validate_enum("QUALBOT_EVAL_MODE", os.getenv("QUALBOT_EVAL_MODE", "llm"), VALID_EVAL_MODES)
    retrieval_backend = _validate_enum(
        "QUALBOT_RETRIEVAL_BACKEND",
        os.getenv("QUALBOT_RETRIEVAL_BACKEND", "chroma"),
        VALID_RETRIEVAL_BACKENDS,
    )
    dependency_failure_policy = _validate_enum(
        "QUALBOT_DEPENDENCY_FAILURE_POLICY",
        os.getenv("QUALBOT_DEPENDENCY_FAILURE_POLICY", "strict"),
        VALID_DEPENDENCY_POLICIES,
    )

    return Settings(
        db_url=os.getenv("QUALBOT_DB_URL", "sqlite:///./backend/data/qualbot.db"),
        ollama_base_url=os.getenv("QUALBOT_OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("QUALBOT_OLLAMA_MODEL", "qwen2.5:7b"),
        ollama_timeout_seconds=float(os.getenv("QUALBOT_OLLAMA_TIMEOUT_SECONDS", "90")),
        enable_ollama=os.getenv("QUALBOT_ENABLE_OLLAMA", "0") == "1",
        enable_chroma=os.getenv("QUALBOT_ENABLE_CHROMA", "0") == "1",
        eval_mode=eval_mode,
        retrieval_backend=retrieval_backend,
        ollama_judge_model=os.getenv("QUALBOT_OLLAMA_JUDGE_MODEL"),
        ollama_claim_model=os.getenv("QUALBOT_OLLAMA_CLAIM_MODEL"),
        ollama_evidence_model=os.getenv("QUALBOT_OLLAMA_EVIDENCE_MODEL"),
        chroma_persist_dir=os.getenv("QUALBOT_CHROMA_PERSIST_DIR", "backend/data/chroma"),
        chroma_collection=os.getenv("QUALBOT_CHROMA_COLLECTION", "qualbot-kb"),
        dependency_failure_policy=dependency_failure_policy,
        prompt_version=os.getenv("QUALBOT_PROMPT_VERSION", "v1.0"),
        kb_version=os.getenv("QUALBOT_KB_VERSION", "v1.0"),
        evaluator_version=os.getenv("QUALBOT_EVALUATOR_VERSION", "eval-v1"),
        api_host=os.getenv("QUALBOT_API_HOST", "0.0.0.0"),
        api_port=int(os.getenv("QUALBOT_API_PORT", "8000")),
    )
