# 17 Game Store Capstone — Relay Http And Ops Surface

`04-capstone/17-game-store-capstone`는 거래 일관성, outbox, 운영 기본 요소를 하나의 게임 상점 API로 통합한 필수 capstone이다. 이 글에서는 9단계: httpapi 구현 -> 10단계: relay 구현 -> 11단계: cmd/api 진입점 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 9단계: httpapi 구현
- 10단계: relay 구현
- 11단계: cmd/api 진입점

## Day 1
### Session 1

- 당시 목표: 문제 정의와 답안 요약, docs/notion을 분리해 제출 가능한 공개 표면을 정리한다.
- 변경 단위: `solution/go/internal/httpapi/handler.go`, `solution/go/internal/relay/relay.go`
- 처음 가설: OAuth나 마이크로서비스는 제외하고 거래 일관성과 재현성에 집중했다.
- 실제 진행: 4개 엔드포인트 + loggingMiddleware + rateLimitMiddleware. `decoder.DisallowUnknownFields()` 적용. 에러 → HTTP 상태 코드 매핑. `OutboxStore` + `Publisher` 인터페이스. `Relay.PollOnce` 공개 메서드 (테스트용). API + Relay를 같은 프로세스에서 실행 (별도 고루틴). Graceful shutdown: SIGTERM → Relay 중지 → HTTP 서버 Shutdown.

CLI:

```bash
go test ./internal/relay/ -v

# 로컬 실행
make run
# 또는: go run ./cmd/api

# 빌드
mkdir -p ./bin
go build -o ./bin/api ./cmd/api
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/internal/httpapi/handler.go`

```go
type API struct {
	purchaseService *service.PurchaseService
	queryService    *service.QueryService
	logger          *slog.Logger
	limiter         *RateLimiter
}

// NewAPI는 API 핸들러를 생성합니다.
func NewAPI(
	purchaseService *service.PurchaseService,
	queryService *service.QueryService,
	logger *slog.Logger,
	rateLimitRPS int,
) *API {
	var limiter *RateLimiter
	if rateLimitRPS > 0 {
		limiter = NewRateLimiter(rateLimitRPS)
	}
```

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- e2e 테스트는 unit test가 놓치는 통합 문제를 빠르게 드러낸다.

보조 코드: `solution/go/internal/relay/relay.go`

```go
type OutboxStore interface {
	ListUnpublishedOutbox(ctx context.Context, limit int) ([]domain.OutboxEvent, error)
	MarkOutboxPublished(ctx context.Context, eventID string) error
}
type Publisher interface {
	Publish(ctx context.Context, event domain.OutboxEvent) error
}
type Relay struct {
	store     OutboxStore
	publisher Publisher
	logger    *slog.Logger
	interval  time.Duration
	batchSize int
}

func New(store OutboxStore, publisher Publisher, logger *slog.Logger, interval time.Duration, batchSize int) *Relay {
	if interval <= 0 {
		interval = time.Second
```

왜 이 코드도 같이 봐야 하는가:

이 블록은 동기 write path와 비동기 side effect를 분리하는 설계의 핵심 증거다. "나중에 처리한다"가 아니라 "어떻게 안전하게 넘긴다"를 설명하게 해 준다.

CLI:

```bash
cd 04-capstone/17-game-store-capstone/go
mkdir -p ./bin
go build -o ./bin/api ./cmd/api
go test ./...
make repro
```

검증 신호:

- 2026-03-08 기준 `mkdir -p ./bin && go build -o ./bin/api ./cmd/api`가 통과했다.
- 2026-03-08 기준 `go test ./...`가 통과했다.
- 2026-03-08 기준 `make repro`가 통과했다.

다음:

- 다음 글에서는 `40-repro-and-e2e-hardening.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/httpapi/handler.go` 같은 결정적인 코드와 `cd 04-capstone/17-game-store-capstone/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
