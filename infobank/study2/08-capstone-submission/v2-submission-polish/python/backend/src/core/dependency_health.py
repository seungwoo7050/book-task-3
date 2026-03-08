from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import httpx

from core.config import Settings, load_settings
from core.errors import DependencyUnavailableError


@dataclass(frozen=True)
class DependencyHealth:
    eval_mode: str
    policy: str
    retrieval_backend: str
    provider_chain: list[str]
    upstage_configured: bool
    openai_configured: bool
    ollama_reachable: bool
    chroma_reachable: bool
    models_configured: bool
    langfuse_prepared: bool
    storage_backend: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _check_ollama_reachable(base_url: str) -> bool:
    try:
        with httpx.Client(timeout=2.0) as client:
            response = client.get(f"{base_url}/api/tags")
            response.raise_for_status()
            return True
    except Exception:  # noqa: BLE001
        return False


def _check_chroma_reachable(persist_dir: str | None, collection_name: str | None) -> bool:
    if not persist_dir or not collection_name:
        return False
    try:
        import chromadb
    except BaseException:
        return False

    try:
        client: Any = chromadb.PersistentClient(path=persist_dir)
        client.get_or_create_collection(name=collection_name)
        return True
    except BaseException:  # pragma: no cover - chroma rust panics bypass Exception
        return False


def collect_dependency_health(settings: Settings | None = None) -> DependencyHealth:
    current = settings or load_settings()
    models_configured = bool(
        current.ollama_judge_model and current.ollama_claim_model and current.ollama_evidence_model
    )
    chroma_reachable = False
    if current.retrieval_backend == "chroma" or current.eval_mode == "llm":
        chroma_reachable = _check_chroma_reachable(current.chroma_persist_dir, current.chroma_collection)
    return DependencyHealth(
        eval_mode=current.eval_mode,
        policy=current.dependency_failure_policy,
        retrieval_backend=current.retrieval_backend,
        provider_chain=list(current.provider_chain),
        upstage_configured=bool(current.upstage_api_key and current.upstage_model),
        openai_configured=bool(current.openai_api_key and current.openai_model),
        ollama_reachable=_check_ollama_reachable(current.ollama_base_url),
        chroma_reachable=chroma_reachable,
        models_configured=models_configured,
        langfuse_prepared=bool(
            current.langfuse_enabled and current.langfuse_host and current.langfuse_public_key and current.langfuse_secret_key
        ),
        storage_backend="postgresql" if current.db_url.startswith("postgresql") else "sqlite",
    )


def require_llm_strict_dependencies(health: DependencyHealth) -> None:
    if health.eval_mode != "llm":
        return
    if health.policy != "strict":
        raise DependencyUnavailableError("runtime", "llm mode requires QUALBOT_DEPENDENCY_FAILURE_POLICY=strict")
    if health.retrieval_backend != "chroma":
        raise DependencyUnavailableError("chroma", "llm mode requires QUALBOT_RETRIEVAL_BACKEND=chroma")
    if not health.models_configured:
        raise DependencyUnavailableError(
            "ollama",
            "llm mode requires QUALBOT_OLLAMA_JUDGE_MODEL/CLAIM_MODEL/EVIDENCE_MODEL",
        )
    if not (health.upstage_configured or health.openai_configured or health.ollama_reachable):
        raise DependencyUnavailableError(
            "provider",
            "Provider chain is unavailable: configure Upstage/OpenAI or enable reachable Ollama fallback",
        )
    if "ollama" in health.provider_chain and not health.ollama_reachable and not (
        health.upstage_configured or health.openai_configured
    ):
        raise DependencyUnavailableError("ollama", "Ollama is not reachable")
    if not health.chroma_reachable:
        raise DependencyUnavailableError("chroma", "Chroma is not reachable")
