"""
RDT 3.0 (Stop-and-Wait) 정답 구현.

alternating-bit sequence number, checksum, retransmission timer로
reliable data transfer를 시뮬레이션한다.

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

TIMEOUT = 0.5  # 초


def rdt_send_receive(
    channel_data: UnreliableChannel,
    channel_ack: UnreliableChannel,
    data_list: list[str],
) -> list[str]:
    """RDT 3.0 protocol로 모든 메시지를 전송한다.

    Args:
        channel_data: data packet용 channel (`sender -> receiver`).
        channel_ack: ACK packet용 channel (`receiver -> sender`).
        data_list: 전송할 문자열 메시지 목록.

    Returns:
        receiver가 순서대로 받은 메시지 목록.
    """
    total = len(data_list)
    received: list[str] = []

    # sender 상태
    send_seq = 0
    send_idx = 0
    current_pkt = make_packet(send_seq, data_list[send_idx].encode())
    timer_start = time.time()
    awaiting_ack = False

    # receiver 상태
    expected_seq = 0

    # 첫 패킷을 보낸다.
    channel_data.send(current_pkt)
    timer_start = time.time()
    awaiting_ack = True
    print(f"[SENDER]   Sent packet seq={send_seq}: \"{data_list[send_idx]}\"")

    while len(received) < total:
        # --- receiver 측: data packet 도착 여부 확인 ---
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
                    # duplicate이면 직전 ACK를 다시 보낸다.
                    prev = 1 - expected_seq
                    print(f"[RECEIVER] Duplicate seq={seq}, re-sending ACK {prev}")
                    channel_ack.send(make_ack(prev))
            elif pkt:
                # 손상 packet이면 직전 ACK를 다시 보낸다.
                prev = 1 - expected_seq
                print(f"[RECEIVER] Corrupt packet, re-sending ACK {prev}")
                channel_ack.send(make_ack(prev))

        # --- sender 측: ACK 도착 여부 확인 ---
        if awaiting_ack and channel_ack.has_packet():
            ack_pkt = channel_ack.receive()
            if ack_pkt and is_ack(ack_pkt, send_seq):
                print(f"[SENDER]   ACK {send_seq} received")
                send_seq = 1 - send_seq
                send_idx += 1
                awaiting_ack = False

                # 아직 보낼 메시지가 남아 있으면 다음 packet을 보낸다.
                if send_idx < total:
                    current_pkt = make_packet(send_seq, data_list[send_idx].encode())
                    channel_data.send(current_pkt)
                    timer_start = time.time()
                    awaiting_ack = True
                    print(f"[SENDER]   Sent packet seq={send_seq}: \"{data_list[send_idx]}\"")

        # --- sender 측: timeout 여부 확인 ---
        if awaiting_ack and (time.time() - timer_start > TIMEOUT):
            print(f"[SENDER]   Timeout! Retransmitting seq={send_seq}")
            channel_data.send(current_pkt)
            timer_start = time.time()

        time.sleep(0.01)  # busy-wait를 피하기 위해 잠시 쉰다.

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

    # 최종 수신 결과가 기대한 메시지와 같은지 확인한다.
    if received == messages:
        print("Status:   SUCCESS — All messages delivered correctly!")
    else:
        print("Status:   FAILURE — Messages do not match!")
        for i, (s, r) in enumerate(zip(messages, received)):
            if s != r:
                print(f"  Mismatch at index {i}: sent={s!r}, received={r!r}")


if __name__ == "__main__":
    main()
