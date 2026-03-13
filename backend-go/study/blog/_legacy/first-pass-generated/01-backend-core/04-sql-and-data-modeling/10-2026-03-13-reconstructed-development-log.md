# 04 SQL And Data Modeling 재구성 개발 로그

04 SQL And Data Modeling는 스키마 설계, join, transaction을 게임 상점 예제로 묶어 SQL 기초를 백엔드 문맥에서 익히는 브리지 과제다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: ApplySchema와 Seed로 데이터 모델의 바닥을 먼저 깐다 - `solution/go/catalog/catalog.go`의 `ApplySchema`
- Phase 2: Purchase와 schemawalk CLI로 SQL 경로를 노출한다 - `solution/go/catalog/catalog.go`의 `Purchase`
- Phase 3: catalog_test로 재고 차감과 rollback 계약을 잠근다 - `solution/go/catalog/catalog_test.go`의 `TestPurchase`

                ## Phase 1. ApplySchema와 Seed로 데이터 모델의 바닥을 먼저 깐다

        - 당시 목표: ApplySchema와 Seed로 데이터 모델의 바닥을 먼저 깐다
        - 변경 단위: `solution/go/catalog/catalog.go`의 `ApplySchema`
        - 처음 가설: `ApplySchema`를 먼저 고정하면 I/O보다 데이터 규칙을 더 선명하게 설명할 수 있다고 봤다.
        - 실제 진행: `solution/go/catalog/catalog.go`의 `ApplySchema`를 중심으로 입력을 쪼개고, 계산 규칙을 작은 함수 단위로 고정했다.
        - CLI: `cd solution/go && go run ./cmd/schemawalk`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `alice owns 2 x potion`였다.

        핵심 코드:

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

        왜 이 코드가 중요했는가: `ApplySchema`는 `solution/go/catalog/catalog.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: players`, `items`, `inventory` 분리는 다대다 관계를 명시적으로 드러낸다.
        - 다음: Purchase와 schemawalk CLI로 SQL 경로를 노출한다
        ## Phase 2. Purchase와 schemawalk CLI로 SQL 경로를 노출한다

        - 당시 목표: Purchase와 schemawalk CLI로 SQL 경로를 노출한다
        - 변경 단위: `solution/go/catalog/catalog.go`의 `Purchase`
        - 처음 가설: `Purchase`를 중심에 두면 demo entrypoint는 얇은 연결층으로 남길 수 있다고 판단했다.
        - 실제 진행: `solution/go/catalog/catalog.go`의 `Purchase`와 demo entrypoint를 연결해 사람이 읽는 출력 surface를 만들었다.
        - CLI: `cd solution/go && go test ./...`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `ok  	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/catalog	(cached)`였다.

        핵심 코드:

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

        왜 이 코드가 중요했는가: `Purchase`는 `solution/go/catalog/catalog.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: SQLite in-memory는 입문에는 좋지만 실제 운영 DB의 락/격리 수준과는 다르다.
        - 다음: catalog_test로 재고 차감과 rollback 계약을 잠근다
        ## Phase 3. catalog_test로 재고 차감과 rollback 계약을 잠근다

        - 당시 목표: catalog_test로 재고 차감과 rollback 계약을 잠근다
        - 변경 단위: `solution/go/catalog/catalog_test.go`의 `TestPurchase`
        - 처음 가설: 테스트 이름 `TestPurchase`처럼 계약을 먼저 못 박아야 구현이 흔들리지 않는다고 봤다.
        - 실제 진행: `solution/go/catalog/catalog_test.go`의 `TestPurchase`를 통해 regression or benchmark loop를 남겨 다음 단계 실험이 가능하게 했다.
        - CLI: `cd solution/go && go test ./...`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `ok  	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/catalog	(cached)`였다.

        핵심 코드:

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

        왜 이 코드가 중요했는가: `TestPurchase`는 `solution/go/catalog/catalog_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: quantity <= 0` 같은 제약을 SQL과 애플리케이션 양쪽에서 동시에 생각하지 않으면 빈틈이 생긴다.
        - 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

                ## CLI 1. 현재 저장소에서 다시 돌린 검증

        ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/04-sql-and-data-modeling && cd solution/go && go run ./cmd/schemawalk)
```

```text
alice owns 2 x potion
```
        ## CLI 2. 현재 저장소에서 다시 돌린 검증

                ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/04-sql-and-data-modeling && cd solution/go && go test ./...)
```

```text
ok  	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/catalog	(cached)
?   	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/cmd/schemawalk	[no test files]
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: players`, `items`, `inventory` 분리는 다대다 관계를 명시적으로 드러낸다., PRIMARY KEY (player_id, item_id)`는 같은 아이템의 중복 행 생성을 막는다., `join query는 정규화된 데이터를 읽기 쉬운 뷰로 복원하는 단계다.`, `transaction은 “재고 갱신이 반만 되는 상태”를 막는 최소 단위다.`
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: 메모리 DB 위에서 schema, seed, purchase 흐름을 가장 작은 SQL 계약으로 묶는다.
