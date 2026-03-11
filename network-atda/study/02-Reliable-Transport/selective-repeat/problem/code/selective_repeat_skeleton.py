"""
Selective Repeat — Skeleton Code

Implements reliable data transfer using a sender window, receiver buffer,
per-packet timers, and selective retransmission.

Usage:
    python3 selective_repeat_skeleton.py [--loss RATE] [--corrupt RATE] [--window N]
"""

import argparse

from channel import UnreliableChannel
from packet import make_packet, parse_packet, is_corrupt, make_ack


def selective_repeat_send(channel_data: UnreliableChannel,
                          channel_ack: UnreliableChannel,
                          data_list: list[str],
                          window_size: int = 4) -> None:
    """Selective Repeat sender.

    TODO:
      1. Keep a per-packet timer for all outstanding packets
      2. Retransmit only packets whose timers expire
      3. Slide the sender base only after the lowest outstanding seq is ACKed
    """
    raise NotImplementedError


def selective_repeat_receive(channel_data: UnreliableChannel,
                             channel_ack: UnreliableChannel,
                             expected_count: int,
                             window_size: int = 4) -> list[str]:
    """Selective Repeat receiver.

    TODO:
      1. Accept valid packets within the receive window
      2. Buffer out-of-order packets
      3. ACK each accepted packet individually
      4. Deliver buffered packets in order once the gap is filled
    """
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="Selective Repeat Demo")
    parser.add_argument("--loss", type=float, default=0.2, help="Loss rate")
    parser.add_argument("--corrupt", type=float, default=0.1, help="Corruption rate")
    parser.add_argument("--window", type=int, default=4, help="Window size")
    args = parser.parse_args()

    print("Implement selective_repeat_send() and selective_repeat_receive().")
    print(f"Requested loss={args.loss}, corrupt={args.corrupt}, window={args.window}")


if __name__ == "__main__":
    main()
