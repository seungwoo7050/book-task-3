# TCP Socket Programming in Python

## Overview

A **socket** is an endpoint for communication between two machines over a network. Python's built-in `socket` module provides access to the BSD socket interface, enabling low-level network programming.

TCP (Transmission Control Protocol) provides **reliable, ordered, error-checked** delivery of a stream of bytes between applications.

## Socket Types

| Domain | Type | Protocol | Description |
| :--- | :--- | :--- | :--- |
| `AF_INET` | `SOCK_STREAM` | TCP | Reliable byte-stream (connection-oriented) |
| `AF_INET` | `SOCK_DGRAM` | UDP | Unreliable datagram (connectionless) |

For a web server, we use **`AF_INET` + `SOCK_STREAM`** (TCP).

## TCP Server Workflow

```
 socket()  →  bind()  →  listen()  →  accept()  →  recv/send  →  close()
```

### Step 1: Create a Socket

```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

- `AF_INET`: IPv4 address family
- `SOCK_STREAM`: TCP socket type

### Step 2: Set Socket Options (Recommended)

```python
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

`SO_REUSEADDR` allows the server to rebind to the same port immediately after a restart, avoiding "Address already in use" errors.

### Step 3: Bind to an Address

```python
server_socket.bind(('', 6789))
```

- `''` (empty string) means bind to **all available interfaces** (equivalent to `0.0.0.0`)
- `6789` is the port number

### Step 4: Listen for Connections

```python
server_socket.listen(1)
```

The argument is the **backlog** — the maximum number of queued connections. A value of `1` is sufficient for this assignment.

### Step 5: Accept a Connection

```python
connection_socket, address = server_socket.accept()
```

- `accept()` **blocks** until a client connects
- Returns a **new socket** for communicating with that specific client, plus the client's `(host, port)` address
- The original `server_socket` continues to listen for new connections

### Step 6: Receive and Send Data

```python
# Receive up to 4096 bytes
data = connection_socket.recv(4096)
message = data.decode()  # bytes → str

# Send a response
response = "HTTP/1.1 200 OK\r\n\r\nHello"
connection_socket.sendall(response.encode())  # str → bytes
```

Key methods:
- `recv(bufsize)`: Receive up to `bufsize` bytes. Returns `b""` if the connection is closed.
- `send(data)`: Send data. May not send all bytes in one call.
- `sendall(data)`: Send all data (preferred — handles partial sends automatically).

### Step 7: Close the Connection

```python
connection_socket.close()
```

Always close sockets when done to free resources.

## Complete Minimal Server Example

```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 6789))
server_socket.listen(1)
print("Server ready on port 6789")

while True:
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    request = conn.recv(4096).decode()
    print(request)

    response = "HTTP/1.1 200 OK\r\n\r\n<h1>Hello</h1>"
    conn.sendall(response.encode())
    conn.close()
```

## TCP Client Workflow (for reference)

```python
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 6789))
client_socket.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
response = client_socket.recv(4096)
print(response.decode())
client_socket.close()
```

## Common Pitfalls

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| `OSError: [Errno 98] Address already in use` | Port still in TIME_WAIT state | Use `SO_REUSEADDR` |
| `BrokenPipeError` | Client closed connection before server finished sending | Wrap send in try/except |
| `ConnectionResetError` | Client reset the connection | Wrap recv in try/except |
| Empty `recv()` return | Client closed its end | Check for `b""` and close |

## Encoding and Decoding

- **Encode** (`str.encode()`): Convert Python string → bytes for sending over network
- **Decode** (`bytes.decode()`): Convert received bytes → Python string for processing
- HTTP headers are ASCII text; file bodies may be binary (images, etc.)
- For binary files, do **not** decode — send raw bytes after the header
