# Parser Interpreter 재구성 개발 로그

`parser-interpreter`는 작은 함수형 코어 언어를 직접 토큰화하고, recursive descent parser로 AST를 만들고, tree-walk evaluator로 실행하는 프로젝트다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

token stream을 먼저 고정하고, recursive descent parser와 evaluator를 올린 뒤, closure demo로 lexical scope를 닫는 흐름을 복원한다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: lexer와 token stream contract를 먼저 만든다 — `src/parser_interpreter/lexer.py`, `src/parser_interpreter/tokens.py`
- Phase 2: recursive descent parser와 evaluator로 lexical scope를 연결한다 — `src/parser_interpreter/parser.py`, `src/parser_interpreter/evaluator.py`
- Phase 3: demo program과 pytest로 언어 표면을 닫는다 — `tests/test_parser_interpreter.py`, `src/parser_interpreter/__main__.py`

## Phase 1. lexer와 token stream contract를 먼저 만든다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 파서 프로젝트도 결국 가장 먼저 흔들리면 안 되는 것은 token boundary다.

처음에는 문법 오류를 parser에서 다루기 전에 `tokenize_source`가 identifier, number, keyword를 안정적으로 자르는 쪽이 우선이라고 봤다. 그런데 실제로 글의 중심이 된 조치는 lexer와 token definition을 먼저 고정해 parser가 기대할 입력 표면을 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `src/parser_interpreter/lexer.py`, `src/parser_interpreter/tokens.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`
- 검증 신호: token stream이 먼저 있으니 parser 오류를 문법 문제로 좁힐 수 있다.

### 이 장면을 고정하는 코드 — `tokenize_source` (`src/parser_interpreter/lexer.py:120`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

```python
def tokenize_source(source: str) -> list[Token]:
    return Lexer(source).tokenize()
```

`tokenize_source`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 언어 구현의 첫 단계는 ast보다 먼저 source를 신뢰할 수 있는 token stream으로 바꾸는 일이었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 recursive descent parser로 precedence를 얹는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 언어 구현의 첫 단계는 AST보다 먼저 source를 신뢰할 수 있는 token stream으로 바꾸는 일이었다.

그래서 다음 장면에서는 recursive descent parser로 precedence를 얹는다.

## Phase 2. recursive descent parser와 evaluator로 lexical scope를 연결한다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 `parse_source`, `evaluate_source`, environment helper가 같은 언어 surface를 두 단계로 나눠 설명한다.

처음에는 parser와 evaluator를 강하게 결합하면 closure와 short-circuit reasoning이 흐려질 것 같아 AST를 중심으로 단계를 분리했다. 그런데 실제로 글의 중심이 된 조치는 precedence-aware parser를 만든 뒤 environment/closure evaluator를 separate module로 유지했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `src/parser_interpreter/parser.py`, `src/parser_interpreter/evaluator.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`
- 검증 신호: parser/evaluator 분리가 글에서도 판단 이동을 자연스럽게 보여 준다.

### 이 장면을 고정하는 코드 — `evaluate_source` (`src/parser_interpreter/evaluator.py:115`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

```python
def evaluate_source(source: str) -> object:
    from .parser import parse_source

    return evaluate_expression(parse_source(source))
```

`evaluate_source`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 toy language도 parser와 evaluator를 분리해야 lexical scope와 evaluation order를 더 또렷하게 설명할 수 있었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 demo program과 pytest로 표면을 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 toy language도 parser와 evaluator를 분리해야 lexical scope와 evaluation order를 더 또렷하게 설명할 수 있었다.

그래서 다음 장면에서는 demo program과 pytest로 표면을 닫는다.

## Phase 3. demo program과 pytest로 언어 표면을 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 언어 프로젝트는 내부 AST보다 sample program 결과가 더 직접적인 검증 신호가 된다.

처음에는 examples와 CLI demo가 남아 있어야 closure, short-circuit, typed syntax parsing을 한 번에 재생할 수 있다고 판단했다. 그런데 실제로 글의 중심이 된 조치는 `python3 -m pytest`와 `--demo all` entrypoint를 남겨 parser/evaluator 경로를 반복 실행 가능하게 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `tests/test_parser_interpreter.py`, `src/parser_interpreter/__main__.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`
- 검증 신호: pytest와 demo output이 최종 검증 신호를 남긴다.

### 이 장면을 고정하는 코드 — `main` (`src/parser_interpreter/__main__.py:10`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```python
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse and evaluate the parser-interpreter project language.")
    parser.add_argument("--program", type=Path, help="path to a .plf source file")
    parser.add_argument("--demo", help="demo name or 'all'")
    args = parser.parse_args(argv)
```

`main`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 언어 구현은 repl이 없어도 demo program과 pytest만 있으면 충분히 살아 있는 표면이 된다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 token stream -> AST/evaluator -> demo verification 순서로 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 언어 구현은 REPL이 없어도 demo program과 pytest만 있으면 충분히 살아 있는 표면이 된다.

그래서 다음 장면에서는 token stream -> AST/evaluator -> demo verification 순서로 닫는다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

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

## 이번에 남은 질문

- 개념 축: `environment and closures`, `lexer and token stream`, `recursive descent and precedence`
- 대표 테스트/fixture: `tests/conftest.py`, `tests/test_parser_interpreter.py`
- 다음 질문: 최종 글은 token stream -> AST/evaluator -> demo verification 순서로 닫는다.
