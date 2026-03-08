# HTTP Conditional GET and Caching

## The Problem

Every time a browser requests a resource, the server sends the complete response body. But what if the resource hasn't changed since the last time the browser fetched it? Sending the same data again wastes bandwidth and increases latency.

## Web Caching — The Concept

Web caching stores copies of frequently accessed resources closer to the client. Caching occurs at multiple levels:

1. **Browser cache** — The browser stores responses locally on disk
2. **Proxy cache** — An intermediary (corporate proxy, CDN) stores responses
3. **Server cache** — The origin server caches generated content

The key challenge: **How does the client know if its cached copy is still valid?**

## Conditional GET Mechanism

HTTP provides the **conditional GET** to solve this. The client includes a condition in the request; the server only returns the full body if the condition fails.

### Flow Diagram

```
1st request:
   Client → GET /page.html HTTP/1.1 → Server
   Client ← 200 OK (Last-Modified: Mon, 17 Feb 2025 12:00:00 GMT) ← Server
   [Browser caches the response]

2nd request (resource NOT changed):
   Client → GET /page.html HTTP/1.1
            If-Modified-Since: Mon, 17 Feb 2025 12:00:00 GMT → Server
   Client ← 304 Not Modified (no body) ← Server
   [Browser uses cached copy]

2nd request (resource HAS changed):
   Client → GET /page.html HTTP/1.1
            If-Modified-Since: Mon, 17 Feb 2025 12:00:00 GMT → Server
   Client ← 200 OK (new content, new Last-Modified) ← Server
   [Browser updates cache]
```

## Key Headers

### `Last-Modified` (Response Header)

Sent by the server to indicate when the resource was last changed.

```http
Last-Modified: Mon, 17 Feb 2025 12:00:00 GMT
```

### `If-Modified-Since` (Request Header)

Sent by the client in a conditional GET. Its value is the `Last-Modified` date from the cached response.

```http
If-Modified-Since: Mon, 17 Feb 2025 12:00:00 GMT
```

- If the resource **has not changed** → Server returns **304 Not Modified** (no body)
- If the resource **has changed** → Server returns **200 OK** with the new content

### `ETag` / `If-None-Match`

An alternative to date-based validation using opaque identifiers:

```http
# Server sends in response:
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"

# Client sends in subsequent request:
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
```

ETags are more precise than `Last-Modified` because:
- Dates have 1-second granularity (might miss sub-second changes)
- Some servers cannot reliably determine the last modification time
- ETags can represent content hashes, making them content-aware

## What to Look for in Wireshark

When analyzing a conditional GET trace:

### First Request (No Cache Yet)

| Field | Expected Value |
| :--- | :--- |
| Request method | `GET` |
| `If-Modified-Since` | **Absent** (no cached version) |
| Response code | `200 OK` |
| `Last-Modified` | Present in the response |
| Response body | Present (full HTML content) |

### Second Request (Cached Copy Exists)

| Field | Expected Value |
| :--- | :--- |
| Request method | `GET` |
| `If-Modified-Since` | Present (matches previous `Last-Modified`) |
| Response code | `304 Not Modified` |
| Response body | **Absent** (empty — use cache) |

## Wireshark Filters for Conditional GET

```
http.response.code == 304
http.request.line contains "If-Modified-Since"
http.response.code == 200 || http.response.code == 304
```

## Bandwidth Savings

A `304 Not Modified` response is typically very small (just headers, ~200 bytes) compared to a full `200 OK` response that may be many kilobytes. For frequently accessed resources, this saves significant bandwidth.

| Scenario | Typical Size |
| :--- | :--- |
| Full 200 OK (HTML page) | 5–100 KB |
| 304 Not Modified | ~200 bytes (headers only) |
| Savings per conditional hit | 95–99%+ |
