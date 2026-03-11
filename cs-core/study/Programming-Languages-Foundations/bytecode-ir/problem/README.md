# 문제 경계

이 문서는 `bytecode-ir` 프로젝트에서 무엇을 compile/run 해야 하는지를 현재 기준으로 다시 설명합니다.
별도 starter artifact 없이 이 문서 자체가 요구사항 원본 역할을 합니다.

## 문제 핵심

- `parser-interpreter`, `static-type-checking`와 같은 문법을 다시 파싱해야 합니다.
- AST를 stack-based bytecode로 낮추고, VM이 그 bytecode를 실행해야 합니다.
- nested function은 explicit capture slot을 가진 closure object로 만들어야 합니다.
- disassembler가 instruction sequence를 안정된 텍스트 표면으로 출력해야 합니다.

## 이번 범위에서 일부러 뺀 것

- register allocator, SSA, optimization pass는 포함하지 않습니다.
- native code generation과 JIT는 포함하지 않습니다.
- module/linker, debug info, garbage collector는 포함하지 않습니다.

## 제공 자료

- 별도 starter code는 없습니다.
- `examples/*.plf`와 `tests/test_bytecode_ir.py`가 canonical fixture 역할을 합니다.

## 역사적 출처와 현재 재구성

- 참고 출처: `Essentials of Compilation`, `Crafting Interpreters`
- 현재 재구성 방식: tree-walk evaluator와 static checker 뒤에 오는 세 번째 단계로, 같은 language surface를 stack VM 실험으로 다시 묶었습니다.
- `reference_evaluator.py`를 같이 둔 이유: interpreter와 VM의 결과를 같은 프로젝트 안에서 대조하기 위해서입니다.

## canonical validation

```bash
cd cs-core/study/Programming-Languages-Foundations/bytecode-ir
python3 -m pytest
PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run
PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm
```
