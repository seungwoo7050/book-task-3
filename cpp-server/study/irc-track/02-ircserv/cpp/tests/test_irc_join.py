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
    server_path = project_root / "ircserv"
    port = int(os.environ.get("IRC_TEST_PORT", "6672"))
    password = os.environ.get("IRC_TEST_PASSWORD", "password")

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
            socket.create_connection(("127.0.0.1", port), timeout=2) as carol:

            alice.settimeout(0.5)
            bob.settimeout(0.5)
            carol.settimeout(0.5)

            send_line(alice, "CAP LS 302")
            if "CAP * LS :" not in recv_until(alice, "CAP * LS :", time.time() + 5):
                raise RuntimeError("CAP LS 302 response missing")

            if " 005 alice " not in register(alice, "alice", password):
                raise RuntimeError("alice registration failed")
            if " 005 bob " not in register(bob, "bob", password):
                raise RuntimeError("bob registration failed")
            if " 005 carol " not in register(carol, "carol", password):
                raise RuntimeError("carol registration failed")

            send_line(alice, "JOIN #ops")
            if ":alice JOIN #ops" not in recv_until(alice, ":alice JOIN #ops", time.time() + 5):
                raise RuntimeError("alice join failed")

            send_line(bob, "JOIN #ops")
            if ":bob JOIN #ops" not in recv_until(bob, ":bob JOIN #ops", time.time() + 5):
                raise RuntimeError("bob join failed")

            send_line(alice, "MODE #ops +i")
            if "MODE #ops +i" not in recv_until(alice, "MODE #ops +i", time.time() + 5):
                raise RuntimeError("invite-only mode was not applied")

            send_line(alice, "INVITE carol #ops")
            if " 341 alice carol #ops" not in recv_until(alice, " 341 alice carol #ops", time.time() + 5):
                raise RuntimeError("invite acknowledgement missing")
            if "INVITE carol #ops" not in recv_until(carol, "INVITE carol #ops", time.time() + 5):
                raise RuntimeError("invite event missing for carol")

            time.sleep(0.2)
            send_line(carol, "JOIN #ops")
            if ":carol JOIN #ops" not in recv_until(carol, ":carol JOIN #ops", time.time() + 5):
                raise RuntimeError("carol could not join invited channel")

            send_line(alice, "TOPIC #ops :control room")
            if "TOPIC #ops :control room" not in recv_until(carol, "TOPIC #ops :control room", time.time() + 5):
                raise RuntimeError("topic broadcast missing")

            send_line(alice, "PRIVMSG #ops :hello capstone")
            if "PRIVMSG #ops :hello capstone" not in recv_until(carol, "PRIVMSG #ops :hello capstone", time.time() + 5):
                raise RuntimeError("channel message broadcast missing")

            send_line(alice, "KICK #ops bob :bye")
            if "KICK #ops bob :bye" not in recv_until(bob, "KICK #ops bob :bye", time.time() + 5):
                raise RuntimeError("kick event missing")

            time.sleep(0.2)
            send_line(bob, "JOIN #ops")
            if " 473 bob #ops " not in recv_until(bob, " 473 bob #ops ", time.time() + 8):
                raise RuntimeError("invite-only rejoin rejection missing")

            send_line(alice, "PING capstone")
            if "PONG capstone" not in recv_until(alice, "PONG capstone", time.time() + 5):
                raise RuntimeError("PING/PONG failed")

        print("ircserv capstone smoke passed.")
        return 0
    finally:
        shutdown_process(proc)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ircserv capstone smoke failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
