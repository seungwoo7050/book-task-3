# version conflict를 API 밖으로 숨기지 않은 이유

`D-data-jpa-lab`의 핵심은 JPA를 편의 기능으로 감추지 않는 데 있다. product를 만들고, page로 읽고, 가격을 바꾸고, 오래된 version으로 다시 바꾸려 할 때 실패하는 흐름이 같이 보여야 JPA가 진짜 설계 도구로 읽힌다. macOS + VSCode 통합 터미널 기준으로 `make test`를 돌리면 이 랩이 왜 `@Version`을 전면에 세우는지 훨씬 명확해진다.

## 구현 순서 요약

- `problem/README.md`와 `docs/README.md`가 JPA 랩의 중심을 optimistic locking과 pagination으로 고정한다.
- `ProductEntity`와 `ProductRepository`가 persistence 경계를 만든다.
- `DataApiService`가 create/list/updatePrice에 version contract를 넣는다.
- `DataApiTest`가 CRUD와 conflict를 같은 흐름에서 검증한다.

## Phase 1

### Session 1

- 당시 목표:
  - JPA 랩이 어디까지를 현재 범위로 볼지 먼저 고정한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - 복잡한 검색이나 큰 aggregate를 먼저 넣으면 JPA의 핵심 학습 포인트인 version 관리와 persistence 경계가 흐려진다.
- 실제 진행:
  - current scope를 Flyway-managed table, JPA entity/repository/service, page listing, optimistic locking으로 정리했다.
  - Querydsl 심화와 soft delete는 다음 단계로 분리했다.

CLI:

```bash
cp .env.example .env
make run
```

검증 신호:

- `spring/README.md`가 재현 명령을 고정했고, docs는 왜 larger catalog graph를 일부러 남겼는지 설명한다.

핵심 코드:

```java
@Table(name = "lab_products")
public class ProductEntity {
```

왜 이 코드가 중요했는가:

- entity를 어떤 테이블에 대응시키는지부터 노출해야 JPA 경계가 시작된다. 그래야 뒤의 migration과 service logic이 같은 문제를 다룬다는 사실이 이어진다.

새로 배운 것:

- JPA 학습의 첫 단계는 repository 메서드보다 entity가 어떤 테이블 사실을 감싸는지 분명히 하는 일이다.

다음:

- version과 pagination을 서비스 계약으로 올린다.

## Phase 2

### Session 1

- 당시 목표:
  - optimistic locking을 entity annotation에서 끝내지 않고 service 규칙으로 끌고 온다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/data/domain/ProductEntity.java`
  - `spring/src/main/java/com/webpong/study2/app/data/application/DataApiService.java`
- 처음 가설:
  - API가 version을 받지 않으면 충돌은 결국 "나중에 이상한 에러가 난다" 수준으로만 보인다.
- 실제 진행:
  - `ProductEntity`에 `@Version` 필드를 뒀다.
  - `list()`는 `PageRequest`를 써서 page/size, totalElements, totalPages, hasNext를 envelope로 묶었다.
  - `updatePrice()`는 요청으로 받은 version이 현재 엔티티 version과 다르면 즉시 `Version conflict`를 던졌다.

CLI:

```bash
make test
```

검증 신호:

- `2026-03-13` macOS + VSCode 통합 터미널에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.

핵심 코드:

```java
public ProductResponse updatePrice(long productId, long version, BigDecimal price) {
  ProductEntity product =
      productRepository
          .findById(productId)
          .orElseThrow(() -> new IllegalArgumentException("Product not found"));
  if (product.getVersion() != version) {
    throw new IllegalArgumentException("Version conflict");
  }
  product.changePrice(price);
  return ProductResponse.from(product);
}
```

왜 이 코드가 중요했는가:

- JPA의 optimistic locking을 service 로직에서 한 번 더 드러냈기 때문에, 이 랩은 "버전 충돌이 왜 나는가"를 인터뷰나 학습 기록에서 바로 설명할 수 있다.

새로 배운 것:

- 동시성 제어는 DB의 비밀스러운 기능이 아니라, 클라이언트가 어느 시점의 상태를 바탕으로 수정 요청을 보내는지에 대한 약속이다.

다음:

- 같은 version으로 두 번 patch했을 때 실제 API 응답이 어떻게 달라지는지 고정한다.

## Phase 3

### Session 1

- 당시 목표:
  - CRUD와 version conflict를 사용자 시나리오처럼 검증한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/DataApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - product 생성 후 `version=0`으로 한 번 성공하고 다시 `version=0`으로 실패시키면 optimistic locking의 의미가 가장 직관적으로 드러난다.
- 실제 진행:
  - product 생성, 목록 조회, 정상 업데이트, 오래된 version으로 재업데이트를 한 테스트 안에 묶었다.

CLI:

```bash
make test
make smoke
docker compose up --build
```

검증 신호:

- `2026-03-13` 재실행 후 XML 리포트 4개, `failures=0`이 확인됐다.
- `2026-03-09` 검증 기록에는 lint/test/smoke/Compose health 확인 통과가 남아 있다.

핵심 코드:

```java
mockMvc
    .perform(
        patch("/api/v1/products/{productId}", product.get("id").asLong())
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"price\":159.99,\"version\":0}"))
    .andExpect(status().isBadRequest())
    .andExpect(jsonPath("$.code").value("bad_request"));
```

왜 이 코드가 중요했는가:

- 버전 충돌은 로그로만 확인해선 안 된다. API 계약이 실제로 오래된 version을 거부한다는 사실이 테스트 응답에 남아야 한다.

새로 배운 것:

- JPA를 잘 설명하는 글은 "save가 된다"가 아니라 "어떤 수정은 왜 거부되는가"를 보여 주는 글이다.

다음:

- Querydsl 조건 조합, larger graph, soft delete는 이후 확장으로 남긴다.
