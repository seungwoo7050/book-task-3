# Approach Log — 설계를 어떻게 결정했는가

## 선택지를 놓고 고민한 지점들

인증 랩을 만들 때 가장 먼저 떠오른 방식은 "처음부터 persisted user table과 full reset flow까지 다 넣는 것"이었다. 현실적이고 완결성도 높지만, Spring 학습 트랙의 **첫 번째 랩**으로는 너무 무거웠다. JPA 매핑, 트랜잭션, 마이그레이션까지 한꺼번에 다루면 초점이 흐려진다.

반대쪽 극단은 contract-first scaffold — API shape만 잡아놓고 구현은 거의 스텁으로 두는 방식이었다. 이건 빠르게 전체 구조를 보여줄 수 있지만, "실제로 동작하지 않는 코드"를 학습 재료로 쓰는 건 위험하다. 테스트도 의미 없어지고, 독자가 "이게 진짜 되는 건가?" 하는 의심을 계속 안고 가게 된다.

cookie를 실제 HTTP response cookie로 다루는 방식도 고려했다. 이건 결국 해야 할 일이지만, 처음 scaffold를 잡을 때는 API shape 설명이 우선이었다. 브라우저 통합까지 한 번에 가면, `Set-Cookie` 헤더, `SameSite` 속성, secure 플래그 등 부수적인 주제가 한꺼번에 밀려든다.

## 최종 선택: "동작하는 scaffold"

결국 선택한 방향은 **인메모리 persistence로 흐름을 먼저 완성하기**였다.

**패키지 구조**는 auth 중심의 단일 Spring workspace로 잡았다. `auth.api`(컨트롤러)와 `auth.application`(서비스) 두 패키지가 핵심이고, `global` 패키지에 security config, error handler, health check 같은 공통 인프라를 모았다.

**persistence는 ConcurrentHashMap**이다. `AuthDemoService`가 유저 정보와 세션을 메모리에 들고 있다. 이건 의도적인 결정인데, "refresh rotation이 무엇인지"를 코드로 보여주는 데 JPA는 필요 없기 때문이다. 오히려 순수 자바 자료구조만으로 로직이 드러나니까 학습 효과가 더 좋다.

**security boundary**는 refresh rotation과 CSRF pairing을 먼저 드러내는 데 집중했다. `SecurityConfig`에서는 CSRF를 disable하고 모든 `/api/v1/**` 경로를 permitAll로 열어두었는데, 이건 Spring Security 자체의 CSRF 메커니즘 대신 **애플리케이션 레벨에서 CSRF 토큰을 직접 관리하는 패턴**을 보여주기 위해서다. `AuthController.refresh()`가 `X-CSRF-TOKEN` 헤더를 명시적으로 검증하는 것이 그 증거다.

**integration style**으로는 Mailpit-ready local stack을 Docker Compose에 포함시켰다. 실제 메일이 발송되지는 않지만, Mailpit UI(포트 8125)에서 메일이 도착하는 것을 눈으로 확인할 수 있는 환경은 갖춰놓았다. full mail lifecycle은 의도적으로 뒤로 미뤘다.

이 선택이 이 랩에 맞다고 판단한 이유는 단순하다. **첫 랩의 임무는 개념 지형도를 잡는 것**이다. "refresh token이 rotation 되면 이전 토큰은 무효화된다", "CSRF 토큰이 불일치하면 요청이 거부된다" — 이 두 가지를 테스트 코드로 증명할 수 있으면 성공이다.

## 의식적으로 폐기한 아이디어들

**OAuth2와 2FA를 함께 넣는 방안**은 초기에 잠깐 고려했지만 곧바로 폐기했다. A랩의 범위는 "로컬 계정 인증"이다. OAuth2 social login은 B-federation-security-lab의 영역이고, 여기서 같이 다루면 양쪽 모두 중간까지만 설명하는 어정쩡한 상태가 된다.

**full browser-integrated cookie behavior를 첫 랩 필수 요건으로 두는 방안**도 폐기했다. `Set-Cookie`, `SameSite`, `Secure` 플래그를 제대로 다루려면 프론트엔드까지 붙여야 하고, 학습 반복 속도가 심각하게 느려진다. 이건 "다음 개선"으로 명확히 분류했다.

## 이 결정을 뒷받침하는 근거

- `AuthController.java` — register/login/refresh/logout/me 다섯 가지 엔드포인트가 깔끔하게 한 파일에 모여 있어서 흐름을 한 눈에 파악할 수 있다.
- `AuthDemoService.java` — ConcurrentHashMap 기반 인메모리 로직으로, refresh rotation과 CSRF 검증이 외부 의존성 없이 순수하게 드러난다.
- `AuthFlowApiTest.java` — register → login → refresh 전체 흐름과 CSRF 불일치 거절을 MockMvc로 증명한다.
- `make test` — 위 테스트가 실제로 통과하는 것을 CLI에서 확인할 수 있다.

