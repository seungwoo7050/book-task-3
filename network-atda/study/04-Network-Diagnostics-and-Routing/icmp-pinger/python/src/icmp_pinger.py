"""
ICMP Pinger 정답 구현.

raw ICMP socket을 이용해 ping utility를 구현한다.

Usage:
    sudo python3 icmp_pinger.py <host> [-c count]

root/administrator privilege가 필요하다.
"""

import os
import select
import socket
import struct
import sys
import time

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_HEADER_FORMAT = "!BBHHH"
ICMP_HEADER_SIZE = struct.calcsize(ICMP_HEADER_FORMAT)


def internet_checksum(data: bytes) -> int:
    """Internet checksum(RFC 1071)을 계산한다.

    Args:
        data: checksum을 계산할 bytes.

    Returns:
        16-bit checksum 값.
    """
    if len(data) % 2 != 0:
        data += b"\x00"

    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        total += word

    # 상위 carry를 16-bit 아래로 접어 넣는다.
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)

    return ~total & 0xFFFF


def build_echo_request(identifier: int, sequence: int) -> bytes:
    """ICMP Echo Request packet을 만든다.

    Args:
        identifier: ICMP identifier field 값.
        sequence: ICMP sequence number 값.

    Returns:
        완성된 ICMP packet bytes.
    """
    # checksum을 0으로 둔 임시 header를 먼저 만든다.
    header = struct.pack(
        ICMP_HEADER_FORMAT,
        ICMP_ECHO_REQUEST,  # Type
        0,                   # Code
        0,                   # Checksum (placeholder)
        identifier,          # Identifier
        sequence,            # Sequence
    )

    # payload에는 현재 timestamp를 double 8 bytes로 담는다.
    payload = struct.pack("!d", time.time())

    # header + payload 기준으로 checksum을 계산한다.
    checksum = internet_checksum(header + payload)

    # 올바른 checksum으로 header를 다시 만든다.
    header = struct.pack(
        ICMP_HEADER_FORMAT,
        ICMP_ECHO_REQUEST,
        0,
        checksum,
        identifier,
        sequence,
    )

    return header + payload


def parse_echo_reply(
    data: bytes, identifier: int
) -> tuple[int, float] | None:
    """수신한 data에서 ICMP Echo Reply를 해석한다.

    Args:
        data: IP header를 포함한 raw bytes.
        identifier: 일치해야 하는 ICMP identifier.

    Returns:
        유효하면 `(sequence_number, send_timestamp)`, 아니면 `None`.
    """
    # 앞부분 IPv4 header 길이를 계산한다.
    ip_header_len = (data[0] & 0x0F) * 4

    # IP header 뒤의 ICMP header를 분리한다.
    icmp_data = data[ip_header_len:]
    if len(icmp_data) < ICMP_HEADER_SIZE:
        return None

    icmp_type, code, checksum, pkt_id, sequence = struct.unpack(
        ICMP_HEADER_FORMAT, icmp_data[:ICMP_HEADER_SIZE]
    )

    # 우리가 보낸 Echo Reply인지 확인한다.
    if icmp_type != ICMP_ECHO_REPLY or pkt_id != identifier:
        return None

    # payload에서 timestamp를 복원한다.
    payload = icmp_data[ICMP_HEADER_SIZE:]
    if len(payload) < 8:
        return None

    send_time = struct.unpack("!d", payload[:8])[0]
    return sequence, send_time


def ping(host: str, count: int = 4, timeout: float = 1.0) -> None:
    """ICMP Echo Request를 보내고 결과를 출력한다.

    Args:
        host: 대상 hostname 또는 IP address.
        count: 보낼 ping 횟수.
        timeout: 각 ping의 timeout 초.
    """
    # hostname을 IP로 해석한다.
    try:
        dest_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"ping: cannot resolve {host}: Unknown host")
        sys.exit(1)

    identifier = os.getpid() & 0xFFFF

    print(f"PING {host} ({dest_ip}): {ICMP_HEADER_SIZE + 8} bytes of data\n")

    # raw ICMP socket을 만든다.
    try:
        raw_socket = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP
        )
    except PermissionError:
        print("Error: Raw socket requires root privileges.")
        print("Run with: sudo python3 icmp_pinger.py <host>")
        sys.exit(1)

    rtt_list: list[float] = []

    for seq in range(1, count + 1):
        # Echo Request를 만들어 전송한다.
        packet = build_echo_request(identifier, seq)
        send_time = time.time()
        raw_socket.sendto(packet, (dest_ip, 0))

        # reply를 기다린다.
        ready, _, _ = select.select([raw_socket], [], [], timeout)

        if ready:
            recv_time = time.time()
            data, addr = raw_socket.recvfrom(1024)

            result = parse_echo_reply(data, identifier)
            if result:
                reply_seq, embedded_time = result
                rtt_ms = (recv_time - embedded_time) * 1000
                rtt_list.append(rtt_ms)
                packet_size = len(data) - ((data[0] & 0x0F) * 4)
                print(
                    f"{packet_size} bytes from {addr[0]}: "
                    f"icmp_seq={reply_seq}  RTT={rtt_ms:.3f} ms"
                )
            else:
                print(f"Ping {seq}: Unexpected reply")
        else:
            print(f"Ping {seq}: Request timed out")

        # 마지막 ping이 아니면 1초 간격을 유지한다.
        if seq < count:
            time.sleep(max(0, 1.0 - (time.time() - send_time)))

    raw_socket.close()

    # 최종 통계를 출력한다.
    sent = count
    received = len(rtt_list)
    lost = sent - received
    loss_pct = (lost / sent) * 100

    print(f"\n--- {host} ping statistics ---")
    print(f"{sent} packets sent, {received} received, {loss_pct:.1f}% loss")

    if rtt_list:
        min_rtt = min(rtt_list)
        max_rtt = max(rtt_list)
        avg_rtt = sum(rtt_list) / len(rtt_list)
        print(f"RTT min/avg/max = {min_rtt:.3f}/{avg_rtt:.3f}/{max_rtt:.3f} ms")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 icmp_pinger.py <host> [-c count]")
        sys.exit(1)

    target_host = sys.argv[1]
    ping_count = 4

    if "-c" in sys.argv:
        idx = sys.argv.index("-c")
        ping_count = int(sys.argv[idx + 1])

    ping(target_host, ping_count)
