# Recursive Descent와 Precedence

이 프로젝트의 문법은 special form과 일반 expression을 같은 함수 하나에 전부 몰아넣기보다, recursive descent와 precedence climbing을 나눠 씁니다.

## 왜 두 방식을 함께 쓰는가

- `let`, `if`, `fun`은 prefix keyword로 시작하는 special form이라 recursive descent가 가장 읽기 쉽습니다.
- `+`, `*`, `==`, `and`, `or`는 우선순위와 결합 방향이 중요하므로 precedence climbing이 간결합니다.
- 둘을 섞으면 "문장처럼 보이는 문법"과 "연산처럼 보이는 문법"을 같은 AST로 자연스럽게 합칠 수 있습니다.

## 현재 parser의 읽는 기준

1. 먼저 prefix 위치에서 `let`, `if`, `fun`, unary operator를 판정합니다.
2. 그 외에는 primary expression을 읽고, 바로 뒤의 call suffix `(...)`를 붙입니다.
3. 마지막으로 precedence table에 따라 infix operator를 접습니다.

## 이 구조가 뒤 단계에 주는 이점

- `static-type-checking`가 같은 문법을 다시 파싱할 때 parser shape를 거의 그대로 재사용할 수 있습니다.
- `bytecode-ir` 단계에서도 AST 모양이 크게 바뀌지 않아 evaluator와 VM 결과 비교가 쉬워집니다.
