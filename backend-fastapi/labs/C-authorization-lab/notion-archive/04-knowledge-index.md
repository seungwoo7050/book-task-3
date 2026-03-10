# Knowledge Index

## RBAC (Role-Based Access Control)

역할 이름으로 권한 집합을 표현하는 접근 제어 모델이다. 이 랩에서 역할은 단순한 문자열(viewer, member, admin, owner)이고, 서열이 있다. `ROLE_ORDER` 딕셔너리가 각 역할에 숫자를 매기고, `_require_role`에서 "최소 X 이상"으로 비교한다.

RBAC의 핵심 장점은 **역할 하나만 확인하면** 해당 권한 집합 전체가 결정된다는 것이다. 단점은 역할이 고정적이라서 세밀한 조건부 접근 제어(시간 제한, 리소스 소유자 여부 등)를 표현하기 어렵다는 점이다. 이런 경우에는 ABAC(Attribute-Based Access Control)이나 정책 엔진을 고려해야 한다.

## Membership vs Ownership

이 두 개념은 자주 혼동되지만 다른 것을 말한다:

- **Membership**: "이 사용자가 이 그룹에 속하는가?" → 소속 여부
- **Ownership**: "이 리소스를 누가 만들었는가?" → 생성 책임

이 랩에서 Workspace에는 `owner_user_id` FK와 role="owner" Membership이 동시에 존재한다. FK는 DB가 보장하는 참조 무결성이고, Membership의 role은 RBAC 규칙에서 사용된다. 두 기록이 모두 필요한 이유는, FK만 있으면 RBAC 쿼리에서 별도 조인이 필요하고, Membership만 있으면 "최초 생성자"라는 정보가 불명확해지기 때문이다.

## Invitation Lifecycle Pattern

즉시 멤버십 부여 대신 초대 흐름을 두는 패턴이다:

```
Admin → POST /invites → Invite(status=pending) → 이메일 통지
                                                     ↓
                                        Invitee → POST /accept → Membership 생성
                                        Invitee → POST /decline → status=declined
```

이 패턴의 가치:
1. **동의 기반 가입**: 초대받은 사람이 선택할 수 있다
2. **감사 추적**: pending/accepted/declined 상태가 기록으로 남는다
3. **이메일 검증**: accept 시 actor email과 invite email 비교로 위변조를 막는다

## Header-Based Actor (학습용 단순화)

실제 서비스에서는 절대 사용하면 안 되는 패턴이지만, 학습 맥락에서 authorization 로직을 완전히 고립시키기 위해 사용했다. 장점과 한계:

- **장점**: 테스트에서 `headers={"X-User-Id": user_id}`만으로 어떤 사용자를 흉내낼 수 있다. 토큰 발급 과정 없이 바로 권한 규칙을 테스트한다.
- **한계**: 아무나 헤더를 조작할 수 있으므로 인증이 없는 것과 같다. 반드시 실제 인증 스택 뒤에서 사용하거나 capstone에서 교체해야 한다.

## Forbidden-Path Testing

권한 테스트에서 가장 중요한 것은 **금지 경로도 명시적으로 테스트하는 것**이다. "admin이 초대할 수 있다"만 테스트하면 "viewer가 초대할 수 없다"가 보장되지 않는다.

이 랩의 테스트에서 이 원칙이 적용된 예:
- viewer가 문서를 생성하려 하면 → 403
- outsider가 문서를 읽으려 하면 → 403
- 초대를 거절한 사용자는 workspace 멤버가 아니므로 → 여전히 접근 불가
