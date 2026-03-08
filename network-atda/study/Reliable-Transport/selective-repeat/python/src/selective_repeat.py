"""
Selective Repeat — Complete Solution

Reliable data transfer using individual ACK tracking and per-packet timers.

Usage:
    python3 selective_repeat.py [--loss RATE] [--corrupt RATE] [--window N]
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROBLEM_CODE = PROJECT_ROOT / "problem" / "code"
PROBLEM_DATA = PROJECT_ROOT / "problem" / "data"

sys.path.insert(0, str(PROBLEM_CODE))

from channel import UnreliableChannel
from packet import make_ack, make_packet, parse_packet, is_corrupt

TIMEOUT = 0.5


def selective_repeat_send_receive(
    channel_data: UnreliableChannel,
    channel_ack: UnreliableChannel,
    data_list: list[str],
    window_size: int = 4,
) -> list[str]:
    """Transfer messages using Selective Repeat in a single event loop."""
    total = len(data_list)
    packets = [make_packet(i, item.encode()) for i, item in enumerate(data_list)]
    delivered: list[str] = []

    # Sender state
    send_base = 0
    next_seq = 0
    acked: set[int] = set()
    timers: dict[int, float] = {}

    # Receiver state
    recv_base = 0
    recv_buffer: dict[int, str] = {}

    while len(delivered) < total:
        while next_seq < min(send_base + window_size, total):
            print(f"[SENDER]   Sent packet seq={next_seq}: \"{data_list[next_seq]}\"")
            channel_data.send(packets[next_seq])
            timers[next_seq] = time.time()
            next_seq += 1

        if channel_data.has_packet():
            pkt = channel_data.receive()
            if pkt and not is_corrupt(pkt):
                _, seq, payload = parse_packet(pkt)
                if recv_base <= seq < recv_base + window_size:
                    if seq not in recv_buffer:
                        recv_buffer[seq] = payload.decode()
                        print(f"[RECEIVER] Buffered seq={seq} → ACK {seq}")
                    else:
                        print(f"[RECEIVER] Duplicate seq={seq} in window → ACK {seq}")
                    channel_ack.send(make_ack(seq))

                    while recv_base in recv_buffer:
                        message = recv_buffer.pop(recv_base)
                        delivered.append(message)
                        print(f"[RECEIVER] Delivered seq={recv_base}: \"{message}\"")
                        recv_base += 1
                elif seq < recv_base:
                    print(f"[RECEIVER] Duplicate old seq={seq} → re-ACK {seq}")
                    channel_ack.send(make_ack(seq))
                else:
                    print(f"[RECEIVER] Ignored seq={seq} outside window")
            elif pkt:
                print("[RECEIVER] Corrupt packet dropped")

        if channel_ack.has_packet():
            ack_pkt = channel_ack.receive()
            if ack_pkt and not is_corrupt(ack_pkt):
                _, ack_seq, payload = parse_packet(ack_pkt)
                if payload == b"ACK" and send_base <= ack_seq < next_seq:
                    print(f"[SENDER]   ACK {ack_seq} received")
                    acked.add(ack_seq)
                    timers.pop(ack_seq, None)
                    while send_base in acked:
                        acked.remove(send_base)
                        send_base += 1

        now = time.time()
        for seq in range(send_base, next_seq):
            if seq in acked:
                continue
            started = timers.get(seq)
            if started is not None and now - started > TIMEOUT:
                print(f"[SENDER]   Timeout! Retransmitting seq={seq}")
                channel_data.send(packets[seq])
                timers[seq] = time.time()

        time.sleep(0.01)

    return delivered


def load_messages() -> list[str]:
    """Load the demo payloads used by the test harness."""
    with open(PROBLEM_DATA / "test_messages.txt") as handle:
        return [line.strip() for line in handle if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Selective Repeat")
    parser.add_argument("--loss", type=float, default=0.2, help="Loss rate")
    parser.add_argument("--corrupt", type=float, default=0.1, help="Corruption rate")
    parser.add_argument("--window", type=int, default=4, help="Window size")
    args = parser.parse_args()

    messages = load_messages()

    print(f"=== Selective Repeat (Window Size = {args.window}) ===")
    print(f"Messages to send: {len(messages)}")
    print(f"Loss rate: {args.loss}, Corruption rate: {args.corrupt}\n")

    ch_data = UnreliableChannel(args.loss, args.corrupt)
    ch_ack = UnreliableChannel(args.loss, args.corrupt)

    start = time.time()
    delivered = selective_repeat_send_receive(ch_data, ch_ack, messages, args.window)
    elapsed = time.time() - start

    print("\n=== Transfer Complete ===")
    print(f"Sent:     {len(messages)} messages")
    print(f"Received: {len(delivered)} messages")
    print(f"Time:     {elapsed:.2f} seconds")

    if delivered == messages:
        print("Status:   SUCCESS — All messages delivered correctly!")
    else:
        print("Status:   FAILURE — Messages do not match!")
        sys.exit(1)


if __name__ == "__main__":
    main()
