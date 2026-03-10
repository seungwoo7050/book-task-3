# Retrospective — 인증 랩을 마치고 돌아보며

## 나아진 점

이 랩을 끝내고 가장 크게 달라진 건 **Spring 인증의 구조적 뼈대를 머릿속에 잡은 것**이다.

처음에는 "Spring Security가 알아서 해주겠지"라는 막연한 기대가 있었다. 하지만 직접 `SecurityConfig`를 작성하면서, `SecurityFilterChain`이 어떤 순서로 요청을 거르는지, CSRF를 disable한다는 것이 정확히 무엇을 의미하는지를 손으로 만져볼 수 있었다.

cookie, CSRF, refresh rotation 같은 **보안 용어를 초반부터 고정한 판단**은 결과적으로 좋았다. 이 용어들이 이후 B-federation-security-lab이나 C-authorization-lab에서 등장할 때 "아, 이건 A랩에서 이미 다룬 거"라고 연결할 수 있는 기반이 됐다.

Mailpit-ready local stack 구성도 의외로 유용했다. 직접 메일이 발송되진 않지만, **Docker Compose 하나로 PostgreSQL, Redis, Mailpit이 모두 뜨는 환경**을 갖춰놓으니, 이후 랩에서 메일 발송 기능을 붙일 때 인프라를 다시 고민할 필요가 없어졌다.

## 여전히 약한 부분

솔직하게 말하면, 이 랩의 persistence는 **지금 상태로는 학습용 이상의 가치가 없다**. `ConcurrentHashMap`으로 유저와 세션을 관리하는 건 "인메모리"라는 표현조차 과분하다. 서버를 끄면 모든 데이터가 사라진다.

verification token과 refresh token family의 persistence도 아직 얕다. `RegisterResult`에 `verificationToken` 필드가 있지만, 이 토큰이 실제로 어딘가에 저장되거나 만료되는 로직은 없다.

reset과 verify는 API-first 설명이 더 강한데, 이건 "개념은 알지만 구현은 못 했다"를 세련되게 포장한 것에 가깝다. 다음 단계에서 반드시 실체를 채워야 한다.

## 다시 살펴볼 것들

**단기**: cookie를 실제 HTTP response cookie(`Set-Cookie` 헤더)로 내려주고, 테스트에서 `HttpOnly`, `Secure`, `SameSite` 속성을 검증하는 것. 이건 JSON body로 토큰을 내려주는 현재 방식보다 훨씬 실무에 가깝다.

**중기**: PostgreSQL persistence를 더 일찍 넣을지 재검토. 현재는 D-data-jpa-lab에서 다루기로 했지만, 인증 데이터만큼은 A랩에서부터 실제 DB에 넣는 게 학습 흐름상 자연스러울 수 있다.

**장기**: Spring Security의 deeper integration — `UserDetailsService` 구현, `PasswordEncoder` 적용, `@PreAuthorize`와 method-level security까지 연결하는 것. 이건 capstone 또는 C-authorization-lab에서 다룰 영역이지만, A랩의 scaffold가 그 기반이 된다.

