# Python 구현 안내

## 이 폴더의 역할
이 디렉터리는 `Web Proxy`의 공개 구현을 담습니다. `problem/`의 제공 자료와 분리된 사용자 작성 답안을 이 폴더에서 확인합니다.

## 먼저 볼 파일
- `python/src/web_proxy.py` - 핵심 구현 진입점입니다.
- `python/tests/test_web_proxy.py` - 검증 의도와 보조 테스트를 확인합니다.

## 기준 명령
- 검증: `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`

## 현재 범위
클라이언트 요청을 중계하고 파일 기반 캐시로 재사용하는 간단한 HTTP 프록시 구현입니다.

## 남은 약점
- `Cache-Control`이나 TTL 기반 만료 정책은 없습니다.
- `HTTPS CONNECT`는 지원하지 않습니다.
- 캐시 디렉터리 동시성 제어는 단순한 수준에 머뭅니다.
