# Problem Framing — JPA를 "설계 도구"로 바라보기

## 이 랩이 존재하는 이유

Spring Data JPA를 쓸 줄 안다는 말은 구체적으로 무엇을 의미하는가. `JpaRepository`를 상속하고 `save()`를 호출하면 끝인가. 이 랩은 그 질문에서 출발한다.

현실의 백엔드 프로젝트에서 JPA는 단순한 CRUD 헬퍼가 아니다. entity 경계를 어디에 두느냐, 트랜잭션 범위를 어떻게 잡느냐, 동시 수정이 들어왔을 때 어떤 전략을 택하느냐 — 이런 것들이 모여서 "JPA를 알고 쓴다"는 말이 된다. D-data-jpa-lab의 목표는 product라는 단일 aggregate를 중심으로 이 설계 선택들이 코드에서 어떻게 드러나는지 직접 구현하고 검증하는 것이다.

## 구체적으로 무엇을 다루는가

이 랩에서 직접 구현하는 범위는 다음과 같다.

**제품(Product) CRUD**. 이름과 가격을 가진 제품을 생성하고 조회한다. 단순한 것 같지만, entity와 service 사이의 책임 분리를 연습하는 첫 번째 장이다. `ProductEntity`는 JPA 매핑에 집중하고, 비즈니스 로직은 `DataApiService`가 맡는다.

**페이지네이션**. 전체 목록을 한 번에 반환하는 대신 `PageRequest`를 사용해서 page와 size 단위로 분할한다. Spring의 `Page` 객체를 그대로 API 응답으로 내보내지 않고, `PageEnvelope`이라는 커스텀 record로 감싸서 API 계약을 명확하게 유지한다.

**낙관적 락(Optimistic Locking)**. `@Version` 어노테이션이 붙은 `version` 필드를 통해 동시 수정을 감지한다. 클라이언트가 가격 변경을 요청할 때 자신이 마지막으로 읽은 version을 함께 보내야 하고, 서버는 그 version이 현재와 일치하는지 애플리케이션 레벨에서 확인한다.

## 의도적으로 다루지 않는 것들

이 랩은 의도적으로 범위를 제한한다. 여기서 다루지 않는 것들은 "몰라서"가 아니라 "지금은 아니라서"이다.

- **Querydsl 심화 검색**: `querydsl-jpa`와 `querydsl-apt`가 build.gradle.kts에 설치되어 있지만, 실제로 복잡한 동적 쿼리를 작성하지는 않는다. 설치만 해두고 "이것을 언제 꺼내 쓸 것인가"를 생각하게 하는 것이 현재 단계의 목적이다.
- **N+1 문제 재현과 해결**: 연관 엔티티(category, review)를 아직 도입하지 않았으므로, N+1은 자연스럽게 후속 과제가 된다.
- **Soft delete**: 삭제 플래그를 두는 전략도 다음 단계로 남긴다.
- **인증/인가**: SecurityConfig는 모든 요청을 permitAll로 열어 둔다. 이 랩의 초점은 데이터 영속성 설계이지 보안이 아니다.

## 기술 스택과 제약 조건

| 항목 | 선택 |
|------|------|
| 언어 | Java 21 |
| 프레임워크 | Spring Boot 3.4.x |
| ORM | Spring Data JPA + Querydsl 5.1.0 |
| 스키마 관리 | Flyway |
| 로컬 DB | H2 in-memory (PostgreSQL 호환 모드) |
| 프로덕션 DB | PostgreSQL 16 |
| DDL 전략 | `hibernate.ddl-auto: validate` — 스키마는 Flyway가 관리하고 Hibernate는 검증만 |
| OSIV | `spring.jpa.open-in-view: false` — 명시적으로 비활성화 |

## 성공 기준

1. JPA entity와 service boundary가 명확히 분리되어 있어야 한다
2. 페이지네이션이 page/size 파라미터로 동작해야 한다
3. 낙관적 락이 stale version 요청을 거부해야 한다
4. `make test`와 `make smoke`가 통과해야 한다
5. 현재 구현된 범위와 다음 단계가 문서에 명시되어 있어야 한다

## 남아 있는 불확실성

Querydsl을 설치해 놓고 실제로는 쓰지 않는 상태가 학습에 도움이 되는지 확신이 없었다. 그래도 "의존성은 있지만 꺼내 쓸 시점을 판단하는 것"도 설계 결정이라고 보고 현재 상태를 유지했다. entity 구조와 낙관적 락을 먼저 굳히는 것이 순서상 맞다고 판단했고, 더 깊은 쿼리 작업은 aggregate가 복잡해지는 시점에 자연스럽게 필요해질 것이다.

