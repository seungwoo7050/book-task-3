# TCP Flow Control and Congestion Control

## Flow Control

### Purpose

Flow control prevents the sender from overwhelming the receiver's buffer. The receiver advertises how much buffer space it has available using the **receive window** (`rwnd`) in the TCP header.

### Mechanism

```
Receiver Buffer (size = RcvBuffer)
┌─────────────────────────────────────┐
│  Used by app  │  Received  │  Free  │
│  (read)       │  (buffered)│ (rwnd) │
└─────────────────────────────────────┘

rwnd = RcvBuffer - [data received but not yet read by application]
```

The sender must ensure:

$$\text{LastByteSent} - \text{LastByteAcked} \leq \text{rwnd}$$

### In Wireshark

The **Window** field in the TCP header shows `rwnd`. With the **Window Scale** option, the actual window is:

$$\text{Actual Window} = \text{Window field} \times 2^{\text{shift count}}$$

If the window reaches **zero**, the sender stops transmitting (zero-window condition). It periodically sends **window probe** segments to check if the window has opened.

## Congestion Control

### Purpose

Congestion control prevents the sender from overwhelming the **network** (not just the receiver). TCP infers congestion from packet loss and adjusts its sending rate.

### Congestion Window (cwnd)

TCP maintains a **congestion window** (`cwnd`) variable. The effective sending window is:

$$\text{Effective Window} = \min(\text{cwnd}, \text{rwnd})$$

### TCP Congestion Control Phases

#### 1. Slow Start

When a connection begins (or after a timeout):
- `cwnd` starts at 1 MSS (or IW = Initial Window, often 10 MSS in modern stacks)
- For each ACK received, `cwnd` increases by 1 MSS
- This results in **exponential growth**: cwnd doubles every RTT

```
RTT 1: cwnd = 1 MSS  → send 1 segment
RTT 2: cwnd = 2 MSS  → send 2 segments
RTT 3: cwnd = 4 MSS  → send 4 segments
RTT 4: cwnd = 8 MSS  → send 8 segments
```

Slow start ends when:
- `cwnd` reaches `ssthresh` (slow start threshold) → switch to congestion avoidance
- Loss detected by timeout → set `ssthresh = cwnd/2`, reset `cwnd = 1 MSS`
- 3 duplicate ACKs → set `ssthresh = cwnd/2`, set `cwnd = ssthresh + 3 MSS` (fast recovery)

#### 2. Congestion Avoidance

After `cwnd` reaches `ssthresh`:
- For each RTT (all segments ACKed), `cwnd` increases by 1 MSS
- This results in **linear growth** (Additive Increase)

```
RTT N:   cwnd = 10 MSS
RTT N+1: cwnd = 11 MSS
RTT N+2: cwnd = 12 MSS
```

On loss:
- Timeout: `ssthresh = cwnd/2`, `cwnd = 1 MSS` (back to slow start)
- 3 dup ACKs: `ssthresh = cwnd/2`, `cwnd = ssthresh + 3 MSS` (fast recovery)

#### 3. Fast Recovery (TCP Reno)

After 3 duplicate ACKs:
- `ssthresh = cwnd / 2`
- `cwnd = ssthresh + 3 MSS` (inflate for the 3 dup ACKs)
- For each additional duplicate ACK: `cwnd += 1 MSS`
- When a new (non-duplicate) ACK arrives: `cwnd = ssthresh` → congestion avoidance

### AIMD (Additive Increase, Multiplicative Decrease)

TCP's congestion control is often described as AIMD:
- **Additive Increase**: Increase `cwnd` by 1 MSS per RTT (linear)
- **Multiplicative Decrease**: On loss, cut `cwnd` in half

This produces a characteristic **sawtooth** pattern in throughput over time.

### Visualizing in Wireshark

#### TCP Stream Graphs

In Wireshark: **Statistics → TCP Stream Graphs**

| Graph | What It Shows |
| :--- | :--- |
| **Time-Sequence (Stevens)** | Sequence numbers over time — slope = throughput |
| **Time-Sequence (tcptrace)** | Sequence numbers with ACKs and window |
| **Throughput** | Bytes per second over time |
| **Round-Trip Time** | RTT samples over time |
| **Window Scaling** | Advertised receive window over time |

#### Identifying Phases

- **Slow Start**: Steep exponential rise in the Time-Sequence graph
- **Congestion Avoidance**: Gentler linear rise
- **Loss Event**: Sudden drop in throughput or a retransmission marker
- **Sawtooth**: Repeated pattern of gradual increase followed by sharp decrease

## Summary: TCP vs UDP Comparison

| Feature | TCP | UDP |
| :--- | :--- | :--- |
| Connection | Connection-oriented (handshake) | Connectionless |
| Reliability | Guaranteed delivery (ACKs, retransmit) | Best-effort (no guarantees) |
| Ordering | In-order delivery | No ordering |
| Flow Control | Receive window (rwnd) | None |
| Congestion Control | cwnd, slow start, AIMD | None |
| Header Size | 20–60 bytes | 8 bytes |
| Use Cases | HTTP, FTP, SMTP, SSH | DNS, VoIP, streaming, gaming |
