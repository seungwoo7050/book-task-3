from __future__ import annotations

import os

import pytest
from core.errors import DependencyUnavailableError
from core.provider_chain import ProviderChain


def test_provider_chain_falls_back_to_openai(monkeypatch: pytest.MonkeyPatch):
    os.environ["QUALBOT_PROVIDER_CHAIN"] = "upstage,openai,ollama"
    os.environ["QUALBOT_UPSTAGE_API_KEY"] = "upstage-key"
    os.environ["QUALBOT_OPENAI_API_KEY"] = "openai-key"

    chain = ProviderChain()

    def _fake_request_openai_compatible(**kwargs: object) -> str:
        provider = kwargs["provider"]
        if provider == "upstage":
            raise DependencyUnavailableError("upstage", "upstage unavailable")
        return "openai fallback response"

    monkeypatch.setattr(chain, "_request_openai_compatible", _fake_request_openai_compatible)
    monkeypatch.setattr(
        chain,
        "_request_ollama",
        lambda **_: "ollama should not run",
    )

    response, attempts = chain.generate_text(system_prompt="system", user_prompt="user")

    assert response == "openai fallback response"
    assert [attempt.provider for attempt in attempts] == ["upstage", "openai"]
    assert attempts[0].succeeded is False
    assert attempts[1].succeeded is True


def test_provider_chain_json_falls_back_to_ollama(monkeypatch: pytest.MonkeyPatch):
    os.environ["QUALBOT_PROVIDER_CHAIN"] = "upstage,openai,ollama"
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "1"

    chain = ProviderChain()

    def _fake_request_openai_compatible(**kwargs: object) -> dict[str, object]:
        raise DependencyUnavailableError(str(kwargs["provider"]), "provider unavailable")

    monkeypatch.setattr(chain, "_request_openai_compatible", _fake_request_openai_compatible)
    monkeypatch.setattr(
        chain,
        "_request_ollama",
        lambda **_: {"ok": True, "provider": "ollama"},
    )

    payload, attempts = chain.generate_json(system_prompt="system", user_prompt="user")

    assert payload["ok"] is True
    assert [attempt.provider for attempt in attempts] == ["upstage", "openai", "ollama"]
    assert attempts[-1].succeeded is True
