# 에러 처리 및 보안 고려사항

## 개요

웹 서버는 네트워크 환경에서 불특정 다수의 클라이언트 요청을 처리하므로, 견고한 에러 처리와 기본적인 보안 대비가 필수적이다. 이 문서는 웹 서버 구현 시 고려해야 할 에러 시나리오와 보안 이슈를 정리한다.

## HTTP 에러 응답

### 200 OK

정상 요청 처리 시 반환:

```
HTTP/1.1 200 OK\r\n
Content-Type: text/html\r\n
Content-Length: 153\r\n
\r\n
<파일 내용>
```

### 404 Not Found

요청된 리소스를 찾을 수 없을 때:

```
HTTP/1.1 404 Not Found\r\n
Content-Type: text/html\r\n
\r\n
<html><body><h1>404 Not Found</h1></body></html>
```

Python에서 `FileNotFoundError` 예외를 catch하여 처리:

```python
try:
    with open(filename, "rb") as f:
        body = f.read()
    # → 200 OK 응답
except FileNotFoundError:
    # → 404 Not Found 응답
```

### 400 Bad Request (선택적)

잘못된 형식의 요청을 받았을 때:

```python
tokens = request_line.split()
if len(tokens) < 2:
    # 요청 형식이 올바르지 않음 → 연결 종료 또는 400 응답
    return
```

### 500 Internal Server Error (선택적)

서버 내부에서 예상치 못한 오류 발생 시:

```python
except Exception as e:
    header = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
    connection_socket.sendall(header.encode())
```

## 소켓 레벨 에러 처리

### 주요 예외 유형

| 예외 | 원인 | 대처 |
| :--- | :--- | :--- |
| `ConnectionResetError` | 클라이언트가 연결을 강제 종료 | try/except로 정상 종료 |
| `BrokenPipeError` | 이미 닫힌 소켓에 쓰기 시도 | try/except로 무시 |
| `socket.timeout` | 수신 대기 시간 초과 | 연결 종료 처리 |
| `OSError: Address already in use` | 포트가 TIME_WAIT 상태 | `SO_REUSEADDR` 설정 |

### 방어적 코딩 패턴

```python
def handle_client(connection_socket, address):
    try:
        message = connection_socket.recv(4096).decode()
        if not message:
            return  # 빈 요청 → 무시
        # ... 요청 처리 ...
    except FileNotFoundError:
        # 404 응답
    except (ConnectionResetError, BrokenPipeError):
        pass  # 클라이언트 연결 끊김 → 조용히 처리
    except Exception as e:
        print(f"[ERROR] {address}: {e}")
    finally:
        connection_socket.close()  # 항상 소켓 닫기
```

`finally` 블록에서 소켓을 닫는 것이 **핵심**이다. 소켓을 닫지 않으면 파일 디스크립터가 누수되어 운영체제 리소스가 고갈될 수 있다.

## 보안 고려사항

### 1. 디렉토리 트래버설 (Path Traversal)

공격자가 `GET /../../../etc/passwd HTTP/1.1`과 같은 요청을 보내면, 서버의 작업 디렉토리 밖의 파일에 접근할 수 있다.

**방어 방법:**

```python
import os

# 요청된 경로를 정규화
requested_path = os.path.normpath(filename)

# 상위 디렉토리 접근 차단
if requested_path.startswith("..") or os.path.isabs(requested_path):
    # 403 Forbidden 또는 404 응답
    return
```

> 이 과제의 솔루션에서는 단순화를 위해 경로 검증을 생략했지만, 실제 서비스에서는 **반드시** 구현해야 한다.

### 2. 빈 요청 / 비정상 입력

- `recv()`가 빈 바이트열을 반환하는 경우 (클라이언트 즉시 연결 종료)
- HTTP 형식이 아닌 데이터를 보내는 경우
- 극단적으로 긴 요청 라인 (버퍼 오버플로 시도)

→ `len(tokens) < 2` 검증으로 최소한의 방어가 가능하다.

### 3. 리소스 고갈 (DoS)

- 다수의 동시 연결로 스레드가 과도하게 생성되는 상황
- 각 스레드의 메모리 사용으로 서버 메모리 고갈

**방어 방법 (고급):**

```python
from concurrent.futures import ThreadPoolExecutor

# 최대 10개 스레드로 제한
executor = ThreadPoolExecutor(max_workers=10)

while True:
    conn, addr = server_socket.accept()
    executor.submit(handle_client, conn, addr)
```

> 이 과제에서는 `threading.Thread`를 직접 사용하지만, 프로덕션 환경에서는 스레드 풀이나 비동기 I/O(`asyncio`)를 고려해야 한다.

### 4. 로깅

모든 요청과 에러를 기록하는 것은 디버깅과 보안 감사에 필수적이다:

```python
print(f"[INFO] {address[0]}:{address[1]} — {request_line}")
print(f"[ERROR] {address}: {e}")
```

실제 서비스에서는 Python의 `logging` 모듈을 사용하여 파일에 기록하고 로그 레벨을 관리한다.

## 정리

| 항목 | 이 과제에서 구현 | 실서비스 필수 |
| :--- | :---: | :---: |
| 200/404 응답 | ✅ | ✅ |
| FileNotFoundError 처리 | ✅ | ✅ |
| 소켓 닫기 (finally) | ✅ | ✅ |
| SO_REUSEADDR | ✅ | ✅ |
| 빈 요청 검증 | ✅ | ✅ |
| Path Traversal 방어 | ❌ | ✅ |
| 스레드 풀 제한 | ❌ | ✅ |
| 구조화된 로깅 | ❌ | ✅ |
| HTTPS/TLS | ❌ | ✅ |

## 참고 자료

- [OWASP — Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory](https://cwe.mitre.org/data/definitions/22.html)
- Kurose & Ross, *Computer Networking* — Chapter 2, Security 관련 절
