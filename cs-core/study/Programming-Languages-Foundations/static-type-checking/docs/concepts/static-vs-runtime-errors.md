# Static Error와 Runtime Error

같은 언어라도 오류를 언제 발견할지는 별도 설계 문제입니다.

## static checker가 맡는 것

- `+`, `-`, `*`, `/`에 `Int`가 아닌 값을 넣는 경우
- `if` condition이 `Bool`이 아닌 경우
- then/else branch type이 다른 경우
- function call arity나 argument type이 맞지 않는 경우
- function body type이 declared return type과 다른 경우

## runtime에 남겨 두는 것

- division by zero처럼 실제 값이 있어야 판단 가능한 실패
- host runtime이나 외부 입력 때문에 실행 중에만 드러나는 실패

이 프로젝트는 "무엇을 미리 막을 수 있는가"를 선명하게 보여 주기 위해, static 단계가 맡을 오류를 일부러 좁고 분명하게 고정합니다.
