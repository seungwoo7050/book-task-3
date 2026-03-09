# Approach Log

## Options considered

- Querydsl을 초반부터 heavily 쓰는 방식은 배울 것이 많지만 scaffold를 과하게 복잡하게 만든다.
- 순수 CRUD만 두는 방식은 JPA의 진짜 tradeoff를 보여주기 어렵다.
- one aggregate 중심 접근은 범위는 작지만, entity/repository/service 구조를 설명하기 쉽다.

## Chosen direction

- package structure:
  - entity, repository, service, API boundary를 먼저 분명히 둔다
- persistence choice:
  - Flyway와 JPA를 함께 둔다
- security boundary:
  - auth 없이 data persistence 자체에 집중한다
- integration style:
  - optimistic locking과 page listing을 먼저 보여 준다
- why this is the right choice:
  - JPA-first 사고를 과도한 기능 수보다 설계 경계 중심으로 배울 수 있다

## Rejected ideas

- full catalog graph를 첫 scaffold에 넣는 방식은 폐기했다
- pure Querydsl showcase로 가는 방식은 폐기했다

## Evidence

- `/Users/woopinbell/work/web-pong/study2/labs/D-data-jpa-lab/spring/README.md`
- `/Users/woopinbell/work/web-pong/study2/labs/D-data-jpa-lab/docs/README.md`

