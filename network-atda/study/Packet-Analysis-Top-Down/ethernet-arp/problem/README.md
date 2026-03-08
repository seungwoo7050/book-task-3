# Ethernet & ARP Lab — Problem Specification

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Objective

Analyze pre-captured packet traces to understand Ethernet frame structure, MAC addressing, and the ARP protocol. You will examine how devices on a LAN resolve IP addresses to MAC addresses.

## Trace Files

The following trace files are provided in `data/`:

| File | Scenario | Description |
| :--- | :--- | :--- |
| `ethernet-arp.pcapng` | ARP and Ethernet | ARP request/reply exchanges and Ethernet framing on a LAN |

## Instructions

Open the trace file in Wireshark. Use display filters `arp` and `eth` as needed. Then answer the following questions.

---

## Part 1: Ethernet Frame Structure

1. What is the **48-bit Ethernet (MAC) destination address** in the frame containing the ARP request? Is this a unicast or broadcast address?
2. What is the **48-bit Ethernet source address** in the same frame? What device does this MAC belong to (your computer, router, etc.)?
3. What is the **EtherType** field value? What upper-layer protocol does this indicate?
4. How many bytes from the very start of the Ethernet frame does the ASCII "G" in "GET" appear (for an HTTP packet)? Count the Ethernet header bytes preceding the IP and TCP headers.
5. What is the value of the **Ethernet destination address** in the frame containing the ARP reply? Is this a broadcast or unicast address?
6. What is the **EtherType** field in a frame carrying an IP datagram? How does it differ from the EtherType in an ARP frame?

---

## Part 2: ARP Protocol

7. What are the **hexadecimal values** of the source and destination MAC addresses in the Ethernet frame containing the ARP request?
8. What is the **opcode** value in the ARP request message? What does it mean?
9. Does the ARP request contain the **IP address of the sender**? If so, what is it?
10. What **IP address** is being queried (the target IP) in the ARP request?
11. What is the **target MAC address** field in the ARP request? Why is it this value?
12. Now examine the ARP **reply**. What is the opcode value? What is the sender MAC address in the reply (the answer to the ARP query)?
13. Looking at the ARP reply, what is the **destination MAC address** in the Ethernet frame? How was this address determined?
14. After the ARP exchange, verify that the next IP packet to the resolved address uses the correct MAC address from the ARP reply.

---

## Part 3: ARP Cache

15. Before running the trace, what command can display the **ARP cache** on your operating system? What information does each entry contain?
16. What is the typical **timeout** for ARP cache entries? What happens when an entry expires?
17. If you clear the ARP cache and immediately access a host on the local network, what traffic do you observe in Wireshark?

---

## Evaluation Criteria

| Criterion | Description |
| :--- | :--- |
| **Accuracy** | Correct MAC addresses, EtherType values, and ARP opcodes |
| **Completeness** | Every question answered with supporting evidence |
| **Understanding** | Explanations demonstrate comprehension of Ethernet/ARP mechanics |
| **Evidence** | Answers cite specific Wireshark fields and packet numbers |
