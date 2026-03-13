# SMTP Client 개발 타임라인

## Day 1

### Session 1

- 목표: HTTP와 SMTP가 코드 수준에서 어떻게 다른지 먼저 잡는다. 둘 다 텍스트 프로토콜인데 왜 SMTP가 더 까다로운지.
- 진행: `problem/script/mock_smtp_server.py`를 먼저 열어 봤다. 이 모의 서버가 `HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT` 각각에 대해 정해진 응답 코드(`220`, `250`, `354`, `250`, `221`)를 보내주는 구조였다.
- 이슈: 당시 의문은 "왜 `HELO`부터 보내야 하지? TCP 연결이 됐으면 바로 DATA 가면 안 되나?"였다. mock 서버를 직접 연결해 보니 `HELO` 없이 `DATA`를 보내면 `503 Bad sequence` 같은 응답이 돌아왔다. SMTP는 단계를 건너뛸 수 없다.

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem run-debug-server
SMTP Debug Server running on localhost:1025
```

### Session 2

- 목표: `send_command()`와 `check_reply()` 두 helper를 먼저 만들어 프로토콜 대화의 뼈대를 잡는다.
- 진행: HTTP에서는 한 번 보내고 한 번 받으면 끝이었는데, SMTP는 매 명령마다 응답 코드를 확인해야 했다. 그래서 "보내고 → 받고 → 확인"을 반복하는 구조가 필요했다.

```py
def send_command(sock: socket.socket, command: str) -> str:
    print(f"C: {command}")
    sock.sendall(f"{command}\r\n".encode())
    return recv_reply(sock)

def check_reply(reply: str, expected_code: str) -> None:
    if not reply.startswith(expected_code):
        raise RuntimeError(f"Expected {expected_code}, got: {reply.strip()}")
```

- 이슈: `check_reply()`를 처음에는 경고 로그만 남기게 만들었는데, 그러면 이전 단계가 실패해도 다음 명령이 나가 버렸다. 서버 쪽에서 "아까 HELO 응답이 잘못됐는데 왜 MAIL FROM이 오지?"라는 상태가 되면 전체 대화가 엉켰다.
- 판단: `RuntimeError`로 즉시 중단하는 fail-fast 방식이 SMTP에는 맞았다. 이 프로토콜은 "한 단계라도 틀리면 나머지가 전부 무의미"하다.

### Session 3

- 목표: 실제 대화 시퀀스를 완성한다 — greeting부터 QUIT까지.
- 진행: mock 서버를 띄워 놓고 한 단계씩 추가하면서 돌렸다.

```bash
$ make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem run-solution
Connecting to localhost:1025 ...

S: 220 localhost SMTP Mock Server Ready
C: HELO woopinbell-macbook
S: 250 Hello woopinbell-macbook
C: MAIL FROM:<alice@example.com>
S: 250 OK
C: RCPT TO:<bob@example.com>
S: 250 OK
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: (sending message body — 127 bytes)
S: 250 OK: Message accepted
C: QUIT
S: 221 Bye

Email sent successfully!
```

- 이슈: 본문 전송에서 가장 헷갈렸던 건 종료 구분자였다. `\r\n.\r\n`이 본문 끝을 알린다는 규칙인데, 처음에 `.\r\n`만 보내고 그 앞에 `\r\n`을 빠뜨렸더니 mock 서버가 본문이 끝나지 않았다고 판단해서 계속 기다렸다.

```py
message = (
    f"From: {sender}\r\n"
    f"To: {recipient}\r\n"
    f"Subject: {subject}\r\n"
    f"\r\n"
    f"{body}\r\n"
    f".\r\n"
)
```

나중에 보니 `body` 마지막에 개행이 있으면 `\r\n.\r\n`이 되고, 없으면 `body.\r\n`이 돼서 구분자로 인식이 안 된다. 이 1바이트가 프로토콜의 성패를 갈랐다.

### Session 4

- 목표: 테스트를 돌려 전체 시퀀스가 안정적인지 확인한다.
- 검증:

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test
Starting SMTP Mock Server on port 1025...
Running SMTP Client...
✓ Connection established (220 greeting)
✓ HELO accepted (250)
✓ MAIL FROM accepted (250)
✓ RCPT TO accepted (250)
✓ DATA entered (354)
✓ Message body accepted (250)
✓ QUIT acknowledged (221)
All tests passed!
```

```bash
$ cd study/01-Application-Protocols-and-Sockets/smtp-client/python/tests
$ python3 -m pytest test_smtp_client.py -v
===== 4 passed =====
```

- 정리:
  - 이 프로젝트에서 가장 중요한 함수는 화려한 게 아니라 `check_reply()`라는 3줄짜리 검사였다. 이게 없으면 대화 전체가 불안정해진다.
  - HTTP는 "요청 한 번 → 응답 한 번"이었지만, SMTP는 "매 단계 허가를 기다리는 상태 머신"이었다. 같은 TCP인데 프로토콜이 부여하는 리듬이 완전히 다르다.
  - `.\r\n` 앞에 `\r\n`이 빠지는 실수는 당시에 한참 헤맸다. 결국 SMTP의 핵심은 wire format의 바이트 하나하나였다.
  - 다음은 Web Proxy — 서버와 클라이언트를 한 프로그램 안에서 동시에 해야 하는 구조다.
