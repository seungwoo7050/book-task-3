# Ethernet Frame Reference

## Overview

Ethernet is the dominant wired **link-layer** technology for local area networks (LANs). It defines how data is framed for transmission over physical media (copper, fiber) and uses **MAC addresses** for local delivery.

## Ethernet Frame Structure (IEEE 802.3)

```
┌──────────┬──────────┬──────────┬──────────────┬─────────┬─────┐
│ Preamble │   SFD    │   Dest   │   Source     │EtherType│     │
│ (7 bytes)│ (1 byte) │   MAC    │   MAC        │(2 bytes)│     │
│          │          │ (6 bytes)│  (6 bytes)   │         │     │
├──────────┴──────────┴──────────┴──────────────┴─────────┤     │
│                                                         │ FCS │
│                    Payload (46–1500 bytes)               │(4 B)│
│                                                         │     │
└─────────────────────────────────────────────────────────┴─────┘
```

### Fields

| Field | Size | Description |
| :--- | :--- | :--- |
| **Preamble** | 7 bytes | Alternating 10101010 pattern for clock synchronization |
| **SFD** | 1 byte | Start Frame Delimiter (10101011) — marks frame start |
| **Destination MAC** | 6 bytes | 48-bit hardware address of the intended receiver |
| **Source MAC** | 6 bytes | 48-bit hardware address of the sender |
| **EtherType / Length** | 2 bytes | Protocol type (≥ 0x0600) or frame length (< 0x0600) |
| **Payload** | 46–1500 bytes | Data from the upper layer (IP datagram, ARP message, etc.) |
| **FCS** | 4 bytes | Frame Check Sequence (CRC-32 for error detection) |

> **Note**: Wireshark captures do NOT show the Preamble, SFD, or FCS — these are handled by the NIC hardware.

### What Wireshark Shows

```
Ethernet II, Src: aa:bb:cc:dd:ee:ff, Dst: 11:22:33:44:55:66
    Destination: 11:22:33:44:55:66
    Source: aa:bb:cc:dd:ee:ff
    Type: IPv4 (0x0800)
```

## MAC Addresses

### Format

A MAC address is **48 bits (6 bytes)**, written as 6 hex pairs separated by colons or hyphens:

```
aa:bb:cc:dd:ee:ff   or   AA-BB-CC-DD-EE-FF
```

### Structure

| Portion | Bytes | Description |
| :--- | :--- | :--- |
| **OUI** | First 3 bytes | Organizationally Unique Identifier — identifies the NIC manufacturer |
| **NIC-specific** | Last 3 bytes | Unique identifier assigned by the manufacturer |

### Special Addresses

| Address | Meaning |
| :--- | :--- |
| `ff:ff:ff:ff:ff:ff` | **Broadcast** — delivered to all hosts on the LAN |
| `01:xx:xx:xx:xx:xx` | **Multicast** — least significant bit of first byte is 1 |
| Any other | **Unicast** — delivered to a specific host |

### Unicast vs Broadcast

- **Unicast frame**: Destination MAC is a specific device's address → only that device processes it
- **Broadcast frame**: Destination MAC is `ff:ff:ff:ff:ff:ff` → all devices on the LAN receive and process it
- ARP requests use **broadcast**; ARP replies use **unicast**

## EtherType Values

| EtherType | Protocol |
| :--- | :--- |
| `0x0800` | IPv4 |
| `0x0806` | ARP |
| `0x86DD` | IPv6 |
| `0x8100` | VLAN-tagged frame (802.1Q) |

## Frame Size

| Metric | Value |
| :--- | :--- |
| Minimum frame size (without preamble/FCS) | 60 bytes |
| Minimum payload | 46 bytes (padded if smaller) |
| Maximum payload (MTU) | 1500 bytes |
| Maximum frame size | 1518 bytes |
| Jumbo frames (optional) | Up to 9000 bytes payload |

## How Ethernet Relates to IP

```
Application Data → TCP/UDP → IP Datagram → Ethernet Frame → Physical Medium
```

The IP datagram becomes the **payload** of the Ethernet frame. The Ethernet header provides **local** (hop-by-hop) delivery using MAC addresses, while the IP header provides **end-to-end** delivery using IP addresses.

At each router hop, the Ethernet header is stripped and a new one is created with the next-hop's MAC address, but the IP header remains the same (except TTL decrement).
