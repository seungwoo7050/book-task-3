# 18 Workspace SaaS API Structure Outline

이 문서는 chronology ledger를 바탕으로 최종 blog를 어떤 순서로 전개할지 먼저 고정한 설계 메모다. 기존 `blog/` 초안은 입력에서 제외했고, 실제 코드, README, docs, 테스트, CLI만을 근거로 삼는다.

## Planned Files

- `00-series-map.md`: 프로젝트 범위, source-of-truth, 읽는 순서를 잡는 진입 문서
- `01-evidence-ledger.md`: 파일, 함수, CLI 단위 chronology를 거칠게 복원한 근거 문서
- `10-2026-03-13-reconstructed-development-log.md`: 구현 순서와 판단 전환점을 세션 흐름으로 다시 쓴 최종 blog

## Final Blog Flow

- 도입: README 한 줄 요약과 이번 재검증 범위를 붙여 글의 위치를 먼저 밝힌다.
- 구현 순서 요약: Phase 1 -> Phase 2 -> Phase 3 순서를 미리 보여 준다.
- 세션형 chronology: 각 phase에서 당시 목표, 가설, 조치, 코드 앵커, 검증 신호를 순서대로 다시 적는다.
- CLI로 닫는 구간: 현재 저장소에서 다시 실행한 명령과 excerpt를 붙여 README 계약이 아직 살아 있는지 확인한다.
- 남은 질문: 개념 축과 다음 실험 지점을 남긴다.

## Section Plan

### 1. Phase 1 - token, repository, store로 tenant, auth 바닥을 먼저 세운다

- 목표: token, repository, store로 tenant, auth 바닥을 먼저 세운다
- 변경 단위: `solution/go/internal/auth/tokens.go`의 `SignAccessToken`
- 핵심 가설: `SignAccessToken`를 먼저 세워야 tenant 경계와 auth 토큰 규칙을 이후 API layer와 분리해 설명할 수 있다고 봤다.
- 반드시 넣을 코드 앵커: `SignAccessToken`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestAccessTokenRoundTrip`였다.
- 새로 배운 것 섹션 포인트: organization이 tenant boundary이고, role은 membership에 붙는다.
- 다음 섹션 연결 문장: http server와 worker로 web request와 async notification을 분리한다
### 2. Phase 2 - http server와 worker로 web request와 async notification을 분리한다

- 목표: http server와 worker로 web request와 async notification을 분리한다
- 변경 단위: `solution/go/internal/worker/worker.go`의 `Processor.RunOnce`
- 핵심 가설: `Processor.RunOnce`에 async notification 흐름을 모아 두면 API request path와 worker path를 명확히 분리할 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `Processor.RunOnce`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestRunOncePublishesNotifications`였다.
- 새로 배운 것 섹션 포인트: notification worker를 별도 프로세스로 분리하면 구조는 분명해지지만 로컬 검증 절차가 늘어난다.
- 다음 섹션 연결 문장: e2e와 smoke-ready 구조로 제품형 흐름 전체를 재현한다
### 3. Phase 3 - e2e와 smoke-ready 구조로 제품형 흐름 전체를 재현한다

- 목표: e2e와 smoke-ready 구조로 제품형 흐름 전체를 재현한다
- 변경 단위: `solution/go/e2e/workspace_flow_test.go`의 `TestWorkspaceSaaSFlow`
- 핵심 가설: `TestWorkspaceSaaSFlow` 같은 e2e가 있어야 RBAC, outbox, cache가 한 제품형 흐름으로 닫힌다고 봤다.
- 반드시 넣을 코드 앵커: `TestWorkspaceSaaSFlow`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestRunOncePublishesNotifications`였다.
- 새로 배운 것 섹션 포인트: idempotency key를 단순 unique로만 쓰면 동일 키의 다른 payload 충돌을 설명하기 어렵다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/05-portfolio-projects/18-workspace-saas-api && cd solution/go && go test -v ./internal/auth ./internal/worker)
```

```text
=== RUN   TestAccessTokenRoundTrip
=== PAUSE TestAccessTokenRoundTrip
=== RUN   TestRefreshTokenRoundTrip
=== PAUSE TestRefreshTokenRoundTrip
=== CONT  TestAccessTokenRoundTrip
=== CONT  TestRefreshTokenRoundTrip
--- PASS: TestRefreshTokenRoundTrip (0.00s)
--- PASS: TestAccessTokenRoundTrip (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/auth	(cached)
=== RUN   TestRunOncePublishesNotifications
=== PAUSE TestRunOncePublishesNotifications
=== CONT  TestRunOncePublishesNotifications
--- PASS: TestRunOncePublishesNotifications (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/worker	(cached)
```

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/05-portfolio-projects/18-workspace-saas-api && cd solution/go && go test -run TestRunOncePublishesNotifications -v ./internal/worker)
```

```text
=== RUN   TestRunOncePublishesNotifications
=== PAUSE TestRunOncePublishesNotifications
=== CONT  TestRunOncePublishesNotifications
--- PASS: TestRunOncePublishesNotifications (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/worker	(cached)
```
