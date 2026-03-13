# 14 Cockroach TX — Purchase Service And Http Surface

`03-platform-engineering/14-cockroach-tx`는 idempotency key, optimistic locking, transaction retry를 CockroachDB 호환 흐름으로 묶어 정합성 기초를 다지는 과제다. 이 글에서는 7단계: Service 구현 -> 8단계: HTTP Handler -> 9단계: cmd/server 진입점 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 7단계: Service 구현
- 8단계: HTTP Handler
- 9단계: cmd/server 진입점

## Day 1
### Session 1

- 당시 목표: balance version conflict와 idempotency cached response를 서비스 경계에서 구분한다.
- 변경 단위: `solution/go/service/purchase.go`, `solution/go/handler/purchase.go`
- 처음 가설: HTTP handler, service, repo를 나눠 정합성 로직이 어디에 있어야 하는지 드러냈다.
- 실제 진행: `PurchaseService.Purchase` — `RunInTx` 안에서 6단계 조율: 멱등성 키 확인 → 플레이어 조회 → 잔액 차감 → 인벤토리 upsert → 감사 로그 → 멱등성 키 저장 `PurchaseHandler.ServeHTTP` — `Idempotency-Key` 헤더 검증, JSON 디코딩, ErrConflict → 409 매핑 커넥션 풀: `MaxOpenConns=25`, `MaxIdleConns=10`, `ConnMaxLifetime=5m` Graceful shutdown: SIGTERM/SIGINT → 5초 타임아웃

CLI:

```bash
go test ./service/ -v

# 로컬 실행
make run
# 또는: DATABASE_URL="postgresql://root@localhost:26257/defaultdb?sslmode=disable" go run ./cmd/server
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/service/purchase.go`

```go
type PurchaseRequest struct {
	IdempotencyKey string `json:"idempotency_key"`
	PlayerID       string `json:"player_id"`
	ItemName       string `json:"item_name"`
	Price          int64  `json:"price"`
}
type PurchaseResponse struct {
	Status     string `json:"status"`
	NewBalance int64  `json:"new_balance"`
	Item       string `json:"item"`
}
type PurchaseService struct {
	DB         *sql.DB
	MaxRetries int
}

func NewPurchaseService(db *sql.DB) *PurchaseService {
	return &PurchaseService{
```

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- optimistic locking은 `version` 컬럼으로 충돌을 감지한다.

보조 코드: `solution/go/handler/purchase.go`

```go
type PurchaseHandler struct {
	Service *service.PurchaseService
}
type purchaseInput struct {
	PlayerID string `json:"player_id"`
	ItemName string `json:"item_name"`
	Price    int64  `json:"price"`
}
type errorResponse struct {
	Error string `json:"error"`
}

func (h *PurchaseHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, errorResponse{Error: "method not allowed"})
		return
	}
	idempotencyKey := r.Header.Get("Idempotency-Key")
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 03-platform-engineering/14-cockroach-tx
make -C problem build
make -C problem test

cd 03-platform-engineering/14-cockroach-tx/solution/go
make repro
```

검증 신호:

- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd solution/go && make repro`가 통과했다.

다음:

- 다음 글에서는 `30-repro-and-e2e-proof.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/service/purchase.go` 같은 결정적인 코드와 `cd 03-platform-engineering/14-cockroach-tx` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
