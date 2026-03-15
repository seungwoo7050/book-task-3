# parser-interpreter 문제지

## 왜 중요한가

이 문서는 parser-interpreter 프로젝트에서 무엇을 구현해야 하는지를 현재 기준으로 다시 설명합니다. 외부 starter artifact 없이 이 문서 자체가 요구사항 원본 역할을 합니다.

## 목표

시작 위치의 구현을 완성해 정수/불리언 literal, identifier, let, if, fun, call을 포함한 expression-oriented 언어를 파싱해야 합니다, unary -, not, binary arithmetic/comparison/logical operator의 precedence와 associativity를 안정적으로 처리해야 합니다, lexical closure와 eager evaluation을 지원하는 tree-walk interpreter가 필요합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/__init__.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/__main__.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/ast.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/diagnostics.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/tests/conftest.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/tests/test_parser_interpreter.py`
- `../study/Programming-Languages-Foundations/parser-interpreter/pyproject.toml`

## starter code / 입력 계약

- `../study/Programming-Languages-Foundations/parser-interpreter/src/parser_interpreter/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 정수/불리언 literal, identifier, let, if, fun, call을 포함한 expression-oriented 언어를 파싱해야 합니다.
- unary -, not, binary arithmetic/comparison/logical operator의 precedence와 associativity를 안정적으로 처리해야 합니다.
- lexical closure와 eager evaluation을 지원하는 tree-walk interpreter가 필요합니다.
- type annotation 문법을 파싱하되, 이 단계에서는 실행 의미에 사용하지 않아야 합니다.

## 제외 범위

- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `_print_summary`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_lexer_tokenizes_keywords_and_type_arrows`와 `test_parser_golden_for_let_if_call_and_annotations`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd cs-core/study/Programming-Languages-Foundations/parser-interpreter && python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all`가 통과한다.

## 검증 방법

```bash
cd cs-core/study/Programming-Languages-Foundations/parser-interpreter && python3 -m pytest && PYTHONPATH=src python3 -m parser_interpreter --demo all
```

```bash
cd /Users/woopinbell/work/book-task-3/cs-core/study/Programming-Languages-Foundations/parser-interpreter && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`parser-interpreter_answer.md`](parser-interpreter_answer.md)에서 확인한다.
