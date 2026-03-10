# Python 구현 안내

    이 디렉터리는 `SMTP Client`의 공개 구현을 담습니다. 현재 저장소의 canonical 검증을 통과하는 범위를 기준으로 코드를 읽을 수 있게 정리합니다.

    ## 어디서부터 읽으면 좋은가

    1. `python/src/smtp_client.py` - 핵심 구현 진입점입니다.
2. `python/tests/test_smtp_client.py` - 검증 의도와 보조 테스트를 확인합니다.

    ## 기준 명령

    - 실행: `make -C study/Application-Protocols-and-Sockets/smtp-client/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/smtp-client/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

    ## 현재 범위

    텍스트 기반 명령-응답 프로토콜을 TCP 위에서 직접 수행하는 메일 클라이언트 과제입니다.

    ## 남은 약점

    - `STARTTLS`는 구현하지 않았습니다.
- `AUTH LOGIN`은 구현하지 않았습니다.
- 외부 SMTP 서버 정책과의 차이는 검증하지 않았습니다.
