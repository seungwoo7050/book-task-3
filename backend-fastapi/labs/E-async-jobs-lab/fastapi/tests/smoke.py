from __future__ import annotations

import os
from pathlib import Path
from tempfile import gettempdir

from fastapi.testclient import TestClient


def main() -> None:
    database_path = Path(gettempdir()) / "e_async_jobs_lab_smoke.db"
    os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{database_path}"
    os.environ["REDIS_URL"] = ""
    os.environ["CELERY_TASK_ALWAYS_EAGER"] = "true"
    os.environ["CELERY_BROKER_URL"] = "memory://"
    os.environ["CELERY_RESULT_BACKEND"] = "cache+memory://"

    from app.main import create_app

    with TestClient(create_app()) as client:
        response = client.get("/api/v1/health/live")
        response.raise_for_status()


if __name__ == "__main__":
    main()
