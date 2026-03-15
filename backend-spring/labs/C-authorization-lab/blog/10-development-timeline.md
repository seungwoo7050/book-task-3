# C-authorization-lab: membership lifecycle은 만들었지만 enforcement는 아직 시작 전인 authorization scaffold

`C-authorization-lab`을 다시 읽으면서 먼저 바로잡아야 했던 건 이 랩의 성격이었다. 이름만 보면 authorization이 어느 정도 완성된 실습처럼 보이지만, 실제 소스는 "조직 멤버십 흐름을 어떻게 모델링할 것인가"를 먼저 보여 주는 단계에 가깝다. `problem/README.md`도 success criteria를 organization 생성, invite 발급/수락, role 변경 흐름에 두고 있고, 이번 단계에서 다루지 않는 것으로 method security와 외부 policy engine을 분명히 제외한다.

2026-03-14에는 기존 blog를 입력 근거에서 제외하고, `AuthorizationController`, `AuthorizationDemoService`, `SecurityConfig`, `AuthorizationApiTest`, 실제 `bootRun`과 `curl` 재검증만으로 문서를 다시 썼다. 읽고 나니 이 랩의 핵심 질문은 "인가를 어떻게 막을 것인가"보다 "인가 문제를 어떤 상태 전이로 설명할 것인가"에 더 가까웠다.

## Phase 1. authorization을 actor check가 아니라 membership lifecycle로 먼저 고정했다

가장 먼저 잡히는 단서는 [`AuthorizationController`](../spring/src/main/java/com/webpong/study2/app/authorization/api/AuthorizationController.java)다. public API는 네 개뿐이다. organization 생성, invite 발급, invitation accept, role 변경. 이 구성이 곧 이 랩이 authorization을 다루는 방식이다.

```java
@PostMapping("/organizations")
public AuthorizationDemoService.Organization createOrganization(
    @RequestBody OrganizationRequest request) {
  return service.createOrganization(request.name(), request.ownerEmail());
}

@PostMapping("/organizations/{organizationId}/invites")
public AuthorizationDemoService.Invitation invite(
    @PathVariable long organizationId, @RequestBody InviteRequest request) {
  return service.invite(organizationId, request.email(), request.role());
}
```

여기서 먼저 보이는 건 "누가 호출했는가"가 아니라 "멤버십 상태가 어떻게 생기고 바뀌는가"다. 실제 테스트도 같은 우선순위를 가진다. [`AuthorizationApiTest`](../spring/src/test/java/com/webpong/study2/app/AuthorizationApiTest.java)는 happy path 하나만 고정한다. organization을 만들고, invite를 만들고, accept하고, 마지막에 role을 바꾸면 `MANAGER`가 되는지 본다.

```java
mockMvc
    .perform(post("/api/v1/invitations/{invitationId}/accept", inviteJson.get("id").asLong()))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.role").value("STAFF"));
```

즉 이 랩의 첫 번째 산출물은 authorization enforcement가 아니라 lifecycle sketch다. "role이 있다"보다 "owner가 생기고, invite가 pending을 만들고, accept가 final role을 꽂는다"가 먼저 보이도록 API를 자른 셈이다.

## Phase 2. service는 transition을 만들지만 caller identity나 ownership enforcement는 아직 없다

실제 규칙은 [`AuthorizationDemoService`](../spring/src/main/java/com/webpong/study2/app/authorization/application/AuthorizationDemoService.java)에 있다. `createOrganization()`은 owner email을 곧바로 `OWNER`로 넣고, `invite()`는 `putIfAbsent(email, "PENDING")`으로 멤버십 슬롯을 만든 뒤 invitation token을 저장한다. `accept()`는 accepted flag를 true로 바꾸고, 멤버십 role을 `STAFF` 같은 실제 권한값으로 덮어쓴다.

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

이 구조 덕분에 membership lifecycle 자체는 읽기 쉽다. 다만 enforcement 관점으로 넘어가면 비어 있는 곳이 바로 드러난다.

- controller는 어떤 endpoint에서도 `Principal`, `Authentication`, caller email, actor role을 받지 않는다.
- service도 organization owner가 실제로 role 변경을 수행했는지 검사하지 않는다.
- `changeRole()`은 member 존재 여부만 보고 곧바로 새 role을 써 버린다.
- `accept()`는 invitation이 이미 accepted인지 확인하지 않아서 같은 invitation을 다시 호출해도 또 `200`을 돌려준다.

2026-03-14 수동 재검증에서도 이 한계는 그대로 확인됐다.

```bash
curl -sS -X POST http://127.0.0.1:18082/api/v1/organizations \
  -H 'Content-Type: application/json' \
  -d '{"name":"Store Ops","ownerEmail":"owner@example.com"}'

curl -sS -X POST http://127.0.0.1:18082/api/v1/organizations/1/invites \
  -H 'Content-Type: application/json' \
  -d '{"email":"staff@example.com","role":"STAFF"}'

curl -sS -X POST http://127.0.0.1:18082/api/v1/invitations/1/accept'
curl -sS -X PATCH http://127.0.0.1:18082/api/v1/organizations/1/members/staff@example.com/role \
  -H 'Content-Type: application/json' \
  -d '{"role":"MANAGER"}'
```

응답은 각각 정상적으로 `OWNER -> PENDING -> STAFF -> MANAGER` 흐름을 보여 줬다. 하지만 이어서 같은 invitation을 한 번 더 accept해도 `200 {"organizationId":1,"email":"staff@example.com","role":"STAFF"}`가 그대로 반환됐다. authorization lifecycle은 설명되지만, one-time token 소비 같은 운영 규칙은 아직 없다.

## Phase 3. 보안 설정과 validation을 같이 보면 이 랩은 "인가 모델 설명용 scaffold"라는 게 더 분명해진다

이 랩을 그냥 성공 사례로만 적으면 놓치게 되는 핵심은 보안 설정과 validation 처리다. [`SecurityConfig`](../spring/src/main/java/com/webpong/study2/app/global/security/SecurityConfig.java)는 이전 lab들과 마찬가지로 `/api/v1/**` 전체를 `permitAll()` 한다. 즉 organization 생성, invite, accept, role 변경 모두 인증 없이 호출된다.

```java
http.csrf(csrf -> csrf.disable())
    .authorizeHttpRequests(
        auth ->
            auth.requestMatchers("/api/v1/**", "/v3/api-docs/**", "/swagger-ui/**")
                .permitAll()
                .anyRequest()
                .permitAll())
    .httpBasic(Customizer.withDefaults());
```

또 하나는 request record에 달아 둔 `@Email`, `@NotBlank`가 현재는 실질적으로 작동하지 않는다는 점이다. record component에 annotation은 있지만, controller의 `@RequestBody`에는 `@Valid`가 없다. 그래서 [`GlobalExceptionHandler`](../spring/src/main/java/com/webpong/study2/app/global/error/GlobalExceptionHandler.java)가 `MethodArgumentNotValidException`을 처리할 준비를 해 둬도, 실제로 그 예외가 발생할 경로가 거의 없다.

이건 2026-03-14 수동 호출에서 그대로 드러났다.

```bash
curl -i -X POST http://127.0.0.1:18082/api/v1/organizations \
  -H 'Content-Type: application/json' \
  -d '{"name":"","ownerEmail":"not-an-email"}'
```

응답은 `400`이 아니라 `200`이었고, body는 아래처럼 비어 있는 organization과 잘못된 email을 owner로 받아들였다.

```json
{"id":2,"name":"","members":{"not-an-email":"OWNER"}}
```

role 변경도 같았다.

```bash
curl -i -X PATCH http://127.0.0.1:18082/api/v1/organizations/1/members/staff@example.com/role \
  -H 'Content-Type: application/json' \
  -d '{"role":""}'
```

역시 `200`이었고 결과 role은 빈 문자열이었다. 반대로 truly invalid한 경로 하나는 member가 없을 때였다. 이때는 `AuthorizationDemoService.changeRole()`이 `IllegalArgumentException("Member not found")`를 던지고, `GlobalExceptionHandler`가 `400` problem detail로 바꿔 준다. 즉 현재 에러 경계는 bean validation보다 service guard에 더 의존한다.

## Phase 4. 이번 재검증은 "통과했다"보다 "무엇이 통과했고 무엇이 아직 비어 있는가"를 같이 남겼다

이번 Todo에서는 기존 blog를 신뢰하지 않고 검증을 다시 돌렸다. 로컬 JRE가 없어서 호스트 `make lint/test/smoke` 대신 `eclipse-temurin:21-jdk` 컨테이너에서 순차 실행했다.

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'

docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'

docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

세 명령 모두 2026-03-14에 `BUILD SUCCESSFUL`이었다. 이후 `bootRun` 컨테이너를 18082 포트로 띄워 health와 lab info, organization lifecycle, invalid body, missing member까지 직접 확인했다. `GET /api/v1/health/live`는 `X-Trace-Id`를 포함한 `200`을 돌려 줬고, 이 부분은 [`TraceIdFilter`](../spring/src/main/java/com/webpong/study2/app/global/logging/TraceIdFilter.java)와 일치했다.

그래서 이 랩의 현재 결론은 꽤 선명하다. `C-authorization-lab`은 authorization 완성본이 아니라, membership lifecycle을 먼저 말로 고정해 두는 scaffold다. owner, invite, accept, role change라는 shape는 잘 보인다. 하지만 enforcement를 기대하고 읽으면 아직 비어 있는 부분도 분명하다. actor identity 없음, method security 없음, request validation 미적용, repeated accept 허용, blank role 허용. 이 경계를 숨기지 않고 적어 두는 편이 다음 단계인 persistence와 더 현실적으로 이어진다.
