# B-federation-security-lab: 강화 기능을 만들기보다 강화 기능의 표면을 먼저 흉내 낸 랩

`B-federation-security-lab`은 이름만 보면 A-auth-lab보다 한 단계 더 실전적인 보안 랩처럼 보인다. 그런데 실제 소스를 따라가 보면, 이 랩의 중심은 security hardening 자체보다 federation, second factor, audit를 어떤 API shape로 잘라 낼지 먼저 정하는 데 있다.

## 1. federation은 provider가 아니라 callback contract부터 시작한다

첫 번째 축은 `GET /api/v1/auth/google/authorize`와 `POST /api/v1/auth/google/callback`이다. `FederationSecurityDemoService.authorize()`는 실제 OAuth flow를 열지 않고 Google authorize URL처럼 생긴 문자열, state, nonce를 만들어 돌려준다. `callback()`은 provider verification도 없이 email과 subject를 그대로 `linkedIdentities` map에 넣고 `provider=google` 응답을 반환한다.

이 선택은 테스트에서도 그대로 드러난다. `FederationSecurityApiTest`는 authorize URL에 `google` 문자열이 들어가는지, callback이 `provider=google`을 돌려주는지만 본다. 즉 이 랩의 federation은 외부 provider를 붙이는 단계가 아니라 callback contract와 state 개념을 먼저 눈에 보이게 만드는 단계다.

## 2. 2FA도 실제 검증보다 shape 설명에 더 가깝다

두 번째 축은 TOTP다. `setupTotp()`는 무작위 문자열에서 앞 6글자를 잘라 expected code로 삼고, recovery code 3개를 고정 배열처럼 돌려준다. `verifyTotp()`는 저장된 expected code와 같은지만 보고 true/false를 반환한다.

수동 재실행에서는 이 단순화가 더 선명하다.

```bash
$ POST /api/v1/auth/2fa/setup
200 {"secret":"A5E0C484627B","recoveryCodes":["rec-1","rec-2","rec-3"],"expectedCode":"A5E0C4"}

$ POST /api/v1/auth/2fa/verify
200 {"verified":true}

$ POST /api/v1/auth/2fa/verify
200 {"verified":false}
```

여기서 중요한 건 `verified:false`가 실패 응답이 아니라 성공 `200`이라는 점, 그리고 setup 응답이 `secret`뿐 아니라 `expectedCode`까지 그대로 노출한다는 점이다. 즉 현재 구현은 second factor를 보호하는 기능이 아니라, second factor가 API 표면에서 어떻게 보이는지 설명하는 데 더 가깝다.

## 3. audit는 남기지만 보호하지는 않는다

federation과 TOTP를 묶는 세 번째 축은 audit다. `authorize()`, `callback()`, `setupTotp()`, `verifyTotp()`는 모두 `auditEvents`에 흔적을 남긴다. 그래서 "강화 기능이 상태 변화를 남긴다"는 메시지는 분명해진다.

문제는 이 audit가 보안 기능으로 닫혀 있지 않다는 점이다. `GET /api/v1/audit-events`는 현재 무인증으로 열려 있고, 수동 재실행에서도 모든 이벤트가 그대로 조회된다.

```bash
$ GET /api/v1/audit-events
[{"type":"google_authorize",...},{"type":"google_callback",...},{"type":"totp_setup",...}]
```

게다가 저장소 자체도 `ArrayList`라 동시 요청을 전제로 한 구조가 아니다. 이 랩의 audit는 규제·감사 로그라기보다 "강화 기능의 흔적을 화면에 올려두는 설명용 surface"로 읽어야 한다.

## 4. security 설정과 validation을 보면 아직 scaffold라는 게 더 분명해진다

이 랩이 실제로 hardening 단계가 아니라는 건 `SecurityConfig`에서 가장 선명하다. A-auth-lab과 똑같이 CSRF를 끄고 `/api/v1/**` 전체를 `permitAll()`로 열어 둔다. 즉 federation callback, TOTP setup/verify, audit 조회가 모두 인증 없이 접근 가능하다.

validation도 마찬가지다. request body record에는 `@Email`, `@NotBlank`가 붙어 있지만 controller parameter에 `@Valid`가 없다. 그래서 수동 재실행에서 invalid callback body가 그대로 `200`으로 통과했다.

```bash
$ POST /api/v1/auth/google/callback
{"email":"not-an-email","subject":""}
200 {"email":"not-an-email","provider":"google","subject":""}
```

이 지점이 중요하다. 이 랩은 인증 강화를 "구현했다"고 말하기보다, 어떤 endpoint와 상태 변화가 필요할지를 먼저 잘라 놓은 것이다. 이름만 보고 보안 강도를 추정하면 문서를 잘못 읽게 된다.

## 5. 검증은 통과하지만, 그 의미를 좁게 읽어야 한다

현재 머신에는 JRE가 없어 로컬 `make lint|test|smoke`는 직접 돌릴 수 없었다. 대신 `eclipse-temurin:21-jdk` 컨테이너에서 `spotlessCheck`, `checkstyleMain`, `checkstyleTest`, `test`, `test --tests "*SmokeTest"`를 다시 실행했고 모두 통과했다. `bootRun`도 같은 방식으로 올려 수동 HTTP 응답을 재확인했다.

```bash
$ docker run ... bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
BUILD SUCCESSFUL

$ docker run ... bash -lc './gradlew test'
BUILD SUCCESSFUL

$ docker run ... bash -lc './gradlew test --tests "*SmokeTest"'
BUILD SUCCESSFUL
```

이 통과가 뜻하는 건 "federation/2FA/audit가 안전하다"가 아니다. 더 정확히는 "이 랩이 의도한 demo surface는 현재 코드대로 재현된다"는 뜻이다. 그리고 그 표면에는 callback contract 우선, TOTP secret/expectedCode 노출, 공개 audit endpoint, 비활성화된 Spring Security 보호가 함께 들어 있다.

그래서 다음 랩으로 이어지는 질문도 자연스럽다. 인증 강화 요소를 설명하는 것과, 그 위에서 실제 권한 판단을 수행하는 것은 별개 문제다. `C-authorization-lab`이 바로 그 분리를 맡는다.
