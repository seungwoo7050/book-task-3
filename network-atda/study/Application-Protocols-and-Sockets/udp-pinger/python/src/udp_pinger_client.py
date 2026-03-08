"""
UDP Pinger Client — Complete Solution

Sends 10 ping messages to the UDP pinger server, measures RTT for each
reply, handles timeouts for lost packets, and prints summary statistics.

Usage:
    python3 udp_pinger_client.py [host] [port]
"""

import socket
import sys
import time

PING_COUNT = 10
TIMEOUT = 1  # seconds


def main(host: str = "127.0.0.1", port: int = 12000) -> None:
    """Send ping messages and collect RTT statistics.

    Args:
        host: The server hostname or IP address.
        port: The server UDP port number.
    """
    # Create a UDP socket with a 1-second timeout
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    rtt_list: list[float] = []
    server_address = (host, port)

    print(f"Pinging {host}:{port} with {PING_COUNT} packets ...\n")

    for seq in range(1, PING_COUNT + 1):
        # Build the ping message with sequence number and timestamp
        send_time = time.time()
        message = f"Ping {seq} {send_time}"

        try:
            # Send the ping datagram
            client_socket.sendto(message.encode(), server_address)

            # Wait for the reply
            data, addr = client_socket.recvfrom(1024)
            recv_time = time.time()

            # Calculate RTT in milliseconds
            rtt_ms = (recv_time - send_time) * 1000
            rtt_list.append(rtt_ms)

            print(f"Ping {seq:2d}: Reply from {addr[0]}  RTT = {rtt_ms:.3f} ms")

        except socket.timeout:
            print(f"Ping {seq:2d}: Request timed out")

    # Print summary statistics
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
