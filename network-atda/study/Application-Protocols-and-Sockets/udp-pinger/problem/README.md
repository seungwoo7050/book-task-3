# UDP Pinger — Problem Specification

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Objective

Implement a UDP ping client that sends 10 ping messages to a UDP ping server, measures the round-trip time for each reply, and computes summary statistics. The server simulates an unreliable channel by randomly dropping ~30% of packets.

## Requirements

### Functional Requirements

1. **Ping Messages**
   - Send exactly **10** UDP ping messages to the server
   - Each message must include a sequence number (1–10) and a timestamp
   - Message format: `Ping <sequence_number> <timestamp>`

2. **RTT Measurement**
   - Record the send time before each ping
   - Compute RTT = (reply received time) − (send time) for each response

3. **Timeout Handling**
   - Set a **1-second** socket timeout for each ping
   - If no reply is received within 1 second, print `Request timed out`

4. **Statistics Output**
   - After all 10 pings, print:
     - RTT for each received reply
     - Minimum RTT
     - Maximum RTT
     - Average RTT
     - Packet loss percentage

### Expected Output Format

```
Ping  1: Reply from 127.0.0.1  RTT = 0.324 ms
Ping  2: Request timed out
Ping  3: Reply from 127.0.0.1  RTT = 0.512 ms
...
Ping 10: Reply from 127.0.0.1  RTT = 0.289 ms

--- Ping Statistics ---
10 packets sent, 7 received, 30.0% loss
RTT min/avg/max = 0.289/0.415/0.612 ms
```

## Constraints

- Python 3 standard library only
- Primary module: `socket`
- Do **not** modify the provided server code
- The client must work with the provided server without any protocol changes

## Input / Environment

- Server code is provided in `code/udp_pinger_server.py`
- Client skeleton is in `code/udp_pinger_client_skeleton.py`
- Test script is in `script/test_pinger.sh`

## Evaluation Criteria

| Criterion | Description |
| :--- | :--- |
| **Correct Ping Sending** | Client sends 10 properly formatted UDP messages |
| **RTT Calculation** | RTT is accurately measured for each received reply |
| **Timeout Handling** | Lost packets are detected and reported after 1 second |
| **Statistics** | Correct min/avg/max RTT and packet loss percentage |
| **Code Quality** | Clean, well-commented Python code |
