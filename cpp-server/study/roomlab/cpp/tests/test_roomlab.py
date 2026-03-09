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


def send_line(sock: socket.socket, line: str) -> None:
    sock.sendall((line + "\r\n").encode("utf-8"))


def recv_until(sock: socket.socket, expected: str, deadline: float) -> str:
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


def register(sock: socket.socket, nick: str, password: str) -> str:
    send_line(sock, f"PASS {password}")
    send_line(sock, f"NICK {nick}")
    send_line(sock, f"USER {nick} 0 * :{nick}")
    return recv_until(sock, f" 005 {nick} ", time.time() + 5)


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
    server_path = project_root / "roomlabd"
    port = int(os.environ.get("ROOMLAB_TEST_PORT", "6671"))
    password = os.environ.get("ROOMLAB_TEST_PASSWORD", "password")

    proc = subprocess.Popen(
        [str(server_path), str(port), password],
        cwd=project_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid if hasattr(os, "setsid") else None,
    )

    try:
        wait_for_port(port, time.time() + 5)
        with socket.create_connection(("127.0.0.1", port), timeout=2) as alice, \
            socket.create_connection(("127.0.0.1", port), timeout=2) as bob, \
            socket.create_connection(("127.0.0.1", port), timeout=2) as dup:

            alice.settimeout(0.5)
            bob.settimeout(0.5)
            dup.settimeout(0.5)

            if " 001 alice " not in register(alice, "alice", password):
                raise RuntimeError("alice did not complete registration")
            if " 001 bob " not in register(bob, "bob", password):
                raise RuntimeError("bob did not complete registration")

            send_line(alice, "JOIN #lab")
            if ":alice JOIN #lab" not in recv_until(alice, ":alice JOIN #lab", time.time() + 5):
                raise RuntimeError("alice join failed")

            send_line(bob, "JOIN #lab")
            if ":bob JOIN #lab" not in recv_until(bob, ":bob JOIN #lab", time.time() + 5):
                raise RuntimeError("bob join failed")

            send_line(alice, "PRIVMSG #lab :hello everyone")
            if "PRIVMSG #lab :hello everyone" not in recv_until(bob, "PRIVMSG #lab :hello everyone", time.time() + 5):
                raise RuntimeError("channel broadcast failed")

            send_line(bob, "NOTICE alice :quiet ping")
            if "quiet ping" not in recv_until(alice, "quiet ping", time.time() + 5):
                raise RuntimeError("notice delivery failed")

            send_line(dup, f"PASS {password}")
            send_line(dup, "NICK alice")
            if " 433 alice " not in recv_until(dup, " 433 alice ", time.time() + 5):
                raise RuntimeError("duplicate nickname was not rejected")

            send_line(bob, "PING token123")
            if "PONG token123" not in recv_until(bob, "PONG token123", time.time() + 5):
                raise RuntimeError("PING/PONG failed")

            send_line(alice, "QUIT :gone away")
            if "QUIT :gone away" not in recv_until(bob, "QUIT :gone away", time.time() + 5):
                raise RuntimeError("QUIT cleanup broadcast failed")

            send_line(dup, "PART #lab :nope")
            if " 442 " not in recv_until(dup, " 442 ", time.time() + 5):
                raise RuntimeError("not-on-channel error missing")

        print("roomlab smoke passed.")
        return 0
    finally:
        shutdown_process(proc)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"roomlab smoke failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
