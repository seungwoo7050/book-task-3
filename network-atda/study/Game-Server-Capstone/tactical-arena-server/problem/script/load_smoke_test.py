#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import os
import signal
import socket
import sqlite3
import subprocess
import tempfile
import time
from pathlib import Path


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_tcp(host: str, port: int, timeout: float = 5.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            try:
                sock.connect((host, port))
                return
            except OSError:
                time.sleep(0.05)
    raise RuntimeError(f"server did not open {host}:{port}")


@contextlib.contextmanager
def running_server(build_dir: Path):
    tcp_port = free_port()
    udp_port = free_port()
    temp_dir = Path(tempfile.mkdtemp(prefix="arena-load-"))
    db_path = temp_dir / "arena.sqlite3"
    process = subprocess.Popen(
        [
            str(build_dir / "arena_server"),
            "--tcp-port", str(tcp_port),
            "--udp-port", str(udp_port),
            "--db-path", str(db_path),
            "--thread-count", "4",
            "--match-duration-ms", "2500",
            "--resume-window-ms", "800",
        ],
        cwd=build_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        wait_for_tcp("127.0.0.1", tcp_port)
        yield tcp_port, db_path, process
    finally:
        process.send_signal(signal.SIGTERM)
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)


def main() -> int:
    build_dir = Path(os.sys.argv[1]).resolve()
    with running_server(build_dir) as (tcp_port, db_path, _server):
        completed = subprocess.run(
            [
                str(build_dir / "arena_loadtest"),
                "--host", "127.0.0.1",
                "--tcp-port", str(tcp_port),
                "--room-count", "2",
                "--bots-per-room", "4",
            ],
            cwd=build_dir,
            capture_output=True,
            text=True,
            timeout=45,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr
        assert "status=ok" in completed.stdout
        conn = sqlite3.connect(db_path)
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM match_history")
            assert cur.fetchone()[0] >= 2
            cur.execute("SELECT COUNT(*) FROM players")
            assert cur.fetchone()[0] >= 8
        finally:
            conn.close()
    print("load_smoke_test ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
