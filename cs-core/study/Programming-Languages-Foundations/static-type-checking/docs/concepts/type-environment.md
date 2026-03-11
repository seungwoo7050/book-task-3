# 타입 환경

evaluator의 environment가 이름을 값으로 연결한다면, type checker의 environment는 이름을 타입으로 연결합니다.

## 왜 별도 구조가 필요한가

- `let value = 10 in value + 1`에서 checker는 `value`의 실제 값 `10`이 아니라 타입 `Int`만 알면 충분합니다.
- function body를 검사할 때도 parameter 값은 없지만 parameter type은 있어야 합니다.
- lexical scope 구조는 그대로 유지하되, 저장하는 payload만 값에서 타입으로 바뀐다고 보면 읽기 쉽습니다.

## 현재 프로젝트의 규칙

- `let` annotation이 없으면 value type을 그대로 binding type으로 사용합니다.
- `let` annotation이 있으면 value type과 정확히 같아야 합니다.
- `fun` parameter는 annotation이 없으면 checker가 즉시 거절합니다.
