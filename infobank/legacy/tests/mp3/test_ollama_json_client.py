from __future__ import annotations

import os

import pytest
from core.errors import DependencyUnavailableError
from core.ollama import chat_json_with_ollama


def test_chat_json_with_ollama_success(monkeypatch: pytest.MonkeyPatch):
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "1"
    os.environ["QUALBOT_OLLAMA_BASE_URL"] = "http://fake"

    calls = {"count": 0}

    def _fake_request(_: dict[str, object], timeout: float = 30.0) -> dict[str, object]:
        calls["count"] += 1
        return {"message": {"content": '{"value": 1, "status": "ok"}'}}

    monkeypatch.setattr("core.ollama._request_chat", _fake_request)
    parsed = chat_json_with_ollama(
        model="judge-model",
        system_prompt="system",
        user_prompt="user",
        retries=1,
    )

    assert parsed["value"] == 1
    assert calls["count"] == 1


def test_chat_json_with_ollama_retry(monkeypatch: pytest.MonkeyPatch):
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "1"
    os.environ["QUALBOT_OLLAMA_BASE_URL"] = "http://fake"

    responses = iter(
        [
            {"message": {"content": "not-json"}},
            {"message": {"content": '{"ok": true}'}},
        ]
    )

    def _fake_request(_: dict[str, object], timeout: float = 30.0) -> dict[str, object]:
        return next(responses)

    monkeypatch.setattr("core.ollama._request_chat", _fake_request)
    parsed = chat_json_with_ollama(
        model="judge-model",
        system_prompt="system",
        user_prompt="user",
        retries=1,
    )

    assert parsed["ok"] is True


def test_chat_json_with_ollama_failure(monkeypatch: pytest.MonkeyPatch):
    os.environ["QUALBOT_ENABLE_OLLAMA"] = "1"
    os.environ["QUALBOT_OLLAMA_BASE_URL"] = "http://fake"

    def _fake_request(_: dict[str, object], timeout: float = 30.0) -> dict[str, object]:
        return {"message": {"content": "still-not-json"}}

    monkeypatch.setattr("core.ollama._request_chat", _fake_request)
    with pytest.raises(DependencyUnavailableError):
        chat_json_with_ollama(
            model="judge-model",
            system_prompt="system",
            user_prompt="user",
            retries=1,
        )
