# 18 Workspace SaaS API — Http Worker Seed And Smoke Surface

`05-portfolio-projects/18-workspace-saas-api`는 JWT auth, 조직 단위 RBAC, async notification, Redis cache를 한 제품형 API로 묶은 대표 포트폴리오 과제다. 이 글에서는 Phase 8 — httpapi 패키지 (HTTP 서버) -> Phase 9 — worker 패키지 (알림 워커) -> Phase 10 — Seed 데이터 -> Phase 11 — 테스트 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 8 — httpapi 패키지 (HTTP 서버)
- Phase 9 — worker 패키지 (알림 워커)
- Phase 10 — Seed 데이터
- Phase 11 — 테스트

## Day 1
### Session 1

- 당시 목표: Postgres + Redis 기반 local reproducibility와 smoke script를 README 표면에 올렸다.
- 변경 단위: `internal/httpapi/server.go`, `internal/httpapi/middleware.go`, `internal/httpapi/handlers.go`, `internal/worker/worker.go`, `cmd/worker/main.go`, `seed/`
- 처음 가설: worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 실제 진행: `http.NewServeMux()` 기반 17개 라우트: 인프라 엔드포인트: `/healthz`, `/readyz` (Redis ping 포함). 별도 바이너리. 폴링 루프: outbox_events에서 unpublished 건 조회 이벤트별 조직 멤버 조회 → 알림 INSERT (actor 제외) 대시보드 캐시 무효화 (Redis DEL) outbox published_at 마킹

CLI:

```bash
# API 서버 실행
PORT=4080 APP_ENV=development \
  DATABASE_URL=postgres://postgres:postgres@localhost:54339/workspace_saas?sslmode=disable \
  REDIS_ADDR=localhost:6381 \
  JWT_SECRET=workspace-saas-secret \
  go run ./cmd/api

# Worker 실행
APP_ENV=development \
  DATABASE_URL=postgres://postgres:postgres@localhost:54339/workspace_saas?sslmode=disable \
  REDIS_ADDR=localhost:6381 \
  JWT_SECRET=workspace-saas-secret \
  WORKER_POLL_INTERVAL=250ms \
  go run ./cmd/worker
```

검증 신호:

- Smoke 테스트
- `scripts/smoke.sh` — curl 기반 시나리오. API 서버와 Worker를 백그라운드로 띄우고 전체 플로우 검증:
- make smoke

핵심 코드: `solution/go/internal/httpapi/server.go`

```go
type contextKey string

const principalContextKey contextKey = "workspace-principal"

// Principal은 인증된 호출자 정보를 담는다.
type Principal struct {
	UserID string
	Email  string
}

type appHandler func(http.ResponseWriter, *http.Request) error

// Server는 workspace SaaS API의 HTTP 라우팅과 공통 미들웨어를 담당한다.
type Server struct {
	service   *service.Service
	logger    *slog.Logger
	metrics   *platform.Metrics
	jwtSecret []byte
```

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- dashboard summary는 org 단위 aggregate이며 Redis 캐시 miss 또는 장애 시 DB로 fallback 한다.

보조 코드: `solution/go/internal/worker/worker.go`

```go
type Store interface {
	ListUnpublishedOutbox(ctx context.Context, limit int) ([]repository.OutboxEvent, error)
	ListRecipients(ctx context.Context, organizationID, excludeUserID string) ([]repository.Recipient, error)
	CreateNotification(ctx context.Context, notification repository.Notification) error
	MarkOutboxPublished(ctx context.Context, eventID string) error
}
type SummaryCache interface {
	DeleteDashboardSummary(ctx context.Context, organizationID string) error
}
type Processor struct {
	store   Store
	cache   SummaryCache
	logger  *slog.Logger
	metrics *platform.Metrics
}

func New(store Store, cache SummaryCache, logger *slog.Logger, metrics *platform.Metrics) *Processor {
	if logger == nil {
```

왜 이 코드도 같이 봐야 하는가:

이 블록은 동기 write path와 비동기 side effect를 분리하는 설계의 핵심 증거다. "나중에 처리한다"가 아니라 "어떻게 안전하게 넘긴다"를 설명하게 해 준다.

CLI:

```bash
cd 05-portfolio-projects/18-workspace-saas-api/go
go test ./...
make e2e
make smoke

cd ../../..
make test-portfolio-unit test-portfolio-repro
make test-all
```

검증 신호:

- `go test ./...` 통과
- `make e2e` 통과
- `make smoke` 통과
- [presentation-assets/demo-2026-03-07](presentation-assets/demo-2026-03-07)는
- `make test-portfolio-unit test-portfolio-repro` 통과

다음:

- 다음 글에서는 `50-repro-demo-and-portfolio-proof.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/httpapi/server.go` 같은 결정적인 코드와 `cd 05-portfolio-projects/18-workspace-saas-api/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
