# 18 Workspace SaaS API Evidence Ledger

## 10 bootstrap-schema-and-platform

- 시간 표지: Phase 0 — 프로젝트 초기화와 인프라 구성 -> Phase 1 — 의존성 설치 -> Phase 2 — 마이그레이션 스키마 설계 -> Phase 3 — platform 패키지 (횡단 관심사)
- 당시 목표: 채용 제출용 B2B SaaS API를 로컬에서 완결형으로 재현할 수 있어야 한다.
- 변경 단위: `pgx/v5`, `google/uuid`, `go-redis/v9`, `x/crypto`, `migrations/001_init.sql`, `migrations/embed.go`
- 처음 가설: 이전 과제 코드를 의존성으로 가져오지 않고 대표작 내부에서 다시 소유해 제출용 완성도를 높였다.
- 실제 조치: 디렉터리 구조 설계. cmd/ 아래 api, worker, migrate 세 개의 바이너리. internal/ 아래 7개 패키지로 도메인 분리. Docker Compose 작성 — PostgreSQL 16 Alpine + Redis 7 Alpine: `pgx/v5`: PostgreSQL 드라이버 + connection pool (pgxpool) `google/uuid`: UUIDv4 생성 (PK 전략) `go-redis/v9`: Redis 클라이언트 (세션 캐시 + 대시보드 캐시) `x/crypto`: bcrypt 패스워드 해싱 go.sum 생성 확인:

CLI:

```bash
mkdir -p 18-workspace-saas-api/go && cd 18-workspace-saas-api/go
go mod init github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api

mkdir -p cmd/{api,worker,migrate}
mkdir -p internal/{auth,cache,httpapi,platform,repository,service,worker}
mkdir -p migrations scripts e2e seed
```

- 검증 신호:
- POSTGRES_PASSWORD: postgres
- until docker compose exec -T redis redis-cli ping | grep -q PONG; do sleep 1; done
- `invitations` — token_hash UNIQUE, 부분인덱스 (pending 상태의 org+email)
- `refresh_sessions` — replaced_by, revoked_at (토큰 순환 추적)
- 핵심 코드 앵커: `solution/go/migrations/001_init.sql`
- 새로 배운 것: organization이 tenant boundary이고, role은 membership에 붙는다.
- 다음: 다음 글에서는 `20-auth-and-session-rotation.md`에서 이어지는 경계를 다룬다.
