# 18 Workspace SaaS API Evidence Ledger

## 40 http-worker-seed-and-smoke-surface

- 시간 표지: Phase 8 — httpapi 패키지 (HTTP 서버) -> Phase 9 — worker 패키지 (알림 워커) -> Phase 10 — Seed 데이터 -> Phase 11 — 테스트
- 당시 목표: Postgres + Redis 기반 local reproducibility와 smoke script를 README 표면에 올렸다.
- 변경 단위: `internal/httpapi/server.go`, `internal/httpapi/middleware.go`, `internal/httpapi/handlers.go`, `internal/worker/worker.go`, `cmd/worker/main.go`, `seed/`
- 처음 가설: worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 실제 조치: `http.NewServeMux()` 기반 17개 라우트: 인프라 엔드포인트: `/healthz`, `/readyz` (Redis ping 포함). 별도 바이너리. 폴링 루프: outbox_events에서 unpublished 건 조회 이벤트별 조직 멤버 조회 → 알림 INSERT (actor 제외) 대시보드 캐시 무효화 (Redis DEL) outbox published_at 마킹

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

- 검증 신호:
- Smoke 테스트
- `scripts/smoke.sh` — curl 기반 시나리오. API 서버와 Worker를 백그라운드로 띄우고 전체 플로우 검증:
- make smoke
- 핵심 코드 앵커: `solution/go/internal/httpapi/server.go`
- 새로 배운 것: dashboard summary는 org 단위 aggregate이며 Redis 캐시 miss 또는 장애 시 DB로 fallback 한다.
- 다음: 다음 글에서는 `50-repro-demo-and-portfolio-proof.md`에서 이어지는 경계를 다룬다.
