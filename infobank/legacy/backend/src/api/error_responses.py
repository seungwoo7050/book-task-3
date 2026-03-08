from __future__ import annotations

from core.errors import DependencyUnavailableError
from fastapi.responses import JSONResponse


def dependency_unavailable_response(exc: DependencyUnavailableError) -> JSONResponse:
    return JSONResponse(status_code=503, content=exc.to_dict())
