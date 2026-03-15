# SMTP Client Blog

이 문서 묶음은 `smtp-client`를 "메일을 보낸다"보다 "텍스트 명령-응답 프로토콜을 TCP 위에서 어디까지 직접 책임지는가"라는 질문으로 다시 읽는다. 현재 구현은 `smtplib` 없이 greeting 수신, `HELO -> MAIL FROM -> RCPT TO -> DATA -> QUIT` 순서를 끝까지 수행하고, 각 단계에서 3자리 응답 코드를 직접 검사한다. 따라서 이 lab의 핵심은 메일 기능보다 프로토콜 대화의 단계성과 fail-fast 처리에 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/01-Application-Protocols-and-Sockets/smtp-client/problem/README.md`
- 구현 경계: `README.md`, `python/README.md`, `python/src/smtp_client.py`
- 테스트 근거: `python/tests/test_smtp_client.py`
- 개념 문서: `docs/README.md`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/01-Application-Protocols-and-Sockets/smtp-client/problem test`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/01-Application-Protocols-and-Sockets/smtp-client/problem test`
- 결과: `3 passed, 0 failed`

## 지금 남기는 한계

- `STARTTLS` 미구현
- `AUTH LOGIN` 미구현
- 외부 SMTP 서버 정책 차이 미검증
