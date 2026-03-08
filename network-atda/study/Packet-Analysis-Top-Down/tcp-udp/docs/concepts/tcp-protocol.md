# TCP Protocol Reference

## Overview

The Transmission Control Protocol (TCP) provides **reliable, ordered, connection-oriented** byte-stream delivery over an unreliable network (IP). TCP is defined in RFC 793 and enhanced by many subsequent RFCs.

## TCP Segment Structure

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |U|A|P|R|S|F|                               |
| Offset| Reserved  |R|C|S|S|Y|I|            Window             |
|       |           |G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (variable)                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Header Fields

| Field | Size | Description |
| :--- | :--- | :--- |
| **Source Port** | 16 bits | Sending application's port number |
| **Destination Port** | 16 bits | Receiving application's port number |
| **Sequence Number** | 32 bits | Byte offset of the first data byte in this segment |
| **Acknowledgment Number** | 32 bits | Next byte expected from the other side (if ACK flag set) |
| **Data Offset** | 4 bits | Header length in 32-bit words (minimum 5 = 20 bytes) |
| **Flags** | 6 bits | URG, ACK, PSH, RST, SYN, FIN |
| **Window** | 16 bits | Receive window size (flow control) |
| **Checksum** | 16 bits | Error detection over header + data + pseudo-header |
| **Urgent Pointer** | 16 bits | Offset of urgent data (if URG flag set) |
| **Options** | Variable | MSS, Window Scale, Timestamps, SACK, etc. |

## TCP Flags

| Flag | Bit | Purpose |
| :--- | :--- | :--- |
| **SYN** | S | Synchronize sequence numbers (connection setup) |
| **ACK** | A | Acknowledgment field is valid |
| **FIN** | F | Sender has finished sending data (connection teardown) |
| **RST** | R | Reset the connection (abort) |
| **PSH** | P | Push data to the application immediately |
| **URG** | U | Urgent pointer field is valid |

## TCP Connection Lifecycle

### 3-Way Handshake (Connection Establishment)

```
Client                              Server
  |                                    |
  |--- SYN (seq=x) ------------------>|  Step 1: Client sends SYN
  |                                    |
  |<-- SYN-ACK (seq=y, ack=x+1) -----|  Step 2: Server sends SYN-ACK
  |                                    |
  |--- ACK (seq=x+1, ack=y+1) ------->|  Step 3: Client sends ACK
  |                                    |
  |========= DATA TRANSFER ===========|
```

- **SYN**: `SYN=1, ACK=0`, `seq = ISN_client` (Initial Sequence Number)
- **SYN-ACK**: `SYN=1, ACK=1`, `seq = ISN_server`, `ack = ISN_client + 1`
- **ACK**: `SYN=0, ACK=1`, `seq = ISN_client + 1`, `ack = ISN_server + 1`

### Connection Teardown (4-Way Close)

```
Client                              Server
  |                                    |
  |--- FIN (seq=u) ------------------>|  Step 1: Client sends FIN
  |                                    |
  |<-- ACK (ack=u+1) ----------------|  Step 2: Server ACKs the FIN
  |                                    |
  |<-- FIN (seq=v) ------------------|  Step 3: Server sends its FIN
  |                                    |
  |--- ACK (ack=v+1) ---------------->|  Step 4: Client ACKs
  |                                    |
```

## Sequence and Acknowledgment Numbers

TCP numbers every byte of data sent:

- **Sequence Number**: The byte number of the first byte in this segment's payload
- **Acknowledgment Number**: The byte number the receiver expects next (cumulative ACK)

### Example

```
Segment 1: seq=1000, payload=500 bytes → carries bytes 1000–1499
Segment 2: seq=1500, payload=500 bytes → carries bytes 1500–1999
ACK:        ack=2000 → "I've received all bytes up to 1999, send byte 2000 next"
```

## TCP Options

| Option | Purpose | Typical Value |
| :--- | :--- | :--- |
| **MSS** | Maximum Segment Size | 1460 bytes (Ethernet) |
| **Window Scale** | Multiply window field by $2^{n}$ | Shift count 0–14 |
| **SACK Permitted** | Selective ACK support | (no value, just presence) |
| **Timestamps** | RTT measurement, PAWS | TSval, TSecr |

MSS is negotiated during the handshake. If the MSS is 1460 and the sending application writes 10,000 bytes, TCP will segment the data into multiple segments of up to 1460 bytes each.

## Retransmission

TCP detects lost segments and retransmits them:

1. **Timeout-based**: If no ACK arrives within the Retransmission Timeout (RTO), retransmit
2. **Fast Retransmit**: If 3 duplicate ACKs are received, retransmit without waiting for timeout

In Wireshark, retransmissions are labeled as `[TCP Retransmission]` and duplicate ACKs as `[TCP Dup ACK]`.
