# IP & ICMP Lab — Problem Specification

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Objective

Analyze pre-captured packet traces to understand IPv4 header structure, IP fragmentation, TTL behavior, and ICMP message types. You will examine `traceroute` output and `ping` exchanges.

## Trace Files

The following trace files are provided in `data/`:

| File | Scenario | Description |
| :--- | :--- | :--- |
| `ip-traceroute.pcapng` | Traceroute | ICMP packets from a traceroute to a remote host |
| `ip-fragmentation.pcapng` | Fragmentation | Large ICMP packets that trigger IP fragmentation |

## Instructions

Open each trace file in Wireshark and apply appropriate display filters. Then answer the following questions.

---

## Part 1: IPv4 Header

**Trace file**: `ip-traceroute.pcapng`

1. Select the first ICMP Echo Request sent by your computer. What is the **IP version**? What is the **header length** (in bytes)? What is the **total length** of the IP datagram?
2. What is the **Identification** field value? What are the **Flags** and **Fragment Offset** values? What do these values indicate about fragmentation?
3. What is the **TTL** (Time to Live) value? What is the **Protocol** field value? What protocol is encapsulated in this IP datagram?
4. What are the **source** and **destination** IP addresses?
5. Examine the ICMP Echo Requests sent with increasing TTL values (as used by traceroute). How does the **TTL** field change across successive packets? Do the **Identification** values change?
6. Find the first ICMP **Time Exceeded** message returned by a router. What are the source IP, TTL, and ICMP type/code fields?
7. Are the Identification field values in the Echo Request datagrams the same or different for successive requests? Why?
8. Sort the trace by source IP. How many distinct IP addresses appear as sources of ICMP Time Exceeded messages? These represent the routers along the path.

---

## Part 2: IP Fragmentation

**Trace file**: `ip-fragmentation.pcapng`

9. Find the first ICMP Echo Request that was fragmented. What is the **Identification** field? What are the **Flags** and **Fragment Offset** for each fragment?
10. How many fragments were created from this single IP datagram? How can you identify they belong to the same original datagram?
11. What fields in the IP header change between fragments? What fields stay the same?
12. Verify the fragmentation: For each fragment, what is the **Total Length**? What is the **Fragment Offset** × 8? Do the offsets plus lengths account for the entire original datagram?
13. What is the **More Fragments (MF)** flag value in each fragment? Which fragment has MF = 0?
14. How does IP reassembly work? Which host performs the reassembly — a router or the destination host? How does Wireshark display the reassembled datagram?

---

## Part 3: ICMP Messages

15. What is the ICMP **Type** and **Code** for an Echo Request? For an Echo Reply?
16. What is the ICMP **Type** and **Code** for a Time Exceeded message? What does this message signify?
17. Do ICMP Echo Request and Reply messages share the same **Identifier** and **Sequence Number** fields? What is the purpose of these fields?
18. How many bytes of data are in the ICMP payload of an Echo Request? How does this compare to the Total Length of the enclosing IP datagram?

---

## Evaluation Criteria

| Criterion | Description |
| :--- | :--- |
| **Accuracy** | Correct IP header values, ICMP types, fragment offsets |
| **Completeness** | Every question answered with supporting evidence |
| **Understanding** | Explanations demonstrate comprehension of IP/ICMP mechanics |
| **Fragmentation Analysis** | Correct identification and verification of fragment relationships |
