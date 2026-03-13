# 18 Workspace SaaS API Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: JWT auth, 조직 단위 RBAC, async notification, Redis cache를 한 제품형 API로 묶은 대표 포트폴리오 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/internal/auth/tokens.go`, `solution/go/internal/worker/worker.go`, `solution/go/e2e/workspace_flow_test.go`
- 대표 검증 명령: `cd solution/go && go test -v ./internal/auth ./internal/worker`, `cd solution/go && go test -run TestRunOncePublishesNotifications -v ./internal/worker`
- 핵심 개념 축: `organization이 tenant boundary이고, role은 membership에 붙는다.`, `access token은 짧게, refresh token은 회전시키며 Redis에 필수 상태를 둔다.`, `write flow는 issue/comment 이벤트를 outbox에 남기고 worker가 notification으로 변환한다.`, `dashboard summary는 org 단위 aggregate이며 Redis 캐시 miss 또는 장애 시 DB로 fallback 한다.`
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

                ### 1. Phase 1 - token, repository, store로 tenant, auth 바닥을 먼저 세운다

        - 당시 목표: token, repository, store로 tenant, auth 바닥을 먼저 세운다
        - 변경 단위: `solution/go/internal/auth/tokens.go`의 `SignAccessToken`
        - 처음 가설: `SignAccessToken`를 먼저 세워야 tenant 경계와 auth 토큰 규칙을 이후 API layer와 분리해 설명할 수 있다고 봤다.
        - 실제 조치: `solution/go/internal/auth/tokens.go`의 `SignAccessToken`를 중심으로 tenant-aware auth와 persistence contract를 먼저 세웠다.
        - CLI: `cd solution/go && go test -v ./internal/auth ./internal/worker`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestAccessTokenRoundTrip`였다.
        - 핵심 코드 앵커:
        - `SignAccessToken`: `solution/go/internal/auth/tokens.go`

        ```go
        // SignAccessToken은 HMAC으로 서명한 JWT 호환 액세스 토큰을 만든다.
func SignAccessToken(secret []byte, claims Claims) (string, error) {
	header := base64.RawURLEncoding.EncodeToString([]byte(`{"alg":"HS256","typ":"JWT"}`))
	payloadBytes, err := json.Marshal(claims)
	if err != nil {
		return "", err
	}
	payload := base64.RawURLEncoding.EncodeToString(payloadBytes)
	unsigned := header + "." + payload
	signature := sign(secret, unsigned)
        ```

        - 새로 배운 것: organization이 tenant boundary이고, role은 membership에 붙는다.
        - 다음: http server와 worker로 web request와 async notification을 분리한다
        ### 2. Phase 2 - http server와 worker로 web request와 async notification을 분리한다

        - 당시 목표: http server와 worker로 web request와 async notification을 분리한다
        - 변경 단위: `solution/go/internal/worker/worker.go`의 `Processor.RunOnce`
        - 처음 가설: `Processor.RunOnce`에 async notification 흐름을 모아 두면 API request path와 worker path를 명확히 분리할 수 있다고 판단했다.
        - 실제 조치: `solution/go/internal/worker/worker.go`의 `Processor.RunOnce`에 API request path와 async notification path를 분리해 실서비스 구조를 드러냈다.
        - CLI: `cd solution/go && go test -run TestRunOncePublishesNotifications -v ./internal/worker`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestRunOncePublishesNotifications`였다.
        - 핵심 코드 앵커:
        - `Processor.RunOnce`: `solution/go/internal/worker/worker.go`

        ```go
        }
func (p *Processor) RunOnce(ctx context.Context) (int, error) {
	events, err := p.store.ListUnpublishedOutbox(ctx, 50)
	if err != nil {
		return 0, err
	}

	processed := 0
	for _, event := range events {
		recipients, err := p.store.ListRecipients(ctx, event.OrganizationID, event.ActorUserID)
        ```

        - 새로 배운 것: notification worker를 별도 프로세스로 분리하면 구조는 분명해지지만 로컬 검증 절차가 늘어난다.
        - 다음: e2e와 smoke-ready 구조로 제품형 흐름 전체를 재현한다
        ### 3. Phase 3 - e2e와 smoke-ready 구조로 제품형 흐름 전체를 재현한다

        - 당시 목표: e2e와 smoke-ready 구조로 제품형 흐름 전체를 재현한다
        - 변경 단위: `solution/go/e2e/workspace_flow_test.go`의 `TestWorkspaceSaaSFlow`
        - 처음 가설: `TestWorkspaceSaaSFlow` 같은 e2e가 있어야 RBAC, outbox, cache가 한 제품형 흐름으로 닫힌다고 봤다.
        - 실제 조치: `solution/go/e2e/workspace_flow_test.go`의 `TestWorkspaceSaaSFlow`와 e2e를 함께 돌려 owner, member, worker, cache 흐름이 한 번에 이어지는지 확인했다.
        - CLI: `cd solution/go && go test -run TestRunOncePublishesNotifications -v ./internal/worker`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestRunOncePublishesNotifications`였다.
        - 핵심 코드 앵커:
        - `TestWorkspaceSaaSFlow`: `solution/go/e2e/workspace_flow_test.go`

        ```go
        func TestWorkspaceSaaSFlow(t *testing.T) {
	t.Parallel()

	ctx := context.Background()
	cfg := platform.LoadConfig()
	store, err := repository.Open(ctx, cfg.DatabaseURL)
	if err != nil {
		t.Fatalf("open store: %v", err)
	}
        ```

        - 새로 배운 것: idempotency key를 단순 unique로만 쓰면 동일 키의 다른 payload 충돌을 설명하기 어렵다.
        - 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/05-portfolio-projects/18-workspace-saas-api && cd solution/go && go test -v ./internal/auth ./internal/worker)
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
ok  	github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/auth	0.453s
=== RUN   TestRunOncePublishesNotifications
=== PAUSE TestRunOncePublishesNotifications
=== CONT  TestRunOncePublishesNotifications
--- PASS: TestRunOncePublishesNotifications (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/worker	0.868s
```

```bash
(cd /Users/woopinbell/work/book-task-3/study/05-portfolio-projects/18-workspace-saas-api && cd solution/go && go test -run TestRunOncePublishesNotifications -v ./internal/worker)
```

```text
=== RUN   TestRunOncePublishesNotifications
=== PAUSE TestRunOncePublishesNotifications
=== CONT  TestRunOncePublishesNotifications
--- PASS: TestRunOncePublishesNotifications (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/05-portfolio-projects/18-workspace-saas-api/internal/worker	0.263s
```
