# 타임라인 — Workspace SaaS API 개발 과정

이 문서는 소스 코드에 남지 않는 개발 과정을 기록한다. 환경 구성, CLI 명령, 패키지 설치, 인프라 셋업, 테스트 실행 순서를 시간 흐름에 따라 작성했다.

---

## Phase 0 — 프로젝트 초기화와 인프라 구성

```bash
mkdir -p 18-workspace-saas-api/go && cd 18-workspace-saas-api/go
go mod init github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api
```

디렉터리 구조 설계. cmd/ 아래 api, worker, migrate 세 개의 바이너리. internal/ 아래 7개 패키지로 도메인 분리.

```bash
mkdir -p cmd/{api,worker,migrate}
mkdir -p internal/{auth,cache,httpapi,platform,repository,service,worker}
mkdir -p migrations scripts e2e seed
```

Docker Compose 작성 — PostgreSQL 16 Alpine + Redis 7 Alpine:

```bash
cat > docker-compose.yml << 'EOF'
services:
  postgres:
    image: postgres:16-alpine
    container_name: workspace-saas-postgres
    environment:
      POSTGRES_DB: workspace_saas
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "54339:5432"
  redis:
    image: redis:7-alpine
    container_name: workspace-saas-redis
    ports:
      - "6381:6379"
EOF
```

포트가 54339, 6381인 이유: 로컬에서 다른 프로젝트의 Postgres(54321~54338), Redis(6379~6380)와 충돌을 피하기 위해.

```bash
docker compose up -d postgres redis
```

헬스체크로 준비 완료 대기:

```bash
until docker compose exec -T postgres pg_isready -U postgres -d workspace_saas; do sleep 1; done
until docker compose exec -T redis redis-cli ping | grep -q PONG; do sleep 1; done
```

---

## Phase 1 — 의존성 설치

```bash
go get github.com/jackc/pgx/v5@v5.8.0
go get github.com/google/uuid@v1.6.0
go get github.com/redis/go-redis/v9@v9.18.0
go get golang.org/x/crypto@v0.48.0
```

- `pgx/v5`: PostgreSQL 드라이버 + connection pool (pgxpool)
- `google/uuid`: UUIDv4 생성 (PK 전략)
- `go-redis/v9`: Redis 클라이언트 (세션 캐시 + 대시보드 캐시)
- `x/crypto`: bcrypt 패스워드 해싱

go.sum 생성 확인:

```bash
go mod tidy
```

---

## Phase 2 — 마이그레이션 스키마 설계

`migrations/001_init.sql` 작성. 10개 테이블:

1. `users` — email UNIQUE, password_hash, display_name
2. `organizations` — slug UNIQUE
3. `organization_memberships` — (organization_id, user_id) UNIQUE, role CHECK
4. `invitations` — token_hash UNIQUE, 부분인덱스 (pending 상태의 org+email)
5. `projects` — (organization_id, project_key) UNIQUE
6. `issues` — version 낙관적 잠금, 멱등키 부분인덱스
7. `comments`
8. `refresh_sessions` — replaced_by, revoked_at (토큰 순환 추적)
9. `outbox_events` — published_at IS NULL 부분인덱스
10. `notifications` — (user_id, source_event_id) UNIQUE (멱등)

`migrations/embed.go`에서 `//go:embed *.sql`로 SQL 파일 임베드.

```bash
# migrate 바이너리로 적용
go run ./cmd/migrate up
```

환경 변수:

```
DATABASE_URL=postgres://postgres:postgres@localhost:54339/workspace_saas?sslmode=disable
```

---

## Phase 3 — platform 패키지 (횡단 관심사)

가장 먼저 구현. 다른 모든 패키지가 의존하는 기반 코드:

- `config.go`: 12개 환경 변수 로딩 (PORT, APP_ENV, DATABASE_URL, REDIS_ADDR, JWT_SECRET, WORKER_POLL_INTERVAL 등)
- `errors.go`: AppError (StatusCode, Code, Message, Err), ErrBadRequest/ErrUnauthorized/ErrForbidden/ErrNotFound/ErrConflict 팩토리 함수
- `httputil.go`: WriteJSON, DecodeJSON 헬퍼
- `metrics.go`: atomic.Int64 기반 5개 카운터 (requests, issues_created, auth_logins, auth_refreshes, errors), Prometheus text format Handler

---

## Phase 4 — auth 패키지 (토큰 생성/검증)

```
internal/auth/tokens.go
```

- HMAC-SHA256 JWT: Header.Payload.Signature, base64url 인코딩
- Claims: user_id, email, display_name, exp (15분)
- Refresh token: `crypto/rand` 32바이트 → hex 인코딩 (64자)
- 저장: SHA256(opaque_token) → DB의 token_hash 컬럼
- ParseRefreshToken: hex decode → SHA256 해시 → DB 조회

테스트:

```bash
go test ./internal/auth/ -v -count=1
```

---

## Phase 5 — repository 패키지 (데이터 액세스)

`internal/repository/` 아래 파일별 책임 분리:

- `models.go`: 10+ 도메인 모델 구조체
- `user.go`: CreateUser, GetUserByEmail, GetUserByID
- `organization.go`: CreateOrganization, AddMembership, GetMembership, ListMemberships
- `invitation.go`: CreateInvitation, GetInvitationByToken, AcceptInvitation
- `project.go`: CreateProject, ListProjects, GetProject
- `issue.go`: CreateIssue, GetIssue, ListIssues, UpdateIssue (version 낙관적 잠금)
- `comment.go`: CreateComment, ListComments
- `session.go`: CreateRefreshSession, GetRefreshSession, RevokeSession, RevokeAllUserSessions
- `outbox.go`: InsertOutboxEvent, FetchUnpublished, MarkPublished
- `notification.go`: InsertNotification, ListNotifications
- `dashboard.go`: GetDashboardSummary (COUNT 쿼리 집합)

모든 함수가 `context.Context`와 `pgx.Tx` 또는 `*pgxpool.Pool`을 받는 패턴.

---

## Phase 6 — cache 패키지 (Redis)

```
internal/cache/redis.go
```

- `NewClient`: go-redis/v9 클라이언트 생성, Ping으로 연결 확인
- `SetRefreshSession` / `GetRefreshSession`: 세션 JSON → Redis SET/GET (TTL = 세션 만료시간)
- `SetDashboard` / `GetDashboard`: 대시보드 요약 JSON → Redis SET/GET (30초 TTL)
- `InvalidateDashboard`: DEL 명령
- `Ping` / `Close`: 헬스체크와 정리

Redis 장애 시 에러를 로깅만 하고 nil 반환 → 호출자가 DB fallback.

---

## Phase 7 — service 패키지 (비즈니스 로직)

```
internal/service/service.go
```

모든 유즈케이스를 하나의 Service 구조체에. Repository + Cache + Auth를 주입받는 구조:

- RegisterOwner: 사용자 생성 → 조직 생성 → owner 멤버십 → 토큰 발급
- Login: 이메일 조회 → bcrypt 비교 → 세션/토큰 발급
- RefreshToken: 세션 검증 → 토큰 순환 → 새 세션 → 새 토큰
- Logout: 세션 폐기
- InviteMember: 멤버십 권한 확인 → 토큰 생성 → 초대 INSERT
- AcceptInvitation: 토큰 검증 → 사용자 생성/조회 → 멤버십 추가 → 초대 수락
- CreateIssue: 멤버십 확인 → 이슈 INSERT → outbox INSERT (같은 TX)
- UpdateIssue: 낙관적 잠금(version WHERE 절)
- GetDashboard: Redis 캐시 hit → miss 시 DB 조회 → 캐시 저장

---

## Phase 8 — httpapi 패키지 (HTTP 서버)

```
internal/httpapi/server.go
internal/httpapi/middleware.go
internal/httpapi/handlers.go
```

`http.NewServeMux()` 기반 17개 라우트:

```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/refresh
POST /api/auth/logout
POST /api/orgs/{orgID}/invitations
POST /api/invitations/accept
GET  /api/orgs/{orgID}/members
POST /api/orgs/{orgID}/projects
GET  /api/orgs/{orgID}/projects
POST /api/orgs/{orgID}/projects/{projectID}/issues
GET  /api/orgs/{orgID}/projects/{projectID}/issues
PATCH /api/orgs/{orgID}/issues/{issueID}
POST /api/orgs/{orgID}/issues/{issueID}/comments
GET  /api/orgs/{orgID}/issues/{issueID}/comments
GET  /api/orgs/{orgID}/dashboard
GET  /api/orgs/{orgID}/notifications
GET  /metrics
```

인프라 엔드포인트: `/healthz`, `/readyz` (Redis ping 포함).

미들웨어 체인: withObservability → requireAuth(선택적) → appHandler.

```bash
# API 서버 실행
PORT=4080 APP_ENV=development \
  DATABASE_URL=postgres://postgres:postgres@localhost:54339/workspace_saas?sslmode=disable \
  REDIS_ADDR=localhost:6381 \
  JWT_SECRET=workspace-saas-secret \
  go run ./cmd/api
```

---

## Phase 9 — worker 패키지 (알림 워커)

```
internal/worker/worker.go
cmd/worker/main.go
```

별도 바이너리. 폴링 루프:

1. outbox_events에서 unpublished 건 조회
2. 이벤트별 조직 멤버 조회 → 알림 INSERT (actor 제외)
3. 대시보드 캐시 무효화 (Redis DEL)
4. outbox published_at 마킹

```bash
# Worker 실행
APP_ENV=development \
  DATABASE_URL=postgres://postgres:postgres@localhost:54339/workspace_saas?sslmode=disable \
  REDIS_ADDR=localhost:6381 \
  JWT_SECRET=workspace-saas-secret \
  WORKER_POLL_INTERVAL=250ms \
  go run ./cmd/worker
```

---

## Phase 10 — Seed 데이터

```bash
go run ./cmd/migrate seed
```

`seed/` 디렉터리의 SQL로 테스트용 사용자, 조직, 프로젝트 삽입. INSERT ON CONFLICT DO NOTHING으로 멱등.

---

## Phase 11 — 테스트

### 단위 테스트

```bash
go test ./... -count=1
go test -race ./... -count=1
```

### E2E 테스트

```bash
# DB + Redis 필요
make e2e
# 또는 직접:
DATABASE_URL=... REDIS_ADDR=... JWT_SECRET=... \
  go test -tags=e2e ./e2e -v -count=1
```

빌드 태그 `e2e`로 분리. 실제 Postgres, Redis에 연결하여 API 호출 → 응답 검증.

### Smoke 테스트

```bash
make smoke
```

`scripts/smoke.sh` — curl 기반 시나리오. API 서버와 Worker를 백그라운드로 띄우고 전체 플로우 검증:
1. 사용자 등록 → 로그인 → 토큰 획득
2. 초대 → 수락
3. 프로젝트 생성 → 이슈 생성
4. Worker 처리 대기 → 알림 확인
5. 대시보드 조회

---

## Phase 12 — 전체 재현성 검증

```bash
make repro
```

한 명령으로 전체 검증:

```
make up → make migrate → make seed → make test → make test-race → make e2e → make smoke
```

---

## Phase 13 — Demo Capture

```bash
make demo-capture
```

`scripts/demo_capture.sh` — 프레젠테이션용 아티팩트 생성. 실제 API 호출의 요청/응답을 캡처하여 문서화에 활용.

---

## 주요 환경 변수 정리

| 변수 | 기본값 | 용도 |
|---|---|---|
| `PORT` | `4080` | API 서버 포트 |
| `APP_ENV` | `development` | 환경 구분 |
| `DATABASE_URL` | `postgres://...54339/workspace_saas` | PostgreSQL 연결 |
| `REDIS_ADDR` | `localhost:6381` | Redis 연결 |
| `JWT_SECRET` | `workspace-saas-secret` | HMAC-SHA256 서명 키 |
| `WORKER_POLL_INTERVAL` | `250ms` | Outbox 폴링 주기 |

## 사용된 도구 버전

| 도구 | 버전 |
|---|---|
| Go | 1.24.0 |
| PostgreSQL | 16-alpine |
| Redis | 7-alpine |
| pgx/v5 | 5.8.0 |
| go-redis/v9 | 9.18.0 |
| google/uuid | 1.6.0 |
| x/crypto | 0.48.0 |
