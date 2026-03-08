#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import sys
import threading
import time


COUNTS = {}
LOCK = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, format, *args):
        return

    def do_GET(self):
        parsed = urlparse(self.path)
        key = parsed.path
        if parsed.query:
            key = f"{key}?{parsed.query}"

        with LOCK:
            COUNTS[key] = COUNTS.get(key, 0) + 1
            hit = COUNTS[key]

        if parsed.path.startswith("/slow"):
            time.sleep(2)
            body = f"slow path={key} hit={hit}\n".encode()
        elif parsed.path.startswith("/cacheable"):
            body = f"cacheable path={key} hit={hit}\n".encode()
        elif parsed.path.startswith("/large"):
            prefix = f"large path={key} hit={hit}\n".encode()
            body = prefix + (b"x" * 120000)
        elif parsed.path == "/headers":
            body = (
                f"host={self.headers.get('Host', '')}\n"
                f"user-agent={self.headers.get('User-Agent', '')}\n"
                f"connection={self.headers.get('Connection', '')}\n"
                f"proxy-connection={self.headers.get('Proxy-Connection', '')}\n"
                f"x-test={self.headers.get('X-Test', '')}\n"
            ).encode()
        elif parsed.path == "/health":
            body = b"ok\n"
        else:
            body = f"default path={key} hit={hit}\n".encode()

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <port>", file=sys.stderr)
        return 1

    port = int(sys.argv[1])
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
