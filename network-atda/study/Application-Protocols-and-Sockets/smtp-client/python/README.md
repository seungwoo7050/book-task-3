# Python 구현 안내

이 디렉터리는 `SMTP Client`의 공개 구현을 담는다.

## 구성

- `src/smtp_client.py`
- `tests/test_smtp_client.py`

## 기준 명령

- 실행: `make -C study/Application-Protocols-and-Sockets/smtp-client/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/smtp-client/problem test`

## 구현 메모

- 상태: `verified`
- 현재 범위: 인증과 TLS는 문서에서만 다루고, 공개 구현은 평문 SMTP 대화와 로컬 검증에 집중한다.
- 남은 약점: STARTTLS 미구현
- 남은 약점: AUTH LOGIN 미구현
- 남은 약점: 외부 SMTP 서버와의 정책 차이 미검증
