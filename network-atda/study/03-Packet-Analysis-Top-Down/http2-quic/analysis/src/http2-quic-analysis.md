# HTTP/2 and QUIC Lab — Analysis Answers

## Part 1: HTTP/2 Trace

**Trace file**: `http2-trace.tsv`

### Question 1

**Q: What transport carries HTTP/2 in this trace?**

**A:** HTTP/2 runs over **TCP port 443** in this dataset.

**Evidence:** Every row in `http2-trace.tsv` uses `transport = TCP:443`.

### Question 2

**Q: What signal shows that HTTP/2 was negotiated?**

**A:** The negotiated application protocol is **`h2`**.

**Evidence:** The `alpn` column is `h2` for the connection-level rows.

### Question 3

**Q: Which stream IDs carry application requests?**

**A:** The application requests appear on **stream 1** and **stream 3**.

**Evidence:** Frame **18** is `HEADERS` on stream **1** for `/feed`, and frame **19** is `HEADERS` on stream **3** for `/avatars/42.png`.

### Question 4

**Q: What evidence shows HTTP/2 multiplexing?**

**A:** The trace shows **interleaved streams**: frames **18** and **19** open streams 1 and 3, then frames **20** and **21** deliver `DATA` for those two streams without waiting for one response to fully finish first.

### Question 5

**Q: Which connection-level frame shows flow-control activity?**

**A:** Frame **22** shows a **`WINDOW_UPDATE`** on **stream 0** with `increment 32768`.

**Evidence:** `frame 22 -> stream 0 -> WINDOW_UPDATE -> increment 32768`.

### Question 6

**Q: Does HTTP/2 remove all head-of-line blocking?**

**A:** No. HTTP/2 removes **application-layer request serialization**, but it still rides on **TCP**, so TCP-level **head-of-line blocking** can still stall every stream that shares the same connection.

## Part 2: QUIC Trace

**Trace file**: `quic-trace.tsv`

### Question 7

**Q: What transport carries QUIC in this trace?**

**A:** QUIC runs over **UDP port 443** in this dataset.

**Evidence:** Every row in `quic-trace.tsv` uses `transport = UDP:443`.

### Question 8

**Q: Which packet types appear during the handshake and transition to data?**

**A:** The trace shows **`Initial`**, **`Handshake`**, and **`1-RTT`** packets.

**Evidence:** Frames **31-34** contain `Initial` and `Handshake`, and frames **35-39** contain `1-RTT`.

### Question 9

**Q: What connection IDs are visible?**

**A:** The visible connection IDs are:

- Client-side ID: **`8394c8f03e515708`**
- Server-side ID: **`1f4a7b9c00112233`**

**Evidence:** These values appear in the `connection_id` column of `quic-trace.tsv`.

### Question 10

**Q: Which QUIC stream IDs carry application data?**

**A:** The application data streams are **4** and **8**, while **0** is used as a control stream in the condensed trace.

**Evidence:** Frame **36** is stream **4**, frame **37** is stream **8**, and frame **35** marks stream **0** as control.

### Question 11

**Q: What do the QUIC packet numbers tell you?**

**A:** The client packet numbers are **0, 1, 2, 3, 4** in monotonic order, showing that QUIC packet numbers are transport-level sequence markers and are not TCP-style byte sequence numbers.

**Evidence:** Frames **31**, **33**, **35**, **36**, and **37** use packet numbers `0, 1, 2, 3, 4`.

### Question 12

**Q: Compared with HTTP/2, what architectural difference matters most here?**

**A:** HTTP/2 multiplexes streams **above TCP**, so a lost TCP segment can still trigger cross-stream **head-of-line blocking**. QUIC moves multiplexing into the transport over **UDP**, keeps explicit **connection IDs** and **packet numbers**, and avoids that specific TCP-level coupling across streams.
