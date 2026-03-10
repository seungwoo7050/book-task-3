# Approach Log

## Identity Source를 어디서 끊을 것인가

첫 번째 결정은 인증 스택을 어디까지 포함할 것인가였다. 세 가지 선택지가 있었다:

1. **A/B 랩의 JWT 인증을 그대로 가져오기**: 현실적이지만, 토큰 발급·검증 코드를 다시 복사해야 하고, 테스트 실패 시 원인 분리가 어렵다.
2. **헤더 기반 actor 주입**: 인공적이지만, authorization 로직만 고립해서 볼 수 있다.
3. **mock 인증 미들웨어**: 중간 지점이지만 실질적으로 헤더 주입과 큰 차이가 없다.

헤더 기반을 택했다. `X-User-Id` 헤더 하나로 "이 요청의 주체"를 결정하고, 나머지는 서비스 계층의 authorization 로직에 맡긴다. 이 결정 덕분에 테스트에서 어떤 사용자가 어떤 동작을 시도하는지를 헤더 한 줄로 표현할 수 있다.

## Workspace → Membership → Document: 소유와 소속의 구분

Workspace에는 `owner_user_id`가 있다. 이것은 "누가 이 워크스페이스를 만들었는가"의 기록이다. 동시에 같은 사용자에게 role="owner"인 Membership 레코드가 생성된다. 왜 둘 다 필요할까?

`owner_user_id`는 테이블 레벨의 foreign key로, 워크스페이스와 사용자의 관계를 DB가 보장한다. Membership의 role="owner"는 RBAC 규칙에서 사용된다. 이 이중 기록이 없으면 "소유자인데 membership이 없어서 자기 워크스페이스에 접근 못 하는" 버그가 발생할 수 있다. `create_workspace`에서 Workspace 생성과 owner Membership 생성을 한 트랜잭션으로 묶는 이유다.

Document에도 `owner_user_id`가 있다. 현재는 문서를 읽을 때 워크스페이스 멤버십만 확인하지만, 나중에 "자신이 만든 문서만 삭제 가능" 같은 규칙을 추가할 때 이 필드가 필요해진다.

## Invite Lifecycle: 즉시 추가 대신 초대 흐름을 둔 이유

가장 단순한 방식은 admin이 바로 Membership을 생성하는 것이다. 하지만 실제 서비스에서는 초대된 사람이 "수락 여부를 선택"할 수 있어야 한다. Invite 모델은 이 선택을 표현한다:

1. admin이 `POST /workspaces/{id}/invites`로 초대 생성 → status="pending"
2. 초대받은 사용자가 `POST /invites/{token}/accept` → Membership 생성, status="accepted"
3. 또는 `POST /invites/{token}/decline` → status="declined"

핵심 제약: accept 시 actor의 email과 invite의 email이 일치해야 한다. 이것은 "초대 링크를 가로챈 다른 사람이 수락하는" 시나리오를 막는다.

## 역할 변경의 제한

역할 변경(`PATCH /workspaces/{id}/members/{user_id}`)은 owner만 할 수 있다. admin도 못 한다. 이것은 "admin이 자기 자신을 owner로 승격하는" 권한 상승을 막기 위한 결정이다. 코드에서는 `_require_role(minimum="owner")`로 먼저 검증하고, 추가로 `membership.role != "owner"`를 다시 체크하는 이중 검증을 한다.

## 기각된 방향

- **ownership 개념 제거**: membership만으로 권한을 판단하면 구조가 단순해지지만, "누가 만들었는가"라는 현실적 질문에 답할 수 없다.
- **정책 엔진(OPA 등) 도입**: 이 랩의 규모에서는 과도하다. 규칙이 4단계 역할 비교에 불과하므로 서비스 메서드 안에서 직접 판단하는 것이 더 명확하다.
