# SMTP Client development timeline

`SMTP Client`의 핵심은 완성 결과보다, 어떤 순서로 범위를 좁히고 검증까지 닫았는가에 있다.

본문은 코드나 trace를 한 번에 길게 복붙하지 않고, 판단이 바뀐 지점만 골라 이어 붙인다.

## 구현 순서 한눈에 보기

1. `study/01-Application-Protocols-and-Sockets/smtp-client/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 실행 표면과 entrypoint를 먼저 고정하기

처음에는 `SMTP Client`를 어디서부터 설명해야 할지부터 정리해야 했다. 그래서 문제 문서와 `make help` 출력으로 공개된 실행 표면을 먼저 잡았다.

- 당시 목표: `SMTP Client`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `def recv_reply`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: 3자리 SMTP 응답 코드에 따른 제어 흐름

핵심 코드/trace:

```python
def recv_reply(sock: socket.socket) -> str:
    """SMTP server의 응답을 읽어 반환한다.

    Args:
        sock: SMTP server에 연결된 TCP socket.

    Returns:
        decode된 server 응답 문자열.
    """
    reply = sock.recv(4096).decode()
```

왜 이 코드가 중요했는가:

이 부분을 먼저 보여 주는 이유는, 이 프로젝트의 진입점과 실행 표면이 여기서 한 번에 정리되기 때문이다.

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem help
  run-debug-server       Start a local SMTP debug server on port $(PORT)
  run-client             Run the skeleton SMTP client
  run-solution           Run the solution SMTP client
  test                   Run the test script with a temporary SMTP mock server
```

## 2. 명령 전송과 응답 확인을 대화 단계에 맞춰 정리하기

이제부터는 설명을 추상적으로 유지할 수 없었다. 실제 분기나 frame evidence가 모이는 지점을 찾아야 글이 살아났다.

- 당시 목표: `텍스트 기반 명령-응답 프로토콜을 TCP 위에서 직접 수행하는 메일 클라이언트 과제입니다.`를 실제 근거에 붙인다.
- 실제 진행: `def send_command` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: `CRLF`와 `DATA` 종료 구분자 처리

핵심 코드/trace:

```python
def send_command(sock: socket.socket, command: str) -> str:
    """SMTP command를 보내고 server 응답을 반환한다.

    Args:
        sock: SMTP server에 연결된 TCP socket.
        command: CRLF를 제외한 SMTP command 문자열.

    Returns:
        decode된 server 응답 문자열.
    """
```

왜 이 코드가 중요했는가:

여기서는 구현이나 분석의 무게중심이 바뀐다. 그래서 파일 전체보다 이 좁은 구간을 먼저 보는 편이 훨씬 정확하다.

CLI:

```bash
$ rg -n -e 'def recv_reply' -e 'def send_command' -e 'def check_reply' -e 'client_socket.sendall(message.encode())' 'study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py' 'study/01-Application-Protocols-and-Sockets/smtp-client/python/tests/test_smtp_client.py'
study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py:17:def recv_reply(sock: socket.socket) -> str:
study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py:31:def send_command(sock: socket.socket, command: str) -> str:
study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py:46:def check_reply(reply: str, expected_code: str) -> None:
```

## 3. 테스트와 남은 범위를 정리하기

끝맺음에서 중요한 건 멋진 회고가 아니라 경계선이다. 통과한 범위와 남겨 둔 범위를 같은 문맥 안에 두려고 했다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`를 다시 실행하고, `def test_full_smtp_dialogue`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: envelope 주소와 헤더 주소의 차이

핵심 코드/trace:

```python
def test_full_smtp_dialogue(self):
        """전체 SMTP dialogue가 정상적으로 완료되어야 한다."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((HOST, PORT))
            greeting = sock.recv(1024).decode()
            assert greeting.startswith("220")

            sock.sendall(b"HELO localhost\r\n")
```

왜 이 코드가 중요했는가:

최종 단계에서 중요한 것은 '잘 됐다'가 아니라 '무엇을 확인했고 무엇은 아직 안 했다'인데, 그 기준이 이 파일에 가장 잘 남아 있다.

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test
TEST: Client completes SMTP dialogue           [PASS]
TEST: Output indicates success                 [PASS]
TEST: Output shows SMTP dialogue               [PASS]
 Results: 3 passed, 0 failed
```

## 남은 경계

- `STARTTLS`는 구현하지 않았습니다.
- `AUTH LOGIN`은 구현하지 않았습니다.
- 외부 SMTP 서버 정책과의 차이는 검증하지 않았습니다.
