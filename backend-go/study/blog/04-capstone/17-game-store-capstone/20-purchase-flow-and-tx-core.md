# 17 Game Store Capstone — Purchase Flow And Tx Core

`04-capstone/17-game-store-capstone`는 거래 일관성, outbox, 운영 기본 요소를 하나의 게임 상점 API로 통합한 필수 capstone이다. 이 글에서는 5단계: domain 패키지 -> 6단계: repository 구현 -> 7단계: txn 패키지 (재사용) -> 8단계: service 구현 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 5단계: domain 패키지
- 6단계: repository 구현
- 7단계: txn 패키지 (재사용)
- 8단계: service 구현

## Day 1
### Session 1

- 당시 목표: idempotency key, optimistic locking, outbox relay, rate limiting을 한 프로젝트 안에서 다시 조합했다.
- 변경 단위: `txn/retry.go`
- 처음 가설: OAuth나 마이크로서비스는 제외하고 거래 일관성과 재현성에 집중했다.
- 실제 진행: 외부 의존 없는 순수 타입. `Store` struct에 전체 SQL 접근 메서드. 모든 쓰기 메서드는 `*sql.Tx` 인자. 프로젝트 14의 `txn/retry.go`를 그대로 복사. `PgError` 인터페이스, `IsRetryable`, `RunInTx`. `PurchaseService.Purchase` — 7단계 트랜잭션 로직: 멱등성 키 확인 → 플레이어/아이템 조회 → 잔액 차감 → 구매/인벤토리 → Outbox INSERT → 멱등성 키 INSERT

CLI:

```bash
go build ./internal/repository/

go test ./internal/txn/ -v
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/internal/service/purchase_service.go`

```go
var (
	// ErrPlayerNotFound는 요청한 플레이어가 존재하지 않을 때 반환된다.
	ErrPlayerNotFound = errors.New("player not found")
	// ErrItemNotFound는 요청한 카탈로그 아이템이 없을 때 반환된다.
	ErrItemNotFound = errors.New("catalog item not found")
	// ErrInsufficientBalance는 잔액이 아이템 가격보다 부족할 때 반환된다.
	ErrInsufficientBalance = errors.New("insufficient balance")
	// ErrIdempotencyKeyConflict는 같은 멱등 키에 다른 요청 내용이 들어왔을 때 반환된다.
	ErrIdempotencyKeyConflict = errors.New("idempotency key conflict")
)

// ValidationError는 입력 검증 실패를 표현한다.
type ValidationError struct {
	Field   string
	Message string
}

func (e *ValidationError) Error() string {
```

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- capstone의 핵심은 새 알고리즘보다 “여러 운영 제약이 한 곳에서 만날 때의 구조”다.

보조 코드: `solution/go/internal/txn/retry.go`

```go
type sqlStateError interface {
	error
	SQLState() string
}

func IsRetryable(err error) bool {
	var se sqlStateError
	if errors.As(err, &se) {
		return se.SQLState() == RetryableErrorCode
	}
	return false
}
func RunInTx(ctx context.Context, db *sql.DB, maxRetries int, fn func(tx *sql.Tx) error) error {
	if maxRetries <= 0 {
		maxRetries = 3
	}

	var lastErr error
```

왜 이 코드도 같이 봐야 하는가:

이 코드는 충돌이 나는 환경에서 작업을 어떤 조건으로 다시 감을지 정한 핵심 invariant다. 분산 저장소나 고충돌 환경을 다룬다는 말은 결국 이 재시도 규칙을 어떻게 세웠는가로 좁혀진다.

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

- 다음 글에서는 `30-relay-http-and-ops-surface.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/service/purchase_service.go` 같은 결정적인 코드와 `cd 04-capstone/17-game-store-capstone/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
