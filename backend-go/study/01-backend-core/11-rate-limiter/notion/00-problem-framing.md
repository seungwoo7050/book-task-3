# 문제 정의 — 왜 Rate Limiter인가

## API를 보호해야 한다

05부터 09까지 HTTP API를 만들었다. 하지만 이 서버들은 클라이언트가 초당 수천 개의 요청을 보내도 막을 방법이 없다. 실서비스에서 이런 요청은 서버 자원을 고갈시키고, 정상 사용자의 경험을 해친다.

Rate limiter는 이 문제의 가장 기본적인 방어선이다.

## 핵심 과제

세 부분으로 나뉜다:

### Part 1: Token Bucket 알고리즘
- `rate` 토큰/초로 연속 리필
- `burst`(버킷 용량)만큼 순간 요청 허용
- `Allow()` → true(토큰 소비)/false(거부)
- 스레드 안전

### Part 2: Per-Client 제한
- IP별로 독립된 Limiter 관리
- 3분 이상 요청 없는 클라이언트 자동 정리(cleanup goroutine)
- context cancellation으로 cleanup goroutine 종료

### Part 3: HTTP Middleware
- 429 Too Many Requests + `Retry-After` 헤더
- `r.RemoteAddr`에서 IP 추출 (포트 분리)

## 10과의 연결

10에서 goroutine 관리, context cancellation, channel을 배웠다. 11에서는 이 패턴들이 실제 인프라 컴포넌트(rate limiter)에 적용된다:
- `cleanup` goroutine → 10의 worker goroutine과 동일한 종료 패턴
- context → cleanup 종료 신호
- `sync.Mutex` → 03에서 시작해 반복적으로 사용

## 외부 의존성 없음

Go 표준 라이브러리만 사용. `golang.org/x/time/rate` 같은 라이브러리가 있지만, 알고리즘을 직접 구현해야 Token Bucket의 수학적 기반을 이해할 수 있다.
