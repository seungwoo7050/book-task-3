# 문제 정의

## 문제

서비스가 분리된 뒤에도 외부 클라이언트는 하나의 API만 보고 싶다. 이 랩은 gateway가 public API shape를 유지하고, cookie와 CSRF를 edge에만 두며, 내부 서비스에는 request id와 bearer token만 전달하는 구조를 연습한다.

## 성공 기준

- gateway가 `/api/v1/auth/*`, `/api/v1/platform/*` 경로를 유지한다.
- 로그인 후 쿠키가 gateway에서만 설정된다.
- 내부 호출에 `X-Request-ID`가 전달된다.

## 제외 범위

- circuit breaker
- service discovery
- 고급 edge cache
