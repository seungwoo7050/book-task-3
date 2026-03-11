# 01 Approach Log

## 설계 선택

- parser는 `parser-interpreter`와 거의 같은 구조를 유지했습니다. 바뀐 것은 AST에 line/column을 더 적극적으로 남긴 점입니다.
- `let`은 annotation이 없으면 value type을 binding type으로 사용하고, annotation이 있으면 exact match만 허용했습니다.
- function parameter annotation은 필수로 두고, missing annotation은 바로 static diagnostic으로 거절했습니다.
- higher-order function도 별도 special case를 두지 않고 function type의 한 형태로 처리했습니다.
