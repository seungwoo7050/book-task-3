# 문제 정의

상품 정보를 SQLite에 저장하는 작은 CRUD API를 만들고 optimistic update와 transaction rollback을 구현한다.

## 성공 기준

- migration up/down 파일을 둔다.
- `POST /v1/products`
- `GET /v1/products`
- `GET /v1/products/{id}`
- `PATCH /v1/products/{id}`
- 재고 부족 시 transaction rollback을 수행한다.

## 제공 자료와 출처

- `study`에서 새로 설계한 브리지 과제다.
- 이 문서가 공개용 canonical 문제 정의다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `cd solution/go && go run ./cmd/server`
- `cd solution/go && go test ./...`

## 제외 범위

- 외부 DB 엔진
- prepared statement tuning
