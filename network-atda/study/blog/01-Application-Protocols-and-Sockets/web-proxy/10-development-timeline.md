# Web Proxy development timeline

`Web Proxy`의 핵심은 완성 결과보다, 어떤 순서로 범위를 좁히고 검증까지 닫았는가에 있다.

본문은 코드나 trace를 한 번에 길게 복붙하지 않고, 판단이 바뀐 지점만 골라 이어 붙인다.

## 구현 순서 한눈에 보기

1. `study/01-Application-Protocols-and-Sockets/web-proxy/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 실행 표면과 entrypoint를 먼저 고정하기

처음에는 `Web Proxy`를 어디서부터 설명해야 할지부터 정리해야 했다. 그래서 문제 문서와 `make help` 출력으로 공개된 실행 표면을 먼저 잡았다.

- 당시 목표: `Web Proxy`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `def parse_url`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: 절대 URL 파싱과 origin request 재구성

핵심 코드/trace:

```python
def parse_url(url: str) -> tuple[str, int, str]:
    """절대 HTTP URL을 `(hostname, port, path)`로 분해한다.

    Args:
        url: 절대 HTTP URL.

    Returns:
        `(hostname, port, path)` tuple.
    """
    # `http://` scheme을 제거한다.
```

왜 이 코드가 중요했는가:

이 부분을 먼저 보여 주는 이유는, 이 프로젝트의 진입점과 실행 표면이 여기서 한 번에 정리되기 때문이다.

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem help
  run-proxy          Start the skeleton proxy on port $(PORT)
  run-solution       Start the solution proxy on port $(PORT)
  test               Run the test script with a temporary solution proxy
  request            Send a test request through the proxy
```

## 2. URL 해석과 cache/origin 분기를 한 요청 흐름으로 묶기

이제부터는 설명을 추상적으로 유지할 수 없었다. 실제 분기나 frame evidence가 모이는 지점을 찾아야 글이 살아났다.

- 당시 목표: `클라이언트 요청을 중계하고 파일 기반 캐시로 재사용하는 간단한 HTTP 프록시 구현입니다.`를 실제 근거에 붙인다.
- 실제 진행: `def handle_client` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: 프록시의 server/client 이중 역할

핵심 코드/trace:

```python
def handle_client(client_socket: socket.socket, address: tuple) -> None:
    """client의 단일 proxy 요청을 처리한다.

    Args:
        client_socket: client와 연결된 TCP socket.
        address: client의 `(host, port)` tuple.
    """
    try:
        # client의 HTTP 요청을 읽는다.
        request = client_socket.recv(BUFFER_SIZE).decode(errors="replace")
```

왜 이 코드가 중요했는가:

여기서는 구현이나 분석의 무게중심이 바뀐다. 그래서 파일 전체보다 이 좁은 구간을 먼저 보는 편이 훨씬 정확하다.

CLI:

```bash
$ rg -n -e 'def parse_url' -e 'def fetch_from_origin' -e 'def handle_client' -e 'cache_path = get_cache_path(url)' 'study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py' 'study/01-Application-Protocols-and-Sockets/web-proxy/python/tests/test_web_proxy.py'
study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py:23:def parse_url(url: str) -> tuple[str, int, str]:
study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py:67:def fetch_from_origin(hostname: str, port: int, path: str) -> bytes:
study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py:105:def handle_client(client_socket: socket.socket, address: tuple) -> None:
```

## 3. 테스트와 남은 범위를 정리하기

끝맺음에서 중요한 건 멋진 회고가 아니라 경계선이다. 통과한 범위와 남겨 둔 범위를 같은 문맥 안에 두려고 했다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`를 다시 실행하고, `def test_same_url_same_key`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: MD5 기반 캐시 키 설계

핵심 코드/trace:

```python
def test_same_url_same_key(self):
        p1 = get_cache_path("http://example.com/a")
        p2 = get_cache_path("http://example.com/a")
        assert p1 == p2

    def test_different_url_different_key(self):
        p1 = get_cache_path("http://example.com/a")
        p2 = get_cache_path("http://example.com/b")
        assert p1 != p2
```

왜 이 코드가 중요했는가:

최종 단계에서 중요한 것은 '잘 됐다'가 아니라 '무엇을 확인했고 무엇은 아직 안 했다'인데, 그 기준이 이 파일에 가장 잘 남아 있다.

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test
TEST: Fetch http://127.0.0.1:18080/            [PASS]
TEST: Second fetch (cache check)               [PASS]
TEST: Response body is non-empty               [PASS]
 Results: 3 passed, 0 failed
```

## 남은 경계

- `Cache-Control`이나 TTL 기반 만료 정책은 없습니다.
- `HTTPS CONNECT`는 지원하지 않습니다.
- 캐시 디렉터리 동시성 제어는 단순한 수준에 머뭅니다.
