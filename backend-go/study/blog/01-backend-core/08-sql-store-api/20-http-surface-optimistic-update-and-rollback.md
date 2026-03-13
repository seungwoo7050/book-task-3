# 08 SQL Store API — Http Surface Optimistic Update And Rollback

`01-backend-core/08-sql-store-api`는 SQLite 기반 CRUD API에 migration, optimistic update, transaction rollback을 결합한 백엔드 코어 중심 과제다. 이 글에서는 7단계: 에러 정의 -> 8단계: App 구조체와 라우트 -> 9단계: 핸들러 구현 -> 10단계: main.go 작성 -> 11단계: 테스트 작성 (store_test.go) -> 12단계: 실행 및 API 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 7단계: 에러 정의
- 8단계: App 구조체와 라우트
- 9단계: 핸들러 구현
- 10단계: main.go 작성
- 11단계: 테스트 작성 (store_test.go)
- 12단계: 실행 및 API 검증

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/internal/store/store_test.go`, `solution/go/internal/store/store.go`
- 처음 가설: optimistic update와 rollback을 같은 과제에 묶어 이후 정합성 과제의 발판으로 삼았다.
- 실제 진행: 각 핸들러의 패턴: JSON 디코딩 → 입력 검증 → Repository 호출 → 에러 매핑 → JSON 응답 에러 매핑: `ErrNotFound` → 404 `ErrConflict` → 409 검증 실패 → 422 포트 4040 사용. 테스트 목록: `TestMigrationUpDown` — up 후 down하면 테이블 없음 확인 `TestRepositoryCRUD` — Create → Get → Update → List `TestReserveStockRollback` — 재고 초과 시 rollback, 원래 수량 유지 `TestCreateProductValidation` — name="" → 422

CLI:

```bash
go test ./internal/store/...

go run ./cmd/server
```

검증 신호:

- 2026-03-07 기준 `go test ./...`가 통과했다.
- 테스트는 migration up/down, CRUD, optimistic update, rollback 성격의 재고 예약을 포함한다.
- 남은 선택 검증: 외부 DB 연결과 connection pool 조정은 다루지 않았다.

핵심 코드: `solution/go/internal/store/store_test.go`

```go
func newTestRepo(t *testing.T) (*Repository, *sql.DB) {
	t.Helper()
	db, err := OpenInMemory()
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	if err := ApplyUpMigration(context.Background(), db); err != nil {
		t.Fatalf("apply migration: %v", err)
	}
	return NewRepository(db), db
}

func TestMigrationUpDown(t *testing.T) {
	t.Parallel()

	db, err := OpenInMemory()
	if err != nil {
		t.Fatalf("open db: %v", err)
```

왜 이 코드가 중요했는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

새로 배운 것:

- repository는 handler가 SQL 세부 사항을 직접 알지 않게 분리해 준다.

보조 코드: `solution/go/internal/store/store.go`

```go
var (
	ErrNotFound          = errors.New("product not found")
	ErrConflict          = errors.New("version conflict")
	ErrInsufficientStock = errors.New("insufficient stock")
)

const schemaUp = `
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    stock INTEGER NOT NULL CHECK (stock >= 0),
    version INTEGER NOT NULL DEFAULT 1
);
`

const schemaDown = `DROP TABLE IF EXISTS products;`

type Product struct {
```

왜 이 코드도 같이 봐야 하는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

CLI:

```bash
cd 01-backend-core/08-sql-store-api/go
go run ./cmd/server
go test ./...
```

검증 신호:

- 2026-03-07 기준 `go test ./...`가 통과했다.
- 테스트는 migration up/down, CRUD, optimistic update, rollback 성격의 재고 예약을 포함한다.

다음:

- 외부 DB 연결과 connection pool 조정은 다루지 않았다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/store/store_test.go` 같은 결정적인 코드와 `cd 01-backend-core/08-sql-store-api/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
