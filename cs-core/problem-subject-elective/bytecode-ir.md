# bytecode-ir 문제지

## 왜 중요한가

이 문서는 bytecode-ir 프로젝트에서 무엇을 compile/run 해야 하는지를 현재 기준으로 다시 설명합니다. 별도 starter artifact 없이 이 문서 자체가 요구사항 원본 역할을 합니다.

## 목표

시작 위치의 구현을 완성해 parser-interpreter, static-type-checking와 같은 문법을 다시 파싱해야 합니다, AST를 stack-based bytecode로 낮추고, VM이 그 bytecode를 실행해야 합니다, nested function은 explicit capture slot을 가진 closure object로 만들어야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Programming-Languages-Foundations/bytecode-ir/src/bytecode_ir/__init__.py`
- `../study/Programming-Languages-Foundations/bytecode-ir/src/bytecode_ir/__main__.py`
- `../study/Programming-Languages-Foundations/bytecode-ir/src/bytecode_ir/ast.py`
- `../study/Programming-Languages-Foundations/bytecode-ir/src/bytecode_ir/compiler.py`
- `../study/Programming-Languages-Foundations/bytecode-ir/tests/conftest.py`
- `../study/Programming-Languages-Foundations/bytecode-ir/tests/test_bytecode_ir.py`
- `../study/Programming-Languages-Foundations/bytecode-ir/pyproject.toml`

## starter code / 입력 계약

- `../study/Programming-Languages-Foundations/bytecode-ir/src/bytecode_ir/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- parser-interpreter, static-type-checking와 같은 문법을 다시 파싱해야 합니다.
- AST를 stack-based bytecode로 낮추고, VM이 그 bytecode를 실행해야 합니다.
- nested function은 explicit capture slot을 가진 closure object로 만들어야 합니다.
- disassembler가 instruction sequence를 안정된 텍스트 표면으로 출력해야 합니다.

## 제외 범위

- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `_print_summary`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_disassembly_golden_for_simple_program`와 `test_vm_matches_reference_evaluator`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd cs-core/study/Programming-Languages-Foundations/bytecode-ir && python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm`가 통과한다.

## 검증 방법

```bash
cd cs-core/study/Programming-Languages-Foundations/bytecode-ir && python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm
```

```bash
cd /Users/woopinbell/work/book-task-3/cs-core/study/Programming-Languages-Foundations/bytecode-ir && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`bytecode-ir_answer.md`](bytecode-ir_answer.md)에서 확인한다.
