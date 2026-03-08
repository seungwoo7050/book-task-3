# Web Server — Problem Specification

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Objective

Implement a simple HTTP web server that can process **one HTTP request at a time**. The server listens on a specified port, accepts incoming TCP connections, and responds with the requested file or an error message.

## Requirements

### Functional Requirements

1. **TCP Connection Handling**
   - Create a TCP server socket bound to `localhost` on port `6789` (configurable)
   - Listen for and accept incoming client connections
   - Handle each connection in a separate thread

2. **HTTP Request Parsing**
   - Extract the requested file path from the HTTP GET request line
   - The request line format: `GET /path/to/file HTTP/1.1\r\n`

3. **HTTP Response Generation**
   - **200 OK**: If the requested file exists, respond with:
     ```
     HTTP/1.1 200 OK\r\n
     Content-Type: <mime-type>\r\n
     \r\n
     <file contents>
     ```
   - **404 Not Found**: If the file does not exist, respond with:
     ```
     HTTP/1.1 404 Not Found\r\n
     Content-Type: text/html\r\n
     \r\n
     <html><body><h1>404 Not Found</h1></body></html>
     ```

4. **File Serving**
   - Serve files relative to the server's working directory
   - Support at least `.html` and `.htm` content types

### Non-Functional Requirements

- The server must remain running and accept multiple sequential connections
- Connections must be properly closed after each response
- The server should print a log message for each request received

## Constraints

- Use only Python 3 standard library modules
- Primary modules: `socket`, `threading`
- No HTTP helper libraries (e.g., `http.server` is **not** allowed)

## Input / Environment

- The starter code skeleton is in `code/server_skeleton.py`
- A sample HTML file for testing is in `data/hello.html`
- A test script is available at `script/test_server.sh`

## Evaluation Criteria

| Criterion | Description |
| :--- | :--- |
| **Correct 200 Response** | Server returns the file with a valid `HTTP/1.1 200 OK` header |
| **Correct 404 Response** | Server returns a `404 Not Found` page for missing files |
| **Connection Handling** | Server properly accepts, processes, and closes connections |
| **Multi-threading** | Each request is handled in its own thread |
| **Code Quality** | Clean, well-commented, and idiomatic Python |
