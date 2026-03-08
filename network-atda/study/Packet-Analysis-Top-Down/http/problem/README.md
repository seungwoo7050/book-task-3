# HTTP Lab — Problem Specification

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Objective

Analyze pre-captured HTTP packet traces using Wireshark to understand how the HTTP protocol operates at the message level. You will examine basic GET exchanges, conditional GET behavior, long document transfers, and multi-object page loads.

## Trace Files

The following trace files are provided in `data/`:

| File | Scenario | Description |
| :--- | :--- | :--- |
| `http-basic.pcapng` | Basic GET | A single HTTP GET request and 200 OK response for a short HTML page |
| `http-conditional.pcapng` | Conditional GET | Two requests to the same page — the second uses `If-Modified-Since` |
| `http-long-document.pcapng` | Long Document | Retrieval of a large HTML document spanning multiple TCP segments |
| `http-embedded-objects.pcapng` | Embedded Objects | Loading a page with multiple embedded images |

## Instructions

Open each trace file in Wireshark and apply the `http` display filter. Then answer the following questions.

---

## Part 1: Basic HTTP GET / Response

**Trace file**: `http-basic.pcapng`

1. Is your browser running HTTP/1.0 or HTTP/1.1? What version of HTTP is the server running?
2. What languages (if any) does your browser indicate that it can accept to the server?
3. What is the IP address of your computer? Of the server (`gaia.cs.umass.edu`)?
4. What is the HTTP status code returned from the server to your browser?
5. When was the HTML file that you are retrieving last modified at the server?
6. How many bytes of content are being returned to your browser?
7. Examine the raw data of the HTTP response packet. Did the server include a `Connection` header? If so, what value?

---

## Part 2: Conditional GET

**Trace file**: `http-conditional.pcapng`

8. Inspect the first HTTP GET request from your browser. Is there an `If-Modified-Since` header in the request? What about `If-None-Match`?
9. Inspect the response. What is the HTTP status code and phrase? Did the server explicitly return the file contents?
10. Now inspect the second HTTP GET request. Is there an `If-Modified-Since` header in this request? If so, what information follows the `If-Modified-Since` header?
11. What is the HTTP status code and phrase returned by the server in response to the second request? Did the server explicitly return the file contents? Explain.

---

## Part 3: Long Documents

**Trace file**: `http-long-document.pcapng`

12. How many HTTP GET request messages did your browser send? How many TCP segments were needed to carry the single HTTP response?
13. What is the status code and phrase in the response?
14. How many data-containing TCP segments were sent by the server in the transfer of the response?
15. What is the `Content-Length` field value in the HTTP response? Is this consistent with the total amount of data transferred?

---

## Part 4: Embedded Objects

**Trace file**: `http-embedded-objects.pcapng`

16. How many HTTP GET request messages did your browser send? To which Internet addresses were these GET requests sent?
17. Can you tell whether your browser downloaded the images serially or in parallel? Explain with evidence from the trace.
18. For the base HTML page, what is the HTTP response status code? For the embedded images?
19. Examine the `Referer` header in the image requests. What URL does it contain, and why?

---

## Evaluation Criteria

| Criterion | Description |
| :--- | :--- |
| **Accuracy** | All answers reference correct packet numbers and field values |
| **Completeness** | Every question is answered with supporting evidence |
| **Understanding** | Explanations demonstrate comprehension of HTTP mechanics |
| **Evidence** | Answers cite specific Wireshark fields and packet data |
