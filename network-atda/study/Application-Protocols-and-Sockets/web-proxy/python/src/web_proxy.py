"""
Web Proxy — Complete Solution

A simple HTTP proxy server with file-based caching.

Usage:
    python3 web_proxy.py [port]

Configure your browser or curl to use localhost:<port> as HTTP proxy.
Default port is 8888.
"""

import hashlib
import os
import socket
import sys
import threading

CACHE_DIR = "cache"
BUFFER_SIZE = 4096


def parse_url(url: str) -> tuple[str, int, str]:
    """Parse an absolute HTTP URL into (hostname, port, path).

    Args:
        url: An absolute HTTP URL.

    Returns:
        A tuple of (hostname, port, path).
    """
    # Remove scheme
    temp = url.replace("http://", "", 1)

    # Split host and path
    if "/" in temp:
        host_port, path = temp.split("/", 1)
        path = "/" + path
    else:
        host_port = temp
        path = "/"

    # Split host and port
    if ":" in host_port:
        hostname, port_str = host_port.split(":", 1)
        port = int(port_str)
    else:
        hostname = host_port
        port = 80

    return hostname, port, path


def get_cache_path(url: str) -> str:
    """Get the cache file path for a given URL.

    Args:
        url: The request URL.

    Returns:
        Path to the cache file.
    """
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{url_hash}.dat")


def fetch_from_origin(hostname: str, port: int, path: str) -> bytes:
    """Fetch a resource from the origin web server.

    Args:
        hostname: The origin server hostname.
        port: The origin server port.
        path: The request path.

    Returns:
        The complete HTTP response as bytes.
    """
    # Build the forwarded request
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {hostname}\r\n"
        f"Connection: close\r\n"
        f"User-Agent: SimpleProxy/1.0\r\n"
        f"\r\n"
    )

    # Connect to the origin server
    origin_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    origin_socket.settimeout(10)
    origin_socket.connect((hostname, port))
    origin_socket.sendall(request.encode())

    # Receive the full response
    response = b""
    while True:
        chunk = origin_socket.recv(BUFFER_SIZE)
        if not chunk:
            break
        response += chunk

    origin_socket.close()
    return response


def handle_client(client_socket: socket.socket, address: tuple) -> None:
    """Handle a single proxy request from a client.

    Args:
        client_socket: TCP socket connected to the client.
        address: Client's (host, port) tuple.
    """
    try:
        # Receive the client's HTTP request
        request = client_socket.recv(BUFFER_SIZE).decode(errors="replace")
        if not request:
            return

        # Parse the request line
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

        # Check cache
        cache_path = get_cache_path(url)
        if os.path.exists(cache_path):
            with open(cache_path, "rb") as f:
                cached_response = f.read()
            client_socket.sendall(cached_response)
            print(f"[HIT]  {url} — served from cache")
            return

        # Parse the URL and fetch from origin
        hostname, port, path = parse_url(url)
        print(f"[FETCH] {url} → {hostname}:{port}{path}")

        response = fetch_from_origin(hostname, port, path)

        # Cache the response
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(cache_path, "wb") as f:
            f.write(response)
        print(f"[CACHE] Stored: {cache_path}")

        # Relay response to client
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
    """Start the proxy server.

    Args:
        port: TCP port to listen on.
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
