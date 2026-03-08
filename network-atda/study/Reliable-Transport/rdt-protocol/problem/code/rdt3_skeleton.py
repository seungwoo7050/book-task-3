"""
RDT 3.0 (Stop-and-Wait) — Skeleton Code

Implements reliable data transfer using alternating-bit sequence numbers,
checksums, and a retransmission timer over an unreliable channel.

Usage:
    python3 rdt3_skeleton.py [--loss RATE] [--corrupt RATE]
"""

import argparse
import time

from channel import UnreliableChannel
from packet import make_packet, parse_packet, is_corrupt, make_ack, is_ack


TIMEOUT = 0.5  # Retransmission timeout in seconds


def rdt_send(channel_to_receiver: UnreliableChannel,
             channel_to_sender: UnreliableChannel,
             data_list: list[str]) -> None:
    """RDT 3.0 Sender.

    Args:
        channel_to_receiver: Channel for sending data packets.
        channel_to_sender: Channel for receiving ACKs.
        data_list: List of messages to send.
    """
    seq_num = 0

    for data in data_list:
        payload = data.encode()
        pkt = make_packet(seq_num, payload)

        # TODO: Implement the rdt 3.0 sender FSM:
        #   1. Send the packet
        #   2. Start a timer
        #   3. Wait for ACK:
        #      - If correct ACK received → move to next packet
        #      - If timeout → retransmit
        #      - If corrupt/wrong ACK → keep waiting
        #   4. Toggle seq_num (0 ↔ 1)

        pass  # Replace


def rdt_receive(channel_to_receiver: UnreliableChannel,
                channel_to_sender: UnreliableChannel,
                expected_count: int) -> list[str]:
    """RDT 3.0 Receiver.

    Args:
        channel_to_receiver: Channel for receiving data packets.
        channel_to_sender: Channel for sending ACKs.
        expected_count: Number of messages expected.

    Returns:
        List of received messages in order.
    """
    received: list[str] = []
    expected_seq = 0

    # TODO: Implement the rdt 3.0 receiver FSM:
    #   1. Wait for a packet
    #   2. If packet is valid and has expected seq:
    #      - Extract payload, add to received list
    #      - Send ACK with this seq number
    #      - Toggle expected_seq
    #   3. If corrupt or wrong seq:
    #      - Send ACK for the previous seq number

    return received


def main():
    parser = argparse.ArgumentParser(description="RDT 3.0 Demo")
    parser.add_argument("--loss", type=float, default=0.2, help="Loss rate")
    parser.add_argument("--corrupt", type=float, default=0.1, help="Corruption rate")
    args = parser.parse_args()

    # Read test data
    try:
        with open("data/test_messages.txt") as f:
            messages = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        messages = ["Hello", "World", "RDT", "Protocol", "Test"]

    print(f"=== RDT 3.0 (Stop-and-Wait) ===")
    print(f"Messages to send: {len(messages)}")
    print(f"Loss rate: {args.loss}, Corruption rate: {args.corrupt}\n")

    ch_data = UnreliableChannel(args.loss, args.corrupt)
    ch_ack = UnreliableChannel(args.loss, args.corrupt)

    # In a real implementation, sender and receiver run concurrently.
    # For this skeleton, implement the logic in the functions above.
    print("[TODO] Implement rdt_send() and rdt_receive()")


if __name__ == "__main__":
    main()
