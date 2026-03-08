"""
SMTP Client — Unit Tests

Usage:
    python3 -m pytest test_smtp_client.py -v

Prerequisites:
    A local SMTP debug server must be running on localhost:1025:
        python3 -m smtpd -n -c DebuggingServer localhost:1025
"""

import socket
import pytest

HOST = "localhost"
PORT = 1025


class TestSMTPClient:
    """Tests for the SMTP Client."""

    def test_server_greeting(self):
        """SMTP server should respond with 220 greeting on connect."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((HOST, PORT))
            greeting = sock.recv(1024).decode()
            assert greeting.startswith("220")
        finally:
            sock.close()

    def test_helo_command(self):
        """Server should reply 250 to HELO."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((HOST, PORT))
            sock.recv(1024)  # greeting
            sock.sendall(b"HELO localhost\r\n")
            reply = sock.recv(1024).decode()
            assert reply.startswith("250")
        finally:
            sock.close()

    def test_full_smtp_dialogue(self):
        """Complete SMTP dialogue should succeed."""
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
