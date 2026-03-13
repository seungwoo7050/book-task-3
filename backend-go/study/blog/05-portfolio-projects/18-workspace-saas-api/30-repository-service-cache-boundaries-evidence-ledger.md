# 18 Workspace SaaS API Evidence Ledger

## 30 repository-service-cache-boundaries

- 시간 표지: Phase 5 — repository 패키지 (데이터 액세스) -> Phase 6 — cache 패키지 (Redis) -> Phase 7 — service 패키지 (비즈니스 로직)
- 당시 목표: Postgres + Redis 기반 local reproducibility와 smoke script를 README 표면에 올렸다.
- 변경 단위: `internal/repository/`, `models.go`, `user.go`, `organization.go`, `invitation.go`, `project.go`
- 처음 가설: worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 실제 조치: `internal/repository/` 아래 파일별 책임 분리: `models.go`: 10+ 도메인 모델 구조체 `user.go`: CreateUser, GetUserByEmail, GetUserByID `organization.go`: CreateOrganization, AddMembership, GetMembership, ListMemberships `invitation.go`: CreateInvitation, GetInvitationByToken, AcceptInvitation `project.go`: CreateProject, ListProjects, GetProject `issue.go`: CreateIssue, GetIssue, ListIssues, UpdateIssue (version 낙관적 잠금) `comment.go`: CreateComment, ListComments `session.go`: CreateRefreshSession, GetRefreshSession, RevokeSession, RevokeAllUserSessions `outbox.go`: InsertOutboxEvent, FetchUnpublished, MarkPublished `notification.go`: InsertNotification, ListNotifications `dashboard.go`: GetDashboardSummary (COUNT 쿼리 집합) `NewClient`: go-redis/v9 클라이언트 생성, Ping으로 연결 확인 `SetRefreshSession` / `GetRefreshSession`: 세션 JSON → Redis SET/GET (TTL = 세션 만료시간) `SetDashboard` / `GetDashboard`: 대시보드 요약 JSON → Redis SET/GET (30초 TTL) `InvalidateDashboard`: DEL 명령 `Ping` / `Close`: 헬스체크와 정리 Redis 장애 시 에러를 로깅만 하고 nil 반환 → 호출자가 DB fallback.

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

- 검증 신호:
- - `invitation.go`: CreateInvitation, GetInvitationByToken, AcceptInvitation
- - `session.go`: CreateRefreshSession, GetRefreshSession, RevokeSession, RevokeAllUserSessions
- - RefreshToken: 세션 검증 → 토큰 순환 → 새 세션 → 새 토큰
- 핵심 코드 앵커: `solution/go/internal/repository/store.go`
- 새로 배운 것: write flow는 issue/comment 이벤트를 outbox에 남기고 worker가 notification으로 변환한다.
- 다음: 다음 글에서는 `40-http-worker-seed-and-smoke-surface.md`에서 이어지는 경계를 다룬다.
