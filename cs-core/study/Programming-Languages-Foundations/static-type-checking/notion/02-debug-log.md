# 02 Debug Log

## 다시 깨질 수 있는 지점

- function type pretty-printer에서 괄호 규칙이 틀리면 `Int -> Int -> Int`와 `(Int -> Int) -> Int`가 섞입니다.
- `bool`이 Python에서 `int`의 subclass라서, checker 보조 로직이 host runtime helper와 섞이면 타입 구분이 흐려질 수 있습니다.
- `let` shadowing을 environment parent chain 대신 단일 dict mutation으로 처리할 때 복구 순서를 놓치면 진단이 흔들릴 수 있습니다.
- line/column을 expression이 아니라 token에서만 들고 있으면 branch mismatch 같은 오류를 어디에 꽂을지 애매해집니다.
