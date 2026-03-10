from __future__ import annotations

import os

from fastapi.testclient import TestClient


def main() -> None:
    os.environ["SECRET_KEY"] = "gateway-smoke-secret"
    os.environ["TOKEN_ISSUER"] = "gateway-smoke"
    os.environ["IDENTITY_SERVICE_URL"] = "http://identity.test/api/v1"
    os.environ["WORKSPACE_SERVICE_URL"] = "http://workspace.test/api/v1"
    os.environ["NOTIFICATION_SERVICE_URL"] = "http://notification.test/api/v1"
    os.environ["REDIS_URL"] = ""

    from app.main import create_app

    with TestClient(create_app()) as client:
        response = client.get("/api/v1/health/live")
        response.raise_for_status()


if __name__ == "__main__":
    main()
