# Web Proxy — Problem Specification

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Objective

Implement an HTTP proxy server that forwards client HTTP GET requests to origin servers, returns the responses to the client, and caches responses for future requests.

## Requirements

### Functional Requirements

1. **Proxy Listening**
   - Listen on a configurable TCP port (default: `8888`)
   - Accept incoming client connections

2. **Request Parsing**
   - Parse the HTTP GET request to extract the target URL
   - A proxy request uses an **absolute URL**:
     ```
     GET http://www.example.com/index.html HTTP/1.1\r\n
     ```
   - Extract: hostname, port (default 80), and path

3. **Forwarding**
   - Open a TCP connection to the origin server
   - Send a modified HTTP request (with relative path):
     ```
     GET /index.html HTTP/1.1\r\n
     Host: www.example.com\r\n
     Connection: close\r\n
     \r\n
     ```
   - Receive the full response from the origin server

4. **Response Relay**
   - Forward the origin server's response back to the client
   - Close the client connection

5. **Caching**
   - After receiving a response from the origin server, cache it locally
   - On subsequent requests for the same URL, serve from cache (no origin contact)
   - Cache files can use a hash of the URL as the filename
   - Print a log message indicating whether a response is served from cache or fetched fresh

6. **Concurrent Connections**
   - Handle each client connection in a separate thread

### Expected Output

```
[INFO] Proxy server started on port 8888
[FETCH] GET http://www.example.com/index.html → origin server
[CACHE] Stored: cache/a1b2c3d4.dat
[HIT]   GET http://www.example.com/index.html → served from cache
```

## Constraints

- Python 3 standard library only
- No HTTP libraries (`http.client`, `urllib`, `requests` are **not** allowed)
- Handle only HTTP GET requests (not HTTPS CONNECT)
- The proxy should handle basic HTTP/1.1 requests

## Input / Environment

- Skeleton code: `code/proxy_skeleton.py`
- Test script: `script/test_proxy.sh`
- Configure your browser to use `localhost:8888` as HTTP proxy, or use curl:
  ```bash
  curl -x http://localhost:8888 http://www.example.com/
  ```

## Evaluation Criteria

| Criterion | Description |
| :--- | :--- |
| **Request Forwarding** | Proxy correctly relays requests to origin servers |
| **Response Relay** | Client receives the complete origin response |
| **Caching** | Repeated requests are served from local cache |
| **URL Parsing** | Hostname, port, and path are extracted correctly |
| **Multi-threading** | Concurrent connections are handled |
| **Code Quality** | Clean, well-documented code |
