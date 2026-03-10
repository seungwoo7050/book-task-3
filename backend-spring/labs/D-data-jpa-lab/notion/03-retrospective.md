# Retrospective — entity 경계가 보이기 시작했다

## 나아진 점

### JPA를 "구조 문제"로 바라보게 되었다

이 랩을 진행하기 전에는 JPA를 "repository에 메서드 시그니처를 한 줄 적으면 쿼리가 만들어지는 도구" 정도로 인식하고 있었다. 물론 그것도 맞는 말이다. 하지만 D-data-jpa-lab을 거치면서 JPA의 더 중요한 측면을 인식하게 되었다. entity가 어디까지 알아야 하는가, service는 entity에 어떤 것을 위임하고 어떤 것을 직접 해야 하는가 — 이것은 코드 구조의 문제이지 프레임워크 API의 문제가 아니다.

`ProductEntity`에 `changePrice(BigDecimal price)` 메서드를 두었을 때, 이 entity가 가질 수 있는 행동의 최소 단위가 무엇인지 생각하게 되었다. 가격을 바꾸는 것은 entity의 책임이다. 하지만 "이 가격 변경이 허용되는가"를 판단하는 것(version 확인)은 service의 책임이다. 이 구분이 코드에 드러나는 것이 entity/service boundary 분리의 핵심이다.

### 낙관적 락을 초기 개념으로 도입한 것이 좋았다

동시성 제어를 나중에 추가하려고 하면 기존 API 계약을 바꿔야 할 수 있다. 처음부터 `version` 필드를 entity에 두고, 클라이언트가 업데이트할 때 version을 함께 보내는 구조를 잡아 놓으면, 나중에 동시 사용자가 늘어나도 API 인터페이스를 변경하지 않아도 된다.

현재 구현은 JPA의 `@Version`이 자동으로 던지는 `OptimisticLockException`에 기대지 않고, 애플리케이션 레벨에서 수동 비교(`product.getVersion() != version`)를 한다. 이 선택은 의도적이다. `@Version`의 자동 동작을 이해하기 전에, 먼저 "version이 왜 필요하고 어떤 시점에 비교해야 하는지"를 코드로 보이고 싶었다.

### Flyway + JPA validate 조합의 의미가 명확해졌다

`hibernate.ddl-auto`를 `update`나 `create-drop`으로 두면 편리하지만, 스키마 변경 이력이 남지 않는다. Flyway가 마이그레이션 SQL을 관리하고 Hibernate가 매핑 정합성만 검증하는 구조는, 프로덕션 환경에서의 스키마 관리 방식을 그대로 학습할 수 있게 해준다. 로컬에서는 H2 in-memory에 PostgreSQL 호환 모드를 사용하므로, Flyway 마이그레이션이 로컬과 Docker 환경 모두에서 동일하게 동작한다.

## 아직 약한 점

### Querydsl의 깊이가 부족하다

`querydsl-jpa`와 `querydsl-apt`가 build.gradle.kts에 있지만, `JPAQueryFactory`나 `BooleanExpression`을 사용하는 코드가 없다. 현재 `ProductRepository`는 `JpaRepository`의 기본 메서드만 사용한다. 이것은 Querydsl을 "써봤다"고 말할 수 없는 상태이고, 02-debug-log에서 분석한 keyword inflation의 가장 명확한 사례이기도 하다.

### 연관 관계가 없다

product만 존재하는 현재 구조에서는 `@ManyToOne`, `@OneToMany` 같은 연관 매핑이 등장하지 않는다. JPA를 쓰면서 연관 관계를 다루지 않는다는 것은, 가장 흥미롭고 위험한 부분을 아직 건드리지 않았다는 의미다.

### N+1 문제를 직접 재현하지 못했다

연관 엔티티가 없으니 N+1이 발생할 조건 자체가 없다. "N+1이 뭔지 안다"와 "N+1을 직접 발생시키고 해결해 봤다"는 전혀 다른 수준의 이해이다.

## 다음에 다시 볼 것들

- **검색 조건 추가**: 이름으로 검색, 가격 범위로 필터링 같은 동적 조건을 Querydsl로 구현하면 실질적인 쿼리 빌드 경험이 생긴다.
- **fetch join + pagination 충돌**: `@OneToMany` 관계에서 fetch join을 쓰면 Hibernate가 메모리에서 페이징을 수행하는 문제가 있다. 이 충돌을 직접 겪어보는 것이 중요하다.
- **다른 기술 스택과의 비교**: Python의 SQLAlchemy나 Django ORM과 "entity boundary"를 비교하는 메모를 만들면, JPA에 특유한 것과 ORM 일반에 해당하는 것을 구분할 수 있다.

