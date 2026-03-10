# Debug Log — 네 번의 실패에서 배운 것

## 실패 1: UserRoleEntity에 createdAt이 없었다

`./gradlew test --tests '*Study2ApplicationTests'`를 돌리자 애플리케이션 컨텍스트 초기화 중 `NULL not allowed for column "CREATED_AT"` 예외가 터졌다. 처음에는 "user_roles 테이블은 role name과 user id만 있으면 충분하지 않나?"라고 생각했다. 하지만 테스트 리포트를 보면 `insert into user_roles (role_name,user_id,id) values (?,?,default)`가 출력되었고, H2가 `CREATED_AT` null 제약 위반을 보고하고 있었다.

**근본 원인**: `V2__commerce.sql`에서 `user_roles.created_at`을 `NOT NULL`로 정의했는데, `UserRoleEntity`에는 해당 필드가 없었다. Flyway 스키마와 JPA entity가 서로 다른 계약을 가지고 있었다.

**수정**: `UserRoleEntity`에 `createdAt` 필드를 추가하고 생성자에서 `Instant.now()`를 넣었다. INSERT 시 JPA가 `created_at` 값을 함께 전달하므로 스키마 제약을 충족한다. `./gradlew test --tests '*Study2ApplicationTests'`가 통과했다.

**남은 취약점**: Flyway 스키마와 entity가 다시 어긋나면 비슷한 문제가 반복된다. schema/entity mismatch를 더 빨리 드러내는 migration smoke test가 있으면 좋겠지만, 이 캡스톤에서는 추가하지 않았다.

---

## 실패 2: CartState의 isEmpty()가 Jackson 직렬화에 노출되었다

`./gradlew test --tests '*RedisCartStoreTest'`에서 `UnrecognizedPropertyException`이 발생하며 `CartState` 역직렬화가 실패했다. 단순 getter만 있으면 Jackson이 문제없이 처리할 거라 생각했는데, 실상은 달랐다.

`CartState`의 `isEmpty()` 메서드가 Jackson에게 boolean property `empty`로 인식되었다. 직렬화 결과에 `"empty": true`가 들어갔고, 역직렬화 시에는 `empty`를 받을 setter가 없어 실패한 것이다.

**근본 원인**: 도메인 편의 메서드 `isEmpty()`가 JSON 직렬화 계약에 의도치 않게 노출되었다. 도메인 모델의 편의 API와 저장 포맷이 충돌한 사례이다.

**수정**: `CartState.isEmpty()`에 `@JsonIgnore`를 붙였다. Redis에 저장되는 cart JSON이 `items`만 포함하게 되어 역직렬화 계약이 단순해졌다. `RedisCartStoreTest`가 통과했다.

**남은 취약점**: cart payload versioning 전략이 없다. Redis에 저장된 예전 포맷의 payload를 읽는 compatibility test가 필요할 수 있지만, 이 캡스톤에서는 추가하지 않았다.

---

## 실패 3: @KafkaListener의 placeholder가 해석되지 않았다

`./gradlew test --tests '*CommerceMessagingIntegrationTest'`에서 `Could not resolve placeholder 'spring.application.name'`이 발생하며 `orderPaidEventConsumer` bean 생성이 실패했다. `@KafkaListener(groupId = "${spring.application.name}")`이 언제나 해석 가능할 것이라 생각했지만, Testcontainers 기반 컨텍스트에서는 Kafka listener post-processor가 해당 placeholder를 해석하지 못했다.

**근본 원인**: listener annotation 안의 placeholder 해석 시점이 예상보다 엄격했고, 테스트 컨텍스트에서는 `spring.application.name`을 해당 위치에서 안정적으로 읽지 못했다.

**수정**: `@KafkaListener`의 `groupId`를 `"commerce-backend-v2"` 고정 문자열로 교체했다. listener 초기화가 placeholder 해석에 의존하지 않게 되어 컨텍스트가 안정적으로 올라왔다. `CommerceMessagingIntegrationTest`가 통과했다.

**남은 취약점**: 환경별로 consumer group을 바꾸고 싶다면 별도 config bean이나 container factory 수준의 구성이 필요하다. messaging-enabled=true 프로파일에서 컨텍스트만 띄우는 smoke test를 분리해 두면 이 종류의 실패를 더 빨리 잡을 수 있다.

---

## 실패 4: Spotless format violation — 컴파일되면 lint도 통과할까?

`make lint`를 돌리자 `spotlessJavaCheck`가 대량의 format violation을 보고했다. 코드가 컴파일되면 formatter도 대체로 통과할 것이라 생각했지만, Google Java Format의 줄바꿈, 인자 정렬, import 정리 규칙은 컴파일과 무관하게 적용된다.

**근본 원인**: 빠르게 기능을 붙이는 과정에서 formatter를 수동으로 맞추지 않았다.

**수정**: `./gradlew spotlessApply --no-daemon`를 실행한 뒤 `make lint`를 다시 돌려 통과시켰다. 저장소의 lint 기준은 수동 포맷이 아니라 Spotless 결과물이기 때문에, 기능 추가 직후 `spotlessCheck`를 바로 돌리는 습관이 필요하다.

---

## 공통 패턴

네 실패 모두 "이쪽이 맞으면 저쪽도 맞겠지"라는 가정에서 비롯되었다. 스키마가 맞으면 entity도 맞고, getter가 있으면 Jackson도 되고, application.yml에 값이 있으면 annotation에서도 읽히고, 컴파일이 되면 lint도 통과한다는 식이다. 실제로는 각 계약이 **독립적으로 검증되어야** 한다. 이 캡스톤에서 가장 반복된 교훈이다.
