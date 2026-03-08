#!/usr/bin/env python3
"""Minimal SMTP mock server for local automated tests."""

from __future__ import annotations

import socketserver
import sys


class SMTPHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        self.wfile.write(b"220 localhost Mock SMTP Service Ready\r\n")
        in_data = False

        while True:
            raw = self.rfile.readline()
            if not raw:
                return

            line = raw.decode(errors="replace").strip("\r\n")
            upper = line.upper()

            if in_data:
                if line == ".":
                    in_data = False
                    self.wfile.write(b"250 Message accepted for delivery\r\n")
                continue

            if upper.startswith("HELO") or upper.startswith("EHLO"):
                self.wfile.write(b"250 Hello\r\n")
                continue
            if upper.startswith("MAIL FROM:"):
                self.wfile.write(b"250 OK\r\n")
                continue
            if upper.startswith("RCPT TO:"):
                self.wfile.write(b"250 OK\r\n")
                continue
            if upper == "DATA":
                in_data = True
                self.wfile.write(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                continue
            if upper == "RSET":
                in_data = False
                self.wfile.write(b"250 OK\r\n")
                continue
            if upper == "NOOP":
                self.wfile.write(b"250 OK\r\n")
                continue
            if upper == "QUIT":
                self.wfile.write(b"221 Bye\r\n")
                return

            self.wfile.write(b"500 Command not recognized\r\n")


class ReusableTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1025

    with ReusableTCPServer((host, port), SMTPHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
