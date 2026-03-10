from __future__ import annotations

import os
from pathlib import Path
from tempfile import gettempdir

from fastapi.testclient import TestClient


def main() -> None:
    db_path = Path(gettempdir()) / "identity_service_smoke.db"
    os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{db_path}"
    os.environ["SECRET_KEY"] = "identity-service-smoke-secret"
    os.environ["TOKEN_ISSUER"] = "identity-service-smoke"

    from app.main import create_app

    with TestClient(create_app()) as client:
        response = client.get("/api/v1/health/live")
        response.raise_for_status()


if __name__ == "__main__":
    main()
