# Bytecode IR

`bytecode-ir`는 같은 toy language를 stack-based bytecode로 낮춘 뒤 작은 VM으로 실행해 표면 문법은 유지한 채 실행 모델만 바꾸는 프로젝트다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| AST를 bytecode instruction sequence로 lowering하고 VM에서 실행해 interpreter와 같은 의미를 유지한다. | stack machine 모델을 유지하고, closure capture와 call frame을 self-contained runtime으로 구현한다. | 구현은 [`src/bytecode_ir/`](src/bytecode_ir), [`tests/`](tests), [`examples/`](examples), run/disasm CLI로 정리한다. | [`problem/README.md`](problem/README.md), [`docs/README.md`](docs/README.md) | lowering, stack machine, closure capture, disassembly, VM execution | `public verified` |

실제 소스코드·테스트·검증 엔트리 기준의 blog 시리즈: [`../../blog/Programming-Languages-Foundations/bytecode-ir/00-series-map.md`](../../blog/Programming-Languages-Foundations/bytecode-ir/00-series-map.md)

## 디렉터리 역할

- `problem/`: compiler/VM 범위와 제외한 항목
- `src/bytecode_ir/`: compiler, bytecode model, VM 구현
- `tests/`: compiler/runtime acceptance test
- `examples/`: run/disasm demo 입력 예제
- `docs/`: stack machine, capture model, bytecode/disassembly 개념 정리
- `notion/`: 접근 로그와 재검증 timeline

## 검증 빠른 시작

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

## 공개 경계

- 이 프로젝트는 self-authored compiler/runtime lab이므로 구현 코드, 테스트, `docs/`, `examples/`, `notion/`을 전부 공개 대상으로 유지한다.
- README는 run/disasm 검증 entrypoint에 집중하고, lowering 세부 reasoning은 `docs/`, `notion/`으로 분리한다.
