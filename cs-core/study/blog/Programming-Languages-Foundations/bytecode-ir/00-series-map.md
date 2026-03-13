# Bytecode IR 시리즈 맵

`bytecode-ir`는 같은 toy language를 stack-based bytecode로 낮춘 뒤 작은 VM으로 실행해 표면 문법은 유지한 채 실행 모델만 바꾸는 프로젝트다. 이 시리즈는 결과만 정리해 둔 회고문이 아니라, 같은 언어 표면을 유지한 채 compiler와 VM을 올리고, reference evaluator/disassembler로 lowering 결과를 확인하는 흐름을 복원한다.를 끝까지 따라가게 만드는 입구다.

2026-03-13에 기존 초안을 `study/blog/_legacy/2026-03-13-isolate-and-rewrite/Programming-Languages-Foundations/bytecode-ir/`로 옮긴 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 시리즈를 다시 썼다. 그래서 이 문서는 '무엇을 만들었는가'보다 '어떤 순서로 읽어야 그 판단 이동이 보이는가'를 먼저 설명한다.

## 이 시리즈를 읽는 방법

가장 먼저 `01-evidence-ledger.md`에서 살아 있는 근거를 모아 본다. 그 다음 `_structure-outline.md`에서 왜 최종 글이 그 순서로 배치되는지 확인한다. 마지막으로 `10-2026-03-13-reconstructed-development-log.md`에서 그 근거가 실제 서사로 어떻게 이어지는지 읽는다.

## 이번 재작성에서 붙잡은 source-of-truth

- 문제 계약: [`README.md`](../../../Programming-Languages-Foundations/bytecode-ir/README.md), [`problem/README.md`](../../../Programming-Languages-Foundations/bytecode-ir/problem/README.md)
- 구현 표면: `src/bytecode_ir/__init__.py`, `src/bytecode_ir/__main__.py`, `src/bytecode_ir/ast.py`, `src/bytecode_ir/compiler.py`, `src/bytecode_ir/diagnostics.py`, `src/bytecode_ir/lexer.py`
- 검증 entrypoint: `python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm` in `.`
- 개념 축: `bytecode disassembly`, `call frame and closure`, `stack machine model`

## 읽는 순서

1. [`01-evidence-ledger.md`](01-evidence-ledger.md) — source-first 근거와 phase별 판단 전환점을 먼저 모아 둔 문서
2. [`_structure-outline.md`](_structure-outline.md) — 최종 글의 읽기 곡선과 장면 배치를 설명하는 편집 설계 메모
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md) — 구현 순서, 코드, CLI를 한 흐름으로 다시 쓴 최종 blog

## 이번에 따라간 질문

같은 언어 표면을 유지한 채 compiler와 VM을 올리고, reference evaluator/disassembler로 lowering 결과를 확인하는 흐름을 복원한다.
