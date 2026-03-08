"""
Traceroute — Complete Solution

Discover the path to a target host using UDP probes and ICMP replies.

Usage:
    sudo python3 traceroute.py <host> [--max-hops N] [--probes N] [--timeout SEC]
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import socket
import struct
import sys
import time

DEFAULT_BASE_PORT = 33434


@dataclass
class ProbeObservation:
    responder: str | None
    rtt_ms: float | None
    icmp_type: int | None
    icmp_code: int | None


def build_probe_port(ttl: int, probe_index: int, probes_per_hop: int, base_port: int = DEFAULT_BASE_PORT) -> int:
    """Return a stable UDP destination port for a probe."""
    return base_port + (ttl - 1) * probes_per_hop + probe_index


def parse_icmp_response(packet: bytes) -> tuple[int, int, int | None] | None:
    """Return (icmp_type, icmp_code, embedded_udp_dest_port) for a raw ICMP reply."""
    if len(packet) < 20:
        return None

    ip_header_len = (packet[0] & 0x0F) * 4
    if len(packet) < ip_header_len + 8:
        return None

    icmp_type = packet[ip_header_len]
    icmp_code = packet[ip_header_len + 1]

    embedded_ip_offset = ip_header_len + 8
    if len(packet) < embedded_ip_offset + 20:
        return icmp_type, icmp_code, None

    embedded_ip_header_len = (packet[embedded_ip_offset] & 0x0F) * 4
    udp_offset = embedded_ip_offset + embedded_ip_header_len
    if len(packet) < udp_offset + 4:
        return icmp_type, icmp_code, None

    _, dest_port = struct.unpack("!HH", packet[udp_offset:udp_offset + 4])
    return icmp_type, icmp_code, dest_port


def format_hop_line(ttl: int, observations: list[ProbeObservation]) -> str:
    """Format a traceroute hop for terminal output."""
    probe_parts = []
    responders: list[str] = []
    for observation in observations:
        if observation.responder is None or observation.rtt_ms is None:
            probe_parts.append("*")
            continue
        probe_parts.append(f"{observation.rtt_ms:.3f} ms")
        if observation.responder not in responders:
            responders.append(observation.responder)

    suffix = f"  {' / '.join(responders)}" if responders else ""
    return f"{ttl:2d}  {'  '.join(probe_parts)}{suffix}"


def resolve_target(host: str) -> str:
    """Resolve a hostname into an IPv4 address."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror as exc:
        raise RuntimeError(f"cannot resolve {host}") from exc


def trace_route(
    host: str,
    max_hops: int = 30,
    probes_per_hop: int = 3,
    timeout: float = 1.0,
    base_port: int = DEFAULT_BASE_PORT,
) -> list[str]:
    """Trace a route and return the rendered hop lines."""
    destination_ip = resolve_target(host)
    lines = [f"traceroute to {host} ({destination_ip}), {max_hops} hops max"]

    try:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError as exc:
        raise RuntimeError("raw ICMP socket requires sudo or root privileges") from exc

    recv_socket.settimeout(timeout)

    try:
        for ttl in range(1, max_hops + 1):
            observations: list[ProbeObservation] = []

            for probe_index in range(probes_per_hop):
                port = build_probe_port(ttl, probe_index, probes_per_hop, base_port)
                send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

                sent_at = time.time()
                send_socket.sendto(b"trace-probe", (destination_ip, port))

                observation = ProbeObservation(None, None, None, None)
                try:
                    while True:
                        packet, address = recv_socket.recvfrom(2048)
                        parsed = parse_icmp_response(packet)
                        if parsed is None:
                            continue
                        icmp_type, icmp_code, embedded_port = parsed
                        if embedded_port != port:
                            continue

                        observation = ProbeObservation(
                            responder=address[0],
                            rtt_ms=(time.time() - sent_at) * 1000,
                            icmp_type=icmp_type,
                            icmp_code=icmp_code,
                        )
                        break
                except socket.timeout:
                    pass
                finally:
                    send_socket.close()

                observations.append(observation)

            lines.append(format_hop_line(ttl, observations))

            if any(
                observation.responder == destination_ip
                and observation.icmp_type == 3
                and observation.icmp_code == 3
                for observation in observations
            ):
                break
    finally:
        recv_socket.close()

    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Traceroute")
    parser.add_argument("host", help="Target hostname or IPv4 address")
    parser.add_argument("--max-hops", type=int, default=30)
    parser.add_argument("--probes", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=1.0)
    parser.add_argument("--base-port", type=int, default=DEFAULT_BASE_PORT)
    args = parser.parse_args()

    try:
        for line in trace_route(
            args.host,
            max_hops=args.max_hops,
            probes_per_hop=args.probes,
            timeout=args.timeout,
            base_port=args.base_port,
        ):
            print(line)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
