# Web Proxy evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 실행 표면과 entrypoint를 먼저 고정하기

- 당시 목표: `Web Proxy`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/web-proxy/problem/README.md`, `study/01-Application-Protocols-and-Sockets/web-proxy/problem/Makefile`, `study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py`
- 무슨 판단을 했는가: 처음엔 코드를 바로 읽기보다, 공개 진입점과 성공 기준부터 고정하는 편이 안전하다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem help
  run-proxy          Start the skeleton proxy on port $(PORT)
  run-solution       Start the solution proxy on port $(PORT)
  test               Run the test script with a temporary solution proxy
  request            Send a test request through the proxy
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 클라이언트와 원 서버의 역할을 한 프로그램 안에서 동시에 다루게 만들어, 앞선 소켓 과제보다 한 단계 복잡한 중개자 구조를 연습하게 합니다.
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py`의 `def parse_url`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. URL 해석과 cache/origin 분기를 한 요청 흐름으로 묶기

- 당시 목표: `클라이언트 요청을 중계하고 파일 기반 캐시로 재사용하는 간단한 HTTP 프록시 구현입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py`
- 무슨 판단을 했는가: 핵심 설명은 한두 함수나 section에 가장 진하게 모여 있을 거라고 봤다.
- 실행한 CLI:

```bash
$ rg -n -e 'def parse_url' -e 'def fetch_from_origin' -e 'def handle_client' -e 'cache_path = get_cache_path(url)' 'study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py' 'study/01-Application-Protocols-and-Sockets/web-proxy/python/tests/test_web_proxy.py'
study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py:23:def parse_url(url: str) -> tuple[str, int, str]:
study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py:67:def fetch_from_origin(hostname: str, port: int, path: str) -> bytes:
study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py:105:def handle_client(client_socket: socket.socket, address: tuple) -> None:
```
- 검증 신호:
  - 이 출력만으로도 `def handle_client` 주변이 설명의 중심축이라는 점이 드러난다.
  - 프록시의 server/client 이중 역할
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py`의 `def handle_client`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. 테스트와 남은 범위를 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/web-proxy/python/tests/test_web_proxy.py`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 마지막에는 성공 신호와 한계를 같이 적어야 글이 매끈한 회고문으로 변하지 않는다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test
TEST: Fetch http://127.0.0.1:18080/            [PASS]
TEST: Second fetch (cache check)               [PASS]
TEST: Response body is non-empty               [PASS]
 Results: 3 passed, 0 failed
```
- 검증 신호:
  - `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - `Cache-Control`이나 TTL 기반 만료 정책은 없습니다.
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/web-proxy/python/tests/test_web_proxy.py`의 `def test_same_url_same_key`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
