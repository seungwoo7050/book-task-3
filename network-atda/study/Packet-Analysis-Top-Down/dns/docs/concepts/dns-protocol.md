# DNS Protocol Reference

## Overview

The Domain Name System (DNS) is a distributed, hierarchical naming system that translates human-readable domain names (e.g., `www.example.com`) into IP addresses (e.g., `93.184.216.34`). DNS operates primarily over **UDP port 53**, though TCP port 53 is used for zone transfers and responses exceeding 512 bytes.

## DNS Message Format

Both queries and responses share the same message format:

```
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                      ID                         |  2 bytes — Transaction ID
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE    |  2 bytes — Flags
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    QDCOUNT                      |  2 bytes — # Questions
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ANCOUNT                      |  2 bytes — # Answer RRs
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    NSCOUNT                      |  2 bytes — # Authority RRs
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ARCOUNT                      |  2 bytes — # Additional RRs
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                   Questions                     |  Variable
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                   Answers                       |  Variable
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                   Authority                     |  Variable
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                   Additional                    |  Variable
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

### Header Flags

| Flag | Bits | Description |
| :--- | :--- | :--- |
| **QR** | 1 | 0 = Query, 1 = Response |
| **Opcode** | 4 | 0 = Standard query |
| **AA** | 1 | Authoritative Answer — set if the responding server is authoritative |
| **TC** | 1 | Truncation — response was truncated (use TCP to retry) |
| **RD** | 1 | Recursion Desired — client asks the server to recurse |
| **RA** | 1 | Recursion Available — server supports recursion |
| **RCODE** | 4 | 0 = No Error, 3 = Name Error (NXDOMAIN) |

### Question Section

Each question entry contains:

| Field | Description |
| :--- | :--- |
| **QNAME** | The domain name being queried (e.g., `www.example.com`) |
| **QTYPE** | The record type (A, AAAA, CNAME, NS, MX, etc.) |
| **QCLASS** | The class (almost always IN = Internet) |

### Resource Record (Answer/Authority/Additional)

Each resource record contains:

| Field | Description |
| :--- | :--- |
| **NAME** | The domain name this record applies to |
| **TYPE** | Record type (A, AAAA, CNAME, NS, MX, etc.) |
| **CLASS** | Class (IN for Internet) |
| **TTL** | Time to Live — seconds the record can be cached |
| **RDLENGTH** | Length of the RDATA field |
| **RDATA** | The record data (format depends on TYPE) |

## DNS Record Types

| Type | Value | Description | RDATA Format |
| :--- | :--- | :--- | :--- |
| **A** | 1 | IPv4 address mapping | 4-byte IPv4 address (e.g., `93.184.216.34`) |
| **AAAA** | 28 | IPv6 address mapping | 16-byte IPv6 address (e.g., `2606:2800:220:1::`) |
| **NS** | 2 | Authoritative name server | Domain name of the NS (e.g., `ns1.example.com`) |
| **CNAME** | 5 | Canonical name (alias) | Alias target (e.g., `example.com` → `cdn.example.net`) |
| **MX** | 15 | Mail exchange server | Preference + mail server domain (e.g., `10 mail.example.com`) |
| **SOA** | 6 | Start of authority | Primary NS, admin email, serial, timers |
| **TXT** | 16 | Text record | Arbitrary text string |
| **PTR** | 12 | Pointer (reverse DNS) | Domain name for reverse lookup |

## Example: DNS Query

```
Transaction ID: 0xa1b2
Flags: 0x0100 (Standard query, RD=1)
Questions: 1
  Name: www.example.com
  Type: A (1)
  Class: IN (1)
Answers: 0
Authority: 0
Additional: 0
```

## Example: DNS Response

```
Transaction ID: 0xa1b2  (matches the query)
Flags: 0x8180 (Response, RD=1, RA=1, No error)
Questions: 1
  Name: www.example.com
  Type: A (1)
  Class: IN (1)
Answers: 1
  Name: www.example.com
  Type: A
  Class: IN
  TTL: 300
  Address: 93.184.216.34
Authority: 0
Additional: 0
```

## Transaction ID Matching

The 16-bit **Transaction ID** field links queries to their responses. The client generates a random ID for each query, and the server echoes it in the response. In Wireshark, this appears as `dns.id`.

## DNS over UDP vs TCP

| Feature | UDP (default) | TCP (fallback) |
| :--- | :--- | :--- |
| Port | 53 | 53 |
| Message size limit | 512 bytes (or larger with EDNS0) | Unlimited |
| Connection setup | None (connectionless) | 3-way handshake |
| Use case | Most queries | Zone transfers, large responses |
