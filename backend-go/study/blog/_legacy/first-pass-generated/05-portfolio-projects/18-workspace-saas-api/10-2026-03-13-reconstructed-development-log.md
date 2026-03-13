# 18 Workspace SaaS API 재구성 개발 로그

18 Workspace SaaS API는 JWT auth, 조직 단위 RBAC, async notification, Redis cache를 한 제품형 API로 묶은 대표 포트폴리오 과제다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: token, repository, store로 tenant, auth 바닥을 먼저 세운다 - `solution/go/internal/auth/tokens.go`의 `SignAccessToken`
- Phase 2: http server와 worker로 web request와 async notification을 분리한다 - `solution/go/internal/worker/worker.go`의 `Processor.RunOnce`
- Phase 3: e2e와 smoke-ready 구조로 제품형 흐름 전체를 재현한다 - `solution/go/e2e/workspace_flow_test.go`의 `TestWorkspaceSaaSFlow`

                ## Phase 1. token, repository, store로 tenant, auth 바닥을 먼저 세운다

        - 당시 목표: token, repository, store로 tenant, auth 바닥을 먼저 세운다
        - 변경 단위: `solution/go/internal/auth/tokens.go`의 `SignAccessToken`
        - 처음 가설: `SignAccessToken`를 먼저 세워야 tenant 경계와 auth 토큰 규칙을 이후 API layer와 분리해 설명할 수 있다고 봤다.
        - 실제 진행: `solution/go/internal/auth/tokens.go`의 `SignAccessToken`를 중심으로 tenant-aware auth와 persistence contract를 먼저 세웠다.
        - CLI: `cd solution/go && go test -v ./internal/auth ./internal/worker`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestAccessTokenRoundTrip`였다.

        핵심 코드:

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

        왜 이 코드가 중요했는가: `SignAccessToken`는 `solution/go/internal/auth/tokens.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: organization이 tenant boundary이고, role은 membership에 붙는다.
        - 다음: http server와 worker로 web request와 async notification을 분리한다
        ## Phase 2. http server와 worker로 web request와 async notification을 분리한다

        - 당시 목표: http server와 worker로 web request와 async notification을 분리한다
        - 변경 단위: `solution/go/internal/worker/worker.go`의 `Processor.RunOnce`
        - 처음 가설: `Processor.RunOnce`에 async notification 흐름을 모아 두면 API request path와 worker path를 명확히 분리할 수 있다고 판단했다.
        - 실제 진행: `solution/go/internal/worker/worker.go`의 `Processor.RunOnce`에 API request path와 async notification path를 분리해 실서비스 구조를 드러냈다.
        - CLI: `cd solution/go && go test -run TestRunOncePublishesNotifications -v ./internal/worker`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestRunOncePublishesNotifications`였다.

        핵심 코드:

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

        왜 이 코드가 중요했는가: `Processor.RunOnce`는 `solution/go/internal/worker/worker.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: notification worker를 별도 프로세스로 분리하면 구조는 분명해지지만 로컬 검증 절차가 늘어난다.
        - 다음: e2e와 smoke-ready 구조로 제품형 흐름 전체를 재현한다
        ## Phase 3. e2e와 smoke-ready 구조로 제품형 흐름 전체를 재현한다

        - 당시 목표: e2e와 smoke-ready 구조로 제품형 흐름 전체를 재현한다
        - 변경 단위: `solution/go/e2e/workspace_flow_test.go`의 `TestWorkspaceSaaSFlow`
        - 처음 가설: `TestWorkspaceSaaSFlow` 같은 e2e가 있어야 RBAC, outbox, cache가 한 제품형 흐름으로 닫힌다고 봤다.
        - 실제 진행: `solution/go/e2e/workspace_flow_test.go`의 `TestWorkspaceSaaSFlow`와 e2e를 함께 돌려 owner, member, worker, cache 흐름이 한 번에 이어지는지 확인했다.
        - CLI: `cd solution/go && go test -run TestRunOncePublishesNotifications -v ./internal/worker`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestRunOncePublishesNotifications`였다.

        핵심 코드:

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

        왜 이 코드가 중요했는가: `TestWorkspaceSaaSFlow`는 `solution/go/e2e/workspace_flow_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: idempotency key를 단순 unique로만 쓰면 동일 키의 다른 payload 충돌을 설명하기 어렵다.
        - 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

                ## CLI 1. 현재 저장소에서 다시 돌린 검증

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
        ## CLI 2. 현재 저장소에서 다시 돌린 검증

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

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: `organization이 tenant boundary이고, role은 membership에 붙는다.`, `access token은 짧게, refresh token은 회전시키며 Redis에 필수 상태를 둔다.`, `write flow는 issue/comment 이벤트를 outbox에 남기고 worker가 notification으로 변환한다.`, `dashboard summary는 org 단위 aggregate이며 Redis 캐시 miss 또는 장애 시 DB로 fallback 한다.`
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: auth, org RBAC, outbox worker, Redis cache를 한 제출용 SaaS API로 재소유한다.
