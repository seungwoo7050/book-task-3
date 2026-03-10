# Retrospective

## Authorization을 고립시키고 나서 보인 것

인증 스택 없이 authorization만 다루니, 역할과 소유권의 차이가 훨씬 선명해졌다. A-auth-lab에서는 "로그인한 사용자"라는 단일 주체만 있었지만, 여기서는 같은 시스템 안에 owner, admin, member, viewer, outsider가 공존한다. 각각이 같은 엔드포인트에 다른 결과를 받는다는 것을 테스트로 명시한 것이 이 랩의 핵심 가치다.

invite lifecycle을 별도 주제로 다룬 것도 좋았다. 멤버십이 "즉시 추가"가 아니라 "초대 → 수락/거절"의 상태 전이를 거친다는 설계는, 실제 서비스에서 "관리자가 실수로 잘못된 사람을 추가하는" 문제를 줄인다. pending 상태의 invite가 있다는 것 자체가 "아직 확정되지 않은 결정"을 표현하는 도메인 언어다.

## Service Boundary에 Permission 판단을 둔 효과

권한 검증이 라우트가 아니라 서비스 계층에 있기 때문에, 테스트에서 HTTP를 거치지 않고도 `AuthorizationService`를 직접 호출해서 규칙을 검증할 수 있다. 이 구조는 나중에 같은 authorization 규칙을 WebSocket이나 배치 작업에서도 재사용할 수 있게 한다.

다만 `_require_role`이 모든 접근 제어를 하는 단일 메서드라는 것은 규칙이 복잡해지면 한계가 있다. 리소스 종류별로 다른 권한 요구사항이 생기면 이 메서드 하나로는 부족해질 수 있다.

## 아직 약한 것들

- **Declarative authorization**: FastAPI에는 Spring Security의 `@PreAuthorize`에 해당하는 내장 기능이 없다. 현재는 서비스 메서드 안에서 명시적으로 호출하는 방식이고, 이것은 실수로 호출을 빼먹을 가능성이 있다.
- **Policy language**: 규칙이 단순한 역할 비교를 넘어서면(시간 기반 접근, 조건부 권한 등) 코드에 직접 박는 것보다 정책 엔진이 나을 수 있다.
- **실제 인증과의 통합**: header-based actor는 학습에 유용하지만, 실제 JWT 인증과 결합했을 때의 미들웨어 구성은 capstone에서 확인해야 한다.

## 다시 보고 싶은 것

- Spring Security method-level annotation과의 비교 분석
- ownership-aware 삭제/수정 규칙 추가 (현재 Document에 owner_user_id가 있지만 활용되지 않음)
- admin이 다른 admin을 초대할 수 있는지, admin hierarchy 관련 edge case
