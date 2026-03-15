# 08-sql-store-api-go 문제지

## 왜 중요한가

상품 정보를 SQLite에 저장하는 작은 CRUD API를 만들고 optimistic update와 transaction rollback을 구현한다.

## 목표

시작 위치의 구현을 완성해 migration up/down 파일을 둔다, POST /v1/products, GET /v1/products를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/01-backend-core/08-sql-store-api/solution/go/cmd/server/main.go`
- `../study/01-backend-core/08-sql-store-api/solution/go/internal/store/store.go`
- `../study/01-backend-core/08-sql-store-api/solution/go/internal/store/store_test.go`
- `../study/01-backend-core/08-sql-store-api/problem/script/001_create_products.down.sql`
- `../study/01-backend-core/08-sql-store-api/problem/script/001_create_products.up.sql`
- `../study/01-backend-core/08-sql-store-api/solution/go/go.mod`
- `../study/01-backend-core/08-sql-store-api/solution/go/go.sum`

## starter code / 입력 계약

- `../study/01-backend-core/08-sql-store-api/solution/go/cmd/server/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- migration up/down 파일을 둔다.
- POST /v1/products
- GET /v1/products
- GET /v1/products/{id}
- PATCH /v1/products/{id}
- 재고 부족 시 transaction rollback을 수행한다.

## 제외 범위

- 외부 DB 엔진
- prepared statement tuning
- `../study/01-backend-core/08-sql-store-api/problem/script/001_create_products.down.sql` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `OpenInMemory`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `newTestRepo`와 `TestMigrationUpDown`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/01-backend-core/08-sql-store-api/problem/script/001_create_products.down.sql` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/08-sql-store-api/solution/go && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/08-sql-store-api/solution/go && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`08-sql-store-api-go_answer.md`](08-sql-store-api-go_answer.md)에서 확인한다.
