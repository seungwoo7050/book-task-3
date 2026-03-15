# parser-interpreter 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 정수/불리언 literal, identifier, let, if, fun, call을 포함한 expression-oriented 언어를 파싱해야 합니다, unary -, not, binary arithmetic/comparison/logical operator의 precedence와 associativity를 안정적으로 처리해야 합니다, lexical closure와 eager evaluation을 지원하는 tree-walk interpreter가 필요합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `main`와 `_print_summary`, `_load_demo_sources` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 정수/불리언 literal, identifier, let, if, fun, call을 포함한 expression-oriented 언어를 파싱해야 합니다.
- unary -, not, binary arithmetic/comparison/logical operator의 precedence와 associativity를 안정적으로 처리해야 합니다.
- lexical closure와 eager evaluation을 지원하는 tree-walk interpreter가 필요합니다.
- 첫 진입점은 `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/__init__.py`이고, 여기서 `main`와 `_print_summary` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/__main__.py`: CLI나 demo 실행 순서를 묶는 진입점 파일이다.
- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/ast.py`: `TypeExpr`, `IntType`, `BoolType`, `FunctionType`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/diagnostics.py`: `Diagnostic`, `ParserInterpreterError`, `SyntaxDiagnosticError`, `RuntimeDiagnosticError`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/environment.py`: `Environment`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Programming-Languages-Foundations/parser-interpreter/tests/conftest.py`: pytest fixture와 테스트 환경 구성을 고정하는 파일이다.
- `../study/Programming-Languages-Foundations/parser-interpreter/tests/test_parser_interpreter.py`: `test_lexer_tokenizes_keywords_and_type_arrows`, `test_parser_golden_for_let_if_call_and_annotations`, `test_operator_precedence_and_left_associativity`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Programming-Languages-Foundations/parser-interpreter/pyproject.toml`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `test_lexer_tokenizes_keywords_and_type_arrows` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd cs-core/study/Programming-Languages-Foundations/parser-interpreter && python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd cs-core/study/Programming-Languages-Foundations/parser-interpreter && python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all
```

```bash
cd /Users/woopinbell/work/book-task-3/cs-core/study/Programming-Languages-Foundations/parser-interpreter && PYTHONPATH=src python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `test_lexer_tokenizes_keywords_and_type_arrows`와 `test_parser_golden_for_let_if_call_and_annotations`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd cs-core/study/Programming-Languages-Foundations/parser-interpreter && python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/__init__.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/__main__.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/ast.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/diagnostics.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/environment.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/tests/conftest.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/tests/test_parser_interpreter.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/pyproject.toml`
