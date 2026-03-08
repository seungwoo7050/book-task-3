"""
RDT Protocol — Unit Tests

Usage:
    python3 -m pytest test_rdt.py -v
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "problem", "code"))

from packet import make_packet, parse_packet, is_corrupt, make_ack, is_ack


class TestPacketModule:
    """Tests for the packet utility module."""

    def test_make_and_parse_packet(self):
        pkt = make_packet(0, b"Hello")
        checksum, seq, payload = parse_packet(pkt)
        assert seq == 0
        assert payload == b"Hello"

    def test_valid_packet_not_corrupt(self):
        pkt = make_packet(1, b"World")
        assert not is_corrupt(pkt)

    def test_corrupted_packet_detected(self):
        pkt = make_packet(0, b"Test")
        # Flip a bit in the payload
        corrupted = bytearray(pkt)
        corrupted[-1] ^= 0xFF
        assert is_corrupt(bytes(corrupted))

    def test_make_ack(self):
        ack = make_ack(0)
        assert not is_corrupt(ack)
        _, seq, payload = parse_packet(ack)
        assert seq == 0
        assert payload == b"ACK"

    def test_is_ack_valid(self):
        ack = make_ack(1)
        assert is_ack(ack, 1)

    def test_is_ack_wrong_seq(self):
        ack = make_ack(0)
        assert not is_ack(ack, 1)

    def test_different_seq_different_checksum(self):
        pkt0 = make_packet(0, b"Same")
        pkt1 = make_packet(1, b"Same")
        cs0, _, _ = parse_packet(pkt0)
        cs1, _, _ = parse_packet(pkt1)
        assert cs0 != cs1
