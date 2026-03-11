"""
SMTP Mail Client 정답 구현.

raw SMTP command를 TCP socket 위에서 직접 보내 메일을 전송한다.

Usage:
    python3 smtp_client.py <server> <port> <sender> <recipient>

Example:
    python3 smtp_client.py localhost 1025 alice@example.com bob@example.com
"""

import socket
import sys


def recv_reply(sock: socket.socket) -> str:
    """SMTP server의 응답을 읽어 반환한다.

    Args:
        sock: SMTP server에 연결된 TCP socket.

    Returns:
        decode된 server 응답 문자열.
    """
    reply = sock.recv(4096).decode()
    print(f"S: {reply.strip()}")
    return reply


def send_command(sock: socket.socket, command: str) -> str:
    """SMTP command를 보내고 server 응답을 반환한다.

    Args:
        sock: SMTP server에 연결된 TCP socket.
        command: CRLF를 제외한 SMTP command 문자열.

    Returns:
        decode된 server 응답 문자열.
    """
    print(f"C: {command}")
    sock.sendall(f"{command}\r\n".encode())
    return recv_reply(sock)


def check_reply(reply: str, expected_code: str) -> None:
    """응답이 기대한 status code로 시작하는지 확인한다.

    Args:
        reply: server에서 받은 원본 응답 문자열.
        expected_code: 기대하는 3자리 reply code.

    Raises:
        RuntimeError: reply code가 기대값과 다를 때.
    """
    if not reply.startswith(expected_code):
        raise RuntimeError(
            f"Expected {expected_code}, got: {reply.strip()}"
        )


def main(server: str, port: int, sender: str, recipient: str) -> None:
    """메일 전송을 위한 SMTP 대화를 끝까지 수행한다.

    Args:
        server: SMTP server hostname.
        port: SMTP server port.
        sender: 발신자 email address.
        recipient: 수신자 email address.
    """
    print(f"Connecting to {server}:{port} ...\n")

    # TCP 연결을 만든다.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)
    client_socket.connect((server, port))

    # 처음 220 greeting을 받는다.
    greeting = recv_reply(client_socket)
    check_reply(greeting, "220")

    # HELO를 보낸다.
    reply = send_command(client_socket, f"HELO {socket.gethostname()}")
    check_reply(reply, "250")

    # MAIL FROM을 보낸다.
    reply = send_command(client_socket, f"MAIL FROM:<{sender}>")
    check_reply(reply, "250")

    # RCPT TO를 보낸다.
    reply = send_command(client_socket, f"RCPT TO:<{recipient}>")
    check_reply(reply, "250")

    # DATA 단계로 진입한다.
    reply = send_command(client_socket, "DATA")
    check_reply(reply, "354")

    # 메일 본문 전체를 전송한다.
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

    # 마지막으로 QUIT를 보낸다.
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
