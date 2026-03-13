# 11 Rate Limiter — Token Bucket Core

`01-backend-core/11-rate-limiter`는 Token Bucket과 per-client limiter를 HTTP middleware까지 연결해 백엔드 보호 기초를 익히는 과제다. 이 글에서는 1단계: 프로젝트 초기화 -> 2단계: 패키지 구조 -> 3단계: Limiter 구조체 (limiter.go) -> 4단계: Allow() 구현 -> 5단계: ClientLimiter 구현 -> 6단계: cleanup goroutine 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 1단계: 프로젝트 초기화
- 2단계: 패키지 구조
- 3단계: Limiter 구조체 (limiter.go)
- 4단계: Allow() 구현
- 5단계: ClientLimiter 구현
- 6단계: cleanup goroutine

## Day 1
### Session 1

- 당시 목표: Token Bucket 알고리즘을 직접 구현해야 한다.
- 변경 단위: `solution/go/limiter.go`, `solution/go/limiter_test.go`
- 처음 가설: rate limiter 자체와 HTTP middleware를 분리해 알고리즘과 네트워크 표면을 따로 읽게 했다.
- 실제 진행: 외부 의존성 없음. Go 1.22+. HTTP 서버가 별도 cmd/로 없는 라이브러리 프로젝트: 패키지 이름: `ratelimiter`. `NewLimiter(rate, burst)` — 버킷을 가득 채운 상태로 시작.

CLI:

```bash
cd study/01-backend-core/11-rate-limiter/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/11-rate-limiter
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/limiter.go`

```go
type Limiter struct {
	mu       sync.Mutex
	rate     float64   // 초당 재충전 토큰 수
	burst    int       // 버킷 최대 용량
	tokens   float64   // 현재 남아 있는 토큰 수
	lastTime time.Time // 마지막 토큰 계산 시각
}

// NewLimiter는 재충전 속도와 burst 용량으로 Limiter를 생성한다.
func NewLimiter(rate float64, burst int) *Limiter {
	return &Limiter{
		rate:     rate,
		burst:    burst,
		tokens:   float64(burst), // 시작 시점에는 토큰을 가득 채운다.
		lastTime: time.Now(),
	}
}
```

왜 이 코드가 중요했는가:

이 블록은 병렬성과 보호 정책을 아이디어가 아니라 코드 invariant로 바꾼다. goroutine, channel, token을 어떤 경계로 묶었는지가 여기서 드러난다.

새로 배운 것:

- token bucket은 burst를 허용하면서 평균 처리율을 제한한다.

보조 코드: `solution/go/limiter_test.go`

```go
func TestLimiterBasic(t *testing.T) {
	l := NewLimiter(2, 3)

	tests := []struct {
		name string
		want bool
	}{
		{"first token", true},
		{"second token", true},
		{"third token", true},
		{"fourth token (empty)", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := l.Allow()
			if got != tt.want {
				t.Errorf("Allow() = %v, want %v", got, tt.want)
```

왜 이 코드도 같이 봐야 하는가:

이 블록은 병렬성과 보호 정책을 아이디어가 아니라 코드 invariant로 바꾼다. goroutine, channel, token을 어떤 경계로 묶었는지가 여기서 드러난다.

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

- 다음 글에서는 `20-http-middleware-and-bench.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/limiter.go` 같은 결정적인 코드와 `cd 01-backend-core/11-rate-limiter` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
