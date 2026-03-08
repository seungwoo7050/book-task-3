"""
ICMP Pinger — Complete Solution

A ping utility using raw ICMP sockets.

Usage:
    sudo python3 icmp_pinger.py <host> [-c count]

Requires root/administrator privileges.
"""

import os
import select
import socket
import struct
import sys
import time

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_HEADER_FORMAT = "!BBHHH"
ICMP_HEADER_SIZE = struct.calcsize(ICMP_HEADER_FORMAT)


def internet_checksum(data: bytes) -> int:
    """Compute the Internet checksum (RFC 1071).

    Args:
        data: The bytes to checksum.

    Returns:
        The 16-bit checksum value.
    """
    if len(data) % 2 != 0:
        data += b"\x00"

    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        total += word

    # Fold carries
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)

    return ~total & 0xFFFF


def build_echo_request(identifier: int, sequence: int) -> bytes:
    """Build an ICMP Echo Request packet.

    Args:
        identifier: The ICMP identifier field.
        sequence: The ICMP sequence number.

    Returns:
        The complete ICMP packet bytes.
    """
    # Header with checksum = 0 (placeholder)
    header = struct.pack(
        ICMP_HEADER_FORMAT,
        ICMP_ECHO_REQUEST,  # Type
        0,                   # Code
        0,                   # Checksum (placeholder)
        identifier,          # Identifier
        sequence,            # Sequence
    )

    # Payload: current timestamp as a double (8 bytes)
    payload = struct.pack("!d", time.time())

    # Compute checksum
    checksum = internet_checksum(header + payload)

    # Rebuild header with correct checksum
    header = struct.pack(
        ICMP_HEADER_FORMAT,
        ICMP_ECHO_REQUEST,
        0,
        checksum,
        identifier,
        sequence,
    )

    return header + payload


def parse_echo_reply(
    data: bytes, identifier: int
) -> tuple[int, float] | None:
    """Parse an ICMP Echo Reply from received data.

    Args:
        data: Raw received bytes (includes IP header).
        identifier: Expected ICMP identifier to match.

    Returns:
        (sequence_number, send_timestamp) if valid, None otherwise.
    """
    # Determine IP header length
    ip_header_len = (data[0] & 0x0F) * 4

    # Extract ICMP header
    icmp_data = data[ip_header_len:]
    if len(icmp_data) < ICMP_HEADER_SIZE:
        return None

    icmp_type, code, checksum, pkt_id, sequence = struct.unpack(
        ICMP_HEADER_FORMAT, icmp_data[:ICMP_HEADER_SIZE]
    )

    # Verify it's an Echo Reply for us
    if icmp_type != ICMP_ECHO_REPLY or pkt_id != identifier:
        return None

    # Extract timestamp from payload
    payload = icmp_data[ICMP_HEADER_SIZE:]
    if len(payload) < 8:
        return None

    send_time = struct.unpack("!d", payload[:8])[0]
    return sequence, send_time


def ping(host: str, count: int = 4, timeout: float = 1.0) -> None:
    """Send ICMP Echo Requests and print results.

    Args:
        host: Target hostname or IP address.
        count: Number of pings to send.
        timeout: Timeout in seconds for each ping.
    """
    # Resolve hostname
    try:
        dest_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"ping: cannot resolve {host}: Unknown host")
        sys.exit(1)

    identifier = os.getpid() & 0xFFFF

    print(f"PING {host} ({dest_ip}): {ICMP_HEADER_SIZE + 8} bytes of data\n")

    # Create raw socket
    try:
        raw_socket = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP
        )
    except PermissionError:
        print("Error: Raw socket requires root privileges.")
        print("Run with: sudo python3 icmp_pinger.py <host>")
        sys.exit(1)

    rtt_list: list[float] = []

    for seq in range(1, count + 1):
        # Build and send Echo Request
        packet = build_echo_request(identifier, seq)
        send_time = time.time()
        raw_socket.sendto(packet, (dest_ip, 0))

        # Wait for reply
        ready, _, _ = select.select([raw_socket], [], [], timeout)

        if ready:
            recv_time = time.time()
            data, addr = raw_socket.recvfrom(1024)

            result = parse_echo_reply(data, identifier)
            if result:
                reply_seq, embedded_time = result
                rtt_ms = (recv_time - embedded_time) * 1000
                rtt_list.append(rtt_ms)
                packet_size = len(data) - ((data[0] & 0x0F) * 4)
                print(
                    f"{packet_size} bytes from {addr[0]}: "
                    f"icmp_seq={reply_seq}  RTT={rtt_ms:.3f} ms"
                )
            else:
                print(f"Ping {seq}: Unexpected reply")
        else:
            print(f"Ping {seq}: Request timed out")

        # Wait 1 second between pings (unless last)
        if seq < count:
            time.sleep(max(0, 1.0 - (time.time() - send_time)))

    raw_socket.close()

    # Print statistics
    sent = count
    received = len(rtt_list)
    lost = sent - received
    loss_pct = (lost / sent) * 100

    print(f"\n--- {host} ping statistics ---")
    print(f"{sent} packets sent, {received} received, {loss_pct:.1f}% loss")

    if rtt_list:
        min_rtt = min(rtt_list)
        max_rtt = max(rtt_list)
        avg_rtt = sum(rtt_list) / len(rtt_list)
        print(f"RTT min/avg/max = {min_rtt:.3f}/{avg_rtt:.3f}/{max_rtt:.3f} ms")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 icmp_pinger.py <host> [-c count]")
        sys.exit(1)

    target_host = sys.argv[1]
    ping_count = 4

    if "-c" in sys.argv:
        idx = sys.argv.index("-c")
        ping_count = int(sys.argv[idx + 1])

    ping(target_host, ping_count)
