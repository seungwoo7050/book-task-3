# 18 Workspace SaaS API Structure

## 이 글이 답할 질문

- Postgres + Redis 기반 local reproducibility와 smoke script를 README 표면에 올렸다.
- worker와 API를 바이너리 수준에서 분리해 async notification과 web request 경계를 명확히 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `05-portfolio-projects/18-workspace-saas-api` 안에서 `30-repository-service-cache-boundaries.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 5 — repository 패키지 (데이터 액세스) -> Phase 6 — cache 패키지 (Redis) -> Phase 7 — service 패키지 (비즈니스 로직)
- 세션 본문: `internal/repository/, models.go, user.go, organization.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/repository/store.go`
- 코드 앵커 2: `solution/go/internal/service/service.go`
- 코드 설명 초점: 이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.
- 개념 설명: write flow는 issue/comment 이벤트를 outbox에 남기고 worker가 notification으로 변환한다.
- 마지막 단락: 다음 글에서는 `40-http-worker-seed-and-smoke-surface.md`에서 이어지는 경계를 다룬다.
