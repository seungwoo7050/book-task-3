# 09 Cache Migrations Observability Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: cache-aside, cache invalidation, migration, metrics, trace header를 한 API로 묶어 운영 기본기를 붙이는 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/internal/app/app.go`, `solution/go/internal/app/app_test.go`
- 대표 검증 명령: `cd solution/go && go test -v ./internal/app`, `cd solution/go && go test -run TestMetricsEndpoint -v ./internal/app`
- 핵심 개념 축: `cache-aside는 읽기 시 캐시를 먼저 보고, miss면 DB를 읽어 캐시에 채우는 패턴이다.`, `쓰기 후 invalidation을 빼먹으면 stale data가 남는다.`, `structured logging은 trace id, path, method 같은 필드를 일관되게 남기는 습관이다.`, /metrics`는 서비스 상태를 외부에서 긁어 갈 수 있는 최소 관측 지점이다.
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

                ### 1. Phase 1 - ApplyUpMigration과 Service로 캐시 가능한 데이터 경계를 먼저 세운다

        - 당시 목표: ApplyUpMigration과 Service로 캐시 가능한 데이터 경계를 먼저 세운다
        - 변경 단위: `solution/go/internal/app/app.go`의 `ApplyUpMigration`
        - 처음 가설: `ApplyUpMigration` 쪽에서 상태 경계를 먼저 세우면 HTTP layer는 훨씬 단순해질 것이라고 봤다.
        - 실제 조치: `solution/go/internal/app/app.go`의 `ApplyUpMigration`를 기준으로 상태와 저장소 경계를 먼저 고정했다.
        - CLI: `cd solution/go && go test -v ./internal/app`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestCacheHitMiss`였다.
        - 핵심 코드 앵커:
        - `ApplyUpMigration`: `solution/go/internal/app/app.go`

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

        - 새로 배운 것: cache-aside는 읽기 시 캐시를 먼저 보고, miss면 DB를 읽어 캐시에 채우는 패턴이다.
        - 다음: metrics, trace, update endpoint로 관측 표면을 붙인다
        ### 2. Phase 2 - metrics, trace, update endpoint로 관측 표면을 붙인다

        - 당시 목표: metrics, trace, update endpoint로 관측 표면을 붙인다
        - 변경 단위: `solution/go/internal/app/app.go`의 `NewService`
        - 처음 가설: `NewService`에 transport 규칙을 모아 두면 validation과 응답 shape를 한곳에서 설명할 수 있다고 판단했다.
        - 실제 조치: `solution/go/internal/app/app.go`의 `NewService`를 통해 transport, validation, auth or cache surface를 노출했다.
        - CLI: `cd solution/go && go test -run TestMetricsEndpoint -v ./internal/app`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestMetricsEndpoint`였다.
        - 핵심 코드 앵커:
        - `NewService`: `solution/go/internal/app/app.go`

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

        - 새로 배운 것: trace backend 없이 trace id만 남기면 상호 연동은 없지만 요청 상관관계는 잡을 수 있다.
        - 다음: app_test로 cache hit/miss와 invalidation 계약을 잠근다
        ### 3. Phase 3 - app_test로 cache hit/miss와 invalidation 계약을 잠근다

        - 당시 목표: app_test로 cache hit/miss와 invalidation 계약을 잠근다
        - 변경 단위: `solution/go/internal/app/app_test.go`의 `TestCacheHitMiss`
        - 처음 가설: `TestCacheHitMiss` 같은 테스트가 있어야 handler, auth, cache 계약이 서로 섞이지 않는다고 봤다.
        - 실제 조치: `solution/go/internal/app/app_test.go`의 `TestCacheHitMiss`를 중심으로 handler contract와 edge case를 묶어 재검증 루프를 닫았다.
        - CLI: `cd solution/go && go test -run TestMetricsEndpoint -v ./internal/app`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestMetricsEndpoint`였다.
        - 핵심 코드 앵커:
        - `TestCacheHitMiss`: `solution/go/internal/app/app_test.go`

        ```go
        func TestCacheHitMiss(t *testing.T) {
	t.Parallel()

	service, cleanup := newService(t)
	defer cleanup()

	if _, err := service.GetItem(context.Background(), 1); err != nil {
		t.Fatalf("first get: %v", err)
	}
        ```

        - 새로 배운 것: metrics를 텍스트로 직접 쓰면 간단하지만 라벨 모델링은 제한적이다.
        - 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

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
