# 11 Rate Limiter Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: Token Bucket과 per-client limiter를 HTTP middleware까지 연결해 백엔드 보호 기초를 익히는 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/limiter.go`, `solution/go/middleware.go`, `solution/go/limiter_test.go`
- 대표 검증 명령: `make -C problem test`, `cd solution/go && go test -bench=. -benchmem ./...`
- 핵심 개념 축: `token bucket은 burst를 허용하면서 평균 처리율을 제한한다.`, `per-client limiter는 같은 서버 안에서 클라이언트 간 간섭을 줄인다.`, `middleware에 붙이면 개별 handler가 rate limit 세부 사항을 몰라도 된다.`, `stale client cleanup을 하지 않으면 장기적으로 메모리 누수가 된다.`
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

                ### 1. Phase 1 - Limiter와 refill 계산으로 token bucket 바닥을 먼저 고정한다

        - 당시 목표: Limiter와 refill 계산으로 token bucket 바닥을 먼저 고정한다
        - 변경 단위: `solution/go/limiter.go`의 `Limiter.Allow`
        - 처음 가설: `Limiter.Allow`에서 refill 계산을 먼저 잠가야 middleware에서 client별 정책을 올려도 흔들리지 않는다고 봤다.
        - 실제 조치: `solution/go/limiter.go`의 `Limiter.Allow`에서 token refill과 burst cap 규칙을 계산식으로 고정했다.
        - CLI: `make -C problem test`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `Running tests...`였다.
        - 핵심 코드 앵커:
        - `Limiter.Allow`: `solution/go/limiter.go`

        ```go
        // Allow는 토큰 1개를 소비할 수 있으면 true를 반환한다.
func (l *Limiter) Allow() bool {
	l.mu.Lock()
	defer l.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(l.lastTime).Seconds()
	l.lastTime = now

	// 경과 시간만큼 토큰을 재충전한다.
        ```

        - 새로 배운 것: token bucket은 burst를 허용하면서 평균 처리율을 제한한다.
        - 다음: ClientLimiter와 middleware로 요청 단위 경계를 붙인다
        ### 2. Phase 2 - ClientLimiter와 middleware로 요청 단위 경계를 붙인다

        - 당시 목표: ClientLimiter와 middleware로 요청 단위 경계를 붙인다
        - 변경 단위: `solution/go/middleware.go`의 `RateLimitMiddleware`
        - 처음 가설: `RateLimitMiddleware`를 분리하면 전역 limiter와 per-client limiter를 같은 구조 안에서 비교하기 쉽다고 판단했다.
        - 실제 조치: `solution/go/middleware.go`의 `RateLimitMiddleware`를 붙여 IP 단위 policy를 HTTP layer로 올렸다.
        - CLI: `cd solution/go && go test -bench=. -benchmem ./...`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
        - 핵심 코드 앵커:
        - `RateLimitMiddleware`: `solution/go/middleware.go`

        ```go
        func RateLimitMiddleware(cl *ClientLimiter) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			ip := extractIP(r)

			if !cl.Allow(ip) {
				w.Header().Set("Retry-After", "1")
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(http.StatusTooManyRequests)
        ```

        - 새로 배운 것: IP 기반 식별은 쉬우나 NAT나 프록시 환경에서는 거칠 수 있다.
        - 다음: unit test와 benchmark로 burst, refill, concurrency 계약을 잠근다
        ### 3. Phase 3 - unit test와 benchmark로 burst, refill, concurrency 계약을 잠근다

        - 당시 목표: unit test와 benchmark로 burst, refill, concurrency 계약을 잠근다
        - 변경 단위: `solution/go/limiter_test.go`의 `TestLimiterConcurrency`
        - 처음 가설: `TestLimiterConcurrency` 같은 test, bench 조합이 있어야 token bucket 설명이 감상이 아니라 수치로 남는다고 봤다.
        - 실제 조치: `solution/go/limiter_test.go`의 `TestLimiterConcurrency`와 benchmark를 통해 limiter가 동시성에서도 버티는지 확인했다.
        - CLI: `cd solution/go && go test -bench=. -benchmem ./...`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `goos: darwin`였다.
        - 핵심 코드 앵커:
        - `TestLimiterConcurrency`: `solution/go/limiter_test.go`

        ```go
        func TestLimiterConcurrency(t *testing.T) {
	l := NewLimiter(1000, 100)

	var wg sync.WaitGroup
	var allowed, denied int64
	var mu sync.Mutex

	for i := 0; i < 200; i++ {
		wg.Add(1)
        ```

        - 새로 배운 것: refill 계산을 부정확하게 하면 burst cap이 깨지거나 토큰이 과도하게 쌓인다.
        - 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/11-rate-limiter && make -C problem test)
```

```text
Running tests...
cd ../solution/go && go test -v -race -count=1 ./...
=== RUN   TestLimiterBasic
=== RUN   TestLimiterBasic/first_token
=== RUN   TestLimiterBasic/second_token
=== RUN   TestLimiterBasic/third_token
=== RUN   TestLimiterBasic/fourth_token_(empty)
--- PASS: TestLimiterBasic (0.00s)
    --- PASS: TestLimiterBasic/first_token (0.00s)
    --- PASS: TestLimiterBasic/second_token (0.00s)
    --- PASS: TestLimiterBasic/third_token (0.00s)
    --- PASS: TestLimiterBasic/fourth_token_(empty) (0.00s)
=== RUN   TestLimiterRefill
--- PASS: TestLimiterRefill (0.25s)
=== RUN   TestLimiterBurstCap
--- PASS: TestLimiterBurstCap (0.10s)
=== RUN   TestLimiterConcurrency
--- PASS: TestLimiterConcurrency (0.00s)
=== RUN   TestClientLimiterBasic
--- PASS: TestClientLimiterBasic (0.00s)
=== RUN   TestClientLimiterCount
--- PASS: TestClientLimiterCount (0.00s)
... (20 more lines)
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/11-rate-limiter && cd solution/go && go test -bench=. -benchmem ./...)
```

```text
goos: darwin
goarch: arm64
pkg: github.com/woopinbell/go-backend/study/01-backend-core/11-rate-limiter
cpu: Apple M1
BenchmarkLimiterAllow-8         	 6170140	       165.1 ns/op	       0 B/op	       0 allocs/op
BenchmarkClientLimiterAllow-8   	 6150458	       203.1 ns/op	       0 B/op	       0 allocs/op
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/11-rate-limiter	3.284s
```
