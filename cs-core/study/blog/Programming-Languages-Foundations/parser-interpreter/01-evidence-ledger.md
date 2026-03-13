# Parser Interpreter Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`parser-interpreter`는 작은 함수형 코어 언어를 직접 토큰화하고, recursive descent parser로 AST를 만들고, tree-walk evaluator로 실행하는 프로젝트다. 구현의 중심은 `src`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `src/parser_interpreter/__init__.py`, `src/parser_interpreter/__main__.py`, `src/parser_interpreter/ast.py`, `src/parser_interpreter/diagnostics.py`, `src/parser_interpreter/environment.py`, `src/parser_interpreter/evaluator.py`, `src/parser_interpreter/lexer.py`, `src/parser_interpreter/parser.py`다. 검증 표면은 `tests/conftest.py`, `tests/test_parser_interpreter.py`와 `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `environment and closures`, `lexer and token stream`, `recursive descent and precedence`이다.

## Git History Anchor

- `2026-03-11	0cccd64	feat: add new project in cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - lexer와 token stream contract를 먼저 만든다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 파서 프로젝트도 결국 가장 먼저 흔들리면 안 되는 것은 token boundary다.

그때 세운 가설은 문법 오류를 parser에서 다루기 전에 `tokenize_source`가 identifier, number, keyword를 안정적으로 자르는 쪽이 우선이라고 봤다. 실제 조치는 lexer와 token definition을 먼저 고정해 parser가 기대할 입력 표면을 만들었다.

- 정리해 둔 근거:
- 변경 단위: `src/parser_interpreter/lexer.py`, `src/parser_interpreter/tokens.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`
- 검증 신호: token stream이 먼저 있으니 parser 오류를 문법 문제로 좁힐 수 있다.
- 새로 배운 것: 언어 구현의 첫 단계는 AST보다 먼저 source를 신뢰할 수 있는 token stream으로 바꾸는 일이었다.

### 코드 앵커 — `tokenize_source` (`src/parser_interpreter/lexer.py:120`)

```python
def tokenize_source(source: str) -> list[Token]:
    return Lexer(source).tokenize()
```

이 조각은 token stream이 먼저 있으니 parser 오류를 문법 문제로 좁힐 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `tokenize_source`를 읽고 나면 다음 장면이 왜 recursive descent parser로 precedence를 얹는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `Token` (`src/parser_interpreter/tokens.py:7`)

```python
class Token:
    kind: str
    lexeme: str
    line: int
    column: int
```

이 조각은 token stream이 먼저 있으니 parser 오류를 문법 문제로 좁힐 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `Token`를 읽고 나면 다음 장면이 왜 recursive descent parser로 precedence를 얹는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 recursive descent parser로 precedence를 얹는다.

## 2. Phase 2 - recursive descent parser와 evaluator로 lexical scope를 연결한다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `parse_source`, `evaluate_source`, environment helper가 같은 언어 surface를 두 단계로 나눠 설명한다.

그때 세운 가설은 parser와 evaluator를 강하게 결합하면 closure와 short-circuit reasoning이 흐려질 것 같아 AST를 중심으로 단계를 분리했다. 실제 조치는 precedence-aware parser를 만든 뒤 environment/closure evaluator를 separate module로 유지했다.

- 정리해 둔 근거:
- 변경 단위: `src/parser_interpreter/parser.py`, `src/parser_interpreter/evaluator.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`
- 검증 신호: parser/evaluator 분리가 글에서도 판단 이동을 자연스럽게 보여 준다.
- 새로 배운 것: toy language도 parser와 evaluator를 분리해야 lexical scope와 evaluation order를 더 또렷하게 설명할 수 있었다.

### 코드 앵커 — `evaluate_source` (`src/parser_interpreter/evaluator.py:115`)

```python
def evaluate_source(source: str) -> object:
    from .parser import parse_source

    return evaluate_expression(parse_source(source))
```

이 조각은 parser/evaluator 분리가 글에서도 판단 이동을 자연스럽게 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `evaluate_source`를 읽고 나면 다음 장면이 왜 demo program과 pytest로 표면을 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `parse_source` (`src/parser_interpreter/parser.py:230`)

```python
def parse_source(source: str) -> Expr:
    return Parser(tokenize_source(source)).parse()
```

이 조각은 parser/evaluator 분리가 글에서도 판단 이동을 자연스럽게 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `parse_source`를 읽고 나면 다음 장면이 왜 demo program과 pytest로 표면을 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 demo program과 pytest로 표면을 닫는다.

## 3. Phase 3 - demo program과 pytest로 언어 표면을 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 언어 프로젝트는 내부 AST보다 sample program 결과가 더 직접적인 검증 신호가 된다.

그때 세운 가설은 examples와 CLI demo가 남아 있어야 closure, short-circuit, typed syntax parsing을 한 번에 재생할 수 있다고 판단했다. 실제 조치는 `python3 -m pytest`와 `--demo all` entrypoint를 남겨 parser/evaluator 경로를 반복 실행 가능하게 만들었다.

- 정리해 둔 근거:
- 변경 단위: `tests/test_parser_interpreter.py`, `src/parser_interpreter/__main__.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`
- 검증 신호: pytest와 demo output이 최종 검증 신호를 남긴다.
- 새로 배운 것: 언어 구현은 REPL이 없어도 demo program과 pytest만 있으면 충분히 살아 있는 표면이 된다.

### 코드 앵커 — `main` (`src/parser_interpreter/__main__.py:10`)

```python
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse and evaluate the parser-interpreter project language.")
    parser.add_argument("--program", type=Path, help="path to a .plf source file")
    parser.add_argument("--demo", help="demo name or 'all'")
    args = parser.parse_args(argv)
```

이 조각은 pytest와 demo output이 최종 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `main`를 읽고 나면 다음 장면이 왜 token stream -> AST/evaluator -> demo verification 순서로 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `test_closure_uses_lexical_scope` (`tests/test_parser_interpreter.py:97`)

```python
def test_closure_uses_lexical_scope():
    source = """
    let make_adder = fun (x: Int) -> Int => fun (y: Int) -> Int => x + y in
    let add_five = make_adder(5) in
    add_five(7)
    """
    assert evaluate_source(source) == 12
```

이 조각은 pytest와 demo output이 최종 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `test_closure_uses_lexical_scope`를 읽고 나면 다음 장면이 왜 token stream -> AST/evaluator -> demo verification 순서로 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 token stream -> AST/evaluator -> demo verification 순서로 닫는다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Programming-Languages-Foundations/parser-interpreter && python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all)
```

```text
body:
    Call
    callee:
      Identifier(apply)
    args:
      Identifier(inc)
-- result --
11
```
