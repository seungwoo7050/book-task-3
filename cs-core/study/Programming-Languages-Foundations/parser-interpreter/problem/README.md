# 문제 경계

이 문서는 `parser-interpreter` 프로젝트에서 무엇을 구현해야 하는지를 현재 기준으로 다시 설명합니다.
외부 starter artifact 없이 이 문서 자체가 요구사항 원본 역할을 합니다.

## 문제 핵심

- 정수/불리언 literal, identifier, `let`, `if`, `fun`, call을 포함한 expression-oriented 언어를 파싱해야 합니다.
- unary `-`, `not`, binary arithmetic/comparison/logical operator의 precedence와 associativity를 안정적으로 처리해야 합니다.
- lexical closure와 eager evaluation을 지원하는 tree-walk interpreter가 필요합니다.
- type annotation 문법을 파싱하되, 이 단계에서는 실행 의미에 사용하지 않아야 합니다.

## 이번 범위에서 일부러 뺀 것

- mutation, statement, loop, object model은 포함하지 않습니다.
- type inference, static checker, bytecode/VM은 다음 단계 범위입니다.
- optimizer, macro, module system은 포함하지 않습니다.

## 제공 자료

- 별도 starter code는 없습니다.
- `examples/*.plf`와 `tests/test_parser_interpreter.py`가 현재 범위의 canonical fixture 역할을 합니다.

## 역사적 출처와 현재 재구성

- 참고 출처: `Crafting Interpreters`, `Types and Programming Languages`, `Essentials of Compilation`
- 현재 재구성 방식: lexer/parser/type/IR 파이프라인 중 첫 단계만 떼어 내어 `cs-core` 학습 트랙에 맞게 self-contained Python 프로젝트로 다시 정리했습니다.
- 타입 주석을 지금부터 문법에 남겨 둔 이유: 뒤의 `static-type-checking`, `bytecode-ir`가 같은 언어를 공유하기 위해서입니다.

## canonical validation

```bash
cd cs-core/study/Programming-Languages-Foundations/parser-interpreter
python3 -m pytest
PYTHONPATH=src python3 -m parser_interpreter --demo all
```
