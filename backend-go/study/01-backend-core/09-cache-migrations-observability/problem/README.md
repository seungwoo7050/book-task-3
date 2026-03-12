# 문제 정의

상품 조회 API에 cache-aside 패턴을 적용하고, cache invalidation과 기본 관측 지표를 함께 노출한다.

## 성공 기준

- migration up/down이 가능해야 한다.
- `GET /v1/items/{id}`와 `PUT /v1/items/{id}`를 제공한다.
- `/metrics`를 노출한다.
- `X-Trace-ID` 응답 헤더를 전달한다.

## 제공 자료와 출처

- `study`에서 새로 설계한 브리지 과제다.
- 이 문서가 공개용 canonical 문제 정의다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `cd solution/go && go run ./cmd/server`
- `cd solution/go && go test ./...`

## 제외 범위

- 실제 Redis adapter
- full tracing stack
