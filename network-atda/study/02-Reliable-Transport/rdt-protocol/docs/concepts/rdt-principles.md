# Principles of Reliable Data Transfer

## The Problem

The transport layer must provide **reliable data transfer** even though the underlying network layer (IP) is **unreliable**. Packets can be:

- **Lost**: Dropped by routers or corrupted beyond repair
- **Corrupted**: Bits flipped during transmission
- **Reordered**: Arriving in a different order than sent
- **Duplicated**: Delivered more than once

## Building Blocks for Reliability

### 1. Checksums — Detecting Corruption

A **checksum** is a value computed from the packet data that allows the receiver to detect whether the data was altered in transit.

**How it works:**
1. Sender computes `checksum = hash(data)` and includes it in the packet header
2. Receiver recomputes the hash of the received data
3. If computed hash ≠ received checksum → packet is corrupt → discard

```python
import hashlib

def checksum(data: bytes) -> bytes:
    return hashlib.md5(data).digest()[:4]  # 4-byte checksum
```

### 2. Acknowledgments (ACKs) — Receiver Feedback

The receiver sends **ACK** (acknowledgment) packets to tell the sender that a packet was received correctly.

- **Positive ACK**: "I received packet N correctly"
- **Negative ACK (NAK)**: "Packet N was corrupt" (used in rdt 2.0, replaced by duplicate ACKs in rdt 3.0)

### 3. Sequence Numbers — Detecting Duplicates

Each packet carries a **sequence number**. The receiver uses it to:
- Detect **duplicate** packets (retransmissions of already-received data)
- Detect **out-of-order** packets
- Know which packet to expect next

For stop-and-wait (rdt 3.0), only 2 sequence numbers are needed: **0** and **1** (alternating bit).

### 4. Retransmission Timer — Detecting Loss

The sender starts a **timer** after sending each packet. If the timer expires before an ACK is received, the sender assumes the packet (or its ACK) was lost and **retransmits**.

```
Sender:                    Receiver:
  send(pkt, seq=0)  →        receives pkt, seq=0
  start_timer()              send(ACK 0) →
  ...ACK lost...
  TIMEOUT!
  resend(pkt, seq=0) →       receives pkt, seq=0 (duplicate)
                              send(ACK 0) → (re-ACK)
  receive(ACK 0) ✓
```

### Choosing Timeout Duration

- **Too short**: Premature retransmissions (unnecessary traffic)
- **Too long**: Slow recovery from actual losses

A typical approach: set timeout slightly larger than the estimated RTT.

## Evolution of RDT Protocols

| Protocol | Handles | Mechanism |
| :--- | :--- | :--- |
| rdt 1.0 | Reliable channel | No mechanisms needed |
| rdt 2.0 | Corruption | Checksum + ACK/NAK |
| rdt 2.1 | Corruption + ACK corruption | Checksum + Seq Nums + ACK/NAK |
| rdt 2.2 | Same as 2.1, NAK-free | Duplicate ACKs instead of NAK |
| **rdt 3.0** | Corruption + Loss | Checksum + Seq Nums + Timer |

## Utilization Problem

Stop-and-wait has poor **utilization** — the sender is idle while waiting for each ACK:

$$
U_{sender} = \frac{L/R}{RTT + L/R}
$$

Where:
- $L$ = packet length (bits)
- $R$ = link rate (bits/sec)
- $RTT$ = round-trip time

For a 1 Gbps link with 30 ms RTT and 8000-bit packets:

$$
U_{sender} = \frac{8000 / 10^9}{0.030 + 8000/10^9} = \frac{0.008\text{ms}}{30.008\text{ms}} \approx 0.00027
$$

This is why **pipelining** (Go-Back-N, Selective Repeat) is needed.
