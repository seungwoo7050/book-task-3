# Problem

상품 정보를 SQLite에 저장하는 작은 CRUD API를 만들고 optimistic update와 transaction rollback을 구현한다.

## Requirements

- migration up/down 파일을 둔다.
- `POST /v1/products`
- `GET /v1/products`
- `GET /v1/products/{id}`
- `PATCH /v1/products/{id}`
- 재고 부족 시 transaction rollback

