# C-authorization-lab Evidence Ledger

- 복원 기준:
  - git 기록만으로는 내부 순서를 세밀하게 나누기 어려워 `problem/README.md`, `docs/README.md`, 서비스/컨트롤러, MockMvc 테스트, `2026-03-13` 재실행 결과를 함께 사용했다.
- 기존 blog 처리:
  - 기존 `blog/`가 없어서 격리 단계는 필요하지 않았다.

## Phase 1

- 시간 표지: Phase 1
- 당시 목표:
  - 인증과 인가를 분리해 authorization 랩의 독립 문제를 먼저 고정한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - membership, invite, role, ownership를 auth 랩과 섞으면 "누구인가"와 "무엇을 할 수 있는가"가 같이 흐려진다.
- 실제 조치:
  - organization 생성, invite 발급/수락, role 변경을 current scope로 선언했다.
  - persistence와 method security는 다음 단계로 남겼다.
- CLI:

```bash
cp .env.example .env
make run
```

- 검증 신호:
  - 실행/검증 명령이 `spring/README.md`에 고정돼 있고, docs는 service logic 중심 baseline이라는 현재 위치를 설명한다.
- 핵심 코드 앵커:
  - 이후 구현은 `AuthorizationDemoService`, `AuthorizationController`, `AuthorizationApiTest`로 압축된다.
- 새로 배운 것:
  - authorization 랩은 프레임워크 annotation보다 membership lifecycle을 먼저 드러내야 읽힌다.
- 다음:
  - invite/accept/changeRole이 한 서비스 안에서 어떻게 이어지는지 구현한다.

## Phase 2

- 시간 표지: Phase 2
- 당시 목표:
  - authorization rule을 외부 엔진 없이도 서비스 로직에서 명시적으로 보이게 한다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/authorization/application/AuthorizationDemoService.java`
  - `spring/src/main/java/com/webpong/study2/app/authorization/api/AuthorizationController.java`
- 처음 가설:
  - membership lifecycle만 명확히 잡아도 role 변경과 ownership 개념의 대부분은 설명 가능하다.
- 실제 조치:
  - `Organization`, `Invitation`, `Membership`를 record로 두고 상태를 `ConcurrentHashMap`에 유지했다.
  - owner를 organization 생성 시점에 바로 넣고, invite는 `PENDING`, accept는 실제 role 승격, changeRole은 member 존재 여부를 먼저 검증하도록 만들었다.
- CLI:

```bash
make test
```

- 검증 신호:
  - `2026-03-13` macOS + VSCode 터미널에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.
- 핵심 코드 앵커:

```java
public Membership accept(long invitationId) {
  Invitation invitation = requireInvitation(invitationId);
  invitations.put(
      invitationId,
      new Invitation(
          invitation.id(),
          invitation.organizationId(),
          invitation.email(),
          invitation.role(),
          invitation.token(),
          true));
  Organization organization = requireOrganization(invitation.organizationId());
  organization.members().put(invitation.email(), invitation.role());
  return new Membership(invitation.organizationId(), invitation.email(), invitation.role());
}
```

- 새로 배운 것:
  - invitation acceptance는 단순 토큰 소비가 아니라 membership 상태를 `PENDING`에서 실제 role로 전환하는 순간이다.
- 다음:
  - invite -> accept -> role change가 API에서 실제로 이어지는지 검증한다.

## Phase 3

- 시간 표지: Phase 3
- 당시 목표:
  - authorization lifecycle을 사용자 행동 순서로 테스트에 고정한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/AuthorizationApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - organization 생성 -> invite -> accept -> role 변경만 고정해도 인가 랩의 중심 규칙을 충분히 설명할 수 있다.
- 실제 조치:
  - organization 생성 응답에서 `id`를 읽고 invite, accept, changeRole 호출로 이어지는 MockMvc 흐름을 만들었다.
- CLI:

```bash
make test
make smoke
docker compose up --build
```

- 검증 신호:
  - `2026-03-13` 재실행 뒤 XML 리포트 4개가 생성됐고 `failures=0`이었다.
  - `2026-03-09` 검증 기록에는 lint/test/smoke/Compose health 확인 통과가 있다.
- 핵심 코드 앵커:

```java
mockMvc
    .perform(
        patch(
                "/api/v1/organizations/{organizationId}/members/{email}/role",
                organizationId,
                "staff@example.com")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"role\":\"MANAGER\"}"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.role").value("MANAGER"));
```

- 새로 배운 것:
  - 인가 규칙은 deny 규칙만큼이나 상태 전이의 이름이 중요하다. `PENDING -> STAFF -> MANAGER` 같은 이동이 보여야 role 시스템이 설명된다.
- 다음:
  - method security, membership persistence, denial-path 강화는 다음 단계로 남긴다.
