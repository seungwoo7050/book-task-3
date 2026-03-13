# C-authorization-lab: 인가를 membership lifecycle로 먼저 고정한 과정

`C-authorization-lab`의 역할은 분명하다. 인증 문제와 인가 문제를 일부러 떼어 내고, "누가 무엇을 할 수 있는가"를 membership lifecycle로 다시 설명하는 것이다. 그래서 이 랩의 핵심은 화려한 policy engine보다 규칙의 위치를 먼저 드러내는 데 있었다.

실제 구현도 그 방향을 따른다. `problem/README.md`에서 authorization을 조직 생성, 초대, 수락, role 변경 문제로 자르고, `AuthorizationApiTest`로 그 흐름을 먼저 고정했다. 이후 `AuthorizationDemoService`에서 owner, pending, accepted membership 전이를 in-memory state로 명시하고, 마지막에 docs와 검증 기록으로 왜 method security를 아직 미뤘는지 정리했다.

## Phase 1. 인가 문제를 먼저 API 시나리오로 고정했다

authorization을 다룬다고 하면 곧바로 `@PreAuthorize`나 외부 policy engine을 떠올리기 쉽다. 하지만 이 랩은 그보다 앞선 질문을 택했다. 초대, 수락, role 변경이라는 membership lifecycle이 먼저 보여야 인가 규칙도 설명 가능해진다는 쪽이었다.

그 판단은 [`AuthorizationApiTest`](../spring/src/test/java/com/webpong/study2/app/AuthorizationApiTest.java)에서 가장 또렷하다.

```java
MvcResult inviteResult =
    mockMvc.perform(
            post("/api/v1/organizations/{organizationId}/invites", organizationId)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"staff@example.com\",\"role\":\"STAFF\"}"))
        .andExpect(status().isOk())
        .andReturn();

mockMvc.perform(post("/api/v1/invitations/{invitationId}/accept", inviteJson.get("id").asLong()))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.role").value("STAFF"));
```

왜 이 코드가 중요했는가. 인가를 추상적인 권한 체크가 아니라, 초대 발급과 수락, role 변경이라는 눈에 보이는 상태 전이로 바꾸기 때문이다. 누가 어떤 조직 안에서 어떤 상태에 있는지 이 테스트가 먼저 보여 준다.

CLI도 그래서 단순하다.

```bash
cd spring
make test
```

`2026-03-13` 테스트 XML 기준으로 `AuthorizationApiTest` 1개 테스트와 `HealthApiTest` 2개 테스트가 모두 통과했다. 숫자는 작지만, 이 랩이 노린 핵심 흐름은 이미 고정된 셈이다.

여기서 새로 보인 개념은 authorization의 최소 단위였다. role 이름 목록보다 membership lifecycle이 더 먼저 설명돼야 했다.

## Phase 2. owner, pending, accepted membership을 서비스 코드에 박아 넣었다

테스트가 먼저 고정되고 나면 membership 상태를 어디에 둘지 결정해야 한다. 이 랩은 persistence보다 service logic을 먼저 택했다. [`AuthorizationDemoService`](../spring/src/main/java/com/webpong/study2/app/authorization/application/AuthorizationDemoService.java)는 조직 생성 시 owner를 넣고, invite 시 `PENDING`, accept 시 실제 role로 바꾸는 흐름을 코드에 직접 남긴다.

```java
public Invitation invite(long organizationId, String email, String role) {
  Organization organization = requireOrganization(organizationId);
  ...
  invitations.put(invitationId, invitation);
  organization.members().putIfAbsent(email, "PENDING");
  return invitation;
}

public Membership accept(long invitationId) {
  Invitation invitation = requireInvitation(invitationId);
  ...
  organization.members().put(invitation.email(), invitation.role());
  return new Membership(invitation.organizationId(), invitation.email(), invitation.role());
}
```

왜 이 코드가 중요했는가. 인가 규칙이 처음으로 owner, pending, accepted라는 상태 전이로 읽히기 때문이다. DB가 없어도 이 흐름이 명확하면, 이후 method security나 persistence를 붙일 기준이 생긴다.

이 단계의 CLI는 smoke와 Compose까지 이어진다.

```bash
cd spring
make smoke
docker compose up --build
```

`docs/verification-report.md`는 `2026-03-09`에 lint, test, smoke, Compose health 확인이 통과했다고 남긴다. `LabInfoApiSmokeTest` XML도 1개 테스트가 실패 없이 끝났음을 보여 준다.

여기서 배운 건 state transition의 가치였다. 인가에서는 storage 기술보다 owner에서 member로, pending에서 accepted로 바뀌는 흐름이 먼저 보여야 설명이 붙는다.

## Phase 3. method security를 미루는 대신 규칙을 더 선명하게 남겼다

이 랩은 의도적으로 `@PreAuthorize` 중심 구조를 아직 도입하지 않는다. [`docs/README.md`](../docs/README.md)는 authorization rule을 service logic에 두고 membership state도 인메모리로 유지한다고 적는다. 지금 단계에서는 enforcement 기술보다 규칙 자체를 선명하게 읽히게 하는 쪽이 더 중요했기 때문이다.

```bash
cd spring
make lint
make test
make smoke
```

검증 신호는 아래처럼 정리된다.

- `2026-03-13` 기준 테스트 XML 4개 suite, 총 5개 테스트, 실패 0
- `2026-03-09` 검증 보고서 기준 lint, test, smoke, Compose health 확인 통과
- docs에 method security 미적용, persistence 미구현이 명시돼 있음

이 숫자와 문서를 같이 보면, 이 랩은 고급 authorization engine의 완성본이 아니라 "인가를 membership lifecycle로 먼저 설명하는 baseline"이다. 그래서 다음 단계로 넘어갈 때도 문제가 섞이지 않는다. 이제 남는 질문은 이 상태를 실제 persistence 선택과 함께 어떻게 설명할 것인가인데, 그 답이 `D-data-jpa-lab`에서 시작된다.
