# A-auth-lab Evidence Ledger

- 복원 기준:
  - git commit granularity가 `2026-03-09`, `2026-03-10`, `2026-03-12` 수준으로 거칠어서 세션 chronology는 `problem/README.md`, `docs/README.md`, `spring/README.md`, 실제 소스, 테스트, `2026-03-13` 재실행 CLI로 다시 세웠다.
- 기존 blog 처리:
  - 기존 `blog/` 디렉터리가 없어서 `isolate-and-rewrite` 규칙상 격리 대상은 없었다.

## Phase 1

- 시간 표지: Phase 1
- 당시 목표:
  - 로컬 계정 인증 랩이 어디까지를 "기본 인증 흐름"으로 다루는지 먼저 고정한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - OAuth, persistence, 메일 인프라를 한 번에 넣으면 로컬 인증의 최소 경계가 흐려진다.
- 실제 조치:
  - 회원가입, 로그인, refresh rotation, logout, `me`를 현재 랩의 canonical scope로 선언했다.
  - Mailpit-ready 환경과 cookie + CSRF 설명 지점을 문서에 남기고, 실제 브라우저 통합과 외부 OAuth는 다음 랩으로 넘겼다.
- CLI:

```bash
cp .env.example .env
make run
```

- 검증 신호:
  - `spring/README.md`가 macOS + VSCode 통합 터미널 기준 진입점으로 `make run`, `make lint`, `make test`, `make smoke`, `docker compose up --build`를 고정했다.
- 핵심 코드 앵커:
  - 이후 구현은 `AuthDemoService`, `AuthController`, `AuthFlowApiTest`의 세 파일을 중심으로 읽히도록 구조가 닫혀 있다.
- 새로 배운 것:
  - 인증 랩의 첫 단계는 "어떤 기술을 붙였는가"보다 "어떤 lifecycle을 한 덩어리로 설명할 것인가"를 먼저 정하는 일이다.
- 다음:
  - persistence 없이도 register/login/refresh/logout/me를 한 서비스에서 닫을 수 있는지 확인한다.

## Phase 2

- 시간 표지: Phase 2
- 당시 목표:
  - 로컬 인증 lifecycle을 가장 작은 in-memory 구조로 먼저 동작시킨다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/auth/application/AuthDemoService.java`
  - `spring/src/main/java/com/webpong/study2/app/auth/api/AuthController.java`
- 처음 가설:
  - refresh rotation은 토큰만 새로 발급하는 문제가 아니라, 이전 refresh token을 즉시 폐기하는 상태 전이로 보여 줘야 한다.
- 실제 조치:
  - `ConcurrentHashMap` 두 개로 사용자와 세션을 분리했다.
  - `login()`은 access/refresh/CSRF를 함께 만든다.
  - `refresh()`는 기존 refresh token을 제거한 뒤 새 세션 스냅샷을 저장한다.
  - `logout()`은 refresh token + CSRF 조합이 맞을 때만 세션을 제거한다.
- CLI:

```bash
make test
```

- 검증 신호:
  - `2026-03-13` macOS + VSCode 터미널에서 `make test`를 다시 실행했을 때 `BUILD SUCCESSFUL`이 나왔다.
- 핵심 코드 앵커:

```java
public SessionSnapshot refresh(String refreshToken, String csrfToken) {
  SessionSnapshot existing = requireSession(refreshToken, csrfToken);
  sessions.remove(refreshToken);
  SessionSnapshot rotated =
      new SessionSnapshot(
          existing.userId(),
          existing.email(),
          "access-" + UUID.randomUUID(),
          "refresh-" + UUID.randomUUID(),
          "csrf-" + UUID.randomUUID());
  sessions.put(rotated.refreshToken(), rotated);
  return rotated;
}
```

- 새로 배운 것:
  - refresh rotation의 핵심은 "새 토큰 발급"이 아니라 "이전 토큰을 더 이상 세션 식별자로 인정하지 않는 것"이다.
- 다음:
  - 이 상태 전이를 API와 테스트에서 어떻게 드러낼지 고정한다.

## Phase 3

- 시간 표지: Phase 3
- 당시 목표:
  - API 레벨에서 register/login/refresh/me가 실제로 이어지고, CSRF mismatch가 예외 envelope로 보이는지 증명한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/AuthFlowApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - 브라우저가 없어도 MockMvc만으로 refresh token과 CSRF의 결합 조건을 충분히 설명할 수 있다.
- 실제 조치:
  - 회원가입 -> 로그인 -> refresh -> `me` 순서를 한 테스트에 묶었다.
  - 잘못된 `X-CSRF-TOKEN` 헤더를 넣었을 때 `bad_request` envelope가 나오는지 별도 테스트로 고정했다.
- CLI:

```bash
make test
make smoke
docker compose up --build
```

- 검증 신호:
  - `2026-03-13` 재실행 후 `build/test-results/test` 아래 XML 리포트 4개가 생성됐고 `failures=0`이었다.
  - 루트 검증 기록에는 `2026-03-09` 기준 `make lint`, `make test`, `make smoke`, Compose health 확인 통과가 남아 있다.
- 핵심 코드 앵커:

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

- 새로 배운 것:
  - cookie를 아직 붙이지 않았더라도, "refresh token + CSRF가 함께 맞아야 갱신된다"는 경계는 테스트 한 줄로 강하게 보여 줄 수 있다.
- 다음:
  - 사용자/토큰 persistence, verify/reset endpoint, 실제 cookie 기반 동작 검증을 다음 단계로 넘긴다.
