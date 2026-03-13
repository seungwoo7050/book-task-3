# SMTP Client evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 실행 표면과 entrypoint를 먼저 고정하기

- 당시 목표: `SMTP Client`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/smtp-client/problem/README.md`, `study/01-Application-Protocols-and-Sockets/smtp-client/problem/Makefile`, `study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py`
- 무슨 판단을 했는가: 처음엔 코드를 바로 읽기보다, 공개 진입점과 성공 기준부터 고정하는 편이 안전하다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem help
  run-debug-server       Start a local SMTP debug server on port $(PORT)
  run-client             Run the skeleton SMTP client
  run-solution           Run the solution SMTP client
  test                   Run the test script with a temporary SMTP mock server
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: HTTP와 비슷하게 텍스트 명령을 쓰지만 상태 전이가 더 길고 명확해서, 응용 계층 프로토콜의 단계적 흐름을 연습하기 좋습니다.
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py`의 `def recv_reply`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. 명령 전송과 응답 확인을 대화 단계에 맞춰 정리하기

- 당시 목표: `텍스트 기반 명령-응답 프로토콜을 TCP 위에서 직접 수행하는 메일 클라이언트 과제입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py`
- 무슨 판단을 했는가: 핵심 설명은 한두 함수나 section에 가장 진하게 모여 있을 거라고 봤다.
- 실행한 CLI:

```bash
$ rg -n -e 'def recv_reply' -e 'def send_command' -e 'def check_reply' -e 'client_socket.sendall(message.encode())' 'study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py' 'study/01-Application-Protocols-and-Sockets/smtp-client/python/tests/test_smtp_client.py'
study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py:17:def recv_reply(sock: socket.socket) -> str:
study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py:31:def send_command(sock: socket.socket, command: str) -> str:
study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py:46:def check_reply(reply: str, expected_code: str) -> None:
```
- 검증 신호:
  - 이 출력만으로도 `def send_command` 주변이 설명의 중심축이라는 점이 드러난다.
  - `CRLF`와 `DATA` 종료 구분자 처리
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py`의 `def send_command`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. 테스트와 남은 범위를 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/smtp-client/python/tests/test_smtp_client.py`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 마지막에는 성공 신호와 한계를 같이 적어야 글이 매끈한 회고문으로 변하지 않는다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test
TEST: Client completes SMTP dialogue           [PASS]
TEST: Output indicates success                 [PASS]
TEST: Output shows SMTP dialogue               [PASS]
 Results: 3 passed, 0 failed
```
- 검증 신호:
  - `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - `STARTTLS`는 구현하지 않았습니다.
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/smtp-client/python/tests/test_smtp_client.py`의 `def test_full_smtp_dialogue`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
