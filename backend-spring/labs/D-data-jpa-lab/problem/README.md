# D-data-jpa-lab 문제 정의

JPA를 "그냥 돌아가는 CRUD"가 아니라, 데이터 경계와 persistence 선택을 설명하는 도구로 다루는 Spring 랩을 만든다.

## 성공 기준

- Flyway와 JPA entity/repository/service 경계가 같이 보인다.
- pagination과 optimistic locking 같은 persistence 고민이 코드에 드러난다.
- Querydsl을 왜 지금은 얕게 두는지 설명할 수 있다.

## 이번 단계에서 다루지 않는 것

- 복잡한 Querydsl 검색 조합
- 대규모 catalog graph
- soft delete와 N+1 회피 심화

이 디렉터리는 문제 정의와 성공 기준을 고정하는 곳이며, 구현 세부는 다른 문서로 분리한다.
