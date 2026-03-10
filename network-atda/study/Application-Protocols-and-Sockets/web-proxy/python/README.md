# Python 구현 안내

    이 디렉터리는 `Web Proxy`의 공개 구현을 담습니다. 현재 저장소의 canonical 검증을 통과하는 범위를 기준으로 코드를 읽을 수 있게 정리합니다.

    ## 어디서부터 읽으면 좋은가

    1. `python/src/web_proxy.py` - 핵심 구현 진입점입니다.
2. `python/tests/test_web_proxy.py` - 검증 의도와 보조 테스트를 확인합니다.

    ## 기준 명령

    - 실행: `make -C study/Application-Protocols-and-Sockets/web-proxy/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/web-proxy/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

    ## 현재 범위

    클라이언트 요청을 중계하고 파일 기반 캐시로 재사용하는 간단한 HTTP 프록시 구현입니다.

    ## 남은 약점

    - `Cache-Control`이나 TTL 기반 만료 정책은 없습니다.
- `HTTPS CONNECT`는 지원하지 않습니다.
- 캐시 디렉터리 동시성 제어는 단순한 수준에 머뭅니다.
