# HTTP/1.1 Protocol Reference

## Overview

HTTP (Hypertext Transfer Protocol) is an application-layer protocol for transmitting hypermedia documents. It follows a **request-response** model: a client sends a request message, and the server replies with a response message.

HTTP uses **TCP** as its transport-layer protocol. Before any HTTP messages are exchanged, the client and server complete a TCP three-way handshake to establish a connection.

## HTTP Message Format

All HTTP messages are plain **ASCII text**, terminated by `\r\n` (carriage return + line feed).

### Request Message

```
<Method> <URL> <Version>\r\n      ← Request line
<Header-Name>: <Value>\r\n        ← Header lines (0 or more)
\r\n                               ← Blank line (end of headers)
<Body>                             ← Optional body
```

**Example — GET Request**

```
GET /hello.html HTTP/1.1\r\n
Host: localhost:6789\r\n
Connection: close\r\n
User-Agent: curl/7.68.0\r\n
\r\n
```

Key fields:
- **Method**: `GET` — requests a resource from the server
- **URL**: `/hello.html` — the path to the requested resource (relative to server root)
- **Version**: `HTTP/1.1` — the HTTP version

### Response Message

```
<Version> <Status-Code> <Reason-Phrase>\r\n   ← Status line
<Header-Name>: <Value>\r\n                     ← Header lines
\r\n                                            ← Blank line
<Body>                                          ← Response body
```

**Example — 200 OK Response**

```
HTTP/1.1 200 OK\r\n
Content-Type: text/html\r\n
Content-Length: 153\r\n
\r\n
<!DOCTYPE html>
<html>...
```

**Example — 404 Not Found Response**

```
HTTP/1.1 404 Not Found\r\n
Content-Type: text/html\r\n
\r\n
<html><body><h1>404 Not Found</h1></body></html>
```

## Common HTTP Methods

| Method | Purpose | Has Body? |
| :--- | :--- | :--- |
| `GET` | Retrieve a resource | No (request), Yes (response) |
| `POST` | Submit data to a resource | Yes |
| `HEAD` | Same as GET but without body | No |
| `PUT` | Replace a resource | Yes |
| `DELETE` | Remove a resource | No |

For this assignment, you only need to handle **GET** requests.

## Common Status Codes

| Code | Phrase | Meaning |
| :--- | :--- | :--- |
| `200` | OK | The request succeeded; resource is in the body |
| `301` | Moved Permanently | The resource has been relocated |
| `400` | Bad Request | The server cannot understand the request |
| `404` | Not Found | The server cannot find the requested resource |
| `500` | Internal Server Error | Generic server-side error |

For this assignment, you need to implement **200 OK** and **404 Not Found**.

## Content-Type Header

The `Content-Type` header tells the client what kind of data the body contains.

| File Extension | Content-Type |
| :--- | :--- |
| `.html`, `.htm` | `text/html` |
| `.css` | `text/css` |
| `.js` | `application/javascript` |
| `.png` | `image/png` |
| `.jpg`, `.jpeg` | `image/jpeg` |
| `.gif` | `image/gif` |
| `.ico` | `image/x-icon` |
| `.txt` | `text/plain` |

## Parsing an HTTP GET Request in Python

```python
# Receive raw bytes from socket
data = connection_socket.recv(4096)
message = data.decode()

# Split into lines
lines = message.split("\r\n")

# Parse the request line
# Example: "GET /hello.html HTTP/1.1"
request_line = lines[0]
parts = request_line.split()
method = parts[0]    # "GET"
path = parts[1]      # "/hello.html"
version = parts[2]   # "HTTP/1.1"

# Extract filename (remove leading '/')
filename = path[1:]  # "hello.html"
```

## Constructing an HTTP Response in Python

```python
# Read the file
with open(filename, "rb") as f:
    body = f.read()

# Build response header
header = "HTTP/1.1 200 OK\r\n"
header += "Content-Type: text/html\r\n"
header += f"Content-Length: {len(body)}\r\n"
header += "\r\n"

# Send header (as bytes) followed by body
connection_socket.sendall(header.encode() + body)
```

## Connection Lifecycle

```
Client                              Server
  |                                   |
  |  ---- TCP SYN ----------------->  |   (1) TCP handshake
  |  <--- TCP SYN-ACK -------------  |
  |  ---- TCP ACK ----------------->  |
  |                                   |
  |  ---- GET /hello.html -------->  |   (2) HTTP request
  |                                   |
  |  <--- HTTP/1.1 200 OK ---------  |   (3) HTTP response
  |  <--- <file contents> ---------  |
  |                                   |
  |  ---- TCP FIN ----------------->  |   (4) Connection close
  |  <--- TCP FIN -----------------  |
  |                                   |
```
