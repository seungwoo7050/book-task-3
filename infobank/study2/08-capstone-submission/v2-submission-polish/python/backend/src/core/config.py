from __future__ import annotations

import os
from dataclasses import dataclass

VALID_EVAL_MODES = {"llm", "heuristic"}
VALID_RETRIEVAL_BACKENDS = {"chroma", "keyword"}
VALID_DEPENDENCY_POLICIES = {"strict"}
VALID_PROVIDER_NAMES = {"upstage", "openai", "ollama"}


@dataclass(frozen=True)
class Settings:
    db_url: str
    provider_chain: tuple[str, ...]
    provider_timeout_seconds: float
    upstage_api_key: str | None
    upstage_base_url: str
    upstage_model: str | None
    openai_api_key: str | None
    openai_base_url: str
    openai_model: str | None
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
    retrieval_version: str
    run_label: str
    dataset_name: str
    langfuse_enabled: bool
    langfuse_host: str | None
    langfuse_public_key: str | None
    langfuse_secret_key: str | None
    api_host: str
    api_port: int


def _validate_enum(name: str, value: str, allowed: set[str]) -> str:
    normalized = value.strip().lower()
    if normalized not in allowed:
        allowed_text = ", ".join(sorted(allowed))
        raise ValueError(f"{name} must be one of [{allowed_text}], got '{value}'")
    return normalized


def _parse_provider_chain(raw: str) -> tuple[str, ...]:
    providers = []
    for token in raw.split(","):
        normalized = token.strip().lower()
        if not normalized:
            continue
        if normalized not in VALID_PROVIDER_NAMES:
            allowed_text = ", ".join(sorted(VALID_PROVIDER_NAMES))
            raise ValueError(f"QUALBOT_PROVIDER_CHAIN must use [{allowed_text}], got '{token}'")
        providers.append(normalized)
    if not providers:
        raise ValueError("QUALBOT_PROVIDER_CHAIN must contain at least one provider")
    return tuple(providers)


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
    provider_chain = _parse_provider_chain(os.getenv("QUALBOT_PROVIDER_CHAIN", "upstage,openai,ollama"))

    return Settings(
        db_url=os.getenv("QUALBOT_DB_URL", "sqlite:///./backend/data/qualbot.db"),
        provider_chain=provider_chain,
        provider_timeout_seconds=float(os.getenv("QUALBOT_PROVIDER_TIMEOUT_SECONDS", "30")),
        upstage_api_key=os.getenv("QUALBOT_UPSTAGE_API_KEY"),
        upstage_base_url=os.getenv("QUALBOT_UPSTAGE_BASE_URL", "https://api.upstage.ai/v1"),
        upstage_model=os.getenv("QUALBOT_UPSTAGE_MODEL", "solar-pro2"),
        openai_api_key=os.getenv("QUALBOT_OPENAI_API_KEY"),
        openai_base_url=os.getenv("QUALBOT_OPENAI_BASE_URL", "https://api.openai.com/v1"),
        openai_model=os.getenv("QUALBOT_OPENAI_MODEL", "gpt-4o-mini"),
        ollama_base_url=os.getenv("QUALBOT_OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("QUALBOT_OLLAMA_MODEL", "qwen2.5:7b"),
        ollama_timeout_seconds=float(os.getenv("QUALBOT_OLLAMA_TIMEOUT_SECONDS", "90")),
        enable_ollama=os.getenv("QUALBOT_ENABLE_OLLAMA", "0") == "1",
        enable_chroma=os.getenv("QUALBOT_ENABLE_CHROMA", "0") == "1",
        eval_mode=eval_mode,
        retrieval_backend=retrieval_backend,
        ollama_judge_model=os.getenv("QUALBOT_OLLAMA_JUDGE_MODEL", os.getenv("QUALBOT_OLLAMA_MODEL", "qwen2.5:7b")),
        ollama_claim_model=os.getenv("QUALBOT_OLLAMA_CLAIM_MODEL", os.getenv("QUALBOT_OLLAMA_MODEL", "qwen2.5:7b")),
        ollama_evidence_model=os.getenv(
            "QUALBOT_OLLAMA_EVIDENCE_MODEL",
            os.getenv("QUALBOT_OLLAMA_MODEL", "qwen2.5:7b"),
        ),
        chroma_persist_dir=os.getenv("QUALBOT_CHROMA_PERSIST_DIR", "backend/data/chroma"),
        chroma_collection=os.getenv("QUALBOT_CHROMA_COLLECTION", "qualbot-kb"),
        dependency_failure_policy=dependency_failure_policy,
        prompt_version=os.getenv("QUALBOT_PROMPT_VERSION", "v1.0"),
        kb_version=os.getenv("QUALBOT_KB_VERSION", "v1.0"),
        evaluator_version=os.getenv("QUALBOT_EVALUATOR_VERSION", "eval-v1"),
        retrieval_version=os.getenv("QUALBOT_RETRIEVAL_VERSION", "retrieval-v2"),
        run_label=os.getenv("QUALBOT_RUN_LABEL", "manual-run"),
        dataset_name=os.getenv("QUALBOT_DATASET_NAME", "golden-set"),
        langfuse_enabled=os.getenv("QUALBOT_LANGFUSE_ENABLED", "0") == "1",
        langfuse_host=os.getenv("QUALBOT_LANGFUSE_HOST"),
        langfuse_public_key=os.getenv("QUALBOT_LANGFUSE_PUBLIC_KEY"),
        langfuse_secret_key=os.getenv("QUALBOT_LANGFUSE_SECRET_KEY"),
        api_host=os.getenv("QUALBOT_API_HOST", "0.0.0.0"),
        api_port=int(os.getenv("QUALBOT_API_PORT", "8000")),
    )
