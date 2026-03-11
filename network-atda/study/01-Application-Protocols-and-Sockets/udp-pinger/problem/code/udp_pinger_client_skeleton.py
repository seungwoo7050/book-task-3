"""
UDP Pinger Client — Skeleton Code

Sends 10 ping messages to the UDP pinger server and measures RTT.

Usage:
    python3 udp_pinger_client_skeleton.py [host] [port]
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
    # --- Create a UDP socket ---
    # TODO: Create a socket using AF_INET and SOCK_DGRAM.
    #       Set the socket timeout to TIMEOUT seconds.

    client_socket = None  # Replace with your socket

    rtt_list: list[float] = []

    for seq in range(1, PING_COUNT + 1):
        # --- Build the ping message ---
        # TODO: Create a message string with the sequence number and current
        #       timestamp.  Format: "Ping <seq> <timestamp>"

        send_time = time.time()
        message = ""  # Fill in

        try:
            # --- Send the ping ---
            # TODO: Send the message to (host, port) using sendto().

            pass  # Replace

            # --- Receive the reply ---
            # TODO: Receive the reply using recvfrom().
            #       Calculate RTT and store it.
            #       Print the result.

            pass  # Replace

        except socket.timeout:
            # --- Handle timeout ---
            # TODO: Print a timeout message for this sequence number.

            pass  # Replace

    # --- Print summary statistics ---
    # TODO: Print packets sent/received, loss %, and min/avg/max RTT.

    if client_socket:
        client_socket.close()


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 12000
    main(host, port)
