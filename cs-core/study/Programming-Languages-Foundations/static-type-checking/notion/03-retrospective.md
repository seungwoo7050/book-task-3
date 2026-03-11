# 03 Retrospective

## 이번 단계에서 얻은 것

- parser를 고정한 상태에서도 checker 하나만 추가하면 언어 설명의 초점이 완전히 달라집니다.
- static/runtime 경계를 explicit하게 분리하면 이후 VM 단계에서 무엇을 믿고 가도 되는지가 훨씬 선명해집니다.

## 일부러 남긴 단순화

- inference는 `let` 수준만 암묵적으로 허용하고, function boundary는 전부 명시적 주석에 의존합니다.
- polymorphism과 recursive type은 다루지 않았습니다.

## 다음 단계

- `bytecode-ir`에서 같은 AST를 stack-based bytecode로 낮추고 VM 결과를 비교합니다.
- 더 깊게 가려면 local inference, let-polymorphism, richer type surface를 따로 떼어 내는 편이 좋습니다.
