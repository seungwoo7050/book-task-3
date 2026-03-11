# Wireshark Transport Layer Analysis Techniques

## Display Filters for TCP

| Filter | Description |
| :--- | :--- |
| `tcp` | All TCP traffic |
| `tcp.port == 80` | TCP traffic on port 80 |
| `tcp.flags.syn == 1` | SYN segments (connection setup) |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | SYN only (first step of handshake) |
| `tcp.flags.syn == 1 && tcp.flags.ack == 1` | SYN-ACK (second step) |
| `tcp.flags.fin == 1` | FIN segments (connection teardown) |
| `tcp.flags.reset == 1` | RST segments (connection abort) |
| `tcp.len > 0` | TCP segments with payload data |
| `tcp.analysis.retransmission` | Retransmitted segments |
| `tcp.analysis.duplicate_ack` | Duplicate ACKs |
| `tcp.analysis.zero_window` | Zero window advertisements |
| `tcp.window_size == 0` | Zero window segments |
| `tcp.stream == 0` | All packets in TCP stream 0 |

## Display Filters for UDP

| Filter | Description |
| :--- | :--- |
| `udp` | All UDP traffic |
| `udp.port == 53` | UDP traffic on port 53 (DNS) |
| `udp.length > 100` | UDP datagrams larger than 100 bytes |
| `udp.srcport >= 49152` | UDP from ephemeral ports |

## TCP Stream Analysis

### Follow TCP Stream

1. Select any TCP packet in the stream
2. Right-click → **Follow → TCP Stream**
3. A dialog shows the complete conversation:
   - **Red text**: Data sent by the client
   - **Blue text**: Data sent by the server

### TCP Stream Graphs

Navigate to **Statistics → TCP Stream Graphs** with a TCP packet selected:

| Graph | Purpose |
| :--- | :--- |
| **Time-Sequence (Stevens)** | Plots sequence numbers vs time. The slope represents throughput. Useful for identifying slow start and congestion avoidance. |
| **Time-Sequence (tcptrace)** | Enhanced plot showing sequence numbers, ACKs, and receive window. Forward and reverse data visible. |
| **Throughput** | Bytes per second over time. Shows bandwidth utilization. |
| **Round-Trip Time** | RTT measurements based on segment-ACK pairs. |
| **Window Scaling** | Advertised receive window size over time. Useful for identifying flow control throttling. |

## Calculating Throughput

$$\text{Throughput} = \frac{\text{Total Data (bytes)}}{\text{Time Duration (seconds)}}$$

To compute from Wireshark:
1. Total data = Final sequence number − Initial sequence number (after SYN)
2. Time = Timestamp of last data ACK − Timestamp of first data segment
3. Or use Statistics → Conversations → TCP for automatic calculation

## Calculating RTT

For a specific segment:

$$\text{RTT} = T_{\text{ACK received}} - T_{\text{segment sent}}$$

Wireshark computes this automatically: expand **[SEQ/ACK analysis]** in the TCP layer.

## Identifying the 3-Way Handshake

Apply the filter:

```
tcp.flags.syn == 1 || (tcp.seq == 1 && tcp.ack == 1 && tcp.len == 0)
```

Or look for the first three packets in a TCP stream:

| Packet | Flags | Seq | Ack |
| :--- | :--- | :--- | :--- |
| 1 (SYN) | `SYN` | x | 0 |
| 2 (SYN-ACK) | `SYN, ACK` | y | x+1 |
| 3 (ACK) | `ACK` | x+1 | y+1 |

## Identifying Retransmissions

Wireshark automatically labels:
- `[TCP Retransmission]` — A segment with the same sequence number as a previously sent segment
- `[TCP Fast Retransmission]` — Retransmission triggered by 3 duplicate ACKs
- `[TCP Dup ACK #N]` — Duplicate acknowledgment (same ack number repeated)

Filter: `tcp.analysis.retransmission || tcp.analysis.duplicate_ack`

## Tips

1. **Relative sequence numbers**: Wireshark shows relative sequence numbers by default (starting from 0). To see absolute numbers: Edit → Preferences → Protocols → TCP → uncheck "Relative sequence numbers."
2. **Window scaling**: Modern TCP uses window scaling. The actual window = window field × scale factor. Wireshark shows the scaled value in the [Calculated window size] field.
3. **Stream index**: Each TCP connection gets a unique Stream index. Use `tcp.stream == N` to isolate a single connection.
4. **Export data**: Use File → Export Objects → HTTP to extract transferred files from the capture.
