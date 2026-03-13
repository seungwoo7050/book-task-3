# 09 Cache Migrations Observability 재구성 개발 로그

09 Cache Migrations Observability는 cache-aside, cache invalidation, migration, metrics, trace header를 한 API로 묶어 운영 기본기를 붙이는 과제다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: ApplyUpMigration과 Service로 캐시 가능한 데이터 경계를 먼저 세운다 - `solution/go/internal/app/app.go`의 `ApplyUpMigration`
- Phase 2: metrics, trace, update endpoint로 관측 표면을 붙인다 - `solution/go/internal/app/app.go`의 `NewService`
- Phase 3: app_test로 cache hit/miss와 invalidation 계약을 잠근다 - `solution/go/internal/app/app_test.go`의 `TestCacheHitMiss`

                ## Phase 1. ApplyUpMigration과 Service로 캐시 가능한 데이터 경계를 먼저 세운다

        - 당시 목표: ApplyUpMigration과 Service로 캐시 가능한 데이터 경계를 먼저 세운다
        - 변경 단위: `solution/go/internal/app/app.go`의 `ApplyUpMigration`
        - 처음 가설: `ApplyUpMigration` 쪽에서 상태 경계를 먼저 세우면 HTTP layer는 훨씬 단순해질 것이라고 봤다.
        - 실제 진행: `solution/go/internal/app/app.go`의 `ApplyUpMigration`를 기준으로 상태와 저장소 경계를 먼저 고정했다.
        - CLI: `cd solution/go && go test -v ./internal/app`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestCacheHitMiss`였다.

        핵심 코드:

        ```go
        func ApplyUpMigration(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, upMigration)
	return err
}

func ApplyDownMigration(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, downMigration)
	return err
}
        ```

        왜 이 코드가 중요했는가: `ApplyUpMigration`는 `solution/go/internal/app/app.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: cache-aside는 읽기 시 캐시를 먼저 보고, miss면 DB를 읽어 캐시에 채우는 패턴이다.
        - 다음: metrics, trace, update endpoint로 관측 표면을 붙인다
        ## Phase 2. metrics, trace, update endpoint로 관측 표면을 붙인다

        - 당시 목표: metrics, trace, update endpoint로 관측 표면을 붙인다
        - 변경 단위: `solution/go/internal/app/app.go`의 `NewService`
        - 처음 가설: `NewService`에 transport 규칙을 모아 두면 validation과 응답 shape를 한곳에서 설명할 수 있다고 판단했다.
        - 실제 진행: `solution/go/internal/app/app.go`의 `NewService`를 통해 transport, validation, auth or cache surface를 노출했다.
        - CLI: `cd solution/go && go test -run TestMetricsEndpoint -v ./internal/app`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestMetricsEndpoint`였다.

        핵심 코드:

        ```go
        func NewService(db *sql.DB, logger *slog.Logger) *Service {
	if logger == nil {
		logger = slog.Default()
	}
	return &Service{
		db:     db,
		logger: logger,
		cache:  make(map[int64]Item),
	}
        ```

        왜 이 코드가 중요했는가: `NewService`는 `solution/go/internal/app/app.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: trace backend 없이 trace id만 남기면 상호 연동은 없지만 요청 상관관계는 잡을 수 있다.
        - 다음: app_test로 cache hit/miss와 invalidation 계약을 잠근다
        ## Phase 3. app_test로 cache hit/miss와 invalidation 계약을 잠근다

        - 당시 목표: app_test로 cache hit/miss와 invalidation 계약을 잠근다
        - 변경 단위: `solution/go/internal/app/app_test.go`의 `TestCacheHitMiss`
        - 처음 가설: `TestCacheHitMiss` 같은 테스트가 있어야 handler, auth, cache 계약이 서로 섞이지 않는다고 봤다.
        - 실제 진행: `solution/go/internal/app/app_test.go`의 `TestCacheHitMiss`를 중심으로 handler contract와 edge case를 묶어 재검증 루프를 닫았다.
        - CLI: `cd solution/go && go test -run TestMetricsEndpoint -v ./internal/app`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestMetricsEndpoint`였다.

        핵심 코드:

        ```go
        func TestCacheHitMiss(t *testing.T) {
	t.Parallel()

	service, cleanup := newService(t)
	defer cleanup()

	if _, err := service.GetItem(context.Background(), 1); err != nil {
		t.Fatalf("first get: %v", err)
	}
        ```

        왜 이 코드가 중요했는가: `TestCacheHitMiss`는 `solution/go/internal/app/app_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: metrics를 텍스트로 직접 쓰면 간단하지만 라벨 모델링은 제한적이다.
        - 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

                ## CLI 1. 현재 저장소에서 다시 돌린 검증

                ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/09-cache-migrations-observability && cd solution/go && go test -v ./internal/app)
```

```text
=== RUN   TestCacheHitMiss
=== PAUSE TestCacheHitMiss
=== RUN   TestInvalidationOnUpdate
=== PAUSE TestInvalidationOnUpdate
=== RUN   TestMetricsEndpoint
=== PAUSE TestMetricsEndpoint
=== RUN   TestTraceHeader
=== PAUSE TestTraceHeader
=== RUN   TestUpdateEndpoint
=== PAUSE TestUpdateEndpoint
=== RUN   TestDownMigration
=== PAUSE TestDownMigration
=== CONT  TestCacheHitMiss
=== CONT  TestDownMigration
=== CONT  TestTraceHeader
=== CONT  TestMetricsEndpoint
=== CONT  TestUpdateEndpoint
=== CONT  TestInvalidationOnUpdate
--- PASS: TestDownMigration (0.00s)
--- PASS: TestMetricsEndpoint (0.00s)
--- PASS: TestCacheHitMiss (0.00s)
--- PASS: TestUpdateEndpoint (0.00s)
... (4 more lines)
```
        ## CLI 2. 현재 저장소에서 다시 돌린 검증

                ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/09-cache-migrations-observability && cd solution/go && go test -run TestMetricsEndpoint -v ./internal/app)
```

```text
=== RUN   TestMetricsEndpoint
=== PAUSE TestMetricsEndpoint
=== CONT  TestMetricsEndpoint
--- PASS: TestMetricsEndpoint (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/09-cache-migrations-observability/internal/app	(cached)
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: `cache-aside는 읽기 시 캐시를 먼저 보고, miss면 DB를 읽어 캐시에 채우는 패턴이다.`, `쓰기 후 invalidation을 빼먹으면 stale data가 남는다.`, `structured logging은 trace id, path, method 같은 필드를 일관되게 남기는 습관이다.`, /metrics`는 서비스 상태를 외부에서 긁어 갈 수 있는 최소 관측 지점이다.
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: cache invalidation, migration, metrics, trace header를 한 서비스로 묶는다.
