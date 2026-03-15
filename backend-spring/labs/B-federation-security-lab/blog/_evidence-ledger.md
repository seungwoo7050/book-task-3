# B-federation-security-lab evidence ledger

이 랩도 세밀한 작업 로그 대신 실제 소스, 테스트, 컨테이너 기반 Gradle 검증, 수동 `bootRun` 결과를 기준으로 chronology를 다시 세웠다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | federation 경계를 provider 연동 전 단계에서 자른다 | `README.md`, `problem/README.md`, `FederationSecurityController.java`, `FederationSecurityApiTest.java` | live Google provider가 있어야 이 랩이 성립할 것 같았다 | authorize URL과 callback body를 먼저 API contract로 고정하고, 테스트도 URL 문자열과 `provider=google` 반환만 검증하는 수준으로 확인했다 | `docker run ... eclipse-temurin:21-jdk bash -lc './gradlew test'` | `BUILD SUCCESSFUL`, `FederationSecurityApiTest` 통과 | `GET /api/v1/auth/google/authorize`, `POST /api/v1/auth/google/callback` | federation의 첫 증명 대상은 provider SDK가 아니라 callback contract다 | second factor와 audit가 같은 흐름인지 봐야 한다 |
| 2 | Phase 2 | 2FA와 audit를 같은 상태 변화로 묶는다 | `FederationSecurityDemoService.java` | TOTP는 federation과 분리된 별도 기능처럼 보였다 | authorize/callback/setupTotp/verifyTotp를 한 서비스에 두고 각 단계마다 audit event를 남기는 구조를 확인했다 | `docker run ... bash -lc './gradlew test --tests "*SmokeTest"'`; `docker run ... bash -lc './gradlew bootRun'`; `curl /api/v1/auth/2fa/setup`; `curl /api/v1/audit-events` | smoke 통과, setup 응답에 recovery codes 존재, audit-events에서 각 단계 흔적 조회 가능 | `auditEvents.add(new AuditEvent(...))`, `return new TotpSetup(secret, List.of(...), expectedCode)` | 이 랩의 audit는 보호된 로그보다 상태 변화 설명용 surface에 가깝다 | 보안 강도가 실제로 어느 정도인지 수동 응답으로 확인해야 한다 |
| 3 | Phase 3 | validation과 보호 경계의 실제 상태를 본다 | `SecurityConfig.java`, `FederationSecurityController.java`, `GlobalExceptionHandler.java` | record field annotation이 있으니 invalid payload는 대체로 막힐 것 같았다 | CSRF disabled + `/api/v1/** permitAll`, controller body에 `@Valid` 부재, invalid callback body가 `200`으로 통과하는 점을 수동 재실행으로 확인했다 | `curl -X POST /api/v1/auth/google/callback -d '{\"email\":\"not-an-email\",\"subject\":\"\"}'` | invalid callback도 `200 {"email":"not-an-email","provider":"google","subject":""}` | `http.csrf(csrf -> csrf.disable())`, `auth.requestMatchers("/api/v1/**"...).permitAll()`, `public record CallbackRequest(@Email String email, @NotBlank String subject)` | annotation이 있어도 controller에 `@Valid`가 없으면 hardening은 생기지 않는다 | TOTP와 audit 응답이 어떤 정보를 노출하는지 기록해야 한다 |
| 4 | Phase 4 | 현재 surface가 노출하는 민감 정보와 한계를 문서에 남긴다 | `FederationSecurityDemoService.java`, `TraceIdFilter.java`, `build.gradle.kts` | 2FA와 audit가 있으니 이전 랩보다 훨씬 안전할 것 같았다 | setup이 `expectedCode`를 노출하고, `verify(false)`도 `200`, audit-events도 공개, 로컬 `make`는 JRE 부재로 막혀 컨테이너 기반 lint/test/smoke로 대체한 사실을 기록했다 | `docker run ... bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'`; `curl /api/v1/auth/2fa/setup`; `curl /api/v1/auth/2fa/verify`; `curl /api/v1/health/live` | lint/test/smoke 모두 컨테이너에서 `BUILD SUCCESSFUL`, health 응답에 `X-Trace-Id`, `setup`에 `expectedCode` 포함 | `public record TotpSetup(String secret, List<String> recoveryCodes, String expectedCode)` | 이 랩은 보안 기능을 완성한 게 아니라 다음 랩들에 앞서 인증 강화 surface를 설명 가능하게 만든 단계다 | authorization은 별도 문제로 분리해야 한다 |

## 근거 파일

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
