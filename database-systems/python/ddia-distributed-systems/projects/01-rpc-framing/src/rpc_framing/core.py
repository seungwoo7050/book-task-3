from __future__ import annotations

import json
import queue
import socket
import struct
import threading
import time
from itertools import count
from tempfile import TemporaryDirectory


def encode_frame(payload) -> bytes:
    if not isinstance(payload, bytes):
        payload = json.dumps(payload).encode("utf-8")
    return struct.pack(">I", len(payload)) + payload


class FrameDecoder:
    def __init__(self) -> None:
        self._buffer = bytearray()

    def feed(self, chunk: bytes) -> list[bytes]:
        self._buffer.extend(chunk)
        payloads: list[bytes] = []
        while len(self._buffer) >= 4:
            size = struct.unpack(">I", self._buffer[:4])[0]
            if len(self._buffer) < 4 + size:
                break
            payloads.append(bytes(self._buffer[4 : 4 + size]))
            del self._buffer[: 4 + size]
        return payloads


class RPCServer:
    def __init__(self, address: str = "127.0.0.1:0") -> None:
        host, port = address.rsplit(":", 1)
        self._bind = (host, int(port))
        self.handlers: dict[str, callable] = {}
        self._socket: socket.socket | None = None
        self._accept_thread: threading.Thread | None = None
        self._connections: set[socket.socket] = set()
        self._lock = threading.Lock()
        self._running = threading.Event()

    def register(self, method: str, handler) -> None:
        self.handlers[method] = handler

    def start(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(self._bind)
        self._socket.listen()
        self._socket.settimeout(0.1)
        self._running.set()
        self._accept_thread = threading.Thread(target=self._accept_loop, daemon=True)
        self._accept_thread.start()

    @property
    def address(self) -> str:
        if self._socket is None:
            return ""
        host, port = self._socket.getsockname()
        return f"{host}:{port}"

    def close(self) -> None:
        self._running.clear()
        if self._socket is not None:
            try:
                self._socket.close()
            except OSError:
                pass
        with self._lock:
            for conn in list(self._connections):
                try:
                    conn.close()
                except OSError:
                    pass
            self._connections.clear()

    def _accept_loop(self) -> None:
        assert self._socket is not None
        while self._running.is_set():
            try:
                conn, _ = self._socket.accept()
            except TimeoutError:
                continue
            except OSError:
                return
            with self._lock:
                self._connections.add(conn)
            threading.Thread(target=self._handle_conn, args=(conn,), daemon=True).start()

    def _handle_conn(self, conn: socket.socket) -> None:
        decoder = FrameDecoder()
        writer_lock = threading.Lock()
        try:
            while self._running.is_set():
                try:
                    chunk = conn.recv(4096)
                except OSError:
                    return
                if not chunk:
                    return
                for payload in decoder.feed(chunk):
                    try:
                        request = json.loads(payload.decode("utf-8"))
                    except json.JSONDecodeError:
                        continue
                    threading.Thread(target=self._dispatch, args=(conn, writer_lock, request), daemon=True).start()
        finally:
            with self._lock:
                self._connections.discard(conn)
            try:
                conn.close()
            except OSError:
                pass

    def _dispatch(self, conn: socket.socket, writer_lock: threading.Lock, request: dict) -> None:
        response = {"type": "response", "correlation_id": request["correlation_id"]}
        handler = self.handlers.get(request["method"])
        if handler is None:
            response["error"] = f"unknown method: {request['method']}"
        else:
            try:
                response["result"] = handler(request.get("params"))
            except Exception as error:  # pragma: no cover - exercised through tests
                response["error"] = str(error)
        frame = encode_frame(response)
        with writer_lock:
            try:
                conn.sendall(frame)
            except OSError:
                return


class RPCClient:
    def __init__(self, address: str) -> None:
        host, port = address.rsplit(":", 1)
        self._address = (host, int(port))
        self._conn: socket.socket | None = None
        self._decoder = FrameDecoder()
        self._pending: dict[str, queue.Queue] = {}
        self._pending_lock = threading.Lock()
        self._send_lock = threading.Lock()
        self._ids = count(1)
        self._closed = threading.Event()

    def connect(self) -> None:
        self._conn = socket.create_connection(self._address)
        threading.Thread(target=self._read_loop, daemon=True).start()

    def close(self) -> None:
        self._closed.set()
        if self._conn is not None:
            try:
                self._conn.close()
            except OSError:
                pass
        self._fail_all("connection closed")

    def call(self, method: str, params, timeout: float | None = None):
        if self._conn is None:
            raise RuntimeError("rpc: client not connected")

        correlation_id = f"req-{next(self._ids)}"
        response_queue: queue.Queue = queue.Queue(maxsize=1)
        with self._pending_lock:
            self._pending[correlation_id] = response_queue

        request = {
            "type": "request",
            "correlation_id": correlation_id,
            "method": method,
            "params": params,
        }
        with self._send_lock:
            self._conn.sendall(encode_frame(request))

        try:
            response = response_queue.get(timeout=timeout)
        except queue.Empty as error:
            with self._pending_lock:
                self._pending.pop(correlation_id, None)
            raise TimeoutError("rpc call timed out") from error

        if "error" in response:
            raise RuntimeError(response["error"])
        return response.get("result")

    def _read_loop(self) -> None:
        assert self._conn is not None
        try:
            while not self._closed.is_set():
                chunk = self._conn.recv(4096)
                if not chunk:
                    raise ConnectionError("connection closed")
                for payload in self._decoder.feed(chunk):
                    response = json.loads(payload.decode("utf-8"))
                    correlation_id = response["correlation_id"]
                    with self._pending_lock:
                        pending = self._pending.pop(correlation_id, None)
                    if pending is not None:
                        pending.put(response)
        except Exception as error:  # pragma: no cover - exercised through close paths
            self._fail_all(str(error))

    def _fail_all(self, message: str) -> None:
        with self._pending_lock:
            pending = self._pending
            self._pending = {}
        for response_queue in pending.values():
            response_queue.put({"error": message})


def demo() -> None:
    _ = TemporaryDirectory  # 다른 프로젝트와 demo 스타일을 맞춘다.
    server = RPCServer()
    server.register("echo", lambda params: params)
    server.start()
    client = RPCClient(server.address)
    client.connect()
    result = client.call("echo", {"msg": "hello"}, timeout=1.0)
    print(result)
    client.close()
    server.close()
