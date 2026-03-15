# static-type-checking 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 parser-interpreter와 같은 문법을 다시 파싱해야 합니다, arithmetic/comparison/logical operator의 operand type을 실행 전에 확인해야 합니다, if condition, then/else branch, function call, function return을 static rule로 검증해야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `main`와 `_print_summary`, `_load_demo_sources` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- parser-interpreter와 같은 문법을 다시 파싱해야 합니다.
- arithmetic/comparison/logical operator의 operand type을 실행 전에 확인해야 합니다.
- if condition, then/else branch, function call, function return을 static rule로 검증해야 합니다.
- 첫 진입점은 `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/__init__.py`이고, 여기서 `main`와 `_print_summary` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/__main__.py`: CLI나 demo 실행 순서를 묶는 진입점 파일이다.
- `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/ast.py`: `TypeExpr`, `IntType`, `BoolType`, `FunctionType`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/checker.py`: `TypeEnvironment`, `check_expression`, `check_source`, `_expect_exact_type`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/diagnostics.py`: `Diagnostic`, `StaticTypeCheckingError`, `SyntaxDiagnosticError`, `TypeDiagnosticError`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Programming-Languages-Foundations/static-type-checking/tests/conftest.py`: pytest fixture와 테스트 환경 구성을 고정하는 파일이다.
- `../study/Programming-Languages-Foundations/static-type-checking/tests/test_static_type_checking.py`: `test_lexer_keeps_type_tokens`, `test_accepts_higher_order_program`, `test_accepts_if_and_let_inference`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Programming-Languages-Foundations/static-type-checking/pyproject.toml`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `test_lexer_keeps_type_tokens` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd cs-core/study/Programming-Languages-Foundations/static-type-checking && python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd cs-core/study/Programming-Languages-Foundations/static-type-checking && python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all
```

```bash
cd /Users/woopinbell/work/book-task-3/cs-core/study/Programming-Languages-Foundations/static-type-checking && PYTHONPATH=src python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `test_lexer_keeps_type_tokens`와 `test_accepts_higher_order_program`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd cs-core/study/Programming-Languages-Foundations/static-type-checking && python3 -m pytest && PYTHONPATH=src python3 -m static_type_checking --demo all`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/__init__.py`
- `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/__main__.py`
- `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/ast.py`
- `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/checker.py`
- `../study/Programming-Languages-Foundations/static-type-checking/src/static_type_checking/diagnostics.py`
- `../study/Programming-Languages-Foundations/static-type-checking/tests/conftest.py`
- `../study/Programming-Languages-Foundations/static-type-checking/tests/test_static_type_checking.py`
- `../study/Programming-Languages-Foundations/static-type-checking/pyproject.toml`
