# 11 Rate Limiter — Http Middleware And Bench

`01-backend-core/11-rate-limiter`는 Token Bucket과 per-client limiter를 HTTP middleware까지 연결해 백엔드 보호 기초를 익히는 과제다. 이 글에서는 7단계: HTTP Middleware (middleware.go) -> 8단계: 테스트 (limiter_test.go) -> 9단계: 미들웨어 테스트 (middleware_test.go) -> 10단계: 벤치마크 -> 11단계: Race detector 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 7단계: HTTP Middleware (middleware.go)
- 8단계: 테스트 (limiter_test.go)
- 9단계: 미들웨어 테스트 (middleware_test.go)
- 10단계: 벤치마크
- 11단계: Race detector

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/middleware.go`, `solution/go/middleware_test.go`
- 처음 가설: distributed limiter를 제외해 단일 프로세스 제어 흐름과 동기화 문제를 먼저 익히게 했다.
- 실제 진행: IP 추출: X-Forwarded-For → X-Real-IP → RemoteAddr 제한 초과 시: 429 + Retry-After: 1 + JSON 에러 응답 테스트 목록: 버스트 내 Allow() → true 버스트 초과 Allow() → false 시간 경과 후 리필 확인 ClientLimiter IP별 독립 제한 cleanup 후 stale 클라이언트 제거 확인 burst 내 요청 → 200 burst 초과 → 429 + Retry-After 헤더 검증 httptest.NewRecorder 사용 Allow() 호출의 ns/op 측정.

CLI:

```bash
go test ./...

go test -run TestMiddleware ./...
```

검증 신호:

- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.
- 남은 선택 검증: Redis-backed shared limiter는 이 과제 범위에 포함하지 않았다.

핵심 코드: `solution/go/middleware.go`

```go
func RateLimitMiddleware(cl *ClientLimiter) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			ip := extractIP(r)

			if !cl.Allow(ip) {
				w.Header().Set("Retry-After", "1")
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(http.StatusTooManyRequests)

				resp := map[string]any{
					"error": map[string]string{
						"message": "rate limit exceeded",
					},
				}
				json.NewEncoder(w).Encode(resp)
				return
			}
```

왜 이 코드가 중요했는가:

이 블록은 요청 수명주기를 감싸는 순서를 고정한다. recovery, logging, auth, CORS는 순서가 틀리면 의미가 달라지기 때문에 이 코드가 글의 축이 된다.

새로 배운 것:

- per-client limiter는 같은 서버 안에서 클라이언트 간 간섭을 줄인다.

보조 코드: `solution/go/middleware_test.go`

```go
func TestRateLimitMiddleware(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	cl := NewClientLimiter(ctx, 2, 2)

	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("ok"))
	})

	middleware := RateLimitMiddleware(cl)(handler)

	tests := []struct {
		name       string
		wantStatus int
	}{
		{"first request allowed", http.StatusOK},
		{"second request allowed", http.StatusOK},
```

왜 이 코드도 같이 봐야 하는가:

이 블록은 요청 수명주기를 감싸는 순서를 고정한다. recovery, logging, auth, CORS는 순서가 틀리면 의미가 달라지기 때문에 이 코드가 글의 축이 된다.

CLI:

```bash
cd 01-backend-core/11-rate-limiter
make -C problem test
make -C problem bench
```

검증 신호:

- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.

다음:

- Redis-backed shared limiter는 이 과제 범위에 포함하지 않았다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/middleware.go` 같은 결정적인 코드와 `cd 01-backend-core/11-rate-limiter` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
