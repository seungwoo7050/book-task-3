# Web Proxy 개발 타임라인

## Day 1

### Session 1

- 목표: proxy가 받는 요청이 일반 서버와 어디가 다른지부터 확인한다.
- 진행: `test_proxy.sh`를 열어 보니 `curl -x http://localhost:8888 http://www.example.com/` 형식이었다. 일반 서버는 `GET /path`만 오는데, proxy는 `GET http://www.example.com/ HTTP/1.1` — absolute URL이 통째로 온다.
- 이슈: 이 차이를 놓치면 proxy 코드의 첫 단계부터 꼬인다. 웹 서버에서 쓰던 파싱 로직을 그대로 가져오면 `http://www.example.com/`을 파일명으로 열려고 시도한다.
- 판단: 가장 먼저 해야 할 건 absolute URL을 `hostname`, `port`, `path`로 분해하는 `parse_url()`이다.

### Session 2

- 목표: URL parsing을 구현하고 edge case를 확인한다.
- 진행:

```py
temp = url.replace("http://", "", 1)

if "/" in temp:
    host_port, path = temp.split("/", 1)
    path = "/" + path
else:
    host_port = temp
    path = "/"

if ":" in host_port:
    hostname, port_str = host_port.split(":", 1)
    port = int(port_str)
else:
    hostname = host_port
    port = 80
```

- 이슈: `http://example.com`처럼 trailing `/`가 없는 URL을 보내면 `path`가 빈 문자열이 됐다. origin으로 `GET  HTTP/1.1`이 나가서 `400` 응답이 돌아왔다. `path = "/"`로 기본값을 넣어야 안정적이었다.
- 검증: unit test에서 `parse_url("http://host:8080/page")` → `("host", 8080, "/page")`를 특히 확인했다.

### Session 3

- 목표: origin fetch를 구현한다 — proxy가 원 서버에 대신 요청을 보내는 부분.
- 진행: origin 요청은 proxy가 "나도 클라이언트"가 되는 순간이다. 새 TCP 소켓을 열고, `GET {path} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n`을 보낸다.
- 이슈: `Connection: close`를 안 넣으면 origin 서버가 연결을 끊지 않아서 `recv()` 루프가 안 끝났다. Web Server에서 "Connection: close를 왜 넣는지" 배웠던 게 여기서 바로 쓰였다.

```py
request = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {hostname}\r\n"
    f"Connection: close\r\n"
    f"\r\n"
)
```

### Session 4

- 목표: cache를 넣어서 같은 URL의 재요청을 origin 없이 처리한다.
- 진행: cache key는 URL의 MD5 해시, cache는 `cache/` 디렉터리에 파일로 저장하는 단순한 구조로 갔다.

```py
cache_path = get_cache_path(url)
if os.path.exists(cache_path):
    with open(cache_path, "rb") as f:
        cached_response = f.read()
    client_socket.sendall(cached_response)
    return
```

- 이슈: 처음에는 cache miss일 때 origin에서 받아온 응답을 파일에 저장하는 코드를 먼저 짰는데, cache hit 검사를 origin fetch 뒤에 넣어버려서 "이미 있는데 또 가져오는" 상황이 됐다. hit 검사가 반드시 fetch 앞에 와야 한다는 게 proxy의 기본 흐름이었다.
- 판단: 분기 순서를 `hit 검사 → miss면 fetch → 저장 → 전달`로 고정했다.

### Session 5

- 목표: 오류 경계를 정리하고 전체를 검증한다.
- 진행: GET이 아닌 요청 → `400 Bad Request`, origin 연결 실패 → `502 Bad Gateway`, origin timeout → `504 Gateway Timeout`으로 나눴다.
- 이슈: `socket.gaierror`(DNS 실패)와 `ConnectionRefusedError`를 처음에 각각 처리했는데, 둘 다 "origin에 닿을 수 없다"는 같은 의미라서 502로 묶는 편이 깔끔했다.
- 검증:

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem run-solution
[INFO] Proxy server started on port 8888

$ curl -x http://localhost:8888 http://www.example.com/
<!doctype html>...

$ curl -x http://localhost:8888 http://www.example.com/
[HIT]  http://www.example.com/ — served from cache

$ make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test
✓ Proxy forwards GET request to origin
✓ Same URL served from cache on second request
✓ Non-GET request returns 400
✓ Unreachable origin returns 502
All tests passed!
```

```bash
$ cd study/01-Application-Protocols-and-Sockets/web-proxy/python/tests
$ python3 -m pytest test_web_proxy.py -v
===== 5 passed =====
```

- 정리:
  - 이 과제에서 가장 중요한 전환점은 "proxy는 서버이자 클라이언트"라는 인식이었다. Web Server에서는 `accept()` → `handle()` → `close()`였지만, proxy는 그 안에서 origin으로 `connect()` → `sendall()` → `recv()` → `close()`를 한 번 더 한다. 소켓이 두 겹이다.
  - URL parsing이 전체 파이프라인의 입구이고, cache hit 검사가 성능의 핵심이고, error 코드가 proxy의 책임 경계를 보여 준다. 이 세 가지가 이 프로젝트의 뼈대였다.
  - 다음 트랙은 Reliable Transport — 이제 응용 계층을 떠나 전송 계층의 신뢰성을 직접 구현한다.
