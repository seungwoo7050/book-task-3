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


def register(sock: socket.socket, nick: str) -> str:
    send_line(sock, f"HELLO {nick}")
    welcome = recv_until(sock, "WELCOME token-", time.time() + 3)
    marker = "WELCOME "
    idx = welcome.find(marker)
    if idx == -1:
        raise RuntimeError(f"{nick} welcome missing")
    token = welcome[idx + len(marker):].split()[0]
    return token


def run_process(server_path: Path, port: int) -> subprocess.Popen[bytes]:
    proc = subprocess.Popen(
        [str(server_path), str(port)],
        cwd=server_path.parent,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid if hasattr(os, "setsid") else None,
    )
    wait_for_port(port, time.time() + 5)
    return proc


def scenario_duel_and_rejoin(server_path: Path, port: int) -> None:
    proc = run_process(server_path, port)
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=2) as alpha, \
            socket.create_connection(("127.0.0.1", port), timeout=2) as bravo, \
            socket.create_connection(("127.0.0.1", port), timeout=2) as dup, \
            socket.create_connection(("127.0.0.1", port), timeout=2) as ghost:

            for sock in (alpha, bravo, dup, ghost):
                sock.settimeout(0.5)

            alpha_token = register(alpha, "alpha")
            _ = register(bravo, "bravo")

            send_line(dup, "HELLO alpha")
            if "ERROR duplicate_nick" not in recv_until(dup, "ERROR duplicate_nick", time.time() + 3):
                raise RuntimeError("duplicate nick rejection missing")

            ghost_token = register(ghost, "ghost")
            ghost.close()

            with socket.create_connection(("127.0.0.1", port), timeout=2) as ghost_rejoin:
                ghost_rejoin.settimeout(0.5)
                send_line(ghost_rejoin, f"REJOIN {ghost_token}")
                if f"WELCOME {ghost_token}" not in recv_until(ghost_rejoin, f"WELCOME {ghost_token}", time.time() + 3):
                    raise RuntimeError("rejoin within grace failed")

            time.sleep(10.5)
            with socket.create_connection(("127.0.0.1", port), timeout=2) as ghost_expired:
                ghost_expired.settimeout(0.5)
                send_line(ghost_expired, f"REJOIN {ghost_token}")
                if "ERROR expired_session" not in recv_until(ghost_expired, "ERROR expired_session", time.time() + 3):
                    raise RuntimeError("expired rejoin was not rejected")

            send_line(alpha, "QUEUE")
            if "ROOM arena-1 lobby" not in recv_until(alpha, "ROOM arena-1 lobby", time.time() + 3):
                raise RuntimeError("alpha lobby join missing")
            send_line(bravo, "QUEUE")
            if "ROOM arena-1 lobby" not in recv_until(bravo, "ROOM arena-1 lobby", time.time() + 3):
                raise RuntimeError("bravo lobby join missing")
            send_line(alpha, "READY")
            send_line(bravo, "READY")
            if "COUNTDOWN 3" not in recv_until(alpha, "COUNTDOWN 3", time.time() + 3):
                raise RuntimeError("countdown start missing")
            if "ROOM arena-1 in_round" not in recv_until(alpha, "ROOM arena-1 in_round", time.time() + 3):
                raise RuntimeError("round start missing")

            send_line(alpha, "INPUT 1 1 1 E 0")
            if "ERROR invalid_input" not in recv_until(alpha, "ERROR invalid_input", time.time() + 3):
                raise RuntimeError("invalid input rejection missing")

            send_line(alpha, "INPUT 1 0 0 E 1")
            send_line(alpha, "INPUT 1 0 0 E 1")
            if "ERROR stale_sequence" not in recv_until(alpha, "ERROR stale_sequence", time.time() + 3):
                raise RuntimeError("stale sequence rejection missing")

            if "HIT" not in recv_until(alpha, "HIT", time.time() + 3):
                raise RuntimeError("first hit missing")
            send_line(alpha, "INPUT 2 0 0 E 1")
            if "HIT" not in recv_until(alpha, "HIT", time.time() + 3):
                raise RuntimeError("second hit missing")
            send_line(alpha, "INPUT 3 0 0 E 1")
            alpha_log = recv_until(alpha, "ROUND_END alpha", time.time() + 5)
            if "ELIM" not in alpha_log or "ROUND_END alpha" not in alpha_log:
                raise RuntimeError("alpha duel win path incomplete")

            send_line(alpha, "PING 12")
            time.sleep(0.2)

            send_line(alpha, "LEAVE")
            send_line(bravo, "LEAVE")

            if not alpha_token.startswith("token-"):
                raise RuntimeError("invalid alpha token format")
    finally:
        shutdown_process(proc)


def scenario_party_lobby(server_path: Path, port: int, size: int) -> None:
    proc = run_process(server_path, port)
    try:
        sockets = [socket.create_connection(("127.0.0.1", port), timeout=2) for _ in range(size + 1)]
        for sock in sockets:
            sock.settimeout(0.5)

        players = sockets[:size]
        overflow = sockets[-1]
        tokens: list[str] = []
        for index, sock in enumerate(players, start=1):
            tokens.append(register(sock, f"p{index}"))
            send_line(sock, "QUEUE")
            if "ROOM arena-1 lobby" not in recv_until(sock, "ROOM arena-1 lobby", time.time() + 3):
                raise RuntimeError("room lobby state missing")

        if size == 4:
            register(overflow, "overflow")
            send_line(overflow, "QUEUE")
            if "ERROR room_full" not in recv_until(overflow, "ERROR room_full", time.time() + 3):
                raise RuntimeError("room_full rejection missing")

        for sock in players:
            send_line(sock, "READY")

        if "COUNTDOWN 3" not in recv_until(players[0], "COUNTDOWN 3", time.time() + 3):
            raise RuntimeError("party countdown missing")
        if "SNAPSHOT 0" not in recv_until(players[0], "SNAPSHOT 0", time.time() + 3):
            raise RuntimeError("party snapshot missing")

        for sock in sockets:
            try:
                sock.close()
            except OSError:
                pass
    finally:
        shutdown_process(proc)


def scenario_draw_timeout(server_path: Path, port: int) -> None:
    proc = run_process(server_path, port)
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=2) as left, \
            socket.create_connection(("127.0.0.1", port), timeout=2) as right:
            left.settimeout(0.5)
            right.settimeout(0.5)
            register(left, "left")
            register(right, "right")
            send_line(left, "QUEUE")
            recv_until(left, "ROOM arena-1 lobby", time.time() + 3)
            send_line(right, "QUEUE")
            recv_until(right, "ROOM arena-1 lobby", time.time() + 3)
            send_line(left, "READY")
            send_line(right, "READY")
            if "ROOM arena-1 in_round" not in recv_until(left, "ROOM arena-1 in_round", time.time() + 3):
                raise RuntimeError("draw scenario round did not start")
            if "ROUND_END draw" not in recv_until(left, "ROUND_END draw", time.time() + 5):
                raise RuntimeError("draw timeout missing")
    finally:
        shutdown_process(proc)


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    server_path = project_root / "arenaserv"
    base_port = int(os.environ.get("ARENASERV_TEST_PORT", "6680"))

    scenario_duel_and_rejoin(server_path, base_port)
    scenario_party_lobby(server_path, base_port + 1, 3)
    scenario_party_lobby(server_path, base_port + 2, 4)
    scenario_draw_timeout(server_path, base_port + 3)
    print("arenaserv smoke passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"arenaserv smoke failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
