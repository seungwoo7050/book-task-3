# Web Proxy — 중개자의 시선으로 HTTP를 보다

## 서버이면서 클라이언트

웹 서버 과제에서는 서버 역할만 했다. SMTP 클라이언트에서는 클라이언트 역할만 했다. 프록시는 둘 다를 **동시에** 해야 한다.

브라우저가 프록시에 요청을 보내면, 프록시는 그 요청을 원래 서버(origin server)에 전달하고, 원 서버의 응답을 받아서 다시 브라우저에게 전달한다. 브라우저 입장에서는 프록시가 서버이고, 원 서버 입장에서는 프록시가 클라이언트다.

이 이중 역할이 프록시의 본질이었고, 코드의 구조를 결정했다.

## 절대 URL과 상대 URL

프록시를 구현하면서 처음 알게 된 것이 있다. 일반적인 HTTP 요청과 프록시 요청의 형식이 다르다는 것이다.

직접 서버에 보내는 요청:
```
GET /index.html HTTP/1.1
Host: www.example.com
```

프록시를 통한 요청:
```
GET http://www.example.com/index.html HTTP/1.1
```

프록시 요청은 **절대 URL** 전체가 들어온다. 프록시는 이 URL에서 호스트명, 포트, 경로를 분리해야 한다.

이 파싱 함수를 작성하는 게 과제의 첫 번째 관문이었다:

```python
def parse_url(url: str) -> tuple[str, int, str]:
    # "http://www.example.com:8080/path" → ("www.example.com", 8080, "/path")
```

`http://`를 제거하고, `/` 기준으로 호스트와 경로를 분리하고, `:`이 있으면 포트를 추출한다. 포트가 없으면 기본 80. 경로가 없으면 `/`.

간단해 보이지만, edge case가 많았다. `http://example.com` (경로 없음), `http://example.com:8080` (포트만 있고 경로 없음), `http://example.com/` (빈 경로) 등을 다 처리해야 했다.

## 원 서버로 전달할 때는 상대 경로로

프록시가 원 서버에 요청을 보낼 때는 절대 URL이 아니라 **상대 경로**로 바꿔야 한다:

```python
request = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {hostname}\r\n"
    f"Connection: close\r\n"
    f"\r\n"
)
```

원 서버는 "내가 프록시를 거쳐 왔다"는 사실을 모르고, 일반 클라이언트가 보낸 요청과 동일하게 처리한다.

`Connection: close`를 명시적으로 넣은 이유는, 응답이 끝나는 시점을 확실히 알기 위해서다. keep-alive를 쓰면 응답이 끝났는지 Content-Length를 파싱해야 하거나 chunked transfer encoding을 다뤄야 해서, 과제 범위를 벗어난다.

## 캐시: MD5 해시로 파일명 만들기

같은 URL에 대한 두 번째 요청은 원 서버에 다시 연결하지 않고 캐시된 응답을 반환한다. 캐시 파일명은 URL의 MD5 해시를 사용했다:

```python
def get_cache_path(url: str) -> str:
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{url_hash}.dat")
```

왜 URL을 그대로 파일명으로 쓰지 않았나? URL에는 `/`, `?`, `&`, `:` 같은 파일 시스템에서 금지되거나 문제가 되는 문자들이 있다. 해시를 쓰면 어떤 URL이든 깔끔한 파일명이 된다.

캐시 히트/미스 로그를 출력해서 확인할 수 있었다:
```
[FETCH] http://www.example.com/ → origin server
[CACHE] Stored: cache/a1b2c3d4e5f6...dat
[HIT]   http://www.example.com/ → served from cache
```

이 캐시에는 TTL(만료 시간) 개념이 없다. 한번 캐시된 응답은 `cache/` 디렉터리를 직접 삭제하기 전까지 영원히 유효하다. 실제 프록시에서는 Cache-Control 헤더를 파싱해 만료 정책을 적용해야 하지만, 이 과제에서는 "캐시가 동작한다"는 것만 보여주면 충분했다.

## 에러 처리: 502와 504

프록시는 일반 서버와 다른 에러 코드를 사용한다:
- **504 Gateway Timeout**: 원 서버가 응답하지 않을 때
- **502 Bad Gateway**: 원 서버에 연결할 수 없을 때 (DNS 실패, 연결 거부)

이 에러 코드들은 프록시/게이트웨이 환경에서만 쓰인다. 평소 웹사이트에서 502/504를 보면, 그건 원 서버 문제가 아니라 **중간 프록시나 로드밸런서가 뒤쪽 서버와 연결 못 했다**는 의미라는 걸 이 과제를 통해 이해했다.

```python
except socket.timeout:
    # 원 서버가 10초 안에 응답하지 않음
    client_socket.sendall(b"HTTP/1.1 504 Gateway Timeout\r\n...")

except (socket.gaierror, ConnectionRefusedError):
    # DNS 실패 또는 연결 거부
    client_socket.sendall(b"HTTP/1.1 502 Bad Gateway\r\n...")
```

## 멀티스레딩: 웹 서버와 동일한 패턴

여러 브라우저 탭이 동시에 프록시를 쓸 수 있으니, 각 클라이언트 연결을 별도 스레드에서 처리했다. 패턴은 웹 서버 과제와 동일하다:

```python
t = threading.Thread(target=handle_client, args=(client_socket, address))
t.daemon = True
t.start()
```

## 테스트: curl의 -x 옵션

프록시를 테스트하는 가장 간단한 방법은 curl의 프록시 옵션이다:

```bash
# 프록시를 통해 요청
curl -x http://localhost:8888 http://www.example.com/

# 첫 번째: [FETCH] + [CACHE] 로그 → 원 서버에서 가져옴
# 두 번째: [HIT] 로그 → 캐시에서 반환
```

자동 테스트(`test_proxy.sh`)는 더 정교하다:
1. 임시 디렉터리에 테스트 HTML 생성
2. `python3 -m http.server`로 간이 원 서버 기동
3. 프록시를 통해 요청 → 200 확인
4. 원 서버 종료 후 같은 요청 → 캐시에서 200 확인
5. 존재하지 않는 호스트 → 502 확인

## 이 과제에서 가져간 것

프록시를 만들면서 HTTP의 구조가 더 깊이 보였다. 절대 URL과 상대 URL의 차이, Host 헤더의 역할, Connection 헤더의 의미, 502/504 에러 코드의 출처. 이런 것들은 프록시를 직접 구현해봐야 체감할 수 있는 세부사항이었다.

또한 "중개자"라는 아키텍처 패턴을 처음 경험했다. 클라이언트와 서버 사이에 서서, 양쪽의 프로토콜을 이해하고, 요청/응답을 변환해서 전달한다. 이 패턴은 나중에 로드밸런서, API 게이트웨이, 리버스 프록시를 이해하는 데 기반이 됐다.

---

> **학습 키워드**: HTTP 프록시, 절대 URL 파싱, 캐싱(MD5 해시), `Connection: close`, 502/504 에러 코드, 중개자 패턴