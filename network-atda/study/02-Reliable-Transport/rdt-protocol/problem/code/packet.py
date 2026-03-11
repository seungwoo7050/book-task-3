"""
Packet Utilities (Provided)

Provides functions for creating, parsing, and verifying RDT packets.

Packet format:
    [checksum: 4 bytes][seq_num: 4 bytes][payload: variable]

Usage:
    from packet import make_packet, parse_packet, is_corrupt, make_ack
"""

import hashlib
import struct


def compute_checksum(seq_num: int, payload: bytes) -> bytes:
    """Compute a 4-byte checksum over the sequence number and payload.

    Args:
        seq_num: The packet sequence number.
        payload: The packet payload bytes.

    Returns:
        4-byte checksum.
    """
    data = struct.pack("!I", seq_num) + payload
    return hashlib.md5(data).digest()[:4]


def make_packet(seq_num: int, payload: bytes) -> bytes:
    """Create an RDT packet.

    Args:
        seq_num: Sequence number (integer).
        payload: Payload data (bytes).

    Returns:
        The complete packet bytes: [checksum(4)][seq(4)][payload].
    """
    checksum = compute_checksum(seq_num, payload)
    header = struct.pack("!4sI", checksum, seq_num)
    return header + payload


def parse_packet(packet: bytes) -> tuple[bytes, int, bytes]:
    """Parse an RDT packet into its components.

    Args:
        packet: The raw packet bytes.

    Returns:
        A tuple of (checksum, seq_num, payload).
    """
    checksum = packet[:4]
    seq_num = struct.unpack("!I", packet[4:8])[0]
    payload = packet[8:]
    return checksum, seq_num, payload


def is_corrupt(packet: bytes) -> bool:
    """Check if a packet has been corrupted.

    Recomputes the checksum and compares it to the one in the packet.

    Args:
        packet: The raw packet bytes.

    Returns:
        True if the packet is corrupt, False if it is valid.
    """
    checksum, seq_num, payload = parse_packet(packet)
    expected = compute_checksum(seq_num, payload)
    return checksum != expected


def make_ack(seq_num: int) -> bytes:
    """Create an ACK packet for the given sequence number.

    Args:
        seq_num: The sequence number being acknowledged.

    Returns:
        An ACK packet (payload is b"ACK").
    """
    return make_packet(seq_num, b"ACK")


def is_ack(packet: bytes, expected_seq: int) -> bool:
    """Check if a packet is a valid ACK for the expected sequence number.

    Args:
        packet: The raw packet bytes.
        expected_seq: The expected ACK sequence number.

    Returns:
        True if valid ACK, False otherwise.
    """
    if is_corrupt(packet):
        return False
    _, seq_num, payload = parse_packet(packet)
    return seq_num == expected_seq and payload == b"ACK"
