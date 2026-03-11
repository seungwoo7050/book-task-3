# 00 Problem Framing

## 핵심 질문

- parser는 유지한 채 error surface만 static checker로 옮기려면 어떤 최소 type rule이 필요한가?
- optional `let` annotation과 mandatory function boundary를 같이 두면 어떤 학습 포인트가 생기는가?
- runtime evaluator가 하던 책임 중 무엇을 checker가 먼저 가져가야 하는가?

## 성공 기준

- accept/reject fixture가 operator, branch, call, return, unbound name 케이스를 모두 덮는다.
- CLI가 성공 시 결과 타입 하나를 안정적으로 출력한다.
- 다음 단계 `bytecode-ir`와 공유할 문법 계약이 흔들리지 않는다.
