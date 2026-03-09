# 타임라인 — SQL Store API 개발 전체 과정

## 1단계: 프로젝트 초기화

```bash
cd study/01-backend-core/08-sql-store-api/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/08-sql-store-api
```

## 2단계: 외부 의존성 설치

```bash
go get modernc.org/sqlite
```

`go.mod`에 `require modernc.org/sqlite v1.38.2`와 간접 의존성들이 추가된다.

## 3단계: 디렉토리 구조 생성

```bash
mkdir -p internal/store
mkdir -p cmd/server
```

```
go/
├── go.mod
├── cmd/
│   └── server/
│       └── main.go
└── internal/
    └── store/
        ├── store.go
        └── store_test.go
```

## 4단계: 스키마 정의 (store.go)

```go
const schemaUp = `
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    stock INTEGER NOT NULL CHECK (stock >= 0),
    version INTEGER NOT NULL DEFAULT 1
);`

const schemaDown = `DROP TABLE IF EXISTS products;`
```

## 5단계: DB 연결 및 마이그레이션 함수

```go
func OpenInMemory() (*sql.DB, error) {
    return sql.Open("sqlite", fmt.Sprintf("file:sql-store-api-%d?mode=memory&cache=shared", time.Now().UnixNano()))
}

func ApplyUpMigration(ctx context.Context, db *sql.DB) error { ... }
func ApplyDownMigration(ctx context.Context, db *sql.DB) error { ... }
```

## 6단계: Product 구조체 및 Repository

```go
type Product struct {
    ID      int64  `json:"id"`
    Name    string `json:"name"`
    Stock   int    `json:"stock"`
    Version int    `json:"version"`
}
```

Repository 메서드 순서:
1. `Create` — INSERT, LastInsertId로 ID 취득
2. `Get` — SELECT + Scan, sql.ErrNoRows 처리
3. `List` — QueryContext + rows.Next 순회
4. `Update` — WHERE version = ? 조건으로 optimistic update
5. `ReserveStock` — BeginTx + 재고 확인 + UPDATE + Commit/Rollback

## 7단계: 에러 정의

```go
var (
    ErrNotFound          = errors.New("product not found")
    ErrConflict          = errors.New("version conflict")
    ErrInsufficientStock = errors.New("insufficient stock")
)
```

## 8단계: App 구조체와 라우트

```go
mux.HandleFunc("POST /v1/products", a.createProduct)
mux.HandleFunc("GET /v1/products", a.listProducts)
mux.HandleFunc("GET /v1/products/{id}", a.showProduct)
mux.HandleFunc("PATCH /v1/products/{id}", a.updateProduct)
```

## 9단계: 핸들러 구현

각 핸들러의 패턴:
- JSON 디코딩 → 입력 검증 → Repository 호출 → 에러 매핑 → JSON 응답

에러 매핑:
- `ErrNotFound` → 404
- `ErrConflict` → 409
- 검증 실패 → 422

## 10단계: main.go 작성

```go
db, _ := store.OpenInMemory()
store.ApplyUpMigration(context.Background(), db)
app := store.NewApp(store.NewRepository(db))
log.Println("listening on :4040")
http.ListenAndServe(":4040", app.Routes())
```

포트 4040 사용.

## 11단계: 테스트 작성 (store_test.go)

```bash
go test ./internal/store/...
```

테스트 목록:
- `TestMigrationUpDown` — up 후 down하면 테이블 없음 확인
- `TestRepositoryCRUD` — Create → Get → Update → List
- `TestReserveStockRollback` — 재고 초과 시 rollback, 원래 수량 유지
- `TestCreateProductValidation` — name="" → 422

## 12단계: 실행 및 API 검증

```bash
go run ./cmd/server
```

### 상품 생성

```bash
curl -X POST http://localhost:4040/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name":"potion","stock":10}'
```

### 전체 조회

```bash
curl http://localhost:4040/v1/products
```

### 단일 조회

```bash
curl http://localhost:4040/v1/products/1
```

### 수정 (optimistic update)

```bash
curl -X PATCH http://localhost:4040/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"super potion","stock":15,"version":1}'
```

### 버전 충돌 테스트

```bash
# 같은 version으로 두 번째 수정 시도 → 409
curl -X PATCH http://localhost:4040/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"mega potion","stock":20,"version":1}'
```

### 입력 검증 테스트

```bash
# name 비어있음 → 422
curl -X POST http://localhost:4040/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name":"","stock":1}'
```

## 파일 목록

| 순서 | 파일 | 설명 |
|------|------|------|
| 1 | `go.mod` | 모듈 정의, modernc.org/sqlite 의존성 |
| 2 | `internal/store/store.go` | Repository, App, 핸들러, 마이그레이션, 에러 |
| 3 | `internal/store/store_test.go` | CRUD, rollback, validation 테스트 |
| 4 | `cmd/server/main.go` | 엔트리포인트, :4040 |
