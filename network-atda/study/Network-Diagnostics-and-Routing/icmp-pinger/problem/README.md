# ICMP Pinger — Problem Specification

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Objective

Implement a ping utility that sends ICMP Echo Request packets and processes ICMP Echo Reply packets using raw sockets. The program should behave similarly to the standard `ping` command.

## Requirements

### Functional Requirements

1. **ICMP Packet Construction**
   - Build ICMP Echo Request packets with:
     - Type: `8` (Echo Request)
     - Code: `0`
     - Checksum: Computed using the Internet checksum algorithm
     - Identifier: Process ID (or a chosen constant)
     - Sequence Number: Incrementing from 1
     - Payload: Timestamp data for RTT calculation

2. **Raw Socket Usage**
   - Create a raw socket: `socket.socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)`
   - Send crafted ICMP packets via `sendto()`
   - Receive ICMP replies via `recvfrom()` (must parse past the IP header)

3. **Reply Processing**
   - Extract the ICMP reply from the received data (skip IP header, typically 20 bytes)
   - Verify the ICMP type is `0` (Echo Reply) and the identifier matches
   - Calculate RTT from the embedded timestamp

4. **Statistics**
   - After all pings, print:
     - Number of packets sent and received
     - Packet loss percentage
     - Minimum, maximum, and average RTT

### Expected Output

```
PING google.com (142.250.80.46): 64 bytes

64 bytes from 142.250.80.46: icmp_seq=1  RTT=12.345 ms
64 bytes from 142.250.80.46: icmp_seq=2  RTT=11.234 ms
64 bytes from 142.250.80.46: icmp_seq=3  RTT=13.456 ms
64 bytes from 142.250.80.46: icmp_seq=4  RTT=12.789 ms

--- google.com ping statistics ---
4 packets sent, 4 received, 0.0% loss
RTT min/avg/max = 11.234/12.456/13.456 ms
```

## Constraints

- Python 3 standard library only
- Must use raw ICMP sockets (not UDP)
- Must implement the Internet checksum manually
- Requires root/administrator privileges to run

## Input / Environment

- Skeleton code: `code/icmp_pinger_skeleton.py`
- Test script: `script/test_icmp.sh`
- Run with: `sudo python3 icmp_pinger_skeleton.py <target_host>`

## Evaluation Criteria

| Criterion | Description |
| :--- | :--- |
| **Packet Construction** | ICMP Echo Request is correctly formatted |
| **Checksum** | Internet checksum is correctly computed |
| **Reply Parsing** | Echo Reply is correctly extracted and verified |
| **RTT Measurement** | RTT is accurately calculated for each ping |
| **Statistics** | Correct min/avg/max RTT and packet loss |
| **Code Quality** | Clean, well-documented code |
