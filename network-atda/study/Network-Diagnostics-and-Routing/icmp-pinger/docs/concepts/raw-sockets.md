# Raw Sockets in Python

## Overview

A **raw socket** allows a program to send and receive packets at the IP layer (Layer 3), bypassing the transport layer (TCP/UDP). This is necessary for ICMP because ICMP is not a transport-layer protocol — it operates directly on top of IP.

## Creating a Raw ICMP Socket

```python
import socket

raw_socket = socket.socket(
    socket.AF_INET,      # IPv4
    socket.SOCK_RAW,     # Raw socket
    socket.IPPROTO_ICMP  # ICMP protocol
)
```

- `SOCK_RAW`: Raw socket — gives direct access to the IP layer
- `IPPROTO_ICMP`: Protocol number 1 (ICMP)

## Privilege Requirement

Raw sockets require **elevated privileges**:
- **Linux**: Run as root (`sudo python3 script.py`) or set `CAP_NET_RAW` capability
- **macOS**: Run as root (`sudo python3 script.py`)
- **Windows**: Run as Administrator

```bash
# Linux
sudo python3 icmp_pinger.py google.com

# Alternative: set capability (persistent)
sudo setcap cap_net_raw=ep $(which python3)
```

## Sending ICMP Packets

```python
# Build the ICMP packet (header + payload)
packet = build_echo_request(identifier=os.getpid() & 0xFFFF, sequence=1)

# Send to the target
target_addr = socket.gethostbyname("google.com")
raw_socket.sendto(packet, (target_addr, 0))
# Note: port is 0 for raw sockets (ICMP doesn't use ports)
```

## Receiving ICMP Replies

```python
# Set a timeout
raw_socket.settimeout(1.0)

try:
    data, addr = raw_socket.recvfrom(1024)
    # data includes the IP header (20 bytes) + ICMP message
except socket.timeout:
    print("Request timed out")
```

### Using `select` for Timeout (Alternative)

The `select` module provides a more precise timeout mechanism:

```python
import select

# Wait up to 1 second for data to be available
ready, _, _ = select.select([raw_socket], [], [], 1.0)

if ready:
    data, addr = raw_socket.recvfrom(1024)
else:
    print("Request timed out")
```

`select` is preferred because it separates the timeout logic from the socket configuration.

## Received Data Format

When `recvfrom()` returns data from a raw ICMP socket, the data layout is:

```
[IP Header (20+ bytes)][ICMP Header (8 bytes)][ICMP Payload (variable)]
```

You must skip the IP header to get to the ICMP portion:

```python
# Determine IP header length from the first byte
ip_header_len = (data[0] & 0x0F) * 4

# ICMP data starts after the IP header
icmp_data = data[ip_header_len:]
```

## Common Issues

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| `PermissionError: [Errno 1]` | Not running as root | Use `sudo` |
| Receiving others' ICMP replies | Raw socket sees all ICMP traffic | Filter by identifier field |
| `OSError: [Errno 22]` | Invalid packet data | Check packet construction |
| Infinite wait | No timeout set | Use `select()` or `settimeout()` |

## Filtering Replies

A raw ICMP socket receives **all** ICMP traffic on the host, not just replies to your pings. Always verify:

1. ICMP Type == 0 (Echo Reply)
2. Identifier matches your process ID
3. Sequence number matches the expected value

```python
icmp_type, _, _, pkt_id, seq = struct.unpack("!BBHHH", icmp_data[:8])
if icmp_type == 0 and pkt_id == my_id:
    # This is our reply
    ...
```
