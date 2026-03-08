"""
RDT 3.0 (Stop-and-Wait) — Complete Solution

Reliable data transfer using alternating-bit sequence numbers,
checksums, and retransmission timers.

Usage:
    python3 rdt3.py [--loss RATE] [--corrupt RATE]
"""

import argparse
from pathlib import Path
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROBLEM_CODE = PROJECT_ROOT / "problem" / "code"
PROBLEM_DATA = PROJECT_ROOT / "problem" / "data"

sys.path.insert(0, str(PROBLEM_CODE))

from channel import UnreliableChannel
from packet import make_packet, parse_packet, is_corrupt, make_ack, is_ack

TIMEOUT = 0.5  # seconds


def rdt_send_receive(
    channel_data: UnreliableChannel,
    channel_ack: UnreliableChannel,
    data_list: list[str],
) -> list[str]:
    """Run the RDT 3.0 protocol to transfer all messages.

    This implementation simulates both sender and receiver in a single
    thread using an interleaved event loop.

    Args:
        channel_data: Channel for data packets (sender → receiver).
        channel_ack: Channel for ACK packets (receiver → sender).
        data_list: List of string messages to transfer.

    Returns:
        List of messages received in order by the receiver.
    """
    total = len(data_list)
    received: list[str] = []

    # Sender state
    send_seq = 0
    send_idx = 0
    current_pkt = make_packet(send_seq, data_list[send_idx].encode())
    timer_start = time.time()
    awaiting_ack = False

    # Receiver state
    expected_seq = 0

    # Initial send
    channel_data.send(current_pkt)
    timer_start = time.time()
    awaiting_ack = True
    print(f"[SENDER]   Sent packet seq={send_seq}: \"{data_list[send_idx]}\"")

    while len(received) < total:
        # --- Receiver side: check for data packets ---
        if channel_data.has_packet():
            pkt = channel_data.receive()
            if pkt and not is_corrupt(pkt):
                _, seq, payload = parse_packet(pkt)
                if seq == expected_seq:
                    msg = payload.decode()
                    received.append(msg)
                    print(f"[RECEIVER] Received seq={seq}: \"{msg}\" → ACK {seq}")
                    ack = make_ack(expected_seq)
                    channel_ack.send(ack)
                    expected_seq = 1 - expected_seq
                else:
                    # Duplicate — re-ACK previous
                    prev = 1 - expected_seq
                    print(f"[RECEIVER] Duplicate seq={seq}, re-sending ACK {prev}")
                    channel_ack.send(make_ack(prev))
            elif pkt:
                # Corrupt — re-ACK previous
                prev = 1 - expected_seq
                print(f"[RECEIVER] Corrupt packet, re-sending ACK {prev}")
                channel_ack.send(make_ack(prev))

        # --- Sender side: check for ACKs ---
        if awaiting_ack and channel_ack.has_packet():
            ack_pkt = channel_ack.receive()
            if ack_pkt and is_ack(ack_pkt, send_seq):
                print(f"[SENDER]   ACK {send_seq} received")
                send_seq = 1 - send_seq
                send_idx += 1
                awaiting_ack = False

                # Send next packet if available
                if send_idx < total:
                    current_pkt = make_packet(send_seq, data_list[send_idx].encode())
                    channel_data.send(current_pkt)
                    timer_start = time.time()
                    awaiting_ack = True
                    print(f"[SENDER]   Sent packet seq={send_seq}: \"{data_list[send_idx]}\"")

        # --- Sender side: check for timeout ---
        if awaiting_ack and (time.time() - timer_start > TIMEOUT):
            print(f"[SENDER]   Timeout! Retransmitting seq={send_seq}")
            channel_data.send(current_pkt)
            timer_start = time.time()

        time.sleep(0.01)  # Small delay to prevent busy-waiting

    return received


def main():
    parser = argparse.ArgumentParser(description="RDT 3.0 (Stop-and-Wait)")
    parser.add_argument("--loss", type=float, default=0.2, help="Loss rate")
    parser.add_argument("--corrupt", type=float, default=0.1, help="Corruption rate")
    args = parser.parse_args()

    try:
        with open(PROBLEM_DATA / "test_messages.txt") as f:
            messages = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        messages = ["Hello", "World", "RDT", "Protocol", "Test"]

    print(f"=== RDT 3.0 (Stop-and-Wait) ===")
    print(f"Messages to send: {len(messages)}")
    print(f"Loss rate: {args.loss}, Corruption rate: {args.corrupt}\n")

    ch_data = UnreliableChannel(args.loss, args.corrupt)
    ch_ack = UnreliableChannel(args.loss, args.corrupt)

    start = time.time()
    received = rdt_send_receive(ch_data, ch_ack, messages)
    elapsed = time.time() - start

    print(f"\n=== Transfer Complete ===")
    print(f"Sent:     {len(messages)} messages")
    print(f"Received: {len(received)} messages")
    print(f"Time:     {elapsed:.2f} seconds")

    # Verify correctness
    if received == messages:
        print("Status:   SUCCESS — All messages delivered correctly!")
    else:
        print("Status:   FAILURE — Messages do not match!")
        for i, (s, r) in enumerate(zip(messages, received)):
            if s != r:
                print(f"  Mismatch at index {i}: sent={s!r}, received={r!r}")


if __name__ == "__main__":
    main()
