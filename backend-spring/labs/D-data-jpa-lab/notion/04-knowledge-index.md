# Knowledge Index — JPA 설계 패턴과 개념 사전

## 재사용 가능한 개념들

### Entity와 Service의 경계 분리

JPA entity에 모든 비즈니스 규칙을 밀어 넣으면 편리하지만, entity가 JPA 매핑 관심사와 도메인 규칙을 동시에 가지게 된다. 이 랩에서 택한 방식은 entity에는 최소한의 도메인 행동(`changePrice()`)만 두고, 검증과 조회 로직은 service(`DataApiService`)에 위치시키는 것이다.

이 구분의 실질적인 기준은 "이 메서드가 영속성 컨텍스트 없이도 의미가 있는가"이다. `changePrice()`는 entity 내부 상태를 변경하는 것이므로 entity에 있어도 자연스럽다. 하지만 "이 제품의 version이 요청과 일치하는가"는 외부 입력과의 비교이므로 service가 담당한다.

이 패턴은 DDD의 aggregate root 개념과 연결된다. product가 단일 aggregate의 root이고, 모든 상태 변경은 이 root를 통해서만 일어난다. 현재는 aggregate 안에 entity가 하나뿐이지만, category나 review가 추가되면 aggregate boundary를 어디에 두느냐가 새로운 설계 결정이 된다.

### Flyway + JPA validate 조합

스키마 진화와 ORM 매핑을 함께 관리하는 방식이다. Flyway는 `V1__init.sql`, `V2__lab_products.sql` 같은 번호가 매겨진 마이그레이션 파일로 스키마를 변경하고, Hibernate는 `ddl-auto: validate`로 entity 클래스와 실제 테이블 구조가 일치하는지만 확인한다.

이 조합의 장점은 세 가지다:
1. 스키마 변경 이력이 SQL 파일로 남아서 추적이 가능하다
2. Hibernate가 자동으로 테이블을 만들거나 변경하는 것(create, update)을 방지하므로 프로덕션에서 안전하다
3. 로컬(H2)과 Docker(PostgreSQL) 환경에서 동일한 마이그레이션이 실행되므로 환경 차이로 인한 문제가 줄어든다

### 낙관적 락(Optimistic Locking)

version 기반 충돌 감지로 stale update를 막는 패턴이다. 이 랩에서는 두 가지 메커니즘이 함께 동작한다:

1. **JPA `@Version` 자동 동작**: Hibernate가 UPDATE 쿼리를 실행할 때 `WHERE version = ?`를 자동으로 추가한다. version이 일치하지 않으면 `OptimisticLockException`을 던진다.
2. **애플리케이션 레벨 수동 확인**: `DataApiService.updatePrice()`에서 `product.getVersion() != version`으로 먼저 확인하고, 불일치하면 `IllegalArgumentException("Version conflict")`를 던진다.

두 가지가 겹치는 것은 의도적이다. 수동 확인이 먼저 실행되어 ProblemDetail 형식의 에러 응답을 만들어내고, `@Version`은 추가적인 안전장치로 작동한다. 면접에서 "낙관적 락을 어떻게 구현했나"라는 질문에 답할 때, JPA 자동 동작과 애플리케이션 레벨 검증의 차이를 설명할 수 있어야 한다.

### PageEnvelope 패턴

Spring Data의 `Page` 객체를 그대로 API 응답으로 반환하면 `Pageable`, `Sort` 같은 Spring 내부 구조가 외부에 노출된다. `PageEnvelope<T>`라는 generic record를 만들어서 `content`, `page`, `size`, `totalElements`, `totalPages`, `hasNext`만 노출하면 API 계약이 프레임워크에 종속되지 않는다.

```java
public record PageEnvelope<T>(
    java.util.List<T> content,
    int page, int size,
    long totalElements, int totalPages,
    boolean hasNext) {}
```

### Open Session In View 비활성화

`spring.jpa.open-in-view: false`는 controller 레이어에서 lazy loading이 동작하지 않게 만든다. 이렇게 하면 "service 레이어에서 필요한 데이터를 모두 로딩해야 한다"는 제약이 생기고, 트랜잭션 경계가 명확해진다. OSIV를 켜놓으면 편리하지만, 어디서 DB 쿼리가 실행되는지 예측하기 어려워진다.

## 용어 사전

- **N+1 문제**: 목록 조회(1번의 쿼리) 후 각 항목의 연관 데이터를 개별 쿼리(N번)로 반복 로드하는 비효율. 해결 방법은 fetch join, `@EntityGraph`, batch size 설정 등이 있다. 이 랩에서는 아직 연관 관계가 없으므로 발생하지 않지만, entity가 추가되면 반드시 마주치게 된다.

- **Querydsl**: type-safe한 쿼리 빌드 도구. 컴파일 타임에 쿼리 오류를 잡을 수 있다. `querydsl-apt`가 annotation processing으로 `QProductEntity` 같은 메타모델 클래스를 생성하고, 이를 통해 `BooleanExpression`, `OrderSpecifier` 같은 타입 안전한 쿼리 조각을 조합한다.

- **IDENTITY 전략**: `@GeneratedValue(strategy = GenerationType.IDENTITY)`는 DB의 auto-increment를 사용한다. 이 전략의 특징은 `persist()` 시점에 INSERT가 즉시 실행되어야 ID를 알 수 있다는 것이다. SEQUENCE 전략과 달리 batch insert가 불가능하다는 tradeoff가 있다.

- **ProblemDetail**: Spring 6(Spring Boot 3)에서 도입된 RFC 7807 Problem Details 응답 형식. `GlobalExceptionHandler`에서 `ProblemDetail.forStatusAndDetail()`로 생성하고, `code`, `traceId`, `errors` 같은 커스텀 속성을 추가한다.

## 참고 자료

- **D-data-jpa-lab docs/README.md** — 현재 구현 범위, 단순화된 부분, 다음 개선 방향이 정리되어 있다. 코드를 읽다가 "이게 의도적으로 빠진 건지, 빼먹은 건지" 궁금할 때 이 문서를 확인하면 된다.
- **problem/README.md** — 이 랩의 한 줄 문제 정의: "Build a persistence-heavy lab that makes JPA tradeoffs explicit instead of hiding them behind framework magic."
- **Spring Data JPA Reference**: `Page`, `Pageable`, `JpaRepository`의 기본 동작과 커스텀 쿼리 메서드 작성법
- **Hibernate ORM `@Version` documentation**: `@Version` 필드가 있을 때 UPDATE 쿼리에 자동으로 version 조건이 추가되는 메커니즘
