# RDT Protocol — Problem Specification

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Objective

Implement reliable data transfer protocols that deliver data correctly over an unreliable channel. You will implement two protocols:

1. **RDT 3.0** — Stop-and-Wait with alternating-bit sequence numbers
2. **GBN** — Go-Back-N with a sliding window and cumulative ACKs

## Requirements

### Part 1: RDT 3.0 (Stop-and-Wait)

**Sender:**
1. Accept data from the application layer
2. Create a packet with: checksum, sequence number (0 or 1), and payload
3. Send the packet and start a timer
4. Wait for an ACK:
   - Correct ACK received → advance sequence number, send next packet
   - Timeout → retransmit the current packet
   - Corrupt/wrong ACK → ignore, wait for timeout

**Receiver:**
1. Receive a packet
2. Verify the checksum
3. If the packet has the expected sequence number and is not corrupt:
   - Deliver the payload to the application layer
   - Send an ACK with the received sequence number
4. If corrupt or duplicate:
   - Re-send the previous ACK

### Part 2: Go-Back-N (GBN)

**Sender:**
1. Maintain a window of size N
2. Send packets within the window without waiting for individual ACKs
3. On receiving a cumulative ACK for sequence number `n`:
   - Slide the window past `n`
   - Reset the timer if there are still unacknowledged packets
4. On timeout:
   - Retransmit ALL packets in the current window

**Receiver:**
1. Maintain the expected sequence number
2. If a packet with the expected sequence number arrives (and is not corrupt):
   - Deliver to application, send ACK, increment expected
3. Otherwise:
   - Discard the packet, re-send ACK for the last correctly received packet

### Packet Format

```
+------------------+------------------+------------------+
|   Checksum (4B)  |  Seq Number (4B) |  Payload (var)   |
+------------------+------------------+------------------+
```

- **Checksum**: MD5 hash of (seq_number + payload), truncated to 4 bytes
- **Sequence Number**: 4-byte integer (big-endian)
- **Payload**: Variable-length data

### Expected Output

```
[SENDER] Sending packet seq=0: "Hello"
[CHANNEL] Packet seq=0 delivered
[RECEIVER] Received packet seq=0: "Hello" → ACK 0
[SENDER] ACK 0 received. Sending packet seq=1: "World"
[CHANNEL] Packet seq=1 LOST (simulated)
[SENDER] Timeout! Retransmitting packet seq=1
...
[SENDER] All data transferred successfully.
```

## Constraints

- Python 3 standard library only
- Do **not** modify the channel simulator
- Checksums must detect corruption introduced by the simulator
- Timer values should be configurable

## Input / Environment

- Channel simulator: `code/channel.py`
- Packet utilities: `code/packet.py`
- RDT 3.0 skeleton: `code/rdt3_skeleton.py`
- GBN skeleton: `code/gbn_skeleton.py`
- Test data: `data/test_messages.txt`
- Test script: `script/test_rdt.sh`

## Evaluation Criteria

| Criterion | Description |
| :--- | :--- |
| **Correct Delivery** | All data arrives at the receiver in order, without corruption |
| **Loss Handling** | Lost packets are detected and retransmitted |
| **Corruption Handling** | Corrupt packets are detected via checksum and discarded |
| **Duplicate Handling** | Duplicate packets are detected and not re-delivered |
| **GBN Window** | Sender correctly manages the sliding window |
| **Code Quality** | Clean, well-documented code |
