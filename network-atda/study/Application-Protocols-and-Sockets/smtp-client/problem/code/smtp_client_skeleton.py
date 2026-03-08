"""
SMTP Mail Client — Skeleton Code

Sends an email via raw SMTP commands over a TCP socket.

Usage:
    python3 smtp_client_skeleton.py <server> <port> <sender> <recipient>

Example:
    python3 smtp_client_skeleton.py localhost 1025 alice@example.com bob@example.com
"""

import socket
import sys


def send_command(sock: socket.socket, command: str) -> str:
    """Send an SMTP command and return the server's reply.

    Args:
        sock: The TCP socket connected to the SMTP server.
        command: The SMTP command string (without trailing CRLF).

    Returns:
        The server's reply as a decoded string.
    """
    # TODO: Send the command (append \r\n), receive and return the reply.
    pass


def check_reply(reply: str, expected_code: str) -> None:
    """Verify that the server's reply starts with the expected code.

    Args:
        reply: The raw reply string from the server.
        expected_code: The expected 3-digit reply code (e.g., "250").

    Raises:
        Exception: If the reply code does not match.
    """
    # TODO: Check if reply starts with expected_code. If not, raise an error.
    pass


def main(server: str, port: int, sender: str, recipient: str) -> None:
    """Conduct an SMTP dialogue to send an email.

    Args:
        server: SMTP server hostname.
        port: SMTP server port.
        sender: Sender email address.
        recipient: Recipient email address.
    """
    print(f"Connecting to {server}:{port} ...")

    # --- Step 1: Create TCP connection ---
    # TODO: Create a TCP socket and connect to (server, port).
    #       Receive the initial 220 greeting.

    client_socket = None  # Replace with your socket

    # --- Step 2: HELO ---
    # TODO: Send HELO command and verify 250 reply.

    # --- Step 3: MAIL FROM ---
    # TODO: Send MAIL FROM command and verify 250 reply.

    # --- Step 4: RCPT TO ---
    # TODO: Send RCPT TO command and verify 250 reply.

    # --- Step 5: DATA ---
    # TODO: Send DATA command and verify 354 reply.

    # --- Step 6: Send message body ---
    # TODO: Send the email headers (From, To, Subject), a blank line,
    #       the body, and terminate with \r\n.\r\n
    #       Verify 250 reply.

    # --- Step 7: QUIT ---
    # TODO: Send QUIT command and verify 221 reply.

    print("Email sent successfully!")

    if client_socket:
        client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 smtp_client_skeleton.py <server> <port> <sender> <recipient>")
        sys.exit(1)

    main(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])
