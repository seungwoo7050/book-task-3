# Round-Trip Time (RTT) Measurement

## What is RTT?

**Round-Trip Time (RTT)** is the time elapsed between sending a request and receiving the corresponding response. It is a fundamental metric for measuring network latency.

$$
RTT = T_{reply\_received} - T_{request\_sent}
$$

## Measuring RTT in Python

Python's `time` module provides high-resolution timestamps:

```python
import time

send_time = time.time()        # Record time before sending
# ... send packet and wait for reply ...
recv_time = time.time()        # Record time after receiving

rtt = recv_time - send_time    # RTT in seconds
rtt_ms = rtt * 1000            # Convert to milliseconds
```

### `time.time()` vs. `time.perf_counter()`

| Function | Resolution | Use Case |
| :--- | :--- | :--- |
| `time.time()` | ~1 μs | Wall-clock time (includes date) |
| `time.perf_counter()` | ~100 ns | High-precision interval timing |

Both work well for RTT measurement. `time.time()` is used in the standard Kurose & Ross assignments.

## Computing Statistics

After collecting RTT values for all successful pings, compute:

```python
rtt_list = [0.324, 0.512, 0.289, 0.415, 0.367, 0.498, 0.301]

min_rtt = min(rtt_list)
max_rtt = max(rtt_list)
avg_rtt = sum(rtt_list) / len(rtt_list)
```

## Packet Loss

Since UDP does not guarantee delivery, some pings will receive no reply. The **packet loss rate** is:

$$
\text{Loss \%} = \frac{\text{packets sent} - \text{replies received}}{\text{packets sent}} \times 100
$$

```python
sent = 10
received = len(rtt_list)  # e.g., 7
loss_pct = ((sent - received) / sent) * 100  # 30.0%
```

## Formatting Output

A typical ping statistics summary:

```
--- Ping Statistics ---
10 packets sent, 7 received, 30.0% loss
RTT min/avg/max = 0.289/0.415/0.612 ms
```

```python
print(f"\n--- Ping Statistics ---")
print(f"{sent} packets sent, {received} received, {loss_pct:.1f}% loss")
if rtt_list:
    print(f"RTT min/avg/max = {min_rtt:.3f}/{avg_rtt:.3f}/{max_rtt:.3f} ms")
else:
    print("No replies received — 100% loss")
```

## Why Ping Uses UDP (Conceptually)

The standard ICMP ping actually operates at the network layer, not the transport layer. However, this assignment uses UDP to demonstrate:

- **Unreliable delivery**: packets can be lost (simulated by the server)
- **Timeout handling**: the client must decide when to give up waiting
- **Stateless protocol**: each ping is independent — no connection setup needed

These are the same challenges that arise in real unreliable networks.
