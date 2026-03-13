# Web Proxy structure guide

## 이 글의 중심 질문

- 클라이언트 요청, origin fetch, cache 저장을 프록시 안에서 어떻게 이어 붙였는가?
- 한 줄 답: 클라이언트 요청을 중계하고 파일 기반 캐시로 재사용하는 간단한 HTTP 프록시 구현입니다.

## 권장 흐름

1. 실행 표면과 entrypoint를 먼저 고정하기
2. URL 해석과 cache/origin 분기를 한 요청 흐름으로 묶기
3. 테스트와 남은 범위를 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test`
- `study/01-Application-Protocols-and-Sockets/web-proxy/python/src/web_proxy.py`의 `def handle_client`
- `study/01-Application-Protocols-and-Sockets/web-proxy/python/tests/test_web_proxy.py`의 `def test_same_url_same_key`

## 리라이트 주의점

- `Web Proxy`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 `Cache-Control`이나 TTL 기반 만료 정책은 없습니다. 같은 남은 경계를 사람 말로 다시 정리한다.
