"""Traceroute tests that avoid opening real raw sockets."""

from pathlib import Path
import socket
import struct
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "python" / "src"))

import traceroute
from traceroute import ProbeObservation, build_probe_port, format_hop_line, parse_icmp_response


def _build_icmp_packet(dest_port: int, icmp_type: int = 11, icmp_code: int = 0) -> bytes:
    outer_ip = bytearray(20)
    outer_ip[0] = 0x45

    icmp_header = struct.pack("!BBHI", icmp_type, icmp_code, 0, 0)

    embedded_ip = bytearray(20)
    embedded_ip[0] = 0x45
    embedded_ip[9] = socket.IPPROTO_UDP

    udp_header = struct.pack("!HHHH", 50000, dest_port, 8, 0)
    return bytes(outer_ip) + icmp_header + bytes(embedded_ip) + udp_header


def test_build_probe_port_increments_per_hop_and_probe():
    assert build_probe_port(1, 0, 3) == 33434
    assert build_probe_port(1, 2, 3) == 33436
    assert build_probe_port(2, 0, 3) == 33437


def test_parse_icmp_response_extracts_embedded_udp_port():
    packet = _build_icmp_packet(33440, icmp_type=3, icmp_code=3)
    assert parse_icmp_response(packet) == (3, 3, 33440)


def test_format_hop_line_handles_mixed_results():
    line = format_hop_line(
        3,
        [
            ProbeObservation("10.0.0.1", 12.345, 11, 0),
            ProbeObservation(None, None, None, None),
            ProbeObservation("10.0.0.1", 12.876, 11, 0),
        ],
    )
    assert line.startswith(" 3")
    assert "*" in line
    assert "10.0.0.1" in line


class FakeClock:
    """Return a fixed increment each time trace_route queries time."""

    def __init__(self, start: float = 1000.0, step: float = 0.01):
        self.current = start - step
        self.step = step

    def time(self) -> float:
        self.current += self.step
        return self.current


def _build_trace_reply(dest_port: int, icmp_type: int, icmp_code: int) -> bytes:
    outer_ip = bytearray(20)
    outer_ip[0] = 0x45

    icmp_header = struct.pack("!BBHI", icmp_type, icmp_code, 0, 0)

    embedded_ip = bytearray(20)
    embedded_ip[0] = 0x45
    embedded_ip[9] = socket.IPPROTO_UDP

    udp_header = struct.pack("!HHHH", 50000, dest_port, 8, 0)
    return bytes(outer_ip) + icmp_header + bytes(embedded_ip) + udp_header


class FakeRecvSocket:
    def __init__(self, route_map: dict[int, tuple[str, int, int]]):
        self.route_map = route_map
        self.queue: list[tuple[bytes, tuple[str, int]]] = []
        self.closed = False
        self.timeout = None

    def settimeout(self, timeout: float) -> None:
        self.timeout = timeout

    def queue_reply(self, ttl: int, port: int) -> None:
        responder, icmp_type, icmp_code = self.route_map[ttl]
        self.queue.append((_build_trace_reply(port, icmp_type, icmp_code), (responder, 0)))

    def recvfrom(self, _: int) -> tuple[bytes, tuple[str, int]]:
        if not self.queue:
            raise socket.timeout
        return self.queue.pop(0)

    def close(self) -> None:
        self.closed = True


class FakeSendSocket:
    def __init__(self, recv_socket: FakeRecvSocket):
        self.recv_socket = recv_socket
        self.ttl = None
        self.closed = False

    def setsockopt(self, _level: int, option: int, value: int) -> None:
        if option == socket.IP_TTL:
            self.ttl = value

    def sendto(self, _payload: bytes, address: tuple[str, int]) -> None:
        _host, port = address
        if self.ttl in self.recv_socket.route_map:
            self.recv_socket.queue_reply(self.ttl, port)

    def close(self) -> None:
        self.closed = True


def test_trace_route_returns_hops_until_destination(monkeypatch):
    route_map = {
        1: ("10.0.0.1", 11, 0),
        2: ("10.0.1.1", 11, 0),
        3: ("203.0.113.9", 3, 3),
    }
    recv_socket = FakeRecvSocket(route_map)
    fake_clock = FakeClock()

    def fake_socket_factory(_family, sock_type, protocol):
        if sock_type == socket.SOCK_RAW and protocol == socket.IPPROTO_ICMP:
            return recv_socket
        if sock_type == socket.SOCK_DGRAM and protocol == socket.IPPROTO_UDP:
            return FakeSendSocket(recv_socket)
        raise AssertionError("unexpected socket arguments")

    monkeypatch.setattr(traceroute.socket, "gethostbyname", lambda host: "203.0.113.9")
    monkeypatch.setattr(traceroute.socket, "socket", fake_socket_factory)
    monkeypatch.setattr(traceroute.time, "time", fake_clock.time)

    lines = traceroute.trace_route("example.com", max_hops=6, probes_per_hop=2, timeout=0.2)

    assert lines[0] == "traceroute to example.com (203.0.113.9), 6 hops max"
    assert "10.0.0.1" in lines[1]
    assert "10.0.1.1" in lines[2]
    assert "203.0.113.9" in lines[3]
    assert len(lines) == 4
    assert recv_socket.timeout == 0.2
    assert recv_socket.closed is True
