# HTTP Proxy Reference

## What is a Web Proxy?

A **web proxy** is an intermediary server that sits between a client and an origin web server. The client sends all HTTP requests to the proxy, and the proxy forwards them to the appropriate origin server.

```
Client  ──(1)──►  Proxy  ──(2)──►  Origin Server
        ◄──(4)──         ◄──(3)──
```

1. Client sends HTTP request to proxy
2. Proxy forwards request to origin server
3. Origin server sends response to proxy
4. Proxy forwards response to client

## Proxy HTTP Requests vs. Direct Requests

When a browser is configured to use a proxy, it sends requests with **absolute URLs** instead of relative paths:

**Direct request (to origin server):**
```
GET /index.html HTTP/1.1\r\n
Host: www.example.com\r\n
\r\n
```

**Proxy request (to proxy):**
```
GET http://www.example.com/index.html HTTP/1.1\r\n
Host: www.example.com\r\n
\r\n
```

The proxy must:
1. Extract the hostname, port, and path from the absolute URL
2. Open a TCP connection to the origin server
3. Send a **modified** request with a relative path
4. Relay the response back to the client

## Proxy Forwarding Logic

```python
# 1. Parse the client's request
request_line = "GET http://www.example.com/index.html HTTP/1.1"
# Extract: host = "www.example.com", port = 80, path = "/index.html"

# 2. Build a new request for the origin server
forwarded_request = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    f"Connection: close\r\n"
    f"\r\n"
)

# 3. Connect to origin and send
origin_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origin_socket.connect((host, port))
origin_socket.sendall(forwarded_request.encode())

# 4. Receive the full response
response = b""
while True:
    chunk = origin_socket.recv(4096)
    if not chunk:
        break
    response += chunk
origin_socket.close()

# 5. Send response to client
client_socket.sendall(response)
```

## Web Caching

Caching allows the proxy to store responses and serve them for repeated requests without contacting the origin server.

### Benefits
- **Reduced latency**: Cache hits are served instantly
- **Reduced bandwidth**: No redundant origin server traffic
- **Reduced server load**: Origin server handles fewer requests

### Simple Cache Implementation

```python
import hashlib
import os

CACHE_DIR = "cache"

def get_cache_key(url):
    """Generate a cache filename from the URL."""
    return hashlib.md5(url.encode()).hexdigest() + ".dat"

def cache_store(url, data):
    """Store a response in the cache."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, get_cache_key(url))
    with open(path, "wb") as f:
        f.write(data)

def cache_lookup(url):
    """Retrieve a cached response, or None if not cached."""
    path = os.path.join(CACHE_DIR, get_cache_key(url))
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    return None
```

### Cache Flow

```
Client Request
    │
    ▼
Cache Lookup
    │
    ├── HIT  → Return cached response
    │
    └── MISS → Fetch from origin server
                │
                ├── Cache the response
                └── Return to client
```

## Connection: close Header

Always include `Connection: close` in the forwarded request to tell the origin server to close the connection after the response. This simplifies receiving the complete response — you read until `recv()` returns empty bytes.

Without `Connection: close`, the server may keep the connection open (HTTP keep-alive), and `recv()` will block indefinitely.

## Handling Errors

The proxy should handle:
- **Connection refused**: Origin server is down → return 502 Bad Gateway
- **DNS failure**: Hostname doesn't resolve → return 502 Bad Gateway
- **Timeout**: Origin server too slow → return 504 Gateway Timeout
- **Invalid request**: Malformed client request → return 400 Bad Request

For this assignment, basic error handling (try/except with informative logging) is sufficient.
