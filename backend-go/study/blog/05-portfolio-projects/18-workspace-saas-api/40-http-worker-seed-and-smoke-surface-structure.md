# 18 Workspace SaaS API Structure

## 이 글이 답할 질문

- Postgres + Redis 기반 local reproducibility와 smoke script를 README 표면에 올렸다.
- worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `05-portfolio-projects/18-workspace-saas-api` 안에서 `40-http-worker-seed-and-smoke-surface.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 8 — httpapi 패키지 (HTTP 서버) -> Phase 9 — worker 패키지 (알림 워커) -> Phase 10 — Seed 데이터 -> Phase 11 — 테스트
- 세션 본문: `internal/httpapi/server.go, internal/httpapi/middleware.go, internal/httpapi/handlers.go, internal/worker/worker.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/httpapi/server.go`
- 코드 앵커 2: `solution/go/internal/worker/worker.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: dashboard summary는 org 단위 aggregate이며 Redis 캐시 miss 또는 장애 시 DB로 fallback 한다.
- 마지막 단락: 다음 글에서는 `50-repro-demo-and-portfolio-proof.md`에서 이어지는 경계를 다룬다.
