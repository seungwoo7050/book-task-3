# 04-sql-and-data-modeling-go 문제지

## 왜 중요한가

간단한 게임 상점 스키마를 설계하고, join과 transaction으로 재고 구매 흐름을 표현한다.

## 목표

시작 위치의 구현을 완성해 players, items, inventory 테이블을 만든다, FK와 unique constraint를 사용한다, join query로 플레이어 인벤토리를 조회한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/01-backend-core/04-sql-and-data-modeling/solution/go/cmd/schemawalk/main.go`
- `../study/01-backend-core/04-sql-and-data-modeling/solution/go/catalog/catalog.go`
- `../study/01-backend-core/04-sql-and-data-modeling/solution/go/catalog/catalog_test.go`
- `../study/01-backend-core/04-sql-and-data-modeling/solution/go/go.mod`
- `../study/01-backend-core/04-sql-and-data-modeling/solution/go/go.sum`

## starter code / 입력 계약

- `../study/01-backend-core/04-sql-and-data-modeling/solution/go/cmd/schemawalk/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- players, items, inventory 테이블을 만든다.
- FK와 unique constraint를 사용한다.
- join query로 플레이어 인벤토리를 조회한다.
- transaction으로 구매 흐름을 묶는다.

## 제외 범위

- 전용 migration tool
- 외부 운영 DB 최적화
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `OpenInMemory`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `newTestDB`와 `TestListInventory`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/04-sql-and-data-modeling/solution/go && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/04-sql-and-data-modeling/solution/go && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`04-sql-and-data-modeling-go_answer.md`](04-sql-and-data-modeling-go_answer.md)에서 확인한다.
