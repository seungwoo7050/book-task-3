# 개념 문서 안내

이 디렉터리는 `parser-interpreter`를 읽을 때 구현보다 먼저 맞춰 두면 좋은 핵심 개념을 짧게 정리한 공간입니다.

## 먼저 읽을 개념 메모

- [`concepts/lexer-and-token-stream.md`](concepts/lexer-and-token-stream.md): 문자를 token stream으로 나누는 기준과 keyword 처리 방식을 설명합니다.
- [`concepts/recursive-descent-and-precedence.md`](concepts/recursive-descent-and-precedence.md): special form과 infix operator를 어떻게 분리해 파싱하는지 정리합니다.
- [`concepts/environment-and-closures.md`](concepts/environment-and-closures.md): lexical scope, closure, short-circuit evaluation을 runtime 관점에서 묶어 설명합니다.

## 추천 읽기 순서

1. lexer 메모로 token kind와 문법 표면을 먼저 맞춥니다.
2. precedence 메모로 parser가 어떤 구조를 가져야 하는지 확인합니다.
3. closure 메모로 evaluator가 어떤 상태를 유지해야 하는지 읽습니다.
4. [`references/README.md`](references/README.md)로 provenance와 외부 참고 자료를 확인합니다.

## 구현과 연결되는 파일

- `../src/parser_interpreter/lexer.py`
- `../src/parser_interpreter/parser.py`
- `../src/parser_interpreter/evaluator.py`
- `../tests/test_parser_interpreter.py`
