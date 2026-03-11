"""
Go-Back-N (GBN) 정답 구현.

cumulative ACK와 sliding window를 이용해 reliable data transfer를 시뮬레이션한다.

Usage:
    python3 gbn.py [--loss RATE] [--corrupt RATE] [--window N]
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
from packet import make_packet, parse_packet, is_corrupt, make_ack

TIMEOUT = 0.5  # 초


def gbn_send_receive(
    channel_data: UnreliableChannel,
    channel_ack: UnreliableChannel,
    data_list: list[str],
    window_size: int = 4,
) -> list[str]:
    """GBN protocol로 모든 메시지를 전송한다.

    Args:
        channel_data: data packet용 channel.
        channel_ack: ACK packet용 channel.
        data_list: 전송할 문자열 메시지 목록.
        window_size: ACK 없이 outstanding 상태로 둘 최대 packet 수 `N`.

    Returns:
        receiver가 순서대로 받은 메시지 목록.
    """
    total = len(data_list)
    received: list[str] = []

    # 모든 data packet을 미리 만들어 둔다.
    packets = [make_packet(i, data_list[i].encode()) for i in range(total)]

    # sender 상태
    base = 0
    next_seq = 0
    timer_start: float | None = None

    # receiver 상태
    expected_seq = 0

    while len(received) < total:
        # --- sender 측: window 안에서 보낼 수 있는 packet을 전송 ---
        while next_seq < min(base + window_size, total):
            print(f"[SENDER]   Sent packet seq={next_seq}: \"{data_list[next_seq]}\"")
            channel_data.send(packets[next_seq])
            if base == next_seq:
                timer_start = time.time()
            next_seq += 1

        # --- receiver 측: data packet 도착 여부 확인 ---
        if channel_data.has_packet():
            pkt = channel_data.receive()
            if pkt and not is_corrupt(pkt):
                _, seq, payload = parse_packet(pkt)
                if seq == expected_seq:
                    msg = payload.decode()
                    received.append(msg)
                    print(f"[RECEIVER] Received seq={seq}: \"{msg}\" → ACK {seq}")
                    channel_ack.send(make_ack(expected_seq))
                    expected_seq += 1
                else:
                    # 순서가 어긋난 packet이면 마지막 정상 packet의 ACK를 다시 보낸다.
                    last_ack = expected_seq - 1
                    if last_ack >= 0:
                        print(f"[RECEIVER] Out-of-order seq={seq}, re-sending ACK {last_ack}")
                        channel_ack.send(make_ack(last_ack))
                    else:
                        print(f"[RECEIVER] Out-of-order seq={seq}, no ACK to send")
            elif pkt:
                last_ack = expected_seq - 1
                if last_ack >= 0:
                    print(f"[RECEIVER] Corrupt packet, re-sending ACK {last_ack}")
                    channel_ack.send(make_ack(last_ack))

        # --- sender 측: ACK 도착 여부 확인 ---
        if channel_ack.has_packet():
            ack_pkt = channel_ack.receive()
            if ack_pkt and not is_corrupt(ack_pkt):
                _, ack_seq, payload = parse_packet(ack_pkt)
                if payload == b"ACK" and ack_seq >= base:
                    print(f"[SENDER]   ACK {ack_seq} received (cumulative)")
                    base = ack_seq + 1
                    if base == next_seq:
                        timer_start = None  # outstanding packet이 더 이상 없다.
                    else:
                        timer_start = time.time()  # 남은 outstanding packet 기준으로 timer를 재시작한다.

        # --- sender 측: timeout 처리 ---
        if timer_start and (time.time() - timer_start > TIMEOUT):
            print(f"[SENDER]   Timeout! Retransmitting packets {base} to {next_seq - 1}")
            for i in range(base, next_seq):
                channel_data.send(packets[i])
            timer_start = time.time()

        time.sleep(0.01)

    return received


def main():
    parser = argparse.ArgumentParser(description="Go-Back-N")
    parser.add_argument("--loss", type=float, default=0.2, help="Loss rate")
    parser.add_argument("--corrupt", type=float, default=0.1, help="Corruption rate")
    parser.add_argument("--window", type=int, default=4, help="Window size N")
    args = parser.parse_args()

    try:
        with open(PROBLEM_DATA / "test_messages.txt") as f:
            messages = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        messages = ["Hello", "World", "RDT", "Protocol", "Test"]

    print(f"=== Go-Back-N (Window Size = {args.window}) ===")
    print(f"Messages to send: {len(messages)}")
    print(f"Loss rate: {args.loss}, Corruption rate: {args.corrupt}\n")

    ch_data = UnreliableChannel(args.loss, args.corrupt)
    ch_ack = UnreliableChannel(args.loss, args.corrupt)

    start = time.time()
    received = gbn_send_receive(ch_data, ch_ack, messages, args.window)
    elapsed = time.time() - start

    print(f"\n=== Transfer Complete ===")
    print(f"Sent:     {len(messages)} messages")
    print(f"Received: {len(received)} messages")
    print(f"Time:     {elapsed:.2f} seconds")

    if received == messages:
        print("Status:   SUCCESS — All messages delivered correctly!")
    else:
        print("Status:   FAILURE — Messages do not match!")
        for i, (s, r) in enumerate(zip(messages, received)):
            if s != r:
                print(f"  Mismatch at index {i}: sent={s!r}, received={r!r}")


if __name__ == "__main__":
    main()
