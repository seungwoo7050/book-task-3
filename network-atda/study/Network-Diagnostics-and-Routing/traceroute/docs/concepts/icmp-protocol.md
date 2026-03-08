# ICMP Protocol Reference

## Overview

The Internet Control Message Protocol (ICMP) is a network-layer companion to IP, defined in **RFC 792**. ICMP messages are encapsulated directly in IP datagrams (Protocol = 1). They are used for error reporting and diagnostic functions — not for carrying application data.

## ICMP Message Format

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Type      |     Code      |          Checksum             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Type-specific Data                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

| Field | Size | Description |
| :--- | :--- | :--- |
| **Type** | 8 bits | ICMP message type |
| **Code** | 8 bits | Subtype (further detail) |
| **Checksum** | 16 bits | Error detection over the entire ICMP message |
| **Data** | Variable | Type-dependent (echo ID/seq, or original IP header + 8 bytes) |

## ICMP Message Types

### Common Types for This Lab

| Type | Code | Name | Description |
| :--- | :--- | :--- | :--- |
| **0** | 0 | Echo Reply | Response to an Echo Request (ping response) |
| **3** | 0 | Destination Unreachable: Net | Network unreachable |
| **3** | 1 | Destination Unreachable: Host | Host unreachable |
| **3** | 3 | Destination Unreachable: Port | Port unreachable (used by traceroute on Linux) |
| **8** | 0 | Echo Request | Ping request |
| **11** | 0 | Time Exceeded: TTL | TTL expired in transit (used by traceroute) |
| **11** | 1 | Time Exceeded: Fragment | Fragment reassembly time exceeded |

## Echo Request / Echo Reply (Ping)

### Format

```
Type: 8 (request) or 0 (reply)
Code: 0
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identifier            |        Sequence Number        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                          Data (payload)                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

| Field | Purpose |
| :--- | :--- |
| **Identifier** | Unique ID to match requests with replies (typically process ID) |
| **Sequence Number** | Increments with each successive Echo Request |
| **Data** | Arbitrary payload (often timestamps or pattern bytes) |

The Echo Reply copies the Identifier, Sequence Number, and Data from the request. This allows the sender to match replies to requests and calculate RTT.

### Ping Workflow

```
Host A → ICMP Echo Request (Type 8, Code 0, ID=1234, Seq=1) → Host B
Host A ← ICMP Echo Reply  (Type 0, Code 0, ID=1234, Seq=1) ← Host B
```

## Time Exceeded (Traceroute)

### How Traceroute Works

1. Send an IP datagram with **TTL = 1** to the destination
2. The first router decrements TTL to 0 and sends back **ICMP Time Exceeded** (Type 11, Code 0)
3. Send another datagram with **TTL = 2** → the second router replies
4. Continue until the destination is reached:
   - Linux `traceroute`: sends UDP to a high port → destination replies with **ICMP Port Unreachable** (Type 3, Code 3)
   - Windows `tracert`: sends ICMP Echo Request → destination replies with **ICMP Echo Reply** (Type 0)

### Time Exceeded Payload

The ICMP Time Exceeded message includes:
- The **IP header** of the original datagram that caused the error
- The first **8 bytes** of the original datagram's payload

This helps the sender identify which datagram triggered the error.

## ICMP in the IP Protocol Stack

```
Application Layer
Transport Layer (TCP / UDP)
Network Layer: IP + ICMP
Link Layer
Physical Layer
```

ICMP is considered part of the **network layer** but is encapsulated **inside** IP datagrams:

```
Ethernet Frame → IP Header (Protocol = 1) → ICMP Message
```

ICMP is NOT a transport-layer protocol — it does not carry application data.
