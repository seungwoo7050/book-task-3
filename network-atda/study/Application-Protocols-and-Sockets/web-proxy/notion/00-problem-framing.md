# 00 문제 프레이밍

## 프로젝트 정의
- 프로젝트: `Web Proxy`
- 상태: `verified`
- 기준 검증: `make -C study/Application-Protocols-and-Sockets/web-proxy/problem test`
- 문제 배경: 클라이언트와 원본 서버 사이에 끼어드는 중간자 역할을 구현하면서 URL 파싱, 포워딩, 캐시를 함께 배우는 프로젝트다.

## 이번 범위
- 브라우저/`curl -x`가 보낸 HTTP 요청을 받아 원본 서버로 전달한다.
- 절대 URL을 호스트, 포트, 경로로 나누고 원본 서버에는 origin-form 요청으로 다시 보낸다.
- 응답을 URL 기준으로 캐시하고, 이후에는 원본 서버가 내려가도 캐시 히트를 반환한다.

## 제약과 전제
- 범위는 HTTP 평문 요청이다. `CONNECT`와 HTTPS 터널링은 다루지 않는다.
- 캐시 무효화와 만료 정책 대신, 동일 URL 재요청에서 캐시 사용 여부를 확인하는 데 집중한다.
- 에러는 주로 `502 Bad Gateway`, `504 Gateway Timeout`으로 분리한다.

## 성공 기준
- 기본 URL, 포트 포함 URL, 쿼리 문자열 URL을 안정적으로 파싱한다.
- 원본 서버 응답을 정상 전달하고, 캐시 히트가 테스트로 증명된다.
- `make -C study/Application-Protocols-and-Sockets/web-proxy/problem test`가 통과한다.

## 공개 문서
- [`../README.md`](../README.md)
- [`../problem/README.md`](../problem/README.md)
- [`../python/README.md`](../python/README.md)
- [`../docs/README.md`](../docs/README.md)
- [`../docs/references/README.md`](../docs/references/README.md)

## 이번에 일부러 제외한 것
- HTTPS `CONNECT`, 캐시 만료 정책, LRU 축출 정책은 구현하지 않는다.
- 헤더 재작성과 보안 필터링을 제품 수준으로 다듬지 않는다.
