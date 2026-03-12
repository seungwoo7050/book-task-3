# D-data-jpa-lab

JPA를 단순 CRUD 도구가 아니라 설계 선택과 트레이드오프가 드러나는 도구로 다루는 랩입니다.

- 상태: `verified scaffold`
- 실행 진입점: [spring/README.md](spring/README.md)

## 문제 요약

- JPA는 "돌아간다"만으로는 학습이 끝나지 않고, 엔티티 경계와 persistence 전략을 설명할 수 있어야 합니다.
- pagination, optimistic locking, Flyway, Querydsl-ready structure를 함께 읽히게 해야 합니다.
- 상세 성공 기준과 제약은 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- Flyway가 관리하는 테이블과 JPA entity/repository/service 경계를 갖춘 랩을 만들었습니다.
- page 기반 listing과 optimistic locking 스타일의 버전 검증을 넣었습니다.
- Querydsl을 바로 과시하기보다, 나중에 검색 조건을 확장할 수 있는 구조를 먼저 만들었습니다.

## 핵심 설계 선택

- CRUD 완성도보다 JPA 경계와 persistence choice를 설명하는 데 집중했습니다.
- 한 핵심 aggregate에 집중해 데이터 설계 논점을 흐리지 않게 했습니다.
- Querydsl은 설치만 하고, 현재 단계에서는 keyword inflation을 피했습니다.

## 검증

```bash
cd spring
make lint
make test
make smoke
docker compose up --build
```

마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 이번 단계에서 일부러 남긴 것

- 복잡한 Querydsl search 조합
- larger catalog graph 전체 모델링
- soft delete와 N+1 regression coverage의 심화

## 다음에 읽을 문서

- canonical problem statement: [problem/README.md](problem/README.md)
- 실행과 검증: [spring/README.md](spring/README.md)
- 현재 구현 범위와 단순화: [docs/README.md](docs/README.md)
- 학습 로그와 재현 기록: [notion/README.md](notion/README.md)
