# 01 Approach Log

## 설계 선택

- parser는 동일 문법을 유지하고, compiler가 AST를 stack instruction으로 낮추도록 구성했습니다.
- nested function은 `FunctionProto + capture_sources` 조합으로 만들고, runtime에서 실제 capture tuple을 채우도록 했습니다.
- `and`, `or`는 dedicated opcode 대신 jump lowering으로 처리했습니다.
- interpreter-vs-VM equivalence를 위해 같은 프로젝트 안에 `reference_evaluator.py`를 두었습니다.
