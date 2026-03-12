# D-data-jpa-lab 설계 메모

이 문서는 JPA 랩의 현재 구현 범위, 의도적 단순화, 다음 확장 지점을 요약한다.

## 현재 구현 범위

- Flyway-managed `lab_products` 테이블
- JPA entity, repository, service 경계
- page 기반 listing과 optimistic-lock-style version check

## 의도적 단순화

- Querydsl은 설치했지만 깊은 검색 조합은 아직 다루지 않는다
- soft delete는 확장 지점으로만 남겼다
- larger catalog graph 대신 핵심 aggregate 하나에 집중했다

## 다음 개선 후보

- Querydsl 조건 조합과 정렬 시나리오 추가
- category와 review aggregate 확장
- soft delete 및 N+1 regression 테스트 보강
