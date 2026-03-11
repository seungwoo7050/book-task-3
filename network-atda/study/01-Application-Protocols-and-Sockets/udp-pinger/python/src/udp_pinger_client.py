"""
UDP Pinger Client 정답 구현.

UDP pinger server로 10개의 ping을 보내고, 각 응답의 RTT를 측정하며,
loss timeout을 처리하고, 마지막에 요약 통계를 출력한다.

Usage:
    python3 udp_pinger_client.py [host] [port]
"""

import socket
import sys
import time

PING_COUNT = 10
TIMEOUT = 1  # 초


def main(host: str = "127.0.0.1", port: int = 12000) -> None:
    """ping을 보내고 RTT 통계를 수집한다.

    Args:
        host: server hostname 또는 IP address.
        port: server UDP port 번호.
    """
    # 1초 timeout을 갖는 UDP socket을 만든다.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    rtt_list: list[float] = []
    server_address = (host, port)

    print(f"Pinging {host}:{port} with {PING_COUNT} packets ...\n")

    for seq in range(1, PING_COUNT + 1):
        # sequence 번호와 timestamp를 포함한 ping 메시지를 만든다.
        send_time = time.time()
        message = f"Ping {seq} {send_time}"

        try:
            # ping datagram을 전송한다.
            client_socket.sendto(message.encode(), server_address)

            # 응답을 기다린다.
            data, addr = client_socket.recvfrom(1024)
            recv_time = time.time()

            # RTT를 millisecond 단위로 계산한다.
            rtt_ms = (recv_time - send_time) * 1000
            rtt_list.append(rtt_ms)

            print(f"Ping {seq:2d}: Reply from {addr[0]}  RTT = {rtt_ms:.3f} ms")

        except socket.timeout:
            print(f"Ping {seq:2d}: Request timed out")

    # 요약 통계를 출력한다.
    sent = PING_COUNT
    received = len(rtt_list)
    lost = sent - received
    loss_pct = (lost / sent) * 100

    print(f"\n--- Ping Statistics ---")
    print(f"{sent} packets sent, {received} received, {loss_pct:.1f}% loss")

    if rtt_list:
        min_rtt = min(rtt_list)
        max_rtt = max(rtt_list)
        avg_rtt = sum(rtt_list) / len(rtt_list)
        print(f"RTT min/avg/max = {min_rtt:.3f}/{avg_rtt:.3f}/{max_rtt:.3f} ms")
    else:
        print("No replies received — 100% packet loss")

    client_socket.close()


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 12000
    main(host, port)
