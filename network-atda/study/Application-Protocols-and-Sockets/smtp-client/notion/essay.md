# SMTP Client — 메일 한 통을 소켓으로 보내기까지

## 웹 서버와 다른 종류의 프로토콜

웹 서버 과제에서는 HTTP를 다뤘다. 클라이언트가 한 줄 요청을 보내면 서버가 파일을 돌려주는, 비교적 단순한 요청-응답 구조였다.

SMTP는 달랐다. 메일 한 통을 보내려면 클라이언트와 서버가 **여러 번 대화를 주고받아야** 한다. "인사 → 발신자 → 수신자 → 데이터 시작 → 본문 → 종료" 순서를 정확히 밟아야 하고, 각 단계마다 서버가 3자리 숫자로 "알겠다" 혹은 "안 된다"를 응답한다. 한 단계라도 빠뜨리면 메일이 전송되지 않는다.

이 과제의 제약은 명확했다: 파이썬의 `smtplib`는 쓸 수 없다. TCP 소켓 위에서 SMTP 명령어를 문자열로 직접 보내고, 응답 코드를 직접 파싱해야 한다.

## SMTP 대화의 구조

SMTP 대화는 이렇게 진행된다:

```
서버: 220 smtp.example.com ESMTP ready      (연결하면 인사를 받음)
클라: HELO myhost                            → 서버: 250 Hello
클라: MAIL FROM:<alice@example.com>          → 서버: 250 OK
클라: RCPT TO:<bob@example.com>              → 서버: 250 OK
클라: DATA                                   → 서버: 354 (본문 보내라)
클라: (헤더 + 본문 + 마침표 줄)                → 서버: 250 OK
클라: QUIT                                   → 서버: 221 Bye
```

이 순서를 코드로 옮기면 `send_command()` → `recv_reply()` → `check_reply()` 반복이다.

핵심은 **매 단계에서 응답 코드를 검사하는 것**이다. 서버가 `250`을 보내야 다음 단계로 넘어가고, 다른 코드가 오면 즉시 실패로 처리한다. 이렇게 만들면 "어디서 막혔는지"가 곧바로 드러난다.

## CRLF와 DATA 종료 구분자

SMTP에서 모든 명령은 `\r\n`(CRLF)으로 끝나야 한다. `\n`만 보내면 일부 서버는 명령을 인식하지 못한다.

```python
sock.sendall(f"{command}\r\n".encode())
```

더 까다로운 건 DATA 구간의 종료 방식이다. 본문 전송이 끝났음을 알리려면 **줄 바꿈 후 마침표 하나만 있는 줄**을 보내야 한다:

```
\r\n.\r\n
```

이 규약을 몰랐을 때 처음 겪은 현상은, DATA 명령 이후 서버가 아무 응답을 하지 않는 것이었다. 서버가 아직 본문이 끝나지 않았다고 생각하고 계속 기다리고 있었던 거다. 마침표 줄을 보내고 나서야 `250`이 돌아왔다.

## 응답 코드 검증: fail-fast 패턴

```python
def check_reply(reply: str, expected_code: str) -> None:
    if not reply.startswith(expected_code):
        raise RuntimeError(f"Expected {expected_code}, got: {reply.strip()}")
```

이 작은 함수가 디버깅 시간을 크게 줄여줬다. SMTP 대화가 6단계인데, 만약 응답 코드를 검사하지 않고 끝까지 진행하면 "메일이 안 갔다"만 알 뿐 **어느 단계에서 실패했는지** 알 수 없다.

`check_reply()`를 매 단계에 끼워넣으면, 발신자 주소가 거부됐는지(`550`), 서버 인증이 필요한지(`530`) 응답 코드만 보고 즉시 파악할 수 있다.

## 로컬 테스트: 디버깅 SMTP 서버

실제 Gmail이나 회사 메일 서버에 테스트할 수는 없다. 인증이 필요하고, rate limit이 있고, 실수로 메일이 실제 전송될 수 있다.

파이썬 표준 라이브러리에는 디버깅용 SMTP 서버가 내장되어 있다:

```bash
python3 -m smtpd -n -c DebuggingServer localhost:1025
```

이 서버는 받은 메일을 실제로 보내지 않고 터미널에 출력만 해준다. 하지만 이 모듈은 deprecated 경고가 뜨므로, 대안으로 `aiosmtpd`를 쓸 수도 있다:

```bash
pip install aiosmtpd
python3 -m aiosmtpd -n -l localhost:1025
```

이 과제에서는 자체 mock 서버(`problem/script/mock_smtp_server.py`)가 제공되어, 외부 의존 없이 테스트할 수 있었다.

## 실제 전송 흐름

클라이언트를 실행하면 이런 출력이 나온다:

```bash
python3 smtp_client.py localhost 1025 alice@example.com bob@example.com
```

```
Connecting to localhost:1025 ...

S: 220 localhost Mock SMTP Service Ready
C: HELO myhostname
S: 250 Hello
C: MAIL FROM:<alice@example.com>
S: 250 OK
C: RCPT TO:<bob@example.com>
S: 250 OK
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: (sending message body — 87 bytes)
S: 250 Message accepted for delivery
C: QUIT
S: 221 Bye

Email sent successfully!
```

`C:`는 클라이언트가 보낸 것, `S:`는 서버 응답이다. 이 로그 형식이 SMTP 프로토콜의 다단계 대화를 시각적으로 잘 드러내줬다.

## envelope vs header 주소

구현 과정에서 하나 알게 된 개념이 있었다. `MAIL FROM`과 `RCPT TO`에 들어가는 주소(envelope 주소)와, DATA 본문 안의 `From:`, `To:` 헤더는 별개라는 것이다.

envelope 주소는 메일 라우팅에 쓰이고, 헤더 주소는 수신자의 메일 클라이언트에 표시된다. 이 둘이 달라도 기술적으로는 유효하다(스팸에서 이걸 악용한다). 이 과제에서는 둘을 같게 설정했지만, 이 구분을 안다는 것 자체가 프로토콜을 직접 다뤄봤기 때문에 가능한 이해였다.

## 에러 처리와 종료

예외가 발생하면 RuntimeError 메시지에 서버의 응답 코드가 포함된다:

```python
try:
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])
except RuntimeError as e:
    print(f"\n[ERROR] SMTP dialogue failed: {e}")
    sys.exit(1)
```

소켓 타임아웃도 10초로 설정해두었다. 서버가 응답하지 않으면 무한 대기하지 않고 예외를 발생시킨다.

## 이 과제에서 가져간 것

HTTP가 "요청 한 번, 응답 한 번"이라면, SMTP는 "요청 여섯 번, 응답 여섯 번"이다. 같은 TCP 연결 위에서 상태 기계(state machine)처럼 동작하는 프로토콜을 직접 구현해봤다.

이 경험은 나중에 게임 서버의 TCP 제어 채널을 설계할 때 직접적으로 도움이 됐다. LOGIN → CREATE_ROOM → READY 같은 다단계 프로토콜도 결국 SMTP와 같은 "명령-응답 코드" 패턴이었으니까.

---

> **학습 키워드**: SMTP 프로토콜, 3자리 응답 코드, CRLF, DATA 종료 구분자(`.`), fail-fast, envelope vs header 주소, mock 서버 테스트