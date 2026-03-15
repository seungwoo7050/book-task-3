# SMTP Client 시리즈 맵

이 lab의 중심 질문은 단순하다. HTTP처럼 사람이 읽을 수 있는 텍스트 프로토콜을, 더 긴 상태 전이를 가진 SMTP로 옮기면 클라이언트 코드가 어떤 책임을 직접 떠안게 되는가. 현재 구현은 `recv_reply()`, `send_command()`, `check_reply()` 세 함수로 그 책임을 분리하고, `main()`에서 greeting부터 `QUIT`까지 대화를 끝까지 조립한다.

## 이 lab를 읽는 질문

- 왜 SMTP에서는 각 단계의 응답 코드를 계속 검사해야 하는가
- `DATA` 단계는 앞선 명령 단계와 무엇이 다른가
- envelope 주소와 헤더 주소가 코드에서 어떻게 함께 나타나는가

## 이번에 사용한 근거

- `problem/README.md`
- `python/src/smtp_client.py`
- `python/tests/test_smtp_client.py`
- `docs/README.md`
- `make -C .../problem test` 재실행 결과

## 이번 재실행에서 고정한 사실

- 연결 직후 `220` greeting을 먼저 읽는다.
- `HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT` 단계마다 기대 코드가 다르다.
- 본문 전송은 명령 단위가 아니라 헤더+본문+종료 마침표까지 한 번에 보낸다.
- 테스트는 전체 dialogue 성공, success 출력, dialogue 출력 노출까지 확인한다.
