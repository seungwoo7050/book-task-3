# Debug Log — Keyword Inflation이라는 함정

## 이 랩에서 만난 진짜 위험

D-data-jpa-lab에서 가장 위험한 것은 런타임 크래시가 아니었다. 진짜 위험은 "keyword inflation" — 기술 키워드가 실제 구현 깊이보다 더 많은 것을 약속하는 것처럼 보이는 현상이었다.

build.gradle.kts에는 Querydsl, Flyway, Spring Data JPA, Testcontainers 같은 기술 이름들이 빼곡하다. 이 의존성 목록만 보면 마치 복잡한 동적 검색과 다중 엔티티 관계, 통합 테스트까지 모두 구현한 것 같지만, 실제 코드의 깊이는 그보다 얕다. `ProductRepository`는 `JpaRepository`를 상속할 뿐 커스텀 쿼리 메서드가 없고, Querydsl의 `Q` 클래스를 사용하는 코드도 아직 없다.

## 어떻게 이 문제를 자각했는가

이 불일치를 자각하게 된 계기는 docs/README.md를 작성하면서였다. "Implemented now" 섹션에 무엇을 적을 수 있는지 나열할 때, build.gradle.kts의 dependency 목록을 기준으로 적다가 멈췄다. 의존성이 설치되어 있다는 것과 그 기술을 실제로 사용했다는 것은 다른 이야기다.

dependency를 추가한 것만으로 학습 목표를 달성했다고 착각하기 쉽다. 특히 JPA 영역에서는 이 함정이 더 위험하다. `@Entity`를 붙이고 `JpaRepository`를 상속하면 CRUD는 자동으로 동작하기 때문에, "구현했다"는 느낌이 실제 이해보다 앞서갈 수 있다.

## 대응 방법: 현재와 다음을 분리한다

코드를 수정한 것이 아니라, 문서에서 "현재 증명된 범위"와 "다음에 다룰 범위"를 명확하게 분리했다.

docs/README.md의 구조를 세 단계로 나누었다:
- **Implemented now**: Flyway-managed `lab_products` 테이블, JPA entity/repository/service boundary, page-based listing, optimistic-lock-style version check
- **Important simplifications**: Querydsl은 설치되었지만 deep하게 사용되지 않음, soft delete는 extension point, 단일 aggregate만 다룸
- **Next improvements**: Querydsl 검색 조건, category/review 테이블 도입, soft delete, N+1 regression test

이 분리가 중요한 이유는 독자가 코드를 읽을 때 "이 프로젝트가 증명하는 것"과 "앞으로 증명해야 하는 것"을 혼동하지 않기 때문이다.

## 검증 방법

이 랩에 런타임 버그는 없었다. 대신 학습 정합성을 확인하기 위해 두 가지를 실행했다:

```bash
make test    # DataApiTest: create → list → update → version conflict 전체 흐름 통과
make smoke   # LabInfoApiSmokeTest: 애플리케이션 기동 확인
```

`DataApiTest`의 `productCrudAndConflictCheckWork()` 테스트가 통과한다는 것은, 최소한 다음 네 가지가 동작한다는 증거다:
1. `POST /api/v1/products`로 제품 생성 — entity 영속화와 ID 자동생성이 동작
2. `GET /api/v1/products`로 페이지 조회 — PageRequest와 PageEnvelope 변환이 동작
3. `PATCH /api/v1/products/{id}`로 가격 변경 — version 0으로 업데이트 성공
4. 같은 version 0으로 재요청 — 400 Bad Request와 `bad_request` 코드 반환

## 후속으로 남은 부채

- Querydsl을 실제로 사용하는 검색 조건 예시를 추가해야 한다. `BooleanBuilder`나 `Predicate` 기반 동적 검색이 없으면 Querydsl 의존성의 존재 의미가 약하다.
- category, review 같은 연관 엔티티를 도입하고 N+1 regression test를 작성해야 한다. `@ManyToOne`이나 `@OneToMany`가 등장하면 fetch join과 pagination의 충돌 문제가 자연스럽게 따라온다.
- soft delete 전략 — `deleted` 플래그와 `@Where` 어노테이션 또는 Hibernate 6의 `@SoftDelete` 를 검토해야 한다.

