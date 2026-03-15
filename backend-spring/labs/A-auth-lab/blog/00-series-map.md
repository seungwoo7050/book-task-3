# A-auth-lab series map

이 랩은 "Spring으로 auth를 만들었다"기보다, 로컬 계정 인증 lifecycle을 어디까지 baseline으로 설명할지 정하는 scaffold에 가깝다. `register -> login -> refresh -> logout -> me` 표면은 분명히 있지만, 실제 구현은 in-memory map, 가짜 bcrypt prefix, query-param 기반 `me`, 비활성화된 Spring Security CSRF 위에 올라가 있다.

처음 읽을 때는 `problem/README.md`로 요구 범위를 잡고, `AuthController`와 `AuthDemoService`에서 실제 경계를 확인한 뒤, `SecurityConfig`, `GlobalExceptionHandler`, `AuthFlowApiTest`, 수동 `bootRun + curl` 결과로 "무엇이 모델링됐고 무엇이 아직 보안 기능이 아닌가"를 닫는 순서가 가장 좋다.

## 이 글에서 볼 것

- refresh rotation과 `X-CSRF-TOKEN`이 Spring Security 기능이 아니라 controller/service 레벨 모델링으로 구현돼 있다는 점
- JPA, Redis, Kafka, Mail starter를 깔아 두었어도 auth 핵심은 `ConcurrentHashMap` 기반 demo service라는 점
- `/api/v1/auth/me`가 인증 없이 `email` query param만으로 동작하고 `passwordHash`까지 응답하는 현재 위험한 상태

## source of truth

- `labs/A-auth-lab/README.md`
- `labs/A-auth-lab/problem/README.md`
- `labs/A-auth-lab/spring/README.md`
- `labs/A-auth-lab/spring/build.gradle.kts`
- `labs/A-auth-lab/spring/Makefile`
- `labs/A-auth-lab/spring/src/main/java/com/webpong/study2/app/auth/api/AuthController.java`
- `labs/A-auth-lab/spring/src/main/java/com/webpong/study2/app/auth/application/AuthDemoService.java`
- `labs/A-auth-lab/spring/src/main/java/com/webpong/study2/app/global/security/SecurityConfig.java`
- `labs/A-auth-lab/spring/src/main/java/com/webpong/study2/app/global/error/GlobalExceptionHandler.java`
- `labs/A-auth-lab/spring/src/main/java/com/webpong/study2/app/global/logging/TraceIdFilter.java`
- `labs/A-auth-lab/spring/src/main/java/com/webpong/study2/app/global/api/HealthController.java`
- `labs/A-auth-lab/spring/src/main/java/com/webpong/study2/app/global/api/LabInfoController.java`
- `labs/A-auth-lab/spring/src/main/resources/application.yml`
- `labs/A-auth-lab/spring/src/main/resources/db/migration/V1__init.sql`
- `labs/A-auth-lab/spring/src/test/java/com/webpong/study2/app/AuthFlowApiTest.java`
- `labs/A-auth-lab/spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
- `labs/A-auth-lab/spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`

## 구현 흐름 한눈에 보기

1. `AuthController`가 `/api/v1/auth/register|login|refresh|logout|me`를 노출한다.
2. `AuthDemoService`는 사용자와 세션을 `ConcurrentHashMap`에 저장하고, password는 실제 hash가 아니라 `"bcrypt$" + password` 문자열로 비교한다.
3. refresh는 기존 refresh token을 제거한 뒤 새 access/refresh/csrf token을 발급한다.
4. `SecurityConfig`는 CSRF를 비활성화하고 `/api/v1/**`를 전부 `permitAll()`로 열어 둔다.
5. `GlobalExceptionHandler`는 `IllegalArgumentException`과 `MethodArgumentNotValidException`만 ProblemDetail로 감싼다.
6. 수동 실행 결과 `invalid register -> 201`, `invalid me -> 500`, unauthenticated `me -> passwordHash` 노출이 현재 한계로 드러난다.

## 대표 검증

로컬 `make lint|test|smoke`는 현재 머신에서 JRE가 없어 바로 실패했다. 대신 같은 프로젝트를 JDK 컨테이너에서 재실행했다.

```bash
$ docker run --rm -u $(id -u):$(id -g) \
  -v "$PWD":/workspace -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
BUILD SUCCESSFUL

$ docker run --rm -u $(id -u):$(id -g) \
  -v "$PWD":/workspace -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'
BUILD SUCCESSFUL

$ docker run --rm -u $(id -u):$(id -g) \
  -v "$PWD":/workspace -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
BUILD SUCCESSFUL
```

```bash
$ curl -s http://localhost:18080/api/v1/auth/me?email=spring@example.com
{"userId":"...","email":"spring@example.com","passwordHash":"bcrypt$pw-1234","verified":false}

$ curl -s -X POST http://localhost:18080/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"not-an-email","password":""}'
{"userId":"...","email":"not-an-email","verificationToken":"..."}
```

## 지금 시점의 한계

- `register`와 `login` request body에는 `@Valid`가 없어 invalid email/blank password도 현재는 통과한다.
- `/api/v1/auth/me`는 인증이 아니라 query param `email`로 사용자를 찾고, `passwordHash`를 그대로 응답한다.
- `GlobalExceptionHandler`는 `ConstraintViolationException`을 처리하지 않아 invalid `me?email=...`는 ProblemDetail `400`이 아니라 기본 `500`으로 떨어진다.
- `HealthController`의 `live`와 `ready`는 의존성 확인이 아니라 정적 `UP` 응답이다.
- Flyway/JPA는 marker table 하나만 만들고, 실제 auth persistence나 repository 계층은 아직 없다.
