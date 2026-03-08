# UDP Protocol Reference

## Overview

The User Datagram Protocol (UDP) is a **minimal, connectionless** transport-layer protocol defined in RFC 768. It provides a thin layer over IP, adding only port multiplexing and an optional checksum.

## UDP Datagram Structure

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|            Length              |           Checksum            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Header Fields

| Field | Size | Description |
| :--- | :--- | :--- |
| **Source Port** | 16 bits (2 bytes) | Sending application's port number |
| **Destination Port** | 16 bits (2 bytes) | Receiving application's port number |
| **Length** | 16 bits (2 bytes) | Total length of UDP header + data (minimum 8 bytes) |
| **Checksum** | 16 bits (2 bytes) | Error detection (computed over header + data + pseudo-header) |

The UDP header is exactly **8 bytes**. There are only 4 fields.

### Length Field

The Length field specifies the total length of the UDP datagram in bytes, including both the 8-byte header and the payload:

$$\text{Length} = 8 + \text{payload size}$$

Since the Length field is 16 bits, the maximum value is $2^{16} - 1 = 65535$ bytes. Therefore:

$$\text{Max payload} = 65535 - 8 = 65527 \text{ bytes}$$

### Port Numbers

Port numbers are 16-bit unsigned integers:
- Range: 0 to $2^{16} - 1$ = **65535**
- Well-known ports: 0–1023 (e.g., DNS = 53, HTTP = 80)
- Registered ports: 1024–49151
- Ephemeral ports: 49152–65535 (used by clients)

### Checksum

The UDP checksum covers:
1. A **pseudo-header** derived from the IP header (source IP, dest IP, protocol, UDP length)
2. The **UDP header**
3. The **UDP payload**

The checksum is optional in IPv4 (set to 0 if not computed) but mandatory in IPv6.

## UDP in Wireshark

In Wireshark, selecting a UDP packet shows:

```
User Datagram Protocol, Src Port: 52345, Dst Port: 53
    Source Port: 52345
    Destination Port: 53
    Length: 42
    Checksum: 0x1a2b [correct]
    [Checksum Status: Good]
    [Stream index: 0]
```

## IP Protocol Numbers

| Protocol | Number in IP Header |
| :--- | :--- |
| ICMP | 1 |
| TCP | 6 |
| UDP | 17 |

In the IP header, the **Protocol** field identifies the transport-layer protocol. For UDP, this value is **17** (0x11). For TCP, it is **6** (0x06).

## DNS over UDP: Port Relationship

When a DNS client sends a query:
- **Query**: Source = ephemeral port (e.g., 52345), Destination = **53**
- **Response**: Source = **53**, Destination = ephemeral port (e.g., 52345)

The source and destination ports are **swapped** between the query and the response. This is how the OS knows which application should receive the DNS response.

## Why UDP for DNS?

| Reason | Explanation |
| :--- | :--- |
| **Low overhead** | 8-byte header vs TCP's 20+ bytes |
| **No handshake** | Saves 1 RTT delay (TCP needs 3-way handshake before data) |
| **Simple queries** | DNS queries/responses are typically small (< 512 bytes) |
| **Stateless** | Server doesn't need to maintain connection state per client |

DNS falls back to TCP when:
- A response is too large (> 512 bytes or EDNS0 limit)
- Zone transfers (AXFR) are required
