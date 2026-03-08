# Problem

상품 조회 API에 cache-aside 패턴을 적용하고, cache invalidation과 기본 관측 지표를 함께 노출한다.

## Requirements

- migration up/down
- `GET /v1/items/{id}`
- `PUT /v1/items/{id}`
- `/metrics`
- `X-Trace-ID` 응답 헤더

