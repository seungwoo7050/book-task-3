# A-auth-lab: 로컬 인증을 baseline lifecycle로 먼저 고정한 과정

`A-auth-lab`은 `backend-spring`에서 가장 앞에 놓인 랩이다. 그래서 처음부터 기능을 넓히기보다, 로컬 계정 인증을 어디까지 "기본 인증"으로 볼지 먼저 잘라 내는 일이 더 중요했다.

실제 구현 순서는 단순했다. `problem/README.md`로 baseline auth의 범위를 먼저 고정하고, `AuthFlowApiTest`로 회원가입부터 refresh까지 한 번에 묶은 뒤, `AuthDemoService`에서 refresh rotation과 CSRF mismatch를 서비스 규칙으로 드러냈다. 마지막에는 `make lint`, `make test`, `make smoke`, Compose health 기록으로 지금 증명한 범위를 닫았다.

## Phase 1. 로그인 하나가 아니라 lifecycle 전체를 먼저 테스트로 묶었다

처음엔 로그인과 토큰 발급만 있어도 이 랩을 설명할 수 있을 것 같았다. 그런데 `problem/README.md`가 요구한 범위는 더 넓었다. 회원가입, 로그인, refresh, logout, `me` 흐름을 한 랩에서 설명해야 했고, frontend 없이도 cookie와 CSRF 경계를 말할 수 있어야 했다. 그래서 구현은 서비스보다 테스트 표면을 먼저 고정하는 쪽으로 움직였다.

그 기준이 가장 잘 보이는 곳이 [`AuthFlowApiTest`](../spring/src/test/java/com/webpong/study2/app/AuthFlowApiTest.java)다.

```java
MvcResult loginResult =
    mockMvc.perform(post("/api/v1/auth/login")
        .contentType(MediaType.APPLICATION_JSON)
        .content("{\"email\":\"spring@example.com\",\"password\":\"pw-1234\"}"))
    .andExpect(status().isOk())
    .andReturn();

mockMvc.perform(post("/api/v1/auth/refresh")
        .header("X-CSRF-TOKEN", csrfToken)
        .contentType(MediaType.APPLICATION_JSON)
        .content("{\"refreshToken\":\"" + refreshToken + "\"}"))
    .andExpect(status().isOk());
```

왜 이 코드가 중요했는가. 이 테스트가 "토큰을 발급했다"가 아니라 "인증 lifecycle 전체를 따라갈 수 있다"는 기준선을 먼저 세우기 때문이다. persistence를 깊게 넣지 않아도 무엇이 이미 설명 가능하고 무엇이 아직 비어 있는지 여기서 바로 드러난다.

CLI도 이 단계에서는 짧았다.

```bash
cd spring
make test
```

검증 신호는 분명하다. `2026-03-13` 테스트 XML 기준으로 `AuthFlowApiTest` 2개 테스트와 `HealthApiTest` 2개 테스트가 모두 실패 없이 끝났다. baseline auth surface와 부팅 health가 함께 살아 있다는 뜻이다.

여기서 처음 또렷해진 개념은 baseline auth의 최소 단위다. storage가 얼마나 깊은지보다, 사용자가 세션을 만들고 갱신하고 자기 상태를 확인하는 흐름을 한 번에 설명할 수 있는지가 먼저였다.

## Phase 2. refresh rotation과 CSRF mismatch를 서비스 규칙으로 고정했다

테스트 표면을 먼저 잡고 나면 다음 질문이 남는다. refresh는 access token만 다시 만드는 편의 기능인가, 아니면 세션 자체를 다시 만드는 경계인가. `AuthDemoService`는 이 질문에 꽤 분명하게 답한다. 기존 refresh token을 제거하고, 새 refresh token과 새 CSRF token을 함께 만든다.

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

그리고 그 앞단에는 CSRF mismatch를 명확하게 끊는 가드가 있다.

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

왜 이 코드가 중요했는가. 여기서 refresh는 액세스 토큰 재발급이 아니라 세션 재생산 규칙이 된다. cookie 기반 인증을 브라우저 없이 설명하려면 CSRF token도 같이 보아야 하는데, 이 랩은 그 경계를 바로 이 함수들에서 닫는다.

이 단계에서 쓰인 CLI는 smoke와 Compose까지 올라간다.

```bash
cd spring
make smoke
docker compose up --build
```

`docs/verification-report.md`는 `2026-03-09` 기준으로 lint, test, smoke, Compose health 확인이 모두 통과했다고 남긴다. smoke XML도 `LabInfoApiSmokeTest` 1개가 실패 없이 통과했음을 보여 준다.

여기서 배운 건 refresh rotation의 위치였다. 이건 부가 기능이 아니라, 인증 상태를 언제 폐기하고 언제 새로 만드는지 설명하는 핵심 규칙이었다.

## Phase 3. persistence를 늦추는 대신 현재 범위를 문서로 분명히 닫았다

마지막 단계는 기능 확장보다 범위 정리에 가까웠다. [`docs/README.md`](../docs/README.md)는 persistence를 일부러 가볍게 두었고, 이메일 검증과 비밀번호 재설정도 full lifecycle이 아니라 shape 설명에 집중한다고 적는다. 이 선택 덕분에 다음 랩으로 넘어갈 자리가 생긴다.

```bash
cd spring
make lint
make test
make smoke
```

검증 신호는 아래처럼 정리된다.

- `2026-03-13` 기준 테스트 XML 4개 suite, 총 6개 테스트, 실패 0
- `2026-03-09` 검증 보고서 기준 lint, test, smoke, Compose health 확인 통과
- `Study2ApplicationTests`까지 별도 실패 없이 종료

이 숫자가 뜻하는 건 production readiness가 아니다. 대신 "로컬 계정 인증의 baseline을 어디까지 설명하는가"를 다시 실행 가능한 형태로 남겼다는 뜻이다. cookie 실동작, persisted refresh token family, 실제 메일 인프라는 아직 남아 있지만, 그 사실을 docs에 같이 적어 두었기 때문에 현재 범위와 다음 단계가 섞이지 않는다.

이제 남는 질문은 자연스럽다. local auth만으로 설명되지 않는 외부 identity 연동과 두 번째 인증 수단을 어디에 둘 것인가. 그 답이 다음 랩인 `B-federation-security-lab`이다.
