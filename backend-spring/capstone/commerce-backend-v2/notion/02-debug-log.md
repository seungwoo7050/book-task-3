# Debug Log

## Failure 1

- failing command or request:
  - `./gradlew test --tests '*Study2ApplicationTests' --no-daemon`
- exact symptom:
  - 애플리케이션 컨텍스트 초기화 중 `NULL not allowed for column "CREATED_AT"` 예외가 발생했다.
- first incorrect assumption:
  - `user_roles`는 role name과 user id만 있으면 충분하고, JPA entity에 `createdAt`이 없어도 될 것이라고 생각했다.
- evidence collected:
  - 테스트 리포트에 `insert into user_roles (role_name,user_id,id) values (?,?,default)`가 출력되었고, H2가 `CREATED_AT` null 제약 위반을 보고했다.

## Root cause 1

`V2__commerce.sql`에서 `user_roles.created_at`을 `not null`로 정의했는데, `UserRoleEntity`에는 해당 필드가 없었다. 즉 스키마와 entity 모델이 서로 다른 계약을 가지고 있었다.

## Fix and verification 1

- code or config change made:
  - `UserRoleEntity`에 `createdAt` 필드를 추가하고 생성자에서 `Instant.now()`를 넣었다.
- why that change addresses the cause:
  - INSERT 시 JPA가 `created_at` 값을 함께 넘기게 되어 스키마 제약을 충족한다.
- command, test, or log line that proved the fix:
  - `./gradlew test --tests '*Study2ApplicationTests' --tests '*RedisCartStoreTest' --no-daemon`

## Follow-up debt 1

- what brittle area remains even after the fix
  - Flyway 스키마와 entity가 다시 어긋나면 비슷한 문제가 반복될 수 있다.
- what regression test should be added if time allows
  - schema/entity mismatch를 더 빨리 드러내는 migration smoke test를 별도로 둘 수 있다.

---

## Failure 2

- failing command or request:
  - `./gradlew test --tests '*RedisCartStoreTest' --no-daemon`
- exact symptom:
  - `UnrecognizedPropertyException`이 발생하며 `CartState` 역직렬화가 실패했다.
- first incorrect assumption:
  - 단순 getter만 있으면 Jackson이 문제없이 serialize/deserialize할 것이라고 생각했다.
- evidence collected:
  - `CartState`의 `isEmpty()`가 Jackson에게 boolean property처럼 보였고, 직렬화 결과에 `empty`가 들어갔다.
  - 역직렬화 시에는 `empty`를 받을 setter가 없어 실패했다.

## Root cause 2

도메인 편의 메서드 `isEmpty()`가 JSON 계약에 의도치 않게 노출되었다. 즉 도메인 모델의 편의 API와 저장 포맷이 충돌했다.

## Fix and verification 2

- code or config change made:
  - `CartState.isEmpty()`에 `@JsonIgnore`를 붙였다.
- why that change addresses the cause:
  - Redis에 저장되는 cart JSON이 `items`만 포함하게 되어 역직렬화 계약이 단순해졌다.
- command, test, or log line that proved the fix:
  - `./gradlew test --tests '*RedisCartStoreTest' --no-daemon`

## Follow-up debt 2

- what brittle area remains even after the fix
  - cart payload versioning 전략이 없다.
- what regression test should be added if time allows
  - Redis에 저장된 예전 payload를 읽는 compatibility test를 추가할 수 있다.

---

## Failure 3

- failing command or request:
  - `./gradlew test --tests '*CommerceMessagingIntegrationTest' --no-daemon`
- exact symptom:
  - `Could not resolve placeholder 'spring.application.name'`로 `orderPaidEventConsumer` bean 생성이 실패했다.
- first incorrect assumption:
  - `@KafkaListener(groupId = "${spring.application.name}")`는 언제나 해석 가능할 것이라고 생각했다.
- evidence collected:
  - Testcontainers 기반 컨텍스트에서 Kafka listener post-processor가 해당 placeholder를 해석하지 못했다.
  - 실패 지점은 `OrderPaidEventConsumer` 초기화였다.

## Root cause 3

listener annotation 안의 placeholder 해석 시점이 예상보다 엄격했고, 현재 테스트 컨텍스트에서는 `spring.application.name`을 해당 위치에서 안정적으로 읽지 못했다.

## Fix and verification 3

- code or config change made:
  - `@KafkaListener`의 `groupId`를 `commerce-backend-v2` 고정 문자열로 바꿨다.
- why that change addresses the cause:
  - listener 초기화가 placeholder 해석에 의존하지 않게 되어 컨텍스트가 안정적으로 올라온다.
- command, test, or log line that proved the fix:
  - `./gradlew test --tests '*CommerceMessagingIntegrationTest' --no-daemon`

## Follow-up debt 3

- what brittle area remains even after the fix
  - 환경별로 consumer group을 바꾸고 싶다면 별도 config bean이나 container factory 수준의 구성이 필요하다.
- what regression test should be added if time allows
  - messaging-enabled=true profile에서 컨텍스트만 띄우는 smoke test를 분리해 둘 수 있다.

---

## Failure 4

- failing command or request:
  - `make lint`
- exact symptom:
  - `spotlessJavaCheck`가 대량의 format violation을 보고했다.
- first incorrect assumption:
  - 코드가 컴파일되면 formatter도 대체로 통과할 것이라고 생각했다.
- evidence collected:
  - `spotlessJavaCheck`가 여러 파일에서 줄바꿈, 인자 정렬, import 정리를 지적했다.

## Root cause 4

빠르게 기능을 붙이는 과정에서 Google Java Format 규칙을 수동으로 맞추지 않았다.

## Fix and verification 4

- code or config change made:
  - `./gradlew spotlessApply --no-daemon`를 실행한 뒤 `make lint`를 다시 돌렸다.
- why that change addresses the cause:
  - 저장소의 lint 기준이 수동 포맷이 아니라 Spotless 결과물이기 때문이다.
- command, test, or log line that proved the fix:
  - `make lint`

## Follow-up debt 4

- what brittle area remains even after the fix
  - 큰 패치를 한 번에 넣으면 formatter diff가 커져 리뷰성이 떨어진다.
- what regression test should be added if time allows
  - 기능 추가 직후 `spotlessCheck`를 더 자주 돌리는 작업 습관이 필요하다.
