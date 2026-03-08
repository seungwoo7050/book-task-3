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
    temp_dir = Path(tempfile.mkdtemp(prefix="arena-presentation-"))
    db_path = temp_dir / "arena.sqlite3"
    process = subprocess.Popen(
        [
            str(build_dir / "arena_server"),
            "--tcp-port", str(tcp_port),
            "--udp-port", str(udp_port),
            "--db-path", str(db_path),
            "--thread-count", "2",
            "--match-duration-ms", "2500",
            "--resume-window-ms", "800",
        ],
        cwd=build_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        wait_for_tcp("127.0.0.1", tcp_port)
        yield tcp_port, db_path
    finally:
        process.send_signal(signal.SIGTERM)
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)


def parse_line(line: str) -> tuple[str, dict[str, str]]:
    parts = line.strip().split()
    if not parts:
        raise RuntimeError("empty protocol line")
    fields: dict[str, str] = {}
    for token in parts[1:]:
        key, value = token.split("=", 1)
        fields[key] = value
    return parts[0], fields


class ControlClient:
    def __init__(self, host: str, tcp_port: int):
        self.sock = socket.create_connection((host, tcp_port), timeout=2.0)
        self.file = self.sock.makefile("rwb", buffering=0)

    def send(self, verb: str, **fields: str | int) -> None:
        line = verb
        for key, value in fields.items():
            line += f" {key}={value}"
        self.file.write((line + "\n").encode())

    def recv(self, timeout: float = 3.0) -> tuple[str, dict[str, str], str]:
        self.sock.settimeout(timeout)
        line = self.file.readline().decode().strip()
        if not line:
            raise RuntimeError("tcp peer closed")
        verb, fields = parse_line(line)
        return verb, fields, line

    def close(self) -> None:
        self.file.close()
        self.sock.close()


def wait_for_match_events(
    client: ControlClient,
    label: str,
    transcript: list[str],
) -> tuple[int, int]:
    match_id = 0
    udp_port = 0
    while True:
        verb, fields, line = client.recv(timeout=5.0)
        transcript.append(f"{label} <- {line}")
        if verb == "ROOM_UPDATE":
            continue
        if verb == "MATCH_START":
            match_id = int(fields["match"])
            udp_port = int(fields["udp_port"])
            break
    return match_id, udp_port


def main() -> int:
    build_dir = Path(os.sys.argv[1]).resolve()
    transcript: list[str] = []
    with running_server(build_dir) as (tcp_port, db_path):
        alpha = ControlClient("127.0.0.1", tcp_port)
        beta = ControlClient("127.0.0.1", tcp_port)

        transcript.append(f"server listening on tcp={tcp_port}")

        alpha.send("LOGIN", name="demo-alpha")
        transcript.append("alpha -> LOGIN name=demo-alpha")
        _, _, line = alpha.recv()
        transcript.append(f"alpha <- {line}")

        beta.send("LOGIN", name="demo-beta")
        transcript.append("beta -> LOGIN name=demo-beta")
        _, _, line = beta.recv()
        transcript.append(f"beta <- {line}")

        alpha.send("CREATE_ROOM", name="demo-room", max=2)
        transcript.append("alpha -> CREATE_ROOM name=demo-room max=2")
        _, fields, line = alpha.recv()
        transcript.append(f"alpha <- {line}")
        room_id = fields["room"]

        beta.send("JOIN_ROOM", room=room_id)
        transcript.append(f"beta -> JOIN_ROOM room={room_id}")
        _, _, line = beta.recv()
        transcript.append(f"beta <- {line}")
        _, _, line = alpha.recv()
        transcript.append(f"alpha <- {line}")

        alpha.send("READY", value=1)
        beta.send("READY", value=1)
        transcript.append("alpha -> READY value=1")
        transcript.append("beta -> READY value=1")

        wait_for_match_events(alpha, "alpha", transcript)
        wait_for_match_events(beta, "beta", transcript)

        while True:
            verb, _, line = alpha.recv(timeout=5.0)
            transcript.append(f"alpha <- {line}")
            if verb == "MATCH_RESULT":
                break

        while True:
            verb, _, line = beta.recv(timeout=5.0)
            transcript.append(f"beta <- {line}")
            if verb == "MATCH_RESULT":
                break

        alpha.close()
        beta.close()

        conn = sqlite3.connect(db_path)
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM players")
            player_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM match_history")
            match_count = cur.fetchone()[0]
            cur.execute("SELECT result_blob FROM match_history ORDER BY id DESC LIMIT 1")
            result_blob = cur.fetchone()[0]
            transcript.append("")
            transcript.append("sqlite summary")
            transcript.append(f"players={player_count}")
            transcript.append(f"matches={match_count}")
            transcript.append(f"last_result={result_blob}")
        finally:
            conn.close()

    print("\n".join(transcript))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
