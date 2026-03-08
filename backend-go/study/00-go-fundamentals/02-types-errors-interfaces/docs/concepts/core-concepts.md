# Core Concepts

## 핵심 개념

- struct는 상태를, method는 그 상태에 대한 동작을 표현한다.
- interface는 “무엇을 할 수 있는가”를 분리할 때만 쓰는 편이 단순하다.
- custom error 타입은 `errors.As`로 세부 의미를 복원할 수 있게 해 준다.

## Trade-offs

- 작은 예제에서는 interface가 과한 추상화가 되기 쉽다.
- sentinel error는 비교가 쉽지만 문맥이 약하다. custom error는 문맥이 풍부하지만 타입 관리가 필요하다.

## 실패하기 쉬운 지점

- 에러 메시지 문자열 비교에 의존하면 테스트가 취약해진다.
- pointer/value receiver를 뒤섞으면 상태 변경 의도가 흐려진다.

