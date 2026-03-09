# Problem Framing

## 인증이 끝난 후, 진짜 질문이 시작된다

A-auth-lab과 B-federation-security-lab은 "이 사람이 누구인가?"에 답하는 랩이었다. 비밀번호로든, Google OIDC로든, 시스템은 사용자의 identity를 확인했고 토큰을 발급했다. 하지만 토큰을 받은 뒤에 남는 질문이 있다—**"이 사람이 무엇을 할 수 있는가?"**

이 랩은 그 질문에만 집중한다. Workspace를 만들고, 다른 사용자를 초대하고, 역할을 부여하고, 역할에 따라 문서 생성이나 열람을 허용하거나 차단한다. 핵심은 **authorization—권한 판단—을 인증과 분리된 독립 주제로 다루는 것**이다.

## 핵심 단순화: Header-Based Actor

이 랩에서 가장 눈에 띄는 설계 결정은 인증을 완전히 우회했다는 것이다. 사용자 identity는 `X-User-Id` 헤더로 전달된다. JWT도 없고, 쿠키도 없다. `deps.py`의 `get_actor_id`는 단순히 이 헤더 값을 꺼내서 반환한다.

이 선택에는 이유가 있다. 만약 JWT 검증과 RBAC 규칙을 한 랩에 넣으면, 테스트가 실패했을 때 원인이 토큰 파싱인지 권한 규칙인지 구분하기 어렵다. 헤더로 actor를 주입하면 **authorization 규칙만 고립해서 테스트할 수 있다.** 물론 실제 서비스에서는 이렇게 하면 안 된다—아무나 헤더를 조작할 수 있으니까. 이 단순화는 학습 맥락에서만 유효하고, capstone에서 실제 인증 스택과 결합할 때 검증된다.

## 도메인 모델

네 가지 핵심 엔터티가 있다:

- **User**: email과 name만 가진 최소 모델. 인증 관련 필드가 전혀 없다.
- **Workspace**: 이름(name)과 소유자(owner_user_id)가 있는 조직 단위.
- **Membership**: user_id + workspace_id + role. 한 사용자가 한 워크스페이스에 한 번만 소속될 수 있다(유니크 제약).
- **Invite**: 워크스페이스에 사용자를 초대하는 토큰 기반 요청. pending → accepted/declined 상태 전이.
- **Document**: 워크스페이스에 속하고, 생성자(owner_user_id)가 있는 문서.

## 역할 체계

네 단계 역할: viewer < member < admin < owner. 각 역할의 권한 경계:

- **viewer**: 문서 읽기만 가능
- **member**: 문서 생성 가능
- **admin**: 초대 발행 가능
- **owner**: 역할 변경 가능

`_require_role` 메서드가 `ROLE_ORDER` 딕셔너리로 역할 수준을 비교한다. 최소 역할보다 낮으면 403.

## 성공 기준

- workspace 생성 시 생성자가 자동으로 owner membership을 갖는다
- admin 이상만 초대를 발행할 수 있다
- 초대 수락 시 이메일이 일치해야 한다
- viewer는 문서를 읽을 수 있지만 생성할 수 없다
- 워크스페이스에 속하지 않은 사용자는 문서를 읽을 수 없다
- `make lint`, `make test`, `make smoke`, Compose probe 통과

## 불확실성

- header-based actor가 실제 JWT 인증과 결합되었을 때 authorization 규칙이 그대로 작동할지는 이 랩에서 증명하지 않는다
- method-level declarative authorization(Spring Security의 @PreAuthorize 같은)은 시도하지 않았다
- 정책 엔진(OPA, Casbin 등)과의 비교는 없다
