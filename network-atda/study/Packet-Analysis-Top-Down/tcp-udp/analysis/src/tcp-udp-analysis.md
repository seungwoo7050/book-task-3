# TCP & UDP Lab — Analysis Answers

## Trace Limitations

- This report uses only the repository-provided trace files.
- If a worksheet item needs packets that are not present in these traces, the answer is marked as `Not observable in this provided trace`.
- Missing values are not guessed; only decoded packet evidence is used.
- Numeric claims are tied to explicit frame references.

This analysis is based on:
- `tcp-upload.pcapng` (16 TCP packets)
- `udp-dns.pcapng` (2 UDP packets)

Because the TCP trace is very short, some textbook-level observations (full teardown, clear cwnd phase change) are not directly visible.

## Part 1: TCP Segment Structure

**Trace file**: `tcp-upload.pcapng`

### Question 1

**Q: What client/server IP and port are used?**

**A:**
- Client: **192.168.0.2:54000**
- Server: **128.119.245.12:80**

**Evidence:** Frame **#1** (`192.168.0.2:54000 -> 128.119.245.12:80`, SYN).

---

### Question 2

**Q: Sequence number of client SYN? Which field identifies SYN?**

**A:** Client SYN sequence number is **0** (relative numbering). The identifying field is `tcp.flags.syn = 1`.

**Evidence:** Frame **#1**: SYN set, ACK clear, `tcp.seq=0`.

---

### Question 3

**Q: Sequence/ack of SYN-ACK? How was ack determined?**

**A:** Server SYN-ACK has:
- `tcp.seq = 0`
- `tcp.ack = 1`

Ack is `client_syn_seq + 1`.

**Evidence:** Frame **#2**: SYN+ACK flags set, `seq=0`, `ack=1`.

---

### Question 4

**Q: Sequence/ack of segment containing HTTP POST command?**

**A:** HTTP POST appears in frame **#15** with:
- `tcp.seq = 1073`
- `tcp.ack = 1`

**Evidence:** Frame #15 has `http.request.method=POST`, `http.request.uri=/upload`.

---

### Question 5

**Q: First six client data segments: sequence, payload bytes, time, and acknowledgment.**

**A:** First six client data-bearing segments are frames **#4, #5, #7, #9, #11, #13**.

| Client Frame | Time (s) | Seq | Payload (`tcp.len`) | First ACK that covers it |
| :--- | :--- | :--- | :--- | :--- |
| #4 | 0.000358 | 1 | 72 | #6 (`ack=273`) |
| #5 | 0.000549 | 73 | 200 | #6 (`ack=273`) |
| #7 | 0.000858 | 273 | 200 | #8 (`ack=473`) |
| #9 | 0.001171 | 473 | 200 | #10 (`ack=673`) |
| #11 | 0.001481 | 673 | 200 | #12 (`ack=873`) |
| #13 | 0.001811 | 873 | 200 | #14 (`ack=1073`) |

---

## Part 2: TCP Connection Management

### Question 6

**Q: Minimum receiver window? Does it reach zero?**

**A:** Minimum advertised window from server packets is **8192** bytes (SYN-ACK). During data transfer, server advertises **64240** and never reaches zero.

**Evidence:**
- Frame #2 window: 8192
- Frames #6/#8/#10/#12/#14/#16 windows: 64240

---

### Question 7

**Q: Any retransmitted segments?**

**A:** **No retransmissions observed.**

**Evidence:** Filter `tcp.analysis.retransmission` returns no matching frames.

---

### Question 8

**Q: How much data did client transfer?**

**A:** **1272 bytes**.

Computation with relative sequence numbers:
- First client data starts at `seq=1`
- Last client data frame is #15 with `seq=1073`, `len=200`
- Last byte index = `1073 + 200 - 1 = 1272`
- Total transferred = `1272 - 1 + 1 = 1272 bytes`

(Equivalent sum of client `tcp.len`: `72 + 6*200 = 1272`)

---

### Question 9

**Q: Describe TCP teardown (FIN/ACK).**

**A:** **Not observable in this provided trace.** No FIN packets are present.

**Evidence:** No frame has `tcp.flags.fin = 1` in `tcp-upload.pcapng`.

---

## Part 3: TCP Throughput and RTT

### Question 10

**Q: Throughput (bytes/sec).**

**A:** Approximate throughput is **651,639 B/s** (about **5.21 Mb/s**).

Using:
- Total bytes = 1272
- Time window = first client data (#4 at 0.000358) to last server ACK (#16 at 0.002310)
- Duration = `0.002310 - 0.000358 = 0.001952 s`
- Throughput = `1272 / 0.001952 = 651,639 B/s`

---

### Question 11

**Q: Time-Sequence (Stevens) graph pattern?**

**A:** The transfer is very short and appears as a small monotonic staircase (sequence increases in fixed 200-byte steps after the initial 72-byte segment). The short capture is insufficient to show long-run rate transitions.

**Evidence:** Client sequence progression:
`1 -> 73 -> 273 -> 473 -> 673 -> 873 -> 1073`.

---

### Question 12

**Q: Approximate RTT and variation.**

**A:** RTT is around **0.19–0.21 ms** with little variation.

Sample segment-to-ACK deltas:
- #5 -> #6: `0.000740 - 0.000549 = 0.191 ms`
- #7 -> #8: `0.195 ms`
- #9 -> #10: `0.191 ms`
- #11 -> #12: `0.213 ms`
- #13 -> #14: `0.190 ms`
- #15 -> #16: `0.192 ms`

---

## Part 4: TCP Congestion Control

### Question 13

**Q: Identify slow start and congestion avoidance phases.**

**A:** With only 7 client data segments, a clear slow-start to congestion-avoidance transition point is **not reliably observable** in this trace.

**Evidence:** Capture duration and data volume are too small to expose multi-RTT cwnd evolution.

---

### Question 14

**Q: Initial congestion window estimate and growth.**

**A:** Initial send burst before first ACK contains **2 segments** (frames #4 and #5), so initial cwnd is approximately **2 segments** in this trace. Further growth pattern is not rich enough to estimate full slow-start dynamics.

---

## Part 5: UDP

**Trace file**: `udp-dns.pcapng`

### Question 15

**Q: How many UDP header fields? Name them.**

**A:** UDP header has **4 fields**:
1. Source Port
2. Destination Port
3. Length
4. Checksum

---

### Question 16

**Q: Length (bytes) of each UDP header field?**

**A:** Each field is **2 bytes**.

Total UDP header = `2 + 2 + 2 + 2 = 8 bytes`.

---

### Question 17

**Q: UDP Length field specifies what? Verify with packet.**

**A:** UDP Length is **header + payload** size.

**Evidence:** Query frame **#1** has `udp.length=36`.
- Header: 8 bytes
- Payload: `36 - 8 = 28 bytes`

---

### Question 18

**Q: Maximum UDP payload bytes?**

**A:**
- From UDP Length field max (`65535`), theoretical max payload is **65527 bytes** (`65535 - 8`).
- Over IPv4 with 20-byte IP header, practical max payload is **65507 bytes**.

---

### Question 19

**Q: Largest possible source port number?**

**A:** **65535**.

---

### Question 20

**Q: IP protocol number for UDP and TCP?**

**A:**
- UDP: **17**
- TCP: **6**

**Evidence:** `udp-dns.pcapng` packets show `ip.proto=17`; TCP trace uses protocol 6.

---

### Question 21

**Q: Relationship of port numbers in DNS query/response UDP pair?**

**A:** Ports are reversed between request and response.

**Evidence:**
- Query frame **#1**: `55000 -> 53`
- Response frame **#2**: `53 -> 55000`
