#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import os
import signal
import socket
import sqlite3
import struct
import subprocess
import tempfile
import time
from dataclasses import dataclass
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
def running_server(build_dir: Path, *, match_duration_ms: int, resume_window_ms: int):
    tcp_port = free_port()
    udp_port = free_port()
    temp_dir = Path(tempfile.mkdtemp(prefix="arena-integration-"))
    db_path = temp_dir / "arena.sqlite3"
    process = subprocess.Popen(
        [
            str(build_dir / "arena_server"),
            "--tcp-port", str(tcp_port),
            "--udp-port", str(udp_port),
            "--db-path", str(db_path),
            "--thread-count", "2",
            "--match-duration-ms", str(match_duration_ms),
            "--resume-window-ms", str(resume_window_ms),
        ],
        cwd=build_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        wait_for_tcp("127.0.0.1", tcp_port)
        yield {
            "tcp_port": tcp_port,
            "udp_port": udp_port,
            "db_path": db_path,
            "process": process,
            "temp_dir": temp_dir,
        }
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

    def recv(self, timeout: float = 3.0) -> tuple[str, dict[str, str]]:
        self.sock.settimeout(timeout)
        line = self.file.readline().decode().strip()
        if not line:
            raise RuntimeError("tcp peer closed")
        return parse_line(line)

    def close(self) -> None:
        self.file.close()
        self.sock.close()


def login(client: ControlClient, name: str) -> tuple[int, str]:
    client.send("LOGIN", name=name)
    verb, fields = client.recv()
    assert verb == "LOGIN_OK"
    return int(fields["player"]), fields["token"]


def wait_for_match_start(client: ControlClient) -> tuple[int, int]:
    while True:
        verb, fields = client.recv()
        if verb == "MATCH_START":
            return int(fields["match"]), int(fields["udp_port"])


def scenario_full_match(build_dir: Path) -> None:
    with running_server(build_dir, match_duration_ms=2500, resume_window_ms=500) as ctx:
        host_proc = subprocess.Popen(
            [
                str(build_dir / "arena_bot"),
                "--host", "127.0.0.1",
                "--tcp-port", str(ctx["tcp_port"]),
                "--mode", "scripted",
                "--role", "host",
                "--name", "alpha",
                "--room-name", "demo",
                "--max-players", "2",
            ],
            cwd=build_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        time.sleep(0.2)
        join_proc = subprocess.Popen(
            [
                str(build_dir / "arena_bot"),
                "--host", "127.0.0.1",
                "--tcp-port", str(ctx["tcp_port"]),
                "--mode", "scripted",
                "--role", "join",
                "--name", "beta",
            ],
            cwd=build_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        host_out, _ = host_proc.communicate(timeout=15)
        join_out, _ = join_proc.communicate(timeout=15)
        assert host_proc.returncode == 0, host_out
        assert join_proc.returncode == 0, join_out
        assert "MATCH_RESULT" in host_out
        assert "MATCH_RESULT" in join_out

        conn = sqlite3.connect(ctx["db_path"])
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM match_history")
            assert cur.fetchone()[0] == 1
            cur.execute("SELECT COUNT(*) FROM players")
            assert cur.fetchone()[0] == 2
        finally:
            conn.close()


def scenario_resume_same_player(build_dir: Path) -> None:
    with running_server(build_dir, match_duration_ms=3500, resume_window_ms=1200) as ctx:
        alpha = ControlClient("127.0.0.1", ctx["tcp_port"])
        beta = ControlClient("127.0.0.1", ctx["tcp_port"])
        alpha_id, alpha_token = login(alpha, "resume-alpha")
        beta_id, _ = login(beta, "resume-beta")
        assert alpha_id != beta_id
        alpha.send("CREATE_ROOM", name="resume-room", max=2)
        _, fields = alpha.recv()
        room_id = fields["room"]
        beta.send("JOIN_ROOM", room=room_id)
        beta.recv()
        alpha.send("READY", value=1)
        beta.send("READY", value=1)
        wait_for_match_start(alpha)
        wait_for_match_start(beta)
        alpha.close()
        time.sleep(0.2)

        resumed = ControlClient("127.0.0.1", ctx["tcp_port"])
        resumed.send("RESUME", token=alpha_token)
        verb, fields = resumed.recv()
        assert verb == "LOGIN_OK"
        assert int(fields["player"]) == alpha_id
        verb, fields = resumed.recv()
        assert verb == "MATCH_START"
        resumed.close()
        beta.close()


def scenario_forfeit(build_dir: Path) -> None:
    with running_server(build_dir, match_duration_ms=5000, resume_window_ms=300) as ctx:
        alpha = ControlClient("127.0.0.1", ctx["tcp_port"])
        beta = ControlClient("127.0.0.1", ctx["tcp_port"])
        alpha_id, _ = login(alpha, "forfeit-alpha")
        beta_id, _ = login(beta, "forfeit-beta")
        alpha.send("CREATE_ROOM", name="forfeit-room", max=2)
        _, fields = alpha.recv()
        room_id = fields["room"]
        beta.send("JOIN_ROOM", room=room_id)
        beta.recv()
        alpha.send("READY", value=1)
        beta.send("READY", value=1)
        wait_for_match_start(alpha)
        wait_for_match_start(beta)
        alpha.close()
        winner = None
        deadline = time.time() + 6.0
        while time.time() < deadline:
            verb, fields = beta.recv(timeout=6.0)
            if verb == "MATCH_RESULT":
                winner = int(fields["winner"])
                break
        assert winner == beta_id
        conn = sqlite3.connect(ctx["db_path"])
        try:
            cur = conn.cursor()
            cur.execute("SELECT result_blob FROM match_history ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            assert row and f"forfeits={alpha_id}" in row[0]
        finally:
            conn.close()
        beta.close()


def scenario_out_of_order_udp(build_dir: Path) -> None:
    with running_server(build_dir, match_duration_ms=2500, resume_window_ms=800) as ctx:
        alpha = ControlClient("127.0.0.1", ctx["tcp_port"])
        beta = ControlClient("127.0.0.1", ctx["tcp_port"])
        alpha_id, _ = login(alpha, "udp-alpha")
        beta_id, _ = login(beta, "udp-beta")
        alpha.send("CREATE_ROOM", name="udp-room", max=2)
        _, fields = alpha.recv()
        room_id = fields["room"]
        beta.send("JOIN_ROOM", room=room_id)
        beta.recv()
        alpha.send("READY", value=1)
        beta.send("READY", value=1)
        match_id, udp_port = wait_for_match_start(alpha)
        wait_for_match_start(beta)
        alpha.send("UDP_BIND", match=match_id, nonce=123)

        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind(("127.0.0.1", 0))
        udp_sock.settimeout(2.0)

        def input_packet(sequence: int, move_x: int) -> bytes:
            return struct.pack(
                "!BBHIIIbbhhBB",
                1, 1, 0, match_id, alpha_id, sequence,
                move_x, 0, 300, 0, 0, 0,
            )

        udp_sock.sendto(input_packet(5, 1), ("127.0.0.1", udp_port))
        udp_sock.sendto(input_packet(4, -1), ("127.0.0.1", udp_port))

        snapshot = None
        for _ in range(6):
            data, _ = udp_sock.recvfrom(2048)
            kind = data[1]
            if kind != 2:
                continue
            header = struct.unpack("!BBHIIIIBBH", data[:24])
            entity_count = header[7]
            offset = 24
            for _ in range(entity_count):
                entity = struct.unpack("!IffHHHBBI", data[offset:offset + 24])
                offset += 24
                if entity[0] == alpha_id:
                    snapshot = entity
                    break
            if snapshot:
                break
        assert snapshot is not None
        assert snapshot[8] == 5
        assert snapshot[1] > 100.0
        alpha.close()
        beta.close()
        udp_sock.close()


def main() -> int:
    build_dir = Path(os.sys.argv[1]).resolve()
    scenario_full_match(build_dir)
    scenario_resume_same_player(build_dir)
    scenario_forfeit(build_dir)
    scenario_out_of_order_udp(build_dir)
    print("integration_test ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
