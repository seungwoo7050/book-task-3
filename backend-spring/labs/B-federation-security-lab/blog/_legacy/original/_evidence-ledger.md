# B-federation-security-lab Evidence Ledger

- 복원 기준:
  - 세부 세션별 commit이 분리돼 있지 않아 `problem/README.md`, `docs/README.md`, 서비스/컨트롤러, MockMvc 테스트, `2026-03-13` 재실행 CLI를 묶어 chronology를 복원했다.
- 기존 blog 처리:
  - 기존 `blog/`가 없어서 격리할 초안은 없었다.

## Phase 1

- 시간 표지: Phase 1
- 당시 목표:
  - 로컬 인증 다음 단계에서 어떤 보강 요소를 같은 랩으로 묶을지 정한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - federation만 따로 떼면 "인증 강화"의 실제 판단 근거가 약해지고, 2FA와 audit를 같이 봐야 경계가 선명해진다.
- 실제 조치:
  - Google authorize/callback 모양, TOTP setup/verify, audit event surface를 한 랩의 canonical scope로 묶었다.
  - 실제 Google Console 연동과 production-grade TOTP secret 관리는 일부러 뒤로 뺐다.
- CLI:

```bash
cp .env.example .env
make run
```

- 검증 신호:
  - `spring/README.md`가 VSCode 터미널 기준 명령 목록을 고정했고, docs는 contract modeling 단계라는 점을 분명히 남겼다.
- 핵심 코드 앵커:
  - 이후 구현은 `FederationSecurityDemoService`, `FederationSecurityController`, `FederationSecurityApiTest` 세 파일에 집중된다.
- 새로 배운 것:
  - federation 랩의 핵심은 외부 provider 연결 자체보다, provider callback이 들어오기 전에 어떤 상태와 기록을 준비해야 하는지 정리하는 데 있다.
- 다음:
  - authorize URL, callback, TOTP, audit를 한 서비스 안에서 닫는다.

## Phase 2

- 시간 표지: Phase 2
- 당시 목표:
  - 외부 identity 연동과 2FA를 contract-level로 먼저 고정한다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/federation/application/FederationSecurityDemoService.java`
  - `spring/src/main/java/com/webpong/study2/app/federation/api/FederationSecurityController.java`
- 처음 가설:
  - 실제 Google OAuth client를 붙이기 전에도 state, nonce, callback linking, audit는 충분히 설명 가능한 경계다.
- 실제 조치:
  - `authorize()`에서 state와 nonce를 만들고 authorize URL에 넣었다.
  - `callback()`은 email과 provider subject를 연결하고 audit event를 남긴다.
  - `setupTotp()`는 setup secret, recovery code, expected code를 만든다.
  - `verifyTotp()`는 이메일 기준 expected code와 비교한다.
- CLI:

```bash
make test
```

- 검증 신호:
  - `2026-03-13` 재실행에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.
- 핵심 코드 앵커:

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
```

- 새로 배운 것:
  - OAuth authorize 단계에서 가장 먼저 드러나는 값은 access token이 아니라 callback 이후의 신뢰를 묶기 위한 `state`와 `nonce`다.
- 다음:
  - 테스트에서 callback, TOTP, audit까지 한 흐름으로 묶어 본다.

## Phase 3

- 시간 표지: Phase 3
- 당시 목표:
  - federation/2FA/audit가 각각 따로가 아니라 "인증 강화"라는 하나의 흐름으로 읽히게 만든다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/FederationSecurityApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - provider authorize -> callback -> audit 확인, TOTP setup -> verify를 MockMvc 두 테스트로 나눠도 전체 강화 흐름은 충분히 설명된다.
- 실제 조치:
  - authorize endpoint가 실제 google authorize URL 모양을 돌려주는지 검증했다.
  - callback 이후 audit event가 남는지 확인했다.
  - TOTP setup 결과에서 expected code를 꺼내 verify로 연결했다.
- CLI:

```bash
make test
make smoke
docker compose up --build
```

- 검증 신호:
  - `2026-03-13` 재실행 뒤 XML 리포트 4개가 생성됐고 `failures=0`이었다.
  - `2026-03-09` 검증 기록에는 lint/test/smoke/Compose health 통과가 남아 있다.
- 핵심 코드 앵커:

```java
MvcResult setup =
    mockMvc
        .perform(
            post("/api/v1/auth/2fa/setup")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"totp@example.com\"}"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.recoveryCodes[0]").exists())
        .andReturn();
```

- 새로 배운 것:
  - 2FA를 설명할 때 중요한 건 "코드를 맞췄다"보다 setup 단계에서 recovery code를 함께 남기는 것이다. 그래야 운영 중 복구 경로를 이야기할 수 있다.
- 다음:
  - 실제 provider 연동, secret persistence, hard rate limiting은 다음 단계에서 다룬다.
