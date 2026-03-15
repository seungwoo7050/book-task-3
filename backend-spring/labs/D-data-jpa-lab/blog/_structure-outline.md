# D-data-jpa-lab structure outline

## 글 목표

- 이 lab을 JPA CRUD 자랑이 아니라 persistence contract 해설로 다시 쓴다.
- `@Version`의 존재와 실제 API 경험 사이의 차이를 중심에 둔다.
- Querydsl-ready, validation, paging error를 모두 "현재 구현됨"과 "자리만 있음"으로 분리해 적는다.

## 글 순서

1. controller/test가 product CRUD보다 stale-version conflict를 먼저 보여 준다는 점을 확정한다.
2. migration, entity, service를 이어 읽으면서 version check가 수동인지 자동인지 설명한다.
3. validation 공백과 update response version 노출 문제를 manual HTTP 결과와 연결한다.
4. Querydsl dependency와 실제 source 부재를 짚고 현재 lab의 범위를 닫는다.

## 반드시 넣을 코드 앵커

- `DataApiController.update()`
- `DataApiService.list()`
- `DataApiService.updatePrice()`
- `ProductEntity.version`
- `V2__lab_products.sql`
- `DataApiTest.productCrudAndConflictCheckWork()`

## 반드시 넣을 검증 신호

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'

docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'

docker run --rm -u $(id -u):$(id -g) -p 18083:8080 \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew bootRun'
```

## 반드시 남길 한계

- invalid create가 `200`으로 저장되는 상태
- update response version과 persisted version이 즉시 일치하지 않는 상태
- Querydsl이 build dependency 수준에 머무는 상태
