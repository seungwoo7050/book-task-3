"""
Web Proxy — Skeleton Code

A simple HTTP proxy server with caching.

Usage:
    python3 proxy_skeleton.py [port]

Configure your browser or curl to use localhost:<port> as the HTTP proxy.
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
        url: The absolute URL (e.g., "http://www.example.com:80/index.html").

    Returns:
        A tuple of (hostname, port, path).
    """
    # TODO: Remove the "http://" prefix, extract host:port and path.
    #       Default port is 80 if not specified.
    #       Example: "http://www.example.com/index.html" → ("www.example.com", 80, "/index.html")
    return ("", 80, "/")


def get_cache_path(url: str) -> str:
    """Return the filesystem path for a cached URL.

    Uses an MD5 hash of the URL as the filename.

    Args:
        url: The original request URL.

    Returns:
        The file path in the cache directory.
    """
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{url_hash}.dat")


def handle_client(client_socket: socket.socket, address: tuple) -> None:
    """Handle a single proxy request.

    Steps:
        1. Receive the HTTP request from the client
        2. Parse the URL to extract host, port, and path
        3. Check if the response is cached
        4. If cached, serve from cache
        5. If not cached, forward request to origin server, cache and relay response
        6. Close the client connection

    Args:
        client_socket: Socket connected to the client.
        address: Client's (host, port) tuple.
    """
    try:
        # --- Step 1: Receive the client request ---
        request = client_socket.recv(BUFFER_SIZE).decode()
        if not request:
            return

        # --- Step 2: Parse the request line ---
        # TODO: Extract the URL from the request line (e.g., "GET http://... HTTP/1.1")

        # --- Step 3: Check cache ---
        # TODO: If cached, read and send the cached file to the client.
        #       Print a [HIT] log message.

        # --- Step 4: Forward to origin server ---
        # TODO: Open a TCP connection to the origin server.
        #       Send a modified GET request with a relative path.
        #       Receive the full response.

        # --- Step 5: Cache the response ---
        # TODO: Write the response to the cache file.

        # --- Step 6: Send the response to the client ---
        # TODO: Forward the response to the client.

        pass  # Replace with your implementation

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

    # TODO: Create a TCP server socket, bind, listen, and accept connections
    #       in a loop, spawning threads for each client.

    server_socket = None  # Replace

    print(f"[INFO] Proxy server starting on port {port} ...")
    print(f"[INFO] Use:  curl -x http://localhost:{port} http://www.example.com/")
    print("[INFO] Press Ctrl+C to stop\n")

    try:
        while True:
            pass  # Replace with accept + thread dispatch
    except KeyboardInterrupt:
        print("\n[INFO] Proxy shutting down.")
    finally:
        if server_socket:
            server_socket.close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    main(port)
