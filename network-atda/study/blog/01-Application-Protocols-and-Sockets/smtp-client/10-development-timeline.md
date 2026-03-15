# SMTP Client 개발 타임라인

이 lab의 흐름은 긴 기능 추가 역사보다, 프로토콜 단계가 어떤 순서로 고정되는지를 따라가는 편이 더 정확하다. 현재 구현을 다시 읽으면 네 번의 전환점이 뚜렷하다.

## 1. 먼저 greeting을 읽는 클라이언트로 출발한다

SMTP는 HTTP처럼 클라이언트가 먼저 말하지 않는다. 서버가 `220` greeting을 먼저 보낸다. 구현도 `connect()` 직후 바로 `recv_reply()`를 호출하고 `check_reply(greeting, "220")`로 문턱을 세운다. 이 한 줄 때문에 이 lab는 단순 request emitter가 아니라 protocol peer가 된다.

## 2. 명령 단계는 `send_command()` + `check_reply()` 조합으로 고정된다

`HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT`는 모두 같은 패턴을 따른다.

- 명령을 `CRLF`와 함께 보낸다.
- 응답을 읽는다.
- 기대 코드인지 검사한다.

이 패턴 덕분에 클라이언트 흐름이 눈으로 읽히고, 예상치 못한 응답은 바로 `RuntimeError`로 끊긴다.

## 3. `DATA` 단계에서 한 줄 명령에서 메시지 전송으로 넘어간다

이 lab에서 가장 중요한 전환점은 `DATA`다. 여기서부터는 단순 command/reply가 아니라 메시지 본문 전체를 보내야 한다. 구현은 `From`, `To`, `Subject` 헤더와 본문, 마지막 `.\r\n` 종료자를 한 문자열로 조립해서 `sendall()`로 전송한다.

즉 이 단계에서 envelope 주소(`MAIL FROM`, `RCPT TO`)와 메시지 헤더 주소(`From`, `To`)가 같은 흐름 안에 같이 나타난다. 문제 README가 이 차이를 간접적으로 드러내고, 구현은 둘 다 명시적으로 보존한다.

## 4. 테스트는 성공 자체보다 dialogue visibility를 함께 고정한다

2026-03-14 재실행한 정식 테스트는 세 가지를 통과시켰다.

- 전체 SMTP dialogue 완료
- success 문구 출력
- `C:`/`S:` 형태의 dialogue 출력

즉 이 lab의 출력은 단순 로그가 아니라 학습 surface다. 사람이 프로토콜 대화를 눈으로 따라갈 수 있게 만드는 것이 현재 구현의 일부다.

## 지금 남는 한계

현재 범위는 분명하다. `STARTTLS`, `AUTH LOGIN`, 외부 SMTP 정책 대응은 없다. 하지만 이 lab의 목적이 본격 메일 클라이언트보다 텍스트 프로토콜 대화를 직접 구현해 보는 데 있다는 점을 생각하면, 지금의 범위는 오히려 적절하다.
