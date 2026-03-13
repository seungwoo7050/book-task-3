# Static Type Checking Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`static-type-checking`은 같은 toy language를 다시 파싱한 뒤 runtime에 넘기기 전에 어떤 오류를 미리 거를 수 있는지 정리하는 프로젝트다. 구현의 중심은 `src`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `src/static_type_checking/__init__.py`, `src/static_type_checking/__main__.py`, `src/static_type_checking/ast.py`, `src/static_type_checking/checker.py`, `src/static_type_checking/diagnostics.py`, `src/static_type_checking/lexer.py`, `src/static_type_checking/parser.py`, `src/static_type_checking/tokens.py`다. 검증 표면은 `tests/conftest.py`, `tests/test_static_type_checking.py`와 `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `function type checking`, `static vs runtime errors`, `type environment`이다.

## Git History Anchor

- `2026-03-11	0cccd64	feat: add new project in cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - 같은 언어 표면을 다시 파싱 가능한 AST로 유지한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 type checker도 parser가 달라지면 앞 프로젝트와 연결 고리가 끊어진다.

그때 세운 가설은 새 프로젝트지만 parser surface는 최대한 유지하고 type annotation 해석만 덧붙이는 편이 학습 연결이 좋다고 봤다. 실제 조치는 parser/AST를 공유 가능한 형태로 다시 세우고, checker가 기대할 입력 표면을 유지했다.

- 정리해 둔 근거:
- 변경 단위: `src/static_type_checking/parser.py`, `src/static_type_checking/ast.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`
- 검증 신호: shared syntax가 있으니 parser-interpreter와 대비되는 지점이 선명해진다.
- 새로 배운 것: 정적 의미론을 추가할 때도 먼저 지켜야 할 것은 기존 언어 표면과의 연속성이었다.

### 코드 앵커 — `parse_source` (`src/static_type_checking/parser.py:230`)

```python
def parse_source(source: str) -> Expr:
    return Parser(tokenize_source(source)).parse()
```

이 조각은 shared syntax가 있으니 parser-interpreter와 대비되는 지점이 선명해진다는 설명이 실제로 어디서 나오는지 보여 준다. `parse_source`를 읽고 나면 다음 장면이 왜 type environment와 rule checking으로 이동한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `TypeExpr` (`src/static_type_checking/ast.py:6`)

```python
class TypeExpr:
    pass


@dataclass(frozen=True)
class IntType(TypeExpr):
    pass
```

이 조각은 shared syntax가 있으니 parser-interpreter와 대비되는 지점이 선명해진다는 설명이 실제로 어디서 나오는지 보여 준다. `TypeExpr`를 읽고 나면 다음 장면이 왜 type environment와 rule checking으로 이동한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 type environment와 rule checking으로 이동한다.

## 2. Phase 2 - type environment와 rule checking을 별도 층으로 만든다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `check_expression`, `_expect_exact_type`, function type helper가 이 프로젝트의 핵심 전환점이다.

그때 세운 가설은 runtime evaluator처럼 값을 계산하기보다 environment에 타입을 축적하는 규칙을 따로 세워야 오류를 미리 잡을 수 있다고 판단했다. 실제 조치는 type environment, exact-type assertion, function application rule을 checker에 모아 static rule layer를 구성했다.

- 정리해 둔 근거:
- 변경 단위: `src/static_type_checking/checker.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`
- 검증 신호: checker helper가 rule별 판단 이동을 함수 수준으로 보존한다.
- 새로 배운 것: 정적 검사기의 핵심은 값을 구하는 일이 아니라 표현식에 대한 약속을 미리 위반 여부로 바꾸는 것이었다.

### 코드 앵커 — `check_expression` (`src/static_type_checking/checker.py:41`)

```python
def check_expression(expr: Expr, environment: TypeEnvironment | None = None) -> TypeExpr:
    env = environment or TypeEnvironment()
    if isinstance(expr, IntegerLiteral):
        return IntType()
    if isinstance(expr, BooleanLiteral):
        return BoolType()
    if isinstance(expr, Identifier):
        return env.lookup(expr.name, expr.line, expr.column)
    if isinstance(expr, UnaryOp):
        operand_type = check_expression(expr.operand, env)
        if expr.operator == "-":
            _expect_exact_type(operand_type, IntType(), expr.line, expr.column, "operator - requires Int operand")
```

이 조각은 checker helper가 rule별 판단 이동을 함수 수준으로 보존한다는 설명이 실제로 어디서 나오는지 보여 준다. `check_expression`를 읽고 나면 다음 장면이 왜 demo program과 pytest로 static/runtime 경계를 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `_expect_exact_type` (`src/static_type_checking/checker.py:170`)

```python
def _expect_exact_type(actual: TypeExpr, expected: TypeExpr, line: int, column: int, message: str) -> None:
    if actual != expected:
        raise TypeDiagnosticError(Diagnostic(message, line, column))
```

이 조각은 checker helper가 rule별 판단 이동을 함수 수준으로 보존한다는 설명이 실제로 어디서 나오는지 보여 준다. `_expect_exact_type`를 읽고 나면 다음 장면이 왜 demo program과 pytest로 static/runtime 경계를 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 demo program과 pytest로 static/runtime 경계를 닫는다.

## 3. Phase 3 - demo와 pytest로 static/runtime 경계를 보여 준다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 type checker는 통과 프로그램과 실패 프로그램을 함께 보여 줄 때 가장 설명력이 크다.

그때 세운 가설은 CLI demo와 pytest가 있으면 '어떤 오류를 미리 자르는가'를 한 번에 재현할 수 있다고 봤다. 실제 조치는 `--demo all`과 tests를 통해 higher-order, branching, let inference 케이스를 반복 확인하게 만들었다.

- 정리해 둔 근거:
- 변경 단위: `tests/test_static_type_checking.py`, `src/static_type_checking/__main__.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`
- 검증 신호: pytest와 demo output이 마지막 검증 신호를 남긴다.
- 새로 배운 것: 정적 의미론은 긴 이론 설명보다 실제 진단 메시지가 남아 있을 때 더 빨리 이해됐다.

### 코드 앵커 — `main` (`src/static_type_checking/__main__.py:10`)

```python
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the shared PL foundations language before runtime.")
    parser.add_argument("--program", type=Path, help="path to a .plf source file")
    parser.add_argument("--demo", help="demo name or 'all'")
    args = parser.parse_args(argv)
```

이 조각은 pytest와 demo output이 마지막 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `main`를 읽고 나면 다음 장면이 왜 shared parser -> type environment -> diagnostic demo 순서로 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `test_accepts_higher_order_program` (`tests/test_static_type_checking.py:20`)

```python
def test_accepts_higher_order_program():
    source = """
    let compose: ((Int -> Int), (Int -> Int)) -> Int -> Int =
      fun (f: Int -> Int, g: Int -> Int) -> Int -> Int =>
        fun (x: Int) -> Int => f(g(x))
    in
    let inc = fun (n: Int) -> Int => n + 1 in
    let twice = compose(inc, inc) in
    twice(10)
    """
    assert format_type(check_source(source)) == "Int"
```

이 조각은 pytest와 demo output이 마지막 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `test_accepts_higher_order_program`를 읽고 나면 다음 장면이 왜 shared parser -> type environment -> diagnostic demo 순서로 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 shared parser -> type environment -> diagnostic demo 순서로 닫는다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Programming-Languages-Foundations/static-type-checking && python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all)
```

```text
if flag then
      1
    else
      2
in
choose(false)
-- type --
Int
```
