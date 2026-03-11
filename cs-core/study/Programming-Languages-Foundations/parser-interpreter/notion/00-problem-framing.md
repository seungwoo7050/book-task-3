# 00 Problem Framing

## 핵심 질문

- 문자를 token으로 자르는 단계와 AST를 만드는 단계를 어디서 분리해야 구현과 설명이 모두 쉬워지는가?
- lexical closure를 가진 작은 언어를 가장 적은 문법으로 어떻게 보여 줄 수 있는가?
- 타입 주석을 지금부터 문법에 넣되, 실행 단계는 어떻게 단순하게 유지할 것인가?

## 성공 기준

- parser가 precedence와 special form을 안정적으로 처리한다.
- evaluator가 lexical scope, closure, short-circuit를 올바르게 실행한다.
- 타입 주석이 AST에 남아 뒤 단계 `static-type-checking`와 연결된다.
