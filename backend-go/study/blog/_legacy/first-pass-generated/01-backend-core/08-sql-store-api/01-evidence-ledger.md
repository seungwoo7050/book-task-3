# 08 SQL Store API Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: SQLite 기반 CRUD API에 migration, optimistic update, transaction rollback을 결합한 백엔드 코어 중심 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/internal/store/store.go`, `solution/go/internal/store/store_test.go`
- 대표 검증 명령: `cd solution/go && go test -v ./internal/store`, `cd solution/go && go test -run TestReserveStockRollback -v ./internal/store`
- 핵심 개념 축: `migration up/down은 스키마를 코드와 같이 추적하기 위한 최소 장치다.`, `repository는 handler가 SQL 세부 사항을 직접 알지 않게 분리해 준다.`, optimistic update는 `version` 조건으로 충돌을 감지한다., `transaction rollback은 실패한 재고 차감이 반만 남지 않게 한다.`
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

                ### 1. Phase 1 - ApplyUpMigration과 Repository로 저장소 경계를 먼저 세운다

        - 당시 목표: ApplyUpMigration과 Repository로 저장소 경계를 먼저 세운다
        - 변경 단위: `solution/go/internal/store/store.go`의 `ApplyUpMigration`
        - 처음 가설: `ApplyUpMigration` 쪽에서 상태 경계를 먼저 세우면 HTTP layer는 훨씬 단순해질 것이라고 봤다.
        - 실제 조치: `solution/go/internal/store/store.go`의 `ApplyUpMigration`를 기준으로 상태와 저장소 경계를 먼저 고정했다.
        - CLI: `cd solution/go && go test -v ./internal/store`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestMigrationUpDown`였다.
        - 핵심 코드 앵커:
        - `ApplyUpMigration`: `solution/go/internal/store/store.go`

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

        - 새로 배운 것: migration up/down은 스키마를 코드와 같이 추적하기 위한 최소 장치다.
        - 다음: NewApp과 server main으로 store-backed API surface를 연결한다
        ### 2. Phase 2 - NewApp과 server main으로 store-backed API surface를 연결한다

        - 당시 목표: NewApp과 server main으로 store-backed API surface를 연결한다
        - 변경 단위: `solution/go/internal/store/store.go`의 `NewApp`
        - 처음 가설: `NewApp`에 transport 규칙을 모아 두면 validation과 응답 shape를 한곳에서 설명할 수 있다고 판단했다.
        - 실제 조치: `solution/go/internal/store/store.go`의 `NewApp`를 통해 transport, validation, auth or cache surface를 노출했다.
        - CLI: `cd solution/go && go test -run TestReserveStockRollback -v ./internal/store`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestReserveStockRollback`였다.
        - 핵심 코드 앵커:
        - `NewApp`: `solution/go/internal/store/store.go`

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

        - 새로 배운 것: repository 추상화는 테스트성을 높이지만 지나치면 작은 예제를 복잡하게 만들 수 있다.
        - 다음: store_test로 migration, CRUD, rollback 계약을 잠근다
        ### 3. Phase 3 - store_test로 migration, CRUD, rollback 계약을 잠근다

        - 당시 목표: store_test로 migration, CRUD, rollback 계약을 잠근다
        - 변경 단위: `solution/go/internal/store/store_test.go`의 `TestReserveStockRollback`
        - 처음 가설: `TestReserveStockRollback` 같은 테스트가 있어야 handler, auth, cache 계약이 서로 섞이지 않는다고 봤다.
        - 실제 조치: `solution/go/internal/store/store_test.go`의 `TestReserveStockRollback`를 중심으로 handler contract와 edge case를 묶어 재검증 루프를 닫았다.
        - CLI: `cd solution/go && go test -run TestReserveStockRollback -v ./internal/store`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestReserveStockRollback`였다.
        - 핵심 코드 앵커:
        - `TestReserveStockRollback`: `solution/go/internal/store/store_test.go`

        ```go
        func TestReserveStockRollback(t *testing.T) {
	t.Parallel()

	repo, db := newTestRepo(t)
	defer db.Close()

	product := Product{Name: "sword", Stock: 2}
	if err := repo.Create(context.Background(), &product); err != nil {
		t.Fatalf("create: %v", err)
        ```

        - 새로 배운 것: migration down을 아예 테스트하지 않으면 나중에 롤백 감각이 약해진다.
        - 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

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
