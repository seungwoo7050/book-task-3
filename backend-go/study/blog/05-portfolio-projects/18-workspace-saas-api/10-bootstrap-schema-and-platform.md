# 18 Workspace SaaS API — Bootstrap Schema And Platform

`05-portfolio-projects/18-workspace-saas-api`는 JWT auth, 조직 단위 RBAC, async notification, Redis cache를 한 제품형 API로 묶은 대표 포트폴리오 과제다. 이 글에서는 Phase 0 — 프로젝트 초기화와 인프라 구성 -> Phase 1 — 의존성 설치 -> Phase 2 — 마이그레이션 스키마 설계 -> Phase 3 — platform 패키지 (횡단 관심사) 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 0 — 프로젝트 초기화와 인프라 구성
- Phase 1 — 의존성 설치
- Phase 2 — 마이그레이션 스키마 설계
- Phase 3 — platform 패키지 (횡단 관심사)

## Day 1
### Session 1

- 당시 목표: 채용 제출용 B2B SaaS API를 로컬에서 완결형으로 재현할 수 있어야 한다.
- 변경 단위: `pgx/v5`, `google/uuid`, `go-redis/v9`, `x/crypto`, `migrations/001_init.sql`, `migrations/embed.go`
- 처음 가설: 이전 과제 코드를 의존성으로 가져오지 않고 대표작 내부에서 다시 소유해 제출용 완성도를 높였다.
- 실제 진행: 디렉터리 구조 설계. cmd/ 아래 api, worker, migrate 세 개의 바이너리. internal/ 아래 7개 패키지로 도메인 분리. Docker Compose 작성 — PostgreSQL 16 Alpine + Redis 7 Alpine: `pgx/v5`: PostgreSQL 드라이버 + connection pool (pgxpool) `google/uuid`: UUIDv4 생성 (PK 전략) `go-redis/v9`: Redis 클라이언트 (세션 캐시 + 대시보드 캐시) `x/crypto`: bcrypt 패스워드 해싱 go.sum 생성 확인:

CLI:

```bash
mkdir -p 18-workspace-saas-api/go && cd 18-workspace-saas-api/go
go mod init github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api

mkdir -p cmd/{api,worker,migrate}
mkdir -p internal/{auth,cache,httpapi,platform,repository,service,worker}
mkdir -p migrations scripts e2e seed
```

검증 신호:

- POSTGRES_PASSWORD: postgres
- until docker compose exec -T redis redis-cli ping | grep -q PONG; do sleep 1; done
- `invitations` — token_hash UNIQUE, 부분인덱스 (pending 상태의 org+email)
- `refresh_sessions` — replaced_by, revoked_at (토큰 순환 추적)

핵심 코드: `solution/go/migrations/001_init.sql`

```sql
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    display_name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS organization_memberships (
    id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
```

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- organization이 tenant boundary이고, role은 membership에 붙는다.

보조 코드: `solution/go/internal/platform/config.go`

```go
type Config struct {
	AppEnv             string
	Port               int
	DatabaseURL        string
	RedisAddr          string
	RedisPassword      string
	RedisDB            int
	JWTSecret          []byte
	AccessTokenTTL     time.Duration
	RefreshTokenTTL    time.Duration
	WorkerPollInterval time.Duration
	DashboardCacheTTL  time.Duration
}

// LoadConfig는 환경 변수에서 애플리케이션 구성을 읽는다.
func LoadConfig() Config {
	return Config{
		AppEnv:             envString("APP_ENV", "development"),
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

- 다음 글에서는 `20-auth-and-session-rotation.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/migrations/001_init.sql` 같은 결정적인 코드와 `cd 05-portfolio-projects/18-workspace-saas-api/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
