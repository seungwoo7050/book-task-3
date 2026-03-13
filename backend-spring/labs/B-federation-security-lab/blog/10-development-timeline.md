# B-federation-security-lab: provider 연동보다 인증 강화 경계를 먼저 고정한 과정

`B-federation-security-lab`은 local auth 다음에 붙는 인증 강화 요소를 따로 분리한 랩이다. 핵심은 live provider 연동을 빨리 끝내는 데 있지 않고, federation, 2FA, audit가 어떤 경계로 묶이는지 먼저 설명 가능하게 만드는 데 있었다.

구현 순서는 뚜렷하다. `problem/README.md`에서 federation, TOTP, audit를 하나의 문제로 묶고, `FederationSecurityApiTest`로 authorize/callback와 2FA 표면을 먼저 고정했다. 그다음 `FederationSecurityDemoService`에서 state, expected code, audit event를 남기는 흐름을 만들고, 마지막에 문서와 검증 기록으로 아직 production-grade가 아닌 부분을 분명히 닫았다.

## Phase 1. live provider보다 callback contract를 먼저 테스트로 고정했다

보안 랩을 만들다 보면 외부 provider를 실제로 붙여야만 진도가 나간 것처럼 느껴진다. 그런데 이 랩의 출발점은 달랐다. local login 이후에 어떤 경계와 실패 지점이 생기는지 먼저 보여 주는 편이 더 중요했다.

그 판단은 [`FederationSecurityApiTest`](../spring/src/test/java/com/webpong/study2/app/FederationSecurityApiTest.java)에서 바로 드러난다.

```java
mockMvc.perform(get("/api/v1/auth/google/authorize"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.url").value(org.hamcrest.Matchers.containsString("google")));

mockMvc.perform(post("/api/v1/auth/google/callback")
        .contentType(MediaType.APPLICATION_JSON)
        .content("{\"email\":\"oauth@example.com\",\"subject\":\"google-123\"}"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.provider").value("google"));
```

왜 이 코드가 중요했는가. federation의 초점이 실제 Google 로그인 성공이 아니라 callback contract와 state boundary를 먼저 고정하는 데 있다는 점을 이 테스트가 보여 주기 때문이다. provider SDK보다 먼저 contract를 잡아 두어야, 이후 실제 연동이 붙어도 문제 범위가 흐려지지 않는다.

CLI도 그 방향을 그대로 따른다.

```bash
cd spring
make test
```

`2026-03-13` 테스트 XML 기준으로 `FederationSecurityApiTest` 2개 테스트와 `HealthApiTest` 2개 테스트가 모두 실패 없이 끝났다. 이 랩이 callback surface와 health surface를 함께 들고 있다는 뜻이다.

여기서 새로 선명해진 개념은 federation의 첫 기준이었다. 핵심은 provider 설정이 아니라 state, nonce, callback payload를 코드로 설명할 수 있느냐였다.

## Phase 2. TOTP와 audit를 같은 상태 변화로 묶었다

callback contract가 잡히고 나면, 2FA를 별도 부속 기능처럼 두지 않는 선택이 나온다. [`FederationSecurityDemoService`](../spring/src/main/java/com/webpong/study2/app/federation/application/FederationSecurityDemoService.java)는 `authorize()`, `callback()`, `setupTotp()`, `verifyTotp()`를 같은 서비스 안에 두고 모든 단계에 audit event를 남긴다.

```java
public AuthorizationUrl authorize() {
  String state = UUID.randomUUID().toString();
  String nonce = UUID.randomUUID().toString();
  auditEvents.add(new AuditEvent("google_authorize", "generated state=" + state));
  return new AuthorizationUrl(
      "https://accounts.google.com/o/oauth2/v2/auth?state=" + state + "&nonce=" + nonce,
      state,
      nonce);
}

public VerificationResult verifyTotp(String email, String code) {
  boolean verified = code.equals(totpSecrets.get(email));
  auditEvents.add(new AuditEvent("totp_verify", email + ":" + verified));
  return new VerificationResult(verified);
}
```

왜 이 코드가 중요했는가. federation, 2FA, audit가 각각 따로 있는 기능이 아니라 "인증 강화에서 남는 상태 변화"라는 점을 여기서 처음 설명할 수 있기 때문이다. 흔적이 남아야 보안 기능도 블랙박스가 아니라 설명 가능한 흐름이 된다.

이 단계의 CLI는 smoke와 Compose까지 올라간다.

```bash
cd spring
make smoke
docker compose up --build
```

`docs/verification-report.md`는 `2026-03-09`에 lint, test, smoke, Compose health 확인이 모두 통과했다고 적고 있다. `LabInfoApiSmokeTest` XML도 1개 테스트가 실패 없이 끝났음을 보여 준다.

여기서 배운 건 audit의 역할이었다. audit는 부가 로그가 아니라, 인증 강화 기능이 남기는 상태 변화를 바깥에서 다시 읽게 해 주는 최소 기록이었다.

## Phase 3. hardening의 끝이 아니라 hardening의 경계를 문서로 닫았다

보안 랩은 특히 과장되기 쉽다. 외부 provider도 없고 hard rate limiting도 없는데 기능 이름만 보면 다 끝난 것처럼 보일 수 있다. 이 랩은 그 지점을 숨기지 않았다. [`docs/README.md`](../docs/README.md)는 Google integration이 contract modeling 수준이고, TOTP도 단순화 버전이며, Redis-backed hard rate limiting은 아직 다음 단계라고 분명히 적는다.

```bash
cd spring
make lint
make test
make smoke
```

검증 신호는 아래처럼 정리된다.

- `2026-03-13` 기준 테스트 XML 4개 suite, 총 6개 테스트, 실패 0
- `2026-03-09` 검증 보고서 기준 lint, test, smoke, Compose health 확인 통과
- docs에 실제 provider, hard rate limiting 미구현이 명시돼 있음

이 숫자와 문서가 같이 말해 주는 건, 이 랩이 production-ready identity platform이라는 뜻이 아니다. 대신 local auth 다음에 어떤 보안 경계가 붙고, 왜 callback contract와 audit가 먼저여야 하는지를 다시 설명할 수 있다는 뜻이다.

다음으로 넘어갈 질문도 자연스럽다. 인증이 끝난 다음, 누가 무엇을 할 수 있는가는 어디에서 판단할 것인가. 그 문제를 `C-authorization-lab`이 맡는다.
