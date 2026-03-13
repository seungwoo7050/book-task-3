# 04 SQL And Data Modeling — Transaction And Verification Loop

`01-backend-core/04-sql-and-data-modeling`는 스키마 설계, join, transaction을 게임 상점 예제로 묶어 SQL 기초를 백엔드 문맥에서 익히는 브리지 과제다. 이 글에서는 Phase 4: CLI 바이너리 작성 -> Phase 5: 테스트 작성 -> Phase 6: 문서 작성 및 최종 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 4: CLI 바이너리 작성
- Phase 5: 테스트 작성
- Phase 6: 문서 작성 및 최종 검증

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/cmd/schemawalk/main.go`, `problem/README.md`, `docs/README.md`, `docs/concepts/core-concepts.md`, `docs/references/README.md`, `docs/verification.md`
- 처음 가설: 실제 migration tool은 뒤로 미루고 데이터 모델과 transaction 경계를 먼저 학습하게 했다.
- 실제 진행: main.go 작성 (`solution/go/cmd/schemawalk/main.go`) DB 열기 → 스키마 적용 → 시드 → alice 인벤토리 조회 → 출력. `defer db.Close()`로 DB 정리. 테스트 헬퍼 (`newTestDB`) 매 테스트마다 새 in-memory DB를 만들고 스키마와 시드를 적용. `t.Helper()`로 에러 위치를 올바르게 표시.

CLI:

```bash
cd solution/go
go run ./cmd/schemawalk
# alice owns 2 x potion

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

검증 신호:

- DB 열기 → 스키마 적용 → 시드 → alice 인벤토리 조회 → 출력. `defer db.Close()`로 DB 정리.
- --- PASS
- 2026-03-07 기준 `go run ./cmd/schemawalk`가 정상 실행됐다.
- 2026-03-07 기준 `go test ./...`가 통과했다.
- 남은 선택 검증: 실제 migration binary와 외부 RDBMS 연결은 다음 과제에서 다룬다.

핵심 코드: `solution/go/catalog/catalog_test.go`

```go
func newTestDB(t *testing.T) *sqlDB {
	t.Helper()
	db, err := OpenInMemory()
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	ctx := context.Background()
	if err := ApplySchema(ctx, db); err != nil {
		t.Fatalf("apply schema: %v", err)
	}
	if err := Seed(ctx, db); err != nil {
		t.Fatalf("seed: %v", err)
	}
	return &sqlDB{db}
}

type sqlDB struct{ *sql.DB }
```

왜 이 코드가 중요했는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

새로 배운 것:

- `PRIMARY KEY (player_id, item_id)`는 같은 아이템의 중복 행 생성을 막는다.

보조 코드: `solution/go/cmd/schemawalk/main.go`

```go
func main() {
	ctx := context.Background()
	db, err := catalog.OpenInMemory()
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	if err := catalog.ApplySchema(ctx, db); err != nil {
		log.Fatal(err)
	}
	if err := catalog.Seed(ctx, db); err != nil {
		log.Fatal(err)
	}

	rows, err := catalog.ListInventory(ctx, db, "alice")
	if err != nil {
		log.Fatal(err)
```

왜 이 코드도 같이 봐야 하는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

CLI:

```bash
cd 01-backend-core/04-sql-and-data-modeling/go
go run ./cmd/schemawalk
go test ./...
```

검증 신호:

- 2026-03-07 기준 `go run ./cmd/schemawalk`가 정상 실행됐다.
- 2026-03-07 기준 `go test ./...`가 통과했다.

다음:

- 실제 migration binary와 외부 RDBMS 연결은 다음 과제에서 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/catalog/catalog_test.go` 같은 결정적인 코드와 `cd 01-backend-core/04-sql-and-data-modeling/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
