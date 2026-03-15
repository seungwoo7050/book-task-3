# C-authorization-lab structure outline

## 글 목표

- 이 랩을 "authorization 완성본"이 아니라 "membership lifecycle 설명용 scaffold"로 다시 정의한다.
- happy path만이 아니라 실제 enforcement 공백까지 같은 비중으로 적는다.
- 2026-03-14 재검증 결과를 문서의 마지막이 아니라 본문 판단 근거로 연결한다.

## 글 순서

1. controller와 problem statement를 보고 membership lifecycle 중심 랩이라는 점을 먼저 확정한다.
2. service에서 owner, pending, accepted, role overwrite가 어떻게 표현되는지 추적한다.
3. security/validation/error handling을 같이 보고 현재 authorization enforcement가 어디까지 비어 있는지 정리한다.
4. lint/test/smoke/manual HTTP 재실행 결과로 지금 상태를 닫는다.

## 반드시 넣을 코드 앵커

- `AuthorizationController.createOrganization()`
- `AuthorizationController.changeRole()`
- `AuthorizationDemoService.invite()`
- `AuthorizationDemoService.accept()`
- `AuthorizationDemoService.changeRole()`
- `SecurityConfig.securityFilterChain()`
- `GlobalExceptionHandler.handleIllegalArgument()`

## 반드시 넣을 검증 신호

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

## 반드시 남길 한계

- `/api/v1/**`가 모두 `permitAll()`인 상태
- validation annotation이 `@Valid` 없이 선언만 되어 있는 상태
- repeated accept와 blank role이 허용되는 상태
- caller identity와 real ownership enforcement가 아직 없는 상태
