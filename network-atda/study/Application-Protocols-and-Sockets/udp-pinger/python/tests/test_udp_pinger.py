"""
UDP Pinger — Unit Tests

Usage:
    python3 -m pytest test_udp_pinger.py -v

Prerequisites:
    The UDP pinger server must be running on localhost:12000.
"""

import socket
import time

import pytest

HOST = "127.0.0.1"
PORT = 12000


class TestUDPPinger:
    """Tests for the UDP Pinger client logic."""

    def test_server_responds_to_ping(self):
        """Server should echo back at least some pings."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        replies = 0

        for seq in range(1, 11):
            msg = f"Ping {seq} {time.time()}"
            sock.sendto(msg.encode(), (HOST, PORT))
            try:
                data, _ = sock.recvfrom(1024)
                replies += 1
            except socket.timeout:
                pass

        sock.close()
        # With 30% simulated loss, expect at least 1 reply out of 10
        assert replies >= 1, "Expected at least one reply from server"

    def test_reply_is_uppercased(self):
        """Server echoes the message in uppercase."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)

        # Send multiple to increase chance of reply
        for seq in range(1, 11):
            msg = f"Ping {seq} {time.time()}"
            sock.sendto(msg.encode(), (HOST, PORT))
            try:
                data, _ = sock.recvfrom(1024)
                assert data.decode().startswith("PING")
                sock.close()
                return
            except socket.timeout:
                pass

        sock.close()
        pytest.skip("All packets were dropped by server (unlikely but possible)")

    def test_timeout_occurs_for_lost_packets(self):
        """Socket timeout should be raised when server drops a packet."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.01)  # Very short timeout to force a "timeout"

        msg = f"Ping 1 {time.time()}"
        sock.sendto(msg.encode(), (HOST, PORT))

        with pytest.raises(socket.timeout):
            sock.recvfrom(1024)

        sock.close()
