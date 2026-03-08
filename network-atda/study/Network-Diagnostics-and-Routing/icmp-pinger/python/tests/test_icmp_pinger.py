"""ICMP pinger tests that avoid opening real raw sockets."""

from __future__ import annotations

import os
import struct
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import icmp_pinger
from icmp_pinger import (
    ICMP_HEADER_SIZE,
    build_echo_request,
    internet_checksum,
)


class TestInternetChecksum:
    """Tests for the Internet checksum algorithm."""

    def test_known_value(self):
        """Checksum of a known byte sequence."""
        data = b"\x45\x00\x00\x3c\x1c\x46\x40\x00\x40\x06"
        cs = internet_checksum(data)
        assert isinstance(cs, int)
        assert 0 <= cs <= 0xFFFF

    def test_all_zeros(self):
        """Checksum of all zeros should be 0xFFFF."""
        data = b"\x00\x00\x00\x00"
        cs = internet_checksum(data)
        assert cs == 0xFFFF

    def test_verify_checksum_is_zero(self):
        """Including the checksum in recomputation should yield 0."""
        data = b"\x08\x00\x00\x00\x00\x01\x00\x01"
        cs = internet_checksum(data)
        # Pack checksum into the data
        verified = data[:2] + struct.pack("!H", cs) + data[4:]
        assert internet_checksum(verified) == 0

    def test_odd_length_data(self):
        """Odd-length data should be padded and computed correctly."""
        data = b"\x01\x02\x03"
        cs = internet_checksum(data)
        assert isinstance(cs, int)
        assert 0 <= cs <= 0xFFFF


class TestPacketBuilding:
    """Tests for ICMP packet construction."""

    def test_packet_length(self):
        """Packet should be header (8 bytes) + payload (8 bytes)."""
        pkt = build_echo_request(1234, 1)
        assert len(pkt) == ICMP_HEADER_SIZE + 8

    def test_packet_type_field(self):
        """First byte should be type 8 (Echo Request)."""
        pkt = build_echo_request(1234, 1)
        assert pkt[0] == 8

    def test_packet_code_field(self):
        """Second byte should be code 0."""
        pkt = build_echo_request(1234, 1)
        assert pkt[1] == 0

    def test_checksum_valid(self):
        """Recomputing checksum over the whole packet should yield 0."""
        pkt = build_echo_request(1234, 1)
        assert internet_checksum(pkt) == 0

    def test_identifier_and_sequence(self):
        """Identifier and sequence should be correctly packed."""
        pkt = build_echo_request(0xABCD, 42)
        _, _, _, pkt_id, seq = struct.unpack("!BBHHH", pkt[:ICMP_HEADER_SIZE])
        assert pkt_id == 0xABCD
        assert seq == 42


class FakeClock:
    """Return a predictable time sequence for RTT assertions."""

    def __init__(self, *values: float):
        self._values = list(values)
        self._last = values[-1] if values else 0.0
        self.sleeps: list[float] = []

    def time(self) -> float:
        if self._values:
            self._last = self._values.pop(0)
        return self._last

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)


class FakeRawSocket:
    """A fake raw socket that can queue echo replies by sequence number."""

    def __init__(self, response_sequences: set[int], responder_ip: str = "203.0.113.7"):
        self.response_sequences = response_sequences
        self.responder_ip = responder_ip
        self.sent_packets: list[tuple[bytes, tuple[str, int]]] = []
        self.recv_queue: list[tuple[bytes, tuple[str, int]]] = []
        self.closed = False

    def sendto(self, packet: bytes, address: tuple[str, int]) -> None:
        self.sent_packets.append((packet, address))
        _, _, _, identifier, sequence = struct.unpack("!BBHHH", packet[:ICMP_HEADER_SIZE])
        if sequence in self.response_sequences:
            ip_header = bytearray(20)
            ip_header[0] = 0x45
            reply_header = struct.pack("!BBHHH", 0, 0, 0, identifier, sequence)
            payload = packet[ICMP_HEADER_SIZE:]
            self.recv_queue.append((bytes(ip_header) + reply_header + payload, (self.responder_ip, 0)))

    def recvfrom(self, _: int) -> tuple[bytes, tuple[str, int]]:
        return self.recv_queue.pop(0)

    def close(self) -> None:
        self.closed = True


def _fake_select(readable, *_args):
    sock = readable[0]
    return ([sock], [], []) if sock.recv_queue else ([], [], [])


def test_ping_prints_successful_reply_and_loss_stats(monkeypatch, capsys):
    fake_socket = FakeRawSocket({1})
    fake_clock = FakeClock(1000.0, 1000.0, 1000.05, 1000.10, 1001.0, 1001.0)

    monkeypatch.setattr(icmp_pinger.socket, "gethostbyname", lambda host: "203.0.113.10")
    monkeypatch.setattr(icmp_pinger.socket, "socket", lambda *args, **kwargs: fake_socket)
    monkeypatch.setattr(icmp_pinger.select, "select", _fake_select)
    monkeypatch.setattr(icmp_pinger.os, "getpid", lambda: 0x1234)
    monkeypatch.setattr(icmp_pinger.time, "time", fake_clock.time)
    monkeypatch.setattr(icmp_pinger.time, "sleep", fake_clock.sleep)

    icmp_pinger.ping("example.com", count=2, timeout=1.0)

    output = capsys.readouterr().out
    assert "PING example.com (203.0.113.10)" in output
    assert "icmp_seq=1" in output
    assert "Request timed out" in output
    assert "2 packets sent, 1 received, 50.0% loss" in output
    assert "RTT min/avg/max = 50.000/50.000/50.000 ms" in output
    assert len(fake_socket.sent_packets) == 2
    assert fake_socket.closed is True
    assert fake_clock.sleeps == [pytest.approx(0.9)]


def test_ping_handles_total_packet_loss_without_rtt_summary(monkeypatch, capsys):
    fake_socket = FakeRawSocket(set())
    fake_clock = FakeClock(2000.0, 2000.0)

    monkeypatch.setattr(icmp_pinger.socket, "gethostbyname", lambda host: "198.51.100.10")
    monkeypatch.setattr(icmp_pinger.socket, "socket", lambda *args, **kwargs: fake_socket)
    monkeypatch.setattr(icmp_pinger.select, "select", _fake_select)
    monkeypatch.setattr(icmp_pinger.os, "getpid", lambda: 0x5678)
    monkeypatch.setattr(icmp_pinger.time, "time", fake_clock.time)
    monkeypatch.setattr(icmp_pinger.time, "sleep", fake_clock.sleep)

    icmp_pinger.ping("example.net", count=1, timeout=0.2)

    output = capsys.readouterr().out
    assert "1 packets sent, 0 received, 100.0% loss" in output
    assert "RTT min/avg/max" not in output
    assert fake_socket.closed is True
