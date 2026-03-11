# Environment와 Closure

이 프로젝트의 evaluator는 값을 "현재 environment에서 expression을 해석한 결과"로 읽습니다.

## lexical scope를 어떻게 읽을까

- `let`은 현재 environment를 부모로 갖는 child environment를 하나 만들고 이름을 추가합니다.
- `fun`은 즉시 실행하지 않고, body와 parameter 목록, 그리고 **정의 시점 environment**를 함께 묶어 closure를 만듭니다.
- `call`은 closure가 캡처한 environment를 부모로 하는 새 call environment를 만들어 parameter를 바인딩합니다.

## short-circuit가 중요한 이유

- `and`, `or`는 오른쪽 피연산자를 항상 평가하지 않습니다.
- `true or missing_name` 같은 표현이 정상 동작해야 evaluator가 실제 언어 의미를 흉내 낸다고 볼 수 있습니다.

## 지금 단계에서 runtime이 책임지는 것

- arity mismatch
- non-callable value 호출
- unbound name
- non-bool condition / logical operator
- divide by zero

타입이 맞는지, branch type이 같은지는 다음 프로젝트 `static-type-checking`로 넘깁니다.
