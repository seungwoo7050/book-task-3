# Retrospective

## What improved

- JPA를 “repository 한 줄”이 아니라 entity/service boundary 문제로 보기 시작했다.
- optimistic locking을 early concept로 둔 것이 좋았다.
- Flyway와 JPA를 같이 두는 이유가 더 분명해졌다.

## What is still weak

- Querydsl depth가 얕다.
- category/review graph가 아직 약하다.
- N+1 문제를 실제로 재현하는 테스트는 부족하다.

## What to revisit

- search 조건을 richer하게 추가할 수 있다.
- fetch join과 pagination 충돌 주제를 더 볼 수 있다.
- FastAPI data lab과 ORM boundary 비교 메모를 만들 수 있다.

