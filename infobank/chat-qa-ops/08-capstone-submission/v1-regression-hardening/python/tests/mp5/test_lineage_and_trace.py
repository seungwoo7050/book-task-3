from __future__ import annotations

import os

from core.langfuse_trace import create_trace_envelope
from db.database import session_scope
from evaluator.run_registry import create_evaluation_run


def test_golden_set_run_persists_lineage_and_trace(client):
    response = client.post(
        "/api/golden-set/run",
        json={"prompt_version": "v1.0", "run_label": "v1.0", "dataset": "golden-set"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["run_label"] == "v1.0"
    assert payload["run_id"]

    item = payload["items"][0]
    assert item["lineage"]["run_label"] == "v1.0"
    assert item["provider_trace"] == [] or isinstance(item["provider_trace"], list)
    assert isinstance(item["retrieval_trace"], list)
    assert isinstance(item["claim_trace"], list)
    assert isinstance(item["judge_trace"], dict)


def test_version_compare_returns_run_level_deltas(client):
    first = client.post("/api/golden-set/run", json={"prompt_version": "v1.0", "run_label": "v1.0"})
    second = client.post("/api/golden-set/run", json={"prompt_version": "v1.1", "run_label": "v1.1"})
    assert first.status_code == 200
    assert second.status_code == 200

    compare = client.get("/api/dashboard/version-compare?baseline=v1.0&candidate=v1.1&dataset=golden-set")
    assert compare.status_code == 200
    result = compare.json()["result"]
    assert result["baseline"] == "v1.0"
    assert result["candidate"] == "v1.1"
    assert "pass_delta" in result
    assert "fail_delta" in result
    assert "critical_delta" in result
    assert "baseline_failures" in result
    assert "candidate_failures" in result


def test_langfuse_trace_envelope_noop_and_prepared_modes():
    os.environ["QUALBOT_LANGFUSE_ENABLED"] = "0"
    run = create_trace_envelope(
        settings=create_evaluation_run.__globals__["load_settings"](),
        run_label="noop-run",
        dataset="golden-set",
    )
    assert run.transport == "noop"

    os.environ["QUALBOT_LANGFUSE_ENABLED"] = "1"
    os.environ["QUALBOT_LANGFUSE_HOST"] = "https://langfuse.example"
    os.environ["QUALBOT_LANGFUSE_PUBLIC_KEY"] = "public"
    os.environ["QUALBOT_LANGFUSE_SECRET_KEY"] = "secret"
    prepared = create_trace_envelope(
        settings=create_evaluation_run.__globals__["load_settings"](),
        run_label="prepared-run",
        dataset="golden-set",
    )
    assert prepared.transport == "langfuse-prepared"


def test_run_registry_captures_retrieval_version():
    with session_scope() as session:
        run = create_evaluation_run(
            session,
            run_label="compare-v1",
            dataset_name="golden-set",
            retrieval_version="retrieval-v1",
        )
        assert run.run_label == "compare-v1"
        assert run.retrieval_version == "retrieval-v1"
