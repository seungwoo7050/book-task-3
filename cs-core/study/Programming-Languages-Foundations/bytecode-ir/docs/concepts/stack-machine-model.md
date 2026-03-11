# Stack Machine 모델

이 프로젝트의 VM은 register machine이 아니라 stack machine입니다.

## 왜 stack machine을 쓰는가

- toy compiler에서 lowering 규칙이 단순합니다.
- expression language는 "왼쪽 평가 -> 오른쪽 평가 -> 연산 적용" 패턴이 많아 stack과 잘 맞습니다.
- disassembly를 읽을 때도 operand 흐름이 비교적 직관적입니다.

## 현재 instruction이 맡는 역할

- `PUSH_CONST`: literal push
- `LOAD_LOCAL`, `LOAD_CAPTURE`, `LOAD_GLOBAL`: 이름 해석 결과를 stack에 올림
- `STORE_LOCAL`: `let` binding 값을 local slot에 저장
- arithmetic/comparison op: stack top 값을 꺼내 계산
- `JUMP`, `JUMP_IF_FALSE`, `JUMP_IF_TRUE`: `if`, short-circuit lowering
- `MAKE_CLOSURE`, `CALL`, `RETURN`: function runtime
