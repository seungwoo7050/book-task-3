# HTTP/1.1 Protocol Reference

## Overview

HTTP (Hypertext Transfer Protocol) is the foundation of data communication on the World Wide Web. It operates as a **request-response** protocol between a client (typically a web browser) and a server. HTTP uses **TCP** as its transport protocol, with the default port being **80** (or **443** for HTTPS).

## HTTP Message Format

HTTP messages are **plain-text** (ASCII) and consist of a **start line**, **headers**, a **blank line**, and an optional **body**.

### Request Message Structure

```
<Method> <Request-URI> <HTTP-Version>\r\n
<Header-Name>: <Header-Value>\r\n
<Header-Name>: <Header-Value>\r\n
...
\r\n
[Optional Body]
```

**Example GET Request:**

```http
GET /index.html HTTP/1.1\r\n
Host: www.example.com\r\n
User-Agent: Mozilla/5.0\r\n
Accept: text/html,application/xhtml+xml\r\n
Accept-Language: en-us,en;q=0.5\r\n
Accept-Encoding: gzip, deflate\r\n
Connection: keep-alive\r\n
\r\n
```

### Response Message Structure

```
<HTTP-Version> <Status-Code> <Reason-Phrase>\r\n
<Header-Name>: <Header-Value>\r\n
<Header-Name>: <Header-Value>\r\n
...
\r\n
[Response Body]
```

**Example 200 OK Response:**

```http
HTTP/1.1 200 OK\r\n
Date: Tue, 18 Feb 2025 09:30:00 GMT\r\n
Server: Apache/2.4.6\r\n
Last-Modified: Mon, 17 Feb 2025 12:00:00 GMT\r\n
Content-Type: text/html\r\n
Content-Length: 5123\r\n
Connection: keep-alive\r\n
\r\n
<!DOCTYPE html>
<html>...
```

## HTTP Methods

| Method | Description | Request Body | Response Body |
| :--- | :--- | :--- | :--- |
| **GET** | Request a representation of a resource | No | Yes |
| **HEAD** | Same as GET but without the response body | No | No |
| **POST** | Submit data to be processed | Yes | Yes |
| **PUT** | Replace the target resource entirely | Yes | Optional |
| **DELETE** | Delete the specified resource | No | Optional |
| **OPTIONS** | Describe communication options for the resource | No | Yes |

In this lab, you will primarily observe **GET** requests.

## Status Codes

### Categories

| Range | Category | Description |
| :--- | :--- | :--- |
| 1xx | Informational | Request received, continuing process |
| 2xx | Successful | Request successfully received and processed |
| 3xx | Redirection | Further action needed to complete the request |
| 4xx | Client Error | Request contains bad syntax or cannot be fulfilled |
| 5xx | Server Error | Server failed to fulfill a valid request |

### Common Status Codes in This Lab

| Code | Phrase | Meaning |
| :--- | :--- | :--- |
| **200** | OK | Request succeeded; the response body contains the resource |
| **304** | Not Modified | The cached copy is still valid; no body returned |
| **301** | Moved Permanently | Resource has been permanently moved to a new URL |
| **404** | Not Found | The server cannot find the requested resource |

## Key Request Headers

| Header | Purpose | Example |
| :--- | :--- | :--- |
| `Host` | Specifies the domain name of the server | `Host: www.example.com` |
| `User-Agent` | Identifies the client software | `User-Agent: Mozilla/5.0 ...` |
| `Accept` | Media types the client can process | `Accept: text/html, */*` |
| `Accept-Language` | Preferred natural languages | `Accept-Language: en-us` |
| `Accept-Encoding` | Acceptable content encodings | `Accept-Encoding: gzip, deflate` |
| `Connection` | Control options for the connection | `Connection: keep-alive` |
| `If-Modified-Since` | Conditional request — only return if modified | `If-Modified-Since: Mon, 17 Feb 2025 ...` |
| `If-None-Match` | Conditional request — compare ETags | `If-None-Match: "abc123"` |
| `Referer` | The URL of the page that linked to this request | `Referer: http://www.example.com/page.html` |

## Key Response Headers

| Header | Purpose | Example |
| :--- | :--- | :--- |
| `Date` | When the response was generated | `Date: Tue, 18 Feb 2025 09:30:00 GMT` |
| `Server` | The web server software | `Server: Apache/2.4.6` |
| `Content-Type` | The MIME type of the response body | `Content-Type: text/html; charset=UTF-8` |
| `Content-Length` | The size of the response body in bytes | `Content-Length: 5123` |
| `Last-Modified` | When the resource was last changed | `Last-Modified: Mon, 17 Feb 2025 ...` |
| `ETag` | An opaque identifier for the resource version | `ETag: "abc123"` |
| `Connection` | Connection management directive | `Connection: keep-alive` |
| `Cache-Control` | Caching directives | `Cache-Control: max-age=3600` |

## Persistent Connections (HTTP/1.1)

HTTP/1.0 used a **non-persistent** model: a new TCP connection is opened and closed for each request-response pair.

HTTP/1.1 introduced **persistent connections** by default:
- The same TCP connection is reused for multiple request-response exchanges
- The `Connection: keep-alive` header signals the desire to keep the connection open
- The `Connection: close` header signals the connection should be closed after the response
- This reduces the overhead of TCP handshakes for pages with many embedded objects

## How HTTP Appears in Wireshark

In Wireshark, HTTP messages appear as **application-layer payloads** inside TCP segments:

```
Frame (Ethernet) → IP → TCP → HTTP
```

- The **Info** column shows HTTP request methods (GET, POST) and response status codes (200, 304)
- Expanding the **Hypertext Transfer Protocol** layer reveals all headers and body data
- A single HTTP message may span **multiple TCP segments** for large responses
- Wireshark automatically **reassembles** HTTP messages from TCP segments

## Wireshark Columns to Examine

| Column / Field | What to Look For |
| :--- | :--- |
| `frame.number` | Packet sequence number in the trace |
| `ip.src` / `ip.dst` | Source and destination IP addresses |
| `http.request.method` | GET, POST, etc. |
| `http.request.uri` | The requested resource path |
| `http.response.code` | 200, 304, 404, etc. |
| `http.content_length` | Size of the HTTP body |
| `http.last_modified` | Last-Modified header value |
| `http.user_agent` | Client identification string |
