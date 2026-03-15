# SMTP Client Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/01-Application-Protocols-and-Sockets/smtp-client/problem/README.md`
- 구현 엔트리: `study/01-Application-Protocols-and-Sockets/smtp-client/python/src/smtp_client.py`
- 보조 테스트: `study/01-Application-Protocols-and-Sockets/smtp-client/python/tests/test_smtp_client.py`
- 개념 가이드: `study/01-Application-Protocols-and-Sockets/smtp-client/docs/README.md`

## 핵심 코드 근거

- `recv_reply()`: 서버 응답을 읽고 `S:` prefix로 출력한다.
- `send_command()`: 명령을 `CRLF`와 함께 보내고 바로 응답을 읽는다.
- `check_reply()`: 기대 코드와 다르면 `RuntimeError`를 던진다.
- `message` 구성: `From/To/Subject` 헤더와 본문, 마지막 `.\r\n` 종료자를 포함한다.

## 테스트 근거

`make -C network-atda/study/01-Application-Protocols-and-Sockets/smtp-client/problem test`

결과:

- `Client completes SMTP dialogue` pass
- `Output indicates success` pass
- `Output shows SMTP dialogue` pass

## 이번에 고정한 해석

- 이 lab의 핵심은 메일 전송 성공보다 단계별 응답 코드 검증이다.
- `DATA`는 일반 명령처럼 한 줄 보내고 끝나는 단계가 아니라 메시지 전체 전송 구간이다.
- 구현은 fail-fast 구조라 예상치 못한 응답이 오면 즉시 종료한다.
