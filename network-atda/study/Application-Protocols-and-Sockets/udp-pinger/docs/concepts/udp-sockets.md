# UDP Socket Programming in Python

## Overview

UDP (User Datagram Protocol) is a **connectionless**, **unreliable** transport protocol. Unlike TCP, UDP does not establish a connection before sending data, does not guarantee delivery, and does not guarantee ordering.

| Property | TCP | UDP |
| :--- | :--- | :--- |
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | Best-effort (may lose) |
| Ordering | In-order delivery | No ordering guarantee |
| Overhead | Higher (handshake, acks) | Lower (no handshake) |
| Use Cases | Web, email, file transfer | DNS, streaming, gaming |

## UDP Socket API in Python

### Creating a UDP Socket

```python
import socket

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

- `AF_INET`: IPv4
- `SOCK_DGRAM`: UDP datagram socket (contrast with `SOCK_STREAM` for TCP)

### Sending Data

```python
message = "Hello, server!"
server_address = ("127.0.0.1", 12000)

# Send a datagram — no connection required
udp_socket.sendto(message.encode(), server_address)
```

- `sendto(data, address)`: Send a datagram to the specified `(host, port)`
- Each `sendto()` call sends one independent datagram
- No prior `connect()` is needed

### Receiving Data

```python
data, server_address = udp_socket.recvfrom(1024)
print(data.decode())
```

- `recvfrom(bufsize)`: Receive a datagram (up to `bufsize` bytes)
- Returns `(data, address)` where `address` is the sender's `(host, port)`
- **Blocks** until a datagram arrives (or timeout expires)

### Setting a Timeout

```python
udp_socket.settimeout(1.0)  # 1-second timeout

try:
    data, addr = udp_socket.recvfrom(1024)
except socket.timeout:
    print("No response — packet may have been lost")
```

- `settimeout(seconds)`: If no data arrives within the timeout, `recvfrom()` raises `socket.timeout`
- This is essential for UDP because packets can be **lost** — without a timeout, the program would block forever

### Closing the Socket

```python
udp_socket.close()
```

## Server vs. Client

### UDP Server Pattern

```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("", 12000))    # Bind to port 12000

while True:
    message, client_addr = server_socket.recvfrom(1024)
    # Process message...
    server_socket.sendto(reply.encode(), client_addr)
```

- The server **binds** to a well-known port
- `recvfrom()` tells the server who sent the message so it can reply

### UDP Client Pattern

```python
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

client_socket.sendto(message.encode(), ("127.0.0.1", 12000))
try:
    data, addr = client_socket.recvfrom(1024)
except socket.timeout:
    print("Timed out")

client_socket.close()
```

- The client does **not** need to `bind()` — the OS assigns an ephemeral port
- The client should set a timeout to handle lost packets

## Comparison: TCP vs. UDP Socket Flow

```
TCP:                             UDP:
socket()                         socket()
bind()                           bind() (server) / — (client)
listen()                         —
accept() → new socket            —
recv() / send()                  recvfrom() / sendto()
close()                          close()
```

## Common Pitfalls

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| `socket.timeout` exception | No packet received in time | Expected for lost packets — handle with try/except |
| Wrong address in `sendto()` | Typo in host/port | Double-check server address |
| Large messages truncated | Exceeds buffer or MTU | Keep messages under 1024 bytes |
| `bind()` on client | Unnecessary port binding | Clients typically don't need `bind()` |
