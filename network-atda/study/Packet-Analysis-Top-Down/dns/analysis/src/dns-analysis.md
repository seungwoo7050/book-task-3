# DNS Lab — Analysis Answers

## Trace Limitations

- This report uses only the repository-provided trace files.
- If a worksheet item needs packets that are not present in these traces, the answer is marked as `Not observable in this provided trace`.
- Missing values are not guessed; only decoded packet evidence is used.
- Numeric claims are tied to explicit frame references.

This answer set is based strictly on the provided traces:
- `dns-nslookup.pcapng` (4 packets)
- `dns-web-browsing.pcapng` (2 packets)

Some questions in the original worksheet assume richer captures (NS delegation chain, repeated cached lookups, TCP follow-up). For those, this document marks the item as **not observable in the provided trace**.

## Part 1: nslookup

**Trace file**: `dns-nslookup.pcapng`

### Question 1

**Q: What transport-layer protocol is used by DNS? What port number does the DNS server listen on?**

**A:** DNS is carried over **UDP** in this trace, and the DNS server listens on **UDP port 53**.

**Evidence:**
- Query frame **#1**: `udp.srcport=53000`, `udp.dstport=53`
- Query frame **#3**: `udp.srcport=53001`, `udp.dstport=53`

---

### Question 2

**Q: To what IP address is the DNS query sent? Is this the IP of your default local DNS server?**

**A:** The DNS queries are sent to **8.8.8.8**.

**Evidence:**
- Frame **#1** (`example.com A`): `ip.dst=8.8.8.8`
- Frame **#3** (`example.com MX`): `ip.dst=8.8.8.8`

Whether this is the system's default resolver cannot be proven from the pcap alone; this trace only shows traffic to `8.8.8.8`.

---

### Question 3

**Q: What is the type of the DNS query? Does the query contain any answers?**

**A:**
- Frame **#1** query type: **A (1)**, `Answer RRs: 0`
- Frame **#3** query type: **MX (15)**, `Answer RRs: 0`

**Evidence:** DNS `Queries` section and header `Answer RRs` fields in frames #1 and #3.

---

### Question 4

**Q: Examine the DNS response. How many answers are provided? What does each answer contain?**

**A:**
- Frame **#2** (response to A query): `Answer RRs: 1`, answer is `example.com A 93.184.216.34 TTL 300`
- Frame **#4** (response to MX query): `Answer RRs: 1`, record type is MX with `TTL 300`

**Evidence:** DNS `Answers` section in frames #2 and #4.

---

### Question 5

**Q: What is the canonical name (CNAME) for the queried host, if any? What IP addresses are returned?**

**A:** In `dns-nslookup.pcapng` there is **no CNAME** for `example.com`; the A response is direct.

**Evidence:** Frame **#2** answer is `Type: A`, value `93.184.216.34`, with no `Type: CNAME` record.

---

### Question 6

**Q: What mail server names and preference values are returned for an MX query?**

**A:** The trace contains an MX response (frame **#4**) but Wireshark marks it as **Malformed Packet: DNS** before decoding MX preference/exchange fields. So exact mail host and preference are **not recoverable via dissector output** in this capture.

**Evidence:** Frame **#4**:
- `Type: MX (15)` present
- `Data length: 19`
- followed by `[Malformed Packet: DNS]`

---

## Part 2: Authoritative and Non-Authoritative

### Question 7

**Q: To what IP address is the DNS query sent? Is this the default local DNS server?**

**A:** The observed DNS queries are sent to **8.8.8.8** (frames #1 and #3).

**Evidence:** `ip.dst=8.8.8.8` in query frames.

---

### Question 8

**Q: What type is the DNS query? Does it contain any answers?**

**A:** Observed query types are **A** (frame #1) and **MX** (frame #3). Both query packets have **`Answer RRs: 0`**.

---

### Question 9

**Q: What are the authoritative nameservers? Difference between authoritative and non-authoritative answers?**

**A:**
- This trace does **not** include an NS lookup response listing authoritative nameserver hostnames.
- It does include both flag types:
  - Frame **#2**: `Authoritative: 1` (authoritative answer)
  - Frame **#4**: `Authoritative: 0` (non-authoritative answer)

**Meaning:** authoritative means the responder is authoritative for the zone; non-authoritative means resolver/cached response.

---

### Question 10

**Q: Does the response contain IP addresses of the authoritative nameservers?**

**A:** **Not in this trace.** Additional records are empty.

**Evidence:** `Additional RRs: 0` in frames #2 and #4.

---

## Part 3: DNS and Web Browsing

**Trace file**: `dns-web-browsing.pcapng`

### Question 11

**Q: What is the destination IP of the first DNS query when browsing to www.ietf.org?**

**A:** The first query goes to **1.1.1.1**.

**Evidence:** Frame **#1** has `dns.qry.name=www.ietf.org`, `ip.dst=1.1.1.1`, `udp.dstport=53`.

---

### Question 12

**Q: What type is the DNS query? Does it contain answers?**

**A:** Query type is **A (1)** and it contains no answers.

**Evidence:** Frame **#1**:
- Query type A
- DNS header `Answer RRs: 0`

---

### Question 13

**Q: How many answers are in the DNS response? List each answer's type, value, and TTL.**

**A:** Wireshark decodes **1 answer**:
- `www.ietf.org` → `CNAME ietf.map.fastly.net`, TTL **200**

**Evidence:** Frame **#2** DNS `Answers` section (`Answer RRs: 1`, `Type: CNAME`, TTL 200).

**Note:** Frame #2 also contains `Extraneous Data` bytes after the decoded answer. That looks like an additional resource record payload, but it is not decoded as a formal DNS answer in this trace.

---

### Question 14

**Q: Does the subsequent TCP SYN destination IP match one of the DNS response addresses?**

**A:** **Not observable.** This trace contains only 2 DNS packets and **no TCP packets**.

**Evidence:** `tcp` filter returns zero packets for `dns-web-browsing.pcapng`.

---

### Question 15

**Q: Has the TTL changed in a subsequent cached response? What does this indicate?**

**A:** **Not observable in this trace** because there is only one DNS response for `www.ietf.org`.

**Evidence:** `dns-web-browsing.pcapng` has exactly 2 packets (1 query, 1 response).

---

### Question 16

**Q: How many different DNS queries and responses were generated by a single page load? What types of records were queried?**

**A:** In this capture, a single page-load sequence shows:
- **1 DNS query** (frame #1): type **A** for `www.ietf.org`
- **1 DNS response** (frame #2): decoded CNAME answer

So the observed query type set is just **A** in this trace.

**Evidence:** Unique query list from `dns.flags.response==0` has one entry: `www.ietf.org` type 1.
