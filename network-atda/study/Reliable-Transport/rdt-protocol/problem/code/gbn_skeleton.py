"""
Go-Back-N (GBN) — Skeleton Code

Implements reliable data transfer using a sliding window with
cumulative ACKs over an unreliable channel.

Usage:
    python3 gbn_skeleton.py [--loss RATE] [--corrupt RATE] [--window N]
"""

import argparse
import time

from channel import UnreliableChannel
from packet import make_packet, parse_packet, is_corrupt, make_ack, is_ack


TIMEOUT = 0.5  # Retransmission timeout in seconds


def gbn_send(channel_to_receiver: UnreliableChannel,
             channel_to_sender: UnreliableChannel,
             data_list: list[str],
             window_size: int = 4) -> None:
    """GBN Sender.

    Args:
        channel_to_receiver: Channel for sending data packets.
        channel_to_sender: Channel for receiving ACKs.
        data_list: List of messages to send.
        window_size: Maximum number of unacknowledged packets (N).
    """
    base = 0         # Oldest unacknowledged packet
    next_seq = 0     # Next sequence number to use
    total = len(data_list)

    # TODO: Implement GBN sender:
    #   1. Send packets within the window [base, base + N)
    #   2. Start timer when base packet is sent
    #   3. On cumulative ACK n: slide base to n+1
    #   4. On timeout: retransmit all packets in [base, next_seq)

    pass  # Replace


def gbn_receive(channel_to_receiver: UnreliableChannel,
                channel_to_sender: UnreliableChannel,
                expected_count: int) -> list[str]:
    """GBN Receiver.

    Args:
        channel_to_receiver: Channel for receiving data packets.
        channel_to_sender: Channel for sending ACKs.
        expected_count: Number of messages expected.

    Returns:
        List of received messages in order.
    """
    received: list[str] = []
    expected_seq = 0

    # TODO: Implement GBN receiver:
    #   1. If packet has expected seq and is not corrupt:
    #      - Deliver to application
    #      - Send ACK for this seq
    #      - Increment expected_seq
    #   2. Otherwise:
    #      - Discard packet
    #      - Resend ACK for (expected_seq - 1)

    return received


def main():
    parser = argparse.ArgumentParser(description="Go-Back-N Demo")
    parser.add_argument("--loss", type=float, default=0.2, help="Loss rate")
    parser.add_argument("--corrupt", type=float, default=0.1, help="Corruption rate")
    parser.add_argument("--window", type=int, default=4, help="Window size (N)")
    args = parser.parse_args()

    try:
        with open("data/test_messages.txt") as f:
            messages = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        messages = ["Hello", "World", "RDT", "Protocol", "Test"]

    print(f"=== Go-Back-N (Window Size = {args.window}) ===")
    print(f"Messages to send: {len(messages)}")
    print(f"Loss rate: {args.loss}, Corruption rate: {args.corrupt}\n")

    ch_data = UnreliableChannel(args.loss, args.corrupt)
    ch_ack = UnreliableChannel(args.loss, args.corrupt)

    print("[TODO] Implement gbn_send() and gbn_receive()")


if __name__ == "__main__":
    main()
