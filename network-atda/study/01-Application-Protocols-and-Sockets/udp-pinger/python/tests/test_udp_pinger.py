"""
UDP Pinger unit test.

Usage:
    python3 -m pytest test_udp_pinger.py -v

Prerequisites:
    localhost:12000에서 UDP pinger server가 실행 중이어야 한다.
"""

import socket
import time

import pytest

HOST = "127.0.0.1"
PORT = 12000


class TestUDPPinger:
    """UDP Pinger client와 server 상호작용을 확인한다."""

    def test_server_responds_to_ping(self):
        """server는 여러 ping 중 일부에는 응답해야 한다."""
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
        # 손실률이 30%여도 10번 중 최소 1번은 응답이 와야 한다.
        assert replies >= 1, "Expected at least one reply from server"

    def test_reply_is_uppercased(self):
        """server 응답은 대문자 형태여야 한다."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)

        # 응답을 받을 확률을 높이기 위해 여러 번 시도한다.
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
        """server가 packet을 버리면 socket timeout이 발생해야 한다."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.01)  # timeout을 강제로 유도할 정도로 짧게 둔다.

        msg = f"Ping 1 {time.time()}"
        sock.sendto(msg.encode(), (HOST, PORT))

        with pytest.raises(socket.timeout):
            sock.recvfrom(1024)

        sock.close()
