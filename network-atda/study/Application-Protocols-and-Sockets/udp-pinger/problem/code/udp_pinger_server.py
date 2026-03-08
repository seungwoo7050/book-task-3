"""
UDP Pinger Server (Provided — Do NOT Modify)

This server listens for UDP ping messages and echoes them back.
It simulates packet loss by randomly dropping ~30% of incoming packets.

Usage:
    python3 udp_pinger_server.py [port]
"""

import random
import socket
import sys


def main(port: int = 12000) -> None:
    """Run the UDP ping server.

    Args:
        port: UDP port number to listen on.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("", port))

    print(f"[INFO] UDP Pinger Server started on port {port}")
    print("[INFO] Press Ctrl+C to stop\n")

    try:
        while True:
            # Receive a ping message
            message, address = server_socket.recvfrom(1024)

            # Simulate 30% packet loss
            if random.randint(1, 10) <= 3:
                print(f"[DROP] Packet from {address} — simulating loss")
                continue

            # Echo the message back (capitalize to distinguish reply)
            reply = message.decode().upper()
            server_socket.sendto(reply.encode(), address)
            print(f"[ECHO] Replied to {address}: {reply.strip()}")
    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 12000
    main(port)
