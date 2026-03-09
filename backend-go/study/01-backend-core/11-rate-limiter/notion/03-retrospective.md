# 회고 — Token Bucket을 직접 만들어본 뒤

## 무엇을 만들었나

Token Bucket 알고리즘 기반 rate limiter. Limiter(단일), ClientLimiter(IP별), RateLimitMiddleware(HTTP 통합) 세 계층. 외부 의존성 없이 Go 표준 라이브러리만 사용. 파일 네 개(limiter.go, limiter_test.go, middleware.go, middleware_test.go).

## 잘된 점

**연속 리필 구현**이 깔끔했다. goroutine 없이 `Allow()` 호출 시점에 경과 시간으로 토큰을 계산한다. 타이머 기반 리필보다 코드가 단순하고 정확하다.

**세 계층의 분리**가 명확하다. Limiter는 알고리즘만, ClientLimiter는 멀티테넌시만, Middleware는 HTTP 통합만 담당한다. 각각 독립적으로 테스트할 수 있다.

**cleanup goroutine의 종료가 보장된다.** context cancellation + ticker.Stop으로 리소스 누수가 없다. 10에서 배운 goroutine 관리가 바로 적용됐다.

## 아쉬운 점

**분산 환경을 지원하지 않는다.** 서버가 여러 대면 각 서버가 독립된 카운터를 갖는다. Redis 기반 공유 limiter(sliding window log 등)가 필요하지만, 이 프로젝트의 범위는 아니다.

**Retry-After 값이 정적**이다. 토큰 리필까지 남은 시간을 계산해 동적으로 응답하면 클라이언트가 더 효율적으로 재시도할 수 있다.

**rate와 burst의 관계가 문서화되지 않았다.** burst=10, rate=2면 "평소 초당 2개, 순간 최대 10개"라는 의미인데, 이 관계를 코드 주석이나 설정 예시로 설명했으면 좋았을 것이다.

## 커리큘럼에서의 위치

| 프로젝트 | 동시성 요소 |
|---------|-----------|
| 03 | sync.Mutex, -race |
| 09 | atomic.Int64, sync.Mutex로 캐시 보호 |
| 10 | goroutine, channel, WaitGroup, context |
| **11** | **Mutex + context + background goroutine** |

11은 01-backend-core 섹션의 마지막 프로젝트다. HTTP API(05-09) + 동시성(10) + 인프라 컴포넌트(11)를 거쳐, 12부터는 분산 시스템 영역으로 넘어간다.
