# 15 Event Pipeline — Relay Consumer And Delivery Boundary

`03-platform-engineering/15-event-pipeline`는 outbox pattern, relay, idempotent consumer를 통해 DB 정합성과 비동기 전달 경계를 함께 다루는 대표 과제다. 이 글에서는 5단계: Relay 구현 -> 6단계: Consumer 구현 -> 7단계: CLI 진입점 -> 8단계: Kafka 토픽 생성 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 5단계: Relay 구현
- 6단계: Consumer 구현
- 7단계: CLI 진입점
- 8단계: Kafka 토픽 생성

## Day 1
### Session 1

- 당시 목표: aggregate_id를 기준으로 ordering을 맞추고, consumer는 processed event tracking으로 중복 처리를 막는다.
- 변경 단위: `relay/main.go`, `consumer/main.go`
- 처음 가설: consumer idempotency를 별도 책임으로 두어 relay와 downstream 처리의 경계를 선명하게 했다.
- 실제 진행: `Relay.Run(ctx)` — ticker 루프, 폴링 → Kafka 발행 → MarkPublished. 설정: `PollInterval` (기본 1초), `BatchSize` (기본 100). Key = AggregateID, Headers = event_type + event_id + aggregate_type. 2단계 멱등성: 인메모리 map → DB processed_events. `FetchMessage` + `CommitMessages` 수동 커밋. Handler 실패 시 오프셋 미커밋 → 자동 재전달. 각각 독립 프로세스로 실행 가능. 파티션 3개: Consumer Group 내 최대 3개 Consumer 병렬 처리.

CLI:

```bash
go test ./relay/ -v

go test ./consumer/ -v
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/relay/relay.go`

```go
type Relay struct {
	repo     *outbox.Repository
	writer   *kafka.Writer
	logger   *slog.Logger
	interval time.Duration
	batch    int
}

// Config는 릴레이의 폴링 간격과 배치 크기를 정의한다.
type Config struct {
	PollInterval time.Duration
	BatchSize    int
}

// New는 outbox 릴레이를 생성한다.
func New(repo *outbox.Repository, writer *kafka.Writer, logger *slog.Logger, cfg Config) *Relay {
	if cfg.PollInterval == 0 {
		cfg.PollInterval = time.Second
```

왜 이 코드가 중요했는가:

이 블록은 동기 write path와 비동기 side effect를 분리하는 설계의 핵심 증거다. "나중에 처리한다"가 아니라 "어떻게 안전하게 넘긴다"를 설명하게 해 준다.

새로 배운 것:

- relay는 outbox row를 브로커로 밀어내는 별도 프로세스다.

보조 코드: `solution/go/consumer/consumer.go`

```go
type Handler func(ctx context.Context, eventType string, payload json.RawMessage) error

// Consumer는 Kafka 메시지를 읽고 중복 여부를 확인한 뒤 처리한다.
type Consumer struct {
	reader  *kafka.Reader
	db      *sql.DB
	handler Handler
	logger  *slog.Logger

	// 최근 처리 이력을 메모리에 유지해 같은 프로세스 안에서 빠르게 중복을 걸러낸다.
	mu        sync.RWMutex
	processed map[string]struct{}
}

// New는 Kafka consumer 인스턴스를 생성한다.
func New(reader *kafka.Reader, db *sql.DB, handler Handler, logger *slog.Logger) *Consumer {
	return &Consumer{
		reader:    reader,
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 03-platform-engineering/15-event-pipeline
make -C problem build
make -C problem test

cd 03-platform-engineering/15-event-pipeline/solution/go
make repro
```

검증 신호:

- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd solution/go && make repro`가 통과했다.

다음:

- 다음 글에서는 `30-repro-and-e2e-proof.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/relay/relay.go` 같은 결정적인 코드와 `cd 03-platform-engineering/15-event-pipeline` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
