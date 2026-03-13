# Web Server evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 실행 표면과 entrypoint를 먼저 고정하기

- 당시 목표: `Web Server`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/web-server/problem/README.md`, `study/01-Application-Protocols-and-Sockets/web-server/problem/Makefile`, `study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py`
- 무슨 판단을 했는가: 문제 설명보다 실행 표면을 먼저 잡아야 뒤 설명이 흔들리지 않는다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-server/problem help
  run-server         Start the skeleton web server on port $(PORT)
  run-solution       Start the solution web server on port $(PORT)
  test               Run the test script with a temporary solution server
  request            Send a single test GET request
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 이 트랙의 출발점으로, 연결 수립부터 요청 파싱, 파일 읽기, 응답 생성, 연결 종료까지 서버의 기본 생애주기를 가장 짧은 경로로 경험하게 합니다.
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py`의 `def main`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. 요청 파싱과 200/404 분기를 한 흐름으로 묶기

- 당시 목표: `TCP 소켓과 HTTP/1.1 응답 조합으로 정적 파일 서버를 구현하는 파일럿 과제입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py`
- 무슨 판단을 했는가: 중심 규칙은 넓게 흩어져 있지 않고, 실제 분기나 frame evidence가 모이는 지점에 있다고 봤다.
- 실행한 CLI:

```bash
$ rg -n -e 'def handle_client' -e 'def get_content_type' -e 'def send_request' 'study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py' 'study/01-Application-Protocols-and-Sockets/web-server/python/tests/test_web_server.py'
study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py:40:def get_content_type(filename: str) -> str:
study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py:53:def handle_client(connection_socket: socket.socket, address: tuple) -> None:
study/01-Application-Protocols-and-Sockets/web-server/python/tests/test_web_server.py:23:def send_request(path: str) -> tuple[int, str]:
```
- 검증 신호:
  - 이 출력만으로도 `def handle_client` 주변이 설명의 중심축이라는 점이 드러난다.
  - 정적 파일 서빙과 `Content-Type` 결정
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py`의 `def handle_client`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. 테스트와 남은 범위를 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/web-server/python/tests/test_web_server.py`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 검증 출력이 좋게 나와도 README limitation을 그대로 남겨야 범위가 정확해진다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-server/problem test
TEST: GET /hello.html returns 200              [PASS]
TEST: GET /nonexistent returns 404             [PASS]
TEST: Body contains HTML content               [PASS]
 Results: 3 passed, 0 failed
```
- 검증 신호:
  - `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - path traversal 방어는 아직 구현하지 않았습니다.
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/web-server/python/tests/test_web_server.py`의 `def test_200_ok_for_existing_file`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
