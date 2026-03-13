# 18 Workspace SaaS API — Repository Service Cache Boundaries

`05-portfolio-projects/18-workspace-saas-api`는 JWT auth, 조직 단위 RBAC, async notification, Redis cache를 한 제품형 API로 묶은 대표 포트폴리오 과제다. 이 글에서는 Phase 5 — repository 패키지 (데이터 액세스) -> Phase 6 — cache 패키지 (Redis) -> Phase 7 — service 패키지 (비즈니스 로직) 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 5 — repository 패키지 (데이터 액세스)
- Phase 6 — cache 패키지 (Redis)
- Phase 7 — service 패키지 (비즈니스 로직)

## Day 1
### Session 1

- 당시 목표: Postgres + Redis 기반 local reproducibility와 smoke script를 README 표면에 올렸다.
- 변경 단위: `internal/repository/`, `models.go`, `user.go`, `organization.go`, `invitation.go`, `project.go`
- 처음 가설: worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 실제 진행: `internal/repository/` 아래 파일별 책임 분리: `models.go`: 10+ 도메인 모델 구조체 `user.go`: CreateUser, GetUserByEmail, GetUserByID `organization.go`: CreateOrganization, AddMembership, GetMembership, ListMemberships `invitation.go`: CreateInvitation, GetInvitationByToken, AcceptInvitation `project.go`: CreateProject, ListProjects, GetProject `issue.go`: CreateIssue, GetIssue, ListIssues, UpdateIssue (version 낙관적 잠금) `comment.go`: CreateComment, ListComments `session.go`: CreateRefreshSession, GetRefreshSession, RevokeSession, RevokeAllUserSessions `outbox.go`: InsertOutboxEvent, FetchUnpublished, MarkPublished `notification.go`: InsertNotification, ListNotifications `dashboard.go`: GetDashboardSummary (COUNT 쿼리 집합) `NewClient`: go-redis/v9 클라이언트 생성, Ping으로 연결 확인 `SetRefreshSession` / `GetRefreshSession`: 세션 JSON → Redis SET/GET (TTL = 세션 만료시간) `SetDashboard` / `GetDashboard`: 대시보드 요약 JSON → Redis SET/GET (30초 TTL) `InvalidateDashboard`: DEL 명령 `Ping` / `Close`: 헬스체크와 정리 Redis 장애 시 에러를 로깅만 하고 nil 반환 → 호출자가 DB fallback.

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

- - `invitation.go`: CreateInvitation, GetInvitationByToken, AcceptInvitation
- - `session.go`: CreateRefreshSession, GetRefreshSession, RevokeSession, RevokeAllUserSessions
- - RefreshToken: 세션 검증 → 토큰 순환 → 새 세션 → 새 토큰

핵심 코드: `solution/go/internal/repository/store.go`

```go
var (
	ErrNotFound               = errors.New("not found")
	ErrEmailExists            = errors.New("email already exists")
	ErrOrganizationSlugExists = errors.New("organization slug already exists")
	ErrAlreadyMember          = errors.New("user is already a member")
	ErrPendingInvitation      = errors.New("pending invitation already exists")
	ErrProjectKeyExists       = errors.New("project key already exists")
	ErrVersionConflict        = errors.New("version conflict")
	ErrIdempotencyConflict    = errors.New("idempotency key conflict")
)

type Store struct {
	db *sql.DB
}

func Open(ctx context.Context, databaseURL string) (*Store, error) {
	db, err := sql.Open("pgx", databaseURL)
	if err != nil {
```

왜 이 코드가 중요했는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

새로 배운 것:

- write flow는 issue/comment 이벤트를 outbox에 남기고 worker가 notification으로 변환한다.

보조 코드: `solution/go/internal/service/service.go`

```go
type Service struct {
	store             *repository.Store
	cache             *cache.Client
	logger            *slog.Logger
	metrics           *platform.Metrics
	jwtSecret         []byte
	accessTokenTTL    time.Duration
	refreshTokenTTL   time.Duration
	dashboardCacheTTL time.Duration
	now               func() time.Time
}

// New는 애플리케이션 서비스 레이어를 생성한다.
func New(
	store *repository.Store,
	cacheClient *cache.Client,
	logger *slog.Logger,
	metrics *platform.Metrics,
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

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

- 다음 글에서는 `40-http-worker-seed-and-smoke-surface.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/repository/store.go` 같은 결정적인 코드와 `cd 05-portfolio-projects/18-workspace-saas-api/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
