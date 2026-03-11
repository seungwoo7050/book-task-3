"""
Web Server 정답 구현.

정적 파일을 제공하는 multi-threaded HTTP web server이다.

Usage:
    python3 web_server.py [port]

현재 working directory의 파일을 제공한다.
기본 port는 6789다.
"""

import os
import socket
import sys
import threading

# 파일 확장자를 MIME content type으로 매핑한다.
CONTENT_TYPES = {
    ".html": "text/html",
    ".htm": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".ico": "image/x-icon",
    ".txt": "text/plain",
}

NOT_FOUND_PAGE = (
    b"<html><head><title>404 Not Found</title></head>"
    b"<body><h1>404 Not Found</h1>"
    b"<p>The requested resource was not found on this server.</p>"
    b"</body></html>"
)


def get_content_type(filename: str) -> str:
    """주어진 filename에 대응하는 MIME content type을 반환한다.

    Args:
        filename: 파일 이름.

    Returns:
        MIME type 문자열. 기본값은 `application/octet-stream`.
    """
    _, ext = os.path.splitext(filename)
    return CONTENT_TYPES.get(ext.lower(), "application/octet-stream")


def handle_client(connection_socket: socket.socket, address: tuple) -> None:
    """연결된 client의 단일 HTTP 요청을 처리한다.

    Args:
        connection_socket: client와 연결된 TCP socket.
        address: client를 식별하는 `(host, port)` tuple.
    """
    try:
        # HTTP 요청을 최대 4 KB까지 읽는다.
        message = connection_socket.recv(4096).decode()
        if not message:
            return

        # 요청 라인 예시: "GET /hello.html HTTP/1.1"
        request_line = message.splitlines()[0]
        print(f"[INFO] {address[0]}:{address[1]} — {request_line}")

        tokens = request_line.split()
        if len(tokens) < 2:
            return

        # 앞의 '/'를 제거해 실제 filename을 얻는다.
        filename = tokens[1][1:]
        if filename == "":
            filename = "hello.html"  # 기본 페이지

        # 요청한 파일을 열어 body를 읽는다.
        with open(filename, "rb") as f:
            body = f.read()

        # 200 OK 응답을 구성해 전송한다.
        content_type = get_content_type(filename)
        header = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )
        connection_socket.sendall(header.encode() + body)

    except FileNotFoundError:
        # 파일이 없으면 404 Not Found 응답을 전송한다.
        header = (
            f"HTTP/1.1 404 Not Found\r\n"
            f"Content-Type: text/html\r\n"
            f"Content-Length: {len(NOT_FOUND_PAGE)}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )
        connection_socket.sendall(header.encode() + NOT_FOUND_PAGE)

    except Exception as e:
        print(f"[ERROR] {address}: {e}")

    finally:
        connection_socket.close()


def main(port: int = 6789) -> None:
    """multi-threaded web server를 시작한다.

    Args:
        port: listen할 TCP port 번호.
    """
    # TCP server socket을 준비한다.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen(5)

    print(f"[INFO] Web server started on port {port}")
    print(f"[INFO] Serving files from: {os.getcwd()}")
    print(f"[INFO] Open http://localhost:{port}/hello.html in your browser")
    print("[INFO] Press Ctrl+C to stop\n")

    try:
        while True:
            # 새 연결을 받는다.
            connection_socket, address = server_socket.accept()

            # 각 연결은 daemon thread에서 처리한다.
            t = threading.Thread(
                target=handle_client,
                args=(connection_socket, address),
            )
            t.daemon = True
            t.start()
    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 6789
    main(port)
