# 02 Debug Log

## 다시 깨질 수 있는 지점

- function type pretty-printer에서 단항 함수 타입 괄호를 빼면 `(Int -> Int) -> Int`와 `Int -> Int -> Int`가 구분되지 않습니다.
- `bool`이 Python에서 `int`의 subclass라서, runtime type check를 `isinstance(value, int)`로 쓰면 `true + 1` 같은 케이스가 잘못 통과할 수 있습니다.
- short-circuit를 일반 binary operator처럼 구현하면 `true or missing_name`이 unbound name 오류로 깨집니다.
- `src` 레이아웃 프로젝트는 테스트 수집 시 import path를 명시적으로 잡지 않으면 `ModuleNotFoundError`가 발생합니다.
