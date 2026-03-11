#!/usr/bin/env python3
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path


def wait_for_port(port: int, deadline: float) -> None:
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("server did not start listening in time")


def recv_text(sock: socket.socket, deadline: float, expected: str) -> str:
    chunks: list[str] = []
    while time.time() < deadline:
        try:
            data = sock.recv(4096)
        except socket.timeout:
            continue
        if not data:
            break
        chunks.append(data.decode("utf-8", "ignore"))
        joined = "".join(chunks)
        if expected in joined:
            return joined
    return "".join(chunks)


def send_line(sock: socket.socket, line: str) -> None:
    sock.sendall((line + "\r\n").encode("utf-8"))


def shutdown_process(proc: subprocess.Popen[bytes]) -> None:
    if proc.poll() is not None:
        return
    if hasattr(os, "killpg") and proc.pid > 0:
        os.killpg(proc.pid, signal.SIGINT)
    else:
        proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    server_path = project_root / "eventlabd"
    port = int(os.environ.get("EVENTLAB_TEST_PORT", "6670"))

    proc = subprocess.Popen(
        [str(server_path), str(port)],
        cwd=project_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid if hasattr(os, "setsid") else None,
    )

    try:
        wait_for_port(port, time.time() + 5)
        with socket.create_connection(("127.0.0.1", port), timeout=2) as a, socket.create_connection(("127.0.0.1", port), timeout=2) as b:
            a.settimeout(0.5)
            b.settimeout(0.5)

            welcome_a = recv_text(a, time.time() + 3, "WELCOME")
            welcome_b = recv_text(b, time.time() + 3, "WELCOME")
            if "WELCOME" not in welcome_a or "WELCOME" not in welcome_b:
                raise RuntimeError("did not receive welcome on both connections")

            send_line(a, "hello eventlab")
            echoed = recv_text(a, time.time() + 3, "ECHO hello eventlab")
            if "ECHO hello eventlab" not in echoed:
                raise RuntimeError("echo path failed")

            send_line(a, "PING keepalive")
            pong = recv_text(a, time.time() + 3, "PONG keepalive")
            if "PONG keepalive" not in pong:
                raise RuntimeError("ping/pong path failed")

            time.sleep(3)
            send_line(a, "PING wakeup")
            _ = recv_text(a, time.time() + 3, "PONG wakeup")
            idle_ping = recv_text(b, time.time() + 5, "PING :idle-check")
            if "PING :idle-check" not in idle_ping:
                raise RuntimeError("idle keep-alive ping did not arrive")

            send_line(a, "QUIT")
            bye = recv_text(a, time.time() + 3, "BYE")
            if "BYE" not in bye:
                raise RuntimeError("quit path failed")

        print("eventlab smoke passed.")
        return 0
    finally:
        shutdown_process(proc)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"eventlab smoke failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
