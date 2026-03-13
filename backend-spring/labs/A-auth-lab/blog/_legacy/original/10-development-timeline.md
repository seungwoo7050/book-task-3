# 로컬 인증 흐름을 먼저 in-memory로 고정한 이유

`A-auth-lab`이 프로젝트 전체에서 맡는 자리는 아주 선명하다. OAuth나 2FA를 더하기 전에, 로컬 계정 인증이 어떤 상태 전이를 가져야 하는지 먼저 닫는 자리다. macOS에서 VSCode를 열고 통합 터미널로 `make`와 `./gradlew`를 직접 호출하는 흐름을 기준으로 보면, 이 랩의 구현 순서는 문서가 scope를 고정하고, 서비스가 상태를 만들고, MockMvc 테스트가 그 상태 전이를 증명하는 순서로 읽힌다.

## 구현 순서 요약

- `problem/README.md`와 `docs/README.md`가 로컬 인증의 현재 범위를 `register`, `login`, `refresh`, `logout`, `me`로 먼저 닫는다.
- `AuthDemoService`가 사용자 저장소와 세션 저장소를 분리해 refresh rotation과 CSRF 검사를 구현한다.
- `AuthController`가 `/api/v1/auth/*` surface를 API로 드러낸다.
- `AuthFlowApiTest`가 성공 경로와 실패 경로를 같이 고정한다.

## Phase 1

### Session 1

- 당시 목표:
  - 로컬 인증 랩이 어디까지를 "기본 흐름"으로 다루는지 먼저 잘라 낸다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - persistence나 외부 provider를 초반에 섞으면 인증의 최소 lifecycle이 흐려진다.
- 실제 진행:
  - `problem/README.md`는 회원가입, 로그인, refresh, logout, `me`를 성공 기준으로 못 박고, OAuth와 production-grade persistence는 현재 단계에서 제외했다.
  - `docs/README.md`는 refresh rotation, CSRF, Mailpit-ready 환경을 지금 설명할 이유와 일부러 남긴 범위를 분리했다.
  - `spring/README.md`는 VSCode 터미널에서 바로 따라갈 수 있는 명령 목록을 남겼다.

CLI:

```bash
cp .env.example .env
make run
```

검증 신호:

- 실행 진입점이 `spring/README.md`에 고정돼 있어서 IDE 실행 버튼 없이도 같은 순서를 재현할 수 있다.
- 문서가 "지금 구현한 것"과 "일부러 남긴 것"을 분리해서, 이후 코드가 왜 in-memory인지 먼저 이해하게 만든다.

핵심 코드:

```java
@RequestMapping("/api/v1/auth")
public class AuthController {
```

왜 이 코드가 중요했는가:

- scope를 먼저 잘라 놓지 않으면 컨트롤러 경로가 계속 넓어진다. 이 랩은 `/api/v1/auth` 밑에 로컬 인증 lifecycle만 두겠다는 선언부터 시작한다.

새로 배운 것:

- 인증 랩의 첫 단계는 해시 알고리즘보다 "지금 설명할 lifecycle이 어디서 시작하고 끝나는가"를 고정하는 일이다.

다음:

- in-memory여도 refresh rotation과 CSRF를 납득 가능한 형태로 구현할 수 있는지 본다.

## Phase 2

### Session 1

- 당시 목표:
  - 로컬 인증 lifecycle을 가장 작은 상태 저장 구조로 닫는다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/auth/application/AuthDemoService.java`
  - `spring/src/main/java/com/webpong/study2/app/auth/api/AuthController.java`
- 처음 가설:
  - refresh token을 새로 발급만 하면 rotation을 설명했다고 말할 수 없고, 이전 토큰이 무효가 되는 시점까지 함께 보여 줘야 한다.
- 실제 진행:
  - `users`와 `sessions`를 별도 `ConcurrentHashMap`으로 두고, 계정 정보와 로그인 세션을 분리했다.
  - `login()`은 access token, refresh token, CSRF token을 한 번에 만든다.
  - `refresh()`는 기존 refresh token을 제거한 뒤 새 세션 스냅샷을 저장한다.
  - `logout()`은 refresh token과 CSRF token이 같이 맞아야 세션을 제거한다.

CLI:

```bash
make test
```

검증 신호:

- `2026-03-13` macOS + VSCode 통합 터미널에서 `make test`를 다시 실행했을 때 `BUILD SUCCESSFUL`이 확인됐다.

핵심 코드:

```java
private SessionSnapshot requireSession(String refreshToken, String csrfToken) {
  SessionSnapshot session = sessions.get(refreshToken);
  if (session == null) {
    throw new IllegalArgumentException("Refresh token not found");
  }
  if (!session.csrfToken().equals(csrfToken)) {
    throw new IllegalArgumentException("CSRF token mismatch");
  }
  return session;
}
```

왜 이 코드가 중요했는가:

- 이 랩에서 refresh token은 혼자 유효성을 가지지 않는다. CSRF token이 같이 맞아야 세션으로 인정한다는 규칙이 여기에 압축돼 있다.

새로 배운 것:

- refresh rotation은 저장소 설계 문제이기도 하지만, 더 직접적으로는 "어떤 조합을 세션 증거로 인정할 것인가"를 정하는 규칙이다.

다음:

- 이 규칙이 진짜로 API surface에 드러나는지 테스트로 증명한다.

## Phase 3

### Session 1

- 당시 목표:
  - 성공 경로와 실패 경로를 같이 고정해서 이 랩이 설명하려는 인증 경계를 테스트로 남긴다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/AuthFlowApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - 브라우저 cookie를 완전히 붙이지 않아도 MockMvc만으로 refresh/CSRF 경계를 충분히 드러낼 수 있다.
- 실제 진행:
  - `AuthFlowApiTest`에 회원가입 -> 로그인 -> refresh -> `me` 순서를 하나의 테스트 흐름으로 묶었다.
  - 잘못된 `X-CSRF-TOKEN`을 보냈을 때 `bad_request`가 나오는 실패 경로를 별도 테스트로 고정했다.
  - health, lab info smoke 테스트도 같이 남겨 scaffold가 깨지지 않는지 확인했다.

CLI:

```bash
make test
make smoke
docker compose up --build
```

검증 신호:

- `2026-03-13` 재실행 뒤 `build/test-results/test`에서 XML 리포트 4개가 생성됐고 `failures=0`이었다.
- 루트의 `docs/verification-report.md`에는 `2026-03-09` 기준 `make lint`, `make test`, `make smoke`, Compose health 확인 통과가 남아 있다.

핵심 코드:

```java
mockMvc
    .perform(
        post("/api/v1/auth/refresh")
            .header("X-CSRF-TOKEN", "csrf-invalid")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"refreshToken\":\"" + refreshToken + "\"}"))
    .andExpect(status().isBadRequest())
    .andExpect(jsonPath("$.code").value("bad_request"));
```

왜 이 코드가 중요했는가:

- 이 실패 테스트가 있어야 "CSRF mismatch도 인증 경계의 일부"라는 말이 추상 설명으로 끝나지 않는다.

새로 배운 것:

- 인증 흐름을 설명할 때는 성공 테스트보다 실패 테스트가 더 많은 설계 정보를 준다. 어떤 요청을 거부하는지가 곧 경계이기 때문이다.

다음:

- verify/reset endpoint, 사용자 persistence, 실제 response cookie 검증은 다음 확장 단계로 남긴다.
