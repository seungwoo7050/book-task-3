# Bytecode IR Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`bytecode-ir`는 같은 toy language를 stack-based bytecode로 낮춘 뒤 작은 VM으로 실행해 표면 문법은 유지한 채 실행 모델만 바꾸는 프로젝트다. 구현의 중심은 `src`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `src/bytecode_ir/__init__.py`, `src/bytecode_ir/__main__.py`, `src/bytecode_ir/ast.py`, `src/bytecode_ir/compiler.py`, `src/bytecode_ir/diagnostics.py`, `src/bytecode_ir/lexer.py`, `src/bytecode_ir/parser.py`, `src/bytecode_ir/reference_evaluator.py`다. 검증 표면은 `tests/conftest.py`, `tests/test_bytecode_ir.py`와 `python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `bytecode disassembly`, `call frame and closure`, `stack machine model`이다.

## Git History Anchor

- `2026-03-11	0cccd64	feat: add new project in cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - source surface를 bytecode compiler 입력으로 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 bytecode IR 프로젝트도 parser surface가 바뀌면 앞선 두 프로젝트와 연결 고리가 끊어진다.

그때 세운 가설은 언어 표면은 유지하고 실행 모델만 바꾸는 편이 lowering의 의미를 더 분명하게 드러낼 것이라고 판단했다. 실제 조치는 shared AST/parse 단계 위에 `compile_source`, `_compile_expr`, `_compile_function`을 올려 compiler 경로를 만들었다.

- 정리해 둔 근거:
- 변경 단위: `src/bytecode_ir/compiler.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm`
- 검증 신호: compiler가 별도 모듈로 남아 있어 lowering 자체를 독립 단계로 설명할 수 있다.
- 새로 배운 것: lowering을 이해하려면 새 언어를 만드는 것이 아니라 같은 언어를 다른 실행 모델로 옮긴다는 사실을 계속 유지해야 했다.

### 코드 앵커 — `compile_source` (`src/bytecode_ir/compiler.py:90`)

```python
def compile_source(source: str) -> FunctionProto:
    from .parser import parse_source

    return compile_expression(parse_source(source))
```

이 조각은 compiler가 별도 모듈로 남아 있어 lowering 자체를 독립 단계로 설명할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `compile_source`를 읽고 나면 다음 장면이 왜 VM과 reference evaluator를 연결한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `_compile_expr` (`src/bytecode_ir/compiler.py:110`)

```python
def _compile_expr(expression: Expr, context: CompileContext) -> None:
    if isinstance(expression, IntegerLiteral):
        context.emit("PUSH_CONST", expression.value)
        return
    if isinstance(expression, BooleanLiteral):
        context.emit("PUSH_CONST", expression.value)
        return
    if isinstance(expression, Identifier):
        source = context.resolve(expression.name)
        if source is None:
            context.emit("LOAD_GLOBAL", expression.name)
            return
```

이 조각은 compiler가 별도 모듈로 남아 있어 lowering 자체를 독립 단계로 설명할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `_compile_expr`를 읽고 나면 다음 장면이 왜 VM과 reference evaluator를 연결한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 VM과 reference evaluator를 연결한다.

## 2. Phase 2 - VM, closure, disassembler를 실행 모델의 중심에 둔다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `run_source`, `_run_closure`, `disassemble_source`, reference evaluator가 이 프로젝트의 핵심 비교축이다.

그때 세운 가설은 compiler만 있으면 bytecode가 맞는지 설명하기 어렵기 때문에 VM과 reference evaluator를 같이 두어 결과를 상호 검증해야 한다고 봤다. 실제 조치는 stack machine, call frame, closure execution, disassembly 출력을 분리해 bytecode와 실행 결과를 동시에 읽히게 했다.

- 정리해 둔 근거:
- 변경 단위: `src/bytecode_ir/vm.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm`
- 검증 신호: VM/disassembler/reference evaluator 삼각 구도가 판단 전환점을 가장 잘 보존한다.
- 새로 배운 것: IR 설명은 opcode 목록보다 '같은 프로그램이 reference evaluator와 VM에서 어떻게 일치하는가'로 볼 때 훨씬 명확했다.

### 코드 앵커 — `run_source` (`src/bytecode_ir/vm.py:18`)

```python
def run_source(source: str) -> object:
    return run_proto(compile_source(source))


def run_proto(proto: FunctionProto) -> object:
    return _run_closure(Closure(proto, ()), [], {})
```

이 조각은 vm/disassembler/reference evaluator 삼각 구도가 판단 전환점을 가장 잘 보존한다는 설명이 실제로 어디서 나오는지 보여 준다. `run_source`를 읽고 나면 다음 장면이 왜 demo run과 disasm 출력으로 lowering 결과를 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `disassemble_source` (`src/bytecode_ir/vm.py:26`)

```python
def disassemble_source(source: str) -> str:
    return disassemble_proto(compile_source(source))


def disassemble_proto(proto: FunctionProto) -> str:
    lines: list[str] = []
    seen: set[int] = set()
```

이 조각은 vm/disassembler/reference evaluator 삼각 구도가 판단 전환점을 가장 잘 보존한다는 설명이 실제로 어디서 나오는지 보여 준다. `disassemble_source`를 읽고 나면 다음 장면이 왜 demo run과 disasm 출력으로 lowering 결과를 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 demo run과 disasm 출력으로 lowering 결과를 닫는다.

## 3. Phase 3 - demo run과 disassembly로 compiler path를 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 bytecode 프로젝트는 테스트 통과만으로는 충분하지 않고, lowering 결과를 사람이 읽을 수 있어야 한다.

그때 세운 가설은 CLI에서 실행 결과와 disassembly를 둘 다 남기면 compiler가 무엇을 만들었는지 설명이 더 쉬워질 것이라고 판단했다. 실제 조치는 `--emit run`, `--emit disasm`, pytest를 남겨 compile -> execute -> inspect 경로를 한 번에 재생하게 만들었다.

- 정리해 둔 근거:
- 변경 단위: `tests/test_bytecode_ir.py`, `src/bytecode_ir/__main__.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm`
- 검증 신호: pytest와 demo/disasm output이 마지막 검증 신호를 남긴다.
- 새로 배운 것: IR 학습은 내부 자료구조보다 bytecode를 직접 보고 reference evaluator와 비교하는 순간 가장 빠르게 이해됐다.

### 코드 앵커 — `test_disassembly_golden_for_simple_program` (`tests/test_bytecode_ir.py:9`)

```python
def test_disassembly_golden_for_simple_program():
    source = "let choose = fun (flag: Bool) -> Int => if flag then 7 else 9 in choose(false)"
    assert (
        disassemble_source(source)
        == textwrap.dedent(
            """
            fn <module> arity=0 locals=1 captures=[-]
            0000 MAKE_CLOSURE <lambda> captures=[-]
            0001 STORE_LOCAL 0
            0002 LOAD_LOCAL 0
            0003 PUSH_CONST False
            0004 CALL 1
```

이 조각은 pytest와 demo/disasm output이 마지막 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `test_disassembly_golden_for_simple_program`를 읽고 나면 다음 장면이 왜 compiler -> VM/reference evaluator -> disassembly verification 순서로 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `main` (`src/bytecode_ir/__main__.py:10`)

```python
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile the shared PL foundations language to bytecode and run it.")
    parser.add_argument("--program", type=Path, help="path to a .plf source file")
    parser.add_argument("--demo", help="demo name or 'all'")
    parser.add_argument("--emit", choices=["run", "disasm"], default="run")
    args = parser.parse_args(argv)
```

이 조각은 pytest와 demo/disasm output이 마지막 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `main`를 읽고 나면 다음 장면이 왜 compiler -> VM/reference evaluator -> disassembly verification 순서로 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 compiler -> VM/reference evaluator -> disassembly verification 순서로 닫는다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Programming-Languages-Foundations/bytecode-ir && python3 -m pytest && PYTHONPATH=src python3 -m bytecode_ir --demo all --emit run && PYTHONPATH=src python3 -m bytecode_ir --demo disasm-sample --emit disasm)
```

```text
============================== 9 passed in 0.04s ===============================
0005 RETURN
fn <lambda> arity=1 locals=1 captures=[-]
0000 LOAD_LOCAL 0
0001 JUMP_IF_FALSE 4
0002 PUSH_CONST 7
0003 JUMP 5
0004 PUSH_CONST 9
```
