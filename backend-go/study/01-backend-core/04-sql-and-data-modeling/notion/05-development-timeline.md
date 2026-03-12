# 개발 타임라인 — 처음부터 끝까지

이 문서는 프로젝트 04를 처음부터 완성까지 만드는 전체 과정을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 뼈대와 의존성

### 1-1. 디렉터리 구조 생성

```bash
mkdir -p 01-backend-core/04-sql-and-data-modeling/{solution/go/cmd/schemawalk,solution/go/catalog,docs/concepts,docs/references,problem}
```

### 1-2. Go 모듈 초기화 및 의존성 설치

```bash
cd 01-backend-core/04-sql-and-data-modeling/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling
go get modernc.org/sqlite
```

이 프로젝트부터 처음으로 외부 의존성을 사용한다. `modernc.org/sqlite`는 순수 Go로 구현된 SQLite 드라이버로, CGO 없이 동작한다. `go get`을 실행하면 `go.mod`에 `require` 줄이 추가되고 `go.sum`이 생성된다.

### 1-3. Workspace 등록

```bash
cd study
go work use 01-backend-core/04-sql-and-data-modeling/go
```

---

## Phase 2: 스키마 설계

### 2-1. SQL 스키마 작성 (`solution/go/catalog/catalog.go`)

세 테이블의 DDL을 Go 상수로 작성했다:
- `players`: 플레이어 (id, name)
- `items`: 아이템 (id, name, price_cents)
- `inventory`: 인벤토리 (player_id, item_id, quantity) — composite PK

CHECK constraint로 `price_cents > 0`, `quantity > 0`을 보장했다. INDEX는 `inventory(player_id)`에 추가해서 페이어별 조회를 빠르게 했다.

### 2-2. DB 연결 함수 (`OpenInMemory`)

`sql.Open("sqlite", ...)` 으로 in-memory DB를 연다. `cache=shared`와 고유 타임스탬프를 사용해서 병렬 테스트 간 DB 격리를 보장했다.

### 2-3. 스키마 적용 함수 (`ApplySchema`)

`db.ExecContext(ctx, schema)`로 DDL을 실행. 에러만 반환하는 단순한 함수.

### 2-4. 시드 데이터 함수 (`Seed`)

alice, bob 플레이어와 potion, sword 아이템, alice의 potion 2개를 초기 데이터로 삽입.

---

## Phase 3: 쿼리 구현

### 3-1. ListInventory — JOIN 쿼리

세 테이블을 JOIN해서 플레이어 이름으로 인벤토리를 조회. 파라미터 바인딩(`?`)으로 SQL injection 방지. `rows.Close()`를 `defer`로 확실히 정리.

`InventoryRow` struct를 반환 타입으로 정의해서 DB 행을 Go 타입으로 매핑했다.

### 3-2. Purchase — 트랜잭션

```go
tx, err := db.BeginTx(ctx, nil)
defer tx.Rollback()  // 실패 시 자동 롤백
```

1. 아이템 이름으로 ID 조회 (`tx.QueryRowContext`)
2. inventory에 UPSERT (`ON CONFLICT ... DO UPDATE`)
3. 성공하면 `tx.Commit()`

존재하지 않는 아이템이면 `ErrUnknownItem` sentinel error를 반환. `sql.ErrNoRows`와 `errors.Is`로 비교했다.

---

## Phase 4: CLI 바이너리 작성

### 4-1. main.go 작성 (`solution/go/cmd/schemawalk/main.go`)

DB 열기 → 스키마 적용 → 시드 → alice 인벤토리 조회 → 출력. `defer db.Close()`로 DB 정리.

### 4-2. 첫 실행

```bash
cd solution/go
go run ./cmd/schemawalk
# alice owns 2 x potion
```

---

## Phase 5: 테스트 작성

### 5-1. 테스트 헬퍼 (`newTestDB`)

매 테스트마다 새 in-memory DB를 만들고 스키마와 시드를 적용. `t.Helper()`로 에러 위치를 올바르게 표시.

### 5-2. 테스트 케이스

| 테스트 | 검증 대상 |
|--------|-----------|
| `TestListInventory` | alice의 인벤토리에 potion이 있는지 |
| `TestPurchase` | sword 구매 후 인벤토리가 2행이 되는지 |
| `TestPurchaseUnknownItem` | 없는 아이템 구매 시 `ErrUnknownItem` 반환 |

### 5-3. 테스트 실행

```bash
cd solution/go
go test ./...
go test -v ./catalog/

# === RUN   TestListInventory
# --- PASS
# === RUN   TestPurchase
# --- PASS
# === RUN   TestPurchaseUnknownItem
# --- PASS
```

---

## Phase 6: 문서 작성 및 최종 검증

### 6-1. 문서 시스템

| 파일 | 내용 |
|------|------|
| `problem/README.md` | 과제 명세 |
| `docs/README.md` | 문서 개요 |
| `docs/concepts/core-concepts.md` | 스키마 설계, JOIN, 트랜잭션 핵심 개념 |
| `docs/references/README.md` | 참고 자료 |
| `docs/verification.md` | 검증 기록 |

### 6-2. 최종 검증

```bash
cd study
make test-new
make check-docs
```

`verified` 상태 확정.

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| Go 1.24+ | 컴파일, 실행, 테스트 |
| `modernc.org/sqlite` | 순수 Go SQLite 드라이버 |
| `go get` | 외부 패키지 의존성 설치 |
| `database/sql` | Go 표준 DB 인터페이스 |
| `make` | 전체 검증 |

Docker나 외부 DB 서버 불필요. `go test`만으로 모든 것이 검증된다.
