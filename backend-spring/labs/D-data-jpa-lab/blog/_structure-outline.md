# D-data-jpa-lab structure outline

## 글 목표

- JPA를 CRUD 성공담이 아니라 schema와 충돌 제어의 연결로 설명한다.
- macOS + VSCode 통합 터미널 기준의 검증 흐름을 유지한다.

## 글 순서

1. CRUD와 version conflict를 함께 고정한 단계
2. Flyway, entity, service guard를 묶은 단계
3. Querydsl과 확장 범위를 뒤로 미룬 이유를 닫는 단계

## 반드시 넣을 코드 앵커

- `DataApiTest.productCrudAndConflictCheckWork()`
- `V2__lab_products.sql`
- `DataApiService.updatePrice()`

## 반드시 넣을 CLI

```bash
cd spring
make test
make smoke
docker compose up --build
```

## 핵심 개념

- JPA에서는 migration과 entity를 같이 봐야 의미가 생긴다.
- optimistic locking은 쓰기 충돌을 어디서 감지할지 정하는 규칙이다.
