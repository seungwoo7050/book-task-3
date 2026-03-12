# 문제 정의

간단한 게임 상점 스키마를 설계하고, join과 transaction으로 재고 구매 흐름을 표현한다.

## 성공 기준

- `players`, `items`, `inventory` 테이블을 만든다.
- FK와 unique constraint를 사용한다.
- join query로 플레이어 인벤토리를 조회한다.
- transaction으로 구매 흐름을 묶는다.

## 제공 자료와 출처

- `study`에서 새로 설계한 브리지 과제다.
- 이 문서가 공개용 한국어 canonical 문제 정의다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `cd solution/go && go run ./cmd/schemawalk`
- `cd solution/go && go test ./...`

## 제외 범위

- 전용 migration tool
- 외부 운영 DB 최적화
