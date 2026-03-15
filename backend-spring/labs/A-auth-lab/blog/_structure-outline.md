# A-auth-lab structure outline

## 글 목표

- 이 랩을 "auth 구현"보다 "auth lifecycle을 먼저 잘라 낸 scaffold"로 보이게 쓴다.
- Spring starter와 실제 auth 동작 사이의 간격을 숨기지 않는다.

## 글 순서

1. baseline을 lifecycle로 잡은 단계
2. refresh rotation과 CSRF를 application-level 규칙으로 둔 단계
3. SecurityConfig, validation, `/me` 응답이 드러내는 현재 구멍
4. 컨테이너 기반 Gradle 검증과 수동 `bootRun` 확인으로 마무리

## 반드시 넣을 코드 앵커

- `AuthFlowApiTest.registerLoginAndRefreshFlowWorks()`
- `AuthDemoService.refresh()`
- `AuthDemoService.requireSession()`
- `SecurityConfig.securityFilterChain()`
- `AuthDemoService.UserProfile`

## 반드시 넣을 CLI

```bash
docker run --rm -u $(id -u):$(id -g) -v "$PWD":/workspace -w /workspace \
  eclipse-temurin:21-jdk bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
docker run --rm -u $(id -u):$(id -g) -v "$PWD":/workspace -w /workspace \
  eclipse-temurin:21-jdk bash -lc './gradlew test'
docker run --rm -u $(id -u):$(id -g) -p 18080:8080 -v "$PWD":/workspace -w /workspace \
  eclipse-temurin:21-jdk bash -lc './gradlew bootRun'
```

## 핵심 개념

- refresh rotation은 단순 재발급이 아니라 세션 재생산 규칙이다.
- 현재 CSRF는 Spring Security 기능이 아니라 service 규칙이다.
- validation, authz, response redaction은 아직 scaffold 수준이다.
