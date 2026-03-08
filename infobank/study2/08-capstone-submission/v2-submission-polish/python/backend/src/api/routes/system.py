from __future__ import annotations

from core.config import load_settings
from core.dependency_health import collect_dependency_health, require_llm_strict_dependencies
from core.errors import DependencyUnavailableError
from evaluator.pipeline_stats import get_stats_store
from fastapi import APIRouter

from api.error_responses import dependency_unavailable_response

router = APIRouter(prefix="/api", tags=["system"])


@router.get("/system/pipeline-stats")
def pipeline_stats() -> dict[str, object]:
    return get_stats_store().snapshot().to_dict()


@router.get("/system/dependency-health")
def dependency_health() -> dict[str, object]:
    try:
        settings = load_settings()
        health = collect_dependency_health(settings)
        require_llm_strict_dependencies(health)
        return health.to_dict()
    except ValueError as exc:
        return dependency_unavailable_response(DependencyUnavailableError("runtime", str(exc)))  # type: ignore[return-value]
    except DependencyUnavailableError as exc:
        return dependency_unavailable_response(exc)  # type: ignore[return-value]
