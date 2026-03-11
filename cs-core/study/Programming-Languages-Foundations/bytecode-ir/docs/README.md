# 개념 문서 안내

이 디렉터리는 `bytecode-ir`를 읽기 전에 compiler와 VM의 최소 개념을 맞추는 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/stack-machine-model.md`](concepts/stack-machine-model.md): AST 결과를 stack machine instruction으로 바꾸는 기본 모델을 설명합니다.
- [`concepts/call-frame-and-closure.md`](concepts/call-frame-and-closure.md): local slot, capture slot, call frame이 어떻게 엮이는지 설명합니다.
- [`concepts/bytecode-disassembly.md`](concepts/bytecode-disassembly.md): disassembler를 왜 유지하는지, 어떤 정보를 stable text로 남기는지 설명합니다.

## 추천 읽기 순서

1. stack machine 메모로 lowering 목표를 먼저 맞춥니다.
2. call frame/closure 메모로 runtime 구조를 읽습니다.
3. disassembly 메모로 테스트가 어떤 표면을 고정하는지 확인합니다.
4. [`references/README.md`](references/README.md)로 provenance를 확인합니다.
