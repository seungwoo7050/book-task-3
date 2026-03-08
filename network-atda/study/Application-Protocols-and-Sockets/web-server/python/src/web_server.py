"""
Web Server — Complete Solution

A multi-threaded HTTP web server that serves static files.

Usage:
    python3 web_server.py [port]

Serves files from the current working directory.
Default port is 6789.
"""

import os
import socket
import sys
import threading

# Mapping of file extensions to MIME content types
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
    """Return the MIME content type for a given filename.

    Args:
        filename: The name of the file.

    Returns:
        The MIME type string. Defaults to 'application/octet-stream'.
    """
    _, ext = os.path.splitext(filename)
    return CONTENT_TYPES.get(ext.lower(), "application/octet-stream")


def handle_client(connection_socket: socket.socket, address: tuple) -> None:
    """Handle a single HTTP request from a connected client.

    Parses the HTTP GET request, reads the requested file, and returns
    an HTTP 200 response with the file contents, or an HTTP 404 response
    if the file does not exist.

    Args:
        connection_socket: The TCP socket connected to the client.
        address: The (host, port) tuple identifying the client.
    """
    try:
        # Receive the HTTP request (up to 4 KB)
        message = connection_socket.recv(4096).decode()
        if not message:
            return

        # Parse the request line: "GET /hello.html HTTP/1.1"
        request_line = message.splitlines()[0]
        print(f"[INFO] {address[0]}:{address[1]} — {request_line}")

        tokens = request_line.split()
        if len(tokens) < 2:
            return

        # Extract filename — remove leading '/'
        filename = tokens[1][1:]
        if filename == "":
            filename = "hello.html"  # default page

        # Open and read the requested file
        with open(filename, "rb") as f:
            body = f.read()

        # Build and send the 200 OK response
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
        # Build and send the 404 Not Found response
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
    """Start the multi-threaded web server.

    Args:
        port: TCP port number to listen on.
    """
    # Create a TCP server socket
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
            # Accept a new connection
            connection_socket, address = server_socket.accept()

            # Handle the connection in a new daemon thread
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
