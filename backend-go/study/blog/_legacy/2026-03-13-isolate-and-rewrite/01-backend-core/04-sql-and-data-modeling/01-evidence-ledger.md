# 04 SQL And Data Modeling Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: 스키마 설계, join, transaction을 게임 상점 예제로 묶어 SQL 기초를 백엔드 문맥에서 익히는 브리지 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/catalog/catalog.go`, `solution/go/catalog/catalog_test.go`
- 대표 검증 명령: `cd solution/go && go run ./cmd/schemawalk`, `cd solution/go && go test ./...`
- 핵심 개념 축: `players`, `items`, `inventory` 분리는 다대다 관계를 명시적으로 드러낸다., `PRIMARY KEY (player_id, item_id)`는 같은 아이템의 중복 행 생성을 막는다., join query는 정규화된 데이터를 읽기 쉬운 뷰로 복원하는 단계다., transaction은 “재고 갱신이 반만 되는 상태”를 막는 최소 단위다.
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

### 1. Phase 1 - ApplySchema와 Seed로 데이터 모델의 바닥을 먼저 깐다

- 당시 목표: ApplySchema와 Seed로 데이터 모델의 바닥을 먼저 깐다
- 변경 단위: `solution/go/catalog/catalog.go`의 `ApplySchema`
- 처음 가설: `ApplySchema`를 먼저 고정하면 I/O보다 데이터 규칙을 더 선명하게 설명할 수 있다고 봤다.
- 실제 조치: `solution/go/catalog/catalog.go`의 `ApplySchema`를 중심으로 입력을 쪼개고, 계산 규칙을 작은 함수 단위로 고정했다.
- CLI: `cd solution/go && go run ./cmd/schemawalk`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `alice owns 2 x potion`였다.
- 핵심 코드 앵커:
- `ApplySchema`: `solution/go/catalog/catalog.go`

```go
func ApplySchema(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, schema)
	return err
}

func Seed(ctx context.Context, db *sql.DB) error {
	statements := []string{
		`INSERT INTO players(id, name) VALUES (1, 'alice'), (2, 'bob')`,
		`INSERT INTO items(id, name, price_cents) VALUES (1, 'potion', 300), (2, 'sword', 1500)`,
```

- 새로 배운 것: `players`, `items`, `inventory` 분리는 다대다 관계를 명시적으로 드러낸다.
- 다음: Purchase와 schemawalk CLI로 SQL 경로를 노출한다
### 2. Phase 2 - Purchase와 schemawalk CLI로 SQL 경로를 노출한다

- 당시 목표: Purchase와 schemawalk CLI로 SQL 경로를 노출한다
- 변경 단위: `solution/go/catalog/catalog.go`의 `Purchase`
- 처음 가설: `Purchase`를 중심에 두면 demo entrypoint는 얇은 연결층으로 남길 수 있다고 판단했다.
- 실제 조치: `solution/go/catalog/catalog.go`의 `Purchase`와 demo entrypoint를 연결해 사람이 읽는 출력 surface를 만들었다.
- CLI: `cd solution/go && go test ./...`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `ok  	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/catalog	(cached)`였다.
- 핵심 코드 앵커:
- `Purchase`: `solution/go/catalog/catalog.go`

```go
func Purchase(ctx context.Context, db *sql.DB, playerID int, itemName string, quantity int) error {
	if quantity <= 0 {
		return fmt.Errorf("quantity must be positive")
	}

	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
```

- 새로 배운 것: SQLite in-memory는 입문에는 좋지만 실제 운영 DB의 락/격리 수준과는 다르다.
- 다음: catalog_test로 재고 차감과 rollback 계약을 잠근다
### 3. Phase 3 - catalog_test로 재고 차감과 rollback 계약을 잠근다

- 당시 목표: catalog_test로 재고 차감과 rollback 계약을 잠근다
- 변경 단위: `solution/go/catalog/catalog_test.go`의 `TestPurchase`
- 처음 가설: 테스트 이름 `TestPurchase`처럼 계약을 먼저 못 박아야 구현이 흔들리지 않는다고 봤다.
- 실제 조치: `solution/go/catalog/catalog_test.go`의 `TestPurchase`를 통해 regression or benchmark loop를 남겨 다음 단계 실험이 가능하게 했다.
- CLI: `cd solution/go && go test ./...`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `ok  	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/catalog	(cached)`였다.
- 핵심 코드 앵커:
- `TestPurchase`: `solution/go/catalog/catalog_test.go`

```go
func TestPurchase(t *testing.T) {
	t.Parallel()

	db := newTestDB(t)
	if err := Purchase(context.Background(), db.DB, 1, "sword", 1); err != nil {
		t.Fatalf("purchase: %v", err)
	}
	rows, err := ListInventory(context.Background(), db.DB, "alice")
	if err != nil {
```

- 새로 배운 것: `quantity <= 0` 같은 제약을 SQL과 애플리케이션 양쪽에서 동시에 생각하지 않으면 빈틈이 생긴다.
- 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/04-sql-and-data-modeling && cd solution/go && go run ./cmd/schemawalk)
```

```text
alice owns 2 x potion
```

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/04-sql-and-data-modeling && cd solution/go && go test ./...)
```

```text
ok  	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/catalog	(cached)
?   	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/cmd/schemawalk	[no test files]
```
