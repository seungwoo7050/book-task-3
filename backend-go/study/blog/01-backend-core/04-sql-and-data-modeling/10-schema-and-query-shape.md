# 04 SQL And Data Modeling — Schema And Query Shape

`01-backend-core/04-sql-and-data-modeling`는 스키마 설계, join, transaction을 게임 상점 예제로 묶어 SQL 기초를 백엔드 문맥에서 익히는 브리지 과제다. 이 글에서는 Phase 1: 프로젝트 뼈대와 의존성 -> Phase 2: 스키마 설계 -> Phase 3: 쿼리 구현 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 1: 프로젝트 뼈대와 의존성
- Phase 2: 스키마 설계
- Phase 3: 쿼리 구현

## Day 1
### Session 1

- 당시 목표: 스키마 설계와 관계 모델링을 실제 도메인 예제로 익혀야 한다.
- 변경 단위: `modernc.org/sqlite`, `solution/go/catalog/catalog.go`
- 처음 가설: ORM 없이 SQL 구조를 먼저 보여 주기 위해 스키마와 쿼리 자체를 학습 표면에 올렸다.
- 실제 진행: 디렉터리 구조 생성 Go 모듈 초기화 및 의존성 설치 SQL 스키마 작성 (`solution/go/catalog/catalog.go`) 세 테이블의 DDL을 Go 상수로 작성했다: `players`: 플레이어 (id, name) `items`: 아이템 (id, name, price_cents) `inventory`: 인벤토리 (player_id, item_id, quantity) — composite PK

CLI:

```bash
mkdir -p 01-backend-core/04-sql-and-data-modeling/{solution/go/cmd/schemawalk,solution/go/catalog,docs/concepts,docs/references,problem}

cd 01-backend-core/04-sql-and-data-modeling/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling
go get modernc.org/sqlite
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/catalog/catalog.go`

```go
var ErrUnknownItem = errors.New("unknown item")

const schema = `
CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price_cents INTEGER NOT NULL CHECK (price_cents > 0)
);

CREATE TABLE inventory (
    player_id INTEGER NOT NULL REFERENCES players(id),
    item_id INTEGER NOT NULL REFERENCES items(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
```

왜 이 코드가 중요했는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

새로 배운 것:

- `players`, `items`, `inventory` 분리는 다대다 관계를 명시적으로 드러낸다.

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

- 다음 글에서는 `20-transaction-and-verification-loop.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/catalog/catalog.go` 같은 결정적인 코드와 `cd 01-backend-core/04-sql-and-data-modeling/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
