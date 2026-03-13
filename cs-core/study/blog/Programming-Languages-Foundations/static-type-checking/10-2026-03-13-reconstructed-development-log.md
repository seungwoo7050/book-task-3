# Static Type Checking 재구성 개발 로그

`static-type-checking`은 같은 toy language를 다시 파싱한 뒤 runtime에 넘기기 전에 어떤 오류를 미리 거를 수 있는지 정리하는 프로젝트다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

parser surface를 유지한 채 type environment와 checker를 얹고, runtime 전에 어떤 오류를 끊어낼 수 있는지 demo로 닫는 흐름을 복원한다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: 같은 언어 표면을 다시 파싱 가능한 AST로 유지한다 — `src/static_type_checking/parser.py`, `src/static_type_checking/ast.py`
- Phase 2: type environment와 rule checking을 별도 층으로 만든다 — `src/static_type_checking/checker.py`
- Phase 3: demo와 pytest로 static/runtime 경계를 보여 준다 — `tests/test_static_type_checking.py`, `src/static_type_checking/__main__.py`

## Phase 1. 같은 언어 표면을 다시 파싱 가능한 AST로 유지한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 type checker도 parser가 달라지면 앞 프로젝트와 연결 고리가 끊어진다.

처음에는 새 프로젝트지만 parser surface는 최대한 유지하고 type annotation 해석만 덧붙이는 편이 학습 연결이 좋다고 봤다. 그런데 실제로 글의 중심이 된 조치는 parser/AST를 공유 가능한 형태로 다시 세우고, checker가 기대할 입력 표면을 유지했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `src/static_type_checking/parser.py`, `src/static_type_checking/ast.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`
- 검증 신호: shared syntax가 있으니 parser-interpreter와 대비되는 지점이 선명해진다.

### 이 장면을 고정하는 코드 — `parse_source` (`src/static_type_checking/parser.py:230`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

```python
def parse_source(source: str) -> Expr:
    return Parser(tokenize_source(source)).parse()
```

`parse_source`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 정적 의미론을 추가할 때도 먼저 지켜야 할 것은 기존 언어 표면과의 연속성이었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 type environment와 rule checking으로 이동한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 정적 의미론을 추가할 때도 먼저 지켜야 할 것은 기존 언어 표면과의 연속성이었다.

그래서 다음 장면에서는 type environment와 rule checking으로 이동한다.

## Phase 2. type environment와 rule checking을 별도 층으로 만든다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 `check_expression`, `_expect_exact_type`, function type helper가 이 프로젝트의 핵심 전환점이다.

처음에는 runtime evaluator처럼 값을 계산하기보다 environment에 타입을 축적하는 규칙을 따로 세워야 오류를 미리 잡을 수 있다고 판단했다. 그런데 실제로 글의 중심이 된 조치는 type environment, exact-type assertion, function application rule을 checker에 모아 static rule layer를 구성했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `src/static_type_checking/checker.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`
- 검증 신호: checker helper가 rule별 판단 이동을 함수 수준으로 보존한다.

### 이 장면을 고정하는 코드 — `check_expression` (`src/static_type_checking/checker.py:41`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

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

`check_expression`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 정적 검사기의 핵심은 값을 구하는 일이 아니라 표현식에 대한 약속을 미리 위반 여부로 바꾸는 것이었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 demo program과 pytest로 static/runtime 경계를 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 정적 검사기의 핵심은 값을 구하는 일이 아니라 표현식에 대한 약속을 미리 위반 여부로 바꾸는 것이었다.

그래서 다음 장면에서는 demo program과 pytest로 static/runtime 경계를 닫는다.

## Phase 3. demo와 pytest로 static/runtime 경계를 보여 준다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 type checker는 통과 프로그램과 실패 프로그램을 함께 보여 줄 때 가장 설명력이 크다.

처음에는 CLI demo와 pytest가 있으면 '어떤 오류를 미리 자르는가'를 한 번에 재현할 수 있다고 봤다. 그런데 실제로 글의 중심이 된 조치는 `--demo all`과 tests를 통해 higher-order, branching, let inference 케이스를 반복 확인하게 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `tests/test_static_type_checking.py`, `src/static_type_checking/__main__.py`
- CLI: `python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`
- 검증 신호: pytest와 demo output이 마지막 검증 신호를 남긴다.

### 이 장면을 고정하는 코드 — `main` (`src/static_type_checking/__main__.py:10`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```python
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the shared PL foundations language before runtime.")
    parser.add_argument("--program", type=Path, help="path to a .plf source file")
    parser.add_argument("--demo", help="demo name or 'all'")
    args = parser.parse_args(argv)
```

`main`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 정적 의미론은 긴 이론 설명보다 실제 진단 메시지가 남아 있을 때 더 빨리 이해됐다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 shared parser -> type environment -> diagnostic demo 순서로 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 정적 의미론은 긴 이론 설명보다 실제 진단 메시지가 남아 있을 때 더 빨리 이해됐다.

그래서 다음 장면에서는 shared parser -> type environment -> diagnostic demo 순서로 닫는다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

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

## 이번에 남은 질문

- 개념 축: `function type checking`, `static vs runtime errors`, `type environment`
- 대표 테스트/fixture: `tests/conftest.py`, `tests/test_static_type_checking.py`
- 다음 질문: 최종 글은 shared parser -> type environment -> diagnostic demo 순서로 닫는다.
