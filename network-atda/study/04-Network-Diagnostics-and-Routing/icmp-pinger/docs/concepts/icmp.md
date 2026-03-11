# ICMP Protocol Reference

## Overview

**ICMP** (Internet Control Message Protocol) is a network-layer protocol used for diagnostics and error reporting. It is defined in **RFC 792** and rides directly on top of IP (protocol number 1).

ICMP is the protocol behind:
- `ping` — tests reachability using Echo Request/Reply
- `traceroute` — discovers network path using TTL-exceeded messages

## ICMP Message Types

| Type | Code | Description |
| :--- | :--- | :--- |
| `0` | `0` | **Echo Reply** (ping response) |
| `3` | `0–15` | Destination Unreachable |
| `8` | `0` | **Echo Request** (ping request) |
| `11` | `0` | Time Exceeded (TTL expired) |
| `12` | `0` | Parameter Problem |

For this assignment, we only use **Type 8** (Echo Request) and **Type 0** (Echo Reply).

## ICMP Echo Request/Reply Format

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Type      |     Code      |          Checksum             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Identifier          |        Sequence Number        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Payload (Data)                        |
|                            ...                                |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

| Field | Size | Description |
| :--- | :--- | :--- |
| **Type** | 1 byte | `8` for Echo Request, `0` for Echo Reply |
| **Code** | 1 byte | `0` for both |
| **Checksum** | 2 bytes | Internet checksum of the ICMP message |
| **Identifier** | 2 bytes | Unique ID (typically process ID) to match requests/replies |
| **Sequence Number** | 2 bytes | Incremented with each ping |
| **Payload** | Variable | Arbitrary data (commonly a timestamp for RTT) |

## How Ping Works

```
Client                                 Target Host
  │                                      │
  │  ICMP Echo Request (Type 8)          │
  │  [ID=1234, Seq=1, Payload=timestamp] │
  │ ─────────────────────────────────►   │
  │                                      │
  │  ICMP Echo Reply (Type 0)            │
  │  [ID=1234, Seq=1, Payload=timestamp] │
  │ ◄─────────────────────────────────   │
  │                                      │
  │  RTT = time_received - timestamp     │
```

The target host's OS kernel automatically processes Echo Requests and generates Echo Replies — no special server software is needed.

## Constructing an ICMP Packet in Python

```python
import struct

ICMP_ECHO_REQUEST = 8

# Create header with checksum = 0 (placeholder)
header = struct.pack(
    "!BBHHH",
    ICMP_ECHO_REQUEST,  # Type
    0,                   # Code
    0,                   # Checksum (placeholder)
    identifier,          # Identifier
    sequence,            # Sequence Number
)

# Payload: current timestamp as a double (8 bytes)
payload = struct.pack("!d", time.time())

# Compute checksum over header + payload
checksum = internet_checksum(header + payload)

# Rebuild header with correct checksum
header = struct.pack(
    "!BBHHH",
    ICMP_ECHO_REQUEST,
    0,
    checksum,
    identifier,
    sequence,
)

packet = header + payload
```

## Parsing an ICMP Reply

When receiving data from a raw socket, the response includes the **IP header** (typically 20 bytes) followed by the ICMP message:

```python
data, addr = raw_socket.recvfrom(1024)

# Skip IP header (20 bytes)
icmp_header = data[20:28]
icmp_type, code, checksum, pkt_id, sequence = struct.unpack("!BBHHH", icmp_header)

# Extract payload (timestamp)
payload = data[28:]
send_time = struct.unpack("!d", payload[:8])[0]
rtt = (time.time() - send_time) * 1000  # in ms
```

## IP Header Size Note

The IP header is **usually** 20 bytes but can vary if IP options are present. To be safe, extract the header length from the first byte:

```python
ip_header_length = (data[0] & 0x0F) * 4  # In bytes
icmp_data = data[ip_header_length:]
```
