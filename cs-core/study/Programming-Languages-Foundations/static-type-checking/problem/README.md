# 문제 경계

이 문서는 `static-type-checking` 프로젝트에서 무엇을 검사해야 하는지를 현재 기준으로 다시 설명합니다.
별도 starter artifact 없이 이 문서 자체가 요구사항 원본 역할을 합니다.

## 문제 핵심

- `parser-interpreter`와 같은 문법을 다시 파싱해야 합니다.
- arithmetic/comparison/logical operator의 operand type을 실행 전에 확인해야 합니다.
- `if` condition, then/else branch, function call, function return을 static rule로 검증해야 합니다.
- function parameter annotation은 필수, `let` annotation은 선택으로 유지해야 합니다.

## 이번 범위에서 일부러 뺀 것

- Hindley-Milner 스타일 전역 추론은 포함하지 않습니다.
- subtyping, generic, ADT, pattern matching은 포함하지 않습니다.
- code generation과 runtime optimization은 다음 단계 범위입니다.

## 제공 자료

- 별도 starter code는 없습니다.
- `examples/*.plf`와 `tests/test_static_type_checking.py`가 canonical accept/reject fixture 역할을 합니다.

## 역사적 출처와 현재 재구성

- 참고 출처: `Types and Programming Languages`, `Crafting Interpreters`, `Essentials of Compilation`
- 현재 재구성 방식: 작은 expression language를 유지한 채, evaluator 대신 type environment와 diagnostics를 앞세운 self-contained Python 프로젝트로 다시 정리했습니다.
- 같은 문법을 유지한 이유: `parser-interpreter`와 `bytecode-ir`를 하나의 커리큘럼으로 묶기 위해서입니다.

## canonical validation

```bash
cd cs-core/study/Programming-Languages-Foundations/static-type-checking
python3 -m pytest
PYTHONPATH=src python3 -m static_type_checking --demo all
```
