# D-data-jpa-lab evidence ledger

- 작성 기준일: 2026-03-14
- 복원 원칙: 기존 blog 본문은 입력 근거에서 제외하고, source, tests, build config, 재실행 결과만 사용했다.
- 핵심 근거: `problem/README.md`, `docs/README.md`, `spring/build.gradle.kts`, `spring/Makefile`, `DataApiController.java`, `DataApiService.java`, `ProductEntity.java`, `ProductRepository.java`, `V2__lab_products.sql`, `DataApiTest.java`, `HealthApiTest.java`, `LabInfoApiSmokeTest.java`

## Phase 1. API surface와 test contract 확인

- 목표: 이 lab이 단순 CRUD인지, 아니면 conflict branch까지 포함한 persistence lab인지 먼저 확인한다.
- 확인 파일:
  - `spring/src/main/java/com/webpong/study2/app/data/api/DataApiController.java`
  - `spring/src/test/java/com/webpong/study2/app/DataApiTest.java`
- 확인 결과:
  - API는 create/list/update 세 개만 둔다.
  - 테스트는 create -> list -> update -> stale version conflict까지 한 흐름으로 고정한다.
- 핵심 앵커:

```java
mockMvc
    .perform(
        patch("/api/v1/products/{productId}", product.get("id").asLong())
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"price\":159.99,\"version\":0}"))
    .andExpect(status().isBadRequest());
```

- 메모:
  - conflict는 lab의 부가 기능이 아니라, controller/test contract 중심에 있다.
  - request DTO에 validation annotation은 있지만 `@Valid`는 없다.

## Phase 2. schema/entity/service에서 version이 어떻게 연결되는지 확인

- 목표: version conflict가 실제로 어떤 층에서 구현되는지 확인한다.
- 확인 파일:
  - `spring/src/main/resources/db/migration/V2__lab_products.sql`
  - `spring/src/main/java/com/webpong/study2/app/data/domain/ProductEntity.java`
  - `spring/src/main/java/com/webpong/study2/app/data/application/DataApiService.java`
- 확인 결과:
  - DB schema에 `version bigint not null default 0`
  - entity에 `@Version`
  - service는 `if (product.getVersion() != version)`으로 수동 conflict check
- 핵심 앵커:

```java
if (product.getVersion() != version) {
  throw new IllegalArgumentException("Version conflict");
}
product.changePrice(price);
return ProductResponse.from(product);
```

- 메모:
  - update response는 flush 이전 entity snapshot을 반환할 수 있다.
  - 실제로 2026-03-14 수동 호출에서 update response는 `version: 0`, 직후 list 결과는 `version: 1`이었다.

## Phase 3. Querydsl-ready 주장과 실제 구현 거리 확인

- 목표: docs가 말하는 search-ready structure가 실제 코드에 얼마나 구현되어 있는지 확인한다.
- 확인 파일:
  - `spring/build.gradle.kts`
  - `docs/README.md`
- 확인 결과:
  - build에는 `querydsl-jpa`, `querydsl-apt` dependency가 있다.
  - source tree에는 `JPAQueryFactory`, generated Q type, custom search repository가 없다.
- 메모:
  - 현재 "Querydsl-ready"는 code path라기보다 extension slot에 가깝다.

## Phase 4. 2026-03-14 재실행 검증

- lint:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
```

- 결과: `BUILD SUCCESSFUL in 1m 33s`

- test:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'
```

- 결과: `BUILD SUCCESSFUL in 1m 52s`

- smoke:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

- 결과: `BUILD SUCCESSFUL in 1m 40s`

- manual boot run:

```bash
docker run --rm -u $(id -u):$(id -g) -p 18083:8080 \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew bootRun'
```

- manual HTTP checks:
  - valid create -> `{"id":1,"name":"Keyboard","price":129.99,"version":0}`
  - first list -> `version: 0`
  - first patch with `version: 0` -> `200`, response still `version: 0`
  - second patch with stale `version: 0` -> `400`, `detail="Version conflict"`
  - next list -> same row now `version: 1`
  - invalid create `{"name":"","price":-1}` -> `200`, invalid data persisted
  - negative page query -> `400`, `detail="Page index must not be less than zero"`

## 이번 Todo의 결론

- 이 lab은 JPA persistence boundary를 설명하는 데는 성공하지만, API contract는 아직 완전히 polished optimistic locking surface가 아니다.
- 문서에 반드시 남겨야 할 현재 한계:
  - validation annotation이 runtime에서 적용되지 않음
  - update response가 incremented version을 바로 보여 주지 않음
  - Querydsl은 dependency만 있고 query path는 아직 없음
