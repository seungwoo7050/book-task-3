from __future__ import annotations

import shutil
import subprocess
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent


def _project_name() -> str:
    return f"{ROOT.parent.name.lower()}-{uuid.uuid4().hex[:8]}"


def _compose(
    *args: str,
    project_name: str,
    capture_output: bool = False,
    timeout_seconds: int | None = None,
) -> subprocess.CompletedProcess[str]:
    command = ["docker", "compose", "-p", project_name, "-f", "compose.yaml", *args]
    return subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=capture_output,
        timeout=timeout_seconds,
    )


def wait_for(url: str, timeout_seconds: int = 120) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            response = httpx.get(url, timeout=5.0)
            if response.status_code == 200:
                return
        except httpx.HTTPError:
            pass
        time.sleep(2)
    raise TimeoutError(f"Timed out waiting for {url}")


@contextmanager
def compose_stack() -> Iterator[str]:
    project_name = _project_name()
    env_path = ROOT / ".env"
    created_env = False
    if not env_path.exists():
        shutil.copy(ROOT / ".env.example", env_path)
        created_env = True
    try:
        _compose("up", "--build", "-d", project_name=project_name)
        wait_for("http://127.0.0.1:8014/api/v1/health/live")
        wait_for("http://127.0.0.1:8014/api/v1/health/ready")
        yield project_name
    finally:
        try:
            _compose(
                "down",
                "-v",
                "--remove-orphans",
                project_name=project_name,
                capture_output=True,
                timeout_seconds=30,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            pass
        if created_env:
            env_path.unlink(missing_ok=True)
