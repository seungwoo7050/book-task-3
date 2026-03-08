from __future__ import annotations

import json
import time
from typing import Any

import httpx

from core.config import Settings, load_settings
from core.errors import DependencyUnavailableError
from core.ollama import _parse_json_response, _request_chat
from core.types import ProviderAttempt


class ProviderChain:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or load_settings()

    def generate_text(self, *, system_prompt: str, user_prompt: str) -> tuple[str, list[ProviderAttempt]]:
        attempts: list[ProviderAttempt] = []
        for provider in self.settings.provider_chain:
            text, attempt = self._generate(provider, system_prompt=system_prompt, user_prompt=user_prompt, want_json=False)
            attempts.append(attempt)
            if isinstance(text, str):
                return text, attempts
        raise DependencyUnavailableError("provider", self._build_error_message(attempts, "text"))

    def generate_json(self, *, system_prompt: str, user_prompt: str, model_hint: str | None = None) -> tuple[dict[str, Any], list[ProviderAttempt]]:
        attempts: list[ProviderAttempt] = []
        for provider in self.settings.provider_chain:
            payload, attempt = self._generate(
                provider,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                want_json=True,
                model_hint=model_hint,
            )
            attempts.append(attempt)
            if isinstance(payload, dict):
                return payload, attempts
        raise DependencyUnavailableError("provider", self._build_error_message(attempts, "json"))

    def _build_error_message(self, attempts: list[ProviderAttempt], mode: str) -> str:
        if not attempts:
            return f"No provider configured for {mode} generation"
        joined = ", ".join(
            f"{attempt.provider}:{attempt.error or 'unknown error'}"
            for attempt in attempts
        )
        return f"Provider chain failed for {mode} generation: {joined}"

    def _generate(
        self,
        provider: str,
        *,
        system_prompt: str,
        user_prompt: str,
        want_json: bool,
        model_hint: str | None = None,
    ) -> tuple[str | dict[str, Any] | None, ProviderAttempt]:
        started = time.perf_counter()
        try:
            if provider == "upstage":
                model = model_hint or self.settings.upstage_model
                payload = self._request_openai_compatible(
                    provider="upstage",
                    base_url=self.settings.upstage_base_url,
                    api_key=self.settings.upstage_api_key,
                    model=model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    want_json=want_json,
                )
            elif provider == "openai":
                model = model_hint or self.settings.openai_model
                payload = self._request_openai_compatible(
                    provider="openai",
                    base_url=self.settings.openai_base_url,
                    api_key=self.settings.openai_api_key,
                    model=model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    want_json=want_json,
                )
            elif provider == "ollama":
                model = model_hint or self.settings.ollama_model
                payload = self._request_ollama(
                    model=model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    want_json=want_json,
                )
            else:  # pragma: no cover - guarded by config parser
                raise DependencyUnavailableError("provider", f"Unsupported provider: {provider}")
            latency_ms = int((time.perf_counter() - started) * 1000)
            return payload, ProviderAttempt(
                provider=provider,
                model=model_hint or self._model_for(provider),
                mode="json" if want_json else "text",
                succeeded=True,
                latency_ms=latency_ms,
            )
        except DependencyUnavailableError as exc:
            latency_ms = int((time.perf_counter() - started) * 1000)
            return None, ProviderAttempt(
                provider=provider,
                model=model_hint or self._model_for(provider),
                mode="json" if want_json else "text",
                succeeded=False,
                latency_ms=latency_ms,
                error=exc.message,
            )

    def _model_for(self, provider: str) -> str | None:
        if provider == "upstage":
            return self.settings.upstage_model
        if provider == "openai":
            return self.settings.openai_model
        if provider == "ollama":
            return self.settings.ollama_model
        return None

    def _request_openai_compatible(
        self,
        *,
        provider: str,
        base_url: str,
        api_key: str | None,
        model: str | None,
        system_prompt: str,
        user_prompt: str,
        want_json: bool,
    ) -> str | dict[str, Any]:
        if not api_key:
            raise DependencyUnavailableError(provider, f"{provider} API key is not configured")
        if not model:
            raise DependencyUnavailableError(provider, f"{provider} model is not configured")
        url = base_url.rstrip("/") + "/chat/completions"
        body: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        }
        if want_json:
            body["response_format"] = {"type": "json_object"}
        try:
            with httpx.Client(timeout=self.settings.provider_timeout_seconds) as client:
                response = client.post(
                    url,
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json=body,
                )
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPError as exc:
            raise DependencyUnavailableError(provider, f"{provider} request failed: {exc}") from exc

        try:
            content = str(payload["choices"][0]["message"]["content"]).strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise DependencyUnavailableError(provider, f"{provider} response schema is invalid") from exc
        if want_json:
            try:
                return _parse_json_response(content)
            except Exception as exc:  # noqa: BLE001
                raise DependencyUnavailableError(provider, f"{provider} JSON parse failed: {exc}") from exc
        return content

    def _request_ollama(
        self,
        *,
        model: str | None,
        system_prompt: str,
        user_prompt: str,
        want_json: bool,
    ) -> str | dict[str, Any]:
        if not self.settings.enable_ollama:
            raise DependencyUnavailableError("ollama", "QUALBOT_ENABLE_OLLAMA=1 is required for Ollama fallback")
        if not model:
            raise DependencyUnavailableError("ollama", "Ollama model is not configured")

        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": 0, "seed": 42},
        }
        if want_json:
            payload["format"] = "json"

        result = _request_chat(payload, timeout=self.settings.ollama_timeout_seconds)
        content = str(result.get("message", {}).get("content", "")).strip()
        if want_json:
            try:
                return _parse_json_response(content)
            except (ValueError, json.JSONDecodeError) as exc:
                raise DependencyUnavailableError("ollama", f"Ollama JSON parse failed: {exc}") from exc
        if not content:
            raise DependencyUnavailableError("ollama", "Ollama returned an empty response")
        return content
