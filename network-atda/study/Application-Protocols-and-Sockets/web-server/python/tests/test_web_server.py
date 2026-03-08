"""
Web Server — Unit Tests

Tests for the web server solution.

Usage:
    python3 -m pytest test_web_server.py -v

Prerequisites:
    The web server must be running on localhost:6789 before executing tests.
    Start it with:  cd ../../problem/data && python3 ../../python/src/web_server.py
"""

import socket
import time

import pytest

HOST = "localhost"
PORT = 6789


def send_request(path: str) -> tuple[int, str]:
    """Send an HTTP GET request and return (status_code, body).

    Args:
        path: The URL path to request (e.g., "/hello.html").

    Returns:
        A tuple of (HTTP status code, response body as string).
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((HOST, PORT))
        request = f"GET {path} HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode())

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

    text = response.decode(errors="replace")
    # Parse status code from the first line
    status_line = text.split("\r\n")[0]
    status_code = int(status_line.split()[1])
    # Extract body (after the blank line)
    body = text.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in text else ""
    return status_code, body


class TestWebServer:
    """Tests for the Web Server assignment."""

    def test_200_ok_for_existing_file(self):
        """Server should return 200 for an existing file."""
        status, body = send_request("/hello.html")
        assert status == 200

    def test_response_contains_html(self):
        """Response body should contain the HTML content."""
        status, body = send_request("/hello.html")
        assert "<html" in body.lower()
        assert "hello" in body.lower()

    def test_404_for_missing_file(self):
        """Server should return 404 for a non-existent file."""
        status, body = send_request("/nonexistent_file_xyz.html")
        assert status == 404

    def test_404_body_contains_error_message(self):
        """404 response should contain an error message."""
        status, body = send_request("/nonexistent_file_xyz.html")
        assert "404" in body or "not found" in body.lower()

    def test_multiple_sequential_requests(self):
        """Server should handle multiple sequential requests."""
        for _ in range(3):
            status, _ = send_request("/hello.html")
            assert status == 200
