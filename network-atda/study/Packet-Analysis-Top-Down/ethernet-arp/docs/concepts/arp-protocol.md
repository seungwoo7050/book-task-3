# ARP Protocol Reference

## Overview

The Address Resolution Protocol (ARP) maps **IP addresses** to **MAC addresses** on a local network. When a host needs to send an IP datagram to another host on the same subnet, it must know the destination's MAC address. If the mapping is not in the ARP cache, the host broadcasts an ARP request.

ARP is defined in **RFC 826** and operates at the boundary between the network layer and the link layer.

## When ARP Is Needed

```
Host A wants to send to Host B (same subnet):
  - Host A knows: B's IP address (192.168.1.5)
  - Host A needs: B's MAC address (??:??:??:??:??:??)
  
Solution: Host A sends an ARP request to find B's MAC address
```

ARP is only needed for **hosts on the same subnet**. For hosts on different subnets, the sender uses ARP to resolve the **default gateway's** MAC address and sends the frame to the router.

## ARP Message Format

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Hardware Type         |         Protocol Type         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| HW Addr Len   | Proto Addr Len|           Opcode              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Sender Hardware Address                    |
|                    (6 bytes for Ethernet)                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Sender Protocol Address                    |
|                    (4 bytes for IPv4)                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Target Hardware Address                    |
|                    (6 bytes for Ethernet)                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Target Protocol Address                    |
|                    (4 bytes for IPv4)                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Fields

| Field | Size | Description |
| :--- | :--- | :--- |
| **Hardware Type** | 2 bytes | Type of link-layer address (1 = Ethernet) |
| **Protocol Type** | 2 bytes | Type of network-layer address (0x0800 = IPv4) |
| **HW Address Length** | 1 byte | Length of hardware address (6 for Ethernet MAC) |
| **Protocol Address Length** | 1 byte | Length of protocol address (4 for IPv4) |
| **Opcode** | 2 bytes | Operation: **1** = ARP Request, **2** = ARP Reply |
| **Sender Hardware Address** | 6 bytes | MAC address of the sender |
| **Sender Protocol Address** | 4 bytes | IP address of the sender |
| **Target Hardware Address** | 6 bytes | MAC address of the target (00:00:00:00:00:00 in requests) |
| **Target Protocol Address** | 4 bytes | IP address of the target |

## ARP Request / Reply Flow

```
Step 1: ARP Request (Broadcast)
  Ethernet: Src=A_MAC, Dst=ff:ff:ff:ff:ff:ff, Type=0x0806
  ARP:      Opcode=1 (Request)
            Sender MAC=A_MAC, Sender IP=A_IP
            Target MAC=00:00:00:00:00:00, Target IP=B_IP
  
  → "Who has B_IP? Tell A_IP (A_MAC)"
  → All hosts on the LAN receive this broadcast

Step 2: ARP Reply (Unicast)
  Ethernet: Src=B_MAC, Dst=A_MAC, Type=0x0806
  ARP:      Opcode=2 (Reply)
            Sender MAC=B_MAC, Sender IP=B_IP
            Target MAC=A_MAC, Target IP=A_IP

  → "B_IP is at B_MAC"
  → Only Host A receives this unicast reply

Step 3: Host A adds entry to ARP cache
  B_IP → B_MAC (TTL: ~60-300 seconds)

Step 4: Host A sends IP packet to B
  Ethernet: Src=A_MAC, Dst=B_MAC, Type=0x0800
  IP:       Src=A_IP, Dst=B_IP, ...
```

## ARP Cache

Each host maintains an **ARP cache** (also called ARP table) that stores recent IP-to-MAC mappings.

### Viewing the ARP Cache

| OS | Command |
| :--- | :--- |
| macOS | `arp -a` |
| Linux | `arp -n` or `ip neigh show` |
| Windows | `arp -a` |

### Cache Entry Example

```
? (192.168.1.1) at aa:bb:cc:dd:ee:ff on en0 ifscope [ethernet]
? (192.168.1.5) at 11:22:33:44:55:66 on en0 ifscope [ethernet]
```

### Cache Timeout

ARP cache entries typically expire after **60 seconds** (Linux) to **5 minutes** (varies by OS). When an entry expires, the next packet to that IP triggers a new ARP request.

### Clearing the Cache

```bash
# macOS
sudo arp -a -d

# Linux
sudo ip neigh flush all

# Windows
netsh interface ip delete arpcache
```

## Gratuitous ARP

A **gratuitous ARP** is an ARP request or reply where the sender and target IP are the same. It serves two purposes:
1. **Announce** a new IP address to the network
2. **Detect IP conflicts** — if another host replies, a duplicate IP exists

## ARP and Security

ARP has no authentication, making it vulnerable to:
- **ARP Spoofing** — An attacker sends fake ARP replies to redirect traffic
- **ARP Cache Poisoning** — Corrupting the ARP cache to perform man-in-the-middle attacks
