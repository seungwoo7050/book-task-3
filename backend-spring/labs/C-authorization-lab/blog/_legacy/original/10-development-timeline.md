# membership lifecycle을 먼저 드러내야 인가가 읽힌다

`C-authorization-lab`은 인가를 거창한 framework 기능이 아니라 membership lifecycle로 환원해서 보여 주는 랩이다. owner가 organization을 만들고, invite를 발급하고, invite를 수락한 뒤 role을 바꾸는 흐름이 코드에 명시되면, 그 다음에야 `@PreAuthorize` 같은 annotation을 어디에 얹을지 말할 수 있다. macOS + VSCode 통합 터미널 기준으로 `make test`를 다시 돌려 보면 이 랩이 왜 service logic 중심 baseline인지 더 분명해진다.

## 구현 순서 요약

- `problem/README.md`와 `docs/README.md`가 authorization을 auth와 분리된 문제로 먼저 고정한다.
- `AuthorizationDemoService`가 organization, invitation, membership 상태를 in-memory로 관리한다.
- `AuthorizationController`가 organization 생성, invite, accept, role change endpoint를 드러낸다.
- `AuthorizationApiTest`가 membership lifecycle 전체를 한 흐름으로 검증한다.

## Phase 1

### Session 1

- 당시 목표:
  - auth와 authorization의 경계를 먼저 분리한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - 로그인 성공 여부와 리소스 접근 권한을 같은 랩에서 동시에 설명하면 membership 규칙이 흐려진다.
- 실제 진행:
  - organization 생성, invite 발급/수락, role 변경을 이 랩의 success criteria로 고정했다.
  - persistence, method security, external policy engine은 다음 단계로 미뤘다.

CLI:

```bash
cp .env.example .env
make run
```

검증 신호:

- `spring/README.md`는 VSCode 통합 터미널 기준 명령을 고정했고, docs는 service logic 중심 baseline이라는 현재 위치를 분명히 남긴다.

핵심 코드:

```java
@RequestMapping("/api/v1")
public class AuthorizationController {
```

왜 이 코드가 중요했는가:

- 이 랩은 auth controller 아래에 숨어 있지 않고 `/organizations`, `/invitations`라는 authorization 전용 surface를 가진다. 경계를 분리했다는 말이 경로 구조에 그대로 남는다.

새로 배운 것:

- authorization을 설명하려면 "권한 판단이 일어나는 자리"보다 먼저 "멤버십이 어떻게 생기고 바뀌는가"를 보여 줘야 한다.

다음:

- membership lifecycle을 서비스 로직으로 먼저 구현한다.

## Phase 2

### Session 1

- 당시 목표:
  - invite, accept, role change를 서비스 로직에서 명시적으로 보이게 한다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/authorization/application/AuthorizationDemoService.java`
  - `spring/src/main/java/com/webpong/study2/app/authorization/api/AuthorizationController.java`
- 처음 가설:
  - 조직 생성 시 owner를 먼저 심고, invite는 `PENDING`, accept는 실제 role 승격으로 다루면 authorization lifecycle이 가장 읽기 쉽다.
- 실제 진행:
  - organization 생성 시 owner를 즉시 `OWNER`로 넣었다.
  - invite는 UUID token과 함께 `PENDING` 상태를 만든다.
  - accept는 invitation accepted 플래그를 바꾸고 membership을 실제 role로 올린다.
  - changeRole은 member 존재 여부를 먼저 검증한 뒤 role을 바꾼다.

CLI:

```bash
make test
```

검증 신호:

- `2026-03-13` macOS + VSCode 통합 터미널에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.

핵심 코드:

```java
public Invitation invite(long organizationId, String email, String role) {
  Organization organization = requireOrganization(organizationId);
  long invitationId = invitationSequence.getAndIncrement();
  Invitation invitation =
      new Invitation(
          invitationId, organizationId, email, role, UUID.randomUUID().toString(), false);
  invitations.put(invitationId, invitation);
  organization.members().putIfAbsent(email, "PENDING");
  return invitation;
}
```

왜 이 코드가 중요했는가:

- 이 랩에서 invite는 단순 이메일 알림이 아니라 membership table에 `PENDING`이라는 중간 상태를 만드는 사건이다. 인가 규칙이 "최종 role만 있는 세계"가 아니라는 점이 여기서 드러난다.

새로 배운 것:

- 인가 모델에서는 중간 상태를 숨기면 설명력이 급격히 떨어진다. `PENDING` 같은 임시 상태가 실제 운영 규칙을 더 잘 보여 준다.

다음:

- 이 상태 전이가 MockMvc 호출 순서에서 자연스럽게 이어지는지 확인한다.

## Phase 3

### Session 1

- 당시 목표:
  - membership lifecycle이 실제 API 순서에서 끊기지 않는지 증명한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/AuthorizationApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - organization 생성 -> invite -> accept -> role 변경을 한 테스트 흐름으로 묶으면 authorization baseline을 충분히 복원할 수 있다.
- 실제 진행:
  - organization 생성 응답에서 `id`를 읽고 invite API에 연결했다.
  - invitation `id`를 다시 accept API에 넣어 membership 승격을 검증했다.
  - 마지막에는 role change API로 `STAFF -> MANAGER` 전이를 고정했다.

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
    .perform(post("/api/v1/invitations/{invitationId}/accept", inviteJson.get("id").asLong()))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.role").value("STAFF"));
```

왜 이 코드가 중요했는가:

- invite와 role change 사이에 accept 단계를 따로 두었기 때문에, authorization이 "role 문자열 수정"이 아니라 membership lifecycle이라는 점이 분명해진다.

새로 배운 것:

- 인가를 설명할 때는 거절 규칙만큼이나 승격 규칙이 중요하다. 누가 어떤 절차를 거쳐 member가 되는지가 권한 체계의 절반이다.

다음:

- method security, persistence, denial-path 테스트는 다음 단계에서 보강한다.
