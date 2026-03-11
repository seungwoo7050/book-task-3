# Python 구현 안내

## 이 폴더의 역할
이 디렉터리는 `SMTP Client`의 공개 구현을 담습니다. `problem/`의 제공 자료와 분리된 사용자 작성 답안을 이 폴더에서 확인합니다.

## 먼저 볼 파일
- `python/src/smtp_client.py` - 핵심 구현 진입점입니다.
- `python/tests/test_smtp_client.py` - 검증 의도와 보조 테스트를 확인합니다.

## 기준 명령
- 검증: `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`

## 현재 범위
텍스트 기반 명령-응답 프로토콜을 TCP 위에서 직접 수행하는 메일 클라이언트 과제입니다.

## 남은 약점
- `STARTTLS`는 구현하지 않았습니다.
- `AUTH LOGIN`은 구현하지 않았습니다.
- 외부 SMTP 서버 정책과의 차이는 검증하지 않았습니다.
