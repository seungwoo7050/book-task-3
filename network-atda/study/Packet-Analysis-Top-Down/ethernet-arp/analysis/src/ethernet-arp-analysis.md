# Ethernet & ARP Lab — Analysis Answers

## Trace Limitations

- This report uses only the repository-provided trace file.
- If a worksheet item needs packets that are not present in this trace, the answer is marked as `Not observable in this provided trace`.
- Missing values are not guessed; only decoded packet evidence is used.
- Numeric claims are tied to explicit frame references.

This analysis uses `ethernet-arp.pcapng` (3 frames total). The trace is minimal and does not contain an HTTP GET packet.

## Part 1: Ethernet Frame Structure

### Question 1

**Q: Destination MAC in ARP request frame? Unicast or broadcast?**

**A:** Destination MAC is **ff:ff:ff:ff:ff:ff** (broadcast).

**Evidence:** Frame **#1** Ethernet II destination address.

---

### Question 2

**Q: Source MAC in same frame? What device does it belong to?**

**A:** Source MAC is **00:11:22:33:44:55**. In this trace it is the requesting host (the local machine that sends ARP query for gateway MAC).

**Evidence:** Frame **#1**:
- Ethernet source: `00:11:22:33:44:55`
- ARP sender IP: `192.168.0.2`

---

### Question 3

**Q: EtherType value? What upper-layer protocol?**

**A:** EtherType is **0x0806**, indicating **ARP**.

**Evidence:** Frame **#1** Ethernet `Type: ARP (0x0806)`.

---

### Question 4

**Q: Byte offset of ASCII "G" in "GET" for an HTTP packet?**

**A:** **Not observable in this provided trace.** There is no HTTP packet (only ARP request/reply and one IP frame).

**Evidence:** `http.request` filter matches zero frames in `ethernet-arp.pcapng`.

---

### Question 5

**Q: Ethernet destination in ARP reply frame? Broadcast or unicast?**

**A:** Destination MAC is **00:11:22:33:44:55** and it is **unicast**.

**Evidence:** Frame **#2** Ethernet destination address.

---

### Question 6

**Q: EtherType in frame carrying IP datagram? How differs from ARP frame?**

**A:**
- IP frame EtherType: **0x0800** (IPv4)
- ARP frame EtherType: **0x0806** (ARP)

**Evidence:**
- Frame **#3**: `eth.type=0x0800`
- Frames **#1/#2**: `eth.type=0x0806`

---

## Part 2: ARP Protocol

### Question 7

**Q: Hex source/destination MAC in ARP request frame?**

**A:** Frame **#1**:
- Source MAC: **00:11:22:33:44:55**
- Destination MAC: **ff:ff:ff:ff:ff:ff**

---

### Question 8

**Q: Opcode in ARP request? Meaning?**

**A:** Opcode is **1** = **ARP Request**.

**Evidence:** Frame #1 `arp.opcode=1`.

---

### Question 9

**Q: Does ARP request contain sender IP? What is it?**

**A:** Yes. Sender IP is **192.168.0.2**.

**Evidence:** Frame #1 `arp.src.proto_ipv4=192.168.0.2`.

---

### Question 10

**Q: What target IP is queried in ARP request?**

**A:** Target IP is **192.168.0.1**.

**Evidence:** Frame #1 `arp.dst.proto_ipv4=192.168.0.1`.

---

### Question 11

**Q: Target MAC in ARP request? Why this value?**

**A:** Target MAC is **00:00:00:00:00:00** because the requester does not yet know the MAC for `192.168.0.1`.

**Evidence:** Frame #1 `arp.dst.hw_mac=00:00:00:00:00:00`.

---

### Question 12

**Q: ARP reply opcode and sender MAC?**

**A:**
- Opcode: **2** (ARP Reply)
- Sender MAC: **66:77:88:99:aa:bb**

**Evidence:** Frame **#2** `arp.opcode=2`, `arp.src.hw_mac=66:77:88:99:aa:bb`.

---

### Question 13

**Q: Destination MAC in ARP reply Ethernet frame? How determined?**

**A:** Destination MAC is **00:11:22:33:44:55**. It is copied from the ARP request sender MAC so the reply is sent directly back to requester.

**Evidence:**
- Frame #1 requester MAC: `00:11:22:33:44:55`
- Frame #2 Ethernet destination: `00:11:22:33:44:55`

---

### Question 14

**Q: After ARP exchange, does next IP packet use resolved MAC?**

**A:** Yes.

**Evidence:**
- ARP reply (frame #2) says `192.168.0.1 -> 66:77:88:99:aa:bb`
- Next IP frame (frame #3) has Ethernet destination **66:77:88:99:aa:bb**.

---

## Part 3: ARP Cache

### Question 15

**Q: Command to display ARP cache? What does each entry contain?**

**A:**
- Linux/macOS: `arp -a` or `ip neigh`
- Windows: `arp -a`

Typical entry fields: IP address, MAC address, interface, state/type (dynamic/static, reachable/stale).

---

### Question 16

**Q: Typical timeout for ARP cache entries? What happens on expiry?**

**A:** Timeout is OS-dependent (commonly tens of seconds to minutes). When expired, host sends a new ARP request before sending next L3 packet to that IP.

**Trace relation:** This pcap does not include long-duration timing, so timeout value itself is not directly measurable here.

---

### Question 17

**Q: If ARP cache is cleared then host is accessed, what traffic appears?**

**A:** Exactly the sequence seen here:
1. ARP Request (broadcast) — frame #1
2. ARP Reply (unicast) — frame #2
3. Then IP traffic using resolved MAC — frame #3
