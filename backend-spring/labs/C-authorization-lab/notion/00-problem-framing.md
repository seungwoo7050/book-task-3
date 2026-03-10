# Problem Framing — "누가 무엇을 할 수 있는가"를 코드로 표현하기

## 이 랩이 풀려는 문제

인증(authentication)이 "이 사람이 누구인가"를 확인하는 것이라면, 인가(authorization)는 **"이 사람이 이걸 해도 되는가"**를 결정하는 것이다. A랩과 B랩을 거치면서 "누구인지는 확인할 수 있게 됐다"면, 이제 남은 질문은 "그래서 이 사용자에게 뭘 허용할 것인가"이다.

이 랩은 인증과 의도적으로 분리해서, **role, membership, ownership** 세 가지 축에서 authorization이 어떻게 작동하는지를 보여준다. 구체적으로는:

1. **Organization 생성과 소유권** — 조직을 만든 사람이 OWNER가 된다.
2. **Invite lifecycle** — 초대장을 발행하고, 수락하면 멤버가 된다. 즉시 권한을 부여하는 대신 invite 상태를 거치는 이유는 보안과 감사 추적 때문이다.
3. **Role change** — 멤버의 역할(STAFF → MANAGER 등)을 변경한다.
4. **Ownership check** — 같은 role이라도 생성자/소유자에게만 허용되는 규칙이 있다.

처음엔 이 주제를 auth 랩에 합치는 것도 고려했다. 하지만 직접 작업해보니, 인증과 인가를 같은 코드에 넣으면 "login 실패인지 permission 거부인지" 원인 추적이 어려워진다. 실패 원인이 섞이면 디버깅도, 학습도 방해된다.

## 기술 환경과 제약

**언어와 프레임워크**: Java 21, Spring Boot 3.4.x.

**핵심 제약**: 이 랩에서 **membership state는 인메모리**(`ConcurrentHashMap`)다. `AuthorizationDemoService`가 조직, 초대장, 멤버십을 모두 메모리에 관리한다. Spring Security의 `@PreAuthorize` 같은 method-level security는 아직 적용하지 않았다 — authorization 규칙 자체를 service logic으로 먼저 이해하게 하기 위해서다.

## 성공 기준

1. **invite, membership, role change**가 service logic 수준에서 명확히 드러나야 한다.
2. **forbidden path**(권한이 없는 경우의 거부)를 설명할 수 있어야 한다.
3. 문서에 적힌 명령어(`make lint`, `make test`, `make smoke`)가 실제로 통과해야 한다.
4. **in-memory simplification**을 숨기지 않아야 한다.

## 아직 확실하지 않은 것들

인메모리 membership이 policy complexity를 충분히 보여주는지는 제한적이다. 실제 서비스에서는 "이 사용자가 이 조직의 이 리소스에 대해 이 작업을 할 수 있는가"라는 훨씬 복잡한 판단이 필요하다. 그래도 scaffold 단계에서는 **rule의 형태(shape)를 먼저 고정하는 것**이 낫다고 판단했다. persistence와 method security는 후속 과제로 남겨두었다.

