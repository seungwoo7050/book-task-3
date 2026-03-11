"""
Web Proxy 정답 구현.

파일 기반 caching을 갖는 간단한 HTTP proxy server이다.

Usage:
    python3 web_proxy.py [port]

browser나 curl이 localhost:<port>를 HTTP proxy로 쓰도록 설정한다.
기본 port는 8888이다.
"""

import hashlib
import os
import socket
import sys
import threading

CACHE_DIR = "cache"
BUFFER_SIZE = 4096


def parse_url(url: str) -> tuple[str, int, str]:
    """절대 HTTP URL을 `(hostname, port, path)`로 분해한다.

    Args:
        url: 절대 HTTP URL.

    Returns:
        `(hostname, port, path)` tuple.
    """
    # `http://` scheme을 제거한다.
    temp = url.replace("http://", "", 1)

    # host 부분과 path 부분을 나눈다.
    if "/" in temp:
        host_port, path = temp.split("/", 1)
        path = "/" + path
    else:
        host_port = temp
        path = "/"

    # host와 port를 다시 분리한다.
    if ":" in host_port:
        hostname, port_str = host_port.split(":", 1)
        port = int(port_str)
    else:
        hostname = host_port
        port = 80

    return hostname, port, path


def get_cache_path(url: str) -> str:
    """주어진 URL에 대응하는 cache file path를 계산한다.

    Args:
        url: 요청 URL.

    Returns:
        cache file path.
    """
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{url_hash}.dat")


def fetch_from_origin(hostname: str, port: int, path: str) -> bytes:
    """origin web server에서 resource를 가져온다.

    Args:
        hostname: origin server hostname.
        port: origin server port.
        path: 요청 path.

    Returns:
        전체 HTTP 응답 bytes.
    """
    # origin으로 넘길 요청을 구성한다.
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {hostname}\r\n"
        f"Connection: close\r\n"
        f"User-Agent: SimpleProxy/1.0\r\n"
        f"\r\n"
    )

    # origin server에 연결한다.
    origin_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    origin_socket.settimeout(10)
    origin_socket.connect((hostname, port))
    origin_socket.sendall(request.encode())

    # 응답을 끝까지 읽어 모은다.
    response = b""
    while True:
        chunk = origin_socket.recv(BUFFER_SIZE)
        if not chunk:
            break
        response += chunk

    origin_socket.close()
    return response


def handle_client(client_socket: socket.socket, address: tuple) -> None:
    """client의 단일 proxy 요청을 처리한다.

    Args:
        client_socket: client와 연결된 TCP socket.
        address: client의 `(host, port)` tuple.
    """
    try:
        # client의 HTTP 요청을 읽는다.
        request = client_socket.recv(BUFFER_SIZE).decode(errors="replace")
        if not request:
            return

        # 요청 라인을 파싱한다.
        request_line = request.splitlines()[0]
        tokens = request_line.split()
        if len(tokens) < 3 or tokens[0] != "GET":
            print(f"[WARN] Unsupported request: {request_line}")
            error_response = (
                b"HTTP/1.1 400 Bad Request\r\n"
                b"Content-Type: text/html\r\n"
                b"Connection: close\r\n"
                b"\r\n"
                b"<html><body><h1>400 Bad Request</h1>"
                b"<p>Only HTTP GET requests are supported.</p></body></html>"
            )
            client_socket.sendall(error_response)
            return

        url = tokens[1]
        print(f"[REQ]  {address[0]}:{address[1]} — {request_line}")

        # 먼저 cache hit 여부를 확인한다.
        cache_path = get_cache_path(url)
        if os.path.exists(cache_path):
            with open(cache_path, "rb") as f:
                cached_response = f.read()
            client_socket.sendall(cached_response)
            print(f"[HIT]  {url} — served from cache")
            return

        # URL을 해석한 뒤 origin에서 응답을 가져온다.
        hostname, port, path = parse_url(url)
        print(f"[FETCH] {url} → {hostname}:{port}{path}")

        response = fetch_from_origin(hostname, port, path)

        # 받은 응답을 cache에 저장한다.
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(cache_path, "wb") as f:
            f.write(response)
        print(f"[CACHE] Stored: {cache_path}")

        # 최종 응답을 client에 그대로 전달한다.
        client_socket.sendall(response)

    except socket.timeout:
        print(f"[ERROR] Timeout connecting to origin server")
        error_resp = (
            b"HTTP/1.1 504 Gateway Timeout\r\n"
            b"Content-Type: text/html\r\n\r\n"
            b"<html><body><h1>504 Gateway Timeout</h1></body></html>"
        )
        client_socket.sendall(error_resp)

    except (socket.gaierror, ConnectionRefusedError) as e:
        print(f"[ERROR] Cannot reach origin: {e}")
        error_resp = (
            b"HTTP/1.1 502 Bad Gateway\r\n"
            b"Content-Type: text/html\r\n\r\n"
            b"<html><body><h1>502 Bad Gateway</h1></body></html>"
        )
        client_socket.sendall(error_resp)

    except Exception as e:
        print(f"[ERROR] {address}: {e}")

    finally:
        client_socket.close()


def main(port: int = 8888) -> None:
    """proxy server를 시작한다.

    Args:
        port: listen할 TCP port.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen(10)

    print(f"[INFO] Proxy server started on port {port}")
    print(f"[INFO] Use:  curl -x http://localhost:{port} http://www.example.com/")
    print("[INFO] Press Ctrl+C to stop\n")

    try:
        while True:
            client_socket, address = server_socket.accept()
            t = threading.Thread(
                target=handle_client,
                args=(client_socket, address),
            )
            t.daemon = True
            t.start()
    except KeyboardInterrupt:
        print("\n[INFO] Proxy shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    main(port)
