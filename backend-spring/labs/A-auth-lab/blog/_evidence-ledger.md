# A-auth-lab evidence ledger

이 경로의 git history를 따로 따라가기보다, 실제 코드와 재실행 결과를 기준으로 chronology를 다시 세웠다. 특히 이번에는 로컬 JRE 부재, 컨테이너 기반 Gradle 검증, 수동 `bootRun` HTTP 확인을 함께 묶었다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | baseline auth 범위를 lifecycle로 고정한다 | `README.md`, `problem/README.md`, `spring/src/test/java/.../AuthFlowApiTest.java`, `AuthController.java`, `AuthDemoService.java` | 로그인과 토큰 발급만 있으면 충분할 것 같았다 | register, login, refresh, `me`를 한 흐름으로 읽되 실제 구현은 in-memory demo service라는 점까지 함께 확인했다 | `docker run ... eclipse-temurin:21-jdk bash -lc './gradlew test'` | `BUILD SUCCESSFUL`, `AuthFlowApiTest`/`HealthApiTest` 통과 | `AuthFlowApiTest.registerLoginAndRefreshFlowWorks()`, `Map<String, UserProfile> users = new ConcurrentHashMap<>()` | 이 랩의 baseline은 persistence 깊이가 아니라 lifecycle 설명 범위다 | refresh/CSRF가 어느 층에 구현됐는지 봐야 한다 |
| 2 | Phase 2 | refresh rotation과 CSRF 경계를 확인한다 | `AuthController.refresh()`, `AuthDemoService.refresh()`, `AuthDemoService.requireSession()` | Spring Security CSRF가 이 흐름을 담당할 것 같았다 | `X-CSRF-TOKEN` 헤더와 refresh token을 service 레벨에서 대조하고, rotation 시 기존 refresh token을 삭제한 뒤 새 token 묶음을 발급하는 구조를 확인했다 | `docker run ... ./gradlew bootRun`; `curl -X POST /api/v1/auth/login`; `curl -X POST /api/v1/auth/refresh` | login `200`, refresh `200`, 잘못된 CSRF는 `400 {"detail":"CSRF token mismatch"}` | `sessions.remove(refreshToken)`, `if (!session.csrfToken().equals(csrfToken))` | 이 랩의 CSRF는 Spring Security 기능이 아니라 application-level modeling이다 | SecurityConfig와 예외 처리가 이 모델과 맞는지 확인해야 한다 |
| 3 | Phase 3 | 보안 경계와 validation의 실제 상태를 본다 | `SecurityConfig.java`, `GlobalExceptionHandler.java`, `TraceIdFilter.java`, `AuthController.java` | API body에 `@Email`, `@NotBlank`가 있으니 validation도 대체로 맞을 것 같았다 | CSRF disabled + `/api/v1/** permitAll`, `me`는 query param 기반 무인증 조회, body는 `@Valid` 부재로 invalid register 통과, invalid `me`는 `ConstraintViolationException`이 handler 밖으로 새는 점을 확인했다 | `curl -X POST /api/v1/auth/register -d '{"email":"not-an-email","password":""}'`; `curl /api/v1/auth/me?email=not-an-email` | invalid register `201`, invalid `me`는 기본 `500`, health 응답엔 `X-Trace-Id` 헤더 포함 | `http.csrf(csrf -> csrf.disable())`, `auth.requestMatchers("/api/v1/**"...).permitAll()`, `public UserProfile me(@RequestParam @Email String email)` | annotation이 있다는 사실과 실제 validation/runtime 보장은 다르다 | `/me` 응답이 무엇을 노출하는지 확인해야 한다 |
| 4 | Phase 4 | 실제 응답이 현재 한계를 어떻게 드러내는지 기록한다 | `AuthDemoService.UserProfile`, `HealthController.java`, `V1__init.sql`, `build.gradle.kts` | docs가 말하는 persistence/메일/redis 준비도가 auth API에도 반영됐을 것 같았다 | `/me` 응답이 `passwordHash`를 그대로 노출하고, health는 정적 `UP`, Flyway는 marker table 하나만 만들며, starter 의존성 다수는 아직 scaffold 준비 수준임을 문서에 반영했다 | `curl /api/v1/auth/me?email=spring@example.com`; `docker run ... ./gradlew spotlessCheck checkstyleMain checkstyleTest`; `docker run ... ./gradlew test --tests "*SmokeTest"` | `/me`에서 `"passwordHash":"bcrypt$pw-1234"`, lint/test/smoke 모두 컨테이너 안에서 `BUILD SUCCESSFUL` | `public record UserProfile(String userId, String email, String passwordHash, boolean verified)`, `create table if not exists study2_marker` | 이 랩은 auth 기능 구현보다 auth shape와 다음 단계의 빈칸을 보여 주는 scaffold다 | federation, real persistence, external mail은 다음 랩으로 넘긴다 |

## 근거 파일

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
- `labs/A-auth-lab/spring/src/main/resources/application.yml`
- `labs/A-auth-lab/spring/src/main/resources/db/migration/V1__init.sql`
- `labs/A-auth-lab/spring/src/test/java/com/webpong/study2/app/AuthFlowApiTest.java`
- `labs/A-auth-lab/spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
- `labs/A-auth-lab/spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
