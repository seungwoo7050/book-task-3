from __future__ import annotations


def test_golden_set_run_and_overview_consistency(client):
    run_response = client.post("/api/golden-set/run", json={"prompt_version": "v1.0", "kb_version": "v1.0"})
    assert run_response.status_code == 200
    run_payload = run_response.json()
    assert run_payload["count"] > 0

    overview_response = client.get("/api/dashboard/overview")
    assert overview_response.status_code == 200
    overview = overview_response.json()

    eval_list_response = client.get("/api/evaluations")
    assert eval_list_response.status_code == 200
    evaluations = eval_list_response.json()["items"]

    assert overview["evaluation_count"] == len(evaluations)



def test_phase2_compare_hook(client):
    client.post("/api/golden-set/run", json={"prompt_version": "v1.0"})
    client.post("/api/golden-set/run", json={"prompt_version": "v1.1"})

    compare = client.get("/api/dashboard/version-compare?baseline=v1.0&candidate=v1.1")
    assert compare.status_code == 200
    result = compare.json()["result"]
    assert result["baseline"] == "v1.0"
    assert result["candidate"] == "v1.1"

    pipeline_stats = client.get("/api/system/pipeline-stats")
    assert pipeline_stats.status_code == 200
    stats = pipeline_stats.json()
    assert "eval_total_ms_avg" in stats
    assert "critical_short_circuit_rate" in stats
    assert "retrieval_backend" in stats
    assert "dependency_fail_count" in stats


def test_dashboard_metrics_match_evaluations(client):
    client.post("/api/golden-set/run", json={"prompt_version": "v1.0"})

    overview = client.get("/api/dashboard/overview").json()
    metrics = client.get("/api/dashboard/metrics").json()
    evaluations = client.get("/api/evaluations").json()["items"]

    critical_count = sum(1 for item in evaluations if item["is_critical"])
    assert overview["evaluation_count"] == len(evaluations)
    assert metrics["eval_total"] == len(evaluations)
    assert metrics["eval_critical"] == critical_count
