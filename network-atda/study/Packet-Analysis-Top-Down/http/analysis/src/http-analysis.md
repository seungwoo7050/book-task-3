# HTTP Lab — Analysis Answers

## Part 1: Basic HTTP GET / Response

**Trace file**: `http-basic.pcapng`

### Question 1

**Q: Is your browser running HTTP/1.0 or HTTP/1.1? What version of HTTP is the server running?**

**A:** Both client and server use **HTTP/1.1**.

**Evidence:**
- Request packet **#4**: `GET /kurose_ross_small/HTTP/index.html HTTP/1.1`
- Response packet **#6**: `HTTP/1.1 200 OK`

---

### Question 2

**Q: What languages (if any) does your browser indicate that it can accept to the server?**

**A:** The browser advertises `Accept-Language: en-us,en;q=0.5`.

**Evidence:** Request packet **#4** HTTP header `Accept-Language`.

---

### Question 3

**Q: What is the IP address of your computer? Of the server (gaia.cs.umass.edu)?**

**A:**
- Client (my computer): **192.168.0.2**
- Server (`gaia.cs.umass.edu`): **128.119.245.12**

**Evidence:** Packet **#4** IPv4 header (`ip.src=192.168.0.2`, `ip.dst=128.119.245.12`).

---

### Question 4

**Q: What is the HTTP status code returned from the server to your browser?**

**A:** **200 OK**.

**Evidence:** Response packet **#6** status line `HTTP/1.1 200 OK`.

---

### Question 5

**Q: When was the HTML file that you are retrieving last modified at the server?**

**A:** `Mon, 17 Feb 2025 06:59:02 GMT`.

**Evidence:** Response packet **#6** header `Last-Modified`.

---

### Question 6

**Q: How many bytes of content are being returned to your browser?**

**A:** **36 bytes**.

**Evidence:** Response packet **#6** header `Content-Length: 36`.

---

### Question 7

**Q: Did the server include a Connection header? If so, what value?**

**A:** Yes. The server includes `Connection: keep-alive`.

**Evidence:** Response packet **#6** HTTP header `Connection: keep-alive`.

---

## Part 2: Conditional GET

**Trace file**: `http-conditional.pcapng`

### Question 8

**Q: Inspect the first HTTP GET request. Is there an If-Modified-Since header? What about If-None-Match?**

**A:** No. The first GET contains neither `If-Modified-Since` nor `If-None-Match`.

**Evidence:** Request packet **#4** contains only `Host: gaia.cs.umass.edu` (no conditional headers).

---

### Question 9

**Q: What is the HTTP status code and phrase? Did the server explicitly return the file contents?**

**A:** **200 OK**, and yes, the server returns the file body.

**Evidence:**
- Response packet **#5** status line `HTTP/1.1 200 OK`
- `Content-Length: 18`
- Body payload: `<html>first</html>`

---

### Question 10

**Q: Inspect the second HTTP GET request. Is there an If-Modified-Since header? What information follows it?**

**A:** Yes. The second GET includes:

`If-Modified-Since: Mon, 17 Feb 2025 06:59:02 GMT`

**Evidence:** Request packet **#7** HTTP headers.

---

### Question 11

**Q: What is the HTTP status code and phrase returned for the second request? Did the server return the file contents?**

**A:** **304 Not Modified**. The server does not return the resource body.

**Evidence:**
- Response packet **#8** status line `HTTP/1.1 304 Not Modified`
- Response contains `Date` header only in this trace and no entity body bytes.

---

## Part 3: Long Documents

**Trace file**: `http-long-document.pcapng`

### Question 12

**Q: How many HTTP GET requests did your browser send? How many TCP segments were needed to carry the single HTTP response?**

**A:**
- HTTP GET requests: **1** (packet **#4**)
- TCP segments carrying server response data: **7** (packets **#5–#11**)

**Evidence:**
- `http.request` appears once (frame #4)
- `ip.src==128.119.245.12 && tcp.len>0` matches frames #5, #6, #7, #8, #9, #10, #11.

---

### Question 13

**Q: What is the status code and phrase in the response?**

**A:** **200 OK**.

**Evidence:** Response packet **#11** contains `HTTP/1.1 200 OK` and `Content-Length: 9000`.

---

### Question 14

**Q: How many data-containing TCP segments were sent by the server?**

**A:** **7 segments**.

**Evidence:** Server-to-client segments with `tcp.len > 0` are frames **#5–#11**.

---

### Question 15

**Q: What is the Content-Length value? Is it consistent with the total data transferred?**

**A:** `Content-Length` is **9000** bytes, and it is consistent.

**Evidence:**
- Response header in packet **#11**: `Content-Length: 9000`
- Sum of server `tcp.len` values (frames #5–#11): `1460*6 + 306 = 9066`
- `9066 = HTTP headers (66 bytes) + body (9000 bytes)`.

---

## Part 4: Embedded Objects

**Trace file**: `http-embedded-objects.pcapng`

### Question 16

**Q: How many HTTP GET requests were sent? To which addresses?**

**A:** **3 GET requests** were sent, all to **128.119.245.12**.

**Evidence:**
- Packet **#4**: `GET /index.html`
- Packet **#7**: `GET /img1.png`
- Packet **#10**: `GET /img2.png`
- All three have `ip.dst = 128.119.245.12`.

---

### Question 17

**Q: Were the images downloaded serially or in parallel?**

**A:** **Serially**.

**Evidence:** In the TCP stream:
1. Client requests `/img1.png` (packet #7)
2. Server responds to `/img1.png` (packet #8; reassembled HTTP `200 OK`)
3. Client then requests `/img2.png` (packet #10)
4. Server responds `/img2.png` (packet #11)

There is no overlap of multiple outstanding image requests.

---

### Question 18

**Q: What are the HTTP response status codes for the base page and the images?**

**A:**
- Base page (`/index.html`): **200 OK** (packet **#5**)
- Embedded image (`/img1.png`): **200 OK** (packet **#8**, visible in reassembled TCP stream)
- Embedded image (`/img2.png`): **200 OK** (packet **#11**)

---

### Question 19

**Q: What does the Referer header in image requests contain, and why?**

**A:** The image requests include `Referer: /index.html`.

**Evidence:** Request packets **#7** and **#10** both include that header.

**Why:** The browser indicates that the image fetch was triggered while rendering `/index.html`.
