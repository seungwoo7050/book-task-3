# TCP & UDP Lab — Problem Specification

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Objective

Analyze pre-captured packet traces to understand TCP segment structure, connection management, reliable data transfer, flow control, and congestion control. Also examine UDP's lightweight datagram service for comparison.

## Trace Files

The following trace files are provided in `data/`:

| File | Scenario | Description |
| :--- | :--- | :--- |
| `tcp-upload.pcapng` | TCP File Upload | A file uploaded to a server via HTTP POST over TCP |
| `udp-dns.pcapng` | UDP DNS Traffic | DNS queries and responses over UDP |

## Instructions

Open each trace file in Wireshark and apply the appropriate display filter. Then answer the following questions.

---

## Part 1: TCP Segment Structure

**Trace file**: `tcp-upload.pcapng`

1. What is the IP address and TCP port number used by the **client** (source)? What is the IP address and port used by the **server** (destination)?
2. What is the **sequence number** of the TCP SYN segment that initiates the connection? What field in the segment identifies it as a SYN segment?
3. What is the **sequence number** of the SYN-ACK segment sent by the server? What is the **acknowledgment number**? How did the server determine this acknowledgment value? What flags identify this as a SYN-ACK?
4. What is the **sequence number** of the TCP segment containing the HTTP POST command? What is its **acknowledgment number**?
5. Consider the first six TCP data segments sent by the client. For each, report the **sequence number**, **number of bytes of payload**, and the **time sent**. What is the acknowledgment number for each?

---

## Part 2: TCP Connection Management

6. What is the minimum amount of available buffer space advertised by the **receiver** (server) during the entire trace? Does the receiver ever throttle the sender (i.e., does the receive window ever reach zero)?
7. Are there any **retransmitted segments** in the trace? How can you identify them? (Hint: look for duplicate sequence numbers or Wireshark's `[TCP Retransmission]` labels.)
8. How much data (in bytes) did the client transfer to the server? How can you calculate this from the sequence numbers?
9. Describe the **TCP connection teardown**. Which side initiates the close? What are the FIN and ACK sequence numbers?

---

## Part 3: TCP Throughput and Round-Trip Time

10. What is the **throughput** (bytes per second) of the TCP connection? Calculate it from the total data transferred and the time duration between the first data segment and the last ACK.
11. Use Wireshark's **TCP Stream Graphs** (Statistics → TCP Stream Graphs) to plot the **Time-Sequence (Stevens)** graph. Describe the pattern: is the sending rate roughly constant, or does it change?
12. Examine the **round-trip time (RTT)** values using Wireshark's TCP stream graph or by calculating `time(ACK) - time(segment)` for individual segments. What is the approximate RTT? Does it vary significantly?

---

## Part 4: TCP Congestion Control

13. Use the **Time-Sequence (Stevens)** graph or the **Window Scaling** graph to identify phases of **slow start** and **congestion avoidance**. At what segment/time does the transition from slow start to congestion avoidance occur?
14. What is the initial value of the **congestion window** (estimated from the number of segments sent before the first ACK)? How does it grow during slow start?

---

## Part 5: UDP

**Trace file**: `udp-dns.pcapng`

15. Select a UDP packet. How many **header fields** are in the UDP header? Name each field.
16. What is the **length** (in bytes) of each UDP header field?
17. The **Length** field in the UDP header specifies what? Verify with an actual UDP packet.
18. What is the maximum number of bytes that can be included in a UDP payload? (Hint: consider the maximum value of the Length field.)
19. What is the largest possible source port number?
20. What is the protocol number for UDP in the IP header? What about TCP?
21. Examine a pair of UDP packets (DNS query and response). What is the relationship between the **port numbers** in the two packets?

---

## Evaluation Criteria

| Criterion | Description |
| :--- | :--- |
| **Accuracy** | Correct sequence numbers, port numbers, and calculations |
| **Completeness** | Every question answered with supporting evidence |
| **Understanding** | Explanations demonstrate comprehension of TCP/UDP mechanics |
| **Calculations** | Throughput and RTT calculations are correct with shown work |
