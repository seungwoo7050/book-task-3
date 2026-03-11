# IPv4 Header Reference

## Overview

The Internet Protocol version 4 (IPv4) is the primary network-layer protocol responsible for addressing and routing datagrams across internetworks. Every IP datagram carries a 20-byte (minimum) header containing all the information needed for routing and delivery.

## IPv4 Header Structure

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |    DSCP   |ECN|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (if IHL > 5)                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Header Fields

| Field | Size | Description |
| :--- | :--- | :--- |
| **Version** | 4 bits | IP version (4 for IPv4) |
| **IHL** | 4 bits | Internet Header Length in 32-bit words (minimum 5 = 20 bytes) |
| **DSCP** | 6 bits | Differentiated Services Code Point (QoS) |
| **ECN** | 2 bits | Explicit Congestion Notification |
| **Total Length** | 16 bits | Total datagram size in bytes (header + data). Max = 65,535 bytes |
| **Identification** | 16 bits | Unique ID for the datagram (used for fragment reassembly) |
| **Flags** | 3 bits | Bit 0: Reserved. Bit 1: DF (Don't Fragment). Bit 2: MF (More Fragments) |
| **Fragment Offset** | 13 bits | Position of this fragment in the original datagram (in 8-byte units) |
| **TTL** | 8 bits | Time to Live — decremented by each router; datagram discarded at 0 |
| **Protocol** | 8 bits | Upper-layer protocol (1=ICMP, 6=TCP, 17=UDP) |
| **Header Checksum** | 16 bits | Error detection for the header only (recomputed at each hop) |
| **Source Address** | 32 bits | Sender's IPv4 address |
| **Destination Address** | 32 bits | Receiver's IPv4 address |

## IP Fragmentation

### Why Fragmentation Occurs

Each link has a **Maximum Transmission Unit (MTU)** — the maximum frame payload size. For Ethernet, MTU = **1500 bytes**. If an IP datagram exceeds the link's MTU, the router must fragment it.

### Fragmentation Fields

| Field | Role in Fragmentation |
| :--- | :--- |
| **Identification** | Same value for all fragments of the same original datagram |
| **MF (More Fragments)** | 1 = more fragments follow; 0 = this is the last (or only) fragment |
| **Fragment Offset** | Position in the original datagram's data, in 8-byte units |
| **Total Length** | Size of THIS fragment (header + fragment data) |

### Fragmentation Example

Original datagram: 4000 bytes total (20-byte header + 3980 bytes data), MTU = 1500.

| Fragment | ID | MF | Offset | Total Length | Data Bytes | Byte Range |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 12345 | 1 | 0 | 1500 | 1480 | 0–1479 |
| 2 | 12345 | 1 | 185 | 1500 | 1480 | 1480–2959 |
| 3 | 12345 | 0 | 370 | 1040 | 1020 | 2960–3979 |

Fragment Offset is in 8-byte units: $185 \times 8 = 1480$, $370 \times 8 = 2960$.

### Reassembly

- Reassembly occurs only at the **destination host**, not at intermediate routers
- The destination uses Identification, Fragment Offset, and MF flag to reconstruct
- If any fragment is lost, the entire datagram is discarded (IP provides no retransmission)
- Wireshark shows reassembled datagrams with `[Reassembled IPv4]` annotations

## TTL (Time to Live)

- Set by the sender (common initial values: 64, 128, 255)
- Each router decrements TTL by 1
- If TTL reaches 0, the router **discards** the datagram and sends an **ICMP Time Exceeded** message back to the source
- Purpose: prevents datagrams from circulating indefinitely due to routing loops

### TTL and Traceroute

`traceroute` exploits TTL behavior:
1. Send a packet with TTL = 1 → first router decrements to 0, sends ICMP Time Exceeded
2. Send a packet with TTL = 2 → second router sends ICMP Time Exceeded
3. Continue increasing TTL until the destination is reached (ICMP Echo Reply or Port Unreachable)

Each ICMP Time Exceeded reply reveals the IP address of one router along the path.

## Protocol Numbers

| Number | Protocol |
| :--- | :--- |
| 1 | ICMP |
| 6 | TCP |
| 17 | UDP |
| 41 | IPv6 encapsulation |
| 89 | OSPF |
