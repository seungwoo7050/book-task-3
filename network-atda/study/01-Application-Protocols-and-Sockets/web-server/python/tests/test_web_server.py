"""
Web Server unit test.

web server 정답 구현을 대상으로 동작을 확인한다.

Usage:
    python3 -m pytest test_web_server.py -v

Prerequisites:
    테스트 전에 localhost:6789에서 web server가 실행 중이어야 한다.
    Start it with:  cd ../../problem/data && python3 ../../python/src/web_server.py
"""

import socket
import time

import pytest

HOST = "localhost"
PORT = 6789


def send_request(path: str) -> tuple[int, str]:
    """HTTP GET 요청을 보내고 `(status_code, body)`를 반환한다.

    Args:
        path: 요청할 URL path. 예: `"/hello.html"`.

    Returns:
        `(HTTP status code, response body 문자열)` tuple.
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
    # 첫 줄에서 status code를 분리한다.
    status_line = text.split("\r\n")[0]
    status_code = int(status_line.split()[1])
    # 빈 줄 뒤의 body를 추출한다.
    body = text.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in text else ""
    return status_code, body


class TestWebServer:
    """Web Server 과제 동작을 확인하는 test 모음."""

    def test_200_ok_for_existing_file(self):
        """존재하는 파일에는 200 응답이 와야 한다."""
        status, body = send_request("/hello.html")
        assert status == 200

    def test_response_contains_html(self):
        """응답 body에는 HTML 내용이 포함되어야 한다."""
        status, body = send_request("/hello.html")
        assert "<html" in body.lower()
        assert "hello" in body.lower()

    def test_404_for_missing_file(self):
        """없는 파일에는 404 응답이 와야 한다."""
        status, body = send_request("/nonexistent_file_xyz.html")
        assert status == 404

    def test_404_body_contains_error_message(self):
        """404 응답 body에는 에러 메시지가 들어 있어야 한다."""
        status, body = send_request("/nonexistent_file_xyz.html")
        assert "404" in body or "not found" in body.lower()

    def test_multiple_sequential_requests(self):
        """여러 요청을 연속으로 처리할 수 있어야 한다."""
        for _ in range(3):
            status, _ = send_request("/hello.html")
            assert status == 200
