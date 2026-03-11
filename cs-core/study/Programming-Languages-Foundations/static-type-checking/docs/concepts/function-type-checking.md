# 함수 타입 검사

function boundary는 toy language에서도 가장 많은 규칙이 모이는 곳입니다.

## 검사 순서

1. parameter annotation이 모두 있는지 확인합니다.
2. parameter type을 type environment에 넣고 body를 검사합니다.
3. body type과 declared return type을 비교합니다.
4. call site에서는 callee가 function type인지, arity가 맞는지, 각 argument type이 맞는지 확인합니다.

## higher-order function이 특별해 보이는 이유

`Int -> Int` 자체가 값처럼 전달되기 때문입니다. 하지만 checker 입장에서는 결국 "parameter 타입 중 하나가 function type"인 경우일 뿐입니다.

이 프로젝트는 generic이나 inference를 넣지 않아서, higher-order function도 명시적 annotation만 있으면 일반 function과 같은 경로로 검사됩니다.
