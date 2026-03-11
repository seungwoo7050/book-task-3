# Bytecode IR

같은 toy language를 stack-based bytecode로 낮춘 뒤 작은 VM으로 실행하는 프로젝트입니다.
표면 문법은 유지한 채 실행 모델만 바꾸는 것이 핵심입니다.

## 이 프로젝트에서 배우는 것

- AST를 instruction sequence로 낮추는 최소 compiler 구조를 익힙니다.
- call frame, local slot, capture slot이 closure runtime에서 어떤 역할을 하는지 확인합니다.
- tree-walk interpreter와 VM이 같은 결과를 내도록 비교하는 방법을 배웁니다.

## 누구를 위한 문서인가

- parser와 checker 다음에 compiler/runtime 단계까지 이어 보고 싶은 학습자
- stack machine, closure capture, disassembly를 작은 언어로 직접 확인하고 싶은 사람
- execution model을 바꾸더라도 언어 표면은 유지된다는 점을 보고 싶은 사람

## 먼저 읽을 곳

1. `problem/README.md`로 compiler/VM 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 문서로 stack machine과 capture model을 맞춥니다.
3. `src/bytecode_ir/compiler.py`, `src/bytecode_ir/vm.py`, `tests/test_bytecode_ir.py`를 함께 읽습니다.
4. `examples/`와 CLI로 run/disasm 두 출력 표면을 직접 확인합니다.
5. `notion/README.md`와 `notion/05-development-timeline.md`로 재검증 순서를 확인합니다.

## 디렉터리 구조

```text
bytecode-ir/
  README.md
  problem/
  docs/
  examples/
  src/bytecode_ir/
  tests/
  notion/
  notion-archive/
```

## 검증 명령

```bash
cd cs-core/study/Programming-Languages-Foundations/bytecode-ir
python3 -m pytest
PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run
PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm
```

2026-03-11 기준 대표 결과:

- `tests/test_bytecode_ir.py` 9개 테스트 통과
- run demo 결과: `closure-pipeline` -> `42`, `disasm-sample` -> `9`, `higher-order` -> `12`
- disasm demo에서 `MAKE_CLOSURE`, `CALL`, `JUMP_IF_FALSE`, `RETURN` 흐름이 안정적으로 출력됨

## 공개 범위

- 이 프로젝트는 self-authored compiler/runtime lab이므로 구현 코드, 테스트, `docs/`, `examples/`, `notion/`을 전부 공개 대상으로 유지합니다.
- 외부 비공개 자산 없이 현재 저장소 안의 fixture와 CLI 출력만으로 lowering과 runtime을 재현할 수 있습니다.

## 구현에서 집중할 포인트

- nested function이 outer local/capture를 어떤 순서로 capture slot에 저장하는지 봅니다.
- `let` shadowing을 compile-time binding 복구와 runtime local slot 증가로 어떻게 동시에 처리하는지 확인합니다.
- short-circuit `and`, `or`를 jump 기반으로 lowering해 불필요한 오른쪽 평가를 피하는지 봅니다.

## 포트폴리오로 확장하는 힌트

- disassembly screenshot이나 VM trace를 추가하면 compiler/runtime 설명력이 크게 올라갑니다.
- optimizer pass나 richer IR를 후속 프로젝트로 떼어 내면 "학습용 compiler pipeline" 서사가 더 선명해집니다.
