from __future__ import annotations

from fastapi.testclient import TestClient


def test_auth_bootstrap_and_session_cookie(client: TestClient) -> None:
    unauth = client.get("/api/datasets")
    assert unauth.status_code == 401

    session_before = client.get("/api/auth/session")
    assert session_before.status_code == 200
    assert session_before.json() == {"authenticated": False, "email": None}

    login = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "password123"},
    )
    assert login.status_code == 200
    assert login.json()["authenticated"] is True

    session_after = client.get("/api/auth/session")
    assert session_after.status_code == 200
    assert session_after.json() == {"authenticated": True, "email": "admin@example.com"}


def test_sample_assets_are_bootstrapped_for_first_run(auth_client: TestClient) -> None:
    dataset_response = auth_client.get("/api/datasets")
    bundle_response = auth_client.get("/api/kb-bundles")

    assert dataset_response.status_code == 200
    assert bundle_response.status_code == 200

    datasets = dataset_response.json()["items"]
    bundles = bundle_response.json()["items"]

    assert any(item["is_sample"] and item["record_count"] >= 4 for item in datasets)
    assert any(item["is_sample"] and item["doc_count"] >= 10 for item in bundles)
