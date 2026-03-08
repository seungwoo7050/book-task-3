from __future__ import annotations

import json
from typing import Any

import httpx

from core.config import load_settings
from core.errors import DependencyUnavailableError


def _parse_json_response(content: str) -> dict[str, Any]:
    stripped = content.strip()
    if not stripped:
        raise ValueError("empty ollama response")
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        parsed = json.loads(stripped[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("ollama json response is not an object")
    return parsed


def _request_chat(payload: dict[str, Any], timeout: float | None = None) -> dict[str, Any]:
    settings = load_settings()
    effective_timeout = timeout if timeout is not None else settings.ollama_timeout_seconds
    try:
        with httpx.Client(timeout=effective_timeout) as client:
            response = client.post(f"{settings.ollama_base_url}/api/chat", json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as exc:
        raise DependencyUnavailableError("ollama", f"Ollama request failed: {exc}") from exc


def chat_with_ollama(system_prompt: str, user_prompt: str) -> dict[str, Any] | None:
    settings = load_settings()
    if not settings.enable_ollama:
        return None

    payload = {
        "model": settings.ollama_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {"temperature": 0, "seed": 42},
    }

    try:
        return _request_chat(payload)
    except DependencyUnavailableError:
        return None


def chat_json_with_ollama(
    *,
    model: str | None,
    system_prompt: str,
    user_prompt: str,
    retries: int = 1,
    timeout: float | None = None,
) -> dict[str, Any]:
    settings = load_settings()
    if not settings.enable_ollama:
        raise DependencyUnavailableError("ollama", "QUALBOT_ENABLE_OLLAMA=1 is required in llm mode")
    if not model:
        raise DependencyUnavailableError("ollama", "Missing required Ollama model env for evaluator")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0, "seed": 42},
    }

    last_error: Exception | None = None
    for _ in range(max(1, retries + 1)):
        result = _request_chat(payload, timeout=timeout)
        content = str(result.get("message", {}).get("content", "")).strip()
        try:
            return _parse_json_response(content)
        except Exception as exc:  # noqa: BLE001
            last_error = exc

    raise DependencyUnavailableError("ollama", f"Ollama JSON parse failed: {last_error}")
