# state, nonce, TOTP, audit를 먼저 묶어 둔 이유

`B-federation-security-lab`은 로그인 성공 이후를 다루는 랩이지만, 여기서도 출발점은 기술 키워드가 아니라 경계다. 실제 Google Console이나 authenticator 앱을 붙이기 전에, 어떤 값이 authorize 단계에서 생기고 callback에서 어떤 연결이 일어나며, 2FA setup과 audit가 어떤 흔적을 남기는지부터 닫아야 했다. macOS + VSCode 통합 터미널에서 `make test`를 돌려 보는 흐름으로 따라가면 이 랩의 설계 의도가 더 잘 보인다.

## 구현 순서 요약

- `problem/README.md`와 `docs/README.md`가 federation, 2FA, audit를 같은 랩으로 묶는다.
- `FederationSecurityDemoService`가 authorize URL, callback linking, TOTP setup/verify, audit event를 한 서비스 안에서 닫는다.
- `FederationSecurityController`가 `/api/v1/auth/google/*`, `/api/v1/auth/2fa/*`, `/api/v1/audit-events` surface를 만든다.
- `FederationSecurityApiTest`가 강화 흐름의 성공 경로를 검증한다.

## Phase 1

### Session 1

- 당시 목표:
  - 로컬 인증 이후에 무엇을 보강할지 문서 수준에서 먼저 자른다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - provider integration 하나만 강조하면 실제로 중요한 state, callback, recovery, audit 경계가 보이지 않는다.
- 실제 진행:
  - canonical scope를 authorize/callback, TOTP setup/verify, audit event로 고정했다.
  - 실제 Google Console 연동과 production-grade secret 관리는 다음 단계로 명시했다.

CLI:

```bash
cp .env.example .env
make run
```

검증 신호:

- `spring/README.md`가 VSCode 터미널 기준 재현 명령을 고정했고, docs는 contract modeling 단계라는 현재 위치를 분명히 적는다.

핵심 코드:

```java
@RequestMapping("/api/v1")
public class FederationSecurityController {
```

왜 이 코드가 중요했는가:

- 이 랩의 surface는 `/auth/google/*`, `/auth/2fa/*`, `/audit-events` 셋으로 닫힌다. 어떤 강화 기능을 이번 랩에서 함께 본다는 선언이 경로 구조에 남아 있다.

새로 배운 것:

- 인증 강화는 기능 추가가 아니라 "새로운 신뢰 근거를 어디서 만들고 어디에 남길지"를 정하는 일이다.

다음:

- authorize와 callback, TOTP와 audit를 한 서비스에 먼저 올린다.

## Phase 2

### Session 1

- 당시 목표:
  - 실제 provider 연결 없이도 federation과 2FA의 shape를 코드로 먼저 보여 준다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/federation/application/FederationSecurityDemoService.java`
  - `spring/src/main/java/com/webpong/study2/app/federation/api/FederationSecurityController.java`
- 처음 가설:
  - state/nonce, provider subject linking, recovery code, audit event만 있어도 인증 강화의 대부분을 설명할 수 있다.
- 실제 진행:
  - `authorize()`는 state와 nonce를 만들고 authorize URL을 조립한다.
  - `callback()`은 email과 provider subject를 연결한다.
  - `setupTotp()`는 secret, recovery code, expected code를 반환하고 audit에 남긴다.
  - `verifyTotp()`는 email 기준 expected code와 비교해 verification 결과를 만든다.

CLI:

```bash
make test
```

검증 신호:

- `2026-03-13` macOS + VSCode 통합 터미널 재실행에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.

핵심 코드:

```java
public TotpSetup setupTotp(String email) {
  String secret = UUID.randomUUID().toString().replace("-", "").substring(0, 12).toUpperCase();
  String expectedCode = secret.substring(0, 6);
  totpSecrets.put(email, expectedCode);
  auditEvents.add(new AuditEvent("totp_setup", email));
  return new TotpSetup(secret, List.of("rec-1", "rec-2", "rec-3"), expectedCode);
}
```

왜 이 코드가 중요했는가:

- 2FA를 "코드 검증" 하나로 줄이지 않고, setup secret과 recovery code를 함께 만든다는 점이 이 랩의 설계 의도를 가장 잘 보여 준다.

새로 배운 것:

- setup 단계가 약하면 verify 단계는 설명할 게 거의 남지 않는다. 강화 기능은 언제나 준비 단계가 더 중요하다.

다음:

- callback, TOTP, audit가 테스트에서 실제로 이어지는지 확인한다.

## Phase 3

### Session 1

- 당시 목표:
  - 강화 표면이 실제 API 호출 순서에서 자연스럽게 이어지는지 증명한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/FederationSecurityApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - authorize -> callback -> audit 확인, setup -> verify 흐름을 각각 고정하면 전체 인증 강화 시나리오가 충분히 복원된다.
- 실제 진행:
  - authorize URL이 google authorize 형태를 포함하는지 확인했다.
  - callback 이후 `/api/v1/audit-events`에 실제 기록이 남는지 검증했다.
  - TOTP setup 응답에서 `expectedCode`를 꺼내 verify 호출에 다시 넣었다.

CLI:

```bash
make test
make smoke
docker compose up --build
```

검증 신호:

- `2026-03-13` 재실행 뒤 XML 리포트 4개가 생성됐고 `failures=0`이었다.
- `2026-03-09` 검증 기록에는 lint/test/smoke/Compose health 확인 통과가 남아 있다.

핵심 코드:

```java
mockMvc
    .perform(get("/api/v1/audit-events"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$[0].type").exists());
```

왜 이 코드가 중요했는가:

- 인증 강화 기능은 성공 여부만으로 끝나지 않는다. 어떤 흔적이 남았는지가 있어야 운영과 추적을 이야기할 수 있다.

새로 배운 것:

- audit는 부가 기능이 아니라 강화 기능의 일부다. state, callback, TOTP가 모두 나중에 설명 가능한 흔적로 남아야 한다.

다음:

- 실제 provider config, secret persistence, rate limit enforcement는 다음 단계에서 구현한다.
