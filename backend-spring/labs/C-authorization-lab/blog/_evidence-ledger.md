# C-authorization-lab evidence ledger

- 작성 기준일: 2026-03-14
- 복원 원칙: 기존 blog 본문은 입력 근거로 쓰지 않고, problem statement, source, test, 재실행 결과만 사용했다.
- 핵심 근거: `problem/README.md`, `docs/README.md`, `spring/Makefile`, `AuthorizationController.java`, `AuthorizationDemoService.java`, `SecurityConfig.java`, `GlobalExceptionHandler.java`, `TraceIdFilter.java`, `AuthorizationApiTest.java`, `HealthApiTest.java`, `LabInfoApiSmokeTest.java`

## Phase 1. membership lifecycle surface 확인

- 목표: authorization 랩이 어떤 리소스와 액션을 public surface로 드러내는지 먼저 확인한다.
- 확인 파일:
  - `spring/src/main/java/com/webpong/study2/app/authorization/api/AuthorizationController.java`
  - `spring/src/test/java/com/webpong/study2/app/AuthorizationApiTest.java`
- 확인 결과:
  - endpoint는 `POST /organizations`, `POST /organizations/{id}/invites`, `POST /invitations/{id}/accept`, `PATCH /organizations/{id}/members/{email}/role` 네 개다.
  - 테스트는 invite -> accept -> role change happy path 하나를 고정한다.
- 핵심 앵커:

```java
public record OrganizationRequest(@NotBlank String name, @Email String ownerEmail) {}
public record InviteRequest(@Email String email, @NotBlank String role) {}
public record RoleRequest(@NotBlank String role) {}
```

- 메모:
  - validation annotation은 선언돼 있지만 `@RequestBody`에 `@Valid`가 없어 enforcement로 이어지지 않는다.
  - controller method 어디에도 caller identity가 없다.

## Phase 2. service state transition 확인

- 목표: owner, pending, accepted membership 전이가 실제로 어디서 일어나는지 확인한다.
- 확인 파일:
  - `spring/src/main/java/com/webpong/study2/app/authorization/application/AuthorizationDemoService.java`
- 확인 결과:
  - `createOrganization()`은 owner email을 바로 `OWNER`로 저장한다.
  - `invite()`는 `UUID` token을 만들고 `members().putIfAbsent(email, "PENDING")`를 수행한다.
  - `accept()`는 accepted flag를 true로 바꾸고 membership role을 invitation role로 덮어쓴다.
  - `changeRole()`은 member 존재만 검사하고 caller authorization은 보지 않는다.
- 핵심 앵커:

```java
organization.members().put(ownerEmail, "OWNER");
organization.members().putIfAbsent(email, "PENDING");
organization.members().put(invitation.email(), invitation.role());
```

- 메모:
  - repeated accept를 막는 guard가 없다.
  - `organizations`와 `invitations`는 `ConcurrentHashMap`이지만 audit trail이나 durable persistence는 없다.

## Phase 3. security와 error boundary 확인

- 목표: authorization enforcement가 실제로 어느 층에서 빠져 있는지 확인한다.
- 확인 파일:
  - `spring/src/main/java/com/webpong/study2/app/global/security/SecurityConfig.java`
  - `spring/src/main/java/com/webpong/study2/app/global/error/GlobalExceptionHandler.java`
  - `spring/src/main/java/com/webpong/study2/app/global/logging/TraceIdFilter.java`
- 확인 결과:
  - `/api/v1/**` 전체가 `permitAll()`이다.
  - `IllegalArgumentException`은 problem detail `400`으로 바뀐다.
  - `MethodArgumentNotValidException` handler는 있지만, 현재 controller wiring으로는 거의 트리거되지 않는다.
  - 모든 응답에 `X-Trace-Id`가 주입된다.

## Phase 4. 2026-03-14 재실행 검증

- lint:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
```

- 결과: `BUILD SUCCESSFUL in 1m 40s`

- test:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'
```

- 결과: `BUILD SUCCESSFUL in 1m 25s`

- smoke:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

- 결과: `BUILD SUCCESSFUL in 1m 22s`

- manual boot run:

```bash
docker run --rm -u $(id -u):$(id -g) -p 18082:8080 \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew bootRun'
```

- manual HTTP checks:
  - `GET /api/v1/health/live` -> `200`, `X-Trace-Id` 헤더 확인
  - `GET /api/v1/lab/info` -> `200`, `track=study2`
  - valid organization/invite/accept/changeRole flow -> 모두 `200`
  - invalid organization body `{"name":"","ownerEmail":"not-an-email"}` -> `200`, invalid owner accepted
  - blank role change body `{"role":""}` -> `200`, blank role accepted
  - missing member role change -> `400`, `code=bad_request`, `detail="Member not found"`
  - repeated invitation accept -> 다시 `200`

## 이번 Todo의 결론

- 이 lab은 authorization을 enforcement로 완성한 단계가 아니라 membership lifecycle을 먼저 설명하는 scaffold다.
- 문서에서 반드시 남겨야 할 현재 한계:
  - public `/api/v1/**`
  - caller identity 없음
  - owner/role authorization check 없음
  - validation 미적용
  - repeated accept 허용
