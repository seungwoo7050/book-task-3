"""
SMTP Mail Client — Complete Solution

Sends an email using raw SMTP commands over a TCP socket.

Usage:
    python3 smtp_client.py <server> <port> <sender> <recipient>

Example:
    python3 smtp_client.py localhost 1025 alice@example.com bob@example.com
"""

import socket
import sys


def recv_reply(sock: socket.socket) -> str:
    """Receive and return the SMTP server's reply.

    Args:
        sock: The TCP socket connected to the SMTP server.

    Returns:
        The server's reply as a decoded string.
    """
    reply = sock.recv(4096).decode()
    print(f"S: {reply.strip()}")
    return reply


def send_command(sock: socket.socket, command: str) -> str:
    """Send an SMTP command and return the server's reply.

    Args:
        sock: The TCP socket connected to the SMTP server.
        command: The SMTP command string (without CRLF).

    Returns:
        The server's reply as a decoded string.
    """
    print(f"C: {command}")
    sock.sendall(f"{command}\r\n".encode())
    return recv_reply(sock)


def check_reply(reply: str, expected_code: str) -> None:
    """Verify that the reply starts with the expected status code.

    Args:
        reply: The raw reply string from the server.
        expected_code: The expected 3-digit reply code.

    Raises:
        RuntimeError: If the reply code does not match.
    """
    if not reply.startswith(expected_code):
        raise RuntimeError(
            f"Expected {expected_code}, got: {reply.strip()}"
        )


def main(server: str, port: int, sender: str, recipient: str) -> None:
    """Conduct a complete SMTP dialogue to send an email.

    Args:
        server: SMTP server hostname.
        port: SMTP server port.
        sender: Sender email address.
        recipient: Recipient email address.
    """
    print(f"Connecting to {server}:{port} ...\n")

    # Create TCP connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)
    client_socket.connect((server, port))

    # Receive the 220 greeting
    greeting = recv_reply(client_socket)
    check_reply(greeting, "220")

    # HELO
    reply = send_command(client_socket, f"HELO {socket.gethostname()}")
    check_reply(reply, "250")

    # MAIL FROM
    reply = send_command(client_socket, f"MAIL FROM:<{sender}>")
    check_reply(reply, "250")

    # RCPT TO
    reply = send_command(client_socket, f"RCPT TO:<{recipient}>")
    check_reply(reply, "250")

    # DATA
    reply = send_command(client_socket, "DATA")
    check_reply(reply, "354")

    # Send the email message
    subject = "Test Email from SMTP Client Assignment"
    body = (
        "Hello!\n"
        "\n"
        "This email was sent using a raw SMTP socket client\n"
        "as part of the Computer Networking programming assignment.\n"
        "\n"
        "Best regards,\n"
        "SMTP Client"
    )

    message = (
        f"From: {sender}\r\n"
        f"To: {recipient}\r\n"
        f"Subject: {subject}\r\n"
        f"\r\n"
        f"{body}\r\n"
        f".\r\n"
    )

    print(f"C: (sending message body — {len(body)} bytes)")
    client_socket.sendall(message.encode())
    reply = recv_reply(client_socket)
    check_reply(reply, "250")

    # QUIT
    reply = send_command(client_socket, "QUIT")
    check_reply(reply, "221")

    client_socket.close()
    print("\nEmail sent successfully!")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 smtp_client.py <server> <port> <sender> <recipient>")
        sys.exit(1)

    try:
        main(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])
    except RuntimeError as e:
        print(f"\n[ERROR] SMTP dialogue failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
