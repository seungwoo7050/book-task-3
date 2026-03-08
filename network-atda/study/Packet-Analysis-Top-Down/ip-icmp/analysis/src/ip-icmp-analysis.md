# IP & ICMP Lab — Analysis Answers

## Trace Limitations

- This report uses only the repository-provided trace files.
- If a worksheet item needs packets that are not present in these traces, the answer is marked as `Not observable in this provided trace`.
- Missing values are not guessed; only decoded packet evidence is used.
- Numeric claims are tied to explicit frame references.

This analysis uses:
- `ip-traceroute.pcapng`
- `ip-fragmentation.pcapng`

## Part 1: IPv4 Header

**Trace file**: `ip-traceroute.pcapng`

### Question 1

**Q: First ICMP Echo Request — IP version, header length, total length?**

**A:**
- IP version: **4**
- Header length: **20 bytes** (`IHL=5`)
- Total length: **33 bytes**

**Evidence:** Frame **#1** IPv4 header fields.

---

### Question 2

**Q: Identification, Flags, Fragment Offset? What do they indicate?**

**A:**
- Identification: **0x0fa0**
- DF: **0**, MF: **0**
- Fragment Offset: **0**

This indicates the datagram is not fragmented.

**Evidence:** Frame **#1** IPv4 fragmentation fields.

---

### Question 3

**Q: TTL and Protocol field value?**

**A:**
- TTL: **1**
- Protocol: **1** (ICMP)

**Evidence:** Frame **#1** IPv4 `Time to Live` and `Protocol`.

---

### Question 4

**Q: Source and destination IP addresses?**

**A:**
- Source: **10.0.0.2**
- Destination: **93.184.216.34**

**Evidence:** Frame **#1** IPv4 `Source Address` / `Destination Address`.

---

### Question 5

**Q: How does TTL change across successive Echo Requests? Do Identification values change?**

**A:**
- Echo Request TTL values increment: **1 -> 2 -> 3** (frames #1, #3, #5)
- Identification values also increment: **0x0fa0 -> 0x0fa1 -> 0x0fa2**

**Evidence:** Frames #1, #3, #5.

---

### Question 6

**Q: First Time Exceeded message: source IP, TTL, ICMP type/code?**

**A:** First Time Exceeded is frame **#2**:
- Source IP: **10.0.0.1**
- IP TTL: **64**
- ICMP Type/Code: **11/0**

**Evidence:** Frame #2 outer IPv4 + ICMP headers.

---

### Question 7

**Q: Are Identification values same or different across successive Echo Requests? Why?**

**A:** They are **different** (`0x0fa0`, `0x0fa1`, `0x0fa2`) because each probe is a distinct IP datagram.

**Evidence:** Frames #1, #3, #5 `ip.id`.

---

### Question 8

**Q: How many distinct router IP addresses appear as ICMP Time Exceeded sources?**

**A:** **2 routers**:
- `10.0.0.1` (frame #2)
- `172.16.0.1` (frame #4)

---

## Part 2: IP Fragmentation

**Trace file**: `ip-fragmentation.pcapng`

### Question 9

**Q: First fragmented Echo Request — Identification, Flags, Fragment Offset per fragment?**

**A:** All fragments share `ip.id = 0x3039`.

| Frame | MF | Fragment Offset | `Offset*8` (bytes) |
| :--- | :--- | :--- | :--- |
| #1 | 1 | 0 | 0 |
| #2 | 1 | 175 | 1400 |
| #3 | 0 | 350 | 2800 |

---

### Question 10

**Q: How many fragments were created? How identify same original datagram?**

**A:** **3 fragments**. They are grouped by shared `ip.id=0x3039` plus consistent offset chain.

**Evidence:** Frames #1/#2/#3 share same source/destination/protocol/ID.

---

### Question 11

**Q: What fields change between fragments? What stays the same?**

**A:**
- Changes: `ip.flags.mf`, `ip.frag_offset`, `ip.len` (and header checksum)
- Same: source/destination IP, protocol (=ICMP), `ip.id=0x3039`, TTL (=64)

---

### Question 12

**Q: Verify fragmentation with Total Length and Offset*8.**

**A:**
- Frame #1: `ip.len=1420` -> payload `1400`, start `0`
- Frame #2: `ip.len=1420` -> payload `1400`, start `1400`
- Frame #3: `ip.len=728` -> payload `708`, start `2800`

Coverage:
- Bytes `[0..1399]`, `[1400..2799]`, `[2800..3507]`
- Reassembled payload size = **3508 bytes**.

Wireshark confirms: `[3 IPv4 Fragments (3508 bytes)]` and `[Reassembled IPv4 length: 3508]`.

---

### Question 13

**Q: MF flag values per fragment? Which has MF=0?**

**A:**
- Frames #1/#2: `MF=1`
- Frame #3: `MF=0` (last fragment)

---

### Question 14

**Q: How does reassembly work? Router or destination host? How shown in Wireshark?**

**A:** Reassembly is performed by the **destination host**, not by transit routers. Wireshark shows reassembly metadata on the final fragment (frame #3), including fragment list and reassembled length.

---

## Part 3: ICMP Messages

### Question 15

**Q: ICMP Type/Code for Echo Request and Echo Reply?**

**A:**
- Echo Request: **Type 8, Code 0** (frames #1/#3/#5)
- Echo Reply: **Type 0, Code 0** (frame #6)

---

### Question 16

**Q: ICMP Type/Code for Time Exceeded? Meaning?**

**A:** **Type 11, Code 0** (frames #2/#4). It means TTL expired in transit.

---

### Question 17

**Q: Do Echo Request/Reply share Identifier and Sequence Number? Purpose?**

**A:** Yes. Example:
- Request frame #5: Identifier **4660**, Sequence **3**
- Reply frame #6: Identifier **4660**, Sequence **3**

These fields match request↔reply pairs.

---

### Question 18

**Q: ICMP payload bytes in Echo Request? Compare with IP Total Length.**

**A:** For frame **#1**:
- IP total length = 33
- IP header = 20
- ICMP header = 8
- ICMP payload = `33 - 20 - 8 = 5 bytes`

This matches ICMP data `0x7472616365` (`"trace"`, 5 bytes).
