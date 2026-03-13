# 08 SQL Store API — Sql Store And Migrations

`01-backend-core/08-sql-store-api`는 SQLite 기반 CRUD API에 migration, optimistic update, transaction rollback을 결합한 백엔드 코어 중심 과제다. 이 글에서는 1단계: 프로젝트 초기화 -> 2단계: 외부 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: 스키마 정의 (store.go) -> 5단계: DB 연결 및 마이그레이션 함수 -> 6단계: Product 구조체 및 Repository 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 1단계: 프로젝트 초기화
- 2단계: 외부 의존성 설치
- 3단계: 디렉토리 구조 생성
- 4단계: 스키마 정의 (store.go)
- 5단계: DB 연결 및 마이그레이션 함수
- 6단계: Product 구조체 및 Repository

## Day 1
### Session 1

- 당시 목표: `database/sql` 기반 CRUD API를 구현해야 한다.
- 변경 단위: `require modernc.org/sqlite v1.38.2`
- 처음 가설: DB 접근은 `database/sql`과 repository 계층으로 감싸 ORM 없이 경계를 드러냈다.
- 실제 진행: `go.mod`에 `require modernc.org/sqlite v1.38.2`와 간접 의존성들이 추가된다. Repository 메서드 순서: `Create` — INSERT, LastInsertId로 ID 취득 `Get` — SELECT + Scan, sql.ErrNoRows 처리 `List` — QueryContext + rows.Next 순회 `Update` — WHERE version = ? 조건으로 optimistic update `ReserveStock` — BeginTx + 재고 확인 + UPDATE + Commit/Rollback

CLI:

```bash
cd study/01-backend-core/08-sql-store-api/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/08-sql-store-api

go get modernc.org/sqlite
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/internal/store/store.go`

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

왜 이 코드가 중요했는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

새로 배운 것:

- migration up/down은 스키마를 코드와 같이 추적하기 위한 최소 장치다.

보조 코드: `solution/go/cmd/server/main.go`

```go
func main() {
	db, err := store.OpenInMemory()
	if err != nil {
		log.Fatal(err)
	}
	if err := store.ApplyUpMigration(context.Background(), db); err != nil {
		log.Fatal(err)
	}

	app := store.NewApp(store.NewRepository(db))
	log.Println("listening on :4040")
	log.Fatal(http.ListenAndServe(":4040", app.Routes()))
}
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

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

- 다음 글에서는 `20-http-surface-optimistic-update-and-rollback.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/store/store.go` 같은 결정적인 코드와 `cd 01-backend-core/08-sql-store-api/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
