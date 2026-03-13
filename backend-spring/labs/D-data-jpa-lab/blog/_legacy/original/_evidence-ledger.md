# D-data-jpa-lab Evidence Ledger

- 복원 기준:
  - commit granularity가 세밀하지 않아 `problem/README.md`, `docs/README.md`, JPA entity/repository/service, MockMvc 테스트, `2026-03-13` 재실행 CLI를 합쳐 chronology를 세웠다.
- 기존 blog 처리:
  - 기존 `blog/` 디렉터리가 없어서 격리 대상은 없었다.

## Phase 1

- 시간 표지: Phase 1
- 당시 목표:
  - JPA 랩이 단순 CRUD가 아니라 persistence 경계를 설명하는 랩이라는 점을 먼저 고정한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - Flyway, entity, repository, service 경계를 같이 보이게 하지 않으면 JPA가 그냥 "저장된다" 수준으로만 읽힌다.
- 실제 조치:
  - Flyway-managed `lab_products`, page listing, optimistic locking, search-ready structure를 canonical scope로 정했다.
  - Querydsl 심화와 larger catalog graph는 다음 단계로 남겼다.
- CLI:

```bash
cp .env.example .env
make run
```

- 검증 신호:
  - `spring/README.md`가 VSCode 터미널 진입점을 고정하고, docs는 JPA 경계와 트레이드오프를 현재 랩의 중심으로 명시한다.
- 핵심 코드 앵커:
  - 이후 읽기는 `ProductEntity`, `ProductRepository`, `DataApiService`, `DataApiTest`로 닫힌다.
- 새로 배운 것:
  - JPA를 설명하려면 컨트롤러보다 먼저 데이터 경계와 version 관리가 왜 필요한지부터 보여 줘야 한다.
- 다음:
  - entity와 service에 version check를 실제 규칙으로 넣는다.

## Phase 2

- 시간 표지: Phase 2
- 당시 목표:
  - 낙관적 락과 pagination을 API 계약 안으로 끌고 온다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/data/domain/ProductEntity.java`
  - `spring/src/main/java/com/webpong/study2/app/data/domain/ProductRepository.java`
  - `spring/src/main/java/com/webpong/study2/app/data/application/DataApiService.java`
  - `spring/src/main/resources/db/migration/V2__lab_products.sql`
- 처음 가설:
  - version 충돌을 DB 내부 구현에 숨기지 말고, API 입력값으로 드러내야 JPA의 동시성 의미를 설명할 수 있다.
- 실제 조치:
  - `ProductEntity`에 `@Version` 필드를 뒀다.
  - `list()`는 `PageRequest`로 page/size envelope를 만든다.
  - `updatePrice()`는 현재 version이 맞을 때만 가격을 바꾸고, 틀리면 `Version conflict`를 던진다.
- CLI:

```bash
make test
```

- 검증 신호:
  - `2026-03-13` 재실행에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.
- 핵심 코드 앵커:

```java
@Version private long version;
```

- 새로 배운 것:
  - optimistic locking은 "나중에 DB가 막아 준다"가 아니라, 현재 읽은 버전으로 업데이트를 시도한다는 애플리케이션 계약이다.
- 다음:
  - version conflict가 실제 API 응답에서 어떻게 보이는지 고정한다.

## Phase 3

- 시간 표지: Phase 3
- 당시 목표:
  - 생성, 조회, 가격 변경, version conflict를 하나의 API 흐름으로 검증한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/DataApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - 같은 product에 `version=0`으로 두 번 patch를 보내면 충돌을 가장 직관적으로 보여 줄 수 있다.
- 실제 조치:
  - product 생성 -> 목록 조회 -> 정상 가격 변경 -> 오래된 version으로 재변경 시도 순서를 MockMvc 테스트에 묶었다.
- CLI:

```bash
make test
make smoke
docker compose up --build
```

- 검증 신호:
  - `2026-03-13` 재실행 뒤 XML 리포트 4개, `failures=0`이 확인됐다.
  - `2026-03-09` 검증 기록에는 lint/test/smoke/Compose health 확인 통과가 있다.
- 핵심 코드 앵커:

```java
if (product.getVersion() != version) {
  throw new IllegalArgumentException("Version conflict");
}
```

- 새로 배운 것:
  - JPA의 동시성 제어는 엔티티 annotation 하나보다, 그 version을 언제 비교하고 어떤 에러로 번역하는지가 더 중요하다.
- 다음:
  - Querydsl 조건 조합, soft delete, larger graph는 다음 단계로 남긴다.
