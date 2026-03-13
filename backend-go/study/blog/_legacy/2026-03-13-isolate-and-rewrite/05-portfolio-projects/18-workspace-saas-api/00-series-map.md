# 18 Workspace SaaS API 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../../05-portfolio-projects/18-workspace-saas-api/README.md), [`problem/README.md`](../../../05-portfolio-projects/18-workspace-saas-api/problem/README.md)
- 구현 표면:
- `solution/go/internal/auth/tokens.go`
- `solution/go/internal/worker/worker.go`
- `solution/go/e2e/workspace_flow_test.go`
- 검증 표면: `cd solution/go && go test -v ./internal/auth ./internal/worker`, `cd solution/go && go test -run TestRunOncePublishesNotifications -v ./internal/worker`
- 개념 축: organization이 tenant boundary이고, role은 membership에 붙는다., access token은 짧게, refresh token은 회전시키며 Redis에 필수 상태를 둔다., write flow는 issue/comment 이벤트를 outbox에 남기고 worker가 notification으로 변환한다.

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

auth, org RBAC, outbox worker, Redis cache를 한 제출용 SaaS API로 재소유한다.
