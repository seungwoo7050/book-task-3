# Bytecode IR Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Bytecode IR에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 source surface를 bytecode compiler 입력으로 고정한다 -> Phase 2 VM, closure, disassembler를 실행 모델의 중심에 둔다 -> Phase 3 demo run과 disassembly로 compiler path를 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - source surface를 bytecode compiler 입력으로 고정한다

이 구간의 중심 장면은 bytecode IR 프로젝트도 parser surface가 바뀌면 앞선 두 프로젝트와 연결 고리가 끊어진다.

본문에서는 먼저 언어 표면은 유지하고 실행 모델만 바꾸는 편이 lowering의 의미를 더 분명하게 드러낼 것이라고 판단했다. 그 다음 문단에서는 shared AST/parse 단계 위에 `compile_source`, `_compile_expr`, `_compile_function`을 올려 compiler 경로를 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `compile_source`, `_compile_expr`
- 붙일 CLI: `python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm`
- 강조할 검증 신호: compiler가 별도 모듈로 남아 있어 lowering 자체를 독립 단계로 설명할 수 있다.
- 장면이 끝날 때 남길 문장: VM과 reference evaluator를 연결한다.

## 2. Phase 2 - VM, closure, disassembler를 실행 모델의 중심에 둔다

이 구간의 중심 장면은 `run_source`, `_run_closure`, `disassemble_source`, reference evaluator가 이 프로젝트의 핵심 비교축이다.

본문에서는 먼저 compiler만 있으면 bytecode가 맞는지 설명하기 어렵기 때문에 VM과 reference evaluator를 같이 두어 결과를 상호 검증해야 한다고 봤다. 그 다음 문단에서는 stack machine, call frame, closure execution, disassembly 출력을 분리해 bytecode와 실행 결과를 동시에 읽히게 했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `run_source`, `disassemble_source`
- 붙일 CLI: `python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm`
- 강조할 검증 신호: VM/disassembler/reference evaluator 삼각 구도가 판단 전환점을 가장 잘 보존한다.
- 장면이 끝날 때 남길 문장: demo run과 disasm 출력으로 lowering 결과를 닫는다.

## 3. Phase 3 - demo run과 disassembly로 compiler path를 닫는다

이 구간의 중심 장면은 bytecode 프로젝트는 테스트 통과만으로는 충분하지 않고, lowering 결과를 사람이 읽을 수 있어야 한다.

본문에서는 먼저 CLI에서 실행 결과와 disassembly를 둘 다 남기면 compiler가 무엇을 만들었는지 설명이 더 쉬워질 것이라고 판단했다. 그 다음 문단에서는 `--emit run`, `--emit disasm`, pytest를 남겨 compile -> execute -> inspect 경로를 한 번에 재생하게 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `test_disassembly_golden_for_simple_program`, `main`
- 붙일 CLI: `python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm`
- 강조할 검증 신호: pytest와 demo/disasm output이 마지막 검증 신호를 남긴다.
- 장면이 끝날 때 남길 문장: compiler -> VM/reference evaluator -> disassembly verification 순서로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Programming-Languages-Foundations/bytecode-ir && python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
