# A-auth-lab: auth 기능보다 auth 경계를 먼저 잘라 낸 scaffold

`A-auth-lab`은 Spring 트랙의 첫 랩이라서, 처음부터 완성형 auth를 만들기보다 "무엇을 baseline lifecycle로 설명할 것인가"를 먼저 잘라 내는 쪽으로 움직인다. 문제 정의는 refresh rotation, recovery, cookie + CSRF 경계를 말하라고 하지만, 실제 구현은 그걸 production auth로 완성하기보다 demo service와 테스트 표면으로 먼저 모델링한다.

## 1. baseline은 persistence가 아니라 lifecycle로 잡는다

처음 눈에 들어오는 건 `AuthFlowApiTest`다. 이 테스트는 register, login, refresh, `me`를 한 번에 묶어 baseline auth를 정의한다. Spring Security를 깊게 붙이기 전에 "사용자 흐름을 어디까지 설명 가능한가"를 먼저 고정하는 셈이다.

그런데 소스 안쪽으로 들어가면 구현 강도가 훨씬 낮다. `AuthDemoService`는 사용자와 세션을 둘 다 `ConcurrentHashMap`에 넣고, password는 실제 bcrypt hash가 아니라 `"bcrypt$" + password` 문자열로 저장하고 비교한다. build에는 JPA, Redis, Kafka, Mail starter까지 들어가 있지만, auth 핵심은 여전히 in-memory demo service다. 이 차이가 이 랩의 핵심 톤을 결정한다.

## 2. refresh와 CSRF는 Spring Security가 아니라 서비스 규칙이다

`AuthController`는 `/api/v1/auth/refresh`와 `/logout`에서 `X-CSRF-TOKEN` 헤더를 받고, `AuthDemoService.refresh()`는 기존 refresh token을 제거한 뒤 새 access/refresh/csrf token을 다시 만든다. 수동 재실행으로도 이 흐름은 그대로 확인됐다.

```bash
$ POST /api/v1/auth/login
200 {"accessToken":"access-...","refreshToken":"refresh-...","csrfToken":"csrf-..."}

$ POST /api/v1/auth/refresh
200 {"accessToken":"access-...","refreshToken":"refresh-...","csrfToken":"csrf-..."}
```

실제 CSRF mismatch도 서비스 코드에서 막는다.

```bash
$ POST /api/v1/auth/refresh -H 'X-CSRF-TOKEN: csrf-invalid'
400 {"detail":"CSRF token mismatch","code":"bad_request", ...}
```

여기서 중요한 건 이 CSRF가 Spring Security의 built-in CSRF가 아니라는 점이다. `SecurityConfig`는 `http.csrf(csrf -> csrf.disable())`로 프레임워크 CSRF를 꺼 두고 `/api/v1/**`를 전부 `permitAll()`로 열어 둔다. 즉 이 랩에서 CSRF는 보안 필터 체인이 아니라, refresh token 가족을 설명하기 위한 application-level 규칙이다.

## 3. cross-cutting을 보면 더 분명한 구멍이 보인다

이 랩의 공통 계층은 깔끔하게 보인다. `TraceIdFilter`가 `X-Trace-Id`를 심고, `GlobalExceptionHandler`는 `IllegalArgumentException`과 `MethodArgumentNotValidException`을 ProblemDetail로 감싼다. health와 lab info endpoint도 있다.

하지만 실제로 수동 실행을 해 보면 이 계층이 아직 거칠다. `/api/v1/auth/me`는 인증 없이 query param `email`만으로 호출되고, 응답에는 `passwordHash`가 그대로 포함된다.

```bash
$ GET /api/v1/auth/me?email=spring@example.com
200 {"userId":"...","email":"spring@example.com","passwordHash":"bcrypt$pw-1234","verified":false}
```

또 하나는 validation 경계다. request body record 안에 `@Email`, `@NotBlank`를 붙여 뒀지만, controller parameter에 `@Valid`가 없어서 invalid register body가 현재는 그대로 통과한다.

```bash
$ POST /api/v1/auth/register
{"email":"not-an-email","password":""}
201 {"email":"not-an-email", ...}
```

반대로 `me(@RequestParam @Email String email)`는 method validation이 걸려 invalid email이면 `ConstraintViolationException`이 터지는데, `GlobalExceptionHandler`가 이 예외를 처리하지 않아 지금은 ProblemDetail `400`이 아니라 기본 `500`으로 떨어진다. 즉 validation이 있는 곳과 없는 곳이 어긋나 있다.

## 4. 실제 검증은 통과하지만, 그것이 의미하는 범위를 좁게 읽어야 한다

현재 머신에서는 로컬 JRE가 없어 `make lint`, `make test`, `make smoke`가 모두 실패했다. 대신 같은 프로젝트를 `eclipse-temurin:21-jdk` 컨테이너에서 재실행해 `spotlessCheck`, `checkstyleMain`, `checkstyleTest`, `test`, `test --tests "*SmokeTest"`를 모두 통과시켰다. `bootRun`도 같은 방식으로 올려 수동 HTTP 확인을 마쳤다.

```bash
$ docker run ... bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
BUILD SUCCESSFUL

$ docker run ... bash -lc './gradlew test'
BUILD SUCCESSFUL

$ docker run ... bash -lc './gradlew test --tests "*SmokeTest"'
BUILD SUCCESSFUL
```

이 결과가 뜻하는 건 "auth가 안전하다"가 아니다. 더 정확히는 "이 랩이 의도한 scaffold 범위, 즉 auth lifecycle 설명용 표면은 현재 코드대로 재현된다"는 뜻이다. 그리고 그 표면 안에 인-memory storage, CSRF의 application-level 모델링, unauthenticated `me`, body validation 구멍이 함께 들어 있다는 사실까지 포함해서 읽어야 한다.

그래서 다음 랩 `B-federation-security-lab`으로 넘어가기 전에 이 랩에서 꼭 챙겨야 할 질문이 남는다. 지금의 로컬 auth는 무엇을 설명해 주고, 무엇은 아직 실제 보안 기능이 아닌가. 이 문서는 바로 그 경계를 다시 고정하는 기록이다.
