"""
Web Server — Skeleton Code

A simple multi-threaded HTTP web server.

Usage:
    python3 server_skeleton.py [port]

The server serves files from the current working directory.
Default port is 6789.
"""

import socket
import sys
import threading


def handle_client(connection_socket: socket.socket, address: tuple) -> None:
    """Handle a single HTTP request from a client.

    Steps:
        1. Receive the HTTP request message from the client
        2. Parse the request to extract the requested file path
        3. Read the file from disk (or determine it does not exist)
        4. Build and send the appropriate HTTP response
        5. Close the connection

    Args:
        connection_socket: The TCP socket connected to the client.
        address: The (host, port) tuple of the client.
    """
    try:
        # --- Step 1: Receive the request message ---
        message = connection_socket.recv(4096).decode()
        print(f"[INFO] Request from {address}:\n{message.splitlines()[0]}")

        # --- Step 2: Extract the requested filename ---
        # TODO: Parse the first line of the HTTP request to get the filename.
        #       The request line looks like: GET /hello.html HTTP/1.1
        filename = ""  # Fill in

        # --- Step 3: Open and read the requested file ---
        # TODO: Open the file in binary mode ("rb") and read its contents.
        #       If the file is not found, raise a FileNotFoundError (or IOError).

        # --- Step 4: Build and send the HTTP 200 OK response ---
        # TODO: Construct the response header and send it along with the file
        #       contents back to the client.
        #       Header format:
        #           HTTP/1.1 200 OK\r\n
        #           Content-Type: text/html\r\n
        #           \r\n

        pass  # Replace with your implementation

    except FileNotFoundError:
        # --- Step 4 (alt): Build and send the HTTP 404 response ---
        # TODO: Send an HTTP 404 Not Found response with a simple error page.
        pass  # Replace with your implementation

    finally:
        # --- Step 5: Close the connection ---
        connection_socket.close()


def main(port: int = 6789) -> None:
    """Start the web server.

    Args:
        port: The TCP port number to listen on.
    """
    # --- Create a TCP server socket ---
    # TODO: Create a socket using socket.AF_INET and socket.SOCK_STREAM.
    #       Bind it to ('', port) and start listening.
    #       Hint: Use socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #       to allow port reuse.

    server_socket = None  # Replace with your socket

    print(f"[INFO] Web server starting on port {port} ...")
    print(f"[INFO] Open http://localhost:{port}/hello.html in your browser")
    print("[INFO] Press Ctrl+C to stop the server\n")

    try:
        while True:
            # --- Accept an incoming connection ---
            # TODO: Accept a connection and spawn a new thread to handle it.
            #       Use threading.Thread with target=handle_client.

            pass  # Replace with your implementation
    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down.")
    finally:
        if server_socket:
            server_socket.close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 6789
    main(port)
