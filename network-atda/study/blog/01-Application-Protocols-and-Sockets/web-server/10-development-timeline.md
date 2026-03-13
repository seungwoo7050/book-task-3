# Web Server development timeline

`Web Server`를 읽을 때 먼저 잡아야 하는 것은 기능 목록이 아니라, 어디서부터 구현이나 분석이 무거워졌는가이다.

그래서 이 문서는 문제 문서, 핵심 파일, 테스트, CLI 출력만 남기고 나머지 군더더기는 걷어 냈다.

## 구현 순서 한눈에 보기

1. `study/01-Application-Protocols-and-Sockets/web-server/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 실행 표면과 entrypoint를 먼저 고정하기

이 단계에서는 구현 세부로 바로 내려가지 않았다. 먼저 어떤 파일이 진입점이고 어떤 명령이 검증 기준인지 고정하는 일이 더 급했다.

- 당시 목표: `Web Server`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `def main`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: HTTP 요청 라인의 최소 파싱 규칙

핵심 코드/trace:

```python
def main(port: int = 6789) -> None:
    """multi-threaded web server를 시작한다.

    Args:
        port: listen할 TCP port 번호.
    """
    # TCP server socket을 준비한다.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
```

왜 이 코드가 중요했는가:

문제 사양을 읽은 뒤 바로 이 지점으로 내려오면, 말로 적힌 요구가 실제 파일 구조와 어떻게 만나는지 곧바로 보인다.

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-server/problem help
  run-server         Start the skeleton web server on port $(PORT)
  run-solution       Start the solution web server on port $(PORT)
  test               Run the test script with a temporary solution server
  request            Send a single test GET request
```

## 2. 요청 파싱과 200/404 분기를 한 흐름으로 묶기

중간 단계의 핵심은 '무엇을 만들었나'보다 '어느 줄에서 규칙이 드러나는가'를 잡는 일이었다.

- 당시 목표: `TCP 소켓과 HTTP/1.1 응답 조합으로 정적 파일 서버를 구현하는 파일럿 과제입니다.`를 실제 근거에 붙인다.
- 실제 진행: `def handle_client` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: 정적 파일 서빙과 `Content-Type` 결정

핵심 코드/trace:

```python
def handle_client(connection_socket: socket.socket, address: tuple) -> None:
    """연결된 client의 단일 HTTP 요청을 처리한다.

    Args:
        connection_socket: client와 연결된 TCP socket.
        address: client를 식별하는 `(host, port)` tuple.
    """
    try:
        # HTTP 요청을 최대 4 KB까지 읽는다.
        message = connection_socket.recv(4096).decode()
```

왜 이 코드가 중요했는가:

핵심은 함수 이름 자체가 아니라, 이 줄 주변에서 어떤 입력이 어떤 결과로 바뀌는지가 한 번에 드러난다는 점이다.

CLI:

```bash
$ rg -n -e 'def handle_client' -e 'def get_content_type' -e 'def send_request' 'study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py' 'study/01-Application-Protocols-and-Sockets/web-server/python/tests/test_web_server.py'
study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py:40:def get_content_type(filename: str) -> str:
study/01-Application-Protocols-and-Sockets/web-server/python/src/web_server.py:53:def handle_client(connection_socket: socket.socket, address: tuple) -> None:
study/01-Application-Protocols-and-Sockets/web-server/python/tests/test_web_server.py:23:def send_request(path: str) -> tuple[int, str]:
```

## 3. 테스트와 남은 범위를 정리하기

마지막 단계에서는 단순히 테스트가 통과했다는 사실만 적지 않으려고 했다. 어디까지 확인됐고 무엇이 아직 범위 밖인지 같이 남겨야 글이 정직해진다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test`를 다시 실행하고, `def test_200_ok_for_existing_file`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: 404 응답 생성과 연결 종료 시점

핵심 코드/trace:

```python
def test_200_ok_for_existing_file(self):
        """존재하는 파일에는 200 응답이 와야 한다."""
        status, body = send_request("/hello.html")
        assert status == 200

    def test_response_contains_html(self):
        """응답 body에는 HTML 내용이 포함되어야 한다."""
        status, body = send_request("/hello.html")
        assert "<html" in body.lower()
        assert "hello" in body.lower()
```

왜 이 코드가 중요했는가:

마지막에 이 파일을 남겨 두는 이유는, 이 프로젝트가 실제로 무엇을 통과해야 끝나는지 가장 직접적으로 보여 주기 때문이다.

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/web-server/problem test
TEST: GET /hello.html returns 200              [PASS]
TEST: GET /nonexistent returns 404             [PASS]
TEST: Body contains HTML content               [PASS]
 Results: 3 passed, 0 failed
```

## 남은 경계

- path traversal 방어는 아직 구현하지 않았습니다.
- 스레드 수 제한이나 thread pool은 없습니다.
- GET 외 메서드는 지원하지 않습니다.
