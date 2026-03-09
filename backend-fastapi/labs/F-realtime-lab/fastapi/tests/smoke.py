from __future__ import annotations

import os

from fastapi.testclient import TestClient


def main() -> None:
    os.environ["REDIS_URL"] = ""

    from app.main import create_app

    with TestClient(create_app()) as client:
        response = client.get("/api/v1/health/live")
        response.raise_for_status()


if __name__ == "__main__":
    main()
