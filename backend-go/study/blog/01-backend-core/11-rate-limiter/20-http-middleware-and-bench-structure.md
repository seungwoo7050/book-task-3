# 11 Rate Limiter Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- distributed limiter를 제외해 단일 프로세스 제어 흐름과 동기화 문제를 먼저 익히게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/11-rate-limiter` 안에서 `20-http-middleware-and-bench.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 7단계: HTTP Middleware (middleware.go) -> 8단계: 테스트 (limiter_test.go) -> 9단계: 미들웨어 테스트 (middleware_test.go) -> 10단계: 벤치마크 -> 11단계: Race detector
- 세션 본문: `solution/go/middleware.go, solution/go/middleware_test.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/middleware.go`
- 코드 앵커 2: `solution/go/middleware_test.go`
- 코드 설명 초점: 이 블록은 요청 수명주기를 감싸는 순서를 고정한다. recovery, logging, auth, CORS는 순서가 틀리면 의미가 달라지기 때문에 이 코드가 글의 축이 된다.
- 개념 설명: per-client limiter는 같은 서버 안에서 클라이언트 간 간섭을 줄인다.
- 마지막 단락: Redis-backed shared limiter는 이 과제 범위에 포함하지 않았다.
