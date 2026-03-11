"""
SMTP Client unit test.

Usage:
    python3 -m pytest test_smtp_client.py -v

Prerequisites:
    localhost:1025에서 local SMTP debug server가 실행 중이어야 한다.
        python3 -m smtpd -n -c DebuggingServer localhost:1025
"""

import socket
import pytest

HOST = "localhost"
PORT = 1025


class TestSMTPClient:
    """SMTP Client 동작을 확인하는 test 모음."""

    def test_server_greeting(self):
        """연결 직후 SMTP server는 220 greeting을 보내야 한다."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((HOST, PORT))
            greeting = sock.recv(1024).decode()
            assert greeting.startswith("220")
        finally:
            sock.close()

    def test_helo_command(self):
        """HELO에 대해 server는 250으로 응답해야 한다."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((HOST, PORT))
            sock.recv(1024)  # 초기 greeting을 소비한다.
            sock.sendall(b"HELO localhost\r\n")
            reply = sock.recv(1024).decode()
            assert reply.startswith("250")
        finally:
            sock.close()

    def test_full_smtp_dialogue(self):
        """전체 SMTP dialogue가 정상적으로 완료되어야 한다."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((HOST, PORT))
            greeting = sock.recv(1024).decode()
            assert greeting.startswith("220")

            sock.sendall(b"HELO localhost\r\n")
            assert sock.recv(1024).decode().startswith("250")

            sock.sendall(b"MAIL FROM:<test@example.com>\r\n")
            assert sock.recv(1024).decode().startswith("250")

            sock.sendall(b"RCPT TO:<recipient@example.com>\r\n")
            assert sock.recv(1024).decode().startswith("250")

            sock.sendall(b"DATA\r\n")
            assert sock.recv(1024).decode().startswith("354")

            sock.sendall(
                b"From: test@example.com\r\n"
                b"To: recipient@example.com\r\n"
                b"Subject: Test\r\n"
                b"\r\n"
                b"Test body\r\n"
                b".\r\n"
            )
            assert sock.recv(1024).decode().startswith("250")

            sock.sendall(b"QUIT\r\n")
            assert sock.recv(1024).decode().startswith("221")
        finally:
            sock.close()
