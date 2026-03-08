# TLS/SSL — Solution

## Trace Limitations

- This report uses only the repository-provided trace file.
- If a worksheet item needs packets that are not present in this trace, the answer is marked as `Not observable in this provided trace`.
- Missing values are not guessed; only decoded packet evidence is used.
- Numeric claims are tied to explicit frame references.

Trace used: `tls-trace.pcap` (6 frames total).

Important constraint: this is a **minimal synthetic trace**. The Certificate record is marked malformed, so several certificate-detail questions are not directly recoverable from dissector output.

## Part 1: ClientHello (Q1–Q5)

### Q1. TLS Record Content Type and Version

- ClientHello is in frame **#4**.
- Record content type: **22 (Handshake)**
- Record version: **0x0303 (TLS 1.2)**
- Handshake version in ClientHello: **0x0303 (TLS 1.2)**

**Evidence:** Frame #4 TLS record and ClientHello fields.

### Q2. Client Cipher Suites

Client advertises **2 cipher suites** in frame #4:
1. `TLS_AES_128_GCM_SHA256 (0x1301)`
2. `TLS_AES_256_GCM_SHA384 (0x1302)`

No additional suites are present in this capture.

### Q3. Server Name Indication (SNI)

SNI is **not present** in frame #4.

**Evidence:** ClientHello `Extensions Length: 0`; no `server_name` extension decoded.

### Q4. Supported TLS Versions

No `supported_versions` extension is present (extensions length 0). The only explicit version value visible is `0x0303` in record and handshake headers.

### Q5. Other Notable Extensions

No notable extensions can be listed from this trace because ClientHello extensions are empty (`Extensions Length: 0`).

---

## Part 2: ServerHello and Certificate (Q6–Q11)

### Q6. Selected Cipher Suite

Server selects **`TLS_AES_128_GCM_SHA256 (0x1301)`** in frame **#5** (ServerHello).

### Q7. Negotiated TLS Version

ServerHello in frame #5 shows version `0x0303`. No `supported_versions` extension is present, so negotiation metadata is limited to this value in the trace.

### Q8. Certificate Chain Count and Subjects

Frame #5 includes a Certificate handshake record with:
- `Certificates Length: 27`
- `Certificate Length: 24`

So the trace exposes **1 certificate blob**, but subject CN fields are not decoded due malformed packet parsing.

### Q9. Leaf Issuer and Root Inclusion

Not directly recoverable from this capture.

**Evidence:** Frame #5 is flagged `[Malformed Packet: TLS]` during certificate dissection, so issuer/chain identity fields are not decoded.

### Q10. Certificate Validity and Signature Algorithm

Not directly recoverable from this capture for the same reason (malformed/truncated certificate dissection in frame #5).

### Q11. ServerKeyExchange Presence

No explicit `ServerKeyExchange` message is decoded in the trace. Server side shows only `Server Hello` + `Certificate` in frame #5.

---

## Part 3: Handshake Completion (Q12–Q16)

### Q12. ChangeCipherSpec Messages

Observed ChangeCipherSpec count: **1**.
- Frame **#6** from client (`192.168.0.2:56000 -> 93.184.216.34:443`)

No server-side ChangeCipherSpec appears in this capture.

### Q13. Message After ChangeCipherSpec

In frame #6, ChangeCipherSpec is immediately followed by **Application Data** record:
- Content Type: 23
- Length: 32

Payload is encrypted bytes; plaintext contents are not directly visible without decryption context.

### Q14. Complete Message Sequence with Frame Numbers

Observed sequence:
1. Frame #1: TCP SYN (client -> server)
2. Frame #2: TCP SYN-ACK (server -> client)
3. Frame #3: TCP ACK (client -> server)
4. Frame #4: TLS ClientHello (client -> server)
5. Frame #5: TLS ServerHello + Certificate (server -> client, certificate marked malformed)
6. Frame #6: TLS ChangeCipherSpec + ApplicationData (client -> server)

This is a shortened flow; a full textbook handshake message set is not present.

### Q15. TCP Segments / Round Trips Before Application Data

From first ClientHello to first Application Data:
- TLS-bearing segments: **3** (`#4`, `#5`, `#6`)
- First Application Data appears in frame **#6**

Approximate elapsed time: `0.000757 - 0.000364 = 0.000393 s`.

### Q16. TLS 1.3 vs TLS 1.2 Differences in This Trace

Trace suggests a **hybrid/minimal synthetic pattern**:
- Uses TLS 1.3-style cipher suite IDs (`0x1301`, `0x1302`)
- But version fields remain `0x0303`
- Has ChangeCipherSpec record
- Lacks rich extension metadata and full TLS 1.2/1.3 canonical flow

So strict 1.2 vs 1.3 comparison is limited by trace construction.

---

## Part 4: Application Data and Record Protocol (Q17–Q20)

### Q17. Application Data Record Type and Length

Application Data is in frame **#6**:
- Content Type: **23**
- Record length: **32** bytes

### Q18. Can We Infer Application Protocol Without Decryption?

Direct plaintext application messages are not visible. However, context leaks include:
- Destination TCP port **443**
- Wireshark labels record as `Application Data Protocol: Hypertext Transfer Protocol` in this synthetic trace.

No SNI or ALPN extension is present to give hostname/protocol hints.

### Q19. Are Application Data Record Lengths Uniform or Variable? Max Size Observed?

Only one Application Data record is present, so variability cannot be evaluated.
- Maximum observed Application Data record length in this capture: **32** bytes.

### Q20. Decryption with SSLKEYLOGFILE

Not performed for this trace (no key log provided here). As captured, HTTP request/response plaintext is not shown.

If key material and a complete decryptable handshake were available, Wireshark could show decrypted HTTP messages under TLS packets.
