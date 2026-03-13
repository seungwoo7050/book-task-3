# 08 SQL Store API 재구성 개발 로그

08 SQL Store API는 SQLite 기반 CRUD API에 migration, optimistic update, transaction rollback을 결합한 백엔드 코어 중심 과제다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: ApplyUpMigration과 Repository로 저장소 경계를 먼저 세운다 - `solution/go/internal/store/store.go`의 `ApplyUpMigration`
- Phase 2: NewApp과 server main으로 store-backed API surface를 연결한다 - `solution/go/internal/store/store.go`의 `NewApp`
- Phase 3: store_test로 migration, CRUD, rollback 계약을 잠근다 - `solution/go/internal/store/store_test.go`의 `TestReserveStockRollback`

                ## Phase 1. ApplyUpMigration과 Repository로 저장소 경계를 먼저 세운다

        - 당시 목표: ApplyUpMigration과 Repository로 저장소 경계를 먼저 세운다
        - 변경 단위: `solution/go/internal/store/store.go`의 `ApplyUpMigration`
        - 처음 가설: `ApplyUpMigration` 쪽에서 상태 경계를 먼저 세우면 HTTP layer는 훨씬 단순해질 것이라고 봤다.
        - 실제 진행: `solution/go/internal/store/store.go`의 `ApplyUpMigration`를 기준으로 상태와 저장소 경계를 먼저 고정했다.
        - CLI: `cd solution/go && go test -v ./internal/store`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestMigrationUpDown`였다.

        핵심 코드:

        ```go
        func ApplyUpMigration(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, schemaUp)
	return err
}

func ApplyDownMigration(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, schemaDown)
	return err
}
        ```

        왜 이 코드가 중요했는가: `ApplyUpMigration`는 `solution/go/internal/store/store.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: migration up/down은 스키마를 코드와 같이 추적하기 위한 최소 장치다.
        - 다음: NewApp과 server main으로 store-backed API surface를 연결한다
        ## Phase 2. NewApp과 server main으로 store-backed API surface를 연결한다

        - 당시 목표: NewApp과 server main으로 store-backed API surface를 연결한다
        - 변경 단위: `solution/go/internal/store/store.go`의 `NewApp`
        - 처음 가설: `NewApp`에 transport 규칙을 모아 두면 validation과 응답 shape를 한곳에서 설명할 수 있다고 판단했다.
        - 실제 진행: `solution/go/internal/store/store.go`의 `NewApp`를 통해 transport, validation, auth or cache surface를 노출했다.
        - CLI: `cd solution/go && go test -run TestReserveStockRollback -v ./internal/store`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestReserveStockRollback`였다.

        핵심 코드:

        ```go
        func NewApp(repo *Repository) *App {
	return &App{repo: repo}
}

func (r *Repository) Create(ctx context.Context, product *Product) error {
	result, err := r.db.ExecContext(ctx, `INSERT INTO products(name, stock) VALUES (?, ?)`, product.Name, product.Stock)
	if err != nil {
		return err
	}
        ```

        왜 이 코드가 중요했는가: `NewApp`는 `solution/go/internal/store/store.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: repository 추상화는 테스트성을 높이지만 지나치면 작은 예제를 복잡하게 만들 수 있다.
        - 다음: store_test로 migration, CRUD, rollback 계약을 잠근다
        ## Phase 3. store_test로 migration, CRUD, rollback 계약을 잠근다

        - 당시 목표: store_test로 migration, CRUD, rollback 계약을 잠근다
        - 변경 단위: `solution/go/internal/store/store_test.go`의 `TestReserveStockRollback`
        - 처음 가설: `TestReserveStockRollback` 같은 테스트가 있어야 handler, auth, cache 계약이 서로 섞이지 않는다고 봤다.
        - 실제 진행: `solution/go/internal/store/store_test.go`의 `TestReserveStockRollback`를 중심으로 handler contract와 edge case를 묶어 재검증 루프를 닫았다.
        - CLI: `cd solution/go && go test -run TestReserveStockRollback -v ./internal/store`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestReserveStockRollback`였다.

        핵심 코드:

        ```go
        func TestReserveStockRollback(t *testing.T) {
	t.Parallel()

	repo, db := newTestRepo(t)
	defer db.Close()

	product := Product{Name: "sword", Stock: 2}
	if err := repo.Create(context.Background(), &product); err != nil {
		t.Fatalf("create: %v", err)
        ```

        왜 이 코드가 중요했는가: `TestReserveStockRollback`는 `solution/go/internal/store/store_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: migration down을 아예 테스트하지 않으면 나중에 롤백 감각이 약해진다.
        - 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

                ## CLI 1. 현재 저장소에서 다시 돌린 검증

                ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/08-sql-store-api && cd solution/go && go test -v ./internal/store)
```

```text
=== RUN   TestMigrationUpDown
=== PAUSE TestMigrationUpDown
=== RUN   TestRepositoryCRUD
=== PAUSE TestRepositoryCRUD
=== RUN   TestReserveStockRollback
=== PAUSE TestReserveStockRollback
=== RUN   TestCreateProductValidation
=== PAUSE TestCreateProductValidation
=== CONT  TestMigrationUpDown
=== CONT  TestReserveStockRollback
=== CONT  TestCreateProductValidation
=== CONT  TestRepositoryCRUD
--- PASS: TestCreateProductValidation (0.00s)
--- PASS: TestReserveStockRollback (0.00s)
--- PASS: TestMigrationUpDown (0.00s)
--- PASS: TestRepositoryCRUD (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/08-sql-store-api/internal/store	(cached)
```
        ## CLI 2. 현재 저장소에서 다시 돌린 검증

                ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/08-sql-store-api && cd solution/go && go test -run TestReserveStockRollback -v ./internal/store)
```

```text
=== RUN   TestReserveStockRollback
=== PAUSE TestReserveStockRollback
=== CONT  TestReserveStockRollback
--- PASS: TestReserveStockRollback (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/08-sql-store-api/internal/store	(cached)
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: `migration up/down은 스키마를 코드와 같이 추적하기 위한 최소 장치다.`, `repository는 handler가 SQL 세부 사항을 직접 알지 않게 분리해 준다.`, optimistic update는 `version` 조건으로 충돌을 감지한다., `transaction rollback은 실패한 재고 차감이 반만 남지 않게 한다.`
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: migration 가능한 저장소와 HTTP app을 같이 세워 CRUD와 재고 reserve rollback을 설명한다.
