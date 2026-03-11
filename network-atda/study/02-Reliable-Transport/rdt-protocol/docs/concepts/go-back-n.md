# Go-Back-N (GBN) Protocol

## Overview

Go-Back-N is a **pipelined** reliable data transfer protocol that allows the sender to have up to **N** unacknowledged packets outstanding at any time. It uses:

- A **sliding window** of size N at the sender
- **Cumulative ACKs**: ACK n means "all packets up to and including n are received"
- A single **timer** for the oldest unacknowledged packet
- On timeout, retransmit **all** packets in the window

## Sliding Window

```
                    Window (size N=4)
                 ┌───────────────────┐
  [0][1][2][3]   │[4][5][6][7]       │  [8][9][10]...
  ▲              ▲              ▲     │
  ACKed          base           next  │  Not yet
  (done)         (oldest        seq   │  sendable
                  unACKed)            │
                 └───────────────────┘

  Sequence number space:
  ├── Already ACKed ──┤── Window (sendable) ──┤── Not usable yet ──►
      [0, base)           [base, base+N)          [base+N, ∞)
```

### Window Variables

- `base`: Sequence number of the oldest unacknowledged packet
- `nextseqnum`: Sequence number of the next packet to send
- Window: `[base, base + N)`

## Sender Rules

1. **Data from application:**
   - If `nextseqnum < base + N` (window not full): send packet, increment `nextseqnum`
   - If `nextseqnum >= base + N` (window full): refuse/buffer the data

2. **ACK n received:**
   - Set `base = n + 1` (cumulative: all packets up to n are ACKed)
   - If `base == nextseqnum`: stop timer (all ACKed)
   - Else: restart timer (more unACKed packets)

3. **Timeout:**
   - Retransmit all packets from `base` to `nextseqnum - 1`
   - Restart timer

## Receiver Rules

1. **Packet with expected seq and not corrupt:**
   - Deliver to application
   - Send ACK with this seq number
   - Increment expected seq

2. **Any other packet (corrupt, out-of-order, duplicate):**
   - Discard
   - Re-send ACK for `expectedseqnum - 1` (last correctly received)

The GBN receiver is **simple** — it does not buffer out-of-order packets.

## Example Scenario (N=4)

```
Sender                                          Receiver
  │  pkt 0 ─────────────────────────────────►  │ deliver, ACK 0
  │  pkt 1 ─────────────────────────────────►  │ deliver, ACK 1
  │  pkt 2 ────────── X (LOST) ─────────────  │
  │  pkt 3 ─────────────────────────────────►  │ wrong seq! ACK 1
  │  pkt 4 ─────────────────────────────────►  │ wrong seq! ACK 1
  │  ◄──────────────────────── ACK 0           │
  │  ◄──────────────────────── ACK 1           │
  │  ◄──────────────────────── ACK 1 (dup)     │
  │  ◄──────────────────────── ACK 1 (dup)     │
  │                                             │
  │  TIMEOUT (for pkt 2)                        │
  │  retransmit pkt 2, 3, 4 ──────────────►   │
  │                                             │
```

## Cumulative ACK Explained

When the receiver sends **ACK n**, it means:
> "I have successfully received all packets with sequence numbers 0, 1, 2, ..., n."

This is more robust than individual ACKs because if ACK 3 arrives but ACK 2 was lost, the sender still knows packets 0–3 are all received.

## Performance

GBN improves utilization over stop-and-wait by filling the pipeline:

$$
U_{sender} = \frac{N \cdot L/R}{RTT + L/R}
$$

With N = 4 and the same parameters as before:
$$
U_{sender} = \frac{4 \times 0.008\text{ms}}{30.008\text{ms}} \approx 0.00107
$$

A 4× improvement over stop-and-wait. Larger N → higher utilization.

## GBN vs. Selective Repeat

| Feature | Go-Back-N | Selective Repeat |
| :--- | :--- | :--- |
| Receiver buffering | No (discard OOO) | Yes (buffer OOO) |
| ACK type | Cumulative | Individual |
| Retransmission | All from base | Only lost packet |
| Complexity | Simpler | More complex |
| Efficiency | Wastes bandwidth on retransmit | More efficient |

## Implementation Tips

```python
def gbn_sender(channel_data, channel_ack, messages, N=4):
    base = 0
    next_seq = 0
    packets = [make_packet(i, m.encode()) for i, m in enumerate(messages)]
    total = len(packets)
    timer_start = None

    while base < total:
        # Send packets within window
        while next_seq < min(base + N, total):
            channel_data.send(packets[next_seq])
            if base == next_seq:
                timer_start = time.time()
            next_seq += 1

        # Check for ACKs
        if channel_ack.has_packet():
            ack = channel_ack.receive()
            if not is_corrupt(ack):
                _, ack_seq, _ = parse_packet(ack)
                base = ack_seq + 1
                timer_start = time.time() if base < next_seq else None

        # Check for timeout
        if timer_start and (time.time() - timer_start > TIMEOUT):
            # Retransmit all from base
            for i in range(base, next_seq):
                channel_data.send(packets[i])
            timer_start = time.time()
```
