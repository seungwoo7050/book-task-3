from __future__ import annotations


def test_live_ready_and_metrics(client) -> None:
    live = client.get("/api/v1/health/live")
    assert live.status_code == 200

    ready = client.get("/api/v1/ops/ready")
    assert ready.status_code == 200
    assert ready.json()["status"] == "ok"

    metrics = client.get("/api/v1/ops/metrics")
    assert metrics.status_code == 200
    assert "app_requests_total" in metrics.text
