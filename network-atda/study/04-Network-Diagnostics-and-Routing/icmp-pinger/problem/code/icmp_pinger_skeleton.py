"""
ICMP Pinger — Skeleton Code

A ping utility using raw ICMP sockets.

Usage:
    sudo python3 icmp_pinger_skeleton.py <host> [-c count]

Requires root/administrator privileges for raw socket access.
"""

import os
import select
import socket
import struct
import sys
import time


ICMP_ECHO_REQUEST = 8  # ICMP Type 8
ICMP_ECHO_REPLY = 0    # ICMP Type 0
ICMP_HEADER_FORMAT = "!BBHHH"  # Type, Code, Checksum, ID, Sequence
ICMP_HEADER_SIZE = struct.calcsize(ICMP_HEADER_FORMAT)


def internet_checksum(data: bytes) -> int:
    """Compute the Internet checksum (RFC 1071).

    Args:
        data: The bytes to checksum.

    Returns:
        The 16-bit checksum value.
    """
    # TODO: Implement the Internet checksum algorithm:
    #   1. Sum all 16-bit words
    #   2. Add carry bits back
    #   3. Take one's complement
    #   Hint: If data has an odd number of bytes, pad with a zero byte.
    return 0  # Replace


def build_echo_request(identifier: int, sequence: int) -> bytes:
    """Build an ICMP Echo Request packet.

    Args:
        identifier: The ICMP identifier field (e.g., process ID).
        sequence: The ICMP sequence number.

    Returns:
        The complete ICMP packet bytes.
    """
    # TODO:
    #   1. Create the ICMP header with checksum = 0
    #   2. Create a payload (e.g., current timestamp as 8 bytes)
    #   3. Compute the checksum over header + payload
    #   4. Rebuild the header with the correct checksum
    #   5. Return header + payload
    return b""  # Replace


def parse_echo_reply(data: bytes, identifier: int) -> tuple[int, float] | None:
    """Parse an ICMP Echo Reply from received data.

    Args:
        data: The raw received bytes (includes IP header).
        identifier: The expected ICMP identifier.

    Returns:
        A tuple (sequence_number, timestamp) if valid, or None.
    """
    # TODO:
    #   1. Skip the IP header (first 20 bytes)
    #   2. Unpack the ICMP header
    #   3. Verify type == 0 (Echo Reply) and identifier matches
    #   4. Extract the timestamp from the payload
    #   5. Return (sequence, timestamp)
    return None  # Replace


def ping(host: str, count: int = 4, timeout: float = 1.0) -> None:
    """Send ICMP Echo Requests and print results.

    Args:
        host: Target hostname or IP address.
        count: Number of pings to send.
        timeout: Timeout in seconds for each ping.
    """
    # TODO:
    #   1. Resolve the hostname to an IP address
    #   2. Create a raw ICMP socket
    #   3. For each ping:
    #      a. Build and send an Echo Request
    #      b. Wait for a reply (using select for timeout)
    #      c. Parse the reply and calculate RTT
    #      d. Print the result
    #   4. Print summary statistics

    print("[TODO] Implement the ping() function")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 icmp_pinger_skeleton.py <host> [-c count]")
        sys.exit(1)

    host = sys.argv[1]
    count = 4
    if "-c" in sys.argv:
        idx = sys.argv.index("-c")
        count = int(sys.argv[idx + 1])

    ping(host, count)
