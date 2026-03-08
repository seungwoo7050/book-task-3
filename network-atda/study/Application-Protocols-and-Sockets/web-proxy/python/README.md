# Python 구현 안내

이 디렉터리는 `Web Proxy`의 공개 구현을 담는다.

## 구성

- `src/web_proxy.py`
- `tests/test_web_proxy.py`

## 기준 명령

- 실행: `make -C study/Application-Protocols-and-Sockets/web-proxy/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/web-proxy/problem test`

## 구현 메모

- 상태: `verified`
- 현재 범위: HTTP GET과 간단한 파일 캐시만 다룬다. HTTPS 터널링이나 만료 정책은 다루지 않는다.
- 남은 약점: TTL/Cache-Control 기반 만료 정책 없음
- 남은 약점: HTTPS CONNECT 미지원
- 남은 약점: cache 디렉터리 동시성 제어 없음
