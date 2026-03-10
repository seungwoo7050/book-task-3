from __future__ import annotations


def test_health_and_metrics(client) -> None:
    assert client.get("/api/v1/health/live").status_code == 200
    assert client.get("/api/v1/ops/metrics").status_code == 200
