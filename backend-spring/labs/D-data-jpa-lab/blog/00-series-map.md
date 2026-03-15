# D-data-jpa-lab series map

이 시리즈는 `D-data-jpa-lab`을 "JPA CRUD 데모"가 아니라 "schema, entity, service guard가 어느 정도까지 persistence 의미를 만들고 있는가"라는 질문으로 다시 읽는다. 특히 `@Version`이 붙어 있어도 실제 API 계약이 곧바로 optimistic locking처럼 보이지는 않는다는 점까지 같이 확인한다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   migration, entity, page listing, version conflict, validation 공백이 어떤 순서로 드러났는지 따라간다.

## 이 시리즈가 답하는 질문

- `lab_products.version` 컬럼과 `@Version`은 실제 API에서 어떻게 보이는가
- 현재 충돌 감지는 JPA가 자동으로 처리하는가, 아니면 service가 수동으로 막는가
- Querydsl-ready라는 설명과 실제 구현 사이에는 어느 정도 거리가 있는가
