# B-federation-security-lab series map

이 랩은 local auth 다음에 federation, second factor, audit를 붙이는 척하지만, 실제 구현은 "인증 강화 기능의 계약을 먼저 흉내 내는 scaffold"에 더 가깝다. authorize URL, callback payload, TOTP setup/verify, audit trail 표면은 있지만, 실제 provider 연동도 없고 강제 보호 경계도 거의 없다.

처음 읽을 때는 `problem/README.md`로 요구 범위를 잡고, `FederationSecurityController`와 `FederationSecurityDemoService`가 실제로 무엇을 하고 무엇은 하지 않는지 본 뒤, `SecurityConfig`, `FederationSecurityApiTest`, 수동 `bootRun + curl` 결과로 현재 보안 강도를 닫는 순서가 가장 좋다.

## 이 글에서 볼 것

- Google OAuth2가 실제 연동이 아니라 `authorize URL + callback body` 계약 수준으로만 모델링돼 있다는 점
- TOTP setup이 secret과 `expectedCode`를 응답에 그대로 노출하는 demo 흐름이라는 점
- `/api/v1/audit-events`, callback, 2FA endpoint가 모두 무인증으로 열려 있고 invalid body도 현재 `200`으로 통과한다는 점

## source of truth

- `labs/B-federation-security-lab/README.md`
- `labs/B-federation-security-lab/problem/README.md`
- `labs/B-federation-security-lab/spring/README.md`
- `labs/B-federation-security-lab/spring/build.gradle.kts`
- `labs/B-federation-security-lab/spring/Makefile`
- `labs/B-federation-security-lab/spring/src/main/java/com/webpong/study2/app/federation/api/FederationSecurityController.java`
- `labs/B-federation-security-lab/spring/src/main/java/com/webpong/study2/app/federation/application/FederationSecurityDemoService.java`
- `labs/B-federation-security-lab/spring/src/main/java/com/webpong/study2/app/global/security/SecurityConfig.java`
- `labs/B-federation-security-lab/spring/src/main/java/com/webpong/study2/app/global/error/GlobalExceptionHandler.java`
- `labs/B-federation-security-lab/spring/src/main/java/com/webpong/study2/app/global/logging/TraceIdFilter.java`
- `labs/B-federation-security-lab/spring/src/main/resources/application.yml`
- `labs/B-federation-security-lab/spring/src/main/resources/db/migration/V1__init.sql`
- `labs/B-federation-security-lab/spring/src/test/java/com/webpong/study2/app/FederationSecurityApiTest.java`
- `labs/B-federation-security-lab/spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
- `labs/B-federation-security-lab/spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`

## 구현 흐름 한눈에 보기

1. `GET /api/v1/auth/google/authorize`는 Google authorize URL처럼 보이는 문자열과 state/nonce를 만든다.
2. `POST /api/v1/auth/google/callback`은 email과 subject를 그대로 저장하고 linked identity를 반환한다.
3. `POST /api/v1/auth/2fa/setup`은 secret을 만들고 recovery code 3개와 `expectedCode`를 응답에 같이 넣는다.
4. `POST /api/v1/auth/2fa/verify`는 stored expected code와 일치 여부만 보고 `verified: true|false`를 돌려준다.
5. 모든 단계는 `auditEvents`에 흔적을 남기고, `GET /api/v1/audit-events`로 무인증 조회된다.
6. `SecurityConfig`는 A-auth-lab과 마찬가지로 CSRF를 끄고 `/api/v1/**` 전체를 `permitAll()`로 둔다.

## 대표 검증

로컬 `make lint|test|smoke`는 현재 머신에 JRE가 없어 바로 실행되지 않았다. 대신 JDK 컨테이너와 수동 `bootRun`으로 다시 확인했다.

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
$ GET /api/v1/auth/google/authorize
200 {"url":"https://accounts.google.com/o/oauth2/v2/auth?...","state":"...","nonce":"..."}

$ POST /api/v1/auth/2fa/setup
200 {"secret":"A5E0C484627B","recoveryCodes":["rec-1","rec-2","rec-3"],"expectedCode":"A5E0C4"}

$ POST /api/v1/auth/google/callback {"email":"not-an-email","subject":""}
200 {"email":"not-an-email","provider":"google","subject":""}
```

## 지금 시점의 한계

- request body record에 `@Email`, `@NotBlank`가 있어도 controller parameter에 `@Valid`가 없어 invalid callback/setup/verify payload가 현재 통과한다.
- TOTP setup 응답이 `secret`뿐 아니라 `expectedCode`까지 그대로 노출한다.
- `BAD_VERIFY`도 `400`이 아니라 `200 {"verified":false}`로 끝나며 rate limiting이나 attempt tracking이 없다.
- audit trail은 보호 대상이 아니라 공개 조회 endpoint로 노출된다.
- auditEvents 저장소는 `ArrayList`라 동시 요청 상황을 고려한 구조가 아니다.
